# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import argparse
import re
import os
import sys
import tempfile

from functools import wraps
from pathlib import Path

from azureml.core import Workspace, Run, ScriptRunConfig
from azure.ml.component._core._component_definition import ComponentType
from azure.ml.component._core._launcher_definition import LauncherType
from azureml.exceptions import UserErrorException
from azure.ml.component._debug._constants import DIR_PATTERN
from azure.ml.component._debug._step_run_debug_helper import DebugOnlineStepRunHelper, _print_step_info, logger, \
    SLEEP_COMMAND, ITP_COMPUTE_TYPE, DebugCommonRuntimeStepHelper
from azure.ml.component.dsl._pipeline_project import _get_telemetry_logger
from azure.ml.component.dsl._utils import _change_working_dir
from azure.ml.component._execution._component_run_helper import MODULE_PROPERTY_NAME
from azure.ml.component._restclients.service_caller_factory import _DesignerServiceCallerFactory
from azure.ml.component._util._loggerfactory import track, _PUBLIC_API, _LoggerFactory
from azure.ml.component._util._telemetry import WorkspaceTelemetryMixin
from azure.ml.component._util._utils import _str_to_bool, _download_snapshot_by_id
from azure.ml.component._api._api import ComponentAPI


class DebugRunner:
    def __init__(self, target=None):
        if target is None:
            target = os.getcwd()
        self.target = target
        self.file_dir = os.path.dirname(os.path.abspath(__file__))
        self.step_run = None
        self.step_detail = None
        self.python_path = None

    def run(self):
        pass

    def run_step(self, setup_func, prepare_func=None):
        # run all steps passed in failed_steps
        @wraps(setup_func)
        def wrapper():
            if prepare_func:
                # Hint to install requirements
                prepare_func()

            return setup_func()

        return wrapper

    @staticmethod
    def hint_to_reopen_in_container(target):
        _print_step_info(f'Please open the generated folder {target} in Vs Code, and reopen in Container '
                         'to start debugging. See detail doc here: https://aka.ms/azureml-component-debug')


