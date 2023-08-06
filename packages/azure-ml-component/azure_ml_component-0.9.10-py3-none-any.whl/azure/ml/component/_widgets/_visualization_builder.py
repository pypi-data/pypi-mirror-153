# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import Dict, List
from azure.ml.component._util._utils import _unique


class _Port(object):
    """
    Defines the construct of input source used to build visualization dict.
    """
    def __init__(self, node_id: str, port_name: str=None, graph_port_name: str=None):
        self.node_id = node_id
        self.port_name = port_name
        self.graph_port_name = graph_port_name

    def __str__(self):
        if self.port_name is not None:
            return '{}_{}'.format(self.node_id, self.port_name)
        elif self.graph_port_name is not None:
            return self.graph_port_name
        else:
            return self.node_id

    def __iter__(self):
        for attr, value in self.__dict__.items():
            if value is not None:
                yield attr, value


class _ComponentDef(object):
    """
    Defines the contract for module's definition used to build visualization dict.
    """
    def __init__(self, identifier: str, name: str, display_name: str, version: str, description: str=None,
                 inputs: List[Dict]=[], outputs: List[Dict]=[], type: str=None):
        self.identifier = identifier
        self.name = name
        self.version = version
        self.description = description
        self.inputs = inputs
        self.outputs = outputs
        self.display_name = display_name
        self.type = type

    def to_dict(self):
        entity = {
            'name': self.name,
            'display_name': self.display_name,
            'module_id': self.identifier,
            'version': self.version,
            'description': self.description,
            'type': self.type,
            'structured_interface': {
                'inputs': self.inputs,
                'outputs': self.outputs,
            }
        }
        return entity

    @classmethod
    def get_module_identifier(cls, module: '_ComponentDef'):
        return module.identifier


class _DataNode(object):
    """
    Defines the contract for data source used to build visualization dict.
    """
    def __init__(self, name: str, node_id: str, data_id: str,
                 description: str=None, mode: str=None,
                 path_on_datastore: str=None, datastore: str=None,
                 version: str=None, reg_id: str=None, saved_id: str=None):
        self.name = name
        self.path_on_datastore = path_on_datastore
        self.datastore = datastore
        self.mode = mode
        self.description = description
        self.version = version
        self.dataset_id = reg_id if reg_id is not None else name
        self.registered_id = reg_id if reg_id is not None else name
        self.saved_id = saved_id
        self.node_id = node_id
        # used for data source
        self.nodeId = data_id

    def _get_not_none_dict(self, attrs):
        result = {}
        for attr, value in self.__dict__.items():
            if attr in attrs and value is not None:
                result[attr] = value
        return result

    def to_data_ref_dict(self):
        data_ref_attrs = [
            'name',
            'mode',
            'saved_id',
            'dataset_id',
            'datastore',
            'path_on_datastore'
        ]
        return self._get_not_none_dict(data_ref_attrs)

    def _to_data_source_dict(self):
        data_source_attrs = [
            'name',
            'datastore',
            'path_on_datastore',
            'description',
            'version',
            'registered_id',
            'saved_id',
            'nodeId'
        ]
        return self._get_not_none_dict(data_source_attrs)

    @classmethod
    def get_data_identifier(cls, data):
        return data.nodeId + data.node_id


class _Component(object):
    """
    Defines the contract for steps used to build visualization dict.
    """
    def __init__(self, id, inputs: Dict[str, _Port], outputs: Dict[str, _Port],
                 parameters: Dict[str, str], module_identifier: str, validation_info: List[str] = [],
                 name: str = None, comment: str = None, created_by: str = None, compute: str = None,
                 compute_url: str = None, graph_id: str = None, component_name: str = None):
        self.id = id
        self.name = name
        self.inputs = inputs
        self.outputs = outputs
        self.parameters = parameters
        self.module_identifier = module_identifier
        self.validation_info = validation_info
        self.comment = comment
        self.created_by = created_by
        self.compute = compute
        self.compute_url = compute_url
        self.graph_id = graph_id
        # store component name used for error message for pipeline validation
        self.component_name = component_name

    def add_input_port(self, name, input_port: _Port):
        if self.inputs is None:
            self.inputs = {}
        self.inputs.update({name: input_port})

    def add_output_port(self, name, output_port: _Port):
        if self.outputs is None:
            self.outputs = {}
        self.outputs.update({name: output_port})


class _SubGraphPort(object):
    """
    Defines the contract for a subgraph's port used to build visualization dict.
    """
    def __init__(self, name, internal: List[_Port], external: List[_Port]):
        self.name = name
        self.internal = internal
        self.external = external

    def to_dict(self):
        return {
            'name': self.name,
            'internal': [dict(i) for i in self.internal],
            'external': [dict(e) for e in self.external]
        }


class _SubGraph(object):
    """
    Defines the contract for sub pipelines info used to build visualization dict.
    """
    def __init__(self, id, name, parent_graph_id,
                 inputs: List[_SubGraphPort], outputs: List[_SubGraphPort], comment: str = None):
        self.id = id
        self.name = name
        self.parent_graph_id = parent_graph_id
        self.inputs = inputs
        self.outputs = outputs
        self.comment = comment

    def to_dict(self):
        return {
            'name': self.name,
            'id': self.id,
            'parent_graph_id': self.parent_graph_id,
            'inputs': [i.to_dict() for i in self.inputs],
            'outputs': [o.to_dict() for o in self.outputs],
            'comment': self.comment
        }


