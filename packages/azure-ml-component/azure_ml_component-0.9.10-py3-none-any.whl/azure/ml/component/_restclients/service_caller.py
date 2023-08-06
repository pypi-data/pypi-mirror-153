# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""service_calller.py, module for interacting with the AzureML service."""
import json
import logging
import os
import sys
from functools import lru_cache
from typing import List

from azure.core.pipeline import PipelineResponse
from azure.ml.component._restclients.designer.models import AssetScopeTypes, DataCategory, ModuleScope
from azureml._base_sdk_common import _ClientSessionId
from azureml.core.authentication import InteractiveLoginAuthentication
from azureml.exceptions._azureml_exception import UserErrorException
from .designer.designer_service_client import DesignerServiceClient
from msrest.exceptions import HttpOperationError
from .designer.models import SavePipelineDraftRequest, \
    PipelineType, PipelineDraftMode, BatchGetModuleRequest, AmlModuleNameMetaInfo, UpdateModuleRequest, \
    ComponentNameMetaInfo, BatchGetComponentRequest, ExperimentComputeMetaInfo, GraphModuleNodeRunSetting, \
    ModuleRunSettingTypes, ModuleDtoFields
from .pipeline_draft import PipelineDraft
from azure.ml.component._util._cache import ComputeTargetCache, RunsettingParametersDiskCache, \
    RegisteredComponentDiskCache, RegisteredPipelineComponentDiskCache
from azure.ml.component._util._loggerfactory import _LoggerFactory, track, _get_package_version
from azure.ml.component._util._telemetry import WorkspaceTelemetryMixin, RequestTelemetryMixin
from azure.ml.component._util._utils import _is_uuid, get_pipeline_response_content
from azureml.core.compute import ComputeTarget

_logger = None
_GLOBAL_MODULE_NAMESPACE = 'azureml'
_run_setting_type = ModuleRunSettingTypes.FULL
_module_dto_fields = ModuleDtoFields.MINIMAL


def _get_logger():
    global _logger
    if _logger is not None:
        return _logger
    _logger = _LoggerFactory.get_logger()
    return _logger


def _eat_exception_trace(function_name, function, **kwargs):
    try:
        result = function(**kwargs)
    except HttpOperationError as ex:
        error_msg = "{0} failed with exception: {1}".format(function_name, ex.message)
        raise UserErrorException(error_msg) from ex
    return result


