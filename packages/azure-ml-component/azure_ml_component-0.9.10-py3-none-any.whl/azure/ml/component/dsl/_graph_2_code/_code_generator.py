# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from pathlib import Path
import logging

from azureml.core.authentication import AzureCliAuthentication

from azure.ml.component._api._utils import _looks_like_a_url
from azure.ml.component._restclients.service_caller import DesignerServiceCaller
from azureml._base_sdk_common.merkle_tree import create_merkletree
from azureml._base_sdk_common.merkle_tree_differ import compute_diff
from azureml.core import Run, Experiment, Workspace
from azureml._common.async_utils import TaskQueue
from azure.ml.component._graph_to_code import _parse_designer_url
from azure.ml.component.dsl._graph_2_code._base_generator import CodeBaseGenerator
from azure.ml.component.dsl._graph_2_code._file_header_generator import CodeFileHeaderGenerator
from azure.ml.component.dsl._graph_2_code._pipeline_generator import PipelineCodeGenerator
from azure.ml.component.dsl._graph_2_code._utils import RUN_TEMPLATE, GraphPackageUtil, \
    _is_anonymous_pipeline_component, NOTE_BOOK_TEMPLATE, _normalize_dict_param_val, _get_pipeline_identifier
from azure.ml.component._util._loggerfactory import _LoggerFactory, _PUBLIC_API, track
from azure.ml.component._restclients.service_caller_factory import _DesignerServiceCallerFactory
from azure.ml.component._restclients.designer.models import PipelineGraph
from azure.ml.component.dsl._component_generator import GraphComponentSnapshotGenerator
from azure.ml.component._util._utils import (
    _sanitize_python_variable_name, TimerContext, environment_variable_overwrite, get_new_dir_name_if_exists,
    _sanitize_folder_name
)
from azure.ml.component._api._snapshots_client import AML_COMPONENT_SNAPSHOT_WITHOUT_DOWNLOAD_PROGRESS_BAR
from azureml.exceptions import UserErrorException

_logger = _LoggerFactory.get_logger("az-ml")
PIPELINE_IDENTIFIER_TRIM_LEN = 20


class RunScript(CodeBaseGenerator):
    DEFAULT_EXPERIMENT_NAME = "sample-experiment-name"
    TARGET_FILE = "run.py"

    def __init__(self, root_pipeline_generator: PipelineCodeGenerator, header=None, run=None,
                 description=None, tags=None, display_name=None, continue_on_step_failure=None,
                 default_compute_target=None):
        super(RunScript, self).__init__(target_file=self.TARGET_FILE, logger=_logger)
        self.pipeline_module_name = root_pipeline_generator.module_name
        self._header = header if header else CodeFileHeaderGenerator(logger=_logger).to_component_entry_code()
        self._experiment_name = self.DEFAULT_EXPERIMENT_NAME if not run else run.experiment.name
        self._description = description
        self._tags = tags
        self._display_name = display_name
        self._continue_on_step_failure = continue_on_step_failure
        self._default_compute_target = default_compute_target

    @property
    def header(self):
        return self._header

    @property
    def pipeline_submit_params(self):
        submit_params = {
            "experiment_name": self._experiment_name,
            "description": self._description,
            "display_name": self._display_name,
            "default_compute_target": self._default_compute_target,
        }
        submit_params = {key: repr(val) for key, val in submit_params.items() if val is not None}
        if self._continue_on_step_failure is not None:
            submit_params["continue_on_step_failure"] = self._continue_on_step_failure
        if self._tags is not None:
            submit_params["tags"] = _normalize_dict_param_val(self._tags)
        return submit_params

    @property
    def entry_template_keys(self):
        return [
            "header",
            "pipeline_module_name",
            "pipeline_submit_params"
        ]

    @property
    def tpl_file(self):
        return RUN_TEMPLATE


