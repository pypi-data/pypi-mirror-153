# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import json
import os
from os import name as os_name
import re
import shlex
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Union, List
from urllib.parse import quote

from azureml.core import Dataset
from azureml.data.datapath import DataPath
from azureml.data.data_reference import DataReference
from azureml.data.dataset_consumption_config import DatasetConsumptionConfig
from azureml.data import FileDataset
from azureml.exceptions._azureml_exception import UserErrorException
from azure.ml.component._util._utils import _get_short_path_name, print_to_terminal, _get_parameter_static_value
from azure.ml.component._util._loggerfactory import track
from .._util._exceptions import ComponentValidationError
from .._core._component_definition import ComponentType, CommandComponentDefinition, \
    ParallelComponentDefinition, DistributedComponentDefinition
from .._core._launcher_definition import LauncherType
from .._pipeline_parameters import PipelineParameter
from .._parameter_assignment import _ParameterAssignment
from ._constants import OUTPUT_DIR_NAME, WINDOWS_CONTAINER_INPUT_PATH, LINUX_CONTAINER_INPUT_PATH, \
    LINUX_CONTAINER_OUTPUT_PATH, WINDOWS_CONTAINER_OUTPUT_PATH, LINUX_CONTAINER_MOUNT_SCRIPTS_PATH, \
    WINDOWS_CONTAINER_MOUNT_SCRIPTS_PATH, MOCK_PARALLEL_DRIVER, RUN_PREPARE_LOG, \
    COMMAND_DRIVER, LINUX_CONTAINER_MOUNT_PATH, WINDOWS_CONTAINER_MOUNT_PATH