class DesignerServiceCaller(WorkspaceTelemetryMixin, RequestTelemetryMixin):
    """DesignerServiceCaller.
    :param base_url: base url
    :type base_url: Service URL
    :param workspace: workspace
    :type workspace: Workspace
    """

    # The default namespace placeholder is used when namespace is None for get_module API.
    DEFAULT_COMPONENT_NAMESPACE_PLACEHOLDER = '-'
    DEFAULT_MODULE_WORKING_MECHANISM = 'OutputToDataset'
    DEFAULT_DATATYPE_MECHANISM = 'RegisterBuildinDataTypeOnly'
    MODULE_CLUSTER_ADDRESS = 'MODULE_CLUSTER_ADDRESS'
    WORKSPACE_INDEPENDENT_ENDPOINT_ADDRESS = 'WORKSPACE_INDEPENDENT_ENDPOINT_ADDRESS'
    DEFAULT_BASE_URL = 'https://{}.api.azureml.ms'
    MASTER_BASE_API = 'https://master.api.azureml-test.ms'
    DEFAULT_BASE_REGION = 'westus2'
    AML_USE_ARM_TOKEN = 'AML_USE_ARM_TOKEN'

    def __init__(self, workspace, base_url=None, region=None):
        """Initializes DesignerServiceCaller."""
        if 'get_instance' != sys._getframe().f_back.f_code.co_name:
            raise Exception('Please use `_DesignerServiceCallerFactory.get_instance()` to get'
                            ' service caller instead of creating a new one.')

        WorkspaceTelemetryMixin.__init__(self, workspace=workspace)
        if workspace is None:
            self.auth = InteractiveLoginAuthentication()
            if region != "master":
                base_url = self.DEFAULT_BASE_URL.format(region or self.DEFAULT_BASE_REGION)
            else:
                base_url = self.MASTER_BASE_API
            # for dev test, change base url with environment variable
            base_url = os.environ.get(self.WORKSPACE_INDEPENDENT_ENDPOINT_ADDRESS, default=base_url)
        else:
            self._service_context = workspace.service_context
            if base_url is None:
                base_url = self._service_context._get_pipelines_url()
                # for dev test, change base url with environment variable
                base_url = os.environ.get(self.MODULE_CLUSTER_ADDRESS, default=base_url)
            self._subscription_id = workspace.subscription_id
            self._resource_group_name = workspace.resource_group
            self._workspace_name = workspace.name
            self.auth = workspace._auth_object
            self._workspace = workspace

        self._service_endpoint = base_url
        logging.getLogger("azure.core.pipeline.policies.http_logging_policy").setLevel(logging.ERROR)
        logging.getLogger('urllib3.connectionpool').setLevel(logging.ERROR)
        self._caller = DesignerServiceClient(base_url=base_url)
        self._default_datastore = None
        self._has_azureml_client_token = False

    def _get_custom_headers(self, use_arm_token=None, enum_to_str=True):
        """Get custom request headers that we will send to designer service.

        :param use_arm_token: indicates whether the header will still use arm token,
         this is needed when designer servcie use this token to call rp directly
        :type use_arm_token: bool
        :param enum_to_str: indicates whether to add x-ms-jsonformat-enum-to-string header
        :type enum_to_str: bool
        :return: custom request header
        :rtype: str
        """

        if use_arm_token is None:
            use_arm_token = (os.environ.get(self.AML_USE_ARM_TOKEN, None) == 'True')

        custom_header = None

        if not use_arm_token:
            # check if the authentication object supports to get azureml client token
            try:
                client_token = self.auth._get_azureml_client_token()
                if client_token is not None:
                    custom_header = {"Authorization": "Bearer " + client_token}
                    self._has_azureml_client_token = True
            except:
                pass

        if custom_header is None:
            custom_header = self.auth.get_authentication_header()
            self._has_azureml_client_token = False

        request_id = self._request_id
        common_header = {
            "x-ms-client-session-id": _ClientSessionId,
            "x-ms-client-request-id": request_id
        }

        custom_header.update(common_header)

        if enum_to_str:
            custom_header.update({"x-ms-jsonformat-enum-to-string": "true"})

        return custom_header

    @track()
    def submit_pipeline_run(self, request, node_composition_mode=None):
        """Submit a pipeline run by graph

        :param request:
        :type request: ~designer.models.SubmitPipelineRunRequest
        :param node_composition_mode: Possible values include: 'None',
         'OnlySequential', 'Full'
        :type node_composition_mode: str
        :return: pipeline run id
        :rtype: str
        :raises:
         :class:`HttpOperationError<designer.models.HttpOperationError>`
        """

        result = self._caller.pipeline_runs_v2.submit_pipeline_run(
            body=request,
            node_composition_mode=node_composition_mode,
            subscription_id=self._subscription_id, resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name,
            headers=self._get_custom_headers())

        if not self._has_azureml_client_token:
            if _check_if_contains_scope_component(request.module_node_run_settings):
                logging.warning(
                    'Your azureml-core with version {} does not support OBO token.'.format(
                        _get_package_version('azureml-core')) +
                    ' Please refer https://aka.ms/scopecomponent' +
                    ' to find azureml-core version that supports OBO token for scope component.')
                # log this warning to app insights as well
                _get_logger().warning(
                    'Your azureml-core with version {} does not support OBO token.'.format(
                        _get_package_version('azureml-core')) +
                    ' Please refer https://aka.ms/scopecomponent' +
                    ' to find azureml-core version that supports OBO token for scope component.')

        return result

    @track()
    def submit_pipeline_draft_run(self, request, draft_id, node_composition_mode=None):
        """Submit a pipelineDraft run

        :param draft_id:
        :type draft_id: str
        :param request:
        :type request: ~designer.models.SubmitPipelineRunRequest
        :param node_composition_mode: Possible values include: 'None',
         'OnlySequential', 'Full'
        :type node_composition_mode: str
        :return: pipeline run id
        :rtype: str
        :raises:
         :class:`HttpOperationError<designer.models.HttpOperationError>`
        """

        result = self._caller.pipeline_drafts_v2.submit_pipeline_run(
            subscription_id=self._subscription_id, resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name, draft_id=draft_id, body=request,
            node_composition_mode=node_composition_mode, headers=self._get_custom_headers())

        return result

    @track()
    def submit_published_pipeline_run(self, request, pipeline_id):
        """Submit a published pipeline run

        :param pipeline_id:
        :type pipeline_id: str
        :param request:
        :type request: ~designer.models.SubmitPipelineRunRequest
        :return: pipeline run id
        :rtype: str
        :raises:
         :class:`ErrorResponseException<designer.models.ErrorResponseException>`
        """

        result = self._caller.published_pipelines_v2.submit_pipeline_run(
            subscription_id=self._subscription_id, resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name, pipeline_id=pipeline_id, body=request,
            headers=self._get_custom_headers())

        return result

    @track()
    def submit_pipeline_endpoint_run(self, request, pipeline_endpoint_id):
        """submit a pipeline endpoint run

        :param request:
        :type request: ~designer.models.SubmitPipelineRunRequest
        :param pipeline_endpoint_id:
        :type pipeline_endpoint_id: str
        :return: pipeline run id
        :rtype: str
        :raises:
         :class:`ErrorResponseException<designer.models.ErrorResponseException>`
        """

        result = self._caller.pipeline_endpoints_v2.submit_pipeline_run(
            subscription_id=self._subscription_id, resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name, pipeline_endpoint_id=pipeline_endpoint_id, body=request,
            headers=self._get_custom_headers())

        return result

    @track()
    def resubmit_pipeline_run(self, request, pipeline_run_id, node_composition_mode=None):
        """Resubmit a pipeline run by graph

        :param request: Resubmit request body, use ResubmitPipelineRunRequest as alias for readability.
        :type request: ~designer.models.SubmitPipelineRunRequest
        :param pipeline_run_id: Submitted pipeline run id.
        :type pipeline_run_id: str
        :param node_composition_mode: Valid values include: None, 'OnlySequential' and 'Full'.
        :type node_composition_mode: str
        :return: resubmitted pipeline run id
        :rtype: str
        """
        result = self._caller.pipeline_runs_v2.resubmit_pipeline_run(
            subscription_id=self._subscription_id,
            resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name,
            pipeline_run_id=pipeline_run_id,
            node_composition_mode=node_composition_mode,
            body=request,
            headers=self._get_custom_headers()
        )

        return result

    @track()
    def register_module(self, validate_only=False, module_source_type=None,
                        yaml_file=None, snapshot_source_zip_file=None, devops_artifacts_zip_url=None,
                        anonymous_registration=False, set_as_default=False, overwrite_module_version=None):
        """Register a module

        :param validate_only:
        :type validate_only: bool
        :param module_source_type:
        :type module_source_type: str
        :param yaml_file:
        :type yaml_file: str
        :param snapshot_source_zip_file:
        :type snapshot_source_zip_file: BinaryIO
        :param devops_artifacts_zip_url:
        :type devops_artifacts_zip_url: str
        :param anonymous_registration:
        :type anonymous_registration: bool
        :param set_as_default:
        :type set_as_default: bool
        :param overwrite_module_version:
        :type overwrite_module_version: str
        :return: ModuleDto
        :rtype: azure.ml.component._restclients.designer.models.ModuleDto
        :raises:
         :class:`HttpOperationError<msrest.exceptions.HttpOperationError>`
        """

        properties = json.dumps({
            'ModuleSourceType': module_source_type,
            'YamlFile': yaml_file,
            'DevopsArtifactsZipUrl': devops_artifacts_zip_url,
            'ModuleWorkingMechanism': self.DEFAULT_MODULE_WORKING_MECHANISM,
            'DataTypeMechanism': self.DEFAULT_DATATYPE_MECHANISM
        })

        result = self._caller.module.register_module(
            subscription_id=self._subscription_id,
            resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name,
            headers=self._get_custom_headers(),
            validate_only=validate_only,
            properties=properties,
            snapshot_source_zip_file=snapshot_source_zip_file,
            anonymous_registration=anonymous_registration,
            upgrade_if_exists=True,
            set_as_default_version=set_as_default,
            overwrite_module_version=overwrite_module_version,
            # We must set to False to make sure the module entity only include required parameters.
            # Note that this only affects **params in module entity** but doesn't affect run_setting_parameters.
            include_run_setting_params=False,
            # Yaml is needed for component definition construction.
            get_yaml=True
        )
        return result

    @track()
    def update_module(self, module_namespace, module_name, body):
        """Update a module.

        :param module_namespace:
        :type module_namespace: str
        :param module_name:
        :type module_name: str
        :return: ModuleDto or PipelineResponse if cls is a custom type or function that will be passed the direct
        response
        :rtype: ~designer.models.ModuleDto or
         ~msrest.pipeline.PipelineResponse
        """
        result = self._caller.module.update_module(
            subscription_id=self._subscription_id,
            resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name,
            headers=self._get_custom_headers(),
            module_namespace=module_namespace,
            module_name=module_name,
            body=body
        )
        return result

    @track()
    def disable_module(self, module_namespace, module_name, version=None):
        """Disables a module.

        :param module_namespace:
        :type module_namespace: str
        :param module_name:
        :type module_name: str
        :param version:
        :type version: str
        :return: ModuleDto or PipelineResponse if cls is a custom type or function that will be passed the direct
        response
        :rtype: ~designer.models.ModuleDto or
         ~msrest.pipeline.PipelineResponse
        """
        request = UpdateModuleRequest(
            module_update_operation_type='DisableModule',
            module_version=version)
        result = self.update_module(
            module_namespace=module_namespace,
            module_name=module_name,
            body=request)
        return result

    @track()
    def parse_module(self, module_source_type=None, yaml_file=None, devops_artifacts_zip_url=None,
                     snapshot_source_zip_file=None):
        """Parse a module.

        :param module_source_type:
        :type module_source_type: str
        :param yaml_file:
        :type yaml_file: str
        :param devops_artifacts_zip_url:
        :type devops_artifacts_zip_url: str
        :param snapshot_source_zip_file:
        :type snapshot_source_zip_file: BinaryIO
        :return: ModuleDto or PipelineResponse if cls is a custom type or function that will be passed the direct
        response
        :rtype: ~designer.models.ModuleDto or
         ~msrest.pipeline.PipelineResponse
        """
        properties = json.dumps({
            'ModuleSourceType': module_source_type,
            'YamlFile': yaml_file,
            'DevopsArtifactsZipUrl': devops_artifacts_zip_url,
            'ModuleWorkingMechanism': self.DEFAULT_MODULE_WORKING_MECHANISM,
        })
        result = self._caller.module.parse_module(
            subscription_id=self._subscription_id,
            resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name,
            headers=self._get_custom_headers(),
            snapshot_source_zip_file=snapshot_source_zip_file,
            properties=properties,
        )
        return result

    @track()
    @lru_cache(maxsize=1)
    def get_component_run_setting_parameters_mapping(self):
        # Cache run setting parameters in disk cache
        disk_cache = RunsettingParametersDiskCache()
        run_setting_parameters = disk_cache.get()
        if not run_setting_parameters:
            # When run setting parameters are not cached in disk. Send a remote call to get run setting parameters.
            run_setting_parameters = \
                self._caller.components_workspace_independent.get_component_run_setting_parameters_mapping(
                    headers=self._get_custom_headers(),
                    run_setting_type=ModuleRunSettingTypes.FULL
                )
            disk_cache.set(value=run_setting_parameters)
        return run_setting_parameters

    @track(_get_logger)
    def register_registry_component(self,
                                    validate_only=False,
                                    upgrade_if_exists=True,
                                    set_as_default_version=True,
                                    overwrite_component_version=None,
                                    registry_name=None,
                                    snapshot_id=None,
                                    module_source_type=None,
                                    yaml_file=None,
                                    snapshot_source_zip_file=None,
                                    devops_artifacts_zip_url=None,
                                    module_working_mechanism=DEFAULT_MODULE_WORKING_MECHANISM,
                                    is_private_repo=False,
                                    data_type_mechanism=DEFAULT_DATATYPE_MECHANISM,
                                    blob_file_info_data_store_name=None,
                                    blob_file_info_root_blob_uri=None,
                                    serialized_module_info=None,
                                    ):
        """

        :param validate_only:
        :type validate_only: bool
        :param upgrade_if_exists:
        :type upgrade_if_exists: bool
        :param set_as_default_version:
        :type set_as_default_version: bool
        :param overwrite_component_version:
        :type overwrite_component_version: str
        :param registry_name:
        :type registry_name: str
        :param snapshot_id:
        :type snapshot_id: str
        :param module_source_type: Possible values include: 'Unknown',
         'Local', 'GithubFile', 'GithubFolder', 'DevopsArtifactsZip',
         'SerializedModuleInfo'
        :type module_source_type: str or ~designer.models.ModuleSourceType
        :param yaml_file:
        :type yaml_file: str
        :param snapshot_source_zip_file:
        :type snapshot_source_zip_file: str
        :param devops_artifacts_zip_url:
        :type devops_artifacts_zip_url: str
        :param module_working_mechanism: Possible values include: 'Normal',
         'OutputToDataset'
        :type module_working_mechanism: str or
         ~designer.models.ModuleWorkingMechanism
        :param is_private_repo:
        :type is_private_repo: bool
        :param data_type_mechanism: Possible values include:
         'ErrorWhenNotExisting', 'RegisterWhenNotExisting',
         'RegisterBuildinDataTypeOnly'
        :type data_type_mechanism: str or ~designer.models.DataTypeMechanism
        :param blob_file_info_data_store_name:
        :type blob_file_info_data_store_name: str
        :param blob_file_info_root_blob_uri:
        :type blob_file_info_root_blob_uri: str
        :param serialized_module_info:
        :type serialized_module_info: str
        :return: None or PipelineResponse if cls is a custom type or function that will be passed the direct
        response
        :rtype: None or ~msrest.pipeline.PipelineResponse
        :raises:
         :class:`ErrorResponseException<designer.models.ErrorResponseException>`
        """
        properties = json.dumps({
            'RegistryName': registry_name,
            'SnapshotId': snapshot_id,
            'ModuleSourceType': module_source_type,
            'YamlFile': yaml_file,
            'DevopsArtifactsZipUrl': devops_artifacts_zip_url,
            'ModuleWorkingMechanism': module_working_mechanism,
            'IsPrivateRepo': is_private_repo,
            'DataTypeMechanism': data_type_mechanism,
            'BlobFileInfo.DataStoreName': blob_file_info_data_store_name,
            'BlobFileInfo.RootBlobUri': blob_file_info_root_blob_uri,
            'SerializedModuleInfo': serialized_module_info,

        })
        return self._caller.components_workspace_independent.register_registry_component(
            validate_only=validate_only,
            upgrade_if_exists=upgrade_if_exists,
            set_as_default_version=set_as_default_version,
            overwrite_component_version=overwrite_component_version,
            snapshot_source_zip_file=snapshot_source_zip_file,
            properties=properties,
            headers=self._get_custom_headers(),
            cls=PipelineResponse
        )

    @track(_get_logger)
    def list_registry_components(self,
                                 name=None,
                                 registry_names=None,
                                 active_only=True,
                                 continuation_header=None,
                                 run_setting_type=_run_setting_type,
                                 module_dto_fields=_module_dto_fields,
                                 ):
        """
        :param name:
        :type name: str
        :param registry_names:
        :type registry_names: list[str]
        :param continuation_header
        :type continuation_header: dict
        :param active_only:
        :type active_only: bool
        :param run_setting_type: Possible values include: 'Default', 'All',
         'Released', 'Testing', 'Legacy', 'Full'
        :type run_setting_type: str or ~designer.models.ModuleRunSettingTypes
        :param module_dto_fields: Possible values include: 'Definition',
         'YamlStr', 'RegistrationContext', 'Minimal', 'Basic',
         'RunSettingParameters', 'Default', 'RunDefinition', 'All'
        :type module_dto_fields: str or ~designer.models.ModuleDtoFields
        :return: PaginatedModuleDtoList or PipelineResponse if cls is a custom type or function that will be passed
        the direct response
        :rtype: ~designer.models.PaginatedModuleDtoList or
         ~msrest.pipeline.PipelineResponse
        :raises:
         :class:`ErrorResponseException<designer.models.ErrorResponseException>`
        """
        custom_headers = self._get_custom_headers()
        if continuation_header is not None:
            custom_headers.update(continuation_header)
        return self._caller.components_workspace_independent.list_registry_components(
            name=name,
            registry_names=registry_names,
            active_only=active_only,
            run_setting_type=run_setting_type,
            module_dto_fields=module_dto_fields,
            headers=custom_headers,
        )

    @track()
    def get_module_yaml(self, module_namespace, module_name, version):
        """Get module yaml.

        :param module_namespace:
        :type module_namespace: str
        :param module_name:
        :type module_name: str
        :param version:
        :type version: str
        """
        result = self._caller.module.get_module_yaml(
            subscription_id=self._subscription_id,
            resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name,
            headers=self._get_custom_headers(),
            module_namespace=module_namespace,
            module_name=module_name,
            version=version
        )
        return result

    @track()
    def get_module_snapshot_url(self, module_namespace, module_name, version):
        """Get module snapshot url.

        :param module_namespace:
        :type module_namespace: str
        :param module_name:
        :type module_name: str
        :param version:
        :type version: str
        """
        result = self._caller.module.get_module_snapshot_url(
            subscription_id=self._subscription_id,
            resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name,
            headers=self._get_custom_headers(),
            module_namespace=module_namespace,
            module_name=module_name,
            version=version
        )
        return result

    @track()
    def get_module_snapshot_url_by_id(self, module_id):
        """get module_snapshot_url by id

        :param module_id:
        :type module_id: str
        :return: str
        :rtype: str
        :raises:
         :class:`HttpOperationError<msrest.exceptions.HttpOperationError>`
        """

        result = self._caller.modules.get_module_snapshot_url_by_id(
            subscription_id=self._subscription_id,
            resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name,
            headers=self._get_custom_headers(),
            module_id=module_id
        )
        return result

    @track()
    def create_pipeline_draft(self, draft_name, draft_description, graph, tags=None, properties=None,
                              module_node_run_settings=None, sub_pipelines_info=None):
        """Create a new pipeline draft with given graph

        :param draft_name:
        :type draft_name: str
        :param draft_description:
        :type draft_description: str
        :param graph:
        :type graph: ~swagger.models.GraphDraftEntity
        :param tags: This is a dictionary
        :type tags: dict[str, str]
        :param properties: This is a dictionary
        :type properties: dict[str, str]
        :param module_node_run_settings: This is run settings for module nodes
        :type module_node_run_settings: List[~swagger.models.GraphModuleNodeRunSetting]
        :param sub_pipelines_info: sub pipelines info for the current graph
        :type sub_pipelines_info: ~swagger.models.SubPipelinesInfo
        :return: str
        :rtype: ~str
        :raises:
         :class:`HttpOperationError`
        """

        request = SavePipelineDraftRequest(
            name=draft_name,
            description=draft_description,
            graph=graph,
            pipeline_type=PipelineType.TRAINING_PIPELINE,  # hard code to Training pipeline
            pipeline_draft_mode=PipelineDraftMode.NORMAL,
            tags=tags,
            properties=properties,
            module_node_run_settings=module_node_run_settings,
            sub_pipelines_info=sub_pipelines_info
        )
        result = self._caller.pipeline_drafts_v2.create_pipeline_draft_extended(
            body=request,
            subscription_id=self._subscription_id,
            resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name,
            headers=self._get_custom_headers())

        return result

    @track()
    def save_pipeline_draft(self, draft_id, draft_name, draft_description, graph, tags=None,
                            module_node_run_settings=None, sub_pipelines_info=None):
        """Save pipeline draft

        :param draft_id:
        :type draft_id: str
        :param draft_name:
        :type draft_name: str
        :param draft_description:
        :type draft_description: str
        :param graph:
        :type graph: ~swagger.models.GraphDraftEntity
        :param tags: This is a dictionary
        :type tags: dict[str, str]
        :param module_node_run_settings: This is run settings for module nodes
        :type module_node_run_settings: List[~swagger.models.GraphModuleNodeRunSetting]
        :param sub_pipelines_info: sub pipelines info for the current graph
        :type sub_pipelines_info: ~swagger.models.SubPipelinesInfo
        """

        request = SavePipelineDraftRequest(
            name=draft_name,
            description=draft_description,
            graph=graph,
            tags=tags,
            module_node_run_settings=module_node_run_settings,
            sub_pipelines_info=sub_pipelines_info
        )
        result = self._caller.pipeline_drafts_v2.save_pipeline_draft(
            draft_id=draft_id,
            body=request,
            subscription_id=self._subscription_id,
            resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name,
            headers=self._get_custom_headers())

        return result

    @track()
    def get_pipeline_draft(self,
                           draft_id, get_status=True, include_run_setting_params=False, has_namespace_concept=True):
        """Get pipeline draft

        :param draft_id:
        :type draft_id: str
        :return: PipelineDraft
        :rtype: PipelineDraft
        :raises:
         :class:`HttpOperationError`
        """

        result = self._caller.pipeline_drafts_v2.get_pipeline_draft(
            draft_id=draft_id,
            get_status=get_status,
            include_run_setting_params=include_run_setting_params,
            has_namespace_concept=has_namespace_concept,
            subscription_id=self._subscription_id,
            resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name,
            headers=self._get_custom_headers())

        return PipelineDraft(
            raw_pipeline_draft=result,
            subscription_id=self._subscription_id,
            resource_group=self._resource_group_name,
            workspace_name=self._workspace_name)

    @track()
    def delete_pipeline_draft(self, draft_id):
        """Delete pipeline draft

        :param draft_id:
        :type draft_id: str
        :return: PipelineDraft
        :rtype: ~swagger.models.PipelineDraft
        :raises:
         :class:`HttpOperationError`
        """

        result = self._caller.pipeline_drafts_v2.delete_pipeline_draft(
            draft_id=draft_id,
            subscription_id=self._subscription_id,
            resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name,
            headers=self._get_custom_headers())

        return result

    @track()
    def publish_pipeline_run(self, request, pipeline_run_id):
        """
        Publish pipeline run by pipeline run id

        :param request:
        :type ~designer.models.CreatePublishedPipelineRequest
        :param pipeline_run_id: pipeline_run_id
        :type pipeline_run_id: str
        :return: str or PipelineResponse if cls is a custom type or function that will be passed the direct
        response
        :rtype: str or ~msrest.pipeline.PipelineResponse
        :raises:
         :class:`ErrorResponseException<designer.models.ErrorResponseException>`
        """
        result = self._caller.pipeline_runs_v2.publish_pipeline_run(
            body=request,
            pipeline_run_id=pipeline_run_id,
            subscription_id=self._subscription_id,
            resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name,
            headers=self._get_custom_headers()
        )

        return result

    @track()
    def publish_pipeline_graph(self, request):
        """
        Publish pipeline run by pipeline run id

        :param request:
        :type ~designer.models.CreatePublishedPipelineRequest
        :return: str or PipelineResponse if cls is a custom type or function that will be passed the direct
        response
        :rtype: str or ~msrest.pipeline.PipelineResponse
        :raises:
         :class:`ErrorResponseException<designer.models.ErrorResponseException>`
        """
        result = self._caller.published_pipelines_v2.publish_pipeline_graph(
            body=request,
            subscription_id=self._subscription_id,
            resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name,
            headers=self._get_custom_headers()
        )

        return result

    @track()
    def list_published_pipelines(self, active_only=True):
        """
        List all published pipelines in workspace

        :param active_only: If true, only return PipelineEndpoints which are currently active.
        :type active_only: bool
        :return: list[PublishedPipeline]
        :rtype: List[azure.ml.component._restclients.designer.modules.PublishedPipeline]
        :raises:
         :class:`ErrorResponseException<designer.models.ErrorResponseException>`
        """
        continuation_token = None
        results = []
        while True:
            paginated_results = self._caller.published_pipelines_v2.list_published_pipelines(
                subscription_id=self._subscription_id,
                resource_group_name=self._resource_group_name,
                workspace_name=self._workspace_name,
                headers=self._get_custom_headers(),
                continuation_token1=continuation_token,
                active_only=active_only
            )
            continuation_token, paginated_results = paginated_results._args[1](paginated_results._args[0]())
            results += paginated_results
            if continuation_token is None:
                break

        return results

    @track()
    def get_published_pipeline(self, pipeline_id):
        """
        Get published pipeline by pipeline id

        :param pipeline_id: pipeline_id
        :type pipeline_id: str
        :return: PublishedPipeline
        :rtype: azure.ml.component._restclients.designer.modules.PublishedPipeline
        :raises:
         :class:`ErrorResponseException<designer.models.ErrorResponseException>`
        """
        result = self._caller.published_pipelines_v2.get_published_pipeline(
            pipeline_id=pipeline_id,
            subscription_id=self._subscription_id,
            resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name,
            headers=self._get_custom_headers()
        )

        return result

    @track()
    def enable_published_pipeline(self, pipeline_id):
        """
        Enable published pipeline by pipeline id

        :param pipeline_id: pipeline_id
        :type pipeline_id: str
        :raises:
         :class:`ErrorResponseException<designer.models.ErrorResponseException>`
        """
        self._caller.published_pipelines_v2.enable_published_pipeline(
            pipeline_id=pipeline_id,
            subscription_id=self._subscription_id,
            resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name,
            headers=self._get_custom_headers()
        )

    @track()
    def disable_published_pipeline(self, pipeline_id):
        """
        Disable published pipeline by pipeline id

        :param pipeline_id: pipeline_id
        :type pipeline_id: str
        :raises:
         :class:`ErrorResponseException<designer.models.ErrorResponseException>`
        """
        self._caller.published_pipelines_v2.disable_published_pipeline(
            pipeline_id=pipeline_id,
            subscription_id=self._subscription_id,
            resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name,
            headers=self._get_custom_headers()
        )

    @track()
    def get_pipeline_endpoint(self, id=None, name=None):
        """
        Get pipeline endpoint by id or name.

        :param id: pipeline endpoint id
        :type id: str
        :param name: pipeline endpoint name
        :type name: str
        :return: PipelineEndpoint or PipelineResponse if cls is a custom type or function that will be passed the
        direct response
        :rtype: ~designer.models.PipelineEndpoint or
         ~msrest.pipeline.PipelineResponse
        :raises:
         :class:`ErrorResponseException<designer.models.ErrorResponseException>`
        """
        if id is not None:
            result = self._caller.pipeline_endpoints_v2.get_pipeline_endpoint(
                pipeline_endpoint_id=id,
                subscription_id=self._subscription_id,
                resource_group_name=self._resource_group_name,
                workspace_name=self._workspace_name,
                headers=self._get_custom_headers()
            )
            return result

        if name is not None:
            result = self._caller.pipeline_endpoints_v2.get_pipeline_endpoint_by_name(
                pipeline_endpoint_name=name,
                subscription_id=self._subscription_id,
                resource_group_name=self._resource_group_name,
                workspace_name=self._workspace_name,
                headers=self._get_custom_headers()
            )
            return result

        raise UserErrorException('Pipeline endpoint id or name must be provided to get PipelineEndpoint')

    @track()
    def get_pipeline_endpoint_pipelines(self, pipeline_endpoint_id):
        """Get pipeline endpoint all pipelines.

        :param pipeline_endpoint_id: pipeline endpoint id
        :rtype pipeline_endpoint_id:str
        :return: list[~designer.models.PublishedPipelineSummary]
        :rtype: list
        """
        continuation_token = None
        pipelines = []
        while True:
            paginated_pipelines = self._caller.pipeline_endpoints_v2.get_pipeline_endpoint_pipelines(
                pipeline_endpoint_id=pipeline_endpoint_id,
                subscription_id=self._subscription_id,
                resource_group_name=self._resource_group_name,
                workspace_name=self._workspace_name,
                headers=self._get_custom_headers(),
                continuation_token1=continuation_token
            )
            continuation_token, paginated_pipelines = paginated_pipelines._args[1](paginated_pipelines._args[0]())
            pipelines += paginated_pipelines
            if continuation_token is None:
                break

        return pipelines

    @track()
    def list_pipeline_endpoints(self, active_only=True):
        """
        Pipeline endpoints list

        :param active_only: If true, only return PipelineEndpoints which are currently active.
        :type active_only: bool
        :return: PaginatedPipelineEndpointSummaryList or PipelineResponse if
         cls is a custom type or function that will be passed the direct
        response
        :rtype: ~designer.models.PaginatedPipelineEndpointSummaryList or
         ~msrest.pipeline.PipelineResponse
        :raises:
         :class:`ErrorResponseException<designer.models.ErrorResponseException>`
        """
        continuation_token = None
        endpoints = []
        while True:
            paginated_endpoints = self._caller.pipeline_endpoints_v2.list_pipeline_endpoints(
                subscription_id=self._subscription_id,
                resource_group_name=self._resource_group_name,
                workspace_name=self._workspace_name,
                headers=self._get_custom_headers(),
                continuation_token1=continuation_token,
                active_only=active_only,
            )
            continuation_token, paginated_endpoints = paginated_endpoints._args[1](paginated_endpoints._args[0]())
            endpoints += paginated_endpoints
            if continuation_token is None:
                break

        return endpoints

    @track()
    def enable_pipeline_endpoint(self, endpoint_id):
        """
        Enable pipeline endpoint by pipeline endpoint id

        :param endpoint_id: pipeline endpoint id
        :type endpoint_id: str
        :raises:
         :class:`ErrorResponseException<designer.models.ErrorResponseException>`
        """
        self._caller.pipeline_endpoints_v2.enable_pipeline_endpoint(
            pipeline_endpoint_id=endpoint_id,
            subscription_id=self._subscription_id,
            resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name,
            headers=self._get_custom_headers()
        )

    @track()
    def disable_pipeline_endpoint(self, endpoint_id):
        """
        Disable pipeline endpoint by pipeline endpoint id

        :param endpoint_id: pipeline endpoint id
        :type endpoint_id: str
        :raises:
         :class:`ErrorResponseException<designer.models.ErrorResponseException>`
        """
        self._caller.pipeline_endpoints_v2.disable_pipeline_endpoint(
            pipeline_endpoint_id=endpoint_id,
            subscription_id=self._subscription_id,
            resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name,
            headers=self._get_custom_headers()
        )

    @track()
    def set_pipeline_endpoint_default_version(self, endpoint_id, version):
        """
        Set the default version of PipelineEndpoint, throws an exception if the specified version is not found.

        :param endpoint_id: pipeline endpoint id
        :type endpoint_id: str
        :param version: The version to set as the default version in PipelineEndpoint.
        :type version: str
        """
        self._caller.pipeline_endpoints_v2.set_default_pipeline(
            version=version,
            pipeline_endpoint_id=endpoint_id,
            subscription_id=self._subscription_id,
            resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name,
            headers=self._get_custom_headers()
        )

    @track()
    def get_pipeline_endpoint_graph(self, endpoint_id, has_namespace_concept=True):
        """
        Get pipeline endpoint graph.

        :param endpoint_id: pipeline endpoint id
        :type endpoint_id: str
        """
        return self._caller.pipeline_endpoints_v2.get_pipeline_endpoint_graph(
            pipeline_endpoint_id=endpoint_id,
            has_namespace_concept=has_namespace_concept,
            include_run_setting_params=False,
            subscription_id=self._subscription_id,
            resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name,
            headers=self._get_custom_headers()
        )

    @track()
    def list_pipeline_drafts(self, continuation_token=None):
        """List pipeline draft

        :param draft_id:
        :type draft_id: str
        :return: PipelineDraft
        :rtype: ~swagger.models.PipelineDraft
        :raises:
         :class:`ErrorResponseException`
        """

        result = self._caller.pipeline_drafts_v2.list_pipeline_drafts(
            subscription_id=self._subscription_id,
            resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name,
            continuation_token1=continuation_token,
            headers=self._get_custom_headers())

        return result

    @track()
    def list_samples(self):
        """List all of our samples
        """

        result = self._caller.samples.list_samples(
            subscription_id=self._subscription_id,
            resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name,
            headers=self._get_custom_headers(),
            cls=PipelineResponse)

        resp_body = json.loads(get_pipeline_response_content(result))
        sample_list = [{'name': sample['name'], 'id': sample['id']}
                       for sample in resp_body]

        return sample_list

    @track()
    def open_sample(self, sample_id):
        """Open sample by sample id
        """

        result = self._caller.samples.open_sample_and_get_draft(
            subscription_id=self._subscription_id,
            resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name,
            id=sample_id,
            headers=self._get_custom_headers()
        )

        return result

    @track()
    def list_datasets(self, data_category="0"):
        """List datasets by category

        :param data_category: Possible values include: 'All', 'Dataset',
         'Model'
        :type data_category: str
        :return: list
        :rtype: list[~designer.models.DataInfo]
        :raises:
         :class:`HttpOperationError<designer.models.HttpOperationError>`
        """

        result = self._caller.data_sets.list_data_sets(
            subscription_id=self._subscription_id,
            resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name,
            headers=self._get_custom_headers(),
            data_category=data_category
        )

        return result

    @track()
    def get_pipeline_run_graph(self, pipeline_run_id, experiment_name=None, experiment_id=None,
                               include_run_setting_params=False):
        """Get pipeline run graph

        :param pipeline_run_id:
        :type pipeline_run_id: str
        :param experiment_name:
        :type experiment_name: str
        :param experiment_id:
        :type experiment_id: str
        :param include_run_setting_params:
        :type include_run_setting_params: bool
        :return: PipelineRunGraphDetail
        :rtype: ~designer.models.PipelineRunGraphDetail
        :raises:
         :class:`HttpOperationError<designer.models.HttpOperationError>`
        """

        result = self._caller.pipeline_runs_v2.get_pipeline_run_graph(
            pipeline_run_id=pipeline_run_id,
            experiment_name=experiment_name,
            experiment_id=experiment_id,
            include_run_setting_params=include_run_setting_params,
            subscription_id=self._subscription_id,
            resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name,
            headers=self._get_custom_headers()
        )

        return result

    @track()
    def get_published_pipeline_graph(self, pipeline_id, include_run_setting_params=False, has_namespace_concept=True):
        """Get pipeline run graph

        :param pipeline_id:
        :type pipeline_id: str
        :param include_run_setting_params:
        :type include_run_setting_params: bool
        :return: PipelineGraph or PipelineResponse if cls is a custom type or function that will be passed the direct
        response
        :rtype: ~designer.models.PipelineGraph or
         ~msrest.pipeline.PipelineResponse
        :raises:
         :class:`ErrorResponseException<designer.models.ErrorResponseException>`
        """

        result = self._caller.published_pipelines_v2.get_published_pipeline_graph(
            pipeline_id=pipeline_id,
            include_run_setting_params=include_run_setting_params,
            has_namespace_concept=has_namespace_concept,
            subscription_id=self._subscription_id,
            resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name,
            headers=self._get_custom_headers()
        )

        return result

    @track()
    def get_pipeline_run_graph_no_status(self, pipeline_run_id,
                                         include_run_setting_params=False,
                                         has_namespace_concept=True,
                                         skip_dataset_load=False,
                                         referenced_node_id=None,
                                         cls=None,
                                         enum_to_str=True):
        """Get pipeline run graph no status

        :param pipeline_run_id:
        :type pipeline_run_id: str
        :param include_run_setting_params:
        :type include_run_setting_params: bool
        :param has_namespace_concept:
        :type has_namespace_concept: bool
        :param skip_dataset_load:
        :type skip_dataset_load: bool
        :param referenced_node_id:
        :type referenced_node_id: str
        :param cls:
        :type cls: a custom type or function that will be passed the direct response
        :param enum_to_str:
        :type enum_to_str: bool
        :return: PipelineRunGraphDetail
        :rtype: ~designer.models.PipelineRunGraphDetail
        :raises:
         :class:`HttpOperationError<designer.models.HttpOperationError>`
        """

        result = self._caller.pipeline_runs_v2.get_pipeline_run_graph_no_status(
            pipeline_run_id=pipeline_run_id,
            include_run_setting_params=include_run_setting_params,
            has_namespace_concept=has_namespace_concept,
            skip_dataset_load=skip_dataset_load,
            referenced_node_id=referenced_node_id,
            subscription_id=self._subscription_id,
            resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name,
            headers=self._get_custom_headers(enum_to_str=enum_to_str),
            cls=cls
        )

        return result

    @track()
    def get_pipeline_draft_sdk_code(self, draft_id, target_code):
        """Export pipeline draft to sdk code

        :param draft_id: the draft to export
        :type draft_id: str
        :param target_code: specify the exported code type: Python or JupyterNotebook
        :type target_code: str
        :return: str or PipelineResponse if cls is a custom type or function that will be passed the direct
        response
        :rtype: str or ~msrest.pipeline.PipelineResponse
        :raises:
        :class:`HttpOperationError<designer.models.HttpOperationError>`
        """
        result = self._caller.pipeline_drafts_v2.get_pipeline_draft_sdk_code(
            subscription_id=self._subscription_id,
            resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name,
            draft_id=draft_id,
            target_code=target_code,
            cls=PipelineResponse,
            headers=self._get_custom_headers()
        )

        return result.http_request.http_response.internal_response

    @track()
    def get_pipeline_run_sdk_code(self, pipeline_run_id, target_code, experiment_name, experiment_id):
        """Export pipeline run to sdk code

        :param pipeline_run_id: the pipeline run to export
        :type pipeline_run_id: str
        :param target_code: specify the exported code type: Python or JupyterNotebook
        :type target_code: str
        :param experiment_name: the experiment that contains the run
        :type experiment_name: str
        :param experiment_id: the experiment that contains the run
        :type experiment_id: str
        :return: str or PipelineResponse if cls is a custom type or function that will be passed the direct
        response
        :rtype: str or ~msrest.pipeline.PipelineResponse
        :raises:
        :class:`HttpOperationError<designer.models.HttpOperationError>`
        """
        result = self._caller.pipeline_runs_v2.get_pipeline_run_sdk_code(
            subscription_id=self._subscription_id,
            resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name,
            pipeline_run_id=pipeline_run_id,
            target_code=target_code,
            experiment_name=experiment_name,
            experiment_id=experiment_id,
            cls=PipelineResponse,
            headers=self._get_custom_headers()
        )

        return result.http_request.http_response.internal_response

    @track()
    def get_pipeline_run_status(
            self, pipeline_run_id, experiment_name=None, experiment_id=None, cls=None, enum_to_str=True):
        """Get pipeline run status

        :param pipeline_run_id:
        :type pipeline_run_id: str
        :param experiment_name:
        :type experiment_name: str
        :param experiment_id:
        :type experiment_id: str
        :param cls:
        :type cls: is a custom type or function that will be passed the direct
        response
        :param enum_to_str:
        :type enum_to_str: bool
        :return: PipelineRunGraphStatus
        :rtype: ~designer.models.PipelineRunGraphStatus
        :raises:
         :class:`HttpOperationError<designer.models.HttpOperationError>`
        """

        result = self._caller.pipeline_runs_v2.get_pipeline_run_status(
            pipeline_run_id=pipeline_run_id,
            experiment_name=experiment_name,
            experiment_id=experiment_id,
            subscription_id=self._subscription_id,
            resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name,
            headers=self._get_custom_headers(enum_to_str=enum_to_str),
            cls=cls
        )

        return result

    @track()
    def get_module_versions(self, module_namespace, module_name):
        """Get module dtos

        :param module_namespace:
        :type module_namespace: str
        :param module_name:
        :type module_name: str
        :return: dict
        :rtype: dict[str, azure.ml.component._module_dto.ModuleDto]
        :raises:
         :class:`HttpOperationError<designer.models.HttpOperationError>`
        """

        result = self._caller.module.get_module_versions(
            module_namespace=module_namespace,
            module_name=module_name,
            subscription_id=self._subscription_id,
            resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name,
            headers=self._get_custom_headers()
        )

        return result

    @track()
    def list_modules(self, module_scope=ModuleScope.WORKSPACE, active_only=True, continuation_header=None):
        """
        List modules.

        :param module_scope: Possible values include: 'All', 'Global',
         'Workspace', 'Anonymous', 'Step'
        :param active_only:
        :type active_only: bool
        :param continuation_header
        :type continuation_header: dict
        :return: PaginatedModuleDtoList or PipelineResponse if cls is a custom type or function that will be passed
        the direct response
        :rtype: ~designer.models.PaginatedModuleDtoList or
         ~msrest.pipeline.PipelineResponse
        :raises:
         :class:`HttpOperationError<designer.models.HttpOperationError>`
        """
        custom_headers = self._get_custom_headers()
        if continuation_header is not None:
            custom_headers.update(continuation_header)
        result = self._caller.module.list_modules(
            subscription_id=self._subscription_id,
            resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name,
            headers=custom_headers,
            active_only=active_only,
            module_scope=module_scope,
            include_run_setting_params=False,
        )
        return result

    @track()
    def batch_get_modules(self, module_version_ids, name_identifiers, include_run_setting_params=False):
        """Get modules dto

        :param module_version_ids:
        :type module_version_ids: list
        :param name_identifiers:
        :type name_identifiers: list
        :return: modules_by_id concat modules_by_identifier
        :rtype: List[azure.ml.component._restclients.designer.models.ModuleDto]
        :raises:
         :class:`HttpOperationError<designer.models.HttpOperationError>`
        """
        module_version_ids, name_identifiers = \
            _refine_batch_load_input(module_version_ids, name_identifiers, self._workspace_name)
        modules = []

        aml_modules = \
            [AmlModuleNameMetaInfo(
                module_name=name,
                module_namespace=namespace,
                module_version=version) for name, namespace, version in name_identifiers]
        request = BatchGetModuleRequest(
            module_version_ids=module_version_ids,
            aml_modules=aml_modules
        )
        result = \
            _eat_exception_trace("Batch load modules",
                                 self._caller.modules.batch_get_modules,
                                 body=request,
                                 include_run_setting_params=include_run_setting_params,
                                 subscription_id=self._subscription_id,
                                 resource_group_name=self._resource_group_name,
                                 workspace_name=self._workspace_name,
                                 get_yaml=True,
                                 headers=self._get_custom_headers())

        modules += result
        # Re-ordered here
        modules, failed_ids, failed_identifiers = \
            _refine_batch_load_output(modules, module_version_ids, name_identifiers, self._workspace_name)
        if len(failed_ids) > 0 or len(failed_identifiers) > 0:
            raise UserErrorException("Batch load failed, failed module_version_ids: {0}, failed identifiers: {1}".
                                     format(failed_ids, failed_identifiers))
        return modules

    @track()
    def get_module(self, module_namespace, module_name, version=None, include_run_setting_params=False,
                   get_yaml=True):
        """Get module dto

        :param module_namespace:
        :type module_namespace: str
        :param module_name:
        :type module_name: str
        :param version:
        :type version: str
        :param include_run_setting_params:
        :type include_run_setting_params: bool
        :param get_yaml:
        :type get_yaml: bool
        :return: ModuleDto
        :rtype: azure.ml.component._module_dto.ModuleDto
        :raises:
         :class:`HttpOperationError<designer.models.HttpOperationError>`
        """
        # Set the default placeholder of module namespace when it is None.
        module_namespace = module_namespace if module_namespace else self.DEFAULT_COMPONENT_NAMESPACE_PLACEHOLDER
        result = self._caller.module.get_module(
            module_namespace=module_namespace,
            module_name=module_name,
            version=version,
            get_yaml=get_yaml,
            include_run_setting_params=include_run_setting_params,
            subscription_id=self._subscription_id,
            resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name,
            headers=self._get_custom_headers()
        )

        return result

    @track()
    def get_module_by_id(self, module_id, include_run_setting_params=False, get_yaml=True):
        """Get module dto by module id
        """

        result = self._caller.modules.get_module_dto_by_id(
            module_id=module_id,
            include_run_setting_params=include_run_setting_params,
            subscription_id=self._subscription_id,
            get_yaml=get_yaml,
            resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name,
            headers=self._get_custom_headers()
        )

        return result

    @track()
    def get_module_yaml_by_id(self, module_id):
        """Get module yaml by module id
        """

        result = self._caller.modules.get_module_yaml_by_id(
            module_id=module_id,
            subscription_id=self._subscription_id,
            resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name,
            headers=self._get_custom_headers(),
        )

        return result

    @track()
    def get_pipeline_run_step_details(self, pipeline_run_id, run_id, include_snaptshot=False):
        """Get pipeline step run details

        :param pipeline_run_id:
        :type pipeline_run_id: str
        :param run_id:
        :type run_id: str
        :param include_snaptshot:
        :type include_snaptshot: bool
        :param dict custom_headers: headers that will be added to the request
        :param callable cls: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: PipelineRunStepDetails or PipelineResponse if cls is a custom type or function that will be passed
        the direct response
        :rtype: ~designer.models.PipelineRunStepDetails or
         ~msrest.pipeline.PipelineResponse
        :raises:
         :class:`HttpOperationError<designer.models.HttpOperationError>`
        """

        result = self._caller.pipeline_runs_v2.get_pipeline_run_step_details(
            pipeline_run_id=pipeline_run_id,
            run_id=run_id,
            include_snaptshot=include_snaptshot,
            subscription_id=self._subscription_id,
            resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name,
            headers=self._get_custom_headers()
        )

        return result

    @track()
    def get_pipeline_run(self, pipeline_run_id, cls=None):
        """

        :param pipeline_run_id:
        :type pipeline_run_id: str
        :param cls
        :type cls: is a custom type or function that will be passed the direct response
        :return: PipelineRun
        :rtype: ~designer.models.PipelineRun or
         ~msrest.pipeline.PipelineResponse
        :raises:
         :class:`ErrorResponseException<designer.models.ErrorResponseException>`
        """

        result = self._caller.pipeline_runs_v2.get_pipeline_run(
            pipeline_run_id=pipeline_run_id,
            subscription_id=self._subscription_id,
            resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name,
            headers=self._get_custom_headers(enum_to_str=True),
            cls=cls
        )

        return result

    @track()
    def get_pipeline_run_step_outputs(self, pipeline_run_id, module_node_id, run_id):
        """Get outputs of a step run.

        :param pipeline_run_id:
        :type pipeline_run_id: str
        :param module_node_id:
        :type module_node_id: str
        :param run_id:
        :type run_id: str
        :return: PipelineStepRunOutputs
        :rtype: ~designer.models.PipelineStepRunOutputs
        :raises:
         :class:`ErrorResponseException<designer.models.ErrorResponseException>`
        """

        result = self._caller.pipeline_runs_v2.get_pipeline_run_step_outputs(
            pipeline_run_id=pipeline_run_id,
            module_node_id=module_node_id,
            run_id=run_id,
            subscription_id=self._subscription_id,
            resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name,
            headers=self._get_custom_headers()
        )

        return result

    @track()
    def get_pipeline_run_profile(self, pipeline_run_id, cls=PipelineResponse):
        """

        :param pipeline_run_id:
        :type pipeline_run_id: str
        :param cls
        :type cls: callable
        :return: PipelineRunProfile
        :rtype: ~designer.models.PipelineRunProfile or
         ~msrest.pipeline.PipelineResponse
        :raises:
         :class:`ErrorResponseException<designer.models.ErrorResponseException>`
        """

        result = self._caller.pipeline_runs_v2.get_pipeline_run_profile(
            pipeline_run_id=pipeline_run_id,
            subscription_id=self._subscription_id,
            resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name,
            headers=self._get_custom_headers(),
            cls=cls
        )

        return result

    @track()
    def get_all_layer_child_runs(self, root_run_id, cls=None):
        """

        :param root_run_id:
        :type root_run_id: str
        :param cls
        :type cls: callable
        :return: list or PipelineResponse if cls is a custom type or function that will be passed the direct
        response
        :rtype: list[~designer.models.RunIndexEntity] or
         ~msrest.pipeline.PipelineResponse
        :raises:
         :class:`ErrorResponseException<designer.models.ErrorResponseException>`
        """

        result = self._caller.pipeline_runs_v2.get_all_layer_child_runs(
            run_id=root_run_id,
            subscription_id=self._subscription_id,
            resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name,
            headers=self._get_custom_headers(enum_to_str=True),
            cls=cls
        )

        return result

    @track()
    def list_experiment_computes(self, include_test_types=False):
        """

        :type include_test_types: bool
        :param dict custom_headers: headers that will be added to the request
        :return: dict
        :rtype: dict[str, ~designer.models.ExperimentComputeMetaInfo]
        :raises:
         :class:`ErrorResponseException<designer.models.ErrorResponseException>`
        """

        result = self._caller.computes.list_experiment_computes(
            include_test_types=include_test_types,
            subscription_id=self._subscription_id,
            resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name,
            # since MT is directly calling compute rp, so we need to path original auth header here
            headers=self._get_custom_headers(use_arm_token=True)
        )
        computes_dict = {c.name: c for c in result}
        return computes_dict

    def cache_all_computes_in_workspace(self):
        computes_dict = self.list_experiment_computes(include_test_types=True)
        for compute_name, compute in computes_dict.items():
            ComputeTargetCache.set_item(self._workspace, compute, compute_name)

    # do not track this cached call as it will be called frequently
    # @track()
    def get_compute_by_name(self, compute_name: str):
        """Get compute by name. Return None if compute does not exist in current workspace.

        :param compute_name
        :type str
        :return: compute
        :rtype: ~designer.models.ExperimentComputeMetaInfo
        :raises:
         :class:`ErrorResponseException<designer.models.ErrorResponseException>`
        """

        if compute_name is None:
            return None
        compute_cache = ComputeTargetCache.get_item(self._workspace, compute_name)
        # Get this single compute from backend, if it's not in cache or expired for not-found cache result.
        if compute_cache is None:
            # Update cache
            compute = self._get_compute_from_workspace_by_name(compute_name)
            ComputeTargetCache.set_item(self._workspace, compute, compute_name)
            return compute
        return compute_cache.item

    @track()
    def _get_compute_from_workspace_by_name(self, compute_name):
        """Return instance of ExperimentComputeMetaInfo, or None if compute doesn't exist."""

        object_dict = ComputeTarget._get(self._workspace, compute_name)
        if object_dict is None:
            return None
        compute_type = object_dict.get('properties').get('computeType')
        return ExperimentComputeMetaInfo(name=compute_name, compute_type=compute_type)

    @track()
    def _get_default_datastore(self):
        return self._workspace.get_default_datastore()

    # do not track this cached call as it will be called frequently
    # @track()
    def get_default_datastore(self):
        if self._default_datastore is None:
            self._default_datastore = self._get_default_datastore()
        return self._default_datastore

    # region Component APIs
    @track()
    def register_component(self, validate_only=False, anonymous_registration=False, upgrade_if_exists=False,
                           set_as_default_version=True, include_run_setting_params=False,
                           overwrite_component_version=None, module_source_type=None, yaml_file=None,
                           snapshot_source_zip_file=None, devops_artifacts_zip_url=None, is_private_repo=None,
                           snapshot_id=None):
        """Register a component

        :param validate_only:
        :type validate_only: bool
        :param anonymous_registration:
        :type anonymous_registration: bool
        :param upgrade_if_exists:
        :type upgrade_if_exists: bool
        :param set_as_default_version:
        :type set_as_default_version: bool
        :param include_run_setting_params:
        :type include_run_setting_params: bool
        :param overwrite_component_version:
        :type overwrite_component_version: str
        :param module_source_type: Possible values include: 'Unknown',
         'Local', 'GithubFile', 'GithubFolder', 'DevopsArtifactsZip'
        :type module_source_type: str or ~designer.models.ModuleSourceType
        :param yaml_file:
        :type yaml_file: str
        :param snapshot_source_zip_file:
        :type snapshot_source_zip_file: str
        :param devops_artifacts_zip_url:
        :type devops_artifacts_zip_url: str
        :param is_private_repo:
        :type is_private_repo: bool
        :param snapshot_id:
        :type snapshot_id: str
        :return: ModuleDto
        :rtype: azure.ml.component._restclients.designer.models.ModuleDto
        :raises:
         :class:`HttpOperationError<msrest.exceptions.HttpOperationError>`
        """

        properties = json.dumps({
            'ModuleSourceType': module_source_type,
            'YamlFile': yaml_file,
            'DevopsArtifactsZipUrl': devops_artifacts_zip_url,
            'ModuleWorkingMechanism': self.DEFAULT_MODULE_WORKING_MECHANISM,
            'DataTypeMechanism': self.DEFAULT_DATATYPE_MECHANISM,
            'SnapshotId': snapshot_id,
        })
        registered_component = None
        disk_cache = RegisteredComponentDiskCache.get_disk_cache()
        if disk_cache and anonymous_registration and not validate_only:
            # Get the module dto of registered anonymous component in disk cache.
            registered_component_keys = {
                "subscription_id": self._subscription_id,
                "resource_group_name": self._resource_group_name,
                "workspace_name": self._workspace_name,
                "properties": properties,
            }
            disk_cache = RegisteredComponentDiskCache()
            registered_component = disk_cache.get(registered_component_keys, default=None)
        if not registered_component:
            registered_component = self._caller.component.register_component(
                subscription_id=self._subscription_id,
                resource_group_name=self._resource_group_name,
                workspace_name=self._workspace_name,
                headers=self._get_custom_headers(),
                validate_only=validate_only,
                properties=properties,
                snapshot_source_zip_file=snapshot_source_zip_file,
                anonymous_registration=anonymous_registration,
                upgrade_if_exists=True,
                set_as_default_version=set_as_default_version,
                overwrite_component_version=overwrite_component_version,
                # We must set to False to make sure the module entity only include required parameters.
                # Note that this only affects **params in module entity** but doesn't affect run_setting_parameters.
                include_run_setting_params=False,
                # Yaml is needed for component definition construction.
                get_yaml=True,
                run_setting_type=_run_setting_type
            )
            if disk_cache and anonymous_registration and not validate_only:
                # Cache the anonymous component
                disk_cache.set(registered_component_keys, registered_component)
        return registered_component

    @track()
    def update_component(self, component_name, body):
        """Update a component.

        :param component_name:
        :type component_name: str
        :param body:
        :type body: ~designer.models.UpdateModuleRequest
        :return: ModuleDto or PipelineResponse if cls is a custom type or function that will be passed the direct
        response
        :rtype: ~designer.models.ModuleDto or
         ~msrest.pipeline.PipelineResponse
        """
        result = self._caller.component.update_component(
            subscription_id=self._subscription_id,
            resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name,
            headers=self._get_custom_headers(),
            component_name=component_name,
            body=body,
            run_setting_type=_run_setting_type
        )
        return result

    @track()
    def disable_component(self, component_name, version=None):
        """Disables a component.

        :param component_name:
        :type component_name: str
        :param version:
        :type version: str
        :return: ModuleDto or PipelineResponse if cls is a custom type or function that will be passed the direct
        response
        :rtype: ~designer.models.ModuleDto or
         ~msrest.pipeline.PipelineResponse
        """
        request = UpdateModuleRequest(
            module_update_operation_type='DisableModule',
            module_version=version)
        result = self.update_component(
            component_name=component_name,
            body=request)
        return result

    @track()
    def parse_component(self, module_source_type=None,
                        yaml_file=None, snapshot_source_zip_file=None, devops_artifacts_zip_url=None,
                        module_working_mechanism=None, is_private_repo=None, data_type_mechanism=None):
        """Parse a component.

        :param module_source_type:
        :type module_source_type: str
        :param yaml_file:
        :type yaml_file: str
        :param devops_artifacts_zip_url:
        :type devops_artifacts_zip_url: str
        :param snapshot_source_zip_file:
        :type snapshot_source_zip_file: BinaryIO
        :return: ModuleDto
        :rtype: ~designer.models.ModuleDto
        """
        properties = json.dumps({
            'ModuleSourceType': module_source_type,
            'YamlFile': yaml_file,
            'DevopsArtifactsZipUrl': devops_artifacts_zip_url,
            'ModuleWorkingMechanism': self.DEFAULT_MODULE_WORKING_MECHANISM,
            'DataTypeMechanism': self.DEFAULT_DATATYPE_MECHANISM,
        })
        result = self._caller.component.parse_component(
            subscription_id=self._subscription_id,
            resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name,
            headers=self._get_custom_headers(),
            snapshot_source_zip_file=snapshot_source_zip_file,
            properties=properties,
            run_setting_type=_run_setting_type
        )
        return result

    @track(_get_logger)
    def get_component_yaml(self, component_name, version, feed_name=None, registry_name=None):
        """Get component yaml.

        :param component_name:
        :type component_name: str
        :param version:
        :type version: str
        :param feed_name:
        :type feed_name: str
        :param registry_name:
        :type registry_name:str
        """
        result = self._caller.component.get_component_yaml(
            subscription_id=self._subscription_id,
            resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name,
            headers=self._get_custom_headers(),
            component_name=component_name,
            version=version,
            feed_name=feed_name,
            registry_name=registry_name
        )
        return result

    @track()
    def get_component_snapshot_url(self, component_name, version):
        """Get component snapshot url.

        :param component_name:
        :type component_name: str
        :param version:
        :type version: str
        """
        result = self._caller.component.get_component_snapshot_url(
            subscription_id=self._subscription_id,
            resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name,
            headers=self._get_custom_headers(),
            component_name=component_name,
            version=version
        )
        return result

    @track()
    def get_component_versions(self, component_name):
        """Get component dtos

        :param component_name:
        :type component_name: str
        :return: dict
        :rtype: dict[str, azure.ml.component._module_dto.ModuleDto]
        :raises:
         :class:`HttpOperationError<designer.models.HttpOperationError>`
        """

        result = self._caller.component.get_component_versions(
            component_name=component_name,
            subscription_id=self._subscription_id,
            resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name,
            headers=self._get_custom_headers(),
            include_run_setting_params=False,
            run_setting_type=_run_setting_type
        )

        return result

    @track()
    def list_components(self, module_scope=ModuleScope.workspace, active_only=True, continuation_header=None,
                        feed_names=None, module_dto_fields=_module_dto_fields):
        """
        List components.

        :param module_scope: Possible values include: 'All', 'Global',
         'Workspace', 'Anonymous', 'Step', 'Draft', 'Feed'
        :param active_only:
        :type active_only: bool
        :param continuation_header
        :type continuation_header: dict
        :param feed_names
        :type feed_names: list[str]
        :param module_dto_fields: Possible values include: 'Definition',
         'YamlStr', 'RegistrationContext', 'Minimal', 'Basic',
         'RunSettingParameters', 'Default', 'RunDefinition', 'All'
        :type module_dto_fields: str or ~designer.models.ModuleDtoFields
        :return: PaginatedModuleDtoList or PipelineResponse if cls is a custom type or function that will be passed
        the direct response
        :rtype: ~designer.models.PaginatedModuleDtoList or
         ~msrest.pipeline.PipelineResponse
        :raises:
         :class:`HttpOperationError<designer.models.HttpOperationError>`
        """
        custom_headers = self._get_custom_headers()
        if continuation_header is not None:
            custom_headers.update(continuation_header)
        result = self._caller.component.list_components(
            subscription_id=self._subscription_id,
            resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name,
            headers=custom_headers,
            active_only=active_only,
            module_scope=module_scope,
            include_run_setting_params=False,
            run_setting_type=_run_setting_type,
            feed_names=feed_names,
            module_dto_fields=module_dto_fields
        )
        return result

    @track(_get_logger)
    def get_component(self, component_name, version=None, feed_name=None, registry_name=None,
                      include_run_setting_params=False, get_yaml=True):
        """Get component dto

        :param component_name:
        :type component_name: str
        :param version:
        :type version: str
        :param feed_name:
        :type feed_name: str
        :param registry_name:
        :type registry_name: str
        :param include_run_setting_params:
        :type include_run_setting_params: bool
        :param get_yaml:
        :type get_yaml: bool
        :return: ModuleDto
        :rtype: azure.ml.component._module_dto.ModuleDto
        :raises:
         :class:`HttpOperationError<designer.models.HttpOperationError>`
        """

        result = self._caller.component.get_component(
            component_name=component_name,
            version=version,
            get_yaml=get_yaml,
            include_run_setting_params=include_run_setting_params,
            subscription_id=self._subscription_id,
            resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name,
            feed_name=feed_name,
            registry_name=registry_name,
            headers=self._get_custom_headers(),
            run_setting_type=_run_setting_type
        )

        return result

    @track(_get_logger)
    def get_registry_component(self, component_name, version, registry_name, get_yaml=True):
        asset_id = f"azureml://registries/{registry_name}/components/{component_name}"
        if version:
            asset_id = asset_id + f"/versions/{version}"
        result = self._caller.components_workspace_independent.get_component_by_asset_id(
            asset_id=asset_id,
            get_yaml=get_yaml,
            run_setting_type=_run_setting_type,
            headers=self._get_custom_headers())

        return result

    @track()
    def get_component_by_id(self, component_id, include_run_setting_params=False, get_yaml=True):
        """Get module dto by module id
        """

        result = self._caller.component.get_component_by_id(
            component_id=component_id,
            include_run_setting_params=include_run_setting_params,
            subscription_id=self._subscription_id,
            get_yaml=get_yaml,
            resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name,
            headers=self._get_custom_headers(),
            run_setting_type=_run_setting_type
        )

        return result

    @track()
    def batch_get_components(self, version_ids, name_identifiers, include_run_setting_params=False):
        """Get modules dto

        :param version_ids:
        :type version_ids: list
        :param name_identifiers:
        :type name_identifiers: list
        :return: modules_by_id concat modules_by_identifier
        :rtype: List[azure.ml.component._restclients.designer.models.ModuleDto]
        :raises:
         :class:`HttpOperationError<designer.models.HttpOperationError>`
        """
        version_ids, name_identifiers = \
            _refine_batch_load_input_component(version_ids, name_identifiers)
        components = []

        name_and_versions = \
            [ComponentNameMetaInfo(
                component_name=name,
                component_version=version) for name, version in name_identifiers]
        request = BatchGetComponentRequest(
            version_ids=version_ids,
            name_and_versions=name_and_versions
        )
        result = \
            _eat_exception_trace("Batch load components",
                                 self._caller.component.batch_get_components,
                                 body=request,
                                 include_run_setting_params=include_run_setting_params,
                                 subscription_id=self._subscription_id,
                                 resource_group_name=self._resource_group_name,
                                 workspace_name=self._workspace_name,
                                 get_yaml=True,
                                 headers=self._get_custom_headers(),
                                 run_setting_type=_run_setting_type)

        components += result
        # Re-ordered here
        components, failed_ids, failed_identifiers = \
            _refine_batch_load_output_component(components, version_ids, name_identifiers)
        if len(failed_ids) > 0 or len(failed_identifiers) > 0:
            raise UserErrorException("Batch load failed, failed version_ids: {0}, failed identifiers: {1}".
                                     format(failed_ids, failed_identifiers))
        return components
    # endregion

    # region Pipeline Component APIs
    @track()
    def register_pipeline_component(self, validate_only=False, overwrite_component_version=None, body=None):
        """Register a pipeline component

        :param validate_only:
        :type validate_only: bool
        :param upgrade_if_exists:
        :type upgrade_if_exists: bool
        :param include_run_setting_params:
        :type include_run_setting_params: bool
        :param overwrite_component_version:
        :type overwrite_component_version: str
        :param get_yaml:
        :type get_yaml: bool
        :param remove_client_not_used_fields:
        :type remove_client_not_used_fields: bool
        :param keep_complete_parameters:
        :type keep_complete_parameters: bool
        :param run_setting_type: Possible values include: 'Default', 'All',
         'Released', 'Testing', 'Legacy', 'Full'
        :type run_setting_type: str or ~designer.models.ModuleRunSettingTypes
        :param body:
        :type body: ~designer.models.GeneratePipelineComponentRequest
        :return: ModuleDto
        :rtype: ~designer.models.ModuleDto
        :raises:
         :class:`ErrorResponseException<designer.models.ErrorResponseException>`
        """
        registered_pipeline_component = None
        is_anoymous_creation = body.module_scope == ModuleScope.ANONYMOUS
        disk_cache = RegisteredPipelineComponentDiskCache.get_disk_cache()
        if is_anoymous_creation and disk_cache:
            registered_pipeline_component = disk_cache.get(workspace=self._workspace,
                                                           generate_request=body, default=None)
        if not registered_pipeline_component:
            registered_pipeline_component = self._caller.pipeline_component.register_component(
                subscription_id=self._subscription_id,
                resource_group_name=self._resource_group_name,
                workspace_name=self._workspace_name,
                validate_only=validate_only,
                upgrade_if_exists=True,
                include_run_setting_params=False,
                overwrite_component_version=overwrite_component_version,
                # Set to false
                get_yaml=False,
                remove_client_not_used_fields=True,
                keep_complete_parameters=False,
                run_setting_type=_run_setting_type,
                body=body,
                headers=self._get_custom_headers()
            )
            if is_anoymous_creation and disk_cache:
                disk_cache.set(workspace=self._workspace, generate_request=body, value=registered_pipeline_component)
        return registered_pipeline_component

    @track()
    def _get_pipeline_component_graph(self, graph_id, fetch_nested_graphs=False, skip_dataset_load=True,
                                      referenced_node_id=None, cls=None, enum_to_str=True):
        """Get the graph of a pipeline component.

        :param graph_id: pipeline component's graph id
        :type graph_id: str
        :param fetch_nested_graphs:
        :type fetch_nested_graphs: bool
        :param skip_dataset_load:
        :type skip_dataset_load: bool
        :param referenced_node_id
        :type referenced_node_id: str
        :param cls:
        :type cls: callable
        :param enum_to_str: indicates whether to add x-ms-jsonformat-enum-to-string header
        :type enum_to_str: bool
        :rtype: ~designer.models.PipelineGraph
        :raises:
         :class:`ErrorResponseException<designer.models.ErrorResponseException>`
        """
        return self._caller.pipeline_component.get_pipeline_component_graph(
            subscription_id=self._subscription_id,
            resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name,
            graph_id=graph_id,
            fetch_nested_graphs=fetch_nested_graphs,
            skip_dataset_load=skip_dataset_load,
            referenced_node_id=referenced_node_id,
            headers=self._get_custom_headers(enum_to_str=enum_to_str),
            cls=cls
        )
    # endregion

    # region datasets api
    @track()
    def _get_data_set_by_name(self, dataset_name, version_id=None, feed_name=None):
        return self._caller.data_sets_v2.get_dataset_by_name(
            subscription_id=self._subscription_id,
            resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name,
            dataset_name=dataset_name,
            version_id=version_id,
            feed_name=feed_name,
            headers=self._get_custom_headers(),
            cls=None
        )

    @track()
    def _list_data_sets(self, feed_names=None):
        return self._caller.data_sets_v2.list_data_sets(
            subscription_id=self._subscription_id,
            resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name,
            data_category=DataCategory.DATASET,
            asset_scope=AssetScopeTypes.FEED,
            feed_names=feed_names,
            headers=self._get_custom_headers(),
            cls=None
        )
    # endregion

    # region models api
    @track()
    def _get_model_by_name(self, model_name, version_id=None, feed_name=None):
        return self._caller.models_v2.get_model_by_name(
            subscription_id=self._subscription_id,
            resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name,
            model_name=model_name,
            version_id=version_id,
            feed_name=feed_name,
            headers=self._get_custom_headers(),
            cls=None
        )

    @track()
    def _list_models(self, feed_names=None):
        return self._caller.models_v2.list_models(
            subscription_id=self._subscription_id,
            resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name,
            feed_names=feed_names,
            headers=self._get_custom_headers(),
            cls=None
        )
    # endregion


