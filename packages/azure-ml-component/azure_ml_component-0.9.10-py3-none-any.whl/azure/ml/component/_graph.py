# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import hashlib
import inspect
import json
import logging
import uuid
import concurrent.futures
from enum import Enum
from pathlib import Path

from azureml.core.compute import AmlCompute, ComputeInstance, RemoteCompute, HDInsightCompute
from azureml.data.abstract_dataset import AbstractDataset
from azureml.data.data_reference import DataReference
from azureml.data.dataset_consumption_config import DatasetConsumptionConfig
from azureml.exceptions import UserErrorException

from azure.ml.component._restclients.designer.models import LegacyDataPath, ParameterValueType
from azure.ml.component._core._component_definition import ComponentType, SweepComponentDefinition
from azure.ml.component._util._utils import _get_dataset_def_from_dataset, _flatten_pipeline_parameters, \
    is_hyper_parameter
from ._api._api import _DefinitionInterface

from .component import Component, Input, Output, _get_workspace_default_datastore
from ._dataset import _GlobalDataset, _FeedDataset
from ._module_dto import _python_type_to_type_code
from ._parameter_assignment import _ParameterAssignment
from ._pipeline_parameters import PipelineParameter
from ._util._loggerfactory import timer
from ._util._utils import _ensure_dataset_saved_in_workspace, _get_parameter_static_value

from ._restclients.designer.models import GraphDraftEntity, GraphModuleNode, GraphDatasetNode, GraphReferenceNode, \
    GraphEdge, ParameterAssignment, PortInfo, DataSetDefinition, EntityInterface, Parameter, DataPathParameter, \
    OutputSetting, InputSetting, GraphModuleNodeRunSetting, ComputeSetting, \
    RunSettingUIWidgetTypeEnum, ComputeType, MlcComputeInfo, RunSettingParameterAssignment, \
    MinMaxParameterRule, EnumParameterRule, NodePortInterface, NodeInputPort, NodeOutputPort, \
    DatastoreSetting, GraphControlNode, ControlOutput
from .run_settings import _get_compute_type
from ._util._loggerfactory import _LoggerFactory


DATAFRAMEDIRECTORY = 'DataFrameDirectory'
_logger = None


def _get_logger():
    global _logger
    if _logger is not None:
        return _logger
    _logger = _LoggerFactory.get_logger()
    return _logger


class _GraphEntityBuilderContext(object):
    def __init__(self, compute_target=None, pipeline_parameters=None, pipeline_regenerate_outputs=None,
                 module_nodes=None, workspace=None, default_datastore=None, outputs=None,
                 pipeline_nodes=None, pipeline_component_definition=None):
        """
        Init the context needed for graph builder.

        :param compute_target: The compute target.
        :type compute_target: tuple(name, type)
        :param pipeline_parameters: The values of pipeline parameters.
        :type pipeline_parameters: dict
        :param pipeline_regenerate_outputs: the `regenerate_output` value of all module node
        :type pipeline_regenerate_outputs: bool
        :param module_nodes: The list of components expanded from the current pipeline
        :type module_nodes: list[Component]
        :param workspace: The workspace of the current pipeline.
        :type workspace: Workspace
        :param default_datastore: The default datastore.
        :type default_datastore: str
        :param outputs: pipeline outputs
        :type outputs: _AttrDict
        :param pipeline_nodes: The top level pipeline nodes in the current pipeline.
        :type pipeline_nodes: list[Pipeline, Component]
        :param pipeline_component_definition: The definition of the current pipeline.
        :type pipeline_component_definition: PipelineComponentDefinition
        """
        self.compute_target = compute_target
        # Copy pipeline parameters here because after build graph, dataset parameters will be removed.
        self.pipeline_parameters = {} if pipeline_parameters is None else {**pipeline_parameters}
        self.pipeline_parameters = _flatten_pipeline_parameters(self.pipeline_parameters)
        self.pipeline_regenerate_outputs = pipeline_regenerate_outputs

        self.module_nodes = module_nodes
        self.workspace = workspace
        # Correct top pipeline's default datastore here.
        if default_datastore is None:
            default_datastore = _get_workspace_default_datastore(workspace)
        self.default_datastore = default_datastore
        self.outputs = outputs
        self.pipeline_nodes = pipeline_nodes
        self._pipeline_component_definition = pipeline_component_definition