class CommandExecutionBuilder:
    """Help to build component execution."""

    def __init__(self, component, working_dir, snapshot_path, tracker, logger, component_env):
        self.component = component
        self.working_dir = working_dir
        self.tracker = tracker
        self.logger = logger
        self.snapshot_path = snapshot_path
        self.component_env = component_env
        self.use_docker = self.component_env.image_name is not None
        # Component execution environment os type.
        self.is_windows = self.component_env.is_windows() if self.use_docker else os_name == 'nt'
        # Component command after replacing parameters.
        self.component_command = None
        # Command using command_driver to invoke component command.
        self.execution_command = None

    @track()
    def build(self):
        """Prepare command, environment and volumes to generate CommandExecution."""
        environment = {}
        cwd = self.snapshot_path

        # Generate command
        run_command = ComponentRunCommand(self.component, self.working_dir, self.is_windows)
        # Generate component command after replacing params.
        self.component_command, volumes = run_command.generate_command(use_docker=self.use_docker)

        # Generate component execution command using command_driver to invoke component command.
        self.execution_command = self._trans_component_command_to_execution_command(self.component_command, volumes)

        # For metric needed environment variables
        if self.tracker.track_run_history:
            environment.update(self._set_environment_variables_for_run())
        # Update environment in runsettings
        runsettings = self.component_env.component.runsettings
        # When runsetting without workspace, hasattr will call __getattribute__ to generate the attribute.
        # Use _has_param to check whether environment_variables exists.
        if runsettings._has_param('environment_variables'):
            if runsettings.environment_variables is not None:
                env_vars = runsettings.environment_variables
                if not isinstance(env_vars, str):
                    env_vars = json.dumps(env_vars)
                # Reload to json dict
                environment.update(json.loads(env_vars))
        if self.component_env.image_name is not None:
            # Add scripts in volumes
            cwd = WINDOWS_CONTAINER_MOUNT_SCRIPTS_PATH if self.component_env.is_windows() \
                else LINUX_CONTAINER_MOUNT_SCRIPTS_PATH
            volumes[self.snapshot_path] = {'bind': cwd, 'mode': 'rw'}

        # To avoid checking docker status leads to longer import time.
        from ._command_execution import CommandExecution
        return CommandExecution(
            command=self.execution_command,
            environment_variables=environment,
            cwd=cwd,
            logger=self.logger,
            command_environment=self.component_env,
            volumes=volumes)

    def _set_environment_variables_for_run(self):
        run = self.tracker.get_run()
        env = {
            'AZUREML_RUN_ID': run.id,
            'AZUREML_ARM_SUBSCRIPTION': run.experiment.workspace.subscription_id,
            'AZUREML_ARM_RESOURCEGROUP': run.experiment.workspace.resource_group,
            'AZUREML_ARM_WORKSPACE_NAME': run.experiment.workspace.name,
            'AZUREML_ARM_PROJECT_NAME': run.experiment.name,
            'AZUREML_RUN_TOKEN': run._client.run.get_token().token,
            'AZUREML_WORKSPACE_ID': run.experiment.workspace._workspace_id,
            'AZUREML_SERVICE_ENDPOINT': run._client.run.get_cluster_url(),
            'AZUREML_DISCOVERY_SERVICE_ENDPOINT': run.experiment.workspace.discovery_url,
        }
        return env

    def _trans_component_command_to_execution_command(self, command, volumes):
        """
        Translate component command to execution command, using _command_driver to invoke component command
        and add _command_driver to volumes.

        :param command: Component command after replacing parameters.
        :type command: str or list[str]
        :param volumes: Volumes of inputs.
        :type volumes: Dict{(str, Dict)}
        """
        # Get command_driver path
        command_driver_path, command_driver_volume = self._get_command_driver_path()
        volumes.update(command_driver_volume)

        # Generater execution command, using command_driver to invoke component command.
        execution_command = self._generate_command_driver_command(command, command_driver_path)
        if self.component.type == ComponentType.DistributedComponent.value:
            if self.component._definition.launcher.type == LauncherType.MPI:
                # Add mpi command in component execution command
                execution_command = translate_mpi_command_by_component(execution_command,
                                                                       self.component, self.is_windows)
            else:
                msg = "Launcher type %r of distributed component is not supported." % self.component.launcher.type
                raise NotImplementedError(msg)
        return execution_command

    def _generate_command_driver_command(self, command, command_driver_path):
        """
        Generate command using command_driver to invoke component command.

        :param command: Component command after replacing parameters.
        :type command: str or list[str]
        :param command_driver_path: Path of command driver in execution environment.
        :type command_driver_path: str
        """
        # Encode command and generate execution command.
        if isinstance(command, list):
            str_command = ' '.join([quote(item) for item in command])
        else:
            str_command = quote(command)

        execute_command = [
            'python', command_driver_path,
            '--successful_return_code', self.component._definition.successful_return_code,
            '--command', str_command,
            '--is_command', str(self.component._definition.is_command)]
        return execute_command

    def _get_command_driver_path(self):
        """
        Get command_driver script path in execution environment.

        :return command_driver_path: Path of command_driver.py in execution environment.
                command_driver_volume: Volume of command_driver.py.
        :rtype str, Dict{(str, Dict)}
        """
        command_driver_path = Path(__file__).parent / COMMAND_DRIVER
        command_driver_volume = {}
        if self.use_docker:
            # Mount _command_driver.py to container. Because unable to map files into Windows container,
            # it will mount the folder where _command_driver.py is located to the container.
            folder_path_in_container = (LINUX_CONTAINER_MOUNT_PATH if not self.is_windows else
                                        WINDOWS_CONTAINER_MOUNT_PATH) + command_driver_path.parent.name
            command_driver_volume[str(command_driver_path.parent)] = {'bind': folder_path_in_container, 'mode': 'rw'}
            command_driver_path = (PurePosixPath(folder_path_in_container) if not self.is_windows
                                   else PureWindowsPath(folder_path_in_container)) / COMMAND_DRIVER
        return str(command_driver_path), command_driver_volume


