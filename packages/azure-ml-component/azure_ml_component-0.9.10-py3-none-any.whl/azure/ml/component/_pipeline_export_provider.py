# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import os
from abc import ABC, abstractmethod

from typing import Union

from azureml.data._dataset import AbstractDataset
from azureml.data.dataset_consumption_config import DatasetConsumptionConfig
from azureml.exceptions._azureml_exception import UserErrorException

from .component import Component, Output, Input
from .pipeline import Pipeline
from ._dataset import _GlobalDataset, _FeedDataset
from ._pipeline_parameters import PipelineParameter
from ._parameter_assignment import _ParameterAssignment
from ._util._utils import _sanitize_python_variable_name, _get_valid_directory_path, \
    _scrubbed_exception, _unique, _get_data_info_hash_id, _get_parameter_static_value
from ._util._yaml_utils import YAML

REMOTE_REF_FORMAT = 'azureml:{}'
DATA_FROM_INPUT_REF_FORMAT = 'inputs.{}'
DATA_TO_OUTPUT_REF_FORMAT = 'outputs.{}'
DATA_FROM_NODE_OUTPUT_REF_FORMAT = 'graph.{}.outputs.{}'
COMPONENT_REF_FORMAT = 'file:./{}'

yaml = YAML(with_additional_representer=True)


def _get_parameter_assignment_as_str(assignment):
    """Get parameter assignment as formatted string."""
    # Format: prefix{inputs.parameter_name}postfix
    return ''.join([
        part.str if part.type == _ParameterAssignment.LITERAL
        else f'{{{DATA_FROM_INPUT_REF_FORMAT.format(part.str)}}}' for part in assignment.assignments])


def _serialize_data(provider, dset):
    """
    Serialize input/runsettings data.

    For more format information, refer to the constants above.
    """
    if isinstance(dset, DatasetConsumptionConfig):
        dset = dset.dataset

    # Indicate source_val is a parameter reference or not
    is_ref = True
    if isinstance(dset, Input):
        source_val = DATA_FROM_INPUT_REF_FORMAT.format(dset.name)
    elif isinstance(dset, Output):
        from_node_instance_id = dset._owner._instance_id
        node = provider.get_node_by_instance_id(from_node_instance_id)
        source_val = DATA_FROM_NODE_OUTPUT_REF_FORMAT.format(node.node_name, dset._name)
    elif isinstance(dset, PipelineParameter):
        source_val = DATA_FROM_INPUT_REF_FORMAT.format(dset.name)
    elif isinstance(dset, AbstractDataset):
        # Ref by name and version and ref by id if anonymous
        source_val = {'name': REMOTE_REF_FORMAT.format(':'.join([dset.name, str(dset.version)]))} \
            if dset.name is not None else {'id': dset.id}
        is_ref = False
    elif isinstance(dset, _GlobalDataset):
        # Ref by path and datastore
        source_val = {
            'path': dset.path_on_datastore, 'datastore': REMOTE_REF_FORMAT.format(dset.data_store_name)}
        is_ref = False
    elif isinstance(dset, _FeedDataset):
        source_val = {'arm_id': dset.arm_id}
    elif isinstance(dset, _ParameterAssignment):
        source_val = _get_parameter_assignment_as_str(dset)
    else:
        source_val = dset
        is_ref = False
    return source_val, is_ref


def _serialize_input(input_name, component, provider, with_data=False, with_def=False):
    """
    Serialize component input.
    :param input_name: The input or parameter name to serialize.
    :type input_name: str
    :param component: The owner of input.
    :type component: Component
    :param provider: Used to serialize data.
    :type provider: PipelineExportProvider
    :param with_data: Return input value in dict.
    :type with_data: bool
    :param with_def: Return input definition in dict.
    :type with_def: bool
    """
    # Add input definition
    if input_name in component._input_ports:
        input_def = component._definition.inputs[input_name]
        entity_dict = input_def._to_dict(remove_name=True) if with_def else {}
        input = component._input_ports[input_name]
        # Export the real input value if is exporting definition.
        data = _get_parameter_static_value(input._dset) if with_def else input._dset
        if isinstance(data, PipelineParameter) and data.default_value is None:
            # Handle special case for None as input
            # None will be wrapped as PipelineParameter
            data = 'None'
        # Add input properties
        if input.mode:
            entity_dict['mode'] = input.mode
        if input._path_on_compute:
            entity_dict['path_on_compute'] = input._path_on_compute
    else:
        if input_name not in component._parameter_params:
            raise Exception(f'{input_name!r} not found in component {component.name!r} parameters!')
        param_def = component._definition.parameters[input_name]
        entity_dict = param_def._to_dict(remove_name=True) if with_def else {}
        from inspect import Parameter
        if with_def and param_def._default is Parameter.empty:
            del entity_dict['default']
        data = component._parameter_params[input_name]
        # Export the real input value if is exporting definition.
        data = _get_parameter_static_value(data) if with_def else data
    # Append input data
    if with_data:
        serialized_data, is_ref = _serialize_data(provider, data)
        if is_ref:
            # If data is pipeline parameter reference, format as 'param: value' and return
            return serialized_data
        else:
            # Else append data to dict
            entity_dict.update({'data': serialized_data})
    return entity_dict