class _GraphEntityBuilder(object):
    """The builder that constructs SMT graph-related entities from `azure.ml.component.Component`."""
    DATASOURCE_PORT_NAME = ''
    DATASOURCE_TYPES = (
        AbstractDataset, DatasetConsumptionConfig, _GlobalDataset, DataReference,
        PipelineParameter,  # Special data source
        _FeedDataset,
        str, Path,  # For local run
    )

    def __init__(self, context: _GraphEntityBuilderContext):
        """
        Init the graph entity builder.

        :param context: The graph entity builder context.
        :type context: _GraphEntityBuilderContext
        """
        self._context = context
        self._nodes = {}
        self._data_path_parameter_input = {}
        self._dataset_parameter_keys = set()
        # This is a mapping from the instance ids of modules(components) in the pipeline
        # to the graph node ids in the built graph.
        # We use this mapping to get the graph node according to the module instance in the pipeline
        # when constructing subpipeline, visualization graph, etc..
        self._module_node_to_graph_node_mapping = {}
        self.data_path_assignments = {}
        self._reversed_outputs = {}

    @property
    def module_node_to_graph_node_mapping(self):
        return self._module_node_to_graph_node_mapping

    def _get_node_by_component(self, component: Component):
        return self._nodes.get(self.module_node_to_graph_node_mapping.get(component._get_instance_id()))

    def _get_mapped_sub_graph_output_port(self, component: Component, port_name: str):
        pipelines = [m for m in self._modules if m._is_pipeline]
        for p in pipelines:
            for k, v in p.outputs.items():
                if v._owner == component and v.port_name == port_name:
                    return PortInfo(node_id=self._get_node_by_component(p).id, port_name=k)

    @timer()
    def build_graph_entity(self, for_registration: bool = False, enable_subpipeline_registration: bool = False,
                           anonymous_creation=True, default_datastore=None):
        """
        Build graph entity that can be used to create pipeline draft, pipeline run and pipeline component.

        Notice that context.pipeline_parameters will be modified after build,
            dataset parameters will be removed.

        :param for_registration: Whether the graph builder is for pipeline component registration.
        In this case, we need to generate specific graph entity interfaces.
        :type for_registration: bool
        :param enable_subpipeline_registration: Whether do sub pipeline registration
        when building the graph draft entity. Currently, we will still need to check the environment variable
        'ENABLE_SUBPIPELINE_REGISTER' to decide if the graph builder will did the registration
        :type enable_subpipeline_registration: bool
        :param anonymous_creation: is anonymous register or not
        :type anonymous_creation: bool
        :param default_datastore: The default datastore.
        :type default_datastore: str

        :return Tuple of (graph entity, module node run settings)
        :rtype tuple
        """
        if self._context.outputs is not None:
            # Create a mapping of the component output port and pipeline output port.
            # The key is a tuple (component, port_name), the value is the list of pipeline output port name.
            for name, val in self._context.outputs.items():
                key = (val._owner, val.port_name)
                if key not in self._reversed_outputs:
                    self._reversed_outputs[key] = []
                self._reversed_outputs[key].append(name)

        # if subpipeline registration is enabled, we need to do three things here:
        # 1. overwrite the module nodes, since we do not want the sub pipeline node be expanded
        # 2. register subpipeline if it is not registered
        if enable_subpipeline_registration:
            thread_pool, create_component_futures = concurrent.futures.ThreadPoolExecutor(), set()
            self._modules = self._context.pipeline_nodes
            for node in self._modules:
                if node._is_pipeline and not node._is_registered(self._context.workspace):
                    # Parallel registering pipeline component.
                    # Because the operations, checking register_task and submitting register task, are not atomic,
                    # it may happen that the registration request of the same definition is sent at the same time.
                    future_task = node._register_sub_pipelines(thread_pool, self._context.workspace, default_datastore)
                    create_component_futures.add(future_task)
            concurrent.futures.wait(create_component_futures, return_when=concurrent.futures.ALL_COMPLETED)
            # Raise exception in the thread pool.
            [future.result() for future in create_component_futures]
        else:
            self._modules = self._context.module_nodes

        # Prepare the entity
        graph_entity = GraphDraftEntity()
        graph_entity.dataset_nodes = []
        graph_entity.module_nodes = []
        graph_entity.sub_graph_nodes = []
        graph_entity.control_nodes = []
        graph_entity.edges = []
        graph_entity.entity_interface = EntityInterface(parameters=[], data_path_parameters=[],
                                                        data_path_parameter_list=[])

        # Set the default_compute and default_datastore
        if self._context.compute_target is not None:
            default_compute_name, default_compute_type = self._context.compute_target
            if default_compute_type is None:
                default_compute_type = _get_compute_type(self._context.workspace, default_compute_name)
            graph_entity.default_compute = ComputeSetting(
                name=default_compute_name,
                compute_type=ComputeType.MLC,
                mlc_compute_info=MlcComputeInfo(mlc_compute_type=default_compute_type)
            )
        if self._context.default_datastore is not None:
            graph_entity.default_datastore = DatastoreSetting(data_store_name=self._context.default_datastore)

        # Note that we need to generate all module nodes before constructing edges.
        for module in self._modules:
            if module._definition._type == ComponentType.PipelineComponent:
                module_node = self._build_graph_ref_node(
                    module, self._context.pipeline_regenerate_outputs,
                    for_registration, self._context.workspace)
                graph_entity.sub_graph_nodes.append(module_node)
            elif module._definition._type == ComponentType.ControlComponent:
                module_node = self._build_graph_control_node(module, for_registration)
                graph_entity.control_nodes.append(module_node)
            else:
                module_node = self._build_graph_module_node(
                    module, self._context.pipeline_regenerate_outputs,
                    for_registration, self._context.workspace)
                graph_entity.module_nodes.append(module_node)
            self._nodes[module_node.id] = module_node

        # Start generating edges and other settings
        module_node_run_settings = []
        for module in self._modules:
            module_node = self._get_node_by_component(module)
            self._produce_module_edges(graph_entity, module, module_node, enable_subpipeline_registration,
                                       for_registration)
            if module._definition._type == ComponentType.ControlComponent:
                self._update_control_node_params(module, module_node)
                continue
            module_node_run_settings.append(
                self._produce_module_runsettings(
                    graph_entity, module, module_node, self._context.pipeline_parameters, self._context.workspace))

            self._update_module_node_params(
                graph_entity, module_node, module, self._context.pipeline_parameters,
                for_registration, default_datastore)

        self._update_data_path_parameter_list(graph_entity)
        self._update_data_path_parameters(graph_entity)

        # disable this for now. Because backend will hit null ref when data path assignments is not valued
        # self._update_data_path_parameters(graph_entity)

        # Set this for further usage including creating subpipeline info, creating visualization graph and export.
        # This is a little hacky, but graph_entity is a swagger generated class which cannot be modified,
        # so currently we just keep this.
        setattr(graph_entity, 'module_node_to_graph_node_mapping', self.module_node_to_graph_node_mapping)

        # Remove empty data source node.
        # Remove instead of just not adding it because we need display empty node when visualize in notebook.
        remove_node_ids = self.resolve_empty_nodes(graph_entity)
        graph_entity.dataset_nodes = [node for node in graph_entity.dataset_nodes
                                      if node.id not in remove_node_ids]
        graph_entity.edges = [edge for edge in graph_entity.edges
                              if edge.source_output_port.node_id not in remove_node_ids]

        # Re-generate entity interface for pipeline component registration graph
        if for_registration:
            self.update_graph_entity_interface(graph_entity, anonymous_creation=anonymous_creation)
        else:
            # Keep graph data path parameter order as original pipeline parameter order.
            # Just easy for customer to read if there are many parameters.
            graph_entity.entity_interface.data_path_parameter_list = \
                self.sort_parameter_order(graph_entity.entity_interface.data_path_parameter_list)
            graph_entity.entity_interface.parameters = \
                self.sort_parameter_order(graph_entity.entity_interface.parameters)

        return graph_entity, module_node_run_settings

    def build_graph_json(self, for_registration: bool = False):
        """Build graph and convert the object to json string recursively."""
        def serialize_object_to_dict(obj):
            if type(obj) in [str, int, float, bool] or obj is None:
                return obj

            if isinstance(obj, dict):
                for k, v in obj.items():
                    obj[k] = serialize_object_to_dict(v)
            elif type(obj) in [tuple, list]:
                obj = [serialize_object_to_dict(i) for i in obj]
            else:
                obj = serialize_object_to_dict(obj.__dict__)
            return obj

        graph, module_node_run_settings = self.build_graph_entity(enable_subpipeline_registration=True,
                                                                  for_registration=for_registration)
        compute_name = None if graph.default_compute is None else graph.default_compute.name
        datastore_name = None if graph.default_datastore is None else graph.default_datastore.data_store_name
        graph_dict = {'module_nodes': [serialize_object_to_dict(i) for i in graph.module_nodes],
                      'sub_graph_nodes': [serialize_object_to_dict(i) for i in graph.sub_graph_nodes],
                      'dataset_nodes': [serialize_object_to_dict(i) for i in graph.dataset_nodes],
                      'edges': [serialize_object_to_dict(i) for i in graph.edges],
                      'entity_interface': serialize_object_to_dict(graph.entity_interface),
                      'default_compute': compute_name,
                      'default_datastore': datastore_name,
                      'module_node_run_settings': serialize_object_to_dict(module_node_run_settings)}

        return json.dumps(graph_dict, indent=4, sort_keys=True)

    def sort_parameter_order(self, parameters_list):
        parameters = {_p.name: _p for _p in parameters_list}
        results = {_k: parameters[_k] for _k in self._context.pipeline_parameters.keys() if _k in parameters}
        results.update({_p.name: _p for _p in parameters_list if _p.name not in results})
        return list(results.values())

    def resolve_empty_nodes(self, graph_entity):
        remove_node_ids = []
        data_path_param_names = set(i.name for i in graph_entity.entity_interface.data_path_parameter_list
                                    if i.default_value is not None)
        for node in graph_entity.dataset_nodes:
            dataset_def = node.data_set_definition
            if node.dataset_id is None and (dataset_def is None or (
                    dataset_def.value is None and dataset_def.parameter_name not in data_path_param_names)):
                remove_node_ids.append(str(node.id))
        return set(remove_node_ids)

    def _produce_module_runsettings(
            self, graph_entity: GraphDraftEntity, module: Component, module_node: GraphModuleNode,
            pipeline_parameters, workspace):
        if module.runsettings is None:
            return None

        # do not remove this, or else module_node_run_setting does not make a difference
        module_node_run_setting = GraphModuleNodeRunSetting()
        identifier = module._definition._identifier_in_workspace(workspace)
        module_node_run_setting.module_id = identifier
        module_node_run_setting.node_id = module_node.id
        module_node_run_setting.step_type = module._definition._module_dto.module_entity.step_type
        # Populate submission runsettings
        module_node_run_setting.run_settings, use_default_compute = \
            _populate_submission_runsettings(module, pipeline_parameters, workspace)
        # module_node.use_graph_default_compute doesn't take effect,
        # only runsettings.target.use_graph_default_compute takes effect
        module_node.use_graph_default_compute = use_default_compute
        # Add required pipeline parameter, add them to graph.
        _GraphEntityBuilder._append_component_runsetting_pipeline_parameter_to_interface(
            graph_entity, module_node_run_setting.run_settings, pipeline_parameters,
            self._context._pipeline_component_definition)
        return module_node_run_setting

    def _produce_module_edges(self, graph_entity, module, module_node, enable_subpipeline_registration,
                              for_registration):
        # Note that for old components(especially for built-in components),
        # input_name could be different from argument name, we need to use input_name as the key
        inputs_map = {
            module._get_input_name_by_argument_name(k): i
            for k, i in module._input_ports.items() if i._dset is not None
        }
        # Produce edge for input port
        for input_name, i in inputs_map.items():
            input_dataset = i._get_internal_data_source()
            input_def = module._get_input_definition_by_argument_name(i.name)
            dest_is_parameter = True if input_def._is_primitive_type else None
            # when the input is assigned with non None value, i._dset will be Input, otherwise PipelineParameter
            if (isinstance(i._dset, Input) or isinstance(i._dset, PipelineParameter)) and \
                    enable_subpipeline_registration and for_registration:
                edge = self._produce_edge_graph_port_to_module_node(
                    i._dset.name, input_name, module_node, dest_is_parameter=dest_is_parameter)
            elif isinstance(input_dataset, _GraphEntityBuilder.DATASOURCE_TYPES):
                dataset_node = self._get_or_create_dataset_node(graph_entity, i)
                edge = self._produce_edge_dataset_node_to_module_node(input_name, dataset_node, module_node)
            elif isinstance(input_dataset, Output):
                edge = self._produce_edge_module_node_to_module_node(
                    input_name, input_dataset, module_node, dest_is_parameter=dest_is_parameter,
                    enable_subpipeline_registration=enable_subpipeline_registration)
            else:
                raise ValueError("Invalid input type: {0}".format(type(input_dataset)))
            if edge is not None:
                graph_entity.edges.append(edge)
        # Produce edge for output as parameter case
        # Note: PipelineParameter(Output) structure is not included,
        # because the Output type of pipeline parameter will not effect pipeline graph structure.
        for input_name, value in module._parameter_params.items():
            input_name = next((
                k for k, v in module._name_to_argument_name_mapping.items() if v == input_name), input_name)
            edge = None
            if isinstance(value, Output):
                edge = self._produce_edge_module_node_to_module_node(
                    input_name, value, module_node, dest_is_parameter=True,
                    enable_subpipeline_registration=enable_subpipeline_registration
                )
            elif isinstance(value, PipelineParameter) and isinstance(value.default_value, Output):
                edge = self._produce_edge_graph_port_to_module_node(
                    value.name, input_name, module_node, dest_is_parameter=True)
            if edge is not None:
                graph_entity.edges.append(edge)
        # Produce edge if module is control by ControlComponent
        if module._control_by is not None:
            control_component, edge_type = module._control_by
            edge = self._produce_edge_control_to_module_node(control_component, edge_type, module_node)
            graph_entity.edges.append(edge)

    def _produce_edge_control_to_module_node(self, control_component, edge_type, module_node):
        source = PortInfo(
            node_id=self._get_node_by_component(control_component).id, port_name=edge_type)
        dest = PortInfo(node_id=module_node.id, port_name='')
        return GraphEdge(source_output_port=source, destination_input_port=dest)

    def _produce_edge_dataset_node_to_module_node(self, input_name, dataset_node, module_node):
        source = PortInfo(node_id=dataset_node.id, port_name=self.DATASOURCE_PORT_NAME)
        dest = PortInfo(node_id=module_node.id, port_name=input_name)
        return GraphEdge(source_output_port=source, destination_input_port=dest)

    def _produce_edge_module_node_to_module_node(
            self, input_name, output: Output, dest_module_node,
            dest_is_parameter=None, enable_subpipeline_registration=True
    ):
        while not enable_subpipeline_registration and output._owner._is_pipeline:
            output = output._owner._outputs_mapping[output._name]

        # Note that we call topology sort before this so we could make sure the source module node has been added.
        source_module_node = self._get_node_by_component(output._owner)
        # if source_module_node is None, it means the output._owner is inside a pipeline component
        # in this case, we should make the source output port as the corresponding pipeline component's output port
        if source_module_node is None:
            source = self._get_mapped_sub_graph_output_port(output._owner, output._port_name)
        else:
            source = PortInfo(node_id=source_module_node.id, port_name=output.port_name)
        dest = PortInfo(node_id=dest_module_node.id, port_name=input_name, is_parameter=dest_is_parameter)
        return GraphEdge(source_output_port=source, destination_input_port=dest)

    def _produce_edge_graph_port_to_module_node(
            self, source_port_name, input_name, module_node, dest_is_parameter=None
    ):
        source = PortInfo(graph_port_name=source_port_name)
        dest = PortInfo(node_id=module_node.id, port_name=input_name, is_parameter=dest_is_parameter)
        return GraphEdge(source_output_port=source, destination_input_port=dest)

    def _get_or_create_dataset_node(self, graph_entity: GraphDraftEntity, input: Input):
        # Need to be refined, what if a dataset provide different modes?
        dataset_node = self._build_graph_datasource_node(input)
        if dataset_node not in graph_entity.dataset_nodes:
            graph_entity.dataset_nodes.append(dataset_node)
            self._nodes[dataset_node.id] = dataset_node

        return dataset_node

    def _build_graph_control_node(self, module: Component, for_registration: bool):
        node_id = self._generate_node_id(module._get_component_name()) \
            if for_registration else self._generate_node_id()
        module_node = GraphControlNode(id=node_id, control_type=module._definition._control_type.value)
        self.module_node_to_graph_node_mapping[module._get_instance_id()] = node_id
        return module_node

    def _build_graph_module_node(self, module: Component,
                                 pipeline_regenerate_outputs: bool, for_registration: bool,
                                 workspace=None) -> GraphModuleNode:
        node_name = module._get_component_name()
        node_id = self._generate_node_id(node_name) \
            if for_registration else self._generate_node_id()

        regenerate_output = pipeline_regenerate_outputs \
            if pipeline_regenerate_outputs is not None else module.regenerate_outputs
        if module._definition.registry_name:
            identifier = module._definition.identifier
        else:
            identifier = module._definition._identifier_in_workspace(workspace)
        module_node = GraphModuleNode(id=node_id, module_id=identifier, name=node_name,
                                      regenerate_output=regenerate_output, comment=module.comment)
        module_node.module_parameters = []
        module_node.module_metadata_parameters = []
        self.module_node_to_graph_node_mapping[module._get_instance_id()] = node_id
        return module_node

    def _build_graph_ref_node(self, module: Component,
                              pipeline_regenerate_outputs: bool, for_registration: bool,
                              workspace=None) -> GraphReferenceNode:
        node_name = module._get_component_name()
        node_id = self._generate_node_id(node_name) \
            if for_registration else self._generate_node_id()

        regenerate_output = pipeline_regenerate_outputs \
            if pipeline_regenerate_outputs is not None else module.regenerate_outputs
        identifier = module._definition._identifier_in_workspace(workspace)
        module_node = GraphReferenceNode(id=node_id, module_id=identifier, name=node_name,
                                         regenerate_output=regenerate_output, comment=module.comment)
        module_node.module_parameters = []
        module_node.module_metadata_parameters = []
        self.module_node_to_graph_node_mapping[module._get_instance_id()] = node_id
        return module_node

    @staticmethod
    def _append_pipeline_parameter_to_interface(
            graph_entity, pipeline_parameters, parameter_name, pipeline_definition=None):
        """
        Add necessary pipeline parameter to resolve parameter reference.

        :param graph_entity: the graph entity.
        :type graph_entity: GraphDraftEntity
        :param pipeline_parameters: the pipeline parameters dict.
        :type pipeline_parameters: dict
        :param parameter_name: the parameter name.
        :type parameter_name: str
        :param pipeline_definition: the pipeline definition used to get parameter definition.
        :type pipeline_definition: PipelineComponentDefinition
        """
        if pipeline_parameters is None or graph_entity is None or parameter_name not in pipeline_parameters:
            return
        exist = next((x for x in graph_entity.entity_interface.parameters
                      if x.name == parameter_name), None) is not None
        if not exist:
            # Here we get literal value
            value = pipeline_parameters[parameter_name]
            # Get the pipeline parameter object in pipeline definition, to reach annotation and group names
            param_in_definition = _flatten_pipeline_parameters(
                pipeline_definition._pipeline_parameters).get(parameter_name) if pipeline_definition else None
            # Default value here should be the parameter's real value, not default in definition.
            # Note: Use annotation from pipeline definition parameters instead of call param._annotation directly.
            # Because param._annotation may be None
            annotation = pipeline_definition._flattened_parameters.get(parameter_name) \
                if param_in_definition is not None else None
            if annotation:
                parameter = Parameter(
                    name=parameter_name, default_value=value,
                    group_names=param_in_definition._groups if param_in_definition._groups else None,
                    label=param_in_definition.name, is_optional=annotation.optional,
                    type=_DefinitionInterface._convert_parameter_type_string_to_enum(annotation.type).value)
            else:
                parameter = Parameter(
                    name=parameter_name, default_value=value,
                    label=parameter_name, is_optional=False, type=_python_type_to_type_code(type(value)))
            graph_entity.entity_interface.parameters.append(parameter)

    @staticmethod
    def _append_pipeline_parameter_in_assignment_to_interface(
            graph_entity, pipeline_parameters, assignment, pipeline_definition=None):
        """Append assignment used parameter to entity interface."""
        if pipeline_parameters is None or not isinstance(assignment, _ParameterAssignment) or graph_entity is None:
            return
        # Add necessary pipeline parameter to resolve parameter reference
        for name in assignment.expand_all_parameter_name_set():
            if name in pipeline_parameters:
                _GraphEntityBuilder._append_pipeline_parameter_to_interface(
                    graph_entity, pipeline_parameters, name, pipeline_definition)

    @staticmethod
    def _append_component_runsetting_pipeline_parameter_to_interface(
            graph_entity, module_node_runsettings, pipeline_parameters, pipeline_definition=None):
        """Append pipeline parameter used in component runsettings to interface."""

        def append_by_type(obj):
            if obj.value_type == _GraphEntityBuilder.GRAPH_PARAMETER_NAME:
                _GraphEntityBuilder._append_pipeline_parameter_to_interface(
                    graph_entity, pipeline_parameters, obj.value, pipeline_definition)
            elif obj.value_type == _GraphEntityBuilder.CONCATENATE:
                for part in obj.assignments_to_concatenate:
                    append_by_type(part)

        for runsetting in module_node_runsettings:
            if runsetting.value_type == _GraphEntityBuilder.LITERAL:
                continue
            append_by_type(runsetting)

    def _update_control_node_params(self, component, control_node: GraphControlNode):
        control_parameter_name = component._definition._control_parameter_name
        control_parameter_value = component.inputs.get(control_parameter_name)
        if type(control_parameter_value) is bool:
            # literal condition
            control_node.control_parameter = ParameterAssignment(
                name=control_parameter_name, value=control_parameter_value,
                value_type=_GraphEntityBuilder.LITERAL
            )
        elif isinstance(control_parameter_value, PipelineParameter) and \
                not isinstance(control_parameter_value.default_value, Output):
            # pipeline parameter condition
            control_node.control_parameter = ParameterAssignment(
                name=control_parameter_name, value=control_parameter_value.name,
                value_type=_GraphEntityBuilder.GRAPH_PARAMETER_NAME
            )
        else:
            # control output or pipeline port condition
            control_node.control_parameter = ParameterAssignment(
                name=control_parameter_name, value=control_parameter_name,
                value_type=_GraphEntityBuilder.INPUT
            )

    def _update_module_node_params(
            self, graph_entity: GraphDraftEntity, module_node: GraphModuleNode, module: Component, pipeline_parameters,
            for_registration: bool, default_datastore=None
    ):
        """Add module node parameters and update it with context.pipeline_parameters."""

        node_parameters = module._get_default_parameters()
        node_pipeline_parameters = {}
        node_str_assignment_parameters = {}

        user_provided_params = module._build_params()
        for param_name, param_value in user_provided_params.items():
            # TODO: Use an enum for value_type
            if isinstance(param_value, Input):
                param_value = param_value._get_internal_data_source()
            if isinstance(param_value, PipelineParameter):
                # Notice that pipeline_param_name != param_name here
                # pipeline_param_name is the real value's pipeline parameter name
                # param_name is the parameter definition name on component
                pipeline_param_name = param_value._full_name
                if pipeline_param_name in pipeline_parameters:
                    node_pipeline_parameters[param_name] = pipeline_param_name
                    # Add necessary pipeline parameter to resolve parameter reference
                    _GraphEntityBuilder._append_pipeline_parameter_to_interface(
                        graph_entity, pipeline_parameters, pipeline_param_name,
                        self._context._pipeline_component_definition)
                    if param_name in node_parameters:
                        del node_parameters[param_name]
                else:
                    # Some call from visualize may reach here,
                    # because they pass the pipeline parameter without default params.
                    node_parameters[param_name] = param_value.default_value
            elif isinstance(param_value, _ParameterAssignment):
                node_str_assignment_parameters[param_name] = param_value
                _GraphEntityBuilder._append_pipeline_parameter_in_assignment_to_interface(
                    graph_entity, pipeline_parameters, param_value, self._context._pipeline_component_definition)
                if param_name in node_parameters:
                    del node_parameters[param_name]
            else:
                # Assign constant and Output object directly
                node_parameters[param_name] = param_value

        # Put PipelineParameter as data_path_parameter for updating datapath list
        module_node.module_input_settings = []
        for input in module._input_ports.values():
            input_def = module._get_input_definition_by_argument_name(input.name)
            # Skip generate input setting for primitive type input
            if input_def._is_primitive_type:
                continue
            input_setting = InputSetting(
                name=input_def.name,
                data_store_mode=input.mode,
                path_on_compute=input._path_on_compute
            )
            module_node.module_input_settings.append(input_setting)

            input_data_source = input._get_internal_data_source()
            if not isinstance(input_data_source, PipelineParameter) or \
                    input_data_source.name in self._data_path_parameter_input:
                continue
            self._data_path_parameter_input[input_data_source.name] = input_data_source

        self._batch_append_module_node_parameter(module_node, node_parameters)
        self._batch_append_module_node_pipeline_parameters(module_node, node_pipeline_parameters)
        # Update formatter parts using new pipeline_parameters dict.
        self._batch_append_module_node_assignment_parameters(
            module_node, node_str_assignment_parameters, pipeline_parameters)

        module_node.module_output_settings = []
        # Resolve the pipeline datastore first
        pipeline_datastore_name = default_datastore or module._resolve_default_datastore(self._context.workspace)

        module_node.use_graph_default_datastore = True

        # If a component's port is exposed as a subgraph port, set use_graph_default_datastore = False
        if self._context.outputs and module.outputs:
            if set([output._owner for output in module.outputs.values()]).intersection(
                    set([key[0] for key in self._reversed_outputs.keys()])):
                module_node.use_graph_default_datastore = False

        for output_name, output in module.outputs.items():
            # for subgraph node, the output port name is not the same as the inner output's port name
            port_name = output_name if module._is_pipeline else output.port_name
            if output.datastore is not None:
                module_node.use_graph_default_datastore = False

            # if module's output is pipeline output, build as data path assignment and add edge for it
            # 1. datastore=pipeline_param  can link pipeline parameters and resumbit
            # 2. return components.outputs can link pipeline parameters and resumbit
            # If there are 1 and 2, we keep 2
            data_assignment_param_names = self._reversed_outputs.get((output._owner, output.port_name), [])

            for data_assignment_param_name in data_assignment_param_names:
                if isinstance(output.datastore, (PipelineParameter, _ParameterAssignment)):
                    output._datastore = _get_parameter_static_value(output.datastore, pipeline_parameters)
                    logging.warning(f'Pipeline paramter binding from {module_node.name}.outputs.'
                                    f'{data_assignment_param_name}.datastore is ignored because of output port '
                                    f'{data_assignment_param_name} also bind as pipeline output')
                if isinstance(output.path_on_datastore, (PipelineParameter, _ParameterAssignment)):
                    output._dataset_output_options.path_on_datastore = \
                        _get_parameter_static_value(output.path_on_datastore, pipeline_parameters)
                    logging.warning(f'Pipeline paramter binding from {module_node.name}.outputs.'
                                    f'{data_assignment_param_name}.path_on_datastore is ignored '
                                    f'because of output port '
                                    f'{data_assignment_param_name} also bind as pipeline output')
                self.data_path_assignments[data_assignment_param_name] = LegacyDataPath(
                    data_store_name=output.datastore if output.datastore else pipeline_datastore_name,
                    relative_path=output.path_on_datastore
                )
                # add edge for pipeline output
                source = PortInfo(node_id=module_node.id, port_name=port_name)
                dest = PortInfo(graph_port_name=data_assignment_param_name)
                graph_entity.edges.append(GraphEdge(source_output_port=source, destination_input_port=dest))

            output_link_attrs = output._get_link_parameter_attr()
            for output_instance, output_attr_name, output_attr_parameter_assignment_name in output_link_attrs:
                self._link_parameter_to_output(
                    graph_entity=graph_entity,
                    pipeline_parameters=pipeline_parameters,
                    output=output_instance,
                    output_attr_name=output_attr_name,
                    output_attr_parameter_assignment_name=output_attr_parameter_assignment_name)

            def generate_module_output_settings(port_name, output,
                                                pipeline_datastore_name, data_assignment_param_name=None):
                output_setting = OutputSetting(
                    name=port_name,
                    data_store_name=None if output._data_store_parameter_assignment
                    else (output.datastore if output.datastore else pipeline_datastore_name),
                    data_store_name_parameter_assignment=output._data_store_parameter_assignment,
                    data_store_mode=output.mode,
                    path_on_compute=None if output._path_on_compute_parameter_assignment else output._path_on_compute,
                    path_on_compute_parameter_assignment=output._path_on_compute_parameter_assignment,
                    data_reference_name=port_name,
                    dataset_registration=output._dataset_registration,
                    dataset_output_options=output._dataset_output_options,
                    parameter_name=data_assignment_param_name,
                )
                if getattr(getattr(output_setting, 'dataset_output_options', None),
                           'path_on_datastore_parameter_assignment', None):
                    output_setting.dataset_output_options.path_on_datastore = None
                return output_setting

            if not for_registration and data_assignment_param_names:
                for data_assignment_param_name in data_assignment_param_names:
                    output_setting = generate_module_output_settings(port_name,
                                                                     output,
                                                                     pipeline_datastore_name,
                                                                     data_assignment_param_name)
                    module_node.module_output_settings.append(output_setting)
            else:
                # NOT set the parameter name in pipeline component's graph, or else it will confuse the backend
                output_setting = generate_module_output_settings(port_name,
                                                                 output,
                                                                 pipeline_datastore_name,
                                                                 data_assignment_param_name=None)
                module_node.module_output_settings.append(output_setting)

    def _link_parameter_to_output(self, graph_entity, pipeline_parameters, output, output_attr_name,
                                  output_attr_parameter_assignment_name):
        output_attr = getattr(output, output_attr_name, None)
        if isinstance(output_attr, PipelineParameter):
            pipeline_param_name = output_attr._full_name
            param_assignment = ParameterAssignment(
                name=None,
                value=pipeline_param_name,
                value_type=self.GRAPH_PARAMETER_NAME)
            setattr(output, output_attr_parameter_assignment_name, param_assignment)
            _GraphEntityBuilder._append_pipeline_parameter_to_interface(
                graph_entity, pipeline_parameters, pipeline_param_name,
                self._context._pipeline_component_definition)
        elif isinstance(output_attr, _ParameterAssignment):
            assignments_to_concatenate = _GraphEntityBuilder._get_assignments_to_concatenate(
                output_attr,
                pipeline_parameters)
            param_assignment = ParameterAssignment(
                name=None,
                value=None,
                value_type=self.CONCATENATE, assignments_to_concatenate=assignments_to_concatenate)
            setattr(output, output_attr_parameter_assignment_name, param_assignment)
            _GraphEntityBuilder._append_pipeline_parameter_in_assignment_to_interface(
                graph_entity, pipeline_parameters, output_attr,
                self._context._pipeline_component_definition)

    def _update_data_path_parameter_list(self, graph_entity: GraphDraftEntity):
        """Update data path parameters with dataset parameters in context.pipeline_parameters."""
        def get_override_parameters_def(name, origin_val, pipeline_parameters):
            # Check if user choose to override with pipeline parameters
            if pipeline_parameters is not None and len(pipeline_parameters) > 0:
                for k, v in pipeline_parameters.items():
                    if k == name:
                        self._dataset_parameter_keys.add(k)
                        if isinstance(v, _GlobalDataset):
                            return _get_dataset_def_from_dataset(v)
                        elif isinstance(v, AbstractDataset):
                            _ensure_dataset_saved_in_workspace(v, self._context.workspace)
                            return _get_dataset_def_from_dataset(v)
                        else:
                            raise UserErrorException('Invalid parameter value for dataset parameter: {0}'.format(k))

            return origin_val

        pipeline_parameters = self._context.pipeline_parameters
        for name, pipeline_parameter in self._data_path_parameter_input.items():
            dset = pipeline_parameter.default_value
            dataset_def = None

            if isinstance(dset, DatasetConsumptionConfig):
                dset = dset.dataset

            if isinstance(dset, AbstractDataset):
                _ensure_dataset_saved_in_workspace(dset, self._context.workspace)
                dataset_def = _get_dataset_def_from_dataset(dset)

            if isinstance(dset, (_GlobalDataset, DataReference)):
                dataset_def = _get_dataset_def_from_dataset(dset)
            dataset_def = get_override_parameters_def(name, dataset_def, pipeline_parameters)
            if dataset_def is not None:
                exist = next((x for x in graph_entity.entity_interface.data_path_parameter_list
                              if x.name == name), None) is not None
                if not exist:
                    graph_entity.entity_interface.data_path_parameter_list.append(DataPathParameter(
                        name=name,
                        default_value=dataset_def.value,
                        is_optional=False,
                        data_type_id=DATAFRAMEDIRECTORY
                    ))

    def _update_data_path_parameters(self, graph_entity: GraphDraftEntity):
        if self._context._pipeline_component_definition is None:
            return
        entity_interface = graph_entity.entity_interface
        for output_name, output_def in self._context._pipeline_component_definition.outputs.items():
            # Leave 'default_value' as None, MT will add the default value
            entity_interface.data_path_parameters.append(DataPathParameter(
                name=output_name,
                is_optional=True,
                documentation=output_def.description,
                data_type_id=output_def.type
            ))

    def update_graph_entity_interface(self, graph_entity: GraphDraftEntity, anonymous_creation=True):
        """For pipeline component registration graph, we need to:
        - update entity_interface.parameters to definitions
        - move entity_interface.data_path_parameter_list to entity_interface.ports.inputs
        - add entity_interface.ports.outputs from output definition"""
        entity_interface = graph_entity.entity_interface
        # Update parameters
        entity_interface.parameters = []
        pipeline_definition = self._context._pipeline_component_definition
        for param_name, param in _flatten_pipeline_parameters(
                pipeline_definition._pipeline_parameters).items():
            # Skip input as we will add them into ports
            if param_name in pipeline_definition.inputs:
                continue
            # Note: Use annotation from pipeline definition parameters instead of call param._annotation directly.
            # Because param._annotation may be None
            param_def = pipeline_definition._flattened_parameters.get(param_name)
            if param_def is None:
                raise Exception(
                    f'Parameter {param_name!r} definition not found in pipeline {pipeline_definition.name!r}, '
                    f'parameters {list(pipeline_definition._flattened_parameters.keys())}')
            param = Parameter(
                name=param_name,
                documentation=param_def.description,
                default_value=(None if param_def.default is inspect.Parameter.empty else param_def.default),
                is_optional=param_def.optional,
                label=param_def.name,
                type=_DefinitionInterface._convert_parameter_type_string_to_enum(param_def.type).value,
                group_names=param._groups if param._groups else None)
            if param_def.min or param_def.max:
                param.min_max_rules = [MinMaxParameterRule(min=param_def.min, max=param_def.max)]
            if param_def.enum:
                param.enum_rules = [EnumParameterRule(valid_values=param_def.enum)]
            entity_interface.parameters.append(param)

        entity_interface.ports = NodePortInterface(inputs=[], outputs=[], control_outputs=[])
        # Update inputs
        pipeline_definition = self._context._pipeline_component_definition
        for input_name, input_def in pipeline_definition.inputs.items():
            if input_def._default and not anonymous_creation:
                _get_logger().warning(
                    f'Default value of pipeline component {pipeline_definition.name!r}'
                    f' port {input_name!r} is not supported and will be ignored.')
            entity_interface.ports.inputs.append(NodeInputPort(
                name=input_name,
                documentation=input_def.description,
                is_optional=input_def.optional,
                data_types_ids=_DefinitionInterface._to_data_type_ids_list(input_def)
            ))
            # Fix edge from dataset node (now is pipeline input port) to component node port
            data_node = next(
                (n for n in graph_entity.dataset_nodes if n.data_set_definition.parameter_name == input_name),
                None)
            if not data_node:
                continue
            edges = [e for e in graph_entity.edges if e.source_output_port.node_id == data_node.id]
            for edge in edges:
                edge.source_output_port = PortInfo(graph_port_name=input_name)
            # Delete dataset node
            graph_entity.dataset_nodes.remove(data_node)

        entity_interface.data_path_parameter_list = []
        entity_interface.data_path_parameters = []
        entity_interface.ports.control_outputs = []

        # Update outputs
        for output_name, output_def in self._context._pipeline_component_definition.outputs.items():
            entity_interface.ports.outputs.append(NodeOutputPort(
                name=output_name,
                documentation=output_def.description,
                data_type_id=output_def.type
            ))
            if output_def.is_control:
                entity_interface.ports.control_outputs.append(ControlOutput(name=output_name))

    LITERAL = ParameterValueType.literal.value
    GRAPH_PARAMETER_NAME = ParameterValueType.graph_parameter_name.value
    CONCATENATE = ParameterValueType.concatenate.value
    INPUT = ParameterValueType.input.value

    @staticmethod
    def _get_assignments_to_concatenate(obj: _ParameterAssignment, pipeline_parameters=None):
        """Convert the _ParameterAssignment to graph type ParameterAssignment."""
        if not isinstance(obj, _ParameterAssignment):
            return None
        obj = obj.flatten()
        # part will be LITERAL/PIPELINE PARAMETER
        return [ParameterAssignment(value=part.str, value_type=part.type) for part in obj.assignments]

    @staticmethod
    def _resolve_parameter_value_and_type(
            parameter_value, pipeline_parameters=None):
        """Return the parameter value, value_type and assignment if there has one."""
        value = parameter_value
        value_type = _GraphEntityBuilder.LITERAL
        assignments = None
        pipeline_parameters = {} if pipeline_parameters is None else pipeline_parameters
        # Note that here the value is name if is pipeline parameter
        # so don't use _get_parameter_static_value here
        if isinstance(value, Input):
            value = value._get_internal_data_source()
        if isinstance(value, _ParameterAssignment):
            value_type = _GraphEntityBuilder.CONCATENATE
            # Get the resolved value if is _ParameterAssignment
            assignments = _GraphEntityBuilder._get_assignments_to_concatenate(value, pipeline_parameters)
            value = value.value
        elif isinstance(value, PipelineParameter):
            pipeline_param_name = value._full_name
            if pipeline_param_name in pipeline_parameters:
                value_type = _GraphEntityBuilder.GRAPH_PARAMETER_NAME
                # Link the pipeline parameter name if is pipeline parameter
                value = pipeline_param_name
            else:
                value = value.default_value
        return value, value_type, assignments

    @staticmethod
    def _resolve_runsetting_parameter_assignment(
            runsetting_def, runsetting_value, component,
            linked_parameter_name=None, pipeline_parameters=None, workspace=None):
        """Resolve the runsetting on component to RunsettingParameterAssignment."""
        is_compute_target = runsetting_def.is_compute_target
        resolved_value, value_type, assignments = \
            _GraphEntityBuilder._resolve_parameter_value_and_type(runsetting_value, pipeline_parameters)

        if is_compute_target:
            # If compute is inherit from pipeline then use_pipeline_default_compute is True.
            compute_name, compute_type, use_pipeline_default_compute = component._resolve_compute(
                pipeline_parameters=pipeline_parameters, workspace=workspace)
            if use_pipeline_default_compute:
                compute_name = None
                compute_type = None
            resolved_value = compute_name if value_type == _GraphEntityBuilder.LITERAL else resolved_value
            return RunSettingParameterAssignment(
                name=runsetting_def.name, value=resolved_value, value_type=value_type,
                use_graph_default_compute=use_pipeline_default_compute, mlc_compute_type=compute_type,
                assignments_to_concatenate=assignments, linked_parameter_name=linked_parameter_name)
        else:
            # If there are pipeline parameter or assignments, we just resolve the real value for validation
            # And it has no effect because we set the correct value_type.
            return RunSettingParameterAssignment(
                name=runsetting_def.name, value=resolved_value, value_type=value_type,
                assignments_to_concatenate=assignments, linked_parameter_name=linked_parameter_name)

    def _batch_append_module_node_pipeline_parameters(self, module_node: GraphModuleNode, params):
        for k, v in params.items():
            param_assignment = ParameterAssignment(name=k, value=v, value_type=self.GRAPH_PARAMETER_NAME)
            module_node.module_parameters.append(param_assignment)

    def _batch_append_module_node_parameter(self, module_node: GraphModuleNode, params):
        for k, v in params.items():
            # Set value type as INPUT and value == name if output as parameter.
            param_assignment = ParameterAssignment(name=k, value=k, value_type=self.INPUT) \
                if isinstance(v, Output) else ParameterAssignment(name=k, value=v, value_type=self.LITERAL)
            module_node.module_parameters.append(param_assignment)

    def _batch_append_module_node_assignment_parameters(
            self, module_node: GraphModuleNode, params: dict, pipeline_parameters: dict):
        """
        Resolve _ParameterAssignment as multiple parameter assignment.

        :param module_node: the module node on graph.
        :type module_node: GraphModuleNode
        :param params: key is param name and value is _StrParameterAssignment.
        :type params: dict[str, _ParameterAssignment]
        :param pipeline_parameters: use pipeline_parameters from user input to update concatenate value.
        :type pipeline_parameters: dict[str, Any]
        """
        for k, v in params.items():
            flattened_v = v.flatten()
            assignments_to_concatenate = \
                _GraphEntityBuilder._get_assignments_to_concatenate(flattened_v, pipeline_parameters)
            param_assignment = ParameterAssignment(
                name=k, value=None,
                value_type=self.CONCATENATE, assignments_to_concatenate=assignments_to_concatenate)
            module_node.module_parameters.append(param_assignment)

    def _append_module_meta_parameter(self, module_node: GraphModuleNode, param_name, param_value):
        param_assignment = ParameterAssignment(name=param_name, value=param_value, value_type=self.LITERAL)
        module_node.module_metadata_parameters.append(param_assignment)

    def _build_graph_datasource_node(self, input: Input) -> GraphDatasetNode:
        input = input._get_internal_data_source()  # Get the actual input
        dataset_def = None
        dataset_id = None

        if isinstance(input, DatasetConsumptionConfig):
            input = input.dataset  # Get the AbstractDataset instance

        if isinstance(input, (AbstractDataset, _GlobalDataset, DataReference)):
            if isinstance(input, AbstractDataset):  # Make sure this dataset is saved.
                _ensure_dataset_saved_in_workspace(input, self._context.workspace)

            dataset_def = _get_dataset_def_from_dataset(input)

        if isinstance(input, PipelineParameter):
            dataset_def = DataSetDefinition(data_type_short_name=DATAFRAMEDIRECTORY,
                                            parameter_name=input.name)

        if isinstance(input, str) or isinstance(input, Path):
            dataset_def = DataSetDefinition(data_type_short_name=DATAFRAMEDIRECTORY,
                                            value=str(input))

        if isinstance(input, _FeedDataset):
            dataset_id = input.arm_id

        if dataset_def is None and dataset_id is None:
            raise NotImplementedError("Unrecognized data source type: %r" % type(input))

        identifier = str(dataset_def.as_dict()) if dataset_def is not None else dataset_id
        node_id = self._generate_node_id(identifier)

        return GraphDatasetNode(id=node_id, dataset_id=dataset_id, data_set_definition=dataset_def)

    @staticmethod
    def _extract_mlc_compute_type(target_type):
        if target_type == AmlCompute._compute_type or target_type == RemoteCompute._compute_type or \
                target_type == HDInsightCompute._compute_type or target_type == ComputeInstance._compute_type:
            if target_type == AmlCompute._compute_type:
                return 'AmlCompute'
            elif target_type == ComputeInstance._compute_type:
                return 'ComputeInstance'
            elif target_type == HDInsightCompute._compute_type:
                return 'Hdi'
        return None

    def _generate_node_id(self, identifier=None) -> str:
        """
        Generate a random 8-character node Id if identifier is None, else generate md5 of the identifier as node Id.

        :param: identifier: identifier used to generate node Id
        :type: identifier: str
        :return: node_id
        :rtype: str
        """
        if identifier is not None:
            s = bytes(identifier, 'utf8')
            return hashlib.md5(s).hexdigest()
        else:
            guid = str(uuid.uuid4())
            return guid[:8]


