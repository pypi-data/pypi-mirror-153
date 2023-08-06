# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import os
from collections import OrderedDict
from datetime import datetime
import concurrent.futures

from .._restclients.designer.models import GraphNodeStatusInfo
from .._restclients.designer.models._designer_service_client_enums import RunStatus, TaskStatusCode
from .._util._utils import _get_short_path_name, trans_to_valid_file_name, _get_parameter_static_value
from ..component import Output, Input
from .._core._component_definition import ComponentType
from .._util._loggerfactory import track
from ._component_run_helper import ComponentRunHelper, update_pipeline_in_visualizer, RunMode
from ._component_snapshot import snapshot_cache
from ._constants import NODE_ID, RUN_ID, PARENT_NODE_ID, EXECUTION_LOGFILE


datetime_format = '%Y-%m-%d %H:%M:%S'
submit_log_format = '[{}] Submitting {} runs, first five are: {} \n'
complete_log_format = '[{}] Completing processing {}\n'
failed_log_format = '[{}] Execution of experiment failed, update experiment status and cancel running nodes.'


class PipelineRunOrchestrator:

    def __init__(self, workspace, input_dataset, pipeline_node_dict, component_execution_dict,
                 pipeline_parameters=None, max_workers=None, component_executor=None,
                 visualization_context=None, pipeline_definition=None):
        """
        Init pipeline run orchestrator.
        :param workspace: The workspace of pipeline.
        :type workspace: azureml.core.Workspace
        :param input_dataset: Input datasets of pipeline
        :type input_dataset: List
        :param pipeline_node_dict: Dict of node id and component, key is node id, value is component.
        :param pipeline_node_dict: OrderedDict[str, Component]
        :param component_execution_dict: Dict of component id and component execution, key is component id,
                                         value is component execution info.
        :type component_execution_dict: dict[component, ComponentExecutionInfo]
        :param pipeline_parameters: An optional dictionary of pipeline parameter
        :type pipeline_parameters: dict({str:str})
        :param max_workers: The maximum number of threads that can be used to execute component nodes.
                            If max_workers is None, it will default to the number of processors on the machine.
        :type max_workers: int
        :param component_executor: The thread pool executor is used to execute component run.
        :type component_executor: ThreadPoolExecutor
        """
        self.workspace = workspace
        self.input_dataset = input_dataset
        self.pipeline_parameters = pipeline_parameters
        self.visualization_context = visualization_context
        if component_executor:
            self.component_executor = component_executor
            self._cur_pipeline_control_executor = False
        else:
            self.component_executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
            self._cur_pipeline_control_executor = True
        # This thread pool executor is used to execute sub pipeline and pipeline component.
        self.pipeline_executor = concurrent.futures.ThreadPoolExecutor()
        self.pipeline_node_dict = pipeline_node_dict
        self.component_execution_dict = component_execution_dict
        self.pipeline_definition = pipeline_definition
        self.root_nodes, self.edge_info = self._get_pipeline_root_nodes()

    @track(is_long_running=True)
    def start_orchestrate(self, working_dir, tracker, *, visualizer=None, show_output=False,
                          continue_on_step_failure=None, mode=RunMode.Docker, raise_on_error=True, workspace=None):
        """
        Orchestrate pipeline run

        Orchestrating pipeline run to make steps executing in parallel. Firstly will submit no dependency
        steps to start pipeline run, using threadpool to parallel execute steps. When previous steps completed,
        will push no dependency steps to threadpool, until all steps completed.

        :param working_dir: pipeline run data and snapshot store path
        :type working_dir: str
        :param tracker: Used for tracking run history.
        :type tracker: RunHistoryTracker
        :param visualizer: To show pipeline graph in notebook
        :type visualizer: azure.ml.component._widgets._visualize
        :param show_output: Indicates whether to show the pipeline run status on sys.stdout.
        :type show_output: bool
        :param continue_on_step_failure: Indicates whether to continue pipeline execution if a step fails.
                                         If True, only steps that have no dependency on the output of the
                                         failed step will continue execution.
        :type continue_on_step_failure: bool
        :param mode: Three modes are supported to run component.
                     docker: Start a container with the component's image and run component in it.
                     conda: Build a conda environment in the host with the component's conda definition and
                            run component in it.
                     host: Directly run component in host environment.
                     For more information about run mode, see https://aka.ms/component-run#overview
        :type mode: azure.ml.component._execution._component_run_helper.RunMode
        :param raise_on_error: Indicates whether to raise an error when the Run is in a failed state
        :type raise_on_error: bool
        :param workspace: The workspace is used to register environment when component is workspace independent.
        :type workspace: azureml.core.Workspace

        :return: Pipeline run status.
        :rtype: ~designer.models.RunStatus
        """
        # Update pipeline status in visualizer
        self.component_execution_dict[PARENT_NODE_ID].run = tracker.get_run()
        self._update_pipeline_visualizer(node_id=PARENT_NODE_ID, visualizer=visualizer,
                                         run_status=RunStatus.PREPARING, task_status=TaskStatusCode.RUNNING)
        pipeline_run_info = self.PipelineRunInfo(working_dir=working_dir, show_output=show_output,
                                                 continue_on_step_failure=continue_on_step_failure, mode=mode,
                                                 visualizer=visualizer, raise_on_error=raise_on_error,
                                                 tracker=tracker, workspace=workspace)
        executed_nodes, cur_pipeline_run_success = set(), True
        execution_log_path = os.path.join(working_dir, EXECUTION_LOGFILE)
        try:
            # Download component node input dataset
            pipeline_execution_workspace = self.workspace or workspace
            ComponentRunHelper.download_datasets(workspace=pipeline_execution_workspace,
                                                 datasource=self.input_dataset,
                                                 working_dir=working_dir,
                                                 pipeline_parameters=self.pipeline_parameters)

            if mode.is_build_env_mode():
                # Build component node execution environment
                for node in self.root_nodes.values():
                    if node.type != ComponentType.PipelineComponent.value:
                        ComponentRunHelper.prepare_component_env(node, working_dir,
                                                                 mode == RunMode.Docker, pipeline_execution_workspace)

            with open(execution_log_path, 'w') as execution_file:
                self._update_pipeline_visualizer(node_id=PARENT_NODE_ID, visualizer=visualizer,
                                                 run_status=RunStatus.RUNNING, log_url=execution_log_path)
                # Start execution of the root node. The key is component run future and value is component run info.
                execution_future_dict = self._execute_nodes(self.root_nodes, pipeline_run_info, execution_file)
                running_execution_futures = execution_future_dict.keys()
                while running_execution_futures or len(executed_nodes) < len(self.pipeline_node_dict):
                    # Wait for one of the component run task in the executor to be completed.
                    done_execution_futures, running_execution_futures = concurrent.futures.wait(
                        running_execution_futures, return_when=concurrent.futures.FIRST_COMPLETED)
                    executed_nodes.update([execution_future_dict[future][NODE_ID] for future in done_execution_futures
                                           if future in execution_future_dict])
                    # Process the executed tasks and get the possible execution nodes.
                    possible_execution_nodes_id, pipeline_run_success = self._handle_done_execution_nodes(
                        done_execution_futures, execution_future_dict, execution_file, pipeline_run_info)
                    cur_pipeline_run_success = cur_pipeline_run_success and pipeline_run_success

                    if not cur_pipeline_run_success and not pipeline_run_info.continue_on_step_failure:
                        # When component in pipeline run failed and continue_on_step_failure is false, wait for all
                        # tasks in executor to complete.
                        concurrent.futures.wait(running_execution_futures,
                                                return_when=concurrent.futures.ALL_COMPLETED)
                        break

                    # Submit the component run task which has prepared input datasets.
                    next_execution_nodes = self._find_next_execute_node(possible_execution_nodes_id, executed_nodes)
                    next_execution_future_dict = self._execute_nodes(next_execution_nodes, pipeline_run_info,
                                                                     execution_file)
                    # Update the running future list.
                    running_execution_futures.update(next_execution_future_dict.keys())
                    execution_future_dict.update(next_execution_future_dict)
        except Exception as e:
            cur_pipeline_run_success = False
            if raise_on_error:
                raise e
        finally:
            # Update pipeline run status
            self.component_executor.submit(tracker.update_run_result_status, cur_pipeline_run_success)
            # Upload pipeline log and get log url
            update_log_future = self.component_executor.submit(tracker.upload_run_log, EXECUTION_LOGFILE,
                                                               execution_log_path)
            # Update pipeline run status in visualizer.
            run_status = RunStatus.COMPLETED if cur_pipeline_run_success else RunStatus.FAILED
            task_status = TaskStatusCode.FINISHED if cur_pipeline_run_success else TaskStatusCode.FAILED
            self._update_pipeline_visualizer(node_id=PARENT_NODE_ID, visualizer=visualizer,
                                             run_status=run_status, task_status=task_status,
                                             log_url=update_log_future.result())
            # Remove long time no used snapshots in cache
            snapshot_cache.clean_up_snapshot_cache()
            if self._cur_pipeline_control_executor:
                # Executor.shutdown will wait for threads in it completed.
                self.component_executor.shutdown()
        return run_status

    class PipelineRunInfo:
        """Used to store the information about pipeline run."""
        def __init__(self, working_dir, tracker, show_output=False, continue_on_step_failure=None,
                     mode=RunMode.Docker, raise_on_error=True, visualizer=None, workspace=None):
            self.working_dir = working_dir
            self.tracker = tracker
            self.show_output = show_output
            self.continue_on_step_failure = continue_on_step_failure
            self.mode = mode
            self.raise_on_error = raise_on_error
            self.visualizer = visualizer
            self.workspace = workspace

    @classmethod
    def generate_orchestrator_by_pipeline_component(cls, pipeline_component, input_dataset, pipeline_parameters=None,
                                                    max_workers=None, component_executor=None):
        """
        Generate pipeline run orchestrator by pipeline component. It will get the graph by send request to backend.
        Then it will create the component of pipeline component and update params and inputs of components, and
        generates the information required by PipelineRunOrchestrator.

        :param pipeline_component: Pipeline component to generate orchestrator
        :type pipeline_component: azure.ml.component.Component
        :param input_dataset: Input datasets of pipeline component
        :type input_dataset: List
        :param pipeline_parameters: An optional dictionary of pipeline parameter
        :type pipeline_parameters: dict({str:str})
        :param max_workers: The maximum number of threads that can be used to execute pipeline steps.
                            If max_workers is None, it will default to the number of processors on the machine.
        :type max_workers: int
        :param component_executor: The thread pool executor is used to execute component run.
        :type component_executor: ThreadPoolExecutor
        :return: Pipeline run orchestrator
        :rtype: PipelineRunOrchestrator
        """
        pipeline_component._definition.generate_register_pipeline()
        pipeline_node_dict = pipeline_component._definition._register_nodes
        component_execution_dict = {
            id: ComponentExecutionInfo(node_id=id,
                                       node_name=pipeline_component._definition._node_id_variable_name_dict[id])
            for id, node in pipeline_node_dict.items()}
        component_execution_dict[PARENT_NODE_ID] = ComponentExecutionInfo(
            node_id=pipeline_component._id, node_name=pipeline_component._get_component_name())
        return PipelineRunOrchestrator(workspace=pipeline_component.workspace, input_dataset=input_dataset,
                                       pipeline_node_dict=pipeline_node_dict,
                                       component_execution_dict=component_execution_dict,
                                       pipeline_parameters=pipeline_parameters,
                                       pipeline_definition=pipeline_component._definition,
                                       max_workers=max_workers, component_executor=component_executor)

    @classmethod
    def generate_orchestrator_by_pipeline(cls, pipeline, input_dataset, visualization_context=None,
                                          pipeline_parameters=None, max_workers=None, component_executor=None,
                                          component_execution_dict=None, pipeline_node_id=None):
        """
        Generate pipeline run orchestrator by pipeline.

        :param pipeline: Pipeline to generate orchestrator
        :type pipeline: azure.ml.component.Pipeline
        :param input_dataset: Input datasets of pipeline
        :type input_dataset: List
        :param visualization_context:
        :type visualization_context:
        :param pipeline_parameters: An optional dictionary of pipeline parameter
        :type pipeline_parameters: dict({str:str})
        :param max_workers: The maximum number of threads that can be used to execute pipeline steps.
                            If max_workers is None, it will default to the number of processors on the machine.
        :type max_workers: int
        :param component_executor: The thread pool executor is used to execute component run.
        :type component_executor: ThreadPoolExecutor
        :param component_execution_dict: Component execution info of parent pipeline.
        :type component_execution_dict: dict({str: ComponentExecutionInfo})
        :param pipeline_node_id: Pipeline node id.
        :type pipeline_node_id: str
        :return: Pipeline run orchestrator
        :rtype: PipelineRunOrchestrator
        """
        from azure.ml.component import Pipeline

        # Mapping of component id and node id.
        component_to_node_dict = visualization_context.module_node_to_graph_node_mapping
        # Dict of component id and component instance.
        pipeline_node_dict = OrderedDict({node._id: node for node in pipeline.nodes})
        # Mapping of component id and component execution information.
        if not component_execution_dict:
            component_execution_dict = {
                node._id: ComponentExecutionInfo(node_id=component_to_node_dict[node._id],
                                                 node_name=node._get_component_name())
                for node in pipeline._expand_pipeline_nodes()}
            # Add parent pipeline to node_mapping
            component_execution_dict[PARENT_NODE_ID] = ComponentExecutionInfo(node_id=PARENT_NODE_ID)

        # Add sub pipeline to component_execution_dict.
        component_execution_dict.update(**{
            node._id: ComponentExecutionInfo(node_id=node._id, node_name=node._get_component_name())
            for node in pipeline_node_dict.values() if isinstance(node, Pipeline)})

        pipeline_parameters = pipeline_parameters or {}
        return PipelineRunOrchestrator(workspace=pipeline.workspace, input_dataset=input_dataset,
                                       pipeline_parameters=pipeline_parameters,
                                       max_workers=max_workers, component_executor=component_executor,
                                       component_execution_dict=component_execution_dict,
                                       pipeline_node_dict=pipeline_node_dict,
                                       pipeline_definition=pipeline._definition,
                                       visualization_context=visualization_context)

    def _get_pipeline_root_nodes(self):
        """
        Get pipeline root nodes and edge info.

        :return: root_nodes: The dict of root node of pipeline, key is node id, value is node instance.
                 edge_info: The dict of source node id and destination nodes id, key is source node id, value is the
                            list of destination nodes id.
        :rtype: dict[str, str], dict[str, List[str]]
        """
        edge_info, root_nodes = {}, {}
        for node_id, node in self.pipeline_node_dict.items():
            is_root_node = True
            for dset in node._input_ports.values():
                if isinstance(dset, Input):
                    dset = dset._get_internal_data_source()
                if isinstance(dset, Output):
                    if dset._owner._id in self.component_execution_dict:
                        if self.component_execution_dict[dset._owner._id].execution_status == \
                                RunStatus.COMPLETED:
                            continue
                    is_root_node = False
                    # Get node edge by input dataset.
                    if dset._owner._id not in edge_info.keys():
                        edge_info[dset._owner._id] = []
                    edge_info[dset._owner._id].append(node_id)
            if is_root_node:
                # If input datasets of node isn't the output of other nodes, it will be considered as root node.
                root_nodes[node_id] = node

        return root_nodes, edge_info

    def _find_next_execute_node(self, possible_execution_nodes_id, executed_nodes_id):
        """
        Find the executable node that the required input datasets are prepared.
        It will check whether the in-degree nodes are executed.

        :param possible_execution_nodes_id: Nodes that may have prepared input datasets.
        :type possible_execution_nodes_id: List[str]
        :param executed_nodes_id: List of the node id of executed node.
        :type executed_nodes_id: List[str]
        :return: Dict of next execution nodes, the key is node id, value in node instance.
        :rtype: Dict[str, azure.ml.component.Component]
        """
        next_execution_nodes = {}
        for node_id in (possible_execution_nodes_id & self.pipeline_node_dict.keys() - executed_nodes_id):
            node = self.pipeline_node_dict[node_id]
            node_inputs = [input_dataset._get_internal_data_source() if isinstance(input_dataset, Input)
                           else input_dataset for input_dataset in node._input_ports.values()]
            # Check whether the in-degree nodes are executed.
            if all([self.component_execution_dict[input._owner._id].execution_status == RunStatus.COMPLETED
                    for input in node_inputs if isinstance(input, Output)]):
                next_execution_nodes[node_id] = node
        return next_execution_nodes

    def _generate_sub_pipeline_parameter(self, pipeline):
        """
        Generate pipeline parameter in the sub pipeline.

        :param pipeline: Sub pipeline
        :type pipeline: Union[Pipeline, PipelineComponent]
        :return: Dict of pipeline parameter in the sub pipeline.
        :rtype: Dict[str, object]
        """
        from azure.ml.component._pipeline_parameters import PipelineParameter

        # Generate pipeline parameters in the sub pipeline.
        pipeline_parameters = {}
        for k, v in pipeline.inputs.items():
            if isinstance(v, PipelineParameter):
                # The key is the name of pipeline parameter.
                pipeline_parameters[v.name] = _get_parameter_static_value(v, self.pipeline_parameters)
            elif isinstance(v, Input):
                # The key is the input name of sub pipeline.
                dset = v._dset
                if isinstance(dset, Output):
                    # Convert the component output to the local path.
                    pipeline_parameters[k] = self.component_execution_dict[dset._owner._id].outputs[dset._name]
                elif isinstance(dset, PipelineParameter):
                    pipeline_parameters[k] = _get_parameter_static_value(dset, self.pipeline_parameters)
                else:
                    pipeline_parameters[k] = dset
        return pipeline_parameters

    def _execute_nodes(self, execution_nodes, pipeline_run_info, execution_file):
        """
        Submit the execution task to executor. And prepare environment of out-of-degree nodes of the execution node.

        :param execution_nodes: The execution nodes.
        :type execution_nodes: dict[str, azure.ml.component.Component]
        :param pipeline_run_info: Information about pipeline run.
        :type pipeline_run_info: PipelineRunOrchestrator
        :param execution_file: Log pipeline run.
        :type execution_file: io.IOBase
        :return: The dict of execution futures, key is the execution future, value is component instance run info.
        :rtype: dict[Future, dict[str, str]]
        """
        from azure.ml.component import Pipeline

        execution_future_dict, next_node_id_list, component_run_ids = {}, set(), []
        for node_id, node in execution_nodes.items():
            # Generate child run for component instance run.
            child_tracker = pipeline_run_info.tracker.get_child_tracker(name=node.name, path=EXECUTION_LOGFILE)
            run_id = child_tracker.get_run_id()
            self.component_execution_dict[node_id].run = child_tracker.get_run()
            # Create working directory for component instance run.
            component_folder = trans_to_valid_file_name(self.component_execution_dict[node_id].node_name)
            node_working_dir = _get_short_path_name(path=os.path.join(pipeline_run_info.working_dir, component_folder),
                                                    is_dir=True, create_dir=True)
            # Submit component instance run task.
            if node.type != ComponentType.PipelineComponent.value:
                run_future = self.component_executor.submit(self._execute_component_node, node, node_working_dir,
                                                            child_tracker, pipeline_run_info)
            else:
                sub_pipeline_parameters = self._generate_sub_pipeline_parameter(node)
                if isinstance(node, Pipeline):
                    # Execute sub pipeline in pipeline_executor.
                    run_future = self.pipeline_executor.submit(
                        self._execute_sub_pipeline, node, node_working_dir,
                        child_tracker, pipeline_run_info, sub_pipeline_parameters)
                else:
                    # Execute pipeline component in pipeline_executor.
                    run_future = self.pipeline_executor.submit(
                        self._execute_pipeline_component_node, node,
                        node_working_dir, child_tracker, pipeline_run_info, sub_pipeline_parameters)
            execution_future_dict[run_future] = {NODE_ID: node_id, RUN_ID: run_id}

            # Get out-of-degree nodes of execution node.
            if node_id in self.edge_info:
                next_node_id_list.update(self.edge_info[node_id])
        if len(component_run_ids) > 0:
            # Update pipeline execution log.
            execution_file.write(submit_log_format.format(datetime.now().strftime(datetime_format),
                                                          len(component_run_ids), ','.join(component_run_ids[0:5])))
        if pipeline_run_info.mode.is_build_env_mode():
            # Prepare building next nodes environment.
            for node in [self.pipeline_node_dict[node_id] for node_id in next_node_id_list]:
                if node.type != ComponentType.PipelineComponent.value:
                    ComponentRunHelper.prepare_component_env(node, pipeline_run_info.working_dir,
                                                             pipeline_run_info.mode == RunMode.Docker,
                                                             pipeline_run_info.workspace)
        return execution_future_dict

    def _execute_component_node(self, node, working_dir, tracker, pipeline_run_info):
        """
        Execute component node

        :param node: Component instance.
        :type node: azure.ml.component.Component
        :param working_dir: Working directory of component run.
        :type working_dir: str
        :param tracker: Used to track component run.
        :type tracker: azure.ml.component._execution._tracker.RunHistoryTracker
        :param pipeline_run_info: Information about pipeline run.
        :type pipeline_run_info: PipelineRunOrchestrator
        :return: status: Component run status.
                 ex: The raised exception during component run.
        :rtype: str, Exception
        """
        try:
            component_run_helper = ComponentRunHelper(
                component=node,
                working_dir=working_dir,
                tracker=tracker,
                mode=pipeline_run_info.mode,
                node_id=self.component_execution_dict[node._id].node_id,
                visualizer=pipeline_run_info.visualizer,
                show_output=pipeline_run_info.show_output,
                component_execution_dict=self.component_execution_dict,
                pipeline_parameters=self.pipeline_parameters)
            # Execute component local run.
            component_execution_workspace = node.workspace or pipeline_run_info.workspace
            status = component_run_helper.component_run(raise_on_error=True, workspace=component_execution_workspace)
            self.component_execution_dict[node._id].working_dir = working_dir
        except Exception as ex:
            return RunStatus.FAILED, ex
        return status, None

    def _execute_pipeline_component_node(self, node, working_dir, tracker, pipeline_run_info, pipeline_parameters):
        """
        Execute pipeline component node. It will generate a pipeline_component_orchestrator by pipeline node.
        After pipeline component local run is completed, it will get output of pipeline run from pipeline graph and
        the pipeline component execution info will be updated.

        :param node: Pipeline instance.
        :type node: azure.ml.component.Pipeline
        :param working_dir: Working directory of pipeline run.
        :type working_dir: str
        :param tracker: Used to track pipeline run.
        :type tracker: azure.ml.component._execution._tracker.RunHistoryTracker
        :param pipeline_run_info: Information about pipeline run.
        :type pipeline_run_info: PipelineRunOrchestrator
        :param pipeline_parameters: Pipeline parameters on node.
        :type pipeline_parameters: dict
        :return: status: Pipeline node run status.
                 ex: The raised exception during pipeline run.
        :rtype: ~designer.models.RunStatus, Exception
        """
        try:
            exception, log_url = None, None
            self._update_pipeline_visualizer(node._id, pipeline_run_info.visualizer,
                                             run_status=RunStatus.PREPARING, task_status=TaskStatusCode.RUNNING)
            input_dataset = \
                [item._dset for item in node._input_ports.values()] + \
                list(node._definition.get_dataset_in_registered_pipeline().values())

            input_dataset = [_get_parameter_static_value(item, self.pipeline_parameters) for item in input_dataset]
            pipeline_component_orchestrator = PipelineRunOrchestrator.generate_orchestrator_by_pipeline_component(
                pipeline_component=node,
                input_dataset=input_dataset,
                pipeline_parameters=pipeline_parameters,
                component_executor=self.component_executor)
            # Execute pipeline component local run.
            self._update_pipeline_visualizer(node._id, pipeline_run_info.visualizer, run_status=RunStatus.RUNNING)
            pipeline_run_status = pipeline_component_orchestrator.start_orchestrate(
                working_dir=working_dir, tracker=tracker, visualizer=pipeline_run_info.visualizer,
                show_output=pipeline_run_info.show_output,
                continue_on_step_failure=pipeline_run_info.continue_on_step_failure,
                mode=pipeline_run_info.mode, raise_on_error=pipeline_run_info.raise_on_error)
            log_url = pipeline_component_orchestrator.component_execution_dict[PARENT_NODE_ID]._log_url

            self.component_execution_dict[node._id].working_dir = working_dir
            # The destination node with out node id is pipeline output port.
            graph_info = node._definition.get_registered_pipeline_graph()
            graph_output_edges = [item for item in graph_info.edges if item.source_output_port.node_id and
                                  not item.destination_input_port.node_id]
            # Update pipeline component outputs
            for output in graph_output_edges:
                graph_output_name = output.destination_input_port.graph_port_name
                source_node = output.source_output_port
                pipeline_component_node_mapping = pipeline_component_orchestrator.component_execution_dict
                self.component_execution_dict[node._id].outputs[graph_output_name] = \
                    pipeline_component_node_mapping[source_node.node_id].outputs[source_node.port_name]
        except Exception as e:
            pipeline_run_status = RunStatus.FAILED
            exception = e

        self._update_pipeline_visualizer(
            node_id=node._id, visualizer=pipeline_run_info.visualizer, run_status=pipeline_run_status,
            task_status=TaskStatusCode.FINISHED, log_url=log_url)
        return pipeline_run_status, exception

    def _execute_sub_pipeline(self, sub_pipeline, working_dir, child_tracker, pipeline_run_info, pipeline_parameters):
        """
        Execute sub pipeline in the pipeline. The execution node type is azure.ml.component.Pipeline.
        After execution of sub pipeline is completed, update the output of pipeline's component execution
        info by pipeline outputs.

        :param sub_pipeline: Sub pipeline
        :type sub_pipeline: azure.ml.component.Pipeline
        :param working_dir: Working directory of pipeline run.
        :type working_dir: str
        :param child_tracker: Used to track pipeline run.
        :type child_tracker: azure.ml.component._execution._tracker.RunHistoryTracker
        :param pipeline_run_info: Information about pipeline run.
        :type pipeline_run_info: PipelineRunOrchestrator
        :param pipeline_parameters: PipelineParameters on node
        :type pipeline_parameters: dict
        :return: status: Pipeline node run status.
                 ex: The raised exception during pipeline run.
        :rtype: ~designer.models.RunStatus, Exception
        """
        log_url = None
        try:
            orchestrator = PipelineRunOrchestrator.generate_orchestrator_by_pipeline(
                sub_pipeline, [], self.visualization_context,
                pipeline_parameters, component_executor=self.component_executor,
                component_execution_dict=self.component_execution_dict,
                pipeline_node_id=self.component_execution_dict[sub_pipeline._id].node_id)
            run_result = orchestrator.start_orchestrate(
                working_dir=working_dir, tracker=child_tracker, visualizer=pipeline_run_info.visualizer,
                show_output=pipeline_run_info.show_output,
                continue_on_step_failure=pipeline_run_info.continue_on_step_failure,
                mode=pipeline_run_info.mode, raise_on_error=pipeline_run_info.raise_on_error,
                workspace=pipeline_run_info.workspace)

            log_url = orchestrator.component_execution_dict[PARENT_NODE_ID]._log_url
            # Update pipeline component outputs
            self.component_execution_dict[sub_pipeline._id].working_dir = working_dir
            for output_name, output in sub_pipeline.outputs.items():
                while output._owner._is_pipeline:
                    output = output._owner._outputs_mapping[output.port_name]
                self.component_execution_dict[sub_pipeline._id].outputs[output_name] = \
                    orchestrator.component_execution_dict[output._owner._id].outputs[output.port_name]
            exception = None
        except Exception as e:
            run_result = RunStatus.FAILED
            exception = e

        self._update_pipeline_visualizer(
            node_id=sub_pipeline._id, visualizer=pipeline_run_info.visualizer, run_status=run_result,
            task_status=TaskStatusCode.FINISHED, log_url=log_url)
        return run_result, exception

    def _handle_done_execution_nodes(self, done_execution_futures, execution_future_dict,
                                     execution_file, pipeline_run_info):
        """
        Process the executed node. Check the status of executed nodes.
        And find the out-of-degree nodes of executed node.

        :param done_execution_futures: Future of executed component node.
        :type: done_execution_futures: List[Future]
        :param execution_future_dict:
        :type execution_future_dict: Dict[Future, dict[str, str]]
        :param execution_file: Log pipeline run.
        :type execution_file: io.IOBase
        :param pipeline_run_info: Information about pipeline run.
        :type pipeline_run_info: PipelineRunOrchestrator
        :return: possible_execution_nodes_id: The out-of-degree nodes of executed node which may have prepared inputs.
                 pipeline_run_success: Whether the execution is successful
        :rtype: List[str], bool
        """
        from azure.ml.component import Pipeline
        possible_execution_nodes_id, pipeline_run_success, exceptions = set(), True, []
        for future in done_execution_futures:
            node_id, run_id = execution_future_dict[future][NODE_ID], execution_future_dict[future][RUN_ID]

            # Check component run status.
            if future.result()[0] != RunStatus.COMPLETED:
                pipeline_run_success = False
                execution_file.write(failed_log_format.format(datetime.now().strftime(datetime_format)))
                exceptions.append(future.result()[1])
                continue
            # Update pipeline run log.
            execution_file.write(
                complete_log_format.format(datetime.now().strftime(datetime_format),
                                           'run id {}'.format(run_id) if run_id else 'node id {}'.format(node_id)))
            if node_id in self.edge_info:
                # Get out-of-degree nodes of executed component node.
                possible_execution_nodes_id.update(self.edge_info[node_id])
            elif isinstance(self.pipeline_node_dict[node_id], Pipeline):
                # Get out-of-degree nodes of sub pipeline.
                sub_pipeline = self.pipeline_node_dict[node_id]
                for node in sub_pipeline._expand_pipeline_nodes():
                    possible_execution_nodes_id.update(self.edge_info.get(node._id, []))

        if not pipeline_run_success:
            if pipeline_run_info.raise_on_error:
                # TODO print exception
                raise exceptions[0]
        return possible_execution_nodes_id, pipeline_run_success

    def _update_pipeline_visualizer(self, node_id, visualizer, run_status=None, task_status=None, log_url=None):
        self.component_execution_dict[node_id].update_node_status(run_status=run_status, task_status=task_status,
                                                                  log_url=log_url)
        update_pipeline_in_visualizer(visualizer, self.component_execution_dict)


