# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from azureml.core import Workspace, Experiment
from .._core._component_definition import ComponentType
from .._restclients.service_caller_factory import _DesignerServiceCallerFactory
from azure.core.pipeline import PipelineResponse

SUBSCRIPTION_ID = 'subscriptionId'
RESOURCE_GROUP = 'resourceGroup'
WORKSPACE_NAME = 'workspaceName'

cached_workspace_by_wsid = {}
_graph_no_status_cache = {}


def _get_run_from_content(content):
    run_id = content.get("runId")
    subscription_id = content.get("subscriptionId")
    resource_group = content.get("resourceGroup")
    workspace_name = content.get("workspaceName")
    experiment_name = content.get("experimentName")

    wsid = '{}/{}/{}'.format(subscription_id, resource_group, workspace_name)
    if wsid in cached_workspace_by_wsid:
        ws = cached_workspace_by_wsid[wsid]
    else:
        ws = Workspace(subscription_id=subscription_id, resource_group=resource_group, workspace_name=workspace_name)
    experiment = Experiment(ws, experiment_name)

    from azure.ml.component import Run
    return Run(experiment, run_id)


def _get_designer_service_caller_from_dict(paras_dict):
    if SUBSCRIPTION_ID not in paras_dict or RESOURCE_GROUP not in paras_dict or WORKSPACE_NAME not in paras_dict:
        return None
    subscription_id = paras_dict[SUBSCRIPTION_ID]
    resource_group = paras_dict[RESOURCE_GROUP]
    workspace_name = paras_dict[WORKSPACE_NAME]
    wsid = '{}/{}/{}'.format(subscription_id, resource_group, workspace_name)
    if wsid in cached_workspace_by_wsid:
        ws = cached_workspace_by_wsid[wsid]
    else:
        ws = Workspace(subscription_id=subscription_id, resource_group=resource_group, workspace_name=workspace_name)
    cached_workspace_by_wsid[wsid] = ws
    service_caller = _DesignerServiceCallerFactory.get_instance(ws)
    return service_caller


def _format_core_run_details(details_dict):
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
    target = details_dict.get('target')
    logFiles = details_dict.get('logFiles')
    return {'input_datasets': input_datasets_dict_list,
            'output_datasets': output_datasets_dict_list,
            'environment': environment_name,
            'environment_version': environment_version,
            'command': command,
            'target': target,
            'logFiles': logFiles}


def _get_node_component_info_from_graph(graph, node_id):
    module_node = next((n for n in graph.module_nodes if n.id == node_id), None)
    if module_node is None:
        module_node = next((n for n in graph.sub_graph_nodes if n.id == node_id), None)

    if module_node is None:
        return {}

    module_dto = next((m for m in graph.graph_module_dtos
                       if m.module_version_id == module_node.module_id), None)

    if module_dto is None:
        return {}

    component_type = ComponentType.get_component_type_by_str(module_dto.job_type)
    return {
        'id': module_dto.module_version_id,
        'version': module_dto.module_version,
        'type': component_type.name if component_type else module_dto.job_type,
        'created_by': module_dto.module_entity.created_by.user_name if module_dto.module_entity.created_by else None}


def _get_graph_from_query_dict(designer_service_caller, query_dict):
    graph_id = query_dict['graphId']
    skip_dataset_load = query_dict.get('skipDatasetLoad', 'true')
    fetch_nested_graphs = query_dict.get('fetchNestedGraphs', 'false')
    skip_dataset_load = True if skip_dataset_load.lower() == 'true' else False
    fetch_nested_graphs = True if fetch_nested_graphs.lower() == 'true' else False
    referenced_node_id = query_dict.get('referencedNodeId', None)

    run_graph = designer_service_caller._get_pipeline_component_graph(
        graph_id=graph_id,
        skip_dataset_load=skip_dataset_load,
        fetch_nested_graphs=fetch_nested_graphs,
        referenced_node_id=referenced_node_id,
        cls=PipelineResponse,
        enum_to_str=True)
    return run_graph


def _get_run_status_from_query_dict(designer_service_caller, query_dict):
    run_status = designer_service_caller.get_pipeline_run_status(
        pipeline_run_id=query_dict['runId'], experiment_id=query_dict['experimentId'], cls=PipelineResponse,
        enum_to_str=True)
    return run_status


def _get_graph_no_staus_from_query_dict(designer_service_caller, query_dict):
    run_id = query_dict['runId']
    include_run_setting_params = query_dict.get('includeRunSettingParams', 'false')
    has_namespace_concept = query_dict.get('hasNamespaceConcept', 'false')
    skip_dataset_load = query_dict.get('skipDatasetLoad', 'true')
    referenced_node_id = query_dict.get('referencedNodeId', None)

    include_run_setting_params = True if include_run_setting_params.lower() == 'true' else False
    has_namespace_concept = True if has_namespace_concept.lower() == 'true' else False
    skip_dataset_load = True if skip_dataset_load.lower() == 'true' else False

    graph_no_status = designer_service_caller.get_pipeline_run_graph_no_status(
        pipeline_run_id=run_id,
        include_run_setting_params=include_run_setting_params,
        has_namespace_concept=has_namespace_concept,
        skip_dataset_load=skip_dataset_load,
        referenced_node_id=referenced_node_id,
        cls=PipelineResponse, enum_to_str=True)

    # the cache will only used in get step run details api
    _graph_no_status_cache[run_id] = graph_no_status.http_response

    return graph_no_status


def _get_step_run_details_from_run(designer_service_caller, run):
    if run._parent_run.id in _graph_no_status_cache:
        parent_run_graph = _graph_no_status_cache[run._parent_run.id]
    else:
        parent_run_graph = designer_service_caller.get_pipeline_run_graph_no_status(
            pipeline_run_id=run._parent_run.id,
            include_run_setting_params=False,
            has_namespace_concept=False,
            skip_dataset_load=True,
            referenced_node_id=False)
        _graph_no_status_cache[run._parent_run.id] = parent_run_graph

    step_nodeid = run._get_node_id()
    component_info = _get_node_component_info_from_graph(parent_run_graph, step_nodeid)
    step_details = _format_core_run_details(run._get_details())
    extended_details = {'componentInfo': component_info}
    extended_details.update({'tags': run._tags})
    step_details.update({'extendedDetails': extended_details})

    return step_details


def _get_child_runs_from_query_dict(designer_service_caller, query_dict):
    run_id = query_dict['runId']
    return designer_service_caller.get_all_layer_child_runs(root_run_id=run_id, cls=PipelineResponse)


def _get_pipeline_run_from_query_dict(designer_service_caller, query_dict):
    run_id = query_dict['runId']
    return designer_service_caller.get_pipeline_run(pipeline_run_id=run_id, cls=PipelineResponse)


def _get_root_run_info_from_query_dict(query_dict):
    run = _get_run_from_content(query_dict)
    root_run_info = {'id': run._core_run._root_run_id}
    return root_run_info