def _assert_graph_json_equal(graph_json1, graph_json2):
    """Compare graph json in same workspace."""
    def standardized_node(graph_json):
        """Standardized node id in graph json."""
        graph = json.loads(graph_json)
        # Map old node id to new
        node_id_dict = {}
        # Record the module id and instance count
        module_count = {}
        # 1. dataset_nodes - Format and update dataset node id as dataset_{number}
        for idx, node in enumerate(graph['dataset_nodes']):
            node_id = node['id']
            new_node_id = f'dataset_{idx}'
            node_id_dict[node_id] = new_node_id
            node['id'] = new_node_id
        # 2. module_nodes - Format and update module node id as {moduleid}_{number}
        # Format and update module node name as node id
        nodes = graph['module_nodes']
        if 'sub_graph_nodes' in graph:
            nodes += graph['sub_graph_nodes']
        for node in nodes:
            node_id = node['id']
            module_id = node['module_id']
            if module_id not in module_count:
                module_count[module_id] = 0
            module_count[module_id] += 1
            new_node_id = f'{module_id}_{module_count[module_id]}'
            node_id_dict[node_id] = new_node_id
            node['id'] = new_node_id
            node['name'] = new_node_id
        # 3. edges - Update node id in edge
        for edge in graph['edges']:
            if edge['destination_input_port'].get('node_id', None) is not None:
                edge['destination_input_port']['node_id'] = node_id_dict[edge['destination_input_port']['node_id']]
            if edge['source_output_port'].get('node_id', None) is not None:
                edge['source_output_port']['node_id'] = node_id_dict[edge['source_output_port']['node_id']]
        # 4. module_node_runsettings - Update node id in module_node_runsettings
        for setting in graph['module_node_run_settings']:
            setting['node_id'] = node_id_dict[setting['node_id']]
            # 5. sort runsettings
            setting['run_settings'].sort(key=lambda item: item['name'])
            for run_setting in setting['run_settings']:
                if run_setting['compute_run_settings'] is not None:
                    run_setting['compute_run_settings'].sort(key=lambda item: item['name'])
        return json.dumps(graph)

    graph_json1 = standardized_node(graph_json1)
    graph_json2 = standardized_node(graph_json2)
    return graph_json1 == graph_json2


