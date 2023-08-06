# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from azureml.data._dataset import AbstractDataset
from azureml.data.data_reference import DataReference
from azure.ml.component import Component, Pipeline

from .component import Output, Input
from ._parameter_assignment import _ParameterAssignment
from ._pipeline_parameters import PipelineParameter

from ._restclients.designer.models import ComputeSetting, DatastoreSetting,\
    SubPipelinesInfo, SubPipelineDefinition, Kwarg, SubPipelineParameterAssignment,\
    Parameter, SubGraphParameterAssignment, DataPathParameter, SubGraphDataPathParameterAssignment,\
    SubGraphConnectionInfo, SubGraphPortInfo, SubGraphInfo, ParameterAssignment, SubGraphConcatenateAssignment

from ._util._utils import _get_data_info_hash_id, _get_dataset_def_from_dataset


class SubPipelinesInfoBuilder(object):
    """Helper to build sub pipelines info from pipeline component.
    """
    def __init__(self, pipeline, module_node_to_graph_node_mapping, pipeline_parameters, workspace=None):
        self.pipeline = pipeline
        self.module_nodes = pipeline._expand_pipeline_nodes()
        self.pipelines = pipeline._expand_pipeline_to_pipelines()
        self.input_to_data_info_dict = pipeline._build_input_to_data_info_dict(pipeline.nodes,
                                                                               pipeline_parameters)
        self.module_node_to_graph_node_mapping = module_node_to_graph_node_mapping
        self.pipeline_parameters = pipeline_parameters
        self.workspace = workspace

    def build(self):
        # pipeline definitions
        definitions = []
        for p in self.pipelines:
            if p._pipeline_definition not in definitions:
                definitions.append(p._pipeline_definition)

        node_id_2_graph_id = {}

        for node in self.module_nodes:
            step_id = self.module_node_to_graph_node_mapping[node._get_instance_id()]
            node_id_2_graph_id[step_id] = node._parent._id

        # sub graph infos
        sub_graph_infos = [self._get_sub_graph_info(p) for p in self.pipelines]

        return SubPipelinesInfo(sub_graph_info=sub_graph_infos,
                                node_id_to_sub_graph_id_mapping=node_id_2_graph_id,
                                sub_pipeline_definition=definitions)

    def _get_sub_graph_info(self, pipeline):
        def _is_default_compute_node(node):
            if isinstance(node, Component) and not isinstance(node, Pipeline):
                return node.runsettings is None or \
                    not hasattr(node.runsettings, 'target') or \
                    node.runsettings.target is None
            return False

        def _is_default_datastore_node(node, default_datastore):
            if isinstance(node, Component) and not isinstance(node, Pipeline):
                non_default_datastore_output = next((output for output in node.outputs.values()
                                                    if output.datastore != default_datastore), None)
                return non_default_datastore_output is None
            return False

        workspace = self.workspace or pipeline.workspace
        compute = _get_compute_setting(pipeline._get_default_compute_target(workspace=workspace)[0])
        datastore = _get_data_store_setting(pipeline._resolve_default_datastore(workspace=workspace))

        sub_graph_default_compute_target_nodes = [_get_graph_node_id(node, self.module_node_to_graph_node_mapping)
                                                  for node in pipeline.nodes
                                                  if _is_default_compute_node(node)]

        sub_graph_default_data_store_nodes = [_get_graph_node_id(node, self.module_node_to_graph_node_mapping)
                                              for node in pipeline.nodes
                                              if _is_default_datastore_node(node, pipeline._default_datastore)]

        sub_graph_parameter_assignment, sub_graph_concatenate_assignment = self._get_parameter_assignments(pipeline)
        sub_graph_data_path_parameter_assignment = self._get_data_parameter_assignments(pipeline)

        sub_graph_input_ports = self._build_sub_graph_input_ports(pipeline)
        sub_graph_output_ports = self._build_sub_graph_output_ports(pipeline)

        sub_graph_info = SubGraphInfo(
            name=pipeline.name, description=pipeline.description,
            default_compute_target=compute, default_data_store=datastore,
            id=pipeline._id, parent_graph_id=pipeline._parent._id if pipeline._parent else None,
            pipeline_definition_id=pipeline._pipeline_definition.id,
            sub_graph_parameter_assignment=sub_graph_parameter_assignment,
            sub_graph_concatenate_assignment=sub_graph_concatenate_assignment,
            sub_graph_data_path_parameter_assignment=sub_graph_data_path_parameter_assignment,
            sub_graph_default_compute_target_nodes=sub_graph_default_compute_target_nodes,
            sub_graph_default_data_store_nodes=sub_graph_default_data_store_nodes,
            inputs=sub_graph_input_ports,
            outputs=sub_graph_output_ports)
        # TODO: Move comment into init after SMT supported.
        sub_graph_info.comment = pipeline.comment

        return sub_graph_info

    def _get_parameter_assignments(self, pipeline):
        parameter_assignments = []
        assignments_to_concatenate = []
        parameter_assignments_mapping = {}
        for p in pipeline._pipeline_definition.parameter_list:
            parameter_assignments_mapping[p.key] = []

        def get_parent_parameter_name(node, para_v):
            # for sub pipeline, it should be a PipelineParameter wrapped with _InputBuilder
            if isinstance(para_v, Input) or isinstance(para_v, PipelineParameter):
                return para_v.name
            else:
                return None

        def get_param_name(dset):
            if isinstance(dset, DataReference):
                return dset.data_reference_name
            else:
                return dset.name

        def try_to_add_assignments(assignments_mapping, parent_param_name, node_id, para_name):
            if parent_param_name in assignments_mapping.keys():
                assignments = assignments_mapping[parent_param_name]
                assignments.append(
                    SubPipelineParameterAssignment(node_id=node_id,
                                                   parameter_name=para_name))

        def try_to_add_assignments_concatenate(node_id, para_name, assignments_obj):
            """Add node assignments concatenate info."""
            parameter = SubPipelineParameterAssignment(node_id=node_id,
                                                       parameter_name=para_name)

            def get_assignments_to_concatenate(obj: _ParameterAssignment):
                assignments = []
                for part in obj.assignments:
                    if part.type in [_ParameterAssignment.LITERAL, _ParameterAssignment.PIPELINE_PARAMETER]:
                        assignments.append(ParameterAssignment(value=part.str, value_type=part.type))
                    else:
                        # If part is CONCATENATE type, value may be:
                        # 1. Input: it is assignment from parent pipeline, convert type to pipeline parameter.
                        # 2. ParameterAssignment: it is build inside current pipeline, flatten it.
                        sub_obj = assignments_obj.assignments_values_dict[part.str]
                        if isinstance(sub_obj, Input):
                            assignments.append(ParameterAssignment(
                                value=sub_obj.name, value_type=_ParameterAssignment.PIPELINE_PARAMETER))
                        else:
                            assignments.extend(get_assignments_to_concatenate(sub_obj))
                return assignments

            concatenate_parameter = get_assignments_to_concatenate(assignments_obj)
            assignments_to_concatenate.append(SubGraphConcatenateAssignment(
                parameter_assignments=parameter,
                concatenate_parameter=concatenate_parameter
            ))

        for node in pipeline.nodes:
            node_id = _get_graph_node_id(node, self.module_node_to_graph_node_mapping)
            for input_name, input_value in node._input_ports.items():
                if isinstance(input_value._dset, (Input, PipelineParameter)):
                    try_to_add_assignments(
                        assignments_mapping=parameter_assignments_mapping,
                        parent_param_name=get_param_name(input_value._dset)
                        if input_value._dset is not None else input_name,
                        node_id=node_id,
                        para_name=input_name)

            for para_k, para_v in node._parameter_params.items():
                if isinstance(para_v, _ParameterAssignment):
                    try_to_add_assignments_concatenate(
                        node_id=node_id,
                        para_name=para_k,
                        assignments_obj=para_v)
                else:
                    try_to_add_assignments(assignments_mapping=parameter_assignments_mapping,
                                           parent_param_name=get_parent_parameter_name(node, para_v),
                                           node_id=node_id,
                                           para_name=para_k)

        for k in parameter_assignments_mapping.keys():
            if k in pipeline._parameter_params:
                exported_default_value = _get_parameter_exported_default_value(pipeline._parameter_params[k])
            else:
                # For data input, the key will not in _parameter_params, and it's default value will set to None
                # When exported to code, we can get the default value from inputs info.
                exported_default_value = None
            parameter = Parameter(name=k, default_value=exported_default_value)
            parameter_assignments.append(SubGraphParameterAssignment(
                parameter=parameter,
                parameter_assignments=parameter_assignments_mapping[k]))

        return parameter_assignments, assignments_to_concatenate

    def _get_data_parameter_assignments(self, pipeline):
        dataset_parameter_assignment = []

        for input_k, input_v in pipeline._input_ports.items():
            # dataset parameter assignment
            if isinstance(input_v, Input) and isinstance(input_v._dset, AbstractDataset):
                dataset_def = _get_dataset_def_from_dataset(input_v._dset)
                data_set_parameter = DataPathParameter(
                    name=input_k,
                    default_value=dataset_def.value,
                    is_optional=False,
                    data_type_id='DataFrameDirectory')
                dataset_parameter_assignment.append(SubGraphDataPathParameterAssignment(
                    data_set_path_parameter=data_set_parameter,
                    # currently, we don't need to know which node is assigned
                    data_set_path_parameter_assignments=[]))

        return dataset_parameter_assignment

    def _find_input_external_port(self, input_source, pipeline):
        # directly from data source node
        if input_source in self.input_to_data_info_dict.keys():
            node_id = _get_data_info_hash_id(self.input_to_data_info_dict[input_source])
            port_name = 'output'
            return [SubGraphConnectionInfo(port_name=port_name, node_id=node_id)]

        # from parent pipeline's input
        if isinstance(input_source, (Input, PipelineParameter)):
            node_id = pipeline._parent._id
            port_name = input_source.name
            return [SubGraphConnectionInfo(port_name=port_name, node_id=node_id)]

        # from brother node's output
        if isinstance(input_source, Output):
            from_node = next((n for n in pipeline._parent.nodes
                              if id(input_source) in map(id, n.outputs.values())), None)
            if isinstance(from_node, Pipeline):
                node_id = from_node._id
                port_name, port_value = next((o for o in from_node.outputs.items()
                                              if id(o[1]) == id(input_source)), None)
            else:
                node_id = self.module_node_to_graph_node_mapping[from_node._get_instance_id()]
                port_name = input_source.port_name
            return [SubGraphConnectionInfo(port_name=port_name, node_id=node_id)]

        return []

    def _find_input_internal_ports(self, input_name, pipeline):
        internals = []
        for node in pipeline.nodes:
            for input in node._input_ports.values():
                if not isinstance(input._dset, (PipelineParameter, Input)):
                    continue
                if input._dset.name == input_name:
                    node_id = _get_graph_node_id(node, self.module_node_to_graph_node_mapping)
                    port_name = _get_graph_port_name(node, input)
                    internals.append(SubGraphConnectionInfo(port_name=port_name, node_id=node_id))

        return internals

    def _find_output_external_ports(self, output_val, pipeline):
        externals = []

        if pipeline._parent is None:
            return externals

        # to parent pipeline's output ports
        for k, output in pipeline._parent.outputs.items():
            if id(output_val) == id(output):
                node_id = pipeline._parent._id
                port_name = k
                externals.append(SubGraphConnectionInfo(port_name=port_name, node_id=node_id))

        # to brother node's input
        for node in pipeline._parent.nodes:
            for input in node._input_ports.values():
                if id(output_val) == id(input._dset):
                    node_id = _get_graph_node_id(node, self.module_node_to_graph_node_mapping)
                    port_name = port_name = _get_graph_port_name(node, input)
                    externals.append(SubGraphConnectionInfo(port_name=port_name, node_id=node_id))

        return externals

    def _find_output_internal_port(self, output_val, pipeline):
        internals = []
        for node in pipeline.nodes:
            for k, output in node.outputs.items():
                if id(output_val) == id(output):
                    node_id = _get_graph_node_id(node, self.module_node_to_graph_node_mapping)
                    port_name = k if isinstance(node, Pipeline) else output.port_name
                    internals.append(SubGraphConnectionInfo(port_name=port_name, node_id=node_id))

        return internals

    def _build_sub_graph_input_ports(self, pipeline):
        if pipeline._parent is None:
            # don't need to build input ports for root pipeline
            return []

        input_ports = []
        for input_name, input_val in pipeline._input_ports.items():
            externals = self._find_input_external_port(input_val._dset, pipeline)
            internals = self._find_input_internal_ports(input_name, pipeline)
            input_ports.append(SubGraphPortInfo(name=input_name, internal=internals, external=externals))

        return input_ports

    def _build_sub_graph_output_ports(self, pipeline):
        if pipeline._parent is None:
            # don't need to build input ports for root pipeline
            return []

        output_ports = []
        for output_name, output_val in pipeline.outputs.items():
            externals = self._find_output_external_ports(output_val, pipeline)
            internals = self._find_output_internal_port(output_val, pipeline)
            output_ports.append(SubGraphPortInfo(name=output_name, internal=internals, external=externals))

        return output_ports