class ComponentRunCommand:
    """Generate component run command"""

    OPTIONAL_PATTERN = re.compile(r"(\[([^\[\]]+?)\])")
    INPUT_PATTERN = re.compile(r"(\{inputs.(\S+?)\})")
    OUTPUT_PATTERN = re.compile(r"(\{outputs.(\S+?)\})")

    def __init__(self, component, working_dir, is_windows=False):
        self.component = component
        self.working_dir = working_dir
        self.is_windows = is_windows

    def generate_command(self, use_docker, check_data_exist=True, container_input_prefix=None,
                         container_output_prefix=None, remove_none_value=True):
        """
        Generate component run command.

        :param use_docker: Use docker.
        :type use_docker: bool
        :param check_data_exist: If check_data_exist=True, when input not exists raise error.
        :type check_data_exist: bool
        :param container_input_prefix: container input prefix
        :type container_input_prefix: str
        :param container_output_prefix: container output prefix
        :type container_output_prefix: str
        :param remove_none_value: whether remove None in command
        :type remove_none_value: bool
        :return input_path: Dict of input name and input path
                volumes: volumes of outputs
        :rtype Dict{(str, str)}, Dict{(str, Dict)}
        """
        input_path, input_volumes = self.generate_inputs(use_docker, check_data_exist, container_input_prefix)
        output_path, output_volumes = self.generate_outputs(use_docker, check_data_exist, container_output_prefix)
        input_volumes.update(output_volumes)

        # Get component inputs
        inputs = {k: input_path.get(k) for k in self.component._definition.inputs}
        params = {k: self.component._parameter_params.get(k) for k in self.component._definition.parameters}
        inputs.update(params)
        # Generate component command after replacing parameters.
        component_command = self.generate_component_command(self.component._definition, inputs, output_path)
        return component_command, input_volumes

    def generate_inputs(self, use_docker, check_data_exist=True, container_input_prefix=None):
        """
        If use_docker=True, generate input path and volumes of container, else generate input path in local.

        :param use_docker: Use docker.
        :type use_docker: bool
        :param check_data_exist: If check_data_exist=True, when input not exists raise error.
        :type check_data_exist: bool
        :param container_input_prefix: container input prefix
        :type container_input_prefix: str
        :return input_path: Dict of input name and input path
                volumes: volumes of outputs
        :rtype Dict{(str, str)}, Dict{(str, Dict)}
        """
        # In order to get the file path format that matches the os type
        if container_input_prefix is None:
            container_input_prefix = WINDOWS_CONTAINER_INPUT_PATH if self.is_windows \
                else LINUX_CONTAINER_INPUT_PATH
        container_input_prefix = PureWindowsPath(container_input_prefix) if self.is_windows \
            else PurePosixPath(container_input_prefix)
        input_path = {}
        volumes = {}
        for input_name, input_item in self.component._input_ports.items():
            input_is_optional = self.component._input_is_optional(input_name)
            if isinstance(input_item._dset, str) or isinstance(input_item._dset, Path):
                # Change to absolute path to avoid relative import error when running locally
                input_item_path = Path(input_item._dset).resolve().absolute()
                input_data_type = self.component._definition.inputs[input_name].type
                short_input_item_path = Path(
                    _get_short_path_name(input_item_path, is_dir=(['AnyFile'] == input_data_type)))
                if ['AnyFile'] == input_data_type:
                    if not short_input_item_path.is_file():
                        short_input_item_path = next(
                            filter(lambda item: item.is_file(), short_input_item_path.iterdir()), None)
                if not check_data_exist or short_input_item_path.exists():
                    if use_docker:
                        if str(short_input_item_path) in volumes:
                            input_port_path = volumes[str(short_input_item_path)]['bind']
                        else:
                            input_port_path = container_input_prefix / os.path.basename(input_name)
                            volumes[str(short_input_item_path)] = {'bind': str(input_port_path), 'mode': 'ro'}
                    else:
                        input_port_path = str(short_input_item_path)
                    input_path[input_name] = str(input_port_path)
                else:
                    if check_data_exist and not input_is_optional:
                        raise UserErrorException(
                            'Local input port path for "{}" does not exist, path: {}'.format(input_name,
                                                                                             input_item._dset))
            else:
                if not input_is_optional:
                    raise UserErrorException('Input port "{}" not set'.format(input_name))
        return input_path, volumes

    def generate_outputs(self, use_docker, check_data_exist=True, container_output_prefix=None):
        """
        If use_docker=True, generate output path and volumes of container, else generate output path in local.

        :param use_docker: Use docker.
        :type use_docker: bool
        :param check_data_exist: If check_data_exist=True, create output folder.
        :type check_data_exist: bool
        :param container_output_prefix: container output prefix
        :type container_output_prefix: str
        :return output_portname_container_path: Dict of output name and output path
                volumes: volumes of outputs
        :rtype Dict{(str, str)}, Dict{(str, Dict)}
        """
        # Prepare output path
        default_output_path = Path(self.working_dir) / OUTPUT_DIR_NAME
        local_output_path = self.generate_outputs_in_local(self.component, default_output_path)
        output_portname_container_path, volumes = self.generate_outputs_in_docker(
            default_output_path=default_output_path, container_output_prefix=container_output_prefix,
        ) if use_docker else (local_output_path, {})

        # Ensure local output path
        default_output_path.mkdir(parents=True, exist_ok=True)
        if check_data_exist:
            for output_port_name, path in local_output_path.items():
                try:
                    if self.component._output_is_file(output_port_name):
                        Path(path).touch(exist_ok=True)
                    else:
                        Path(path).mkdir(parents=True, exist_ok=True)
                except Exception as e:
                    raise UserErrorException(f"Raise exception when generate output for {output_port_name}, {e}")
        return output_portname_container_path, volumes

    @staticmethod
    def generate_outputs_in_local(component, default_output_path):
        return {
            output_port_name: os.path.join(str(default_output_path), output_port_name)
            if value._path_on_compute is None else str(value._path_on_compute)
            for output_port_name, value in component.outputs.items()
        }

    def generate_outputs_in_docker(self, default_output_path, container_output_prefix=None):
        # In order to get the file path format that matches the os type
        if container_output_prefix is None:
            container_output_prefix = WINDOWS_CONTAINER_OUTPUT_PATH if self.is_windows \
                else LINUX_CONTAINER_OUTPUT_PATH
        container_output_prefix = PureWindowsPath(container_output_prefix) if \
            self.is_windows else PurePosixPath(container_output_prefix)

        default_container_output_prefix = container_output_prefix / 'default'
        volumes = {str(default_output_path): {'bind': str(default_container_output_prefix), 'mode': 'rw'}}
        output_portname_container_path = {}
        for output_port_name, value in self.component.outputs.items():
            # For the output which has set path, we mount to the specific path.
            if value._path_on_compute:
                if self.component._output_is_file(output_port_name):
                    raise UserErrorException(
                        "Configure path for a file output is not supported when running in docker."
                    )
                output_port_path = container_output_prefix / output_port_name
                volumes[str(value._path_on_compute)] = {'bind': str(output_port_path), 'mode': 'rw'}
            # Otherwise we use the default path in mounted default folder.
            else:
                output_port_path = default_container_output_prefix / output_port_name
            output_portname_container_path[output_port_name] = str(output_port_path)
        return output_portname_container_path, volumes

    @classmethod
    def replace_command(cls, command_string, inputs=None, outputs=None) -> str:
        """Replace a command string which contains placeholders like {inputs.xx} {outputs.xx}

        :param command_string: The input command string, e.g. "--input {input.i} --output {output.o}"
        :param inputs: The replacement values of inputs.
        :param outputs: The replacement values of outputs.
        :return: The replaced command string.
        """
        inputs = inputs or {}
        outputs = outputs or {}
        replacements = {}
        for input_part, input_name in cls.INPUT_PATTERN.findall(command_string):
            result = inputs.get(input_name)
            if result is None:
                raise ComponentValidationError(
                    "Required input %r is not provided." % input_name,
                    None, ComponentValidationError.MISSING_INPUT
                )
            replacements[input_part] = str(result)
        for output_part, output_name in cls.OUTPUT_PATTERN.findall(command_string):
            result = outputs.get(output_name)
            if result is None:
                raise ComponentValidationError(
                    "Output %r is not provided." % output_name, None, ComponentValidationError.MISSING_PARAMETER
                )
            replacements[output_part] = str(result)
        for k, v in replacements.items():
            command_string = command_string.replace(k, v)
        return command_string

    @classmethod
    def resolve_command(cls, command, inputs=None, outputs=None, split=False) -> Union[str, List[str]]:
        """Resolve the command according to the command, inputs and the outputs.

        :param command: The command string includeing the patterns {inputs.xx} and {outputs.xx} to be resolved.
        :param inputs: A dict from input names to values. Note that an optional input which is not set should also be
                       in the dict with the value None, otherwise a KeyError will be raised.
        :param outputs: A dict from output names to values.
        :param split: If split is True, the return result is a list of replaced string, split by shlex.split,
            otherwise it is a replaced command string.
        :return: The replaced command string or the replaced command list.
        """
        # If provided command has no value (maybe None or ''), return empty list or an empty string.
        if not command:
            return [] if split else ''
        # Resolve optional parameters/inputs to update the command
        inputs, outputs = inputs or {}, outputs or {}
        for optional_part, optional_value in cls.OPTIONAL_PATTERN.findall(command):
            match = cls.INPUT_PATTERN.search(optional_value)
            if not match:
                # If no matching value, we consider the optional string has value
                # This is for some special cases like "python [--arg1 val1]"
                command = command.replace(optional_part, optional_part[1:-1])
                continue
            input_name = match.group(2)
            if input_name not in inputs:
                raise KeyError("Optional input %r is not an input or a parameter of the component." % input_name)
            input_val = inputs[input_name]
            replacement = '' if input_val is None else optional_value
            command = command.replace(optional_part, replacement)

        # If split is required, shlex.split first, then replace
        # Otherwise directly replace the whole string
        return [cls.replace_command(command_item, inputs, outputs) for command_item in shlex.split(command)] \
            if split else cls.replace_command(command, inputs, outputs)

    @classmethod
    def generate_component_command(
        cls,
        definition: Union[CommandComponentDefinition, DistributedComponentDefinition, ParallelComponentDefinition],
        inputs=None, outputs=None,
    ):
        if definition.type in {ComponentType.CommandComponent, ComponentType.DistributedComponent}:
            command_in_def = definition.command
            if definition.type == ComponentType.DistributedComponent:
                command_in_def = definition.launcher.additional_arguments
            if command_in_def is None:  # A component loaded from a yaml may forget command field.
                raise NotImplementedError("The component doesn't have a command.")
            # For AnyCommand, we directly replace inputs/outputs and return the command string for shell.
            # This is to align the behavior of context_injector_manager.py in remote run.
            if definition.is_command:
                return cls.resolve_command(command_in_def, inputs, outputs, split=False)
            else:
                command = cls.resolve_command(command_in_def, inputs, outputs, split=True)
                return command
        elif definition.type == ComponentType.ParallelComponent:
            return cls.generate_parallel_command(definition, inputs, outputs)
        else:
            msg = "Generating command for component type %r is not supported." % definition.type.value
            raise NotImplementedError(msg)

    @classmethod
    def generate_parallel_command(
        cls, definition: ParallelComponentDefinition, inputs=None, outputs=None,
    ):
        if not isinstance(definition, ParallelComponentDefinition):
            raise TypeError("ParallelComponent is required, got %r." % type(definition))
        inputs, outputs = inputs or {}, outputs or {}

        # The following code is a hard code for running parallel components using the mock entry.
        command = ['python', MOCK_PARALLEL_DRIVER, '--scoring_module_name', definition.entry]
        input_index = 0
        for input_name in definition.input_data:
            if not inputs.get(input_name):
                if not definition.inputs[input_name].optional:
                    raise ComponentValidationError(
                        "Required input %r is not provided." % input_name,
                        None, ComponentValidationError.MISSING_INPUT
                    )
                continue
            command.extend(['--input_fds_%d' % input_index, inputs[input_name]])
            input_index += 1
        if definition.output_data:
            if definition.output_data not in outputs:
                raise ComponentValidationError(
                    "Output %r is not provided." % definition.output_data,
                    None, ComponentValidationError.MISSING_PARAMETER
                )
            command.extend(['--output', outputs[definition.output_data]])

        command += cls.resolve_command(definition.args, inputs, outputs, split=True)
        return command


