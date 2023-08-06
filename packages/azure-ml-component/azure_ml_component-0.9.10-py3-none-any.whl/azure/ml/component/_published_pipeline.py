# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from collections import OrderedDict

from azureml._html.utilities import to_html
from azureml.core import Workspace, Experiment

from ._restclients.designer.models import PublishedPipelineSummary, PublishedPipeline as RawPublishedPipeline, \
    CreatePublishedPipelineRequest, SubmitPipelineRunRequest
from ._restclients.service_caller_factory import _DesignerServiceCallerFactory
from ._util._loggerfactory import _LoggerFactory, _PUBLIC_API, track
from ._util._telemetry import WorkspaceTelemetryMixin, _get_telemetry_value_from_pipeline_parameter
from ._util._utils import resolve_pipeline_parameters, ensure_valid_experiment_name
from .run import Run

_logger = None


def _get_logger():
    global _logger
    if _logger is not None:
        return _logger
    _logger = _LoggerFactory.get_logger()
    return _logger


class PublishedPipeline(WorkspaceTelemetryMixin):
    """
    PublishedPipeline

    :param id: The ID of the published pipeline.
    :type id: str
    :param name: The name of the published pipeline.
    :type name: str
    :param description: The description of the published pipeline.
    :type description: str
    :param total_run_steps: The number of steps in this pipeline.
    :type total_run_steps: int
    :param total_runs: The number of runs in this pipeline.
    :type total_runs: int
    :param parameters: parameters of published pipeline.
    :type parameters: dict[str, str]
    :param endpoint: The REST endpoint URL to submit runs for this pipeline.
    :type endpoint: str
    :param graph_id: The ID of the graph for this published pipeline.
    :type graph_id: str
    :param published_date: The published date of this pipeline.
    :type published_date: datetime
    :param last_run_time: The last run time of this pipeline.
    :type last_run_time: datetime
    :param last_run_status: Possible values include: 'NotStarted', 'Running',
     'Failed', 'Finished', 'Canceled'.
    :type last_run_status: str or ~designer.models.PipelineRunStatusCode
    :param published_by: user name who published this pipeline.
    :type published_by: str
    :param tags: tags of pipeline.
    :type tags: dict[str, str]
    :param is_default: if pipeline is the default one in pipeline_endpoint.
    :type is_default: bool
    :param entity_status: Possible values include: 'Active', 'Deprecated',
     'Disabled'
    :type entity_status: str or ~designer.models.EntityStatus
    :param created_date: create date of pipeline.
    :type created_date: datetime
    :param last_modified_date: last modified date of published pipeline.
    :type last_modified_date: datetime
    :param workspace: The workspace of the published pipeline.
    :type workspace: azureml.core.Workspace
    """

    def __init__(self, id: str = None, name: str = None, description: str = None, total_run_steps: int = None,
                 total_runs: int = None, parameters: dict = None, endpoint: str = None, graph_id: str = None,
                 published_date=None, last_run_time=None, last_run_status=None, published_by: str = None,
                 tags=None, entity_status=None, created_date=None, last_modified_date=None,
                 workspace: Workspace = None, data_set_definition_value_assignment=None) -> None:
        """
        Initialize PublishedPipeline

        :param id: The ID of the published pipeline.
        :type id: str
        :param name: The name of the published pipeline.
        :type name: str
        :param description: The description of the published pipeline.
        :type description: str
        :param total_run_steps: The number of steps in this pipeline.
        :type total_run_steps: int
        :param total_runs: The number of runs in this pipeline.
        :type total_runs: int
        :param parameters: parameters of published pipeline.
        :type parameters: dict[str, str]
        :param rest_endpoint: The REST endpoint URL to submit runs for this pipeline.
        :type rest_endpoint: str
        :param graph_id: The ID of the graph for this published pipeline.
        :type graph_id: str
        :param published_date: The published date of this pipeline.
        :type published_date: datetime
        :param last_run_time: The last run time of this pipeline.
        :type last_run_time: datetime
        :param last_run_status: Possible values include: 'NotStarted', 'Running',
         'Failed', 'Finished', 'Canceled'.
        :type last_run_status: str or ~designer.models.PipelineRunStatusCode
        :param published_by: user name who published this pipeline.
        :type published_by: str
        :param tags: tags of pipeline.
        :type tags: dict[str, str]
        :param entity_status: Possible values include: 'Active', 'Deprecated',
         'Disabled'
        :type entity_status: str or ~designer.models.EntityStatus
        :param created_date: create date of pipeline.
        :type created_date: datetime
        :param last_modified_date: last modified date of published pipeline.
        :type last_modified_date: datetime
        :param workspace: The workspace of the published pipeline.
        :type workspace: azureml.core.Workspace
        :param data_set_definition_value_assignment: the dataset parameters value dict.
        :type data_set_definition_value_assignment: dict[str, obj]
        """
        super().__init__(workspace=workspace)
        self._id = id
        self._name = name
        self._description = description
        self._total_run_steps = total_run_steps
        self._total_runs = total_runs
        self._parameters = parameters
        self._endpoint = endpoint
        self._graph_id = graph_id
        self._published_date = published_date
        self._last_run_time = last_run_time
        self._last_run_status = last_run_status
        self._published_by = published_by
        self._tags = tags
        self._status = entity_status
        self._created_date = created_date
        self._last_modified_date = last_modified_date
        self._workspace = workspace
        self._data_set_definition_value_assignment = data_set_definition_value_assignment

    @property
    def id(self):
        """
        Property method to get published_pipeline's id.

        :return: The id.
        :rtype: str
        """
        return self._id

    @property
    def name(self):
        """
        Property method to get published_pipeline's name.

        :return: The name.
        :rtype: str
        """
        return self._name

    @property
    def description(self):
        """
        Property method to get published_pipeline's description.

        :return: The description.
        :rtype: str
        """
        return self._description

    @property
    def workspace(self):
        """
        Property method to get published_pipeline's workspace

        :return: The workspace.
        :rtype: azureml.core.Workspace
        """
        return self._workspace

    @property
    def endpoint(self):
        """
        Property method to get published_pipeline's rest_endpoint url.

        :return: The rest_endpoint.
        :rtype: str
        """
        self._ensure_properties_get()
        return self._endpoint

    @property
    def status(self):
        """
        Property method to get published_pipeline's status.

        :return: The status. Possible values include: 'Active', 'Deprecated',
         'Disabled'.
        :rtype: str
        """
        return self._status

    @property
    def tags(self):
        """
        Get the tags of published_pipeline.

        :return: The tags.
        :rtype: dict
        """
        return self._tags

    @property
    def parameters(self):
        """
        Get the parameters of published_pipeline.

        :return: The parameters.
        :rtype: dict
        """
        self._ensure_properties_get()
        return self._parameters

    @property
    def data_set_definition_value_assignment(self):
        """
        Get the dataset parameter dict values of published_pipeline.

        :return: The dataset definition value.
        :rtype: dict
        """
        return self._data_set_definition_value_assignment

    @staticmethod
    @track(activity_type=_PUBLIC_API)
    def get(workspace, id):
        """
        Get the published pipeline.

        :param workspace: The workspace the published pipeline was created in.
        :type workspace: azureml.core.Workspace
        :param id: The ID of the published pipeline.
        :type id: str

        :return: A PublishedPipeline object.
        :rtype: azure.ml.component._published_pipeline.PublishedPipeline
        """
        service_caller = _DesignerServiceCallerFactory.get_instance(workspace)
        result = service_caller.get_published_pipeline(pipeline_id=id)
        return PublishedPipeline._from_service_caller_model(workspace, result)

    @staticmethod
    @track(activity_type=_PUBLIC_API)
    def list(workspace, active_only=True):
        """
        Get all (includes disabled) published pipelines which has no related pipeline endpoint
            in the current workspace.
        None of returned published pipeline have `total_run_steps`, `total_runs`,
            `parameters` and `rest_endpoint` attribute, you can get them by `PublishedPipeline.get()`
            function with workspace and published pipeline id.

        :param workspace: The workspace the published pipeline was created in.
        :type workspace: azureml.core.Workspace
        :param active_only: list only active pipelines
        :type active_only: bool

        :return: A list of PublishedPipeline objects.
        :rtype: builtin.list[azure.ml.component.published_pipeline_summary.PublishedPipelineSummary]
        """

        service_caller = _DesignerServiceCallerFactory.get_instance(workspace)
        results = service_caller.list_published_pipelines(active_only=active_only)
        return [PublishedPipeline._from_service_caller_summary(workspace, result) for result in results]

    @track(activity_type=_PUBLIC_API)
    def enable(self):
        """Set the published pipeline to 'Active' and available to run."""
        service_caller = _DesignerServiceCallerFactory.get_instance(self.workspace)
        service_caller.enable_published_pipeline(self._id)
        self._status = 'Active'

    @track(activity_type=_PUBLIC_API)
    def disable(self):
        """Set the published pipeline to 'Disabled' and unavailable to run."""
        service_caller = _DesignerServiceCallerFactory.get_instance(self.workspace)
        service_caller.disable_published_pipeline(self._id)
        self._status = 'Disabled'

    @track(activity_type=_PUBLIC_API)
    def submit(self, experiment_name: str = None, description: str = None, pipeline_parameters: dict = None):
        """
        Submit the published pipeline.

        Returns the submitted :class:`azure.ml.component.Run`. Use this object to monitor and
        view details of the run.
        PipelineEndpoints can be used to create new versions of a :class:`azureml.pipeline.core.PublishedPipeline`
        while maintaining the same endpoint. PipelineEndpoints are uniquely named within a workspace.

        Using the endpoint attribute of a PipelineEndpoint object, you can trigger new pipeline runs from external
        applications with REST calls. For information about how to authenticate when calling REST endpoints, see
        https://aka.ms/pl-restep-auth.

        :param experiment_name: The name of the experiment to submit to, if it's not assigned by user, use published
        pipeline name as experiment name.
        :type experiment_name: str
        :param description: A clear description to distinguish runs.
        :type description: str
        :param pipeline_parameters: parameters of pipeline
        :type pipeline_parameters: dict

        :return: The submitted pipeline run.
        :rtype: azure.ml.component.Run
        """
        experiment_name = ensure_valid_experiment_name(experiment_name, self.name)

        if pipeline_parameters is None:
            pipeline_parameters = {}
        pipeline_parameters, dataset_def_value_assignments, data_path_assignments = resolve_pipeline_parameters(
            pipeline_parameters,
            flatten=True,
            resolve_dataset=True,
            workspace=self.workspace,
            resolve_data_path=True
        )

        telemetry_values = self._get_telemetry_values()
        telemetry_values.update({
            'pipeline_id': self._id,
        })
        telemetry_values.update(_get_telemetry_value_from_pipeline_parameter(pipeline_parameters))
        _LoggerFactory.add_track_dimensions(_get_logger(), telemetry_values)

        request = SubmitPipelineRunRequest(
            experiment_name=experiment_name,
            description=description,
            pipeline_parameters=pipeline_parameters if len(pipeline_parameters) > 0 else None,
            data_path_assignments=data_path_assignments if len(data_path_assignments) > 0 else None,
            data_set_definition_value_assignments=dataset_def_value_assignments
            if len(dataset_def_value_assignments) > 0 else None
        )
        service_caller = _DesignerServiceCallerFactory.get_instance(self._workspace)
        run_id = service_caller.submit_published_pipeline_run(request=request, pipeline_id=self._id)
        print('Submitted PublishedPipelineRun', run_id)
        experiment = Experiment(self._workspace, experiment_name)
        run = Run(experiment, run_id)
        print('Link to Azure Machine Learning Portal:', run.get_portal_url())
        return run

    def _ensure_properties_get(self):
        if self._endpoint is None:
            pipeline = self.get(workspace=self.workspace, id=self.id)
            self._total_run_steps = pipeline._total_run_steps
            self._total_runs = pipeline._total_runs
            self._parameters = pipeline._parameters
            self._endpoint = pipeline._endpoint

    @staticmethod
    def create(workspace: Workspace,
               request: CreatePublishedPipelineRequest, run_id=None, pipeline=None) -> RawPublishedPipeline:
        if run_id is None and pipeline is None:
            raise Exception('Both "run_id" and "pipeline" not specified.')

        if pipeline:
            pipeline._ensure_registered_in_workspace(workspace)

        # Assert pipeline endpoint has unique name
        service_caller = _DesignerServiceCallerFactory.get_instance(workspace)
        if request.use_pipeline_endpoint:
            try:
                service_caller.get_pipeline_endpoint(name=request.pipeline_endpoint_name)
            except:
                print('Creating a new pipeline endpoint name "{0}"'.format(request.pipeline_endpoint_name))
                request.use_existing_pipeline_endpoint = False
            else:
                if request.use_existing_pipeline_endpoint is False:
                    raise Exception('Pipeline endpoint "{0}" already exists!'.format(request.pipeline_endpoint_name))
                else:
                    print('Using existing pipeline endpoint "{0}"'.format(request.pipeline_endpoint_name))

        result_id = service_caller.publish_pipeline_run(
            request=request,
            pipeline_run_id=run_id
        ) if run_id is not None \
            else service_caller.publish_pipeline_graph(
            request=request
        )
        return service_caller.get_published_pipeline(pipeline_id=result_id)

    @staticmethod
    def _publish_from_run(run: Run, name: str, description: str = None, tags: dict = None):
        """
        Publish a pipeline run and make it available for rerunning.

        You can get the pipeline rest endpoint from the PublishedPipeline object returned by this function. With the
        rest endpoint, you can invoke the pipeline from external applications using REST calls. For information
        about how to authenticate when calling REST endpoints, see https://aka.ms/pl-restep-auth.

        The original pipeline associated with the pipeline run is used as the base for the published pipeline.

        :param name: The name of the published pipeline.
        :type name: str
        :param description: The description of the published pipeline.
        :type description: str
        :param tags: tags of pipeline to publish
        :type tags: dict[str, str]
        :return: Created published pipeline.
        :rtype: azure.ml.component._published_pipeline.PublishedPipeline
        """
        experiment_name = run._experiment.name
        service_caller = _DesignerServiceCallerFactory.get_instance(run.workspace)
        graph = service_caller.get_pipeline_run_graph(experiment_name=experiment_name, pipeline_run_id=run.id).graph
        request = CreatePublishedPipelineRequest(
            pipeline_name=name,
            experiment_name=experiment_name,
            pipeline_description=description,
            pipeline_endpoint_name=None,
            pipeline_endpoint_description=None,
            tags=tags,
            graph=graph,
            module_node_run_settings=graph.module_node_run_settings,
            set_as_default_pipeline_for_endpoint=True,
            use_existing_pipeline_endpoint=False,
            use_pipeline_endpoint=False,
            properties=run._properties
        )
        result = PublishedPipeline.create(workspace=run.workspace, request=request, run_id=run.id)
        published_pipeline = PublishedPipeline._from_service_caller_model(run.workspace, result)
        telemetry_values = run._get_telemetry_values()
        telemetry_values.update({
            'run_id': run.id,
            'pipeline_id': result.id,
            'use_pipeline_endpoint': False,
        })
        _LoggerFactory.add_track_dimensions(_get_logger(), telemetry_values)
        return published_pipeline

    @staticmethod
    def _publish_to_endpoint_from_run(run: Run, name: str, pipeline_endpoint_name: str,
                                      description: str = None, pipeline_endpoint_description: str = None,
                                      set_as_default: bool = True, use_existing_pipeline_endpoint: bool = True,
                                      tags: dict = None):
        """
        Publish a pipeline run to pipeline_endpoint.

        A pipeline endpoint is a :class:`azure.ml.component.Pipeline` workflow
         that can be triggered from a unique endpoint URL.

        :param name: The name of the published pipeline.
        :type name: str
        :param description: The description of the published pipeline.
        :type description: str
        :param pipeline_endpoint_name: The name of pipeline endpoint.
        :type pipeline_endpoint_name: str
        :param pipeline_endpoint_description: The description of pipeline endpoint.
        :type pipeline_endpoint_description: str
        :param set_as_default: Whether to use pipeline published as the default version of pipeline endpoint.
        :type set_as_default: bool
        :param use_existing_pipeline_endpoint: Whether to use existing pipeline endpoint.
        :type use_existing_pipeline_endpoint: bool
        :param tags: tags of pipeline to publish
        :type tags: dict[str, str]

        :return: Created published pipeline inside pipeline endpoint.
        :rtype: azure.ml.component._published_pipeline.PublishedPipeline
        """
        experiment_name = run._experiment.name
        service_caller = _DesignerServiceCallerFactory.get_instance(run.workspace)
        graph = service_caller.get_pipeline_run_graph(experiment_name=experiment_name, pipeline_run_id=run.id).graph
        request = CreatePublishedPipelineRequest(
            pipeline_name=name,
            experiment_name=experiment_name,
            pipeline_description=description,
            pipeline_endpoint_name=pipeline_endpoint_name,
            pipeline_endpoint_description=pipeline_endpoint_description,
            tags=tags,
            graph=graph,
            module_node_run_settings=graph.module_node_run_settings,
            set_as_default_pipeline_for_endpoint=set_as_default,
            use_existing_pipeline_endpoint=use_existing_pipeline_endpoint,
            use_pipeline_endpoint=True,
            properties=run._properties
        )
        result = PublishedPipeline.create(workspace=run.workspace, request=request, run_id=run.id)
        published_pipeline = PublishedPipeline._from_service_caller_model(run.workspace, result)
        telemetry_values = run._get_telemetry_values()
        telemetry_values.update({
            'run_id': run.id,
            'pipeline_id': result.id,
            'use_pipeline_endpoint': True,
            'set_as_default': set_as_default,
            'use_existing_pipeline_endpoint': use_existing_pipeline_endpoint,
        })
        _LoggerFactory.add_track_dimensions(_get_logger(), telemetry_values)
        return published_pipeline

    @staticmethod
    def _from_service_caller_model(workspace, result: RawPublishedPipeline):
        return PublishedPipeline(
            id=result.id, name=result.name, description=result.description, total_run_steps=result.total_run_steps,
            total_runs=result.total_runs, parameters=result.parameters, endpoint=result.rest_endpoint,
            graph_id=result.graph_id, published_date=result.published_date, last_run_time=result.last_run_time,
            last_run_status=result.last_run_status, published_by=result.published_by, tags=result.tags,
            entity_status=result.entity_status, created_date=result.created_date,
            last_modified_date=result.last_modified_date, workspace=workspace,
            data_set_definition_value_assignment=result.data_set_definition_value_assignment)

    @staticmethod
    def _from_service_caller_summary(workspace, result: PublishedPipelineSummary):
        return PublishedPipeline(
            id=result.id, name=result.name, description=result.description, graph_id=result.graph_id,
            published_date=result.published_date, last_run_time=result.last_run_time,
            last_run_status=result.last_run_status, published_by=result.published_by, tags=result.tags,
            entity_status=result.entity_status, created_date=result.created_date,
            last_modified_date=result.last_modified_date, workspace=workspace)

    def _get_portal_url(self):
        netloc = ('https://ml.azure.com/pipeline/published/'
                  '{0}/detail?wsid=/subscriptions/{1}/resourcegroups/{2}/workspaces/{3}')
        return netloc.format(
            self.id, self._workspace.subscription_id, self._workspace.resource_group, self._workspace._workspace_name)

    def _repr_html_(self):
        info = self._get_base_info_dict()
        return to_html(info)

    def _get_base_info_dict(self):
        info = OrderedDict([
            ('Name', self.name),
            ('Description', self._description),
            ('Date updated', self._last_modified_date),
            ('Published by', self._published_by),
            ('Last run time', self._last_run_time),
            ('Last run status', self._last_run_status),
            ('Status', self.status),
            ('tags', ', '.join(["{}: {}".format(tag, self.tags[tag]) for tag in self.tags])),
            ('Portal Link', self._get_portal_url())
        ])
        return info

    def __str__(self):
        """Return the string representation of the PublishedPipeline."""
        info = self._get_base_info_dict()
        formatted_info = ',\n'.join(["{}: {}".format(k, v) for k, v in info.items()])
        return "PublishedPipeline({0})".format(formatted_info)

    def __repr__(self):
        """Return the representation of the PublishedPipeline."""
        return self.__str__()
