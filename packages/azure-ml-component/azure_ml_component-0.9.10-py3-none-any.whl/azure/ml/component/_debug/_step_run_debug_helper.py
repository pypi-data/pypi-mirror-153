# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import logging
import os
import json
from threading import Thread
import uuid
import shutil
import base64
import zipfile
import tempfile
import subprocess
import re
import time
import shlex
import urllib.request
from pathlib import Path
from os import name as os_name

from azureml.core import Run, Dataset, RunConfiguration
from azureml.core.compute import ComputeTarget
from azureml._model_management._util import get_docker_client
from azureml._restclient.constants import RunStatus
from azureml._execution._commands import _get_content_from_uri
from azureml._base_sdk_common.common import to_camel_case
from azureml.core.datastore import Datastore
from azureml.exceptions import UserErrorException

from azure.ml.component._execution._component_snapshot import _download_snapshot, _extract_zip, \
    _mock_parallel_driver_file, MOCK_PARALLEL_DRIVER
from azure.ml.component._execution._command_execution_builder import translate_parallel_command
from azure.ml.component._restclients.service_caller import DesignerServiceCaller
from azure.ml.component._debug._constants import VSCODE_DIR, INPUT_DIR, LAUNCH_CONFIG, CONTAINER_DIR, \
    CONTAINER_CONFIG, SUBSCRIPTION_KEY, RESOURCE_GROUP_KEY, WORKSPACE_KEY, DEBUG_FOLDER, \
    DATA_REF_PREFIX, EXPERIMENT_KEY, RUN_KEY, ID_KEY
from azure.ml.component._debug._image import ImageBase
from azure.ml.component.dsl._utils import logger, _print_step_info
from azure.ml.component._util._utils import timeout, start_a_local_run
from azure.ml.component.dsl._constants import DATA_FOLDER
from azure.ml.component._core._component_definition import ComponentType
from azure.ml.component._core._launcher_definition import LauncherType
from azure.ml.component._util._loggerfactory import _LoggerFactory
from azureml._common.exceptions import AzureMLException
from azureml._base_sdk_common.field_info import _FieldInfo


TIMEOUT_SECONDS = 60 * 30
REQUEST_INTERVAL_SECONDS = 3
AZUREML_DATASET_PREFIX = '$AZUREML_DATAREFERENCE_'
AZUREML_OUTPUT_PREFIX = 'DatasetOutputConfig:'
AZUREML_PARAM_PREFIX = '$AZUREML_PARAMETER_'
AZUREML_SWEEP_PREFIX = '$AZUREML_SWEEP_'
AZUREML_TRANS_PREFIX = 'AZUREML_TRANS_DATA_PATH_'
ITP_COMPUTE_TYPE = ['Cmk8s', 'AmlK8s']
DISTRIBUTED_SCRIPT = 'mock_distributed_run.py'
SLEEP_COMMAND = 'sleep infinity && '
COMPUTE_DISABLED_SSH_ERR_MSG = "SSH is disabled in the compute %s, please use a compute support SSH to debug the " \
                               "run. You could use 'az ml computetarget create amlcompute --admin-user-ssh-key'" \
                               " to create a compute with SSH, for more details: https://docs.azure.cn/zh-cn/cli/" \
                               "ext/azure-cli-ml/ml/computetarget/create?view=azure-cli-latest#" \
                               "ext_azure_cli_ml_az_ml_computetarget_create_amlcompute"
_az_ml_logger = _LoggerFactory.get_logger("az-ml")


class DebugStepRunHelper:

    PARAM_PATTERN = re.compile('\\%s\\w*|\\%s\\w*' % (AZUREML_PARAM_PREFIX, AZUREML_SWEEP_PREFIX))
    DATA_PATTERN = re.compile('\\%s\\w*|%s\\w*' % (AZUREML_DATASET_PREFIX, AZUREML_OUTPUT_PREFIX))

    @staticmethod
    def installed_requirements():
        exc_map = {
            'docker': "https://www.docker.com/",
            'code': "https://code.visualstudio.com/Download"
        }
        _print_step_info(["Required {} can be installed here: {}".format(exc, url) for exc, url in exc_map.items()])

    @staticmethod
    def create_launch_config(step_name, python_path, commands, arguments, working_dir=''):
        default_config = {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "console": "integratedTerminal",
        }
        if '-m' in commands:
            default_config['module'] = commands[-1]
        else:
            default_config['program'] = commands[-1]
        default_config['args'] = arguments
        default_config['pythonPath'] = python_path
        # create python debug config
        with open(INPUT_DIR / LAUNCH_CONFIG) as container_config:
            data = json.load(container_config)
            data['configurations'].append(default_config)
            os.makedirs(VSCODE_DIR, exist_ok=True)
            launch_config_path = Path(working_dir, VSCODE_DIR, LAUNCH_CONFIG)
            launch_config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(launch_config_path, 'w') as outfile:
                json.dump(data, outfile, indent=4)
        return str(launch_config_path)

    @staticmethod
    def create_container_config(**kwargs):
        # create container config
        with open(INPUT_DIR / CONTAINER_CONFIG) as container_config:
            data = json.load(container_config)
            for key, val in kwargs.items():
                data[key] = val
            os.makedirs(CONTAINER_DIR, exist_ok=True)
            container_config_path = os.path.join(CONTAINER_DIR, CONTAINER_CONFIG)
            with open(container_config_path, 'w') as outfile:
                json.dump(data, outfile, indent=4)
        return container_config_path