# region scope component specified helper function
_SCOPE_COMPONENT_STEP_TYPE = "ScopeModule"


def _check_if_contains_scope_component(module_node_run_settings: List[GraphModuleNodeRunSetting]):
    for setting in module_node_run_settings:
        if setting.step_type == _SCOPE_COMPONENT_STEP_TYPE:
            return True
    return False
# endregion


# region Component batch functions
def get_refined_module_dto_identifiers_component(module_dto):
    identifiers = [(module_dto.module_name, None), (module_dto.module_name, module_dto.module_version)]
    return identifiers


_BUILT_IN_MODULE_PREFIX = 'azureml'
_NAMESPACE_SEPARATOR = '://'
_SELECTOR_NAME_VERSION_SEPARATOR = ':'
_SELECTOR_NAME_LABEL_SEPARATOR = '@'


def _resolve_parameter_from_selector(selector: str, logger=None):
    if logger is None:
        logger = logging.getLogger(_get_logger.__module__)
    name = selector
    version = None
    ns_prefix = ''
    # Separate namespace if exists
    if _NAMESPACE_SEPARATOR in name:
        ns_prefix, name = name.split(_NAMESPACE_SEPARATOR, maxsplit=1)
    # Built-in module handler
    if ns_prefix == _BUILT_IN_MODULE_PREFIX:
        # Built-in module only allow name in selector
        if _SELECTOR_NAME_VERSION_SEPARATOR in name or _SELECTOR_NAME_LABEL_SEPARATOR in name:
            raise UserErrorException('Version/Label is not allowed for built-in module. {}'.format(selector))
        return selector, version
    # Uniqueness check
    if _SELECTOR_NAME_LABEL_SEPARATOR in name and _SELECTOR_NAME_VERSION_SEPARATOR in name:
        raise UserErrorException(
            'It is not allowed to specify version and label at the same time. {}'.format(selector))

    def validate_and_split(sp, sp_name):
        if name.count(sp) > 1:
            raise UserErrorException('The specified {} in selector is ambiguous. "{}"'.format(
                sp_name, selector))
        if name.endswith(sp):
            raise UserErrorException('It is not allowed to use "{}" without specify a {}. {}'.format(
                sp, sp_name, selector))
        return name.split(sp, maxsplit=1)

    # Split
    if _SELECTOR_NAME_VERSION_SEPARATOR in name:
        name, version = validate_and_split(_SELECTOR_NAME_VERSION_SEPARATOR, 'version')
    elif _SELECTOR_NAME_LABEL_SEPARATOR in name:
        # Currently we ignore label in selector. - 11/5/2020
        name, label = validate_and_split(_SELECTOR_NAME_LABEL_SEPARATOR, 'label')
        if label is not None:
            logger.warning('Currently only "default" label in selector is supported,'
                           ' label {} will be ignored.'.format(label))
    # Add back prefix if exists
    name = '{}://{}'.format(ns_prefix, name) if ns_prefix != '' else name

    return name, version