class NotebookGenerator(CodeBaseGenerator):
    DEFAULT_EXPERIMENT_NAME = "sample-experiment-name"
    TARGET_FILE = "run.ipynb"

    def __init__(self, root_pipeline_generator: PipelineCodeGenerator, url=None, run=None,
                 description=None, tags=None, display_name=None, continue_on_step_failure=None,
                 default_compute_target=None):
        super(NotebookGenerator, self).__init__(target_file=self.TARGET_FILE, logger=_logger)
        self.pipeline_module_name = root_pipeline_generator.module_name
        self._url = url if url else CodeFileHeaderGenerator.DEFAULT_URL
        self._experiment_name = self.DEFAULT_EXPERIMENT_NAME if not run else run.experiment.name
        self._description = description
        self._tags = tags
        self._display_name = display_name
        self._continue_on_step_failure = continue_on_step_failure
        self._default_compute_target = default_compute_target
        self._workspace_name = root_pipeline_generator._workspace_name

    @property
    def url(self):
        return self._url

    @property
    def pipeline_submit_params(self):
        submit_params = {
            "workspace": self._workspace_name
        }
        extra_params = {
            "experiment_name": self._experiment_name,
            "description": self._description,
            "display_name": self._display_name,
            "continue_on_step_failure": self._continue_on_step_failure,
            "default_compute_target": self._default_compute_target,
        }
        extra_params = {key: repr(val) for key, val in extra_params.items() if val is not None}
        submit_params.update(extra_params)
        if self._continue_on_step_failure is not None:
            submit_params["continue_on_step_failure"] = self._continue_on_step_failure
        if self._tags is not None:
            # TODO: format this
            submit_params["tags"] = repr({key: self._tags[key] for key in sorted(self._tags)})
        return submit_params

    @property
    def tpl_file(self):
        return NOTE_BOOK_TEMPLATE

    @property
    def entry_template_keys(self):
        # use entry_template_key_val here to customize template keys
        return [
            "url",
            "pipeline_module_name",
            "pipeline_submit_params"
        ]


class PipelinePackageGenerator:

    def __init__(
            self, service_caller: DesignerServiceCaller, root_graph: PipelineGraph, url: str, pipeline_identifier: str,
            include_components: str = None, target_dir=None, root_run: Run = None,
            description: str = None, tags: str = None, display_name: str = None, pipeline_name=None
    ):
        self.url = url
        self.service_caller = service_caller
        self.logger = _logger
        self.pipeline_identifier = pipeline_identifier
        self.description = description
        self.tags = tags
        self.display_name = display_name
        self.root_run = root_run
        self.default_compute_target = root_graph.default_compute.name
        try:
            self.continue_on_step_failure = root_run.properties["azureml.continue_on_step_failure"]
        except AttributeError:
            self.continue_on_step_failure = None
        if not pipeline_name:
            pipeline_name = self.pipeline_identifier
        self.pipeline_name = pipeline_name

        if not target_dir:
            target_dir = self.pipeline_identifier[:PIPELINE_IDENTIFIER_TRIM_LEN]
            self.target_dir = get_new_dir_name_if_exists(Path(target_dir))
        else:
            self.target_dir = Path(target_dir)
        _logger.debug(f"Generating code in {self.target_dir}")

        self.workspace = self.service_caller._workspace
        # Mapping from graph id to graph entity
        self.graph_id_2_entity = {}
        # Mapping from graph id to definition
        self.graph_id_2_definition = {}

        self._get_graphs_for_anonymous_pipeline_components(root_graph)
        self.graphs = list(self.graph_id_2_entity.values())
        self.graphs.append(root_graph)
        self.pkg_util = GraphPackageUtil(self.graphs, include_components=include_components, logger=self.logger)
        self._components_dir = self.target_dir / self.pkg_util.COMPONENT_PACKAGE_NAME
        self._pipelines_dir = self.target_dir / self.pkg_util.PIPELINE_PACKAGE_NAME
        self._sub_pipeline_dir = self._pipelines_dir / self.pkg_util.SUBGRAPH_PACKAGE_NAME
        self.run_script_path = self.target_dir / RunScript.TARGET_FILE

        self._file_header_generator = CodeFileHeaderGenerator(url=self.url, logger=self.logger)
        file_header = self._file_header_generator.to_component_entry_code()
        self._subgraph_generators = [
            PipelineCodeGenerator(
                graph, self.pkg_util,
                definition=self.graph_id_2_definition[id],
                run=self.root_run,
                header=file_header,
                logger=self.logger
            ) for id, graph in self.graph_id_2_entity.items()
        ]
        self._root_graph_generator = PipelineCodeGenerator(
            root_graph, self.pkg_util, is_root=True, module_name=self.pipeline_identifier, run=self.root_run,
            header=file_header, logger=self.logger
        )

        self._run_generator = RunScript(
            root_pipeline_generator=self._root_graph_generator, header=file_header, run=self.root_run,
            description=self.description, tags=self.tags, display_name=self.display_name,
            continue_on_step_failure=self.continue_on_step_failure, default_compute_target=self.default_compute_target)
        self._notebook_generator = NotebookGenerator(
            root_pipeline_generator=self._root_graph_generator, url=self.url, run=self.root_run,
            description=self.description, tags=self.tags, display_name=self.display_name,
            continue_on_step_failure=self.continue_on_step_failure, default_compute_target=self.default_compute_target)

    def _get_graphs_for_anonymous_pipeline_components(self, root_graph: PipelineGraph):
        self.logger.info(f"Fetching subgraph info for {self.pipeline_name}...")
        with TimerContext() as timer_context:
            # Create a separate logger here since we don't want debug info show in console.
            logger = logging.getLogger("get_sub_graphs")
            with TaskQueue(_parent_logger=logger) as task_queue:

                def _get_graphs_recursively(graph_id, graph_definition=None, graph=None):
                    if graph is None:
                        graph = self.service_caller._get_pipeline_component_graph(
                            graph_id=graph_id, skip_dataset_load=False
                        )
                        self.graph_id_2_entity[graph_id] = graph
                        self.graph_id_2_definition[graph_id] = graph_definition
                    subgraph_module_id_2_graph_id = {n.module_id: n.graph_id for n in graph.sub_graph_nodes}
                    for dto in graph.graph_module_dtos:
                        component_id = dto.module_version_id
                        if component_id in subgraph_module_id_2_graph_id.keys() and _is_anonymous_pipeline_component(
                                dto):
                            graph_id = subgraph_module_id_2_graph_id[component_id]
                            if not graph_id:
                                graph_id = dto.module_entity.cloud_settings.sub_graph_config.graph_id
                            # Note: this may run multiple time for same sub graph if they share same graph id
                            if graph_id not in self.graph_id_2_entity.keys():
                                task_queue.add(_get_graphs_recursively, graph_id, dto)

                _get_graphs_recursively(graph_id=None, graph=root_graph)
                # Note: we added tasks that will dynamically add tasks to task queue
                # so we need to flush task queue until it has no tasks left
                while not task_queue._tasks.empty():
                    task_queue.flush(source='iter_files_in_parallel')
        self.logger.info(f"Finished fetch subgraph info in {timer_context.get_duration_seconds()} seconds.")

    def generate(self):
        self.target_dir.mkdir(exist_ok=True)
        # generate root pipeline code
        self._pipelines_dir.mkdir(exist_ok=True)
        self._root_graph_generator.to_component_entry_file(self._pipelines_dir)
        # generate sub pipeline code
        if self._subgraph_generators:
            self._sub_pipeline_dir.mkdir(exist_ok=True)
        for g in self._subgraph_generators:
            g.to_component_entry_file(self._pipelines_dir)
        # generate components
        self._components_dir.mkdir(exist_ok=True)
        # Skip snapshot sas download progress bar
        with environment_variable_overwrite(AML_COMPONENT_SNAPSHOT_WITHOUT_DOWNLOAD_PROGRESS_BAR, "True"):
            GraphComponentSnapshotGenerator(
                workspace=self.workspace, target_directory=self.target_dir,
                module_name=self.pkg_util.COMPONENT_PACKAGE_NAME,
                component_id_2_func_name=self.pkg_util.generated_id_2_function,
                component_id_2_module_name=self.pkg_util.generated_id_2_module,
                snapshot_component_ids=self.pkg_util.snapshot_module_ids
            ).generate()
        # generate workspace config
        self.workspace.write_config(self.target_dir)
        # generate run script
        self._run_generator.to_component_entry_file(target_dir=self.target_dir)
        # generate notebook
        self._notebook_generator.to_component_entry_file(target_dir=self.target_dir)