class ComponentExecutionInfo:
    """Record component execution info."""
    def __init__(self, working_dir=None, node_id=None, outputs=None, execution_status=None,
                 node_name=None, run=None):
        self.node_name = node_name
        self.working_dir = working_dir
        self.node_id = node_id
        self.outputs = outputs or {}
        self.execution_status = execution_status
        self.node_status_info = GraphNodeStatusInfo()
        self.run = run
        self._log_url = None
        self.update_node_status(run_status=RunStatus.NOT_STARTED, task_status=TaskStatusCode.NOT_STARTED)

    def update_node_status(self, run_status=None, task_status=None, log_url=None):
        if run_status == RunStatus.STARTING:
            self.node_status_info.start_time = datetime.now()
        if run_status in [RunStatus.COMPLETED, RunStatus.FAILED]:
            self.node_status_info.end_time = datetime.now()

        self.node_status_info.run_status = run_status or self.node_status_info.run_status
        self.execution_status = self.node_status_info.run_status
        self.node_status_info.status = task_status or self.node_status_info.status
        self.node_status_info.status_code = task_status or self.node_status_info.status_code
        self._log_url = log_url

    def node_status_to_json(self):
        status = self.node_status_info
        if self.node_id != PARENT_NODE_ID:
            return {'status': status.status,
                    'statusCode': status.status_code,
                    'runId': self.run._run_id if self.run else None,
                    'startTime': None if status.start_time is None else status.start_time.isoformat(),
                    'endTime': None if status.end_time is None else status.end_time.isoformat(),
                    'runStatus': status.run_status,
                    'isReused': True if status.reuse_info is not None else False,
                    'runDetailsUrl': self.run._run_details_url if self.run else None,
                    'statusDetail': status.status_detail,
                    # 'meta': node_meta  # TODO add node meta
                    }
        else:
            return {'runStatus': status.run_status,
                    'runId': self.run._run_id if self.run else None,
                    'runDetailsUrl': self.run._run_details_url if self.run else None,
                    'statusDetail': status.status_detail,
                    'subscriptionId': self.run._experiment.workspace.subscription_id if self.run else None,
                    'resourceGroup': self.run._experiment.workspace.resource_group if self.run else None,
                    'workspaceName': self.run._experiment.workspace.name if self.run else None,
                    'experimentName': self.run._experiment.name if self.run else None,
                    'startTime': status.start_time,
                    'endTime': status.end_time}