def _int_str_to_run_setting_ui_widget_type_enum(int_str_value):
    return list(RunSettingUIWidgetTypeEnum)[int(int_str_value)]


def _populate_submission_runsettings(component, pipeline_parameters=None, workspace=None):
    pipeline_parameters = {} if pipeline_parameters is None else pipeline_parameters
    runsettings_values = component._runsettings._get_flat_values()
    runsettings_definition = component._definition.runsettings
    runsettings = []
    # Search space params
    if component.type in [ComponentType.SweepComponent.value, ComponentType.CommandComponent.value]:
        search_space_params = _populate_sweep_search_space_runsettings(
            component, runsettings_definition, runsettings_values, pipeline_parameters)
        runsettings.extend(search_space_params)
    compute_target_param = None
    use_pipeline_default_compute = True

    # RunSettings params
    # When local run the workspace independent component, runsettings_definition will be None.
    runsettings_params = runsettings_definition.params if runsettings_definition else {}
    for name, p in runsettings_params.items():
        value = runsettings_values.get(p.id)
        # Always add compute settings
        # Since module may use default compute, we don't have to detect this, MT will handle
        if p.is_compute_target:
            compute_value = value if value is not None else p.default_value
            compute_target_param = _GraphEntityBuilder._resolve_runsetting_parameter_assignment(
                p, compute_value, component, pipeline_parameters=pipeline_parameters,
                workspace=workspace)
            use_pipeline_default_compute = compute_target_param.use_graph_default_compute
            runsettings.append(compute_target_param)
            continue
        if value is None:
            continue
        runsetting_param = _GraphEntityBuilder._resolve_runsetting_parameter_assignment(
            p, runsettings_values.get(p.id), component, pipeline_parameters=pipeline_parameters)
        runsettings.append(runsetting_param)

    # Compute runsettings
    if compute_target_param is not None and len(runsettings_definition.compute_params) > 0:
        compute_runsettings_values = component._k8srunsettings._get_flat_values()
        compute_settings = []
        for p in runsettings_definition.compute_params.values():
            value = compute_runsettings_values.get(p.id)
            if value is None:
                continue
            compute_param = _GraphEntityBuilder._resolve_runsetting_parameter_assignment(
                p, value, component, pipeline_parameters=pipeline_parameters)
            compute_settings.append(compute_param)
        compute_target_param.compute_run_settings = compute_settings
    return runsettings, use_pipeline_default_compute