def translate_mpi_command_by_component(command, component, is_windows):
    """Translate command of mpi component."""
    # Get process_count_per_node param from run settings, will be 1 if did not find
    process_count_per_node = component._get_run_setting('process_count_per_node', int, 1)
    mpi_cmd = ['mpiexec', '-n', str(process_count_per_node)]

    if not is_windows:
        # If executing in linux, will using root to execute mpi command, need to add --allow-run-as-root in command.
        mpi_cmd.append('--allow-run-as-root')
    command[0:0] = mpi_cmd

    node_count = component._get_run_setting('node_count', int, 1)
    if node_count > 1:
        from ..dsl._utils import logger as dsl_logger
        dsl_logger.warning('Ignore [ %s ] setting node_count = %s, '
                           'component.run only supports executing node on single node' % (component.name, node_count))

    return command


def translate_parallel_command(command, port_arg_map):
    # In parallel component, input value is input_name, and input param name starts with '--input_fds'.
    # This function will translate input name to input path.
    # https://msdata.visualstudio.com/Vienna/_git/AzureMlCli?path=%2Fsrc%2Fazureml-parallel-run%2Fazureml_sys%2Fazureml_sys%2Fparallel_run%2Fjob_args.py&version=GBmaster
    for index, item in enumerate(command):
        if item.startswith('--input_fds_') and index + 1 < len(command) and \
                command[index + 1] in port_arg_map:
            command[index + 1] = port_arg_map[command[index + 1]]
    return command