def _serialize_output(output: Output, with_data=False, with_def=False):
    """
    Serialize pipeline output.
    :param output: The output to serialize.
    :type output: Output
    :param with_data: Return output data binding if exists in dict.
    :type with_data: bool
    :param with_def: Return output definition in dict.
    :type with_def: bool
    """
    # Add parent output reference
    if with_data:
        if output._owner._is_pipeline and id(output) in map(id, output._owner.outputs.values()):
            # When output is one of the sub pipeline outputs.
            # If is ref value, format as 'param: value' and return
            return DATA_TO_OUTPUT_REF_FORMAT.format(output._name)
        else:
            # When output is one of the parent pipeline outputs.
            parent = output._owner._parent
            if parent is not None and id(output) in map(id, parent._outputs_mapping.values()):
                # If is ref value, format as 'param: value' and return
                return DATA_TO_OUTPUT_REF_FORMAT.format(output._name)
    # Add output definition
    output_def = output._owner._definition.outputs[output._name]
    entity_dict = output_def._to_dict(remove_name=True) if with_def else {}
    # Add output properties
    if output._dataset_output_options:
        entity_dict['path'] = output._dataset_output_options.path_on_datastore
    if output._dataset_registration:
        entity_dict['name'] = output._dataset_registration.name
        entity_dict['create_new_version'] = output._dataset_registration.create_new_version
    if output.datastore:
        entity_dict['datastore'] = output.datastore
    if output._path_on_compute:
        entity_dict['path_on_compute'] = output._path_on_compute
    if output._mode:
        entity_dict['mode'] = output._mode
    return entity_dict if entity_dict else None


def _resolve_compute_ref(compute_target):
    """
    Resolve the compute target dict of pipeline or module, it is not
        None if configured by user.

    :return: compute target name
    :rtype: dict or None
    """
    compute_value = None
    if isinstance(compute_target, tuple):
        # Ref compute by name
        compute_target, _ = compute_target
        compute_value = REMOTE_REF_FORMAT.format(compute_target)
    elif isinstance(compute_target, PipelineParameter):
        # Ref compute to pipeline parameter
        compute_value = DATA_FROM_INPUT_REF_FORMAT.format(compute_target.name)
    elif isinstance(compute_target, _ParameterAssignment):
        # Ref compute as prefix{parameter_name}postfix
        compute_value = _get_parameter_assignment_as_str(compute_target)
    elif type(compute_target) is str:
        compute_value = REMOTE_REF_FORMAT.format(compute_target)
    return {'target': compute_value} if compute_value is not None else None


def _dump_file(entity_dict, directory_path, file_name, entity_dict_str=None, ignore_dup=True):
    file_path = os.path.join(directory_path, _sanitize_python_variable_name(file_name) + '.yaml')
    if os.path.exists(file_path):
        if not ignore_dup:
            msg = 'Target file path {} already exists!'
            raise _scrubbed_exception(UserErrorException, msg, file_path)
        else:
            return
    with open(file_path, 'w') as f:
        if entity_dict_str is not None:
            f.write(entity_dict_str)
        else:
            yaml.dump(entity_dict, f)
    print('Successfully dump yaml file at {}'.format(file_path))