class PipelineInfo:
    """A data class which stores pipeline information."""

    def __init__(self, subscription_id: str = None, resource_group: str = None, workspace_name: str = None,
                 draft_id: str = None, run_id: str = None, endpoint_id: str = None,
                 published_pipeline_id: str = None, graph_id: str = None, url: str = None):
        self.subscription_id = subscription_id
        self.resource_group = resource_group
        self.workspace_name = workspace_name
        self.draft_id = draft_id
        self.run_id = run_id
        self.endpoint_id = endpoint_id
        self.published_pipeline_id = published_pipeline_id
        self.graph_id = graph_id
        self.url = url

    def get_workspace(self):
        if self.subscription_id and self.resource_group and self.workspace_name:
            try:
                auth = AzureCliAuthentication()
            except Exception as e:
                # Fall back to interactive login auth.
                auth = None
            return Workspace.get(
                auth=auth,
                name=self.workspace_name,
                resource_group=self.resource_group,
                subscription_id=self.subscription_id
            )
        else:
            _logger.info(f"Failed to get workspace info: {self}")
            path = Path(".").absolute()
            _logger.info(f"Trying to get workspace info from config. Starting location: {path}")
            return Workspace.from_config()

    def get_pipeline_generator_params(self, workspace):
        service_caller = _DesignerServiceCallerFactory.get_instance(workspace)
        root_run, display_name, description, tags = None, None, None, None
        if self.draft_id:
            _logger.debug(f"Fetching pipeline draft: {self.draft_id}")
            pipeline_draft = service_caller.get_pipeline_draft(draft_id=self.draft_id, has_namespace_concept=False)
            pipeline_draft = pipeline_draft._raw_pipeline_draft
            pipeline_graph = pipeline_draft.graph_detail.graph
            # Use draft name as run identifier
            pipeline_identifier = _sanitize_python_variable_name(pipeline_draft.name)
            description = pipeline_draft.description
            tags = pipeline_draft.tags
        elif self.graph_id:
            # TODO(1594373): get pipeline parameter's actual value
            #   pipeline parameter's get from pipeline run id
            #   input binding get from run details
            _logger.debug(f"Fetching sub graph: {self.graph_id}")
            raise NotImplementedError("Exporting sub pipeline is not supported currently.")
        elif self.run_id:
            _logger.debug(f"Fetching pipeline run: {self.run_id}")
            pipeline_run = service_caller.get_pipeline_run(self.run_id)
            experiment_name = pipeline_run.experiment_name
            run_id = pipeline_run.id
            experiment = Experiment(workspace=workspace, name=experiment_name)
            root_run = Run(experiment, run_id=run_id)
            if not self.url:
                self.url = root_run.get_portal_url()
            pipeline_graph = service_caller.get_pipeline_run_graph_no_status(
                pipeline_run_id=run_id, has_namespace_concept=False)
            pipeline_identifier = _get_pipeline_identifier(root_run)
            description = pipeline_run.description
            tags = pipeline_run.tags
            display_name = pipeline_run.display_name
        elif self.published_pipeline_id:
            _logger.debug(f"Fetching published pipeline: {self.published_pipeline_id}")
            pipeline_graph = service_caller.get_published_pipeline_graph(
                pipeline_id=self.published_pipeline_id, has_namespace_concept=False, include_run_setting_params=False)
            published_pipeline = service_caller.get_published_pipeline(pipeline_id=self.published_pipeline_id)
            # Use published pipeline name as run identifier
            pipeline_identifier = _sanitize_python_variable_name(published_pipeline.name)
        elif self.endpoint_id:
            _logger.debug(f"Fetching pipeline endpoint: {self.endpoint_id}")
            pipeline_graph = service_caller.get_pipeline_endpoint_graph(
                endpoint_id=self.endpoint_id, has_namespace_concept=False)
            pipeline_endpoint = service_caller.get_pipeline_endpoint(self.endpoint_id)
            # Use endpoint name as run identifier
            pipeline_identifier = _sanitize_python_variable_name(pipeline_endpoint.name)
        else:
            raise UserErrorException("One of draft_id, run_id, published_pipeline_id, endpoint_id should be provided.")
        return dict(
            service_caller=service_caller, root_graph=pipeline_graph, url=self.url,
            pipeline_identifier=pipeline_identifier,
            root_run=root_run,
            description=description, tags=tags, display_name=display_name
        )

    def __str__(self):
        return str(dict(
            subscription_id=self.subscription_id,
            resource_group=self.resource_group,
            workspace_name=self.workspace_name,
            draft_id=self.draft_id,
            run_id=self.run_id,
            endpoint_id=self.endpoint_id,
            published_pipeline_id=self.published_pipeline_id,
            graph_id=self.graph_id,
            url=self.url
        ))