# region helper_functions
def _get_compute_setting(default_compute_target):
    if default_compute_target is None:
        return None
    elif isinstance(default_compute_target, str):
        return ComputeSetting(name=default_compute_target)
    elif isinstance(default_compute_target, tuple):
        if len(default_compute_target) == 2:
            return ComputeSetting(name=default_compute_target[0])
            # TODO: how to set proper compute_type
            # compute_type=default_compute_target[1])
    else:
        return ComputeSetting(name=default_compute_target.name)
        # compute_type=default_compute_target.type)


def _get_data_store_setting(default_data_store):
    from azureml.data.abstract_datastore import AbstractDatastore
    if isinstance(default_data_store, str):
        return DatastoreSetting(data_store_name=default_data_store)
    elif isinstance(default_data_store, AbstractDatastore):
        return DatastoreSetting(data_store_name=default_data_store.name)
    else:
        return None


def _normalize_from_module_name(from_module_name):
    """Return the bottom module file name.

    If from_module_name = 'some_module', return 'some_module'
    If from_module_name = 'some_module.sub_module', return 'sub_module'
    """
    if from_module_name is None:
        return None

    try:
        import re
        entries = re.split(r'[.]', from_module_name)
        return entries[-1]
    except Exception:
        return None


def _build_sub_pipeline_definition(name, description,
                                   default_compute_target, default_data_store,
                                   id, parent_definition_id=None,
                                   from_module_name=None, parameters=None, func_name=None):
    def parameter_to_kv(parameter):
        return Kwarg(
            key=parameter.name,
            value=_get_parameter_exported_default_value(parameter._default))

    compute_target = _get_compute_setting(default_compute_target)
    data_store = _get_data_store_setting(default_data_store)
    parameter_list = [] if parameters is None else [parameter_to_kv(p) for p in parameters]

    return SubPipelineDefinition(name=name, description=description,
                                 default_compute_target=compute_target, default_data_store=data_store,
                                 pipeline_function_name=func_name,
                                 id=id, parent_definition_id=parent_definition_id,
                                 from_module_name=_normalize_from_module_name(from_module_name),
                                 parameter_list=parameter_list)


def _get_graph_node_id(node, module_node_to_graph_node_mapping):
    if isinstance(node, Pipeline):
        return node._id
    else:
        return module_node_to_graph_node_mapping[node._get_instance_id()]


def _get_graph_port_name(node, input):
    if isinstance(node, Pipeline):
        return input.name
    else:
        return node._pythonic_name_to_input_map[input.name]


def _get_parameter_exported_default_value(v):
    """
    Get the representation of parameter's default value that used in exported code.
    """
    if isinstance(v, int) or isinstance(v, bool) or isinstance(v, float):
        # use the value directly
        return v
    elif isinstance(v, str):
        # wrap with '
        return '\'{}\''.format(v)
    elif isinstance(v, PipelineParameter):
        # use pipeline parameter's name
        return v.name
    elif isinstance(v, Input):
        # use component input's name
        return v.name
    elif isinstance(v, _ParameterAssignment):
        # format concatenate_parameter
        return v._get_code_str()
    else:
        return None
# endregion
