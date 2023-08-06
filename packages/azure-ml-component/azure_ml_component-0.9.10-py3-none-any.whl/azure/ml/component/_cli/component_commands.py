# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import logging
import os
import subprocess
import sys
import tempfile
from contextlib import redirect_stdout
from functools import partial
from pathlib import Path
from typing import List, Dict

from azureml.exceptions import UserErrorException
from azureml._base_sdk_common.cli_wrapper._common import get_cli_specific_output, get_workspace_or_default
from azureml._base_sdk_common.common import CLICommandOutput
from azureml.core.authentication import AzureCliAuthentication

from azure.ml.component._api._component_snapshot import LocalComponentSnapshot
from azure.ml.component._util._utils import _try_to_get_workspace
from azure.ml.component._api._api import ModuleAPI, ComponentAPI
from azure.ml.component._cli.utils import _get_default_namespace, _has_user_error_message, \
    _has_azure_ml_not_found_message
from azure.ml.component._restclients.designer.exceptions import ComponentAlreadyExistsError
from azure.ml.component._restclients.designer.models import ModuleDtoFields
from azure.ml.component._util._loggerfactory import _PUBLIC_API, track
from azure.ml.component._util._telemetry import WorkspaceTelemetryMixin
from .transformers import component_definition_to_detail_dict, component_definition_to_summary_dict, \
    component_definition_to_validation_result_dict, component_definition_to_versions_dict


