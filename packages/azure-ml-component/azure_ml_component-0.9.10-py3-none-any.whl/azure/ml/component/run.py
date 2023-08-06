# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Defines classes for submitted runs, including classes for checking status and retrieving run details."""
import json
import os
import re
import sys
import tempfile
import time
from typing import List
from pathlib import Path

from azureml.core import ScriptRun, Experiment, Run as CoreRun
from azure.core.pipeline import PipelineResponse
from azureml.data.datapath import DataPath
from azureml.core.datastore import Datastore
from azureml.data.azure_data_lake_datastore import AzureDataLakeDatastore
from azureml.exceptions import ExperimentExecutionException, ActivityFailedException
from azureml._execution import _commands
from azureml._restclient.utils import create_session_with_retry
from azureml._restclient.workspace_client import WorkspaceClient
from azureml.exceptions._azureml_exception import UserErrorException

from ._restclients.designer.models import SubmitPipelineRunRequest as ResubmitPipelineRunRequest
from ._restclients.designer.models._designer_service_client_enums import RunStatus
from ._restclients.service_caller_factory import _DesignerServiceCallerFactory
from ._util._loggerfactory import _LoggerFactory, _PUBLIC_API, track
from ._util._telemetry import WorkspaceTelemetryMixin
from ._util._utils import _is_prod_workspace, _get_enum, enabled_subpipeline_registration, \
    resolve_pipeline_parameters, get_pipeline_response_content
from ._visible import Visible
from ._visualization_context import VisualizationContext

RUNNING_STATES = [RunStatus.NOT_STARTED, RunStatus.STARTING,
                  RunStatus.PREPARING, RunStatus.QUEUED, RunStatus.RUNNING, RunStatus.FINALIZING]
# align with UX query status interval
REQUEST_INTERVAL_SECONDS = 5
GENERAL_ERROR_MESSAGE = 'Error: Detailed error not set on the Run. Please check the logs for details.'

_logger = None


def _get_logger():
    global _logger
    if _logger is not None:
        return _logger
    _logger = _LoggerFactory.get_logger()
    return _logger


class _Output(WorkspaceTelemetryMixin):
    """Represents an output object of a :class:`azure.ml.component.Component`."""

    def __init__(self, name, _type, run):
        """
        Initialize a Output object.

        :param name: The name of the output.
        :type name: str.
        :param _type: The type of the output.
        :type _type: str.
        :param run: The associated Run object.
        :type run: azure.ml.component.Run
        """
        self._name = name
        self._type = _type
        self._run = run
        self._workspace = self._run.workspace
        WorkspaceTelemetryMixin.__init__(self, workspace=self._workspace)

    def __repr__(self):
        """Return str(self)."""
        return self.__str__()

    def __str__(self):
        """Return the description of a Output object."""
        return "Output(Name:{},\nType:{},\nStepRun:{})".format(self._name, self._type, self._run)

    @property
    def _run_outputs(self):
        """
        Return the PipelineStepRunOutputs object.

        The PipelineStepRunOutputs object contains much information about the pipeline.

        :return: The PipelineStepRunOutputs object.
        :rtype: azure.ml.component._restclients.designer.models.PipelineStepRunOutputs
        """
        service_caller = _DesignerServiceCallerFactory.get_instance(self._workspace)
        return service_caller.get_pipeline_run_step_outputs(
            self._run._properties['azureml.pipelinerunid'], self._run._get_node_id(),
            self._run.id)

    @property
    def name(self):
        """
        Return the output name.

        The name of a output.

        :return: The output name.
        :rtype: str
        """
        return self._name

    @property
    def run(self):
        """
        Return the Run object.

        An Output object is associated with a Run object.

        :return: The Run object.
        :rtype: azure.ml.component.Run
        """
        return self._run

    @property
    def type(self):
        """
        Return the output type.

        The type of a output.

        :return: The output type.
        :rtype: str
        """
        return self._type

    @track(activity_type=_PUBLIC_API)
    def download(self, local_path: str = None, overwrite: bool = False, show_progress: bool = True):
        """
        Download the data of the output.

        .. remarks::

            download() returns None in below cases:
                (1) the status of :class:azure.ml.component.Run is not in completed state or
                in completed state in the first few seconds.
                (2) the output does not generate any output files.

        :param local_path: Local path to download to. Defaults to None
        :type local_path: str, optional
        :param overwrite: Indicates whether to overwrite existing files. Defaults to False.
        :type overwrite: bool, optional
        :param show_progress: Indicates whether to show the progress of the download in the console.
            Defaults to True.
        :type show_progress: bool, optional
        :return: The path where the files are saved.
        :rtype: str
        """
        if not local_path:
            local_path = tempfile.gettempdir()
        else:
            try:
                Path(local_path).resolve()
            except OSError:
                raise UserErrorException("local_path is not a valid path string, {0}".format(local_path))
        data_path = self.get_data_path()
        if not data_path:
            return None

        if isinstance(data_path._datastore, AzureDataLakeDatastore):
            raise UserErrorException("download is not supported for azure data lake store.")

        data_path._datastore.download(target_path=local_path, prefix=data_path.path_on_datastore,
                                      overwrite=overwrite,
                                      show_progress=show_progress)
        saved_path = os.path.normpath(os.path.join(local_path, data_path.path_on_datastore))
        if not os.path.exists(saved_path):
            return None
        return saved_path

    @track(activity_type=_PUBLIC_API)
    def get_data_path(self) -> DataPath:
        """
        Get the Data object associated with the specific output.

        :return: The Data object associated with the specific output.
        :rtype: object
        """
        module_name_for_dir = re.sub(pattern=' ', repl='_', string=self._name)
        port_outputs = self._run_outputs.port_outputs
        if module_name_for_dir not in port_outputs:
            return None
        output = port_outputs[module_name_for_dir]
        path_on_datastore = output.relative_path
        data_store_name = output.data_store_name
        datastore = Datastore.get(self._workspace, data_store_name)
        data_path = DataPath(datastore=datastore, path_on_datastore=path_on_datastore)
        return data_path


