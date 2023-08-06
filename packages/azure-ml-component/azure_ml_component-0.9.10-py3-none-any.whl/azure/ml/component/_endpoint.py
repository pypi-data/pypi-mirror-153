# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Defines PipelineEndpoint class for managing pipelines including versioning and endpoints."""

from collections import OrderedDict
from datetime import datetime

from azureml._html.utilities import to_html
from azureml.core import Workspace, Experiment
from azureml.exceptions._azureml_exception import UserErrorException

from ._published_pipeline import PublishedPipeline
from ._restclients.designer.models import PipelineEndpoint as RawPipelineEndpoint, PipelineEndpointSummary, \
    SubmitPipelineRunRequest
from ._restclients.service_caller_factory import _DesignerServiceCallerFactory
from ._restclients.designer.models._designer_service_client_enums import EntityStatus
from ._util._loggerfactory import _LoggerFactory, _PUBLIC_API, track
from ._util._telemetry import WorkspaceTelemetryMixin, _get_telemetry_value_from_pipeline_parameter
from ._util._utils import resolve_pipeline_parameters, ensure_valid_experiment_name
from .pipeline import Pipeline
from .run import Run

_logger = None


def _get_logger():
    global _logger
    if _logger is not None:
        return _logger
    _logger = _LoggerFactory.get_logger()
    return _logger