def _refine_batch_load_input_component(ids, selectors):
    """
    Refine batch load input.

    1.replace None value with empty list
    2.standardized tuple length to 2

    :param ids: version_ids
    :type ids: List[str]
    :param selectors: name:version or name@label string list
    :type selectors: List[str]
    :return: input after refined
    :rtype: List[str], List[tuple]
    """
    _ids = [] if ids is None else ids
    _identifiers = []

    badly_formed_id = [_id for _id in _ids if not _is_uuid(_id)]
    if len(badly_formed_id) > 0:
        raise UserErrorException('Badly formed version_id found, '
                                 'expected hexadecimal guid, error list {0}'.format(badly_formed_id))

    if selectors is not None:
        for item in selectors:
            name, version = _resolve_parameter_from_selector(item)
            _identifiers.append((name, version))
    return _ids, _identifiers


def _refine_batch_load_output_component(module_dtos, ids, selectors):
    """
    Copy result for duplicate module_version_id.

    Refine result order.

    :param module_dtos: origin result list
    :type List[azure.ml.component._restclients.designer.models.ModuleDto]
    :param ids: version_ids
    :type List[str]
    :param selectors: name:version or name@label list
    :type selectors: List[str]
    :return: refined output and filed component version ids and identifiers
    :rtype: List[azure.ml.component._restclients.designer.models.ModuleDto], List[str], List[tuple]
    """
    id_set = set(ids)
    id_dto_dict = {module_dto.module_version_id: module_dto
                   for module_dto in module_dtos
                   if module_dto.module_version_id in id_set}
    idf_dto_dict = {_idf: _dto for _dto in module_dtos
                    for _idf in get_refined_module_dto_identifiers_component(_dto)}

    failed_ids = []
    failed_identifiers = []
    refined_output = []
    for _id in ids:
        if _id in id_dto_dict.keys():
            refined_output.append(id_dto_dict[_id])
        else:
            failed_ids.append(_id)

    for _idf in selectors:
        if _idf in idf_dto_dict.keys():
            refined_output.append(idf_dto_dict[_idf])
        else:
            failed_identifiers.append(_idf)
    return refined_output, failed_ids, failed_identifiers