class Run(Visible, WorkspaceTelemetryMixin):
    """Represents a run of a :class:`azure.ml.component.Component`."""

    def __init__(self, experiment, run_id=None):
        """
        Initialize a Run object.

        :param experiment: The experiment object associated with the pipeline run.
        :type experiment: azureml.core.Experiment
        :param run_id: The run's id.
        :type run_id: str
        """
        self._core_run = CoreRun(experiment=experiment, run_id=run_id)
        self._is_pipeline_run = self._type == 'azureml.PipelineRun'
        self._run_details_url = self._core_run._run_details_url
        WorkspaceTelemetryMixin.__init__(self, workspace=self.workspace)
        self._visualization_dict = None
        self._run_outputs = None

    @property
    def id(self):
        """Get run ID.

        The ID of the run is an identifier unique across the containing experiment.

        :return: The run ID.
        :rtype: str
        """
        return self._core_run.id

    @property
    def _id(self):
        """Get run ID."""
        return self.id

    @property
    def _name(self):
        """Return the run name.

        The optional name of the run is a user-specified string useful for later identification of the run.

        :return: The run ID.
        :rtype: str
        """
        return self._core_run.name

    @property
    def _type(self):
        """Get run type.

        Indicates how the run was created or configured.

        :return: The run type.
        :rtype: str
        """
        return self._core_run.type

    @property
    def _experiment(self):
        """Get experiment containing the run.

        :return: Retrieves the experiment corresponding to the run.
        :rtype: azureml.core.Experiment
        """
        return self._core_run.experiment

    @property
    def workspace(self):
        """
        Return the workspace containing the experiment.

        :return: The workspace object.
        :rtype: azureml.core.Workspace
        """
        return self._experiment.workspace

    @property
    def _status(self):
        """Return the run object's status."""
        return self._core_run.status

    @property
    def _properties(self):
        """Return the immutable properties of this run.

        .. remarks::

            Properties include immutable system-generated information such as
            duration, date of execution, user, etc.

        :return: The locally cached properties of the run.
        :rtype: dict[str] or str
        """
        return self._core_run.properties

    @property
    def _tags(self):
        """Return the set of mutable tags on this run.

        :return: The tags stored on the run object.
        :rtype: dict
        """
        return self._core_run.tags

    @property
    def _run_dto(self):
        """Return the internal representation of a run."""
        return self._core_run._run_dto

    @property
    def _parent_run(self):
        return self._core_run.parent

    @property
    def _is_reused(self):
        return self._properties.get('azureml.reusedrunid') is not None

    @track(activity_type=_PUBLIC_API, activity_name='Run_get_portal_url')
    def get_portal_url(self):
        """Azure portal url for the current run."""
        return self._core_run.get_portal_url()

    @track(activity_type=_PUBLIC_API, activity_name='Run_get_lineage')
    def get_lineage(self):
        """
        Return lineage run and type.

        :return: The lineage run object and type formatted as {'from': from_run_object, 'type': lineage_type},
            possible values of 'type' are ['cloned', 'resubmit']. Return value is None if no lineage run exists.
        :rtype: dict
        """
        from_id = self._properties.get('azureml.sourcepipelinerunid')
        if not from_id:
            return None
        lineage_type = self._properties.get('azureml.runLineageType')
        try:
            from_run = Run.get(workspace=self.workspace, run_id=from_id)
        except Exception as e:
            _get_logger().warning(
                f'Found lineage run with type {lineage_type!r} id {from_id!r} but get run failed with {e}')
            raise e
        return {'from': from_run, 'type': lineage_type}

    def _get_portal_url(self):
        """Azure portal url for the current run."""
        return self.get_portal_url()

    @track()
    def _get_children(self, recursive=False, tags=None, properties=None, type=None, status=None, _rehydrate_runs=True):
        """Get all children for the current run selected by specified filters.

        :param recursive: Indicates whether to recurse through all descendants.
        :type recursive: bool
        :param tags:  If specified, returns runs matching specified *"tag"* or {*"tag"*: *"value"*}.
        :type tags: str or dict
        :param properties: If specified, returns runs matching specified *"property"* or {*"property"*: *"value"*}.
        :type properties: str or dict
        :param type: If specified, returns runs matching this type.
        :type type: str
        :param status: If specified, returns runs with status specified *"status"*.
        :type status: str
        :param _rehydrate_runs: Indicates whether to instantiate a run of the original type
            or the base Run.
        :type _rehydrate_runs: bool
        :return: A list of :class:`azure.ml.component.Run` objects.
        :rtype: builtin.list
        """
        raw_children = self._core_run.get_children(recursive=recursive, tags=tags, properties=properties, type=type,
                                                   status=status, _rehydrate_runs=_rehydrate_runs)
        return [Run(run.experiment, run.id) for run in raw_children]

    @track()
    def _get_tags(self):
        """Get tags of the current run."""
        return self._core_run.get_tags()

    @track()
    def _get_details(self):
        """Get the definition, status information, current log files, and other details of the run."""
        return self._core_run.get_details()

    def _get_base_info_dict(self):
        return self._core_run._get_base_info_dict()

    @track(activity_type=_PUBLIC_API, is_long_running=True)
    def wait_for_completion(self, show_output: bool = None, show_graph: bool = True,
                            timeout_seconds: int = sys.maxsize, raise_on_error: bool = True):
        """
        Wait for the completion of this run.

        Returns the status after the wait.

        :param show_output: Indicates whether to show the run status on sys.stdout.
        :type show_output: bool
        :param show_graph: Indicates whether to show the graph with run status on notebook.
         If not in notebook environment, overwrite this value to False. Only works for a PipelineRun for now.
        :type show_graph: bool
        :param timeout_seconds: The number of seconds to wait before timing out.
        :type timeout_seconds: int
        :param raise_on_error: Indicates whether to raise an error when the run is in a failed state.
        :type raise_on_error: bool

        :return: The final status.
        :rtype: str
        """
        if self._is_pipeline_run:
            return self._wait_for_pipeline_run_completion(show_output, show_graph, timeout_seconds, raise_on_error)
        else:
            return self._wait_for_step_run_completion(show_output, timeout_seconds, raise_on_error)

    def _wait_for_pipeline_run_completion(self, show_output: bool = None, show_graph: bool = True,
                                          timeout_seconds: int = sys.maxsize, raise_on_error: bool = True):
        print('PipelineRunId:', self.id)
        print('Link to Azure Machine Learning Portal:', self.get_portal_url())

        start_time = time.time()
        status = self._get_run_status()
        can_visualize = self._can_visualize()

        # in a can-visualize environment, set show_output=False
        if show_output is None:
            show_output = not can_visualize

        # in a cannot-visualize environment:
        # set show_graph=False, and set show_output=True to show the details of pipeline run
        if not can_visualize and show_graph:
            self._visualize_not_support_warning(only_show_in_notebook=False)
            print('Fall back to show output on console.')
            show_graph = False

        if show_graph:
            visualizer = self._get_visualizer()
            self._update_graph_visualization(visualizer)
            self._add_visualize_telemetry_value(can_visualize)

        def timeout(start_time: float, timeout_seconds: float):
            elapsed_time = time.time() - start_time
            if elapsed_time > timeout_seconds:
                print('Timed out of waiting. Elapsed time:', elapsed_time)
                return True
            return False

        processed_step_runs = []
        old_status = None
        while status in RUNNING_STATES:
            children = self._get_children(_rehydrate_runs=False)
            if show_output:
                try:
                    if not status == old_status:
                        old_status = status
                        print('PipelineRun Status:', status.value)
                    for step_run in children:
                        if step_run._id not in processed_step_runs and not Run._is_terminal_state(step_run._core_run):
                            processed_step_runs.append(step_run._id)
                            time_elapsed = time.time() - start_time
                            print('\n')
                            _step_run = Run(self._experiment, run_id=step_run._id)
                            _step_run.wait_for_completion(show_output=show_output,
                                                          timeout_seconds=timeout_seconds - time_elapsed,
                                                          raise_on_error=raise_on_error)
                            print('')
                except KeyboardInterrupt:
                    error_message = "The output streaming for the run interrupted.\n" \
                                    "But the run is still executing on the compute target. \n" \
                                    "Details for canceling the run can be found here: " \
                                    "https://aka.ms/aml-docs-cancel-run"
                    raise ExperimentExecutionException(error_message)
            if show_graph:
                self._update_graph_visualization(visualizer, update_urls=True,
                                                 update_logs=visualizer.server_avaliable())

            if timeout(start_time, timeout_seconds):
                break
            time.sleep(REQUEST_INTERVAL_SECONDS)
            status = self._get_run_status()

        final_details = self._get_details()
        warnings = final_details.get("warnings")
        error = self._get_detailed_error()

        if show_output:
            summary_title = '\nPipelineRun Execution Summary'
            print(summary_title)
            print('=' * len(summary_title))
            print('PipelineRun Status:', status.value)
            if warnings:
                messages = [x.get("message") for x in warnings if x.get("message")]
                if len(messages) > 0:
                    print('\nWarnings:')
                    for message in messages:
                        print(message)
            if error:
                print('\nError:')
                print(json.dumps(error, indent=4))

            print(final_details)
            print('', flush=True)

        if show_graph:
            # do one more extra update to ensure the final status is sent
            self._update_graph_visualization(visualizer, update_urls=True, update_logs=True,
                                             raise_on_error=raise_on_error)

        if error and raise_on_error:
            raise ActivityFailedException(error_details=json.dumps(error, indent=4))

        return status

    def _wait_for_step_run_completion(self, show_output: bool = None,
                                      timeout_seconds: int = sys.maxsize,
                                      raise_on_error: bool = True):
        if show_output:
            try:
                print('StepRunId:', self.id)
                print('Link to Azure Machine Learning Portal:', self.get_portal_url())
                return self._stream_run_output(timeout_seconds=timeout_seconds,
                                               raise_on_error=raise_on_error)
            except KeyboardInterrupt:
                error_message = "The output streaming for the run interrupted.\n" \
                                "But the run is still executing on the compute target. \n" \
                                "Details for canceling the run can be found here: " \
                                "https://aka.ms/aml-docs-cancel-run"

                raise ExperimentExecutionException(error_message)
        else:
            status = self._get_status()
            while status in RUNNING_STATES:
                time.sleep(REQUEST_INTERVAL_SECONDS)
                status = self._get_status()

            error = self._get_detailed_error()
            if error and raise_on_error:
                raise ActivityFailedException(error_details=json.dumps(error, indent=4))

            return status

    def _stream_run_output(self, timeout_seconds: int = sys.maxsize, raise_on_error: bool = True):
        """
        Stream the experiment run output to the specified file handle.

        :param timeout_seconds: Number of seconds to wait before timing out.
        :type sys.timeout_seconds: int
        :param raise_on_error: Indicates whether to raise an error when the Run is in a failed state
        :type raise_on_error: bool
        :return: The status of the run
        :rtype: str
        """
        def incremental_print(log, num_printed):
            count = 0
            for line in log.splitlines():
                if count >= num_printed:
                    print(line)
                    num_printed += 1
                count += 1
            return num_printed

        num_printed_lines = 0
        current_log = None

        start_time = time.time()
        session = create_session_with_retry()

        old_status = None
        status = self._get_status()
        while status in RUNNING_STATES:
            if not status == old_status:
                old_status = status
                print('StepRun(' + self._name + ') Status: ' + status)

            current_details = self._get_details()
            available_logs = [x for x in current_details["logFiles"]
                              if re.match(r"azureml-logs/[\d]{2}.+\.txt", x)]
            available_logs.sort()
            next_log = ScriptRun._get_last_log_primary_instance(available_logs) if available_logs else None

            if available_logs and current_log != next_log:
                num_printed_lines = 0
                current_log = next_log
                print("\nStreaming " + current_log)
                print('=' * (len(current_log) + 10))

            if current_log:
                current_log_uri = current_details["logFiles"].get(current_log)
                if current_log_uri:
                    content = _commands._get_content_from_uri(current_log_uri, session)
                    num_printed_lines = incremental_print(content, num_printed_lines)

            if time.time() - start_time > timeout_seconds:
                print('Timed out of waiting. Elapsed time:', time.time() - start_time)
                break
            time.sleep(REQUEST_INTERVAL_SECONDS)
            status = self._get_status()

        summary_title = '\nStepRun(' + self._name + ') Execution Summary'
        print(summary_title)
        print('=' * len(summary_title))
        print('StepRun(' + self._name + ') Status: ' + status)

        final_details = self._get_details()
        warnings = final_details.get("warnings")
        if warnings:
            messages = [x.get("message") for x in warnings if x.get("message")]
            if len(messages) > 0:
                print('\nWarnings:')
                for message in messages:
                    print(message)

        error = self._get_detailed_error()

        if error and not raise_on_error:
            print('\nError:')
            print(json.dumps(error, indent=4))
        if error and raise_on_error:
            raise ActivityFailedException(error_details=json.dumps(error, indent=4))

        print(final_details)
        print('', flush=True)

        return status

    @track(activity_type=_PUBLIC_API, activity_name="PipelineRun_export_code")
    def _export_code(self, directory=None):
        """
        Export pipeline to python files.

        This is an experimental function, will be changed anytime.

        :param directory: The target directory path. Default current working directory
            path will be used if not provided.
        :type directory: str
        :return: The directory path
        :rtype: str
        """
        from azure.ml.component._graph_to_code import _get_default_output_file_name, _save_graph_sdk_code

        if directory is None:
            directory = os.getcwd()
        if not os.path.exists(directory):
            raise UserErrorException('Target directory not exists, path {}'.format(directory))
        elif not os.path.isdir(directory):
            raise UserErrorException('Expected a directory path , got {}'.format(directory))

        export_format = 'Python'
        service_caller = _DesignerServiceCallerFactory.get_instance(self.workspace)
        result = service_caller.get_pipeline_run_sdk_code(
            pipeline_run_id=self.id, target_code=export_format,
            experiment_id=self._experiment.id, experiment_name=self._experiment.name)

        default_out_file_name = _get_default_output_file_name(export_format=export_format, run_id=self.id)
        export_path = _save_graph_sdk_code(result, directory, default_out_file_name)
        print('Successfully dump pipeline run graph to python files at {}'.format(export_path))
        return export_path

    @classmethod
    def get(cls, workspace, run_id):
        """Get the run for this workspace with its run ID.

        :param workspace: The containing workspace.
        :type workspace: azureml.core.Workspace
        :param run_id: The run ID.
        :type run_id: string
        :return: The submitted run.
        :rtype: azure.ml.component.Run
        """
        client = WorkspaceClient(workspace.service_context)
        run_dto = client.get_run(run_id)

        experiment_dto = client.get_experiment_by_id(run_dto.experiment_id)
        experiment = Experiment(
            workspace,
            experiment_dto.name,
            _id=experiment_dto.experiment_id,
            _archived_time=experiment_dto.archived_time,
            _create_in_cloud=False,
            _experiment_dto=experiment_dto)
        return Run(experiment, run_id)

    @classmethod
    def _get_status_from_raw_value(cls, run_status):
        """Return the status enum according to the raw status from backend."""
        # In a recent change, the run_status will be string instead of int.
        # Here we check both run status index and string value to make sure backward compatibility.
        return _get_enum(run_status, RunStatus)

    @classmethod
    def _is_terminal_state(cls, core_run):
        """
        Check whether run is in terminal state.

        When run exists, if run status is Completed or Failed, it will return True, else return False.

        :param core_run: Run object to indicate whether is ternimal state.
        :type core_run: azureml.core.Run
        :return: Whether run is in terminal state.
        :rtype: bool
        """
        return core_run.get_status() not in RUNNING_STATES

    def _get_run_status(self):
        run_status_entity = self._get_pipeline_run_status()
        return self._get_status_from_raw_value(run_status_entity.status.run_status)

    def _get_pipeline_run_status(self):
        service_caller = _DesignerServiceCallerFactory.get_instance(self.workspace)
        run_status_entity = service_caller.get_pipeline_run_status(pipeline_run_id=self.id,
                                                                   experiment_name=self._experiment.name,
                                                                   experiment_id=self._experiment.id)
        return run_status_entity

    @property
    def _outputs(self) -> List[_Output]:
        """Get outputs of the current run, only for step run."""
        if not self._run_outputs:
            self._create_outputs()
        return self._run_outputs

    def _get_step_structure_interface(self):
        """
        Get structure interface of the step run's component.

        :return: the structure interface of the step run.
        :rtype: ._restclients.designer.models.StructuredInterfaceOutput
        """
        designerServiceCaller = _DesignerServiceCallerFactory.get_instance(self.workspace)
        dto = designerServiceCaller.get_component_by_id(component_id=self._properties['azureml.moduleid'])
        return dto.module_entity.structured_interface

    def _create_outputs(self):
        """Create outputs associated with the step run."""
        output_ports = self._get_step_structure_interface().outputs
        if output_ports:
            self._run_outputs = []
            for port in output_ports:
                self._run_outputs.append(_Output(name=port.label, _type=port.data_type_id, run=self))

    def _get_output(self, name: str) -> _Output:
        """
        Get an Output object by name.

        :param name: The name of the output.
        :type name: str
        :return: The Output object.
        :rtype: azure.ml.component.Output
        """
        for output in self._outputs:
            if name == output.name or ' '.join(name.split('_')).capitalize() == output.name.capitalize():
                return output
        return None

    @track()
    def _visualize(self):
        """Visualize the pipeline run graph with status if in notebook environment."""
        if not self._can_visualize():
            self._visualize_not_support_warning(only_show_in_notebook=False)
        else:
            self.wait_for_completion()

    def _get_visualizer(self):
        from ._widgets._visualize import _visualize
        graph_json = self._build_visualization_dict()
        is_prod = _is_prod_workspace(self.workspace)
        envinfo = WorkspaceTelemetryMixin._get_telemetry_value_from_workspace(self.workspace)
        envinfo.update(
            {
                'runId': self.id,
                'runName': self._name,
                'experimentId': self._experiment.id,
                'experimentName': self._experiment.name
            })
        # also pass graph no status json dict to visualizer at the same time
        # in the end we will only need to pass this
        service_caller = _DesignerServiceCallerFactory.get_instance(self.workspace)
        graph_no_status = service_caller.get_pipeline_run_graph_no_status(
            pipeline_run_id=self.id,
            include_run_setting_params=False,
            has_namespace_concept=False,
            skip_dataset_load=True,
            referenced_node_id=None,
            cls=PipelineResponse)
        graph_no_status = json.loads(get_pipeline_response_content(graph_no_status))
        visualizer = _visualize(graph_json, is_prod=is_prod, envinfo=envinfo, pipeline_graph=graph_no_status)

        return visualizer

    @track()
    def _get_status(self):
        """
        Fetch the latest status of the run.

        :return: The latest status.
        :rtype: str
        """
        if self._is_pipeline_run:
            return self._get_run_status().value
        return self._core_run.get_status()

    def _build_visualization_dict(self):
        if self._visualization_dict is None:
            if self._is_pipeline_run:
                pipeline_run_id = self.id
                selected_node_id = None
            else:
                pipeline_run_id = self._core_run.parent.id
                selected_node_id = self._get_node_id()

            service_caller = _DesignerServiceCallerFactory.get_instance(self.workspace)
            run_graph = service_caller.get_pipeline_run_graph_no_status(pipeline_run_id=pipeline_run_id)

            visualization_context = VisualizationContext.from_run_graph(run_graph, selected_node_id)

            from ._widgets._visualization_builder import VisualizationBuilder
            visualization_builder = VisualizationBuilder(step_nodes=visualization_context.step_nodes,
                                                         module_defs=visualization_context.module_defs,
                                                         data_nodes=visualization_context.data_nodes,
                                                         sub_pipelines_info=visualization_context.sub_pipelines_info)

            self._visualization_dict = visualization_builder.build_visualization_dict()
        return self._visualization_dict

    @track()
    def _find_child_run(self, name: str) -> List:
        """
        Find a list of child runs in the current run by name.

        :param name: The name of child run to find.
        :type name: str

        :return: List of :class:`azure.ml.component.Run` objects with the provided name.
        :rtype: builtin.list
        """
        children = self._get_children()
        step_runs = []
        for child in children:
            if name == child._run_dto['name']:
                step_run = Run(child._experiment, child._id)
                step_runs.append(step_run)

        return step_runs

    @track()
    def _get_child_run(self, _id: str):
        """
        Get a child run by id.

        :param _id: The id of the child run.
        :type _id: str

        :return: The Run object with the provided id.
        :rtype: azure.ml.component.Run
        """
        children = self._get_children()
        for child in children:
            if _id == child._id:
                step_run = Run(child._experiment, child._id)
                return step_run
        return None

    @track()
    def _download_file(self, name, output_file_path=None, _validate_checksum=False):
        """Download an associated file from storage.

        :param name: The name of the artifact to be downloaded.
        :type name: str
        :param output_file_path: The local path where to store the artifact.
        :type output_file_path: str
        """
        self._core_run.download_file(name=name, output_file_path=output_file_path,
                                     _validate_checksum=_validate_checksum)

    @track(activity_type=_PUBLIC_API, activity_name="Run_profile")
    def _profile(self):
        """Visualize the pipeline run profile info if in notebook environment."""
        can_visualize = self._can_visualize()
        if not can_visualize or not self._is_pipeline_run:
            self._visualize_not_support_warning(only_show_in_notebook=False)
            print('profiling is only supported in proper notebook environment for pipeline run.')
        else:
            # todo: handle step run
            from ._widgets._visualize import _visualize_profiling
            graph_json = self._build_visualization_dict()
            is_prod = _is_prod_workspace(self.workspace)
            run_profile_dict = self._get_profile_data_dict()
            envinfo = WorkspaceTelemetryMixin._get_telemetry_value_from_workspace(self.workspace)
            _visualize_profiling(graphyaml=graph_json, profiling=run_profile_dict, is_prod=is_prod, envinfo=envinfo)
            self._add_visualize_telemetry_value(can_visualize)

    def _get_profile_data_dict(self):
        try:
            service_caller = _DesignerServiceCallerFactory.get_instance(self.workspace)
            run_profile_response = service_caller.get_pipeline_run_profile(self.id)
            return json.loads(get_pipeline_response_content(run_profile_response))
        except:
            return {}

    def _get_all_node_logs(self, steps_logs_dict):
        node_logs = {k: v for k, v in steps_logs_dict.items()}
        node_logs.update({'@parent': self._get_details()['logFiles']})
        return node_logs

    def _get_node_status_dict(self, parent_status, graph_node_status, steps_detail_url_dict={}):
        def _graph_node_status_to_json(node_id, status, meta_dict):
            node_meta = meta_dict.get(node_id)
            return {'status': status.status,
                    'statusCode': status.status_code,
                    'runId': status.run_id,
                    'startTime': None if status.start_time is None else status.start_time.isoformat(),
                    'endTime': None if status.end_time is None else status.end_time.isoformat(),
                    'runStatus': status.run_status,
                    'isReused': True if status.reuse_info is not None else False,
                    'runDetailsUrl': node_meta.get('runDetailsUrl') if node_meta else None,
                    'statusDetail': status.status_detail,
                    'meta': node_meta}

        node_status = {k: _graph_node_status_to_json(k, v, steps_detail_url_dict)
                       for k, v in graph_node_status.items()}
        parent_status_dict = {'runStatus': parent_status.run_status,
                              'runId': self.id,
                              'runDetailsUrl': self.get_portal_url(),
                              'statusDetail': parent_status.status_detail,
                              'subscriptionId': self.workspace.subscription_id,
                              'resourceGroup': self.workspace.resource_group,
                              'workspaceName': self.workspace.name,
                              'experimentName': self._experiment.name,
                              'startTime': parent_status.start_time,
                              'endTime': parent_status.end_time}
        # append parent run status and logs
        node_status.update({'@parent': parent_status_dict})
        return node_status

    def _get_telemetry_values(self, additional_value=None):
        telemetry_values = WorkspaceTelemetryMixin._get_telemetry_value_from_workspace(self.workspace)

        if additional_value is not None:
            telemetry_values.update(additional_value)

        return telemetry_values

    def _add_visualize_telemetry_value(self, can_visualize: bool):
        telemetry_value = self._get_telemetry_values(additional_value={
            'visualize': can_visualize
        })

        # We need to distinguish whether a call to validate will visualize ux or not.
        _LoggerFactory.add_track_dimensions(_get_logger(), telemetry_value)

    def _update_graph_visualization(self, visualizer, update_urls: bool = False, update_logs: bool = False,
                                    raise_on_error: bool = False):
        status, logs, error = self._get_graph_node_status_and_logs(update_urls, update_logs)

        visualizer.send_message(message='status', content=status)
        visualizer.send_message(message='profiling', content=self._get_profile_data_dict())

        if update_logs:
            visualizer.send_message(message='logs', content=logs)

        if error and raise_on_error:
            raise ActivityFailedException(error_details=json.dumps(error, indent=4))

    def _get_graph_node_status_and_logs(self, update_urls: bool = False, update_logs: bool = False):
        """Get graph node status dict and node log urls dict and node error details.

        :param update_urls: whether to update the run detail url in node status dict.
        :type update_urls: bool
        :param update_logs: whether to return the node logs urls dict.
        :type update_logs: bool

        :return: node status dict, node logs urls dict, error details
        :rtype: (dict, dict, str)
        """
        run_graph_status = self._get_pipeline_run_status()
        parent_status = run_graph_status.status
        graph_node_status = run_graph_status.graph_nodes_status

        if not update_urls:
            node_status = self._get_node_status_dict(parent_status, graph_node_status)

        if not update_logs:
            node_logs = {}

        error_detail = None

        def get_step_run_meta_info(details_dict, tags_dict):
            input_datasets = details_dict.get('inputDatasets')
            if input_datasets:
                input_datasets_dict_list = \
                    [{'identifier': i.get('identifier'),
                      'comsumptionType': i.get('comsumptionType'),
                      'inputDetails': i.get('inputDetails')} for i in input_datasets._input_datasets]
            else:
                input_datasets_dict_list = []
            output_datasets = details_dict.get('outputDatasets')
            if output_datasets:
                output_datasets_dict_list = \
                    [{'identifier': o.get('identifier'),
                      'outputType': o.get('outputType'),
                      'outputDetails': o.get('outputDetails')} for o in output_datasets]
            else:
                output_datasets_dict_list = []
            run_def = details_dict.get('runDefinition')
            environment = run_def.get('environment') if run_def else None
            environment_name = environment.get('name') if environment else None
            environment_version = environment.get('version') if environment else None
            command = run_def.get('command') if run_def else None
            return {'input_datasets': input_datasets_dict_list,
                    'output_datasets': output_datasets_dict_list,
                    'environment': environment_name,
                    'environment_version': environment_version,
                    'command': command,
                    'tags': tags_dict}

        if update_urls or update_logs:
            steps_logs_dict = {}
            step_run_meta_info_dict = {}
            children = self._get_children(_rehydrate_runs=False)

            for step_run in children:
                final_details = step_run._get_details()
                error = final_details.get("error")
                if error is not None:
                    error_detail = error
                nodeid = step_run._get_node_id()
                steps_logs_dict[nodeid] = final_details['logFiles']
                step_run_meta_info_dict[nodeid] = get_step_run_meta_info(final_details, step_run._tags)
                step_run_meta_info_dict[nodeid].update({'runDetailsUrl': step_run._run_details_url})

            if update_urls:
                node_status = self._get_node_status_dict(parent_status, graph_node_status, step_run_meta_info_dict)

            if update_logs:
                node_logs = self._get_all_node_logs(steps_logs_dict)

        return node_status, node_logs, error_detail

    @track(activity_type=_PUBLIC_API, activity_name="Run_debug")
    def _debug(self, compute=None):
        """
        Debug step run.

        If compute=None, it will reuse the compute config of the previous run.
        If compute is a remote compute name, it will debug step run in the remote compute.
        The main work flow likes this:
            1. Prepare run_config for debug run.
                - Get run_config of the user specified step run and download the snapshot of specified step run.
                - If the step run command starts with python, .vscode/launch.json is generated in snapshot. And add
                  the command which used to replace input/output variables in launch.json to the run_config command.
                - Add the sleep command in the run config command.
                - Update compute config of run_config. If compute isn't provided, using the compute config of
                  specified step run.
            2. Submit debug run.
                - Generate ScriptRunConfig from run_config and snapshot.
                - Submit the debug run by ScriptRunConfig.
            3. Get information about debug run and remote compute.
                - Get step run or job instance link.
                - Get working_dir/script command from run log.
                - Get SSH connection command from compute or job details.
        If compute=local, it will prepare the debug environment in the local machine.
        The main work flow likes this:
            1. Pull the image of step run.
            2. Download the snapshot and input datasets.
            3. Prepare the debug config file.

        :param compute: Compute name in workspace.
        :type compute: str
        :return: The debug run.
        :rtype: azure.ml.component.Run
        """
        from azure.ml.component._debug._step_run_debugger import OnlineStepRunDebugger
        debugger = OnlineStepRunDebugger(run_id=self.id,
                                         workspace_name=self.workspace.name,
                                         resource_group=self.workspace.resource_group,
                                         subscription_id=self.workspace.subscription_id,
                                         experiment_name=self._experiment.name,
                                         compute=compute)
        debug_core_run = debugger.run()
        return Run(experiment=debug_core_run._experiment, run_id=debug_core_run.id)

    @track(activity_type=_PUBLIC_API, activity_name="Run_cancel")
    def cancel(self):
        """Mark the run as canceled."""
        self._core_run.cancel()

    def __str__(self):
        """Return the description of a Run object."""
        info = self._get_base_info_dict()
        formatted_info = ',\n'.join(["{}: {}".format(k, v) for k, v in info.items()])
        return "{0}({1})".format('PipelineRun' if self._is_pipeline_run else 'StepRun', formatted_info)

    def __repr__(self):
        """Return the string representation of a Run object."""
        return self.__str__()

    def _repr_html_(self):
        if enabled_subpipeline_registration():
            from azureml._html.utilities import to_html, make_link
            info = self._get_base_info_dict()
            info.update([
                ('Details Page', make_link(self.get_portal_url(), "Link to Azure Machine Learning studio")),
                ('Docs Page', make_link(self._core_run.get_docs_url(), "Link to Documentation"))
            ])
            return to_html(info)
        else:
            return self._core_run._repr_html_()

    def _get_detailed_error(self):
        if self._get_status() != RunStatus.FAILED:
            return None
        error = self._get_details().get('error')
        return error or GENERAL_ERROR_MESSAGE

    def _get_node_id(self):
        """Return the node id in the pipeline run graph if it is step run."""
        return self._properties.get('azureml.nodeid', None) or self._tags.get('azureml.nodeid', None)

    @track(activity_type=_PUBLIC_API, activity_name='Run_resubmit')
    def resubmit(self, *, pipeline_parameters=None, experiment_name=None, description=None, tags=None,
                 continue_on_step_failure=True, display_name=None, force_rerun=None) -> str:
        """Resubmit an experiment with a different set of parameters, subgraph pipeline run is not supported yet.

        :param pipeline_parameters: A dictionary of pipeline parameter assignments, support partial update.
        :type pipeline_parameters: dict
        :param experiment_name: The experiment name, will inherit current run's if experiment_name is None.
        :type experiment_name: str
        :param description: The description of the resubmitted pipeline run,
            default value is same as previous run's description.
        :type description: str
        :param tags: Tags to be added to the resubmitted run, looks like {tag: value}.
        :type tags: dict
        :param continue_on_step_failure: Indicates whether to continue pipeline execution if a step fails.
            If True, only steps that have no dependency on the output of the failed step will continue execution.
        :type continue_on_step_failure: bool
        :param display_name: The display name of the resubmitted pipeline run,
            default value is same as previous run's display name.
        :type display_name: str
        :return: The resubmitted run id.
        :rtype: str
        :param force_rerun: True to indicate force rerun all child runs under this root pipeline run, all child runs
            will not latch/reuse to any run and cannot be latched/reused by other runs, False to indicate set
            regenerate_output of all child runs to False and do common reuse logic. Default value is None.
        :type force_rerun: bool
        """
        # check if run type is pipeline run
        if not self._is_pipeline_run:
            raise UserErrorException("current run is not pipeline run, resubmit is not supported.")
        # subgraph pipeline run is not supported yet, check by trying to find current run's parent run
        if self._parent_run:
            raise UserErrorException("subgraph pipeline run resubmission is not supported yet.")
        # validate tags, same as Pipeline.submit
        from .pipeline import Pipeline
        Pipeline._validate_pipeline_tags(tags)

        # deal with None parameters
        experiment_name = experiment_name if experiment_name else self._experiment.name
        description = description if description else self._core_run.description
        try:
            display_name = display_name if display_name else self._core_run.display_name
        except AttributeError:
            display_name = display_name if display_name else self._core_run.name  # azureml.core has no display_name

        dataset_def_value_assignments, data_path_assignments = {}, {}
        if pipeline_parameters:
            pipeline_parameters, dataset_def_value_assignments, data_path_assignments = \
                resolve_pipeline_parameters(pipeline_parameters, flatten=True,
                                            resolve_dataset=True, workspace=self.workspace,
                                            resolve_data_path=True)
        if len(dataset_def_value_assignments) == 0:
            dataset_def_value_assignments = None

        request = ResubmitPipelineRunRequest(
            pipeline_parameters=pipeline_parameters, experiment_name=experiment_name, description=description,
            display_name=display_name, tags=tags, continue_run_on_step_failure=continue_on_step_failure,
            data_path_assignments=data_path_assignments,
            data_set_definition_value_assignments=dataset_def_value_assignments,
            enforce_rerun=force_rerun
        )
        service_caller = _DesignerServiceCallerFactory.get_instance(self.workspace)
        resubmit_run_id = service_caller.resubmit_pipeline_run(request=request, pipeline_run_id=self.id)
        print('Resubmitted PipelineRun', resubmit_run_id)
        return resubmit_run_id