def _get_pipeline_info(url: str = None, subscription_id=None, resource_group=None, workspace_name=None, run_id=None):
    if url is not None:
        pipeline_info = PipelineInfo(*_parse_designer_url(url), url=url)
    else:
        pipeline_info = PipelineInfo(
            subscription_id, resource_group, workspace_name, None, run_id, None, None, None)
    return pipeline_info


def _generate_package(
        url: str = None,
        subscription_id=None, resource_group=None, workspace_name=None, run_id=None,
        include_components=None, target_dir=None
):
    pipeline_info = _get_pipeline_info(url, subscription_id, resource_group, workspace_name, run_id)
    _logger.debug(f"Parsed pipeline info {pipeline_info}")
    _logger.info("========== Starting export pipeline code ==========")
    with TimerContext() as timer_context:
        workspace = pipeline_info.get_workspace()
        generator = _generate_code(workspace=workspace, include_components=include_components,
                                   target_dir=target_dir, pipeline_info=pipeline_info)
    _logger.info(f"Generated code location: {generator.target_dir.absolute()}")
    _logger.info(f"Run `python {generator.run_script_path.absolute()}` to submit the generated pipeline.")
    _logger.info(f"Run `python {generator.run_script_path.absolute()} -v` to validate the generated pipeline.")
    _logger.info(
        f"========== Finished generate code in {timer_context.get_duration_seconds()} seconds ==========")