class NodeBase(ABC):
    def __init__(self, compute_target=None, instance=None):
        self.instance = instance
        self.type = self.instance._definition.type.value
        self.schema = self.instance._definition.SCHEMA
        _, self.node_name = instance._parse_graph_path()
        self.target_ref = _resolve_compute_ref(compute_target)

    @abstractmethod
    def export_attribute(self, provider, from_node):
        """
        Export node attribute on graph.

        :param provider: export provider, to resolve input/output node
        :type provider: PipelineExportProvider
        :param from_node: from node of the function call to calculate the relative path
        :type from_node: Union[PipelineNode, ComponentNode]
        :return: attribute dict
        :rtype: dict
        """
        raise NotImplementedError

    @abstractmethod
    def export_definition(self, provider):
        """
        Export basic definition info of component.

        :param provider: export provider, to resolve input/output node
        :type provider: PipelineExportProvider
        :return: definition dict
        :rtype: dict
        """
        instance_def = self.instance._definition
        basic_info = {
            '$schema': self.schema, 'name': instance_def.name,
            'version': instance_def.version, 'display_name': instance_def.display_name,
            'type': self.type, 'description': instance_def.description, 'tags': instance_def.tags}
        return {k: v for k, v in basic_info.items() if v}

    def serialize_node_inputs_outputs(self, provider):
        """
        Serialize single module or pipeline's inputs and outputs provided.
        :return: A dict contains inputs, outputs, parameters mappings.
        :rtype: dict
        """
        instance = self.instance
        # serialize inputs
        inputs_dict = {k: _serialize_input(k, instance, provider, with_data=True)
                       for k, v in instance._input_ports.items()}
        # serialize parameters
        for _k, _v in instance._parameter_params.items():
            # Skip component default values
            if _k in instance._definition.parameters \
                    and _get_parameter_static_value(_v) == instance._definition.parameters[_k].default:
                continue
            source_val = _serialize_input(_k, instance, provider, with_data=True)
            inputs_dict[_k] = source_val
        # serialize outputs
        outputs_dict = {
            k: _serialize_output(v, with_data=True) for k, v in instance.outputs.items()}
        return {'inputs': inputs_dict, 'outputs': outputs_dict}

    @staticmethod
    def _get_file_relative_ref(path, start_file_path):
        start_dir_path, _ = os.path.split(start_file_path)
        formatted_relative_path = os.path.relpath(path, start_dir_path).replace(os.sep, '/')
        return COMPONENT_REF_FORMAT.format(formatted_relative_path)


class ComponentNode(NodeBase):
    ANONYMOUS = 'Anonymous'
    GLOBAL = 'Global'
    WORKSPACE = 'Workspace'

    def __init__(self, component: Component, directory_path):
        compute_target = component.runsettings.target if hasattr(component.runsettings, 'target') else None
        super().__init__(compute_target=compute_target, instance=component)
        self.component_type = component._definition.registration_context.shared_scope
        self.component_ref_path = self.resolve_component_file_path(directory_path)

    def resolve_component_file_path(self, directory_path):
        definition_name = self.instance._definition.name
        if self.component_type is None:
            raise UserErrorException('Pipeline with workspace independent asset does not support export yaml for now.')
        if self.component_type == ComponentNode.ANONYMOUS:
            # Export and refer to local yaml file abs path if is anonymous component
            ref = os.path.join(directory_path, f'{_sanitize_python_variable_name(definition_name)}.yaml')
        elif self.component_type == ComponentNode.WORKSPACE:
            # Refer as azureml:component_name:version
            ref = REMOTE_REF_FORMAT.format(f'{definition_name}:{self.instance._definition.version}')
        elif self.component_type == ComponentNode.GLOBAL:
            # Refer as azureml://component_name
            ref = definition_name
        else:
            raise UserErrorException(f'Unknown component type {self.component_type}')
        return ref

    def export_attribute(self, provider, from_node):
        component_ref = self.component_ref_path
        if self.component_type == ComponentNode.ANONYMOUS:
            # Export separate yaml if is anonymous component
            self.export_definition(provider)
            component_ref = NodeBase._get_file_relative_ref(
                self.component_ref_path, from_node.component_ref_path)
        node_entity = {'component': component_ref}
        if self.target_ref is not None:
            node_entity.update({'compute': self.target_ref})
        inputs_outputs_dict = self.serialize_node_inputs_outputs(provider)
        # serialize compute run setting
        runsetting_dict = self.instance.runsettings._get_values(ignore_none=True)
        # Extract runsetting values
        runsetting_dict = {k: _serialize_data(provider, v)[0] for k, v in runsetting_dict.items()}
        if runsetting_dict:
            inputs_outputs_dict.update({'runsettings': runsetting_dict})
        node_entity.update(inputs_outputs_dict)

        return {self.node_name: node_entity}

    def export_definition(self, provider):
        yaml_str = self.instance._module_dto.yaml_str
        components_directory = provider.components_directory
        if not os.path.exists(components_directory):
            os.mkdir(components_directory)
        # ignore duplicate reference export
        _dump_file(entity_dict=None, entity_dict_str=yaml_str,
                   directory_path=components_directory,
                   file_name=self.instance._definition.name)