class ComponentRunInput:
    """Replace input dataset of component to local dataset path."""

    def __init__(self, component, working_dir, pipeline_parameters={},
                 input_futures=None, component_execution_dict={}, workspace=None):
        self.component = component
        self.working_dir = working_dir
        self.pipeline_parameters = pipeline_parameters
        self.component_execution_dict = component_execution_dict
        self.workspace = workspace
        self.input_futures = input_futures

    @track()
    def get_component_run_inputs_path(self):
        """
        Get input_path of component.

        :return inputs_path: Dict of inputs_path in Component
        :rtype Dict{(str, object)}
        """
        inputs_path = {}
        for input_name, input_value in self.component._input_ports.items():
            inputs_path[input_name] = self._prepare_component_input(input_name, input_value._dset)
        return inputs_path

    def _prepare_component_input(self, input_name, dset):
        """
        Get component input path, if not exists in local will download it to working_dir.

        :param input_name: Input port name.
        :type input_name: str
        :param dset: Dataset
        :type dset: object
        :return inputs_path: input dataset path in local
        :rtype str
        """
        if self.input_futures and dset in self.input_futures:
            if not self.input_futures[dset].done():
                print_to_terminal('Download input dataset [ %s ] starting...\n' % input_name)
                print('%s: download input dataset [ %s ] starting...' % (RUN_PREPARE_LOG, input_name))
                self.input_futures[dset].result()
                print('%s: download input dataset [ %s ] completed...' % (RUN_PREPARE_LOG, input_name))
                print_to_terminal('Download input dataset [ %s ] completed...\n' % input_name)
            if Path(self.input_futures[dset].result()).exists():
                return self.input_futures[dset].result()
        # Download dataset and replace node inputs to local data path

        from ..component import Output, Input
        if isinstance(dset, Input):
            return self._prepare_component_input(input_name, dset._dset)
        if isinstance(dset, PipelineParameter):
            # Update dset value from pipeline parameter
            dset = _get_parameter_static_value(dset, self.pipeline_parameters)
        if isinstance(dset, Output):
            return self.component_execution_dict[dset._owner._id].outputs[dset._name]
        elif isinstance(dset, DataReference) or isinstance(dset, FileDataset) or \
                isinstance(dset, DataPath) or isinstance(dset, DatasetConsumptionConfig):
            return ComponentRunInput.download_input_data(
                workspace=self.workspace, dset=dset, working_dir=self.working_dir)
        elif isinstance(dset, (str, Path)) or not dset:
            return dset
        else:
            raise UserErrorException("Unknown type %s for node input dataset %s" % (type(dset), input_name))

    @staticmethod
    def download_input_data(workspace, dset, working_dir, is_download=True):
        """
        Download input dataset to working_dir.

        :param workspace: The workspace object this input dataset will belong to.
        :type workspace: azureml.core.Workspace
        :param dset: Dataset
        :type dset: object
        :param working_dir: Folder to store dataset
        :type working_dir: dict
        :param is_download: If is_download is true, will download dataset to working_dir,
                            else only return dataset download path
        :type is_download: bool
        :return dataset_path: Download dataset path
        :rtype str
        """
        # Download component input dataset to local
        if isinstance(dset, DataReference):
            path_on_data_store = dset.path_on_datastore
            target_path = Path(working_dir) / path_on_data_store
            if not is_download:
                return str(target_path)
            dset.datastore.download(
                target_path=working_dir, prefix=path_on_data_store, overwrite=True)
            if not target_path.exists():
                target_path.mkdir(parents=True)
            return str(target_path)
        elif isinstance(dset, FileDataset):
            dataset_id = dset.id
            dataset_name = dset.name
            target_path = Path(working_dir, dataset_name if dataset_name else dataset_id)
            if not is_download:
                return str(target_path)
            dataset = Dataset.get_by_id(workspace, dataset_id)
            dataset.download(target_path=str(target_path), overwrite=True)
            return str(target_path)
        elif isinstance(dset, DataPath):
            path_on_data_store = dset._path_on_datastore
            target_path = Path(working_dir) / path_on_data_store
            if not is_download:
                return str(target_path)
            dset._datastore.download(
                target_path=working_dir, prefix=path_on_data_store, overwrite=True)
            if not target_path.exists():
                target_path.mkdir(parents=True)
            return str(target_path)
        elif isinstance(dset, DatasetConsumptionConfig):
            return ComponentRunInput.download_input_data(workspace, dset.dataset, working_dir)
        elif isinstance(dset, str) or isinstance(dset, Path):
            # When generate command will check dset existence
            return dset
        else:
            raise UserErrorException('Input dataset is of unsupported type: {0}'.format(type(dset).__name__))