def _get_python_executable_of_command(command):
    """Return the version and python executable of the specific command."""
    content = subprocess.run(
        command + ['-c', "import sys;print('Python %s\\n%s' % (sys.version, sys.executable))"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=(os.name == 'nt')
    )
    return content.stdout.decode().strip()


def _get_available_python(possible_python):
    """Get an available python in user environment."""
    # TODO: make sure this runs fine in Linux
    use_shell = os.name == 'nt'
    for py_cmd in possible_python:
        ret = subprocess.run(py_cmd + ['--version'], stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=use_shell)
        if ret.returncode != 0:
            continue
        # In Python<=3.6, the version is printed in stderr;
        # in Python>=3.7, the version is printed in stdout.
        result = ret.stdout.decode() or ret.stderr.decode()
        if not result.startswith('Python 3'):
            continue
        try:
            minor_version = int(result.split('.')[1])
        except:
            continue
        # Python >= 3.5 is OK.
        if minor_version >= 5:
            return py_cmd


def _get_logger():
    """Get logger for command handler. Used when handler is called directly from CliCommand instead of decorator."""
    try:
        from knack.log import get_logger
        return get_logger(_get_logger.__module__)
    except ImportError:
        return logging.getLogger(_get_logger.__module__)


def _get_cli_args(*args, **kwargs):
    """Generate command line args from function args."""
    args = list(args)
    for k, v in kwargs.items():
        if v is not None:
            if isinstance(v, list):
                # Converting list types args {'arg_name': [val1, val2]} to ['--arg_name', val1, val2].
                args += ['--' + k] + [str(item) for item in v]
            else:
                args += ['--' + k, str(v)]
    return args


def _run_with_subprocess(entry_module, args, use_shell=os.name == 'nt'):
    """Run entry_module related commands with subprocess.

    :param entry_module: entry module path
    :param args: arguments to run the module
    :param use_shell: If az is running in windows, use shell=True to avoid using python
    of CLI since we need python of user env. Need to investigate why this happens and find a better way.
    :return:
    """
    command = ['python']
    args = ['-m', entry_module] + args
    try:
        return _run_command_in_subprocess(command, args, use_shell)
    except ImportError:
        # For ImportError, we directly raise.
        raise
    except BaseException:
        # For other kinds of errors, it may be caused by python environment problems.
        # We try detecting an available python and use the python to run the command.
        possible_python_commands = [['python'], ['python3'], ['py', '-3']]
        available_python = _get_available_python(possible_python_commands)
        if available_python == command:
            raise
        elif available_python is None:
            msg = "No available python environment is found in user environment, please install python>=3.5 and " + \
                  "install azure-ml-component in your environment before using this command."
            raise RuntimeError(msg)
        else:
            return _run_command_in_subprocess(available_python, args, use_shell)


def _run_command_in_subprocess(command, args, use_shell):
    """Run command in subprocess."""
    content = subprocess.run(
        command + args,
        stderr=subprocess.PIPE, stdout=sys.stderr,
        shell=use_shell, env=os.environ,
    )
    stderr = content.stderr.decode()
    if content.returncode == 0:
        if stderr:
            sys.stderr.write(stderr)
        return {}
    else:
        if _has_azure_ml_not_found_message(stderr):
            # This case is caused by import problems, we hint user to install the package.
            python_executable = _get_python_executable_of_command(command=command)
            from azure.ml.component._version import VERSION
            msg = "Please install azure-ml-component==%s before using this command." % VERSION
            msg += "\nYour python command: %s" % (' '.join(command))
            if python_executable:
                msg += "\nYour python executable: %s" % python_executable
            raise ImportError(msg)
        else:
            # Otherwise we store error message to tmp file and guide user to read it.
            tmp_file = tempfile.NamedTemporaryFile(suffix='.log', delete=False)
            try:
                tmp_file.write(content.stderr)
            finally:
                tmp_file.close()
            msg = "happens when executing {}, detailed error messages are here: {}".format(
                command + args, tmp_file.name)
            if _has_user_error_message(stderr):
                # If running command caused UserErrorException, we need to raise a UserErrorException
                raise UserErrorException('UserErrorException {}'.format(msg))
            else:
                # Otherwise we raise a RuntimeError
                raise RuntimeError('Error {}'.format(msg))


def _run_step_run_debugger(args):
    """Run step run debugger related commands with subprocess since it requires dataprep to download dataset.
    It would be easier for user to install it in their own environment."""
    entry_module = 'azure.ml.component._debug._step_run_debugger'
    _run_with_subprocess(entry_module, args)


def _run_pipeline_project(args):
    """Run module project related commands with subprocess since az uses a separated python environment,
    while we need to use user's environment to build his project to avoid dependency issues.
    """
    entry_module = 'azure.ml.component.dsl._pipeline_project'
    _run_with_subprocess(entry_module, args)


def _set_component_as_default(label, logger):
    """Check if we are setting component as default according to label."""
    if label is not None:
        if label.lower() == 'default':
            return True
        else:
            logger.warning("Only \"default\" is supported as label's value for now, got {}. ".format(label))
            return False
    else:
        return False


def _verify_create_params(spec_file, unsupported_args, **kwargs):
    """Verify if param is not supported for module/component create."""
    from azure.ml.component.dsl._pipeline_project import PipelineProject
    if spec_file is not None and PipelineProject.is_project(Path(spec_file)):
        for arg_name, val in kwargs.items():
            if arg_name in unsupported_args and val:
                raise UserErrorException('{} is not supported for batch register.'.format(arg_name))


def _parse_experiment_url(url):
    """Parse workspace and run info from experiment url."""
    try:
        from azure.ml.component._debug._step_run_debug_helper import DebugOnlineStepRunHelper
    except ImportError:
        raise ImportError("Could not import azure ml component debug utility. \
                          Please make sure azure-ml-component is installed.")
    return DebugOnlineStepRunHelper.parse_designer_url(url)


class CLIOperations(WorkspaceTelemetryMixin):
    def __init__(self, workspace, logger):
        """Init module api

        :param workspace: workspace
        :param logger: logger
        :param from_cli: mark if this service caller is used from cli.
        :param imp: api caller implementation
        """
        super().__init__(workspace)
        self.workspace = workspace
        self.logger = logger
        self.api_caller = None
        self.component_cli = False

    def _register(self, register_func, spec_file, fail_if_exists, version, version_error_msg):
        """Register a module/component, execute register_func to register."""
        from azure.ml.component.dsl._pipeline_project import PipelineProject

        # If user passed a module project via spec_file, batch register it
        # NOTE: We assumes all modules inside .moduleproj can be built in same environment
        if spec_file is not None and PipelineProject.is_project(Path(spec_file)):
            # we should use subprocess to make sure dsl.modules could be loaded correctly.
            with redirect_stdout(sys.stderr):
                _run_pipeline_project(_get_cli_args(
                    'register', target=spec_file, workspace_name=self.workspace.name,
                    resource_group=self.workspace.resource_group, subscription_id=self.workspace.subscription_id,
                    version=version
                ))
                return {}
        try:
            component = register_func()
            if not component._module_dto.is_default_module_version:
                self.logger.warning(
                    version_error_msg, component._module_dto.module_version, component._module_dto.default_version)
        except ComponentAlreadyExistsError as e:
            if fail_if_exists:
                raise e
            else:
                self.logger.warning(e.message)
                return {}
        return component_definition_to_detail_dict(component, to_component_dict=self.component_cli)

    def _init(self, source, component_name, job_type, source_dir, inputs, outputs, entry_only):
        if source is None:
            # Init a module from template
            # Here we directly call ModuleProject.init since azure-ml-component is put in the dependency of
            # azureml-cli. There won't be any dependency issue since sample modules don't have special requirements.
            from azure.ml.component.dsl._pipeline_project import PipelineProject
            PipelineProject.init(
                source=source, name=component_name, job_type=job_type, source_dir=source_dir, entry_only=entry_only)
        else:
            # If init from function/dslmodule,
            # we should use subprocess to make sure user function could be loaded correctly.
            return _run_pipeline_project(_get_cli_args(
                'init', source=source, name=component_name,
                type=job_type, source_dir=source_dir,
                inputs=inputs, outputs=outputs,
                entry_only=entry_only
            ))
        return {}

    def _build(self, target, source_dir):
        """Build module from an existing dsl.module."""
        args = _get_cli_args('build', target=target, source_dir=source_dir)
        # We should use subprocess to make sure user dependencies could be loaded correctly.
        return _run_pipeline_project(args)

    def _debug(self, run_id=None, experiment_name=None, target=None, spec_file=None, compute=None, dry_run=None):
        """
        Debug a component in the local or remote compute. It will prepare the required environment, debug configuration
        and the datasets for component debugging.
        If specified a existing step run, according to the compute user can debug in local or remote compute.
        If specified a spec file path, it will prepare the required environment to debug the component locally.

        :param run_id: The existing step run id.
        :type run_id: str
        :param experiment_name: Experiment name of the step run.
        :type experiment_name: str
        :param target: If debug in local machine, the working directory is used to store the debug files.
        :type target: str
        :param spec_file: The path of component spec file.
        :type spec_file: str
        :param compute: The compute is used for step run debugging. If compute is 'local', it will debug locally.
                        If compute is the name of remote compute, it will debug in remote compute.
                        If compute is None, it will reuse the compute config of step run.
        :type compute: str
        :param dry_run: Used to identify test environment.
        :type dry_run: bool
        """
        with redirect_stdout(sys.stderr):
            if spec_file is not None:
                # debug module
                from azure.ml.component._debug._component_debugger import LocalComponentDebugger
                debugger = LocalComponentDebugger(workspace_name=self.workspace.name,
                                                  resource_group=self.workspace.resource_group,
                                                  subscription_id=self.workspace.subscription_id,
                                                  yaml_file=spec_file)
                debugger.run()
            else:
                # debug step run with workspace
                _run_step_run_debugger(
                    _get_cli_args('debug', run_id=run_id, experiment_name=experiment_name,
                                  workspace_name=self.workspace.name,
                                  resource_group_name=self.workspace.resource_group,
                                  subscription_id=self.workspace.subscription_id,
                                  target=target, dry_run=dry_run, compute=compute))

            return {}

    def validate(self, spec_file, package_zip):
        """Validate a module/component."""
        component = self.api_caller.validate(
            spec_file=spec_file,
            package_zip=package_zip
        )
        return component_definition_to_validation_result_dict(component, to_component_dict=self.component_cli)

    def list(self, include_disabled, module_dto_fields=ModuleDtoFields.MINIMAL):
        """List module/component."""
        components = self.api_caller.list(
            include_disabled=include_disabled,
            module_dto_fields=module_dto_fields
        )
        return [component_definition_to_summary_dict(m, to_component_dict=self.component_cli) for m in components]


class CLIModule(CLIOperations):
    def __init__(self, workspace, logger):
        """Init module api

        :param workspace: workspace
        :param logger: logger
        :param from_cli: mark if this service caller is used from cli.
        :param imp: api caller implementation
        """
        super().__init__(workspace, logger)
        if workspace is not None:
            self.api_caller = ModuleAPI(workspace, logger, from_cli=True)
        # indicate this call is from az ml module xxx, the result should contain namespace, print status as Disabled
        self.component_cli = False

    @track(activity_name="CLI_Module_register", activity_type=_PUBLIC_API)
    def register(self, spec_file, package_zip, set_as_default, amlignore_file, fail_if_exists, version):
        """Register a module."""
        _verify_create_params(
            unsupported_args=['package_zip', 'set_as_default', 'amlignore_file', 'fail_if_exists'], **locals())

        register_func = partial(
            self.api_caller.register,
            spec_file=spec_file,
            package_zip=package_zip,
            anonymous_registration=False,
            set_as_default=set_as_default,
            amlignore_file=amlignore_file,
            version=version)
        version_error_msg = 'Registered new version %s, but the module default version kept to be %s.\n' \
                            'Use "az ml module set-default-version" or ' \
                            '"az ml module register --set-as-default-version" to set default version.'

        component_dict = self._register(register_func, spec_file, fail_if_exists, version, version_error_msg)

        return component_dict

    @track(activity_name="CLI_Module_validate", activity_type=_PUBLIC_API)
    def validate(self, spec_file, package_zip):
        """Validate a module."""
        return super(CLIModule, self).validate(spec_file, package_zip)

    @track(activity_name="CLI_Module_list", activity_type=_PUBLIC_API)
    def list(self, include_disabled):
        """List modules."""
        return super(CLIModule, self).list(include_disabled)

    @track(activity_name="CLI_Module_show", activity_type=_PUBLIC_API)
    def show(self, namespace, module_name, component_version):
        """Show a module."""
        namespace = namespace or _get_default_namespace()
        component = self.api_caller.get(
            name=module_name,
            namespace=namespace,
            version=component_version
        )
        return component_definition_to_detail_dict(component, to_component_dict=self.component_cli)

    @track(activity_name="CLI_Module_enable", activity_type=_PUBLIC_API)
    def enable(self, namespace, module_name):
        """Enable a module."""
        namespace = namespace or _get_default_namespace()
        component = self.api_caller.enable(
            name=module_name,
            namespace=namespace
        )
        return component_definition_to_detail_dict(component, to_component_dict=self.component_cli)

    @track(activity_name="CLI_Module_disable", activity_type=_PUBLIC_API)
    def disable(self, namespace, module_name):
        """Disable a module."""
        namespace = namespace or _get_default_namespace()
        component = self.api_caller.disable(
            name=module_name,
            namespace=namespace
        )
        return component_definition_to_detail_dict(component, to_component_dict=self.component_cli)

    @track(activity_name="CLI_Module_set_default_version", activity_type=_PUBLIC_API)
    def set_default_version(self, namespace, module_name, module_version):
        """Set a version to default for module."""
        namespace = namespace or _get_default_namespace()
        component = self.api_caller.set_default_version(
            name=module_name,
            namespace=namespace,
            version=module_version
        )
        return component_definition_to_detail_dict(component, to_component_dict=self.component_cli)

    @track(activity_name="CLI_Module_download", activity_type=_PUBLIC_API)
    def download(self, namespace, module_name, component_version, target_dir, overwrite):
        """Download a module."""
        namespace = namespace or _get_default_namespace()
        file_path = self.api_caller.download(
            name=module_name,
            namespace=namespace,
            version=component_version,
            target_dir=target_dir,
            overwrite=overwrite
        )
        self.logger.warning(
            "Downloaded spec file: {} is the actual spec used for the module. "
            "Compared to the spec inside snapshot, it contains backend processing logic on additional-includes."
            "".format(file_path['module_spec'])
        )
        return file_path

    @track(activity_name="CLI_Module_init", activity_type=_PUBLIC_API)
    def init(self, source, component_name, job_type, source_dir, inputs, outputs, entry_only):
        """Init a module."""
        return self._init(source, component_name, job_type, source_dir, inputs, outputs, entry_only)

    @track(activity_name="CLI_Module_build", activity_type=_PUBLIC_API)
    def build(self, target, source_dir):
        """Build a module."""
        return self._build(target, source_dir)

    @track(activity_name="CLI_Module_debug", activity_type=_PUBLIC_API)
    def debug(self, run_id=None, experiment_name=None, target=None, spec_file=None, compute=None, dry_run=None):
        """Debug a module."""
        return self._debug(run_id, experiment_name, target, spec_file, compute, dry_run)


class CLIComponent(CLIOperations):
    def __init__(self, workspace, logger, registry=None):
        """Init component api

        :param workspace: workspace
        :param logger: logger
        :param from_cli: mark if this service caller is used from cli.
        """
        super().__init__(workspace, logger)
        if workspace is not None or registry:
            self.api_caller = ComponentAPI(workspace, logger, from_cli=True,
                                           registry=registry, auth=AzureCliAuthentication())
        # indicate this call is from az ml component xxx, the result should not contain namespace
        # print status as Archived
        self.component_cli = True

    @staticmethod
    def validate_name_selector(name, version, selector, logger):
        """Validate name, selector, version, label parameter."""
        from azure.ml.component._restclients.service_caller import _resolve_parameter_from_selector

        # TODO: validate one of version and label can be provided.
        if (name is None) == (selector is None):
            raise UserErrorException("One of component name and selector should be specified.")
        if selector is not None:
            name, selector_version = _resolve_parameter_from_selector(selector, logger)
            if selector_version is not None:
                # overwrite version if selector version is not None
                if version is not None:
                    logger.warning("Got version {} from parameter version and {} from parameter selector, "
                                   "{} will be applied.".format(version, selector_version, selector_version))
                version = selector_version
        # Currently archive, restore works only on component container, so won't check version here
        # TODO: validate version should not be None
        return name, version

    @staticmethod
    def get_spec_file_from_manifest_param(spec_file, package_zip, manifest):
        """Verify spec, package and manifest param, return manifest as spec if valid."""
        if spec_file is not None and package_zip is not None:
            raise UserErrorException('Parameter --file and --package can not be specified at the same time.')
        if manifest is not None:
            if package_zip is None:
                raise UserErrorException('Parameter --manifest can only be specified when --package is specified.')
            else:
                spec_file = manifest
        return spec_file

    @track(activity_name="CLI_Component_build", activity_type=_PUBLIC_API)
    def build(self, file, amlignore_file, target_dir):
        """Build a local snapshot of component.

        :param spec_file: The component spec file. Can only be a local file.
        :type spec_file: str
        :param amlignore_file: The .amlignore or .gitignore file used to exclude files/directories in the snapshot.
        :type amlignore_file: Union[str, None]
        :param output_directory: The built snapshot, will be a temp folder if not specified.
        :type output_directory: Union[str, None]
        :return: The component snapshot path.
        :rtype: dict
        """
        # try to build a dsl.component if a python file is specified.
        if file.endswith('.py'):
            file = Path(file).resolve().absolute()
            self.build_spec(target=file, source_dir=file.parent.as_posix())
            file = Path(file).with_suffix('.spec.yaml').as_posix()
        local_snapshot = LocalComponentSnapshot.from_spec(
            spec_file_path=file,
            additional_amlignore_file=amlignore_file,
            snapshot_folder=target_dir,
            logger=self.logger
        )
        snapshot_folder = local_snapshot._get_snapshot_folder()
        return {'snapshot_folder': snapshot_folder.as_posix()}

    @track(activity_name="CLI_Component_create", activity_type=_PUBLIC_API)
    def create(self, spec_file, package_zip, label, amlignore_file, fail_if_exists, version, manifest,
               params_override: List[str] = None):
        """Create a component."""
        _verify_create_params(
            unsupported_args=['package_zip', 'label', 'amlignore_file', 'fail_if_exists', 'manifest', "registry"],
            **locals())
        spec_file = self.get_spec_file_from_manifest_param(spec_file, package_zip, manifest)
        set_as_default = False
        if _set_component_as_default(label, self.logger):
            # set current version as default only when label is default
            set_as_default = True
        params_override_dict = self.params_override_convert_to_dict(params_override)
        # TODO: actually set label for component version
        # TODO: check if version and label both set or both not set in service caller.

        create_func = partial(
            self.api_caller.register,
            spec_file=spec_file,
            package_zip=package_zip,
            anonymous_registration=False,
            set_as_default=set_as_default,
            amlignore_file=amlignore_file,
            version=version,
            params_override=params_override_dict)
        version_error_msg = 'Created new version %s, but the component default version kept to be %s.\n ' \
                            'Use "az ml component update --label default" or ' \
                            '"az ml component create --label default" to set default version.'
        component = self._register(create_func, spec_file, fail_if_exists, version, version_error_msg)

        return component

    @track(activity_name="CLI_Component_validate", activity_type=_PUBLIC_API)
    def validate(self, spec_file, package_zip, manifest):
        """Validate a component."""
        spec_file = self.get_spec_file_from_manifest_param(spec_file, package_zip, manifest)
        return super(CLIComponent, self).validate(spec_file, package_zip)

    @track(activity_name="CLI_Component_list", activity_type=_PUBLIC_API)
    def list(self, include_disabled, name, module_dto_fields=ModuleDtoFields.MINIMAL):
        """List components."""
        if name is not None:
            # when specified name param, get all versions of that component.
            if self.api_caller.registry is None:
                component_dict = self.api_caller.get_versions(component_name=name)
                return [component_definition_to_versions_dict(m) for m in component_dict.values()]
            else:
                # List specified component in registry
                components = self.api_caller.list(include_disabled=include_disabled,
                                                  module_dto_fields=module_dto_fields, name=name)
                return [component_definition_to_versions_dict(m) for m in components]
        else:
            components = self.api_caller.list(include_disabled=include_disabled, module_dto_fields=module_dto_fields)
            return [component_definition_to_summary_dict(m, to_component_dict=self.component_cli) for m in components]

    @track(activity_name="CLI_Component_show", activity_type=_PUBLIC_API)
    def show(self, component_name, component_version, selector):
        """Show a component."""
        component_name, component_version = CLIComponent.validate_name_selector(
            component_name, component_version, selector, self.logger)
        # Won't parse to component definition here, just print the yaml str returned by backend
        rest_component = self.api_caller.imp.get(
            name=component_name,
            version=component_version,
            registry_name=self.api_caller.registry
        )
        # print component spec directly to system out because azure cli doesn't support ordered dict
        print(rest_component.yaml_str)
        return None

    @track(activity_name="CLI_Component_restore", activity_type=_PUBLIC_API)
    def restore(self, component_name, selector):
        """Enable a component."""
        component_name, component_version = CLIComponent.validate_name_selector(
            component_name, None, selector, self.logger)
        if component_version is not None:
            self.logger.warning('Restoring specific version of component is not supported currently, '
                                'all versions of {} will be restored.'.format(component_name))
        component = self.api_caller.enable(
            name=component_name
        )
        return component_definition_to_detail_dict(component, to_component_dict=self.component_cli)

    @track(activity_name="CLI_Component_archive", activity_type=_PUBLIC_API)
    def archive(self, component_name, selector):
        """Disable a component."""

        component_name, component_version = CLIComponent.validate_name_selector(
            component_name, None, selector, self.logger)
        if component_version is not None:
            self.logger.warning('Archiving specific version of component is not supported currently, '
                                'all versions of {} will be archived.'.format(component_name))
        component = self.api_caller.disable(
            name=component_name
        )
        return component_definition_to_detail_dict(component, to_component_dict=self.component_cli)

    @track(activity_name="CLI_Component_update", activity_type=_PUBLIC_API)
    def update(self, component_name, component_version, label, selector, params_override: List[str] = None):
        """Update a component."""
        component_name, component_version = CLIComponent.validate_name_selector(
            component_name, component_version, selector, self.logger)
        params_override_dict = self.params_override_convert_to_dict(params_override)
        if params_override_dict is None:
            params_override_dict = dict()
        if params_override_dict.get('default_version', False):
            raise UserErrorException("Only --label support to modify the default_version")

        if _set_component_as_default(label, self.logger):
            if component_version is None:
                raise UserErrorException("Component version must be set when updating component label.")
            else:
                params_override_dict['default_version'] = component_version
        elif label:
            self.logger.warning("No action will be taken since label is not \"default\".")
            return

        component = self.api_caller.update_component(
            name=component_name,
            params_override=params_override_dict
        )

        return component_definition_to_detail_dict(component, to_component_dict=self.component_cli)

    @track(activity_name="CLI_Component_download", activity_type=_PUBLIC_API)
    def download(self, component_name, component_version, target_dir, overwrite, selector):
        """Download a component."""
        component_name, component_version = CLIComponent.validate_name_selector(
            component_name, component_version, selector, self.logger)
        file_path = self.api_caller.download(
            name=component_name,
            version=component_version,
            target_dir=target_dir,
            overwrite=overwrite
        )
        self.logger.warning(
            "Downloaded spec file: {} is the actual spec used for the component. "
            "Compared to the spec inside snapshot, it contains backend processing logic on additional-includes."
            "".format(file_path['component_spec'])
        )
        return file_path

    @track(activity_name="CLI_Component_init", activity_type=_PUBLIC_API)
    def init(self, source, component_name, job_type, source_dir, inputs, outputs, entry_only):
        """Init a component."""
        return self._init(source, component_name, job_type, source_dir, inputs, outputs, entry_only)

    @track(activity_name="CLI_Component_build_spec", activity_type=_PUBLIC_API)
    def build_spec(self, target, source_dir):
        """Build a component."""
        self._build(target, source_dir)

    @track(activity_name="CLI_Component_debug", activity_type=_PUBLIC_API)
    def debug(self, run_id=None, experiment_name=None, target=None, spec_file=None, compute=None, dry_run=None):
        """Debug a component."""
        return self._debug(run_id, experiment_name, target, spec_file, compute, dry_run)

    @track(activity_name="CLI_Component_export", activity_type=_PUBLIC_API)
    def export(self, draft_id, run_id, path, export_format):
        """Export pipeline to code."""
        try:
            from azure.ml.component._graph_to_code import _export_pipeline_draft_to_code, _export_pipeline_run_to_code
            from azureml.pipeline.core import PipelineRun
        except ImportError:
            raise ImportError("Could not import azure ml component graph-to-code utility. \
                              Please make sure azure-ml-component is installed.")

        if draft_id is None and run_id is None:
            raise ValueError("One of --draft-id or --run-id should be specified")

        if draft_id is not None and run_id is not None:
            raise ValueError("Cannot specify both --draft-id and --run-id at the same time")

        format_mapping = {
            "python": "Python",
            "py": "Python",
            "jupyternotebook": "JupyterNotebook",
            "ipynb": "JupyterNotebook"
        }
        normallized_export_format = format_mapping.get(export_format.lower())
        if normallized_export_format is None:
            raise ValueError(
                "The specified export_format: {} is not supported. Use python or jupyternotebook".format(
                    export_format))

        if path is None:
            path = os.getcwd()
        if not os.path.exists(path):
            raise ValueError("The specified path: {} does not exist.".format(path))

        saved_to = None
        if draft_id is not None:
            saved_to = _export_pipeline_draft_to_code(workspace=self.workspace,
                                                      draft_id=draft_id,
                                                      path=path,
                                                      export_format=normallized_export_format)
            command_output = CLICommandOutput("Successfully export pipeline draft {} to {}".format(draft_id, saved_to))

        if run_id is not None:
            pipeline_run = PipelineRun.get(workspace=self.workspace, run_id=run_id)
            saved_to = _export_pipeline_run_to_code(workspace=self.workspace,
                                                    pipeline_run_id=run_id,
                                                    path=path,
                                                    export_format=normallized_export_format,
                                                    experiment_name=pipeline_run.experiment.name,
                                                    experiment_id=pipeline_run.experiment.id)
            command_output = CLICommandOutput("Successfully export pipeline run {} to {}".format(run_id, saved_to))

        command_output.set_do_not_print_dict()
        return get_cli_specific_output(command_output)

    @staticmethod
    def params_override_convert_to_dict(params_override: List[str] = None) -> Dict:
        if params_override is None:
            return None
        if not isinstance(params_override, list):
            raise TypeError(f'params_override_convert_to_dict function receives a list, set={params_override}')
        ret = dict()
        # ['tags.url=microsoft.com','tags.python=3.7','environment.name=AzureML','description=test']
        for item in params_override:
            property_list = item.split('=')
            if len(property_list) < 2:
                raise UserErrorException(f'--set format error, {item} should be in format: key=value')
            key_list = property_list[0].split('.')
            tmp = ret
            for key_item in key_list[:-1]:
                tmp[key_item] = tmp.get(key_item, {})
                tmp = tmp[key_item]
            tmp[key_list[-1]] = '='.join(property_list[1:])

        return ret


def _build_component_snapshot(spec_file, amlignore_file, target_dir, logger=None):
    if logger is None:
        logger = _get_logger()
    workspace = _try_to_get_workspace()
    cli_component = CLIComponent(workspace, logger)
    return cli_component.build(
        file=spec_file, amlignore_file=amlignore_file, target_dir=target_dir)


def _create_component(workspace_name, resource_group_name, subscription_id, spec_file, package_zip, label,
                      amlignore_file, fail_if_exists, version, manifest, registry, logger=None, set: List[str] = None):
    if logger is None:
        logger = _get_logger()
    if registry and not workspace_name:
        workspace = None
    else:
        workspace = get_workspace_or_default(subscription_id=subscription_id, resource_group=resource_group_name,
                                             workspace_name=workspace_name)
    cli_component = CLIComponent(workspace, logger, registry)
    return cli_component.create(spec_file=spec_file, package_zip=package_zip,
                                label=label, amlignore_file=amlignore_file,
                                fail_if_exists=fail_if_exists, version=version,
                                manifest=manifest, params_override=set)


def _validate_component(
        workspace_name, resource_group_name, subscription_id, spec_file, package_zip, manifest, logger=None):
    if logger is None:
        logger = _get_logger()
    workspace = get_workspace_or_default(subscription_id=subscription_id, resource_group=resource_group_name,
                                         workspace_name=workspace_name)
    component_cli = CLIComponent(workspace, logger)
    return component_cli.validate(spec_file=spec_file, package_zip=package_zip, manifest=manifest)


def _list_component(
        workspace_name, resource_group_name, subscription_id, include_disabled, component_name, registry,
        logger=None, module_dto_fields=ModuleDtoFields.MINIMAL):
    if logger is None:
        logger = _get_logger()
    if registry and not workspace_name:
        workspace = None
    else:
        workspace = get_workspace_or_default(subscription_id=subscription_id, resource_group=resource_group_name,
                                             workspace_name=workspace_name)
    component_cli = CLIComponent(workspace, logger, registry)

    return component_cli.list(include_disabled=include_disabled, name=component_name,
                              module_dto_fields=module_dto_fields)


def _show_component(workspace_name, resource_group_name, subscription_id, component_name, component_version, selector,
                    registry=None, logger=None):
    if logger is None:
        logger = _get_logger()
    if registry and not workspace_name:
        workspace = None
    else:
        workspace = get_workspace_or_default(subscription_id=subscription_id, resource_group=resource_group_name,
                                             workspace_name=workspace_name)
    component_cli = CLIComponent(workspace, logger, registry)
    return component_cli.show(component_name=component_name, component_version=component_version, selector=selector)


def _restore_component(workspace_name, resource_group_name, subscription_id, component_name, selector, logger=None):
    if logger is None:
        logger = _get_logger()
    workspace = get_workspace_or_default(subscription_id=subscription_id, resource_group=resource_group_name,
                                         workspace_name=workspace_name)
    component_cli = CLIComponent(workspace, logger)
    return component_cli.restore(component_name=component_name, selector=selector)


def _archive_component(workspace_name, resource_group_name, subscription_id, component_name, selector, logger=None):
    if logger is None:
        logger = _get_logger()
    workspace = get_workspace_or_default(subscription_id=subscription_id, resource_group=resource_group_name,
                                         workspace_name=workspace_name)
    component_cli = CLIComponent(workspace, logger)
    return component_cli.archive(component_name=component_name, selector=selector)


def _component_update(workspace_name, resource_group_name, subscription_id, component_name, selector,
                      component_version, label, logger=None, set: List[str] = None):
    if logger is None:
        logger = _get_logger()
    workspace = get_workspace_or_default(subscription_id=subscription_id, resource_group=resource_group_name,
                                         workspace_name=workspace_name)
    component_cli = CLIComponent(workspace, logger)
    return component_cli.update(
        component_name=component_name, component_version=component_version, label=label,
        selector=selector, params_override=set)


def _download_component(workspace_name, resource_group_name, subscription_id, component_name, selector,
                        component_version, target_dir, overwrite, logger=None):
    if logger is None:
        logger = _get_logger()
    workspace = get_workspace_or_default(subscription_id=subscription_id, resource_group=resource_group_name,
                                         workspace_name=workspace_name)
    component_cli = CLIComponent(workspace, logger)
    return component_cli.download(component_name, component_version, target_dir, overwrite, selector=selector)


def _init_component(source, component_name, job_type, source_dir, inputs, outputs, entry_only, logger=None):
    """Entrance of component init."""
    workspace = _try_to_get_workspace()
    component_cli = CLIComponent(workspace, logger)
    return component_cli.init(source, component_name, job_type, source_dir, inputs, outputs, entry_only)


def _build_component_spec(target, source_dir, logger=None):
    """Entrance of component build."""
    workspace = _try_to_get_workspace()
    component_cli = CLIComponent(workspace, logger)
    return component_cli.build_spec(target, source_dir)


def _debug_component(run_id=None,
                     experiment_name=None,
                     url=None,
                     target=None,
                     spec_file=None,
                     compute=None,
                     dry_run=None,
                     subscription_id=None, resource_group_name=None, workspace_name=None):
    """Entrance of component debug."""
    # parse workspace
    if url is not None:
        run_id, experiment_name, workspace_name, resource_group_name, subscription_id = _parse_experiment_url(url)
    workspace = get_workspace_or_default(subscription_id=subscription_id, resource_group=resource_group_name,
                                         workspace_name=workspace_name)
    component_cli = CLIComponent(workspace, None)
    return component_cli.debug(run_id, experiment_name, target, spec_file, compute, dry_run)


def _debug_module(run_id=None,
                  experiment_name=None,
                  url=None,
                  target=None,
                  spec_file=None,
                  compute=None,
                  dry_run=None,
                  subscription_id=None, resource_group_name=None, workspace_name=None):
    """Entrance of module debug."""
    # parse workspace
    if url is not None:
        run_id, experiment_name, workspace_name, resource_group_name, subscription_id = _parse_experiment_url(url)
    workspace = get_workspace_or_default(subscription_id=subscription_id, resource_group=resource_group_name,
                                         workspace_name=workspace_name)
    module_cli = CLIModule(workspace, None)
    return module_cli.debug(run_id, experiment_name, target, spec_file, compute, dry_run)


def _export(url, draft_id, run_id, path, export_format,
            subscription_id=None, resource_group_name=None, workspace_name=None):
    """Export pipeline draft or pipeline run as sdk code."""
    # Note: put export to module_commands because cli requires all handler function in same package
    # TODO: keep one _export (remove export_pipeline from cmd_pipeline)
    try:
        from azure.ml.component._graph_to_code import _parse_designer_url
    except ImportError:
        raise ImportError("Could not import azure ml component graph-to-code utility. \
                          Please make sure azure-ml-component is installed.")

    if url is not None:
        subscription_id, resource_group_name, workspace_name, draft_id, run_id, *_ = _parse_designer_url(url)

    workspace_object = get_workspace_or_default(subscription_id=subscription_id,
                                                resource_group=resource_group_name,
                                                workspace_name=workspace_name)
    component_cli = CLIComponent(workspace_object, None)
    return component_cli.export(draft_id=draft_id, run_id=run_id, path=path, export_format=export_format)