def _populate_sweep_search_space_runsettings(
        component, runsettings_definition, runsettings_values, pipeline_parameters=None):
    algorithm = component._definition.runsettings.algorithm
    search_space_params = []
    if algorithm is None:
        return search_space_params

    # Get linked parameters
    linked_params = algorithm.linked_parameters.keys() if algorithm.linked_parameters else None
    # Get user inputs
    input_values = {
        k: v for k, v in component._parameter_params.items() if
        (component.type == ComponentType.SweepComponent.value and k in linked_params and v is not None) or
        (component.type == ComponentType.CommandComponent.value and is_hyper_parameter(v))
    }
    # get user provided inputs
    user_provided_linked_params = input_values.keys()
    algorithm_value = runsettings_values.get(algorithm.id, None)
    # For handling corner case: user doesn't set the value to the algorithm through runsettings but uses the default,
    # and sets search space params in the component's inputs. We need to get the default algorithm.
    # E.g. component = sweep_func(learning_rate=choice([0.2, 0.3]))
    if algorithm_value is None and any(input_values.values()):
        algorithm_value = algorithm.default_value

    def _parse_input_values_by_type(val):
        """Resolve and update input values by value type."""
        # Supported search-space input
        # 1. sweep_func(learning_rate=choice([0.02, 0.05]))
        # 2. sweep_func(learning_rate=0.05)
        # 3. class Rate(Enum):
        #       rate1 = 0.02
        #    sweep_func(learning_rate = Rate.rate1)
        if val is None:
            return {}
        elif isinstance(val, list):
            # This section is used for parsing input contract hyperparameter expressions from
            # azureml.train.hyperdrive Logic & assumption: for now, we don't support/have list type input,
            # therefore, we use isinstance(input, list) to predicate that the input is a
            # sweep-contract-hyperparameter-contract expression. Attention, if we support list-type parameters,
            # this logic must be changed.
            return SweepComponentDefinition.parse_hyperparameter_expression(val)
        elif _is_supported_sweep_search_space_value(val):
            # convert single value to choice type
            _get_logger().warning(
                "Single value passed to search space parameter '{}', converted it to choice type.".format(p))
            return SweepComponentDefinition.parse_hyperparameter_expression(['choice', [[val]]])
        elif isinstance(val, dict):
            return val
        else:
            # if input_values[p] is not a dict, ignore for now, leave a todo here
            # TODO: validate the type and value of input_values[p] in component.validate
            _get_logger().warning("Parameter '%s' type mismatch. Required 'dict', " % p +
                                  "got '%s'. Will use default value." % type(val).__name__)
            return {}

    # Refine user inputs
    for p in user_provided_linked_params:
        input_values[p] = _parse_input_values_by_type(input_values[p])
    # Process type, use literal type value for validation
    algorithm_literal_value = _get_parameter_static_value(algorithm_value, pipeline_parameters)
    type_spec = next(
        (p.enabled_by[algorithm.name][algorithm_literal_value]
         for p in runsettings_definition.search_space_params.values() if p.argument_name == 'type' and
         algorithm.name in p.enabled_by and algorithm_literal_value in p.enabled_by[algorithm.name]), None)
    if type_spec is None:
        return search_space_params

    # Add type parameter and get params enabled by type for each linked parameter
    for linked_p_name in user_provided_linked_params:
        linked_p_value = input_values.get(linked_p_name)
        if linked_p_value is None:
            # TODO: raise exception here?
            continue
        type_input_value = linked_p_value.get(type_spec.argument_name)
        type_literal_value = _get_parameter_static_value(type_input_value)
        if type_literal_value is None or type_literal_value not in type_spec.enum:
            # Try to validate the type value, if not valid, ignore it
            # TODO: put it in component.validation? and throw exception when invalid?
            continue
        if type_literal_value == 'choice':
            if isinstance(linked_p_value.get('values'), range):
                linked_p_value['values'] = list(linked_p_value['values'])
        # Add type value to submission runsettings
        runsetting_param = _GraphEntityBuilder._resolve_runsetting_parameter_assignment(
            type_spec, type_input_value, component, linked_p_name, pipeline_parameters)
        search_space_params.append(runsetting_param)
        # Append params enabled by type
        params_by_type = [
            p for p in runsettings_definition.search_space_params.values()
            if type_spec.name in p.enabled_by and type_literal_value in p.enabled_by[type_spec.name]]
        for p in params_by_type:
            search_space_param = _GraphEntityBuilder._resolve_runsetting_parameter_assignment(
                p.definition, linked_p_value.get(p.argument_name), component, linked_p_name, pipeline_parameters)
            search_space_params.append(search_space_param)
    return search_space_params


def _is_supported_sweep_search_space_value(value):
    if type(value) in [int, float, str] or isinstance(value, Enum):
        return True
    return False


def _is_sweep_conditional_hyperparameter(values):
    for model in values:
        if not isinstance(model, dict):
            # if values are not with dict type, they are not models
            return False
        for k in model:
            if isinstance(model[k], list):
                return True
    return False