class PipelineEndpoint(WorkspaceTelemetryMixin):
    """
    !!! Currently endpoint parameters are separated as parameters and data_set_definition_value_assignment.
    !!! Handle this problem before make pipeline endpoint public interface.

    Represents a :class:`azure.ml.component.Pipeline` workflow that can be triggered from a unique URL.

    PipelineEndpoints are uniquely named within a workspace.

    Using the endpoint attribute of a PipelineEndpoint object, you can trigger new pipeline runs from external
    applications with REST calls. For information about how to authenticate when calling REST endpoints, see
    https://aka.ms/pl-restep-auth.

    For more information about creating and running machine learning pipelines, see https://aka.ms/pl-first-pipeline.

    .. remarks::

        A PipelineEndpoint can be created from either a :class:`azure.ml.component.PipelineComponent`
        or a :class:`azure.ml.component.Run`.

        An example to publish from a Pipeline or PipelineRun is as follows:

        .. code-block:: python

            from azure.ml.component import PipelineEndpoint

            # The pipeline argument can be either a Pipeline or a PipelineRun
            pipeline_endpoint = PipelineEndpoint.publish(workspace=ws,
                                                         name='PipelineEndpointName',
                                                         pipeline=pipeline,
                                                         set_as_default=True,
                                                         description="New Pipeline Endpoint")

        An example of how to submit a PipelineEndpoint is as follows, it will submit the default pipeline version.
        When submit is called, a :class:`azure.ml.component.Run` is created:

        * parameters: Parameters to pipeline execution, dictionary of {name: value}.

        .. code-block:: python

            from azure.ml.component import PipelineEndpoint

            pipeline_endpoint = PipelineEndpoint.get(workspace=ws, name="PipelineEndpointName")
            pipeline_run = experiment.submit(experiment_name='ExperimentName',
                                             description='PipelineRunDescription',
                                             parameters={"param1": "value1"})

    :param workspace: The workspace object this PipelineEndpoint will belong to.
    :type workspace: azureml.core.Workspace
    :param id: The ID of the PipelineEndpoint.
    :type id: str
    :param name: The name of the PipelineEndpoint.
    :type name: str
    :param description: The description of the PipelineEndpoint.
    :type description: str
    :param status: The new status of the PipelineEndpoint: 'Active' or 'Disabled'.
    :type status: str
    :param default_version: The default version of pipeline in PipelineEndpoint, auto-increments, starts with "0"
    :type default_version: str
    :param published_date: The published date of this pipeline endpoint.
    :type published_date: datetime
    :param published_by: user name who published this pipeline endpoint.
    :type published_by: str
    :param last_run_time: The last run time of this pipeline endpoint.
    :type last_run_time: str
    :param last_run_status: status of last run
    :type last_run_status: str
    :param endpoint: The REST endpoint URL to submit runs for this pipeline endpoint.
    :type endpoint: str
    :param pipeline_parameters: parameters of pipeline endpoint.
    :type pipeline_parameters: dict[str, str]
    :param tags: tags of pipeline endpoint.
    :type tags: dict[str, str]
    :param created_date: created date of this pipeline endpoint.
    :type created_date: datetime
    :param last_modified_date: last modified date of pipeline endpoint.
    :type last_modified_date: datetime
    """

    def __init__(self, workspace: Workspace = None, id: str = None, name: str = None, description: str = None,
                 status: str = None, default_version: str = None, published_date=None,
                 published_by: str = None, last_run_time=None, last_run_status: str = None, endpoint: str = None,
                 pipeline_parameters: dict = None, tags=None, created_date=None, last_modified_date=None,
                 updated_by: str = None, data_set_definition_value_assignment: dict = None):
        """
        Initialize PipelineEndpoint.

        :param workspace: The workspace object this PipelineEndpoint will belong to.
        :type workspace: azureml.core.Workspace
        :param id: The ID of the PipelineEndpoint.
        :type id: str
        :param name: The name of the PipelineEndpoint.
        :type name: str
        :param description: The description of the PipelineEndpoint.
        :type description: str
        :param status: The new status of the PipelineEndpoint: 'Active' or 'Disabled'.
        :type status: str
        :param default_version: The default version of pipeline in PipelineEndpoint, auto-increments, starts with "0"
        :type default_version: str
        :param published_date: The published date of this pipeline endpoint.
        :type published_date: datetime
        :param published_by: user name who published this pipeline endpoint.
        :type published_by: str
        :param last_run_time: The last run time of this pipeline endpoint.
        :type last_run_time: str
        :param last_run_status: status of last run
        :type last_run_status: str
        :param endpoint: The REST endpoint URL to submit runs for this pipeline endpoint.
        :type endpoint: str
        :param pipeline_parameters: parameters of pipeline endpoint.
        :type pipeline_parameters: dict[str, str]
        :param tags: tags of pipeline endpoint.
        :type tags: dict[str, str]
        :param created_date: created date of this pipeline endpoint.
        :type created_date: datetime
        :param last_modified_date: last odufied date of pipeline endpoint.
        :type last_modified_date: datetime
        :param data_set_definition_value_assignment: the dataset parameters value dict.
        :type data_set_definition_value_assignment: dict[str, obj]
        """
        super().__init__(workspace=workspace)
        self._workspace = workspace
        self._id = id
        self._name = name
        self._description = description
        self._status = status
        self._default_version = default_version
        self._published_date = published_date
        self._published_by = published_by
        self._last_run_time = last_run_time
        self._last_run_status = last_run_status
        self._endpoint = endpoint
        self._pipeline_parameters = pipeline_parameters
        self._tags = tags
        self._created_date = created_date
        self._last_modified_date = last_modified_date
        self._updated_by = updated_by
        self._published_pipeline_provider = PublishedPipeline
        self._data_set_definition_value_assignment = data_set_definition_value_assignment

    @property
    def id(self):
        """
        Get the ID of the PipelineEndpoint.

        :return: The ID of the PipelineEndpoint.
        :rtype: str
        """
        return self._id

    @property
    def name(self):
        """
        Get the name of the PipelineEndpoint.

        :return: The name.
        :rtype: str
        """
        return self._name

    @property
    def description(self):
        """
        Get the description of the PipelineEndpoint.

        :return: The description.
        :rtype: str
        """
        return self._description

    @property
    def workspace(self):
        """
        Get the workspace of the PipelineEndpoint.

        :return: The workspace.
        :rtype: azureml.core.Workspace
        """
        return self._workspace

    @property
    def status(self):
        """
        Get the status of the PipelineEndpoint.

        :return: The status.
        :rtype: str
        """
        return self._status

    @property
    def default_version(self):
        """
        Get the default version of the PipelineEndpoint.

        :return: The default version.
        :rtype: str
        """
        self._ensure_properties_get()
        return self._default_version

    @property
    def endpoint(self):
        """
        Get the REST endpoint URL of the PipelineEndpoint.

        The endpoint can be used to trigger runs of the pipeline.

        :return: REST endpoint for PipelineEndpoint to run pipeline.
        :rtype: str
        """
        self._ensure_properties_get()
        return self._endpoint

    @property
    def tags(self):
        """
        Get the tags of PipelineEndpoint.

        :return: Pipeline endpoint tags.
        :rtype: dict
        """
        return self._tags

    @property
    def pipeline_parameters(self):
        """
        Get the pipeline parameters of PipelineEndpoint.

        :return: Pipeline endpoint parameters.
        :rtype: dict
        """
        self._ensure_properties_get()
        return self._pipeline_parameters

    @property
    def data_set_definition_value_assignment(self):
        """
        Get the dataset parameter dict values of pipeline endpoint.

        :return: The dataset definition value.
        :rtype: dict
        """
        self._ensure_properties_get()
        return self._data_set_definition_value_assignment

    @staticmethod
    @track(activity_type=_PUBLIC_API)
    def publish(workspace, name, pipeline, set_as_default: bool = True, description: str = None, tags: dict = None):
        """
        Create a PipelineEndpoint with the specified name and pipeline/pipeline run.

        The pipeline endpoint is a REST API that can be used from external applications. For information about how to
        authenticate when calling REST endpoints, see https://aka.ms/pl-restep-auth.

        For more information about working with pipeline endpoints, see https://aka.ms/pl-first-pipeline.

        :param workspace: The workspace to create the PipelineEndpoint in.
        :type workspace: azureml.core.Workspace
        :param name: The name of the PipelineEndpoint.
        :type name: str
        :param pipeline: The pipeline or pipeline_run.
        :type pipeline: azure.ml.component.Pipeline or azure.ml.component.Run
        :param set_as_default: Whether to use the pipeline as the default version of pipeline endpoint.
        :type set_as_default: bool
        :param description: The description of the PipelineEndpoint.
        :type description: str
        :param tags: The tags of pipeline to publish
        :type tags: dict[str, str]

        :return: A new PipelineEndpoint.
        :rtype: azure.ml.component._endpoint.PipelineEndpoint
        :raises ValueError:
        """
        timenow = datetime.now().strftime('%m-%d-%Y-%H-%M')

        if type(pipeline) is Pipeline:
            experiment_name = pipeline.name + "-" + timenow + "-experiment"
            published_pipeline_name = pipeline.name + "-" + timenow + "-published"
            published_pipeline_description = "description for " + published_pipeline_name
            pipeline._publish_to_endpoint(experiment_name=experiment_name,
                                          name=published_pipeline_name,
                                          description=published_pipeline_description,
                                          pipeline_endpoint_name=name,
                                          pipeline_endpoint_description=description,
                                          set_as_default=set_as_default,
                                          tags=tags,
                                          workspace=workspace)
            pipeline_endpoint = PipelineEndpoint.get(workspace, name=name)
            return pipeline_endpoint

        if type(pipeline) is Run:
            published_pipeline_name = pipeline._experiment.name + "-" + timenow + "-published"
            published_pipeline_description = pipeline._experiment.name + "description for " + published_pipeline_name
            PublishedPipeline._publish_to_endpoint_from_run(run=pipeline,
                                                            pipeline_endpoint_name=name,
                                                            name=published_pipeline_name,
                                                            description=published_pipeline_description,
                                                            pipeline_endpoint_description=description,
                                                            set_as_default=set_as_default,
                                                            tags=tags)
            pipeline_endpoint = PipelineEndpoint.get(workspace, name=name)
            return pipeline_endpoint

        raise UserErrorException("'pipeline' should be either type Pipeline or Run")

    @staticmethod
    @track(activity_type=_PUBLIC_API)
    def get(workspace, id: str = None, name: str = None):
        """
        Get PipelineEndpoint either by id or name.

        :param workspace: The workspace the pipeline endpoint was created in.
        :type workspace: azureml.core.Workspace
        :param id: The id of a PipelineEndpoint
        :type id: str
        :param name: The name of a PipelineEndpoint
        :type name: str

        :return: The PipelineEndpoint object
        :rtype: azure.ml.component._endpoint.PipelineEndpoint
        """
        service_caller = _DesignerServiceCallerFactory.get_instance(workspace)
        result = service_caller.get_pipeline_endpoint(id=id, name=name)

        pipeline_endpoint = PipelineEndpoint._from_service_caller_model(workspace, result)

        return pipeline_endpoint

    @staticmethod
    @track(activity_type=_PUBLIC_API)
    def list(workspace, active_only=True):
        """
        List PipelineEndpoints in the current workspace.

        :param workspace: The workspace of the pipeline endpoint was created in.
        :type workspace: azureml.core.Workspace
        :param active_only: If true, only return PipelineEndpoints which are currently active.
        :type active_only: bool

        :return: The list of :class:`azure.ml.component.endpoint.PipelineEndpoint` objects.
        :rtype: builtin.list
        """
        service_caller = _DesignerServiceCallerFactory.get_instance(workspace)
        endpoints = service_caller.list_pipeline_endpoints(active_only=active_only)

        return [PipelineEndpoint._from_service_caller_summary(workspace, result) for result in endpoints]

    @track(activity_type=_PUBLIC_API)
    def enable(self):
        """Set the pipeline endpoint to 'Active'."""
        service_caller = _DesignerServiceCallerFactory.get_instance(self.workspace)
        service_caller.enable_pipeline_endpoint(self._id)
        self._status = 'Active'

    @track(activity_type=_PUBLIC_API)
    def disable(self):
        """Set the pipeline endpoint to 'Active'."""
        service_caller = _DesignerServiceCallerFactory.get_instance(self.workspace)
        service_caller.disable_pipeline_endpoint(self._id)
        self._status = 'Disabled'

    @track(activity_type=_PUBLIC_API)
    def list_pipelines(self, active_only=True):
        """
        Get list of pipelines in PipelineEndpoint.

        :param active_only: Whether to return only active pipelines.
        :type active_only: bool
        :return: A dict with format {version: azure.ml.component._published_pipeline.PublishedPipeline}.
        :rtype: dict
        """
        service_caller = _DesignerServiceCallerFactory.get_instance(self.workspace)
        results = service_caller.get_pipeline_endpoint_pipelines(pipeline_endpoint_id=self._id)

        results_list = []
        for result in results:
            if active_only is True:
                if result.entity_status == EntityStatus.ACTIVE.value:
                    results_list.append(result)
            else:
                results_list.append(result)

        pipelines_list = {}
        for pipeline in results_list:
            published_pipeline_object = PublishedPipeline._from_service_caller_summary(self._workspace, pipeline)
            pipelines_list[pipeline.version] = published_pipeline_object

        return pipelines_list

    @track(activity_type=_PUBLIC_API)
    def set_default_version(self, version):
        """
        Set the default version of PipelineEndpoint, throws an exception if the specified version is not found.

        :param version: The version to set as the default version in PipelineEndpoint.
        :type version: str
        """
        service_caller = _DesignerServiceCallerFactory.get_instance(self.workspace)
        service_caller.set_pipeline_endpoint_default_version(endpoint_id=self._id, version=version)
        self._default_version = version

    @track(activity_type=_PUBLIC_API)
    def submit(self, experiment_name: str = None, description: str = None, pipeline_parameters: dict = None) -> Run:
        """
        Submit a pipeline experiment of default version.

        :param experiment_name: The name of the experiment to submit the pipeline in, if it's not assigned by user,
            use pipeline endpoint name as experiment name.
        :type experiment_name: str
        :param description: A clear description to distinguish runs.
        :type description: str
        :param pipeline_parameters: The parameters of pipeline.
        :type pipeline_parameters: dict

        :return: The submitted pipeline run.
        :rtype: azure.ml.component.Run
        """
        experiment_name = ensure_valid_experiment_name(experiment_name, self.name)

        status = self.status
        if status != 'Active':
            raise UserErrorException('Status of PipelineEndpoint must be Active, actually {}'.format(status))

        if pipeline_parameters is None:
            pipeline_parameters = {}
        pipeline_parameters, dataset_def_value_assignments, data_path_assignments = resolve_pipeline_parameters(
            pipeline_parameters,
            flatten=True,
            resolve_dataset=True,
            workspace=self.workspace,
            resolve_data_path=True
        )

        workspace = self.workspace
        telemetry_values = self._get_telemetry_values()
        telemetry_values.update({
            'pipeline_endpoint_id': self._id,
            'version': self.default_version
        })
        telemetry_values.update(_get_telemetry_value_from_pipeline_parameter(pipeline_parameters))
        _LoggerFactory.trace(_get_logger(), "PipelineEndpoint_submit", telemetry_values)

        service_caller = _DesignerServiceCallerFactory.get_instance(workspace)
        request = SubmitPipelineRunRequest(
            experiment_name=experiment_name,
            description=description,
            pipeline_parameters=pipeline_parameters if len(pipeline_parameters) > 0 else None,
            data_path_assignments=data_path_assignments if len(data_path_assignments) > 0 else None,
            data_set_definition_value_assignments=dataset_def_value_assignments
            if len(dataset_def_value_assignments) > 0 else None
        )
        run_id = service_caller.submit_pipeline_endpoint_run(request=request,
                                                             pipeline_endpoint_id=self._id)
        print('Submitted PipelineEndpointRun', run_id)
        experiment = Experiment(workspace, experiment_name)
        run = Run(experiment, run_id)
        print('Link to Azure Machine Learning Portal:', run.get_portal_url())
        return run

    def _ensure_properties_get(self):
        if self._endpoint is None:
            pipeline_endpoint = self.get(workspace=self.workspace, id=self.id)
            self._default_version = pipeline_endpoint._default_version
            self._endpoint = pipeline_endpoint._endpoint
            self._pipeline_parameters = pipeline_endpoint._pipeline_parameters
            self._published_date = pipeline_endpoint._published_date
            self._published_by = pipeline_endpoint._published_by
            self._last_run_time = pipeline_endpoint._last_run_time
            self._last_run_status = pipeline_endpoint._last_run_status
            self._data_set_definition_value_assignment = pipeline_endpoint._data_set_definition_value_assignment

    @staticmethod
    def _from_service_caller_model(workspace, result: RawPipelineEndpoint):
        return PipelineEndpoint(
            workspace=workspace, id=result.id, name=result.name, description=result.description,
            status=result.entity_status, default_version=result.default_version,
            endpoint=result.rest_endpoint, published_date=result.published_date, published_by=result.published_by,
            last_run_time=result.last_run_time, last_run_status=result.last_run_status,
            pipeline_parameters=result.parameters, tags=result.tags, created_date=result.created_date,
            last_modified_date=result.last_modified_date, updated_by=result.updated_by,
            data_set_definition_value_assignment=result.data_set_definition_value_assignment)

    @staticmethod
    def _from_service_caller_summary(workspace, result: PipelineEndpointSummary):
        return PipelineEndpoint(
            workspace=workspace, id=result.id, name=result.name, description=result.description,
            status=result.entity_status, tags=result.tags,
            created_date=result.created_date, last_modified_date=result.last_modified_date,
            updated_by=result.updated_by)

    def _get_portal_url(self):
        netloc = ('https://ml.azure.com/endpoint/'
                  '{0}/{1}/pipelines?wsid=/subscriptions/{2}/resourcegroups/{3}/workspaces/{4}')
        return netloc.format(
            self.id, self.name, self._workspace.subscription_id, self._workspace.resource_group,
            self._workspace._workspace_name)

    def _get_base_info_dict(self):
        info = OrderedDict([
            ('Name', self.name),
            ('Description', self._description),
            ('Date updated', self._last_modified_date),
            ('Updated by', self._updated_by),
            ('Last run time', self._last_run_time),
            ('Last run status', self._last_run_status),
            ('Status', self.status),
            ('tags', ', '.join(["{}: {}".format(tag, self.tags[tag]) for tag in self.tags])),
            ('Portal Link', self._get_portal_url())
        ])
        return info

    def _repr_html_(self):
        info = self._get_base_info_dict()
        return to_html(info)

    def __str__(self):
        """Return the string representation of PipelineEndpoint."""
        info = self._get_base_info_dict()
        formatted_info = ',\n'.join(["{}: {}".format(k, v) for k, v in info.items()])
        return "PipelineEndpoint({0})".format(formatted_info)

    def __repr__(self):
        """Return the representation of the PipelineEndpoint."""
        return self.__str__()