# endregion


# region Module batch functions
def get_refined_module_dto_identifiers(module_dto, workspace_name):
    identifiers = [module_dto.module_name, (module_dto.module_name, module_dto.namespace),
                   (module_dto.module_name, module_dto.namespace, module_dto.module_version)]
    _, identifiers = _refine_batch_load_input([], identifiers, workspace_name)
    return identifiers


def _refine_batch_load_input(ids, identifiers, workspace_name):
    """
    Refine batch load input.

    1.replace None value with empty list
    2.standardized tuple length to 3

    :param ids: module_version_ids
    :type ids: List[str]
    :param identifiers: (name,namespace,version) list
    :type identifiers: List[tuple]
    :param workspace_name: default namespace to fill
    :type workspace_name: str
    :return: input after refined
    :rtype: List[str], List[tuple]
    """
    _ids = [] if ids is None else ids
    _identifiers = []

    badly_formed_id = [_id for _id in _ids if not _is_uuid(_id)]
    if len(badly_formed_id) > 0:
        raise UserErrorException('Badly formed module_version_id found, '
                                 'expected hexadecimal guid, error list {0}'.format(badly_formed_id))

    if identifiers is not None:
        for item in identifiers:
            if isinstance(item, tuple):
                if len(item) > 3:
                    raise UserErrorException('Ambiguous identifier tuple found, '
                                             'expected tuple length <= 3, actually {}'.format(item))
                while len(item) < 3:
                    item += (None,)
                _identifiers.append(item)
            else:
                _identifiers.append((item, workspace_name, None))
    return _ids, _identifiers