class DebugOnlineStepRunHelper(DebugStepRunHelper):
    @staticmethod
    def parse_designer_url(url):
        url = re.sub(r'^[^a-zA-Z]+', '', url)
        # portal url could end with numbers, eg: xxx/workspaces/DesignerTest-EUS2
        url = re.sub(r'[^a-zA-Z0-9]+$', '', url)
        args = {}
        entries = re.split(r'[/&?]', url)
        try:
            for i, entry in enumerate(entries):
                if entry == EXPERIMENT_KEY:
                    if entries[i + 1] == ID_KEY:
                        args[EXPERIMENT_KEY] = entries[i + 2]
                    else:
                        args[EXPERIMENT_KEY] = entries[i + 1]
                elif entry in [RUN_KEY, WORKSPACE_KEY, RESOURCE_GROUP_KEY, SUBSCRIPTION_KEY]:
                    args[entry] = entries[i + 1]
            return args[RUN_KEY], args[EXPERIMENT_KEY], args[WORKSPACE_KEY], args[RESOURCE_GROUP_KEY], args[
                SUBSCRIPTION_KEY]
        except BaseException as e:
            raise ValueError(f'Failed to parse portal url: {url}') from e

    @staticmethod
    def get_pipeline_run(run_id, workspace):
        pipeline_run = Run.get(workspace, run_id)

        _print_step_info(
            f'Workspace: {workspace.name} Experiment: {pipeline_run.experiment.name} StepRun: {run_id}')

        return pipeline_run

    @staticmethod
    def get_image_id(step_name, details):
        if 'properties' not in details:
            raise RuntimeError(f'{step_name} does not have properties')
        properties = details['properties']
        if 'AzureML.DerivedImageName' in properties:
            return properties['AzureML.DerivedImageName']
        else:
            for log_file, url in details['logFiles'].items():
                if 'azureml-execution' in log_file:
                    content = urllib.request.urlopen(url).read()
                    m = re.findall(r'latest: Pulling from (azureml/azureml_[^\\n]+)', str(content))
                    if len(m) > 0:
                        return m[0]
                    m = re.findall(r'Start to pulling docker image: [^/]+/(azureml/azureml_[^\\n]+)', str(content))
                    if len(m) > 0:
                        return m[0]
            raise RuntimeError(f'{step_name} does not have valid logs with image pattern azureml/azureml_[^\\n]')

    @staticmethod
    def prepare_dev_container(workspace, step, dry_run=False) -> ImageBase:
        # prepare image
        try:
            environment = step.get_environment()
        except Exception as e:
            original_error_message = f'{e.__class__.__name__}: {e}'
            raise RuntimeError('Failed to get environment details from step run details, '
                               'please make sure this step run has started successfully.\n'
                               f'Original error: {original_error_message}') from e
        image_details = environment.get_image_details(workspace)
        step_run_image = ImageBase(image_details, environment, workspace)

        if dry_run:
            # Won't pull image for dry run,
            # but still need to visit EMS to make sure that image exists and write a config.
            image_name = step_run_image.register_image_name
        else:
            _print_step_info('Preparing image.')
            image_name = step_run_image.get_component_image()
            _print_step_info(f'Prepared image {step_run_image.image_name}')

        # create container config
        data = {'image': image_name}
        DebugOnlineStepRunHelper.create_container_config(**data)
        return step_run_image

    @staticmethod
    def download_snapshot(service_caller: DesignerServiceCaller, step_run: Run, component_type: str,
                          snapshot_path=None, dry_run=False):
        if dry_run:
            return True
        snapshot_path = snapshot_path or os.getcwd()
        try:
            # TODO: move service caller to debugger and use run detail as param
            step_run_id = step_run.parent.id
            run_id = step_run.id
            run_details = service_caller.get_pipeline_run_step_details(run_id, step_run_id, include_snaptshot=True)
            snapshot_url = run_details.snapshot_info.root_download_url
            _download_snapshot(snapshot_url, snapshot_path)
            if component_type and component_type.lower() == 'parallel':
                _mock_parallel_driver_file(os.path.join(snapshot_path, DEBUG_FOLDER))
        except BaseException as e:
            logger.warning(
                f'Failed to download snapshot via SMT, fall back to user azureml core API. Error message: {e}')
            try:
                # Failed to download via SMT, try to download via azureml core API
                zip_path = step_run.restore_snapshot(path=snapshot_path)
                _extract_zip(zip_path, snapshot_path)
            except BaseException:
                return False
        _print_step_info(f'Downloaded snapshot {snapshot_path}')
        return True

    @staticmethod
    def prepare_inputs(workspace, details, dry_run=False):
        if 'runDefinition' not in details:
            raise RuntimeError('Failed to get runDefinition from step run details, '
                               'please make sure this step run has started successfully.')
        port_arg_map = {}
        result = True
        # data reference
        data_references = details['runDefinition']['dataReferences']
        for data_reference_name, data_store in data_references.items():
            data_store_name = data_store['dataStoreName']
            path_on_data_store = data_store['pathOnDataStore']
            # TODO: handle special characters in data path(could not run inside container in VS Code)
            port_arg_map[data_reference_name] = path_on_data_store
            if not dry_run:
                download_result = DebugOnlineStepRunHelper.download_data_reference(workspace, data_store_name,
                                                                                   path_on_data_store)
                result = result and download_result

        # dataset
        dataset = details['runDefinition']['data']
        for dataset_name, data in dataset.items():
            dataset_id = data['dataLocation']['dataset']['id']
            if not dry_run:
                download_result = DebugOnlineStepRunHelper.download_dataset(workspace, dataset_id)
                result = result and download_result
            port_arg_map[dataset_name] = dataset_id
        _print_step_info(f'Downloaded data: {port_arg_map}')

        return port_arg_map, result

    @staticmethod
    def download_data_reference(workspace, data_store_name, path_on_data_store) -> bool:
        data_path = Path(DATA_FOLDER)
        try:
            blob_data_store = Datastore.get(workspace, data_store_name)
            blob_data_store.download(target_path=str(data_path), prefix=path_on_data_store, overwrite=False)
            # output directory might be empty
            if not Path(data_path / path_on_data_store).exists():
                os.makedirs(data_path / path_on_data_store)
            return True
        except Exception as e:
            logger.warning('Could not download dataset {} due to error {}'.format(path_on_data_store, e))
            return False

    @staticmethod
    def download_dataset(workspace, dataset_id) -> bool:
        data_path = Path(DATA_FOLDER)
        try:
            dataset = Dataset.get_by_id(workspace, dataset_id)
            target_path = str(data_path / dataset_id)
            dataset.download(target_path=target_path, overwrite=True)
            return True
        except Exception as e:
            logger.warning('Could not download dataset {} due to error {}'.format(dataset_id, e))
            return False

    @staticmethod
    def prepare_arguments(step_name, details, port_arg_map, component_type):
        if 'runDefinition' not in details:
            raise RuntimeError('Failed to get runDefinition from step run details, '
                               'please make sure this step run has started successfully.')
        run_definition = details['runDefinition']
        if run_definition.get('script', None):
            script, arguments = run_definition['script'], run_definition['arguments']
        else:
            script, arguments = DebugOnlineStepRunHelper.split_python_command(
                command=run_definition['command'],
                interpreter_path=run_definition['environment']['python']['interpreterPath'])
        environment_vars = run_definition['environment']['environmentVariables']
        environment_vars = {f'${key}': environment_vars[key] for key in environment_vars}
        data_path = Path(DATA_FOLDER)
        for data_reference_name, port_dir in port_arg_map.items():
            data_reference_constant = DATA_REF_PREFIX + data_reference_name
            data_reference_path = (data_path / port_dir).as_posix()
            environment_vars[data_reference_constant] = data_reference_path
            port_arg_map[data_reference_name] = data_reference_path

        parsed_arguments = []
        for arg in arguments:
            for env_var, env_var_val in environment_vars.items():
                arg = arg.replace(env_var, env_var_val)
            parsed_arguments.append(arg)

        _print_step_info(f'Prepared arguments: {parsed_arguments} for step {step_name}')
        if component_type.lower() == 'parallel':
            script = f'{DEBUG_FOLDER}/{MOCK_PARALLEL_DRIVER}'
            parsed_arguments = translate_parallel_command(parsed_arguments, port_arg_map)
        else:
            script = run_definition['script']
        return script, parsed_arguments

    @staticmethod
    def check_remote_debug_compute_type(compute_type):
        if compute_type not in ['AmlCompute', 'Cmk8s', 'AmlK8s']:
            raise UserErrorException(
                "Remote debug not support %s as compute, only support AmlCompute and AksCompute." % compute_type)

    @staticmethod
    def get_run_definition_by_step_run(run):
        if len(list(run.get_children())) != 0:
            raise UserErrorException('Remote debug dose not support step run with child run.')
        details = run.get_details()
        run_definition = details["runDefinition"]

        if 'azureml.moduleid' not in run.properties:
            raise UserErrorException("Remote debug only supports the step run submitted by the component.")
        else:
            from azure.ml.component import Component
            component = Component.load(run.experiment.workspace, id=run.properties['azureml.moduleid'])()
            # Check component type
            if component._definition.type not in {ComponentType.CommandComponent, ComponentType.DistributedComponent,
                                                  ComponentType.SweepComponent}:
                raise UserErrorException('Remote debug not support %s component.' % component.type)
            if component.type == ComponentType.DistributedComponent.value and \
                    component._definition.launcher.type != LauncherType.MPI:
                raise UserErrorException("Not support debugging %s type distribute component." %
                                         component._definition.launcher.type)

            # For SweepComponent, parameters are stored in the tags. Set the parameters to the environment variables.
            if component.type == ComponentType.SweepComponent.value:
                for key, val in json.loads(run.tags['hyperparameters']).items():
                    environment_variables_name = 'AZUREML_SWEEP_%s' % re.search('\\w.*', key).group()
                    run_definition['environment']['environmentVariables'][environment_variables_name] = val
        os_type = run_definition['environment']['docker'].get('platform', {}).get('os', None)
        if os_type and os_type.lower() != 'linux':
            raise UserErrorException("Not support %s as execution environment for debugging." % os_type)
        return run_definition, component

    @staticmethod
    def get_compute_type(compute, workspace, run_details):
        """
        Get compute target and type. If compute is None, it will get compute type from run_definition.

        :param compute: Compute name to debug step run.
        :type str or None
        :param workspace: Workspace of step run.
        :type azureml.core.Workspace
        :param run_details: Run details of step run.
        :type dict

        :return: compute: Compute name to debug step run.
                 compute_type: Compute type.
        :rtype: str, str
        """
        compute = compute or run_details.get('target', None)
        if compute:
            compute_info = ComputeTarget._get(workspace=workspace, name=compute)
            if compute_info is None:
                raise UserErrorException('Cannot get compute %s in the workspace.' % compute)
            compute_type = compute_info['properties']['computeType']

            # Validate compute target
            if compute_type == 'AmlCompute' and \
                    'userAccountCredentials' not in compute_info['properties']['properties']:
                raise UserErrorException(COMPUTE_DISABLED_SSH_ERR_MSG % compute)
        else:
            compute_type = run_details['runDefinition']['globalJobDispatcher']['computeType']

        DebugOnlineStepRunHelper.check_remote_debug_compute_type(compute_type=compute_type)
        return compute, compute_type

    @staticmethod
    def update_compute_config(run_config, compute, compute_type):
        """
        Update compute config of run_config.

        :param run_config: Runconfig of step run.
        :type azureml.core.ScriptRunConfig
        :param compute: Compute name to debug step run.
        :type str or None
        :param compute_type: Type of the compute.
        :type str
        """
        def get_resource_configuration(run_config, compute_type):
            resource_keys = ['cpu_count', 'gpu_count', 'memory_request_in_gb']
            resource_configuration = {}
            cm_k8s_resource_configuration = run_config.cmk8scompute.get('configuration', {})
            aml_k8s_resource_configuration = run_config.amlk8scompute.get('resourceConfiguration', {})
            for key in resource_keys:
                camel_key = to_camel_case(key)
                resource_name = key if compute_type == 'Cmk8s' else camel_key
                resource_configuration[resource_name] = \
                    cm_k8s_resource_configuration.get(key, None) or aml_k8s_resource_configuration.get(camel_key, None)
            return resource_configuration

        if compute and hasattr(run_config, 'global_job_dispatcher'):
            # Remove GlobalJobDispatcher when set specific compute.
            run_config.global_job_dispatcher = None
        if compute_type == 'Cmk8s':
            # Enable SSH in job instance.
            if 'configuration' not in run_config.cmk8scompute:
                run_config.cmk8scompute['configuration'] = {}
            run_config.cmk8scompute['configuration']['enable_ssh'] = True
            run_config.cmk8scompute['configuration']['enable_preemption'] = False
            # Update resource configuration
            run_config.cmk8scompute['configuration'].update(get_resource_configuration(run_config, compute_type))
            # Remove aml8scompute config in run config.
            run_config.amlk8scompute = None
        elif compute_type == 'AmlK8s':
            if 'interactiveConfiguration' not in run_config.amlk8scompute:
                run_config.amlk8scompute['interactiveConfiguration'] = {}
            run_config.amlk8scompute['interactiveConfiguration']['isSshEnabled'] = True
            # Update resource configuration
            run_config.amlk8scompute['resourceConfiguration'] = get_resource_configuration(run_config, compute_type)
            # Fix the bug of GJD service that it could not handle PreemptionType=null well.
            # Bug link: https://msdata.visualstudio.com/Vienna/_workitems/edit/1286810
            run_config.amlk8scompute['priorityConfiguration']['isPreemptible'] = False
            # Remove cmk8scompute config in run config.
            run_config.cmk8scompute = None
        run_config.target = compute or 'mock_compute'

    @staticmethod
    def generate_run_config_by_run_definition(run_definition):
        """
        Generate run_config by run_definition.

        :param run_definition: run_definition of step run.
        :type run_definition: dict

        :return: run_config
        :rtype: azureml.core.ScriptRunConfig
        """
        setattr(RunConfiguration, 'amlk8scompute', {})
        setattr(RunConfiguration, 'cmk8scompute', {})
        setattr(RunConfiguration, 'global_job_dispatcher', {})

        RunConfiguration._field_to_info_dict['amlk8scompute'] = _FieldInfo(
            dict, "This attribute is used to pass aml k8s compute configuration.", serialized_name='amlK8sCompute')
        RunConfiguration._field_to_info_dict['cmk8scompute'] = _FieldInfo(dict, "k8scompute specific details.",
                                                                          serialized_name='cmk8scompute')
        RunConfiguration._field_to_info_dict['global_job_dispatcher'] = _FieldInfo(dict, "Global Job Dispatcher")
        # To handle runconfig deserialization failed.
        RunConfiguration._field_to_info_dict['environment_variables'] = _FieldInfo(
            dict, "Runtime environment variables")

        data_path = {}
        for key, val in run_definition['outputData'].items():
            data_path[key] = val['outputLocation'].pop('dataPath')
        # Generate run config by run definition
        runconfig = RunConfiguration._get_runconfig_using_dict(run_definition)

        # Since DataPath needs to set the param values when initialize, it raises error when deserialize to object.
        # Using the info in outputLocation to directly generate DataPath to fix it.
        from azureml.core.runconfig import DataPath
        for key, val in data_path.items():
            if val:
                # Change output name to camel_case to fix cannot find output path in compute.
                output_data = runconfig.output_data.pop(to_camel_case(key))
                output_data.output_location.data_path = DataPath(datastore_name=val['datastoreName'],
                                                                 relative_path=val['relativePath'])
                runconfig.output_data[key] = output_data
        # Used to serialization run_config during sending the request.
        runconfig.__dict__.update(amlk8scompute=runconfig.amlk8scompute,
                                  cmk8scompute=runconfig.cmk8scompute,
                                  global_job_dispatcher=runconfig.global_job_dispatcher)
        return runconfig

    @staticmethod
    def resolve_python_arguments(run_config):
        # Get script and arguments
        if run_config.script:
            return run_config.script, run_config.arguments
        else:
            return DebugOnlineStepRunHelper.split_python_command(run_config.command,
                                                                 run_config.environment.python.interpreter_path)

    @staticmethod
    def split_python_command(command, interpreter_path='python'):
        """
        Split python command to script and arguments
        :param command: Command starts with python or interpreter path.
        :type command: str
        :param interpreter_path: The Python interpreter path.
        :type interpreter_path: str
        :return: script: Script name in command
                 arguments: Arguments of python command.
        :rtype: str, List[str]
        """
        # To avoid execution errors after splitting argument to list, only script is separated.
        argument_group = re.search('((?<=^python )|(?<=^%s )).*' % interpreter_path, command)
        if argument_group:
            script, argument = None, argument_group.group()
            # Identify the interface option of python command, it the option does not start with'-',
            # it's considered that the python code contained in script.
            # https://docs.python.org/3/using/cmdline.html#interface-options
            if not re.match('^-\\w .*', argument):
                script, argument = argument.split(' ', maxsplit=1)
            return script, [argument, ]
        else:
            raise UserErrorException('The command, %s, does not start with python.' % command)

    @staticmethod
    def get_dataset_environment_variables(arguments, compute_type):
        """
        Generate input/output environment variables.

        :param arguments: The command or arguments of step run.
        :type arguments: str or List[str]
        :param compute_type: Compute type
        :type compute_type: str
        :return: dataset_environment_variables: key-value of input/output, key is the dataset in the arguments,
                                                value is the environment variable name.
        :rtype: dict[str, str]
        """
        dataset_environment_variables = {}
        if isinstance(arguments, str):
            arguments = shlex.split(arguments)
        for argument in arguments:
            if AZUREML_DATASET_PREFIX in argument or AZUREML_OUTPUT_PREFIX in argument:
                # Get the param name of the dataset
                data_param_name = re.search(
                    '((?<=\\%s)|(?<=%s)).*' % (AZUREML_DATASET_PREFIX, AZUREML_OUTPUT_PREFIX), argument).group()
                if compute_type in ITP_COMPUTE_TYPE:
                    # Add the prefix AZUREML_TRANS_DATA_PATH_ as an environment variable name for ITP compute.
                    data_env_name = AZUREML_TRANS_PREFIX + data_param_name
                else:
                    # If running in AmlCompute, the input/output environment variables will be set in a env file which
                    # is used to create container. The env key is param name, value is input/output path.
                    data_env_name = data_param_name
                data_pattern = '(\\%s|%s)%s' % (AZUREML_DATASET_PREFIX, AZUREML_OUTPUT_PREFIX, data_param_name)
                dataset_environment_variables[re.search(data_pattern, argument).group()] = data_env_name

        return dataset_environment_variables

    @staticmethod
    def generate_remote_debug_arguments(run_config, dataset_environment):
        """
        Generating arguments are used for VScode launch.json.
        For the params in the run config, because the value of params will be set as env variables,
        it will replace them to ${env:param_name}, it is the reference of env variables in VScode launch.

        For example:
            Run_config arguments:
            [
                "$AZUREML_PARAMETER_param_name", "$AZUREML_DATAREFERENCE_input_name", "DatasetOutputConfig:output_name"
            ]
            VScode debug arguments:
            [
                "${env:AZUREML_PARAMETER_param_name}, "${env:AZUREML_TRANS_DATA_PATH_input_name}",
                "${env:AZUREML_TRANS_DATA_PATH_output_name}"
            ]

        :param run_config: Runconfig of step run.
        :type run_config: azureml.core.ScriptRunConfig
        :param dataset_environment: Input/output environment variables.
        :type dataset_environment: dict[str, str]
        :return: script: python script of step run
                 debug_arguments: arguments used in vscode launch.json
        :rtype: str, List[str]
        """
        script, arguments = DebugOnlineStepRunHelper.resolve_python_arguments(run_config)

        debug_arguments = []
        for argument in arguments:
            debug_argument = argument
            for param_name in re.findall(DebugOnlineStepRunHelper.PARAM_PATTERN, argument):
                # Change environment variable to ${env:env_variable_name} to be identified in vscode debugging.
                debug_argument = debug_argument.replace(param_name, '${env:%s}' % param_name[1:])
            for data_param_name in re.findall(DebugOnlineStepRunHelper.DATA_PATTERN, argument):
                # The input/output param values are obtained during component execution in the remote.
                # It marks the arguments of input/output value and replaces it during the execution.
                # Get parameter name of input/output data in command
                debug_argument = debug_argument.replace(data_param_name,
                                                        '${env:%s}' % dataset_environment[data_param_name])
            debug_arguments.append(debug_argument)
        return script, debug_arguments

    # If compute lacks the resources, the status will remain Queue. Waiting for the resources may cost a lot of time.
    # Waiting for half an hour to wait the status change to Running.
    @staticmethod
    @timeout(timeout_seconds=TIMEOUT_SECONDS,
             timeout_msg='Timed out of waiting for getting the link of debug run. Please check that the compute '
                         'resources are available for execution.',
             prompt_msg='Waiting for the run to start to get debug run link...')
    def get_debug_run_link(run, compute_type):
        """
        If compute_type is AmlCompute, it will get the portal url of step run.
        If compute_type is ITP compute, it will wait for run status to Running and get job link from run tags.
        :param run: The step run to get link.
        :type run: azureml.core.Run
        :param compute_type: Compute type.
        :type compute_type: str

        :return: run_link
        :rtype: str
        """
        if compute_type in ITP_COMPUTE_TYPE:
            # Wait for run status to Running. When step is running, it will set job link to tags.
            status = run.get_status()
            while status in [RunStatus.QUEUED, RunStatus.NOT_STARTED, RunStatus.PREPARING,
                             RunStatus.STARTING, RunStatus.PROVISIONING, RunStatus.UNAPPROVED]:
                time.sleep(REQUEST_INTERVAL_SECONDS)
                status = run.get_status()
            logger.info('Current debug run status is %s' % status)
            run_link = run.tags.get('amlk8s job link', None)
            assert status == RunStatus.RUNNING, 'Run status is %s. %s' % (status,
                                                                          'Run link %s' % run_link if run_link else
                                                                          'Portal link: %s' % run.get_portal_url())
        else:
            run_link = run.get_portal_url()
        return run_link

    # For AmlCompute, building the image may cost a lot of time before execution step command.
    # Wait half an hour for getting the information from run log.
    @staticmethod
    @timeout(timeout_seconds=TIMEOUT_SECONDS,
             timeout_msg='Timed out of waiting for getting debugging information. You may get some information about '
                         'timeout in the running log by the step link.',
             prompt_msg='Waiting for the run to start to get debugging information...')
    def search_in_run_log(run, pattern_log_name, pattern_list):
        """
        Search for information in the specified log file.
        :param run: The step run is retrieved.
        :type run: azureml.core.Run
        :param pattern_log_name: The pattern for specified log file name.
        :type pattern_log_name: str
        :param pattern_list: List of patterns to search.
        :type pattern_list: str

        :return: pattern_results: The key is pattern of parttern_list and the value is the first match.
        :rtype: dict
        """
        pattern_results = {item: None for item in pattern_list}
        pre_logs = {}
        run._output_logs_pattern = pattern_log_name
        run_status = RunStatus.RUNNING
        while not all(pattern_results.values()) and run_status in RunStatus.get_running_statuses():
            current_details = run.get_details()
            run_status = current_details['status']
            if not pre_logs:
                pre_logs = {file_name: 0 for file_name in run._get_logs(current_details)}
            for file_name in pre_logs.keys():
                logs = _get_content_from_uri(current_details['logFiles'][file_name],
                                             timeout=Run._DEFAULT_GET_CONTENT_TIMEOUT).splitlines()
                for regex, result in pattern_results.items():
                    if not result:
                        pattern_results[regex] = next(iter(
                            [re.search(regex, line).group() for line in logs[pre_logs[file_name]:] if
                             re.search(regex, line)]), None)
                # It will streaming get the run log, the last line obtained may not be completed.
                # So mark the second last line as the searched line.
                pre_logs[file_name] = len(logs) - 1 if logs else 0
        return pattern_results

    @staticmethod
    def get_compute_ssh_command(run, compute_type):
        """
        Get the ssh command from compute. If compute is AmlCompute, it will find the compute node which run the step.
        If compute is Cmk8s, it will send request to get the job detail to find ssh command.
        :param run: The step run.
        :type run: azureml.core.Run
        :param compute_type: Compute type.
        :type compute_type: str

        :return: SSH connect command.
        :rtype: str
        """
        DebugOnlineStepRunHelper.check_remote_debug_compute_type(compute_type=compute_type)
        if compute_type == 'AmlCompute':
            return DebugOnlineStepRunHelper._get_amlcompute_ssh_command(run)
        elif compute_type in ITP_COMPUTE_TYPE:
            return DebugOnlineStepRunHelper._get_itp_ssh_command(run)

    @staticmethod
    def _get_amlcompute_ssh_command(run):
        """Get the SSH connection command from the AmlCompute."""
        assert run.status == RunStatus.RUNNING, 'Cannot get SSH connection command from a run is not Running.'
        compute_name = run.get_details()['target']
        compute_target = ComputeTarget(run.experiment.workspace, compute_name)
        run_nodes = list(
            iter(node for node in compute_target.list_nodes() if 'runId' in node and node['runId'] == run.id))
        if not run_nodes:
            raise RuntimeError('Cannot find compute node runs step.')
        if not compute_target.admin_username:
            raise UserErrorException(COMPUTE_DISABLED_SSH_ERR_MSG % compute_name)
        return ["ssh %s@%s -p %s" % (compute_target.admin_username, run_node['publicIpAddress'], run_node['port'])
                for run_node in run_nodes]

    # For AmlCompute, it the component step is running, could directly get connection command from the compute.
    # For ITP compute, if the ssh initialize is success, it will not cost a lot of time.
    # Wait 5min to get the SSH connection command.
    @staticmethod
    @timeout(timeout_seconds=5 * 60,
             timeout_msg='Timed out of waiting for initialization of SSH for job instance. You could investigate '
                         'the root cause of timeout by checking the compute status or running logs of the step.',
             prompt_msg='Waiting for the SSH endpoint initialization to complete to get SSH connection command...')
    def _get_itp_ssh_command(run):
        """Get the SSH connection command from the ITP compute."""
        run_status = RunStatus.RUNNING
        while run_status in RunStatus.get_running_statuses():
            run_status = run.get_status()
            job_detail = DebugOnlineStepRunHelper._get_itp_job_details(run)
            if not job_detail.get('endpointSettings', {}).get('enableSsh', None):
                raise RuntimeError("SSH is disabled in the job instance.")
            elif job_detail['endpoints']:
                endpoints = job_detail['endpoints']
                return {endpoint['name']: endpoint['url'] for endpoint in endpoints if not endpoint['isInvariable']}
            time.sleep(REQUEST_INTERVAL_SECONDS)
        raise RuntimeError('Run status is %s. It is not running, cannot get SSH endpoint.')

    @staticmethod
    def _get_itp_job_details(run):
        """
        Get the details of job instance.
        :param run: The job instance run
        :type run: azureml.core.Run
        :return: The details of job instance.
        :type: dict
        """
        def construct_get_ipt_detail_request(run):
            data = {
                'clusterName': run.properties['Cluster'],
                'jobCategory': "Itp",
                'jobId': run.properties['JobId'],
                'vcName': run.properties['VC']
            }
            headers = run.experiment.workspace._auth.get_authentication_header()
            headers['content-type'] = 'application/json'

            job_detail_url = 'https://amlk8s.azurefd.net/ITP/api/v1.0/Jobs/detail/itp'
            return urllib.request.Request(
                url=job_detail_url, data=bytes(json.dumps(data), 'utf-8'), headers=headers, method='post')

        request = construct_get_ipt_detail_request(run)
        content = urllib.request.urlopen(request).read().decode('utf-8')
        return json.loads(content) if content else {}

    @staticmethod
    def get_debug_run_info(debug_run, component, compute_type, dataset_environment):
        """
        Get working directory and script command from the debug run log. If the component is distributed component
        and runs in ITP compute, it will generate distributed execution command and add to script command.

        :param debug_run: The debug run
        :type debug_run: azureml.core.Run
        :param component: The component generated by component run, is used to identify the component type.
        :type component: azure.ml.component.Component
        :param compute_type: Compute type.
        :type compute_type: str
        :param dataset_environment: Input/output environment variables.
        :type dataset_environment: dict[str, str]
        :return: working_dir: Working directory of debug run
                 script_command: Script command and distributed execution command.
        :rtype: working_dir: str
                script_command: str or dict[str, str]
        """
        working_dir_regex = '(?<=Command Working Directory=).*'
        command_regex = '(?<=Starting Linux command : ).*'
        execution_command = '.*\\$AZ_CMK8S_JOB_PREP.*'
        pattern_list = [working_dir_regex, command_regex]
        # When the component is distributed component and runs in ITP compute, it will get the compute execution
        # command to generate distributed execution command.
        if compute_type in ITP_COMPUTE_TYPE and component.type == ComponentType.DistributedComponent.value:
            pattern_list.append(execution_command)

        # The expect log file name likes these, azureml-logs/azureml/00_08d406bfdda14ba75ef-ps-0_stdout.txt or
        # azureml-logs/azureml/00_08d406bfdda14ba75ef-master-0_stdout.txt
        pattern_log_name = 'azureml-logs/.*(ps-0_stdout|.*master-0_stdout).txt' \
            if compute_type in ITP_COMPUTE_TYPE else '.*driver_log.*.txt'

        pattern_results = DebugOnlineStepRunHelper.search_in_run_log(
            debug_run, pattern_log_name=pattern_log_name, pattern_list=pattern_list)
        working_dir = pattern_results[working_dir_regex]
        if debug_run.status not in RunStatus.get_running_statuses():
            raise RuntimeError("The status of the step run used for debugging is not running. "
                               "Please check the step run log.")
        if not all(pattern_results.values()):
            raise RuntimeError("Cannot get working directory or command from step run log.")
        script_command = re.search('(?<=%s).*' % SLEEP_COMMAND, pattern_results[command_regex]).group()

        if execution_command in pattern_results:
            # Add distributed execution command to script command.
            script_command, distributed_command = DebugOnlineStepRunHelper.generate_distributed_execution_command(
                debug_run, working_dir, pattern_results[execution_command], component, dataset_environment)
            script_command = {'Command': script_command, 'Distributed command': distributed_command}
        return working_dir, script_command

    @staticmethod
    def print_debug_info(run_link, working_dir, commands, ssh_connection_command):
        """Show debug info in terminal."""
        debug_info_list = ['Information about debug run and remote compute:',
                           'Link to debug run: %s' % run_link,
                           'Command Working Directory: %s' % working_dir]
        if isinstance(commands, str):
            debug_info_list.append('Command: %s' % commands)
        else:
            debug_info_list.extend(['Debug Command:'] + ['\t%s: %s' % (k, v) for k, v in commands.items()])

        if isinstance(ssh_connection_command, dict):
            ssh_connection_command = ['%s: %s' % (k, v) for k, v in ssh_connection_command.items()]
        if isinstance(ssh_connection_command, list):
            debug_info_list.extend(['SSH connection command:'] + ['\t%s' % k for k in ssh_connection_command])
        else:
            debug_info_list.append('SSH connection command: %s' % str(ssh_connection_command))
        _print_step_info(debug_info_list)

    @staticmethod
    def print_remote_debug_step(run, compute_type, ssh_connection_command, is_python_command):
        if compute_type == 'AmlCompute':
            host, port = '<host>', '<port>'
            if len(ssh_connection_command) == 1:
                ssh_connection_commands = ssh_connection_command[0].split(' ')
                host, port = ssh_connection_commands[1], ssh_connection_commands[3]
            step_list = [
                'Interactive debug steps using VSCode:',
                '1. Configure ssh-agent on the local system with the private key file. Execute command: '
                '%sssh-add <keyfile path>' % (
                    'sc config ssh-agent start=auto; net start ssh-agent; ' if os.name == 'nt' else ''),
                '2. Create and active Docker context. Execute command: '
                'docker context create %s --docker "host=ssh://%s:%s"; docker context use %s' % (
                    run.id, host, port, run.id),
                '3. Manage Docker as a non-root user, execute "sudo usermod -aG docker $USER" in remote compute.',
                '4. After active the Docker context, connect to the container, which name is "%s", '
                'in Docker extension of VScode.' % run.id
            ]
        else:
            step_list = [
                'Interactive debug steps using VSCode:',
                '1. Add SSH connection config to SSH targets in VScode.',
                '2. Find the SSH target in remote explorer tab to login remote compute.',
                '3. After login the remote compute, open the working directory.'
            ]
        if is_python_command:
            step_list.append('%s. Debugging configuration is recorded in .vscode/launch.json. '
                             'After install python extension, press F5 to debug the script.' % len(step_list))
        step_list.append('%s. Cancel the debug run when finished debugging.%s' % (
            len(step_list), ' And recover the docker context by command: docker context use <previous context name>'
            if compute_type not in ITP_COMPUTE_TYPE else ''))
        step_list.append('For more details, please refer to https://componentsdk.azurewebsites.net/howto/'
                         'debug-component-in-remote-compute.html')
        _print_step_info(step_list)

    @staticmethod
    def get_interpreter_path(run_config):
        """Get python interpreter path from runconfig.environment."""
        interpreter_path = (run_config.environment.python.interpreter_path or 'python') if \
            run_config.environment.python.user_managed_dependencies else \
            '/azureml-envs/%s/bin/python' % \
            run_config.environment.python.conda_dependencies._conda_dependencies['name']
        return interpreter_path

    @staticmethod
    def mock_mpi_execute_script(tempdir):
        with open(os.path.join(tempdir, DISTRIBUTED_SCRIPT), 'w+') as f:
            code = """import subprocess, sys
command = ' '.join(sys.argv[1:])
result = subprocess.check_output(command, shell=True, encoding='utf-8', stderr=subprocess.STDOUT)
print(result)"""
            f.writelines(code)

    @staticmethod
    def generate_distributed_execution_command(run, working_dir, execution_command, component, dataset_environment):
        """
        It will use the compute execution command and script run command to generate distributed execution command.

        :param run: The debug run.
        :type run: azureml.core.Run
        :param working_dir: Working directory of debug run.
        :type working_dir: str
        :param execution_command: The compute execute command, getting from the run log.
        :type execution_command: str
        :param component: The component generated by component run, is used to identify the launcher type.
        :type component: azure.ml.component.Component
        :param dataset_environment: Input/output environment variables.
        :type dataset_environment: dict[str, str]
        :return script_run_command: Script run command in the node.
                distributed_execution_command: Mock distributed execution command in the compute.
        :rtype: str, str
        """
        interpreter_path = DebugOnlineStepRunHelper.get_interpreter_path(run._run_config)
        # Get the script command after removing sleep command.
        script_run_command = re.search('(?<=%s).*' % SLEEP_COMMAND, run._run_config.command).group()
        # Replace input/output variables to the environment variables.
        for k, v in dataset_environment.items():
            script_run_command = script_run_command.replace(k, '$%s' % v)

        if component._definition.launcher.type == LauncherType.MPI:
            # Distributed command consists of three parts, ssh connection command, mpi command, script run command.
            # Script run command is used to execute the script of run, input/output variables are replaced to
            # environment variables. Mpi command is used to execute parallel jobs, it contains script run command.
            # SSH connection command is used to connect to worker and execute mpi command.

            # Generate script run command, like this: /azureml-envs/xxx/python mock_distributed_run.py <run command>
            # Add \ in front of $ to avoid environment variable being escaped.
            mock_script_run_command = ' '.join(['%s %s' % (interpreter_path, DISTRIBUTED_SCRIPT),
                                                script_run_command.replace('$', r'\\\\\\\$')])
            # Get mpirun command, like this: mpirun --tag-output -hostfile /job/\\\${DLTS_JOB_ID}/hostfile --npernode 4
            mpi_command = re.search('mpirun .* /bin/bash --login -c ', execution_command).group()
            # Get the ssh connection command, like this: ssh worker-0 "/bin/bash --login -c \"<mpi command>\""
            ssh_command = re.search('ssh (.*?)/bin/bash --login -c ', execution_command).group() + r'\"%s\""'
            # Add mpi command and script run command to ssh connection command.
            distributed_execution_command = ssh_command % (r'cd %s && %s \\\"%s\\\"' % (working_dir, mpi_command,
                                                                                        mock_script_run_command))
        else:
            raise UserErrorException("Not support debugging %s type distribute component." %
                                     component._definition.launcher.type)
        return script_run_command, distributed_execution_command