class OnlineStepRunDebugger(DebugRunner, WorkspaceTelemetryMixin):
    def __init__(self,
                 url=None,
                 run_id=None,
                 experiment_name=None,
                 workspace_name=None,
                 resource_group=None,
                 subscription_id=None,
                 target=None,
                 dry_run=False,
                 compute=None,
                 runtime=None):
        DebugRunner.__init__(self, target=target)
        if url is not None:
            run_id, experiment_name, workspace_name, resource_group, subscription_id = \
                DebugOnlineStepRunHelper.parse_designer_url(url)
        if all(var is not None for var in
               [run_id, workspace_name, resource_group, subscription_id]):
            self.run_id = run_id
            self.experiment_name = experiment_name
            self.workspace_name = workspace_name
            self.resource_group = resource_group
            self.subscription_id = subscription_id
            self.dry_run = dry_run
            self.compute = compute
            self.runtime = runtime
            self.step_run = None
            self.step_detail = None
            self.service_caller = None
            self.step_id = None
        else:
            raise UserErrorException(
                'One of url or step run params(run_id, workspace_name, '
                'resource_group, subscription_id) should be passed.')
        try:
            self.workspace = Workspace(subscription_id=self.subscription_id, resource_group=self.resource_group,
                                       workspace_name=self.workspace_name)
        except BaseException as e:
            raise UserErrorException(f'Failed to get workspace due to error: {e}')

        # init ws mixin after workspace initialized
        WorkspaceTelemetryMixin.__init__(self, workspace=self.workspace)

        # manually call decorator passing self to decorator
        if compute == 'local':
            if self.runtime == "common":
                # Using common-runtime to create step debug environment.
                self.run = self.run_step(setup_func=self.common_runtime_debug_setup,
                                         prepare_func=DebugCommonRuntimeStepHelper.installed_requirements)
            else:
                # Using step environment to create step debug environment.
                self.run = self.run_step(setup_func=self.local_debug_setup,
                                         prepare_func=DebugOnlineStepRunHelper.installed_requirements)
        else:
            self.run = self.run_step(setup_func=self.remote_debug_setup)

    @track(activity_name="OnlineStepRunDebugger_local_debug", activity_type=_PUBLIC_API)
    def local_debug_setup(self):
        # won't pull image and download data for test
        if '_TEST_ENV' in os.environ:
            logger.warning("Environment variable _TEST_ENV is set, won't pull image and download data.")
            self.dry_run = True
        _print_step_info('Fetching pipeline step run metadata')
        self.step_run = DebugOnlineStepRunHelper.get_pipeline_run(self.run_id, self.workspace)
        self.step_detail = self.step_run.get_details()
        step_id = '%s:%s' % (self.step_run.name, self.step_run.id)
        step_id = re.sub(DIR_PATTERN, '_', step_id)
        self.step_id = step_id
        # This API are only called from CLI currently.
        self.service_caller = _DesignerServiceCallerFactory.get_instance(self.workspace, from_cli=True)

        if MODULE_PROPERTY_NAME not in self.step_detail['properties']:
            # TODO: rename to component when module is deprecated.
            logger.warning(f'Can not find "{MODULE_PROPERTY_NAME}" in step detail, '
                           f'will debug this step as a basic component.')
            component_type = 'basic'
        else:
            component_dto = self.service_caller.get_component_by_id(
                component_id=self.step_detail['properties'][MODULE_PROPERTY_NAME],
                include_run_setting_params=False)
            component_type = component_dto.job_type

        # log trace
        telemetry_values = WorkspaceTelemetryMixin._get_telemetry_value_from_workspace(self.workspace)
        telemetry_values.update({'job_type': component_type})
        _LoggerFactory.trace(_get_telemetry_logger(), "StepRunDebug", telemetry_values)

        with _change_working_dir(Path(self.target) / self.step_id):
            result = True
            # prepare container and it's config
            step_run_image = DebugOnlineStepRunHelper.prepare_dev_container(self.workspace, self.step_run,
                                                                            dry_run=self.dry_run)
            self.python_path = step_run_image.python_path
            # download snapshot
            snapshot_result = DebugOnlineStepRunHelper.download_snapshot(
                self.service_caller, self.step_run, component_type=component_type, dry_run=self.dry_run)
            result = result and snapshot_result
            # download input/output data
            port_arg_map, input_result = DebugOnlineStepRunHelper.prepare_inputs(
                self.workspace, self.step_detail, dry_run=self.dry_run)
            result = result and input_result
            # get run arguments
            script, arguments = DebugOnlineStepRunHelper.prepare_arguments(self.step_id, self.step_detail,
                                                                           port_arg_map, component_type)
            # create vs code debug env
            launch_config_path = DebugOnlineStepRunHelper.create_launch_config(self.step_id, self.python_path,
                                                                               ['${workspaceFolder}/' + script],
                                                                               arguments)
            _print_step_info(f'Created launch config {launch_config_path} for step {self.step_id}')

            # Hint to install vscode extensions
            OnlineStepRunDebugger.hint_to_reopen_in_container(os.getcwd())

            if not result:
                raise RuntimeError('Snapshot/Dataset preparation failed, please prepare them before debugging.')

    @track(activity_name="OnlineStepRunDebugger_remote_debug", activity_type=_PUBLIC_API)
    def remote_debug_setup(self):
        """
        Debug step run in remote compute. If compute=None, it will reuse the compute configuration of step run.

        It can be divided into three parts, validating step run, preparing debug run and getting debug info.
        During validating step run, it will check component type and whether compute is enabled SSH.
        During preparing debug run, it will generate script run config by previous run config and add sleep command to
        debug step command. If command is python style, it will generate launch.json for debugging.
        During getting debug info, it will get the working_directory, script command and ssh connection command.
        """
        logger.info('Preparing to generate debug run...')
        step_run = Run.get(self.workspace, self.run_id)
        details = step_run.get_details()
        # Validate the step run and get the run definition.
        run_definition, component = DebugOnlineStepRunHelper.get_run_definition_by_step_run(step_run)
        compute, compute_type = DebugOnlineStepRunHelper.get_compute_type(self.compute, self.workspace, details)
        run_config = DebugOnlineStepRunHelper.generate_run_config_by_run_definition(run_definition)
        with tempfile.TemporaryDirectory() as tempdir:
            # Download snapshot
            _download_snapshot_by_id(component_api_caller=ComponentAPI(self.workspace, logger=None),
                                     snapshot_id=details['properties']['ContentSnapshotId'], target=tempdir)
            if component.type == ComponentType.DistributedComponent.value and \
                    component._definition.launcher.type == LauncherType.MPI:
                DebugOnlineStepRunHelper.mock_mpi_execute_script(tempdir)

            # Get input/output environment variables
            dataset_environments = DebugOnlineStepRunHelper.get_dataset_environment_variables(
                run_config.command or run_config.arguments, compute_type)
            is_python_command = run_config.script or run_config.command.startswith('python')
            if is_python_command:
                # Generate python debug command for debug, replace reference dataset to environment variables.
                script, arguments = DebugOnlineStepRunHelper.generate_remote_debug_arguments(run_config,
                                                                                             dataset_environments)
                # create vs code debug env
                DebugOnlineStepRunHelper.create_launch_config(
                    step_name=self.run_id, commands=['${workspaceFolder}/' + script],
                    arguments=arguments, working_dir=tempdir,
                    python_path=DebugOnlineStepRunHelper.get_interpreter_path(run_config))

                # Update command of run config.
                run_config.command = run_config.command or ' '.join(['python', run_config.script] +
                                                                    run_config.arguments)
                run_config.script, run_config.arguments = None, []

            add_env_variable_command = ''
            if compute_type in ITP_COMPUTE_TYPE:
                # If running in ITP compute, it will not set input/output path in environment. Add key-value of
                # input/output to /dlts-runtime/env/pod.env which is used to store the environment
                # variable of the step run.
                add_env_variable_command = ''.join(
                    ["(echo 'export %s=%s' | sudo tee -a /dlts-runtime/env/pod.env > /dev/null) && " %
                     (v, k) for k, v in dataset_environments.items()])
            # Add sleep command and environment variables to step run command.
            run_config.command = add_env_variable_command + SLEEP_COMMAND + run_config.command
            # Update compute config of run_config to support SSH when compute is Cmk8s
            DebugOnlineStepRunHelper.update_compute_config(run_config, compute, compute_type)
            # Submit debug run by script config
            script_run_config = ScriptRunConfig(source_directory=tempdir, run_config=run_config)
            debug_run = step_run.experiment.submit(config=script_run_config)
            try:
                run_link = DebugOnlineStepRunHelper.get_debug_run_link(debug_run, compute_type)
                logger.info('Link to debug run: %s' % run_link)
                # Get working directory and command
                working_dir, script_command = DebugOnlineStepRunHelper.get_debug_run_info(
                    debug_run, component, compute_type, dataset_environments)
                # Get SSH connection command
                ssh_connection_command = DebugOnlineStepRunHelper.get_compute_ssh_command(debug_run, compute_type)
                # Show debug info in terminal
                DebugOnlineStepRunHelper.print_debug_info(run_link, working_dir,
                                                          script_command, ssh_connection_command)
                # Show debug steps in terminal
                DebugOnlineStepRunHelper.print_remote_debug_step(debug_run, compute_type,
                                                                 ssh_connection_command, is_python_command)
            except Exception as e:
                debug_run.cancel()
                raise e
        return debug_run

    @track(activity_name="OnlineStepRunDebugger_common_runtime_debug", activity_type=_PUBLIC_API)
    def common_runtime_debug_setup(self):
        # Get run definition by runid
        step_run = Run.get(self.workspace, self.run_id)
        with DebugCommonRuntimeStepHelper(run=step_run) as debug_helper:
            process = None

            try:
                # Call execution service to start a local run
                response = debug_helper.start_local_run()
                # Extra common-runtime info from response
                bootstrapper, job_spec = debug_helper.get_common_runtime_info_by_response(response)

                # Get bootstrapper bin
                bootstrapper_bin = debug_helper.get_bootstrapper_bin(bootstrapper)

                # Execute bootstrapper
                process = debug_helper.execute_bootstrapper(bootstrapper_bin, job_spec)
                # Get container_name and working_dir from DEBUG file.
                container_name, working_dir = debug_helper.get_execution_container_info(process)

                # open the vscode attached to the container
                debug_helper.open_vscode(container_name=container_name,
                                         working_dir=working_dir,
                                         bootstrapper_process=process)
                # create bash to remove containers
                debug_helper.generate_remove_containers_bash(container_name=container_name)
            except Exception as e:
                if process:
                    process.terminate()
                    process.kill()
                if debug_helper.debug_run:
                    debug_helper.debug_run.fail(error_details=e)
                raise e
            if debug_helper.debug_run:
                debug_helper.debug_run.start()