def _refine_batch_load_output(module_dtos, ids, identifiers, workspace_name):
    """
    Copy result for duplicate module_version_id.

    Refine result order.

    :param module_dtos: origin result list
    :type List[azure.ml.component._restclients.designer.models.ModuleDto]
    :param ids: module_version_ids
    :type List[str]
    :param identifiers: (name,namespace,version) list
    :type List[tuple]
    :return: refined output and filed module version ids and identifiers
    :rtype: List[azure.ml.component._restclients.designer.models.ModuleDto], List[str], List[tuple]
    """
    id_set = set(ids)
    id_dto_dict = {module_dto.module_version_id: module_dto
                   for module_dto in module_dtos
                   if module_dto.module_version_id in id_set}
    idf_dto_dict = {_idf: _dto for _dto in module_dtos
                    for _idf in get_refined_module_dto_identifiers(_dto, workspace_name)}

    failed_ids = []
    failed_identifiers = []
    refined_output = []
    for _id in ids:
        if _id in id_dto_dict.keys():
            refined_output.append(id_dto_dict[_id])
        else:
            failed_ids.append(_id)

    for _idf in identifiers:
        if _idf in idf_dto_dict.keys():
            refined_output.append(idf_dto_dict[_idf])
        else:
            failed_identifiers.append(_idf)
    return refined_output, failed_ids, failed_identifiers
# endregion