class DebugCommonRuntimeStepHelper(DebugOnlineStepRunHelper):

    AZUREML_SETUP_PATH = 'azureml-setup'
    COMMON_RUNTIME_BOOTSTRAPPER_INFO = 'common_runtime_bootstrapper_info.json'
    COMMON_RUNTIME_JOB_SPEC = 'common_runtime_job_spec.json'
    DEBUG_FILE = "DEBUG"

    def __init__(self, run):
        self.run = run
        self.debug_run = None
        self.workspace = run.experiment._workspace
        self.common_debug_temp_folder = os.path.join(Path.home(), '.azureml-common-runtime-debug', run.id)
        if os.path.exists(self.common_debug_temp_folder):
            shutil.rmtree(self.common_debug_temp_folder)
        Path(self.common_debug_temp_folder).mkdir(parents=True)
        self.stdout = open(os.path.join(self.common_debug_temp_folder, 'stdout'), 'w+')
        self.stderr = open(os.path.join(self.common_debug_temp_folder, 'stderr'), 'w+')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.stdout.close()
            self.stderr.close()
        except:
            pass

    @staticmethod
    def _login_docker_registry(registry):
        if registry:
            login_command = ["docker", "login",
                             "--username", registry['username'],
                             "--password", registry['password'],
                             registry["url"]]
            login_process = subprocess.run(login_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            if login_process.returncode != 0:
                raise AzureMLException(f'Cannot login docker registry "{registry["url"]}", '
                                       f'more details: {login_process.stdout.read()}')
            else:
                _az_ml_logger.debug(f"Login {registry['url']} successed.")
        else:
            raise AzureMLException(f"Missing registry info in bootstrapper config.")

    @staticmethod
    def installed_requirements():
        DebugStepRunHelper.installed_requirements()
        if os_name == 'nt':
            raise UserErrorException("Please execute the debugging using common-runtime in linux or wsl2.")

    def start_local_run(self):
        """Call execution service to start a local run."""
        from azureml._execution._commands import _serialize_run_config_to_dict

        with tempfile.TemporaryDirectory() as tempdir:
            details = self.run.get_details()
            # Get the run definition.
            run_definition = details["runDefinition"]
            run_definition['target'] = 'local'
            run_definition['environmentVariables']["AZUREML_COMPUTE_USE_COMMON_RUNTIME"] = "true"

            # Set snapshot id in the definition.json and upload an empty project.zip
            definition_json = {
                "Configuration": _serialize_run_config_to_dict(run_definition),
                "SnapshotId": details['properties']['ContentSnapshotId']
            }
            snapshot_path = os.path.join(tempdir, f"{str(uuid.uuid4())}.zip")
            zipfile.ZipFile(snapshot_path, "w")
            with open(snapshot_path, "rb") as archive:
                files = [
                    ("files", ("definition.json", json.dumps(definition_json, indent=4, sort_keys=True))),
                    ("files", ("project.zip", archive))
                ]
                # Call Executor service with run definition to get job spec and bootstrapper info.
                _az_ml_logger.info("Call execution service to get job spec and bootstrapper info.")
                debug_run_id = str(uuid.uuid4())
                response = start_a_local_run(workspace=self.workspace,
                                             experiment_name=self.run.experiment.name,
                                             run_id=debug_run_id,
                                             files=files)
                self.debug_run = Run(experiment=self.run.experiment, run_id=debug_run_id)
                debug_run_log = f"Generate submitted local run, run id: {debug_run_id}"
                _az_ml_logger.debug(debug_run_log)
                self.stdout.write(debug_run_log)
            return response

    def get_common_runtime_info_by_response(self, response):
        """
        Extract common-runtime info from execution service response.

        :param response: The response of /localrun
        :return: bootstrapper_json: bootstrapper info
                 job_spec: job_spec in the response.
        :rtype: dict, str
        """
        _az_ml_logger.info("Extra common-runtime info from execution service response.")
        with tempfile.TemporaryDirectory() as tempdir:
            invocation_zip_path = os.path.join(tempdir, "invocation.zip")
            with open(invocation_zip_path, "wb") as file:
                file.write(response.content)

            with zipfile.ZipFile(invocation_zip_path, "r") as zip_ref:
                bootstrapper_path = f"{self.AZUREML_SETUP_PATH}/{self.COMMON_RUNTIME_BOOTSTRAPPER_INFO}"
                job_spec_path = f"{self.AZUREML_SETUP_PATH}/{self.COMMON_RUNTIME_JOB_SPEC}"
                if not all(file_path in zip_ref.namelist() for file_path in [bootstrapper_path, job_spec_path]):
                    raise AzureMLException(
                        f"{bootstrapper_path}, {job_spec_path} are not in the execution service response.")

                with zip_ref.open(bootstrapper_path, "r") as bootstrapper_file:
                    bootstrapper_json = json.loads(base64.b64decode(bootstrapper_file.read()))
                with zip_ref.open(job_spec_path, "r") as job_spec_file:
                    job_spec = job_spec_file.read().decode('utf-8')
        return bootstrapper_json, job_spec

    def get_bootstrapper_bin(self, bootstrapper):
        """
        Copy bootstrapper from the bootstrapper image.

        :param bootstrapper: bootstrapper info
        :type bootstrapper: dict
        :return: bootstrapper bin path
        :rtype: str
        """
        from azure.ml.component._execution._command_execution import _copy_from_container

        vm_bootstrapper_path = os.path.join(self.common_debug_temp_folder, "vm-bootstrapper")
        Path(self.common_debug_temp_folder).mkdir(parents=True, exist_ok=True)
        _az_ml_logger.info(f"Store vm-bootstrapper binary to {vm_bootstrapper_path}.")

        registry = bootstrapper.get("registry")
        self._login_docker_registry(registry)

        def copy_bootstrapper_from_container(registry, override_bootstrapper_image=None):
            if override_bootstrapper_image:
                bootstrapper_image = override_bootstrapper_image
            else:
                bootstrapper_image = f"{registry['url']}/boot/vm-bootstrapper/binimage/linux:{bootstrapper['tag']}"

            _az_ml_logger.debug(f"Pull the bootstrapper image {bootstrapper_image}.")
            docker_client = get_docker_client()
            boot_img = docker_client.images.pull(bootstrapper_image)
            boot_container = docker_client.containers.create(image=boot_img, command=[""])

            # Copy the vm-bootstrapper to $HOME/common-runtime-debug/<run-id>/vm-bootstrapper
            _az_ml_logger.debug(f"Copy the bootstrapper bin file from container to {vm_bootstrapper_path}.")
            _copy_from_container(boot_container, "vm-bootstrapper", vm_bootstrapper_path)

            # Stop and remove the container
            _az_ml_logger.debug(f"Remove bootstrapper container {boot_container.id}.")
            boot_container.stop()
            boot_container.remove()

        def bootstrapper_support_debug(vm_bootstrapper_path):
            """Check bootstrapper contains debug args"""
            # TODO: Remove this before merging into master.
            process = subprocess.Popen(f"{vm_bootstrapper_path} --help", stdout=subprocess.PIPE, shell=True,
                                       stderr=subprocess.STDOUT, encoding='utf-8')
            process.wait()
            process_stdout = process.stdout.read()
            return "--debug" in process_stdout

        copy_bootstrapper_from_container(registry)
        return vm_bootstrapper_path

    def execute_bootstrapper(self, bootstrapper_bin, job_spec):
        # No need to worry about creating the file or all the directories leading up
        # to this file. vm-bootstrapper should take care of that when it writes to it.
        debug_info_file_path = os.path.join(self.common_debug_temp_folder, self.DEBUG_FILE)
        cmd = [bootstrapper_bin, '--job-spec', job_spec,
               '--debug', debug_info_file_path,
               '--skip-auto-update', '--disable-identity-responder', '--skip-cleanup']
        env = {
            'RUST_BACKTRACE': '1',
            'AZ_BATCHAI_CLUSTER_NAME': 'fake_cluster_name',
            'AZ_BATCH_NODE_ID': 'fake_id',
            'AZ_BATCH_NODE_STARTUP_DIR': '.',
            'AZ_BATCH_CERTIFICATES_DIR': '.',
            'AZ_BATCH_NODE_SHARED_DIR': '.',
            'AZ_LS_CERT_THUMBPRINT': 'fake_thumbprint',
        }
        _az_ml_logger.info(f"Execute bootstrapper binary to prepare debug environment.")
        _az_ml_logger.debug(f"Bootstrapper execution environment variables: {env}")
        _az_ml_logger.debug(f"Bootstrapper execution cwd: {self.common_debug_temp_folder}")
        _az_ml_logger.debug(f"Bootstrapper execution command: {' '.join(cmd)}")

        process = subprocess.Popen(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   cwd=self.common_debug_temp_folder, encoding='utf-8')
        # When log level of az-ml is DEBUG, show the log of bootstrapper.
        show_in_console = False
        for log_handler in _az_ml_logger.handlers:
            if isinstance(log_handler, logging.StreamHandler) and log_handler.level == logging.DEBUG:
                show_in_console = True
        self._log_subprocess(process.stdout, self.stdout, show_in_console)
        self._log_subprocess(process.stderr, self.stderr, show_in_console)
        return process

    def _log_subprocess(self, io, file, show_in_console=False):

        def log_subprocess(io, file, show_in_console):
            for line in iter(io.readline, ''):
                if show_in_console:
                    print(line, end='')
                file.write(line)

        thread = Thread(target=log_subprocess, args=(io, file, show_in_console))
        thread.daemon = True
        thread.start()

    def _check_bootstrapper_process_status(self, bootstrapper_process):
        """
        Check the bootstrapper process status, it process return code is not zero, it will raise RuntimeError.

        :param bootstrapper_process: bootstrapper process
        :type bootstrapper: Popen
        :return: return_code
        :rtype: int
        """
        return_code = bootstrapper_process.poll()
        if return_code:
            self.stderr.seek(0)
            raise AzureMLException(
                f"Bootstrap binary execution failed. Error details: {self.stderr.read()}\nPlease check "
                f"https://componentsdktest.azurewebsites.net/howto/local-debug-using-common-runtime.html#common-issues"
                f" to troubleshoot common issue.")
        else:
            return return_code

    @timeout(timeout_seconds=30 * 60,
             timeout_msg='Timed out retrieving debug environment information.',
             prompt_msg='Retrieving debug environment information...')
    def get_execution_container_info(self, bootstrapper_process):
        """
        After execute vm-bootstrapper bin, container name and working_dir path will be written
        to the DEBUG file in current directory.

        :return: container_name, working_dir
        :rtype: str, str
        """
        debug_info_path = os.path.join(self.common_debug_temp_folder, self.DEBUG_FILE)
        while not os.path.exists(debug_info_path) and \
                not self._check_bootstrapper_process_status(bootstrapper_process):
            time.sleep(REQUEST_INTERVAL_SECONDS)

        _az_ml_logger.info(f"Get execution container info from {debug_info_path}")
        with open(debug_info_path, "r") as f:
            lines = f.readlines()
            if len(lines) != 2:
                raise AzureMLException(f"The format of {debug_info_path} is illegal. "
                                       f"Cannot get the container name and working_dir from {debug_info_path}.")
            container_name, working_dir = lines[0].strip(), lines[1].strip()
            return container_name, working_dir

    @timeout(timeout_seconds=TIMEOUT_SECONDS,
             timeout_msg='Timed out of connecting to debug environment.',
             prompt_msg='Connecting to the debug environment. If this is the first time debugging this run, '
                        'it may take a while. Subsequent tries will be faster...')
    def open_vscode(self, container_name, working_dir, bootstrapper_process):

        def wait_for_container_start(container_name, bootstrapper_process):
            docker_client = get_docker_client()
            container = None
            while True:
                try:
                    container = container or docker_client.containers.get(container_name)
                    if container.status == "running":
                        break
                except Exception:
                    time.sleep(REQUEST_INTERVAL_SECONDS)
                # Raise error when bootstrapper binay execution failed.
                self._check_bootstrapper_process_status(bootstrapper_process)

        wait_for_container_start(container_name, bootstrapper_process=bootstrapper_process)
        container_hex_path = json.dumps({"containerName": container_name}).encode("utf-8").hex()
        vscode_command = f'code --folder-uri "vscode-remote://attached-container%2B{container_hex_path}{working_dir}"'
        _az_ml_logger.info(f"Open the working directory, {working_dir}, in the {container_name} in vscode.")
        process = subprocess.Popen(vscode_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                   bufsize=1, encoding='utf-8')
        return_code = process.wait()
        if return_code:
            _az_ml_logger.error(f"When using vscode to attach to the container failed,"
                                f" error details: {process.stdout.read()}\n\t"
                                f"Please attach vscode to the container {container_name} "
                                f"and open the working dir {working_dir} to start debugging.")

    def generate_remove_containers_bash(self, container_name):
        # Create bash to stop and remove container when debug finished
        remove_script = os.path.join(self.common_debug_temp_folder, "remove_containers.sh")
        container_prefix = re.search(r"(\w*-)", container_name).group()
        with open(remove_script, "w") as f:
            f.write(f"docker ps --filter name={container_prefix}* -aq | xargs docker rm -f\n")

            complete_debug_run_command = [
                "from azure.ml.component import Run",
                "from azureml.core.workspace import Workspace",
                "ws = Workspace.get(name='{}', resource_group='{}', subscription_id='{}')".format(
                    self.workspace.name, self.workspace.resource_group,
                    self.workspace.subscription_id),
                "Run.get(workspace=ws, run_id='{}')._core_run.complete()".format(self.debug_run.id)]
            f.write(f"python -c \"exec(\\\"%s\\\")\"" % '\\n'.join(complete_debug_run_command))
        _az_ml_logger.info(f"When the debug is completed, please execute {remove_script}"
                           f" to remove the debug containers and complete the debug run.")