def _entry(argv):
    """CLI tool for component creating."""

    parser = argparse.ArgumentParser(
        prog="python -m azure.ml.component._debug._step_run_debugger",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""A CLI tool for component debugging.""",
    )

    subparsers = parser.add_subparsers()

    # create component folder parser
    debug_parser = subparsers.add_parser(
        'debug',
        description='A CLI tool for online component debugging.'
    )

    debug_parser.add_argument(
        '--subscription_id', '-s', type=str,
        help="Subscription id."
    )
    debug_parser.add_argument(
        '--resource_group', '-r', type=str,
        help="Resource group."
    )
    debug_parser.add_argument(
        '--workspace_name', '-w', type=str,
        help="Workspace name."
    )
    debug_parser.add_argument(
        '--experiment_name', '-e', type=str,
        help="Experiment name."
    )
    debug_parser.add_argument(
        '--run_id', "-i", type=str,
        help="Run id for specific component run."
    )
    debug_parser.add_argument(
        '--target', type=str,
        help="Target directory to build environment, will use current working directory if not specified."
    )
    debug_parser.add_argument(
        "--url", type=str,
        help="Step run url."
    )
    debug_parser.add_argument(
        "--dry_run", type=_str_to_bool,
        help="Dry run."
    )

    debug_parser.add_argument(
        "--compute", type=str,
        help="Compute to execute step, if compute='local', it will debug in local."
    )

    args, _ = parser.parse_known_args(argv)
    params = vars(args)
    _setup_debug(params)


def _setup_debug(params):

    def _to_vars(url=None, run_id=None, experiment_name=None, workspace_name=None, resource_group=None,
                 subscription_id=None, target=None, dry_run=False, compute=None, runtime=None, **kwargs):
        return url, run_id, experiment_name, workspace_name, resource_group, \
            subscription_id, target, dry_run, compute, runtime

    url, run_id, experiment_name, workspace_name, resource_group,\
        subscription_id, target, dry_run, compute, runtime = _to_vars(**params)
    if url is not None:
        debugger = OnlineStepRunDebugger(url=url, target=target, dry_run=dry_run, compute=compute, runtime=runtime)
    elif all(var is not None for var in
             [run_id, workspace_name, resource_group, subscription_id]):
        debugger = OnlineStepRunDebugger(run_id=run_id,
                                         experiment_name=experiment_name,
                                         workspace_name=workspace_name,
                                         resource_group=resource_group,
                                         subscription_id=subscription_id,
                                         target=target,
                                         dry_run=dry_run,
                                         compute=compute,
                                         runtime=runtime)
    else:
        raise RuntimeError(
            'One of url or step run params(run_id, workspace_name, resource_group, '
            'subscription_id) should be passed.')
    debugger.run()


def main():
    """Use as a CLI entry function to use OnlineStepRunDebugger."""
    _entry(sys.argv[1:])


if __name__ == '__main__':
    main()