@track(activity_type=_PUBLIC_API, activity_name="graph_to_code")
def _generate_code(workspace, target_dir, pipeline_info: PipelineInfo, include_components=None):
    kw_args = pipeline_info.get_pipeline_generator_params(workspace)
    generator = PipelinePackageGenerator(
        include_components=include_components, target_dir=target_dir, **kw_args)
    generator.generate()
    return generator


class PipelinePackageCompare(PipelinePackageGenerator):
    def __init__(
            self, service_caller: DesignerServiceCaller, root_graph: PipelineGraph, url: str, pipeline_identifier: str,
            include_components: str = None, target_dir=None, root_run: Run = None,
            description: str = None, tags: str = None, display_name: str = None):
        super(PipelinePackageCompare, self).__init__(
            service_caller=service_caller, root_graph=root_graph, url="compare_pipeline", pipeline_identifier="main",
            include_components=include_components, target_dir=target_dir, root_run=root_run,
            description=description, tags=tags, display_name=display_name,
            pipeline_name=pipeline_identifier
        )


def _compare_package(
        run_item1: str = None, run_item2: str = None,
        subscription_id=None, resource_group=None, workspace_name=None,
        include_components: str = None, target_dir=None):
    if _looks_like_a_url(run_item1):
        pipeline_info1 = _get_pipeline_info(run_item1, subscription_id, resource_group, workspace_name)
    else:
        pipeline_info1 = _get_pipeline_info(None, subscription_id, resource_group, workspace_name, run_id=run_item1)

    if _looks_like_a_url(run_item2):
        pipeline_info2 = _get_pipeline_info(run_item2, subscription_id, resource_group, workspace_name)
    else:
        pipeline_info2 = _get_pipeline_info(None, subscription_id, resource_group, workspace_name, run_id=run_item2)
    _logger.info("========== Starting export and compare pipeline code ==========")
    with TimerContext() as timer_context:
        workspace1 = pipeline_info1.get_workspace()
        workspace2 = pipeline_info2.get_workspace()
        target_dir1, target_dir2 = _compare_code(workspace1, workspace2, pipeline_info1, pipeline_info2,
                                                 include_components, target_dir)

    def _is_file_excluded(file):
        return False

    folder1 = create_merkletree(target_dir1, _is_file_excluded)
    folder2 = create_merkletree(target_dir2, _is_file_excluded)
    diff = compute_diff(folder1, folder2)
    message = f"the exported pipelines: {target_dir1} {target_dir2}"
    if diff:
        _logger.info(f"Diff detected in {message}")
    else:
        _logger.info(f"No diff detected in {message}")

    _logger.info(
        f"========== Finished generate and compare code in {timer_context.get_duration_seconds()} seconds ==========")
    return target_dir1, target_dir2


@track(activity_type=_PUBLIC_API, activity_name="compare_graph")
def _compare_code(workspace1, workspace2, pipeline_info1, pipeline_info2, include_components, target_dir):
    # get pipeline info
    kw_args1 = pipeline_info1.get_pipeline_generator_params(workspace1)
    kw_args2 = pipeline_info2.get_pipeline_generator_params(workspace2)

    pipeline_identifier_1 = kw_args1["pipeline_identifier"][:PIPELINE_IDENTIFIER_TRIM_LEN]
    pipeline_identifier_2 = kw_args2["pipeline_identifier"][:PIPELINE_IDENTIFIER_TRIM_LEN]

    # generate 2 pipeline codes in one parent folder
    if target_dir is None:
        # trim pipeline identifier due to windows path length limitation.
        target_dir = _sanitize_folder_name(f"{pipeline_identifier_1}-{pipeline_identifier_2}")
    target_dir = get_new_dir_name_if_exists(Path(target_dir))
    target_dir.mkdir()
    target_dir1 = target_dir / "pipeline1"
    target_dir2 = target_dir / "pipeline2"

    # fetch sub-pipelines
    generator1 = PipelinePackageCompare(
        include_components=include_components, target_dir=target_dir1, **kw_args1)
    generator2 = PipelinePackageCompare(
        include_components=include_components, target_dir=target_dir2, **kw_args2)

    generator1.generate()
    generator2.generate()
    # todo: invoke local comparing tool or print message to guide user to open diff tool
    return target_dir1.absolute(), target_dir2.absolute()