class _SubPipelinesInfo(object):
    """
    Defines the contract for sub pipelines info used to build visualization dict.
    """
    def __init__(self, sub_graphs: List[_SubGraph], node_id_to_sub_graph_id: Dict[str, str]):
        self.sub_graphs = sub_graphs
        self.node_id_to_sub_graph_id = node_id_to_sub_graph_id


class VisualizationBuilder(object):
    """
    The builder that constructs visualization info from `designer.models.GraphDraftEntity`.
    """

    def __init__(self, step_nodes: List[_Component], module_defs: List[_ComponentDef],
                 data_nodes: List[_DataNode] =[], sub_pipelines_info: _SubPipelinesInfo=None):
        self._step_nodes = step_nodes
        self._module_defs = _unique(module_defs, _ComponentDef.get_module_identifier)
        self._data_nodes = _unique(data_nodes, _DataNode.get_data_identifier)
        self._sub_pipelines_info = sub_pipelines_info

    def _validate_sub_pipelines_info(self, all_node_ids):
        # validate sub graph info
        # check all the module node id and data node id are in pre-built all_node_ids
        def valid_node_id(node_id, all_sub_graph_ids):
            return node_id in all_sub_graph_ids or node_id in all_node_ids

        if self._sub_pipelines_info is not None:
            if self._sub_pipelines_info.node_id_to_sub_graph_id is None:
                return None
            else:
                for node in self._sub_pipelines_info.node_id_to_sub_graph_id.keys():
                    if node not in all_node_ids:
                        return None
            if self._sub_pipelines_info.sub_graphs is None:
                return None
            else:
                all_sub_graph_ids = [sub.id for sub in self._sub_pipelines_info.sub_graphs]
                for sub_graph in self._sub_pipelines_info.sub_graphs:
                    for input in sub_graph.inputs:
                        for internal in input.internal:
                            if not valid_node_id(internal.node_id, all_sub_graph_ids):
                                return None
                        for external in input.external:
                            if not valid_node_id(external.node_id, all_sub_graph_ids):
                                return None
                    for output in sub_graph.outputs:
                        for internal in output.internal:
                            if not valid_node_id(internal.node_id, all_sub_graph_ids):
                                return None
                        for external in output.external:
                            if not valid_node_id(external.node_id, all_sub_graph_ids):
                                return None

        return self._sub_pipelines_info

    def build_visualization_dict(self):
        # build data references and data sources
        data_references_dict = {}
        data_sources = []
        all_node_ids = []
        for node in self._data_nodes:
            # data ref
            if node.node_id not in data_references_dict.keys():
                data_references_dict[node.node_id] = node.to_data_ref_dict()

                # data source
                # we will merge different data node with same underlying data source,
                # so in the final visualization dict, the data id is used as data node id
                if node.nodeId not in all_node_ids:
                    data_sources.append(node._to_data_source_dict())
                    all_node_ids.append(node.nodeId)

        # build steps
        steps = {}
        for node in self._step_nodes:
            module_def = next((d for d in self._module_defs
                               if d.identifier == node.module_identifier), None)
            assert module_def is not None, 'no module definition found for node {}'.format(node.id)

            inputs = {}
            for i_k, i_v in node.inputs.items():
                data_node = next((node for node in self._data_nodes if node.node_id == i_v.node_id), None)
                if data_node is None:
                    inputs[i_k] = {'source': str(i_v)}
                else:
                    inputs[i_k] = {'source': i_v.node_id}

                if i_v.graph_port_name is not None:
                    inputs[i_k].update({'graph_port': i_v.graph_port_name})

            outputs = {}
            for o_k, o_v in node.outputs.items():
                outputs[o_k] = {'destination': str(o_v)}
                if o_v.graph_port_name is not None:
                    outputs[o_k].update({'graph_port': o_v.graph_port_name})

            module_dict = {'id': module_def.identifier, 'version': module_def.version}

            validate_dict = {
                'error': [{'message': error.descriptor.message, 'type': error.descriptor.type}
                          for error in node.validation_info],
            }

            steps[node.id] = {
                'node_name': node.name,
                'inputs': inputs,
                'outputs': outputs,
                'module': module_dict,
                'parameters': node.parameters,
                'validate': validate_dict,
                'comment': node.comment,
                'created_by': node.created_by,
                'compute': node.compute,
                'compute_url': node.compute_url,
                'sub_graph_id': node.graph_id,
            }

            all_node_ids.append(node.id)

        # build modules
        modules = [d.to_dict() for d in self._module_defs]

        root_pipeline_name = 'parent graph'

        # validate sub pipelines info
        sub_pipelines_info = self._validate_sub_pipelines_info(all_node_ids)
        sub_pipelines_info_dict = {}
        if sub_pipelines_info is not None:
            root_graph = next((p for p in sub_pipelines_info.sub_graphs if p.parent_graph_id is None), None)
            if root_graph is not None and root_graph.name is not None:
                root_pipeline_name = root_graph.name
            sub_pipelines_info_dict['subGraphInfo'] = [s.to_dict() for s in sub_pipelines_info.sub_graphs]
            sub_pipelines_info_dict['nodeIdToSubGraphIdMapping'] = sub_pipelines_info.node_id_to_sub_graph_id

        result = {"pipeline": {"name": root_pipeline_name,
                               "data_references": data_references_dict,
                               "steps": steps},
                  "modules": list(modules),
                  "datasources": list(data_sources)}
        result.update(sub_pipelines_info_dict)

        return result