class ComponentRunParameter:

    def __init__(self, component, pipeline_parameters=None):
        self.component = component
        self.pipeline_parameters = pipeline_parameters

    @track()
    def get_component_run_parameters(self):
        """
        Get parameters of component.

        :return params_value: Dict of params in Component
        :rtype Dict{(str, object)}
        """
        params_value = {}
        for param_name, param_value in self.component._parameter_params.items():
            params_value[param_name] = self._get_component_parameter(param_name, param_value)
        return params_value

    def _get_component_parameter(self, param_name, param_value):
        """Get param value by param_name from component."""
        from ..component import Input
        if isinstance(param_value, PipelineParameter):
            return self._get_pipeline_param(param_name, param_value)
        elif isinstance(param_value, Input):
            return self._get_component_parameter(param_name, param_value._dset)
        elif isinstance(param_value, _ParameterAssignment):
            return param_value.get_value_with_pipeline_parameters(self.pipeline_parameters)
        else:
            return param_value

    def _get_pipeline_param(self, param_name, param_value):
        """Get param value from pipeline_params."""
        default_value = self.pipeline_parameters[param_value.name] if self.pipeline_parameters and \
            param_value.name in self.pipeline_parameters.keys() else param_value.default_value
        if isinstance(default_value, PipelineParameter):
            return self._get_pipeline_param(param_name, default_value)
        if isinstance(default_value, int) or isinstance(default_value, str) or \
                isinstance(default_value, bool) or isinstance(default_value, float):
            return default_value
        else:
            raise UserErrorException(
                'Node parameter {0} is of unsupported type: {1}'.format(param_name, type(default_value).__name__))