class PipelineNode(NodeBase):
    def __init__(self, pipeline: Pipeline, directory_path):
        compute_target, _ = pipeline._get_default_compute_target()
        self.is_primary = not pipeline._is_sub_pipeline
        super().__init__(compute_target=compute_target, instance=pipeline)
        file_name = _sanitize_python_variable_name(self.instance._definition.name)
        # refer to local yaml file
        self.component_ref_path = os.path.join(directory_path, f'{file_name}.yaml')

    def export_attribute(self, provider, from_node):
        """
        Export single pipeline to a dict, do not export it's sub pipeline.

        :param from_node: from node of the function call to calculate the relative path
        :type from_node: Union[PipelineNode, ComponentNode]
        :param provider: pipeline export provider
        :type provider: PipelineExportProvider
        :return:
        """
        pipeline_result = {}
        # add step type and ref
        pipeline_result.update({'component': NodeBase._get_file_relative_ref(
            self.component_ref_path, from_node.component_ref_path)})
        if self.target_ref is not None:
            pipeline_result.update({'compute': self.target_ref})
        inputs_outputs_dict = self.serialize_node_inputs_outputs(provider)
        param_set = set(self.instance._definition._parameters.keys())
        param_set.update(self.instance._definition.inputs.keys())
        inputs_outputs_dict['inputs'] = {k: v for k, v in inputs_outputs_dict['inputs'].items() if k in param_set}
        pipeline_result.update(inputs_outputs_dict)

        entity_dict = {self.node_name: pipeline_result}

        return entity_dict

    def export_definition(self, provider):
        directory_path = provider.directory_path if self.is_primary else provider.components_directory
        if not os.path.exists(directory_path):
            os.mkdir(directory_path)
        pipeline_result = super().export_definition(provider)
        inputs_dict = {
            k: _serialize_input(k, self.instance, provider, with_data=self.is_primary, with_def=True)
            for k, v in self.instance._input_ports.items()}
        inputs_dict.update(
            {k: _serialize_input(k, self.instance, provider, with_data=self.is_primary, with_def=True)
             for k, v in self.instance._parameter_params.items()})
        outputs_dict = {k: _serialize_output(v, with_def=True)
                        for k, v in self.instance.outputs.items()}
        inputs_outputs_dict = {'inputs': inputs_dict, 'outputs': outputs_dict}
        pipeline_result.update(inputs_outputs_dict)
        defaults_config = {}
        if self.target_ref is not None:
            defaults_config.update({'compute': self.target_ref})
        if self.instance.default_datastore:
            defaults_config.update({'datastore': REMOTE_REF_FORMAT.format(self.instance.default_datastore)})

        if defaults_config:
            pipeline_result.update({'defaults': defaults_config})

        # expand steps inside pipeline
        steps = {}
        for node_instance in self.instance.nodes:
            node = provider.get_node_by_instance_id(node_instance._get_instance_id())
            steps.update(node.export_attribute(provider, from_node=self))
            pipeline_result.update({'graph': steps})

        _dump_file(entity_dict=pipeline_result, directory_path=directory_path,
                   file_name=self.instance._definition.name)


class PipelineExportProvider:
    def __init__(self, root_pipeline, pipelines, module_nodes, data_infos, directory_path):
        self.root_pipeline = root_pipeline
        self.pipelines = pipelines
        self.module_nodes = module_nodes
        data_sources = _unique(data_infos, _get_data_info_hash_id)
        self.data_sources = [ds for ds in data_sources if ds.dataset_type != 'parameter']
        # Append pipeline name and suffix if directory path not empty
        self.directory_path = _get_valid_directory_path(
            os.path.join(directory_path, _sanitize_python_variable_name(self.root_pipeline.name)))
        os.mkdir(self.directory_path)
        self.components_directory = os.path.join(self.directory_path, 'components')
        self.instance_id_to_node_dict = self._prepare_instance_id_to_node_dict()

    def _prepare_instance_id_to_node_dict(self) -> dict:
        """
        prepare metadata id to node dict,
            metadata id indicates module._instance_id or pipeline._id.

        :return: module._instance_id/pipeline._id to identifier mapping
        :rtype: dict[str, PipelineNode]
        """
        # create module node
        instance_id_to_node_dict = {module._get_instance_id(): ComponentNode(module, self.components_directory)
                                    for module in self.module_nodes}
        # create pipeline node
        instance_id_to_node_dict.update({pipeline._get_instance_id(): PipelineNode(
            pipeline, self.components_directory if pipeline._is_sub_pipeline else self.directory_path)
            for pipeline in self.pipelines})
        return instance_id_to_node_dict

    def get_node_by_instance_id(self, instance_id) -> Union[ComponentNode, PipelineNode]:
        if instance_id not in self.instance_id_to_node_dict:
            raise Exception('Related node not found. Instance id {}'.format(instance_id))
        return self.instance_id_to_node_dict[instance_id]

    def export_pipeline_entity(self):
        """
        Export a pipeline entity includes sub pipelines.

        :return: pipeline entity dict
        :rtype: dict
        """
        # resolve pipeline graph
        pipeline_def_ids = set()
        for pipeline in self.pipelines:
            # ignore same sub pipeline definition
            def_id = pipeline._definition._id
            if def_id in pipeline_def_ids:
                continue
            pipeline_def_ids.add(def_id)
            self.get_node_by_instance_id(pipeline._get_instance_id()). \
                export_definition(self)
        return self.directory_path
