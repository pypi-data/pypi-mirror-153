# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import json
from pathlib import Path
from urllib.parse import unquote
from typing import List, Union

from pydash import get

from azure.ml.component._core._component_definition import ControlComponentType
from azure.ml.component._pipeline_validator import CycleValidator
from azure.ml.component._restclients.designer.models import (
    PipelineGraph, PortInfo, ModuleDto,
    GraphEdge, GraphDatasetNode, EntityInterface, ParameterAssignment, ParameterValueType,
    StructuredInterfaceOutput, DataSourceType, ParameterType, RunSettingParameterType, ModuleScope
)
from azure.ml.component._util._utils import _get_enum, _sanitize_python_variable_name
from azureml.core import Run

TEMPLATE_FOLDER = Path(__file__).resolve().parent.parent / 'data' / 'graph_to_code'
COMPONENT_NODE_TEMPLATE = TEMPLATE_FOLDER / 'component_node.template'
CONTROL_NODE_TEMPLATE = TEMPLATE_FOLDER / 'control_node.template'
PIPELINE_DEF_TEMPLATE = TEMPLATE_FOLDER / 'pipeline_def.template'
INIT_TEMPLATE = TEMPLATE_FOLDER / 'init.template'
RUN_TEMPLATE = TEMPLATE_FOLDER / 'run.template'
FILE_HEADER_TEMPLATE = TEMPLATE_FOLDER / 'file_header.template'
NOTE_BOOK_TEMPLATE = TEMPLATE_FOLDER / 'notebook.template'


def _normalize_dict_param_val(val, indent=4, last_line_indent=0):
    result = json.dumps(val, indent=indent, sort_keys=True)
    if last_line_indent > 0:
        result = result.replace('}', ' ' * last_line_indent + '}')
    return result


def _equal_to_enum_val(val: str, enum_val):
    """Returns True if val is equal to enum value."""
    # TODO: check if backend can return actual string val instead of enum order
    return _get_enum(val, enum_val.__class__) == enum_val


def _normalize_string_param_val(val):
    # TODO: pretty print multi-line string? If we do that, extra indent will be added to original string
    return repr(val)


def _normalize_param_val(val, val_type: Union[ParameterType, RunSettingParameterType]):
    # TODO: environment variable's RunSettingParameterType is also string, special handle this?
    # TODO: normalize val when first get it
    if val is None or val == "":
        return "None"
    elif _equal_to_enum_val(val_type, val_type.BOOL):
        return val.lower() == "true"
    elif _equal_to_enum_val(val_type, val_type.STRING) or _equal_to_enum_val(val_type, val_type.UNDEFINED) or hasattr(
            val_type, "JSON_STRING") and _equal_to_enum_val(val_type, val_type.JSON_STRING):
        return _normalize_string_param_val(val)
    else:
        return val


def _get_string_concatenate_val(concatenates: List[ParameterAssignment]):
    if not concatenates:
        return "None"
    val = ""
    pipeline_params = []
    for item in concatenates:
        if _equal_to_enum_val(item.value_type, ParameterValueType.GRAPH_PARAMETER_NAME):
            val += "{}"
            pipeline_params.append(item.value)
        else:
            val += item.value
    return f"{val!r}.format({', '.join(pipeline_params)})"


def _is_anonymous_pipeline_component(dto: ModuleDto):
    return _equal_to_enum_val(dto.module_scope, ModuleScope.ANONYMOUS) and _is_pipeline_component(dto)


def _is_pipeline_component(dto: ModuleDto):
    return dto.job_type == "PipelineComponent"


def _get_module_name(component_name):
    return f"{_sanitize_python_variable_name(component_name)}"


def _get_module_file_name(component_name):
    return f"{_get_module_name(component_name)}.py"


def _convert_column_picker_val(val):
    if not val:
        return val
    # url decode
    val = unquote(val)
    # TODO(1548635): support column picker new format?
    return json.dumps(val)


def process_error(error, raise_error=True, logger=None):
    # TODO: raise or warn?
    if raise_error:
        raise error
    else:
        logger.warn(error)


class GraphStructureError(Exception):
    """Exception raised when given graph entity is invalid."""


class UnknownDataSetPathParameterError(GraphStructureError):
    """Exception raised when giving multiple value of a keyword parameter in dynamic functions."""

    def __init__(self, name, dataset_id, saved_dataset_id, dataset_version):
        message = f"Unknown DataSetPathParameter {name}. datasetId:{dataset_id}," \
                  f" savedDatasetId:{saved_dataset_id}, version:{dataset_version}"
        super().__init__(message)


class DataUtil:
    GLOBAL_DATASET_STORE_NAME_SUFFIX = "_globaldatasets"
    LEGACY_DATA_REFERENCE_FORMAT = "azureml/{run-id}/{output-name}"

    # TODO: PipelineParameterAssignments?
    @classmethod
    def is_global_dataset(cls, data: GraphDatasetNode, interface: EntityInterface = None):
        return DataUtil.inline_data_path_datastore_name(data, interface).endswith(cls.GLOBAL_DATASET_STORE_NAME_SUFFIX)

    # TODO: verify these methods
    @classmethod
    def inline_data_path_datastore_name(cls, data: GraphDatasetNode, interface: EntityInterface = None):
        param_name = data.data_path_parameter_name or data.data_set_definition.parameter_name
        return get(
            data, "data_set_definition.value.literal_value.data_store_name", ""
        ) or cls.data_path_datastore_name(interface, param_name)

    @classmethod
    def inline_data_path_relative_path(cls, data: GraphDatasetNode, interface: EntityInterface):
        param_name = data.data_path_parameter_name or data.data_set_definition.parameter_name
        return get(
            data, "data_set_definition.value.literal_value.relative_path", ""
        ) or cls.data_path_relative_path(interface, param_name)

    @classmethod
    def data_path_datastore_name(cls, interface: EntityInterface, param_name: str):
        try:
            data_path_params = next(p for p in interface.data_path_parameters if p.name == param_name)
            return data_path_params.default_value.datastore_name
        except:
            try:
                data_path_params = next(p for p in interface.data_path_parameter_list if p.name == param_name)
                return data_path_params.default_value.literal_value.datastore_name
            except:
                return ""

    @classmethod
    def data_path_relative_path(cls, interface: EntityInterface, param_name: str):
        try:
            data_path_params = next(p for p in interface.data_path_parameters if p.name == param_name)
            return data_path_params.default_value.relative_path
        except:
            try:
                data_path_params = next(p for p in interface.data_path_parameter_list if p.name == param_name)
                return data_path_params.default_value.literal_value.relative_path
            except:
                return ""

    @classmethod
    def get_dataset_name_postfix_by_version(cls, version):
        if version:
            return f"v_{version}"
        else:
            return "latest"

    @classmethod
    def get_dataset_mapping_key(cls, id, saved_id, version, relative_path=None):
        if saved_id:
            return saved_id
        else:
            if id:
                return f"{id}_{cls.get_dataset_name_postfix_by_version(version)}"
            else:
                return relative_path

    @classmethod
    def get_saved_dataset_py_name(cls, saved_id):
        return f"saved_dataset_{saved_id.replace('-', '_')}"

    @classmethod
    def get_aml_dataset_version(cls, interface: EntityInterface, param_name):
        data_path_param = interface.data_path_parameter_list or []
        matched_data = next((d for d in data_path_param if d.name == param_name), None)
        return get(matched_data, "default_value.data_set_reference.version", None)


class GraphPackageUtil:
    """Functionalities used for pipeline package level."""
    MODULE_FUNC_POSTFIX = "_func"
    SUBGRAPH_PACKAGE_NAME = "subgraphs"
    PIPELINE_PACKAGE_NAME = "pipelines"
    COMPONENT_PACKAGE_NAME = "components"
    ALL_COMPONENTS = "*"
    INCLUDED_COMPONENTS_SEP = ","
    AZUREML_PREFIX = "azureml:"
    COMPONENT_VERSION_SEP = ":"
    WORKSPACE_VAR_NAME = "workspace"

    def __init__(self, graphs: List[PipelineGraph], logger, include_components=None):
        self.logger = logger
        self.graphs = graphs
        self.component_id_2_definition = self._get_component_id_2_definition()
        self.component_id_2_module_name, self.component_id_2_func_name = self._get_component_id_2_module_name()
        self.component_module_ids, self.pipeline_module_ids = self._distinguish_component_pipeline_ids()
        self.control_type_2_func_name, self.control_type_2_edge_param_mapping = self._get_control_type_mapping()
        # component module ids which need to generate snapshot
        self.snapshot_module_ids = self._get_snapshot_module_ids(include_components=include_components)
        # component module ids which need to generate package(all components except pipeline components)
        generate_module_ids = self._get_generate_module_ids()
        self.generated_id_2_function = {
            id: func for id, func in self.component_id_2_func_name.items() if id in generate_module_ids
        }
        self.generated_id_2_module = {
            id: module for id, module in self.component_id_2_module_name.items() if id in generate_module_ids
        }
        self.workspace_name = self.WORKSPACE_VAR_NAME

    def _get_component_id_2_definition(self):
        module_id_2_definition = {}
        for graph in self.graphs:
            for dto in graph.graph_module_dtos or []:
                if dto.module_version_id not in module_id_2_definition.keys():
                    module_id_2_definition[dto.module_version_id] = dto
        return module_id_2_definition

    def _get_component_id_2_module_name(self):
        module_id_2_module_name = {}
        module_id_2_func_name = {}

        # use this to handle case when one module name has multiple versions
        module_name_2_dto_list = {}
        for dto in self.component_id_2_definition.values():
            py_name = _sanitize_python_variable_name(dto.module_name)
            if py_name not in module_name_2_dto_list.keys():
                module_name_2_dto_list[py_name] = []
            module_name_2_dto_list[py_name].append(dto)

        for dto in self.component_id_2_definition.values():
            py_name = _sanitize_python_variable_name(dto.module_name)
            # handle case when different anonymous module have same pyName, use name_version_module_version_id as name
            if len(module_name_2_dto_list[py_name]) > 1:
                if dto.module_version:
                    py_name += f"_{dto.module_version}"
                py_name += f"_{dto.module_version_id}"
            py_name = _sanitize_python_variable_name(py_name)
            module_id_2_module_name[dto.module_version_id] = py_name
            module_id_2_func_name[dto.module_version_id] = py_name + self.MODULE_FUNC_POSTFIX
        return module_id_2_module_name, module_id_2_func_name

    def _get_control_type_mapping(self):
        control_types = set({
            node.control_type for graph in self.graphs for node in graph.control_nodes or []
        })
        control_type_2_func_name = {
            type_name: ControlComponentType.get_control_function_name(type_name)
            for type_name in control_types
        }
        control_type_2_edge_type_mapping = {
            type_name: ControlComponentType.get_control_type_edge_param_mapping(type_name)
            for type_name in control_types
        }
        return control_type_2_func_name, control_type_2_edge_type_mapping

    def _distinguish_component_pipeline_ids(self):
        component_module_ids, pipeline_module_ids = set(), set()

        for dto in self.component_id_2_definition.values():
            if _is_pipeline_component(dto):
                pipeline_module_ids.add(dto.module_version_id)
            else:
                component_module_ids.add(dto.module_version_id)
        return component_module_ids, pipeline_module_ids

    def _get_snapshot_module_ids(self, include_components):
        snapshot_module_ids = set()
        if not include_components:
            return snapshot_module_ids
        else:
            # mapping from component name:version to component id
            component_name_version_2_id = {}

            for dto in self.component_id_2_definition.values():
                if dto.module_version_id in self.component_module_ids:
                    # skip pipeline components
                    component_identifier = f"{self.AZUREML_PREFIX}{dto.module_name}:{dto.module_version}"
                    component_name_version_2_id[component_identifier] = dto.module_version_id

            def add_component_id_if_not_built_in(component_id):
                # add component id to generated module ids if it's not a built in component
                component_def = self.component_id_2_definition[component_id]
                component_type = _get_enum(component_def.module_scope, ModuleScope)
                if component_type == ModuleScope.GLOBAL_ENUM:
                    self.logger.warn(f"Skipped generate snapshot for global component: {component_def.module_name}")
                else:
                    snapshot_module_ids.add(component_id)

            # all specified components
            if include_components == self.ALL_COMPONENTS:
                specified_component_ids = component_name_version_2_id.keys()
            else:
                specified_component_ids = set(include_components.split(self.INCLUDED_COMPONENTS_SEP))

            for component_id in specified_component_ids:
                component_id = component_id.strip()
                if component_id in component_name_version_2_id.keys():
                    component_id = component_name_version_2_id[component_id]
                    add_component_id_if_not_built_in(component_id)
                elif component_id in self.component_module_ids:
                    add_component_id_if_not_built_in(component_id)
                else:
                    self.logger.warn(f"Skipped generate not found included component: {component_id}")
            return snapshot_module_ids

    def _get_generate_module_ids(self):
        snapshot_module_ids = set()
        for dto in self.component_id_2_definition.values():
            if dto.module_version_id in self.component_module_ids:
                # skip pipeline components
                snapshot_module_ids.add(dto.module_version_id)
        return snapshot_module_ids


class GraphUtil:
    """Functionalities used for pipeline level."""
    MODULE_FUNC_POSTFIX = "_func"

    def __init__(self, graph: PipelineGraph, pkg_util: GraphPackageUtil, definition: ModuleDto = None):
        self.graph = graph
        self.pkg_util = pkg_util
        self.definition = definition

        self.data_sources = graph.graph_data_sources or []
        self.module_id_2_module = {m.module_version_id: m for m in graph.graph_module_dtos or {}}
        # Module nodes + pipeline nodes
        self.all_nodes = [*(self.graph.module_nodes or []), *(self.graph.sub_graph_nodes or [])]
        # Mapping from node id to node entity(component + subgraph)
        self.node_id_2_node = {n.id: n for n in self.all_nodes}
        # Mapping from node id to node definition
        self.node_id_2_module = {
            id: self.module_id_2_module[node.module_id] for id, node in self.node_id_2_node.items()}
        self.node_id_2_control = {n.id: n for n in graph.control_nodes or {}}
        self.node_id_2_data = {n.id: n for n in graph.dataset_nodes or {}}
        self.node_id_2_run_setting = {
            n.node_id: n for n in graph.module_node_run_settings or {}
        }
        self.node_id_2_run_setting_def = {
            id: node.run_setting_parameters for id, node in self.node_id_2_module.items()
        }
        self.default_datastore = graph.default_datastore
        # Indicate if current graph used datastore
        self.used_datastore = False
        self.used_dataset = False
        self.workspace_name = self.pkg_util.workspace_name
        # Mapping from module id to function name, Mapping from module id to module name
        self.module_id_2_func_name = pkg_util.component_id_2_func_name
        self.module_id_2_module_name = pkg_util.component_id_2_module_name
        # Mapping from control type to function name
        self.control_type_2_func_name = pkg_util.control_type_2_func_name
        self.control_type_2_edge_param_mapping = pkg_util.control_type_2_edge_param_mapping

        # Sorted all nodes according to topological order
        self.sorted_nodes = self._sort_nodes()
        # Mapping from node id to node variable name
        self.node_id_2_var_name = self._get_node_id_2_var_name()
        # Mapping from dataset id to name, for global dataset, use relative path, for custom dataset, gen unique key
        self.dataset_id_2_name = self._get_dataset_id_2_name()
        # Mapping from global & user dataset id python name to definition
        self.global_dataset_py_name_2_def, self.user_dataset_py_name_2_def = self._get_dataset_name_2_definition()
        # Mapping from pipeline parameter to UNIQUE python name
        # Mapping from pipeline parameter name to actual value
        self.pipeline_param_2_py_name, self.pipeline_param_2_actual_val = self._get_pipeline_param_2_actual_val()
        self.used_dsl_types = set()
        # Mapping from pipeline parameter name to default value, None means this param is required
        self.pipeline_param_2_default_val = self._get_pipeline_param_2_default_val()
        # Used early termination policies for sweep runsettings
        self.used_early_termination_policies = set()

    def _get_node_id_2_var_name(self):
        node_id_2_var_name = {}
        module_name_count = {}
        for node in self.all_nodes:
            if not node.name or node.name == self.module_id_2_func_name[node.module_id]:
                # for node without a name or name equals module func name, add a number postfix to it
                module_name = self.module_id_2_func_name[node.module_id].replace(self.MODULE_FUNC_POSTFIX, "")
                step_name = module_name + f"_{module_name_count.get(module_name, 0)}"
                node_id_2_var_name[node.id] = step_name
                module_name_count[module_name] = module_name_count.get(module_name, 0) + 1
            else:
                # Note: UI has no limitation on node name, so we need to sanitize it
                node_id_2_var_name[node.id] = _sanitize_python_variable_name(node.name)
        return node_id_2_var_name

    def _sort_nodes(self):
        nodes = []
        node_id_2_node = {node.id: node for node in self.all_nodes}

        sorted_nodes = CycleValidator.sort(self.all_nodes, self.graph.edges, process_error)
        for node_id in sorted_nodes:
            nodes.append(node_id_2_node[node_id])
        return nodes

    def _get_dataset_id_2_name(self):
        # TODO: verify this logic, what's dataset_key when registered dataset has multi version
        dataset_id_2_name = {}
        for data_source in self.data_sources:
            if _equal_to_enum_val(data_source.data_source_type, DataSourceType.GLOBAL_DATASET):
                self.used_datastore = True
                dataset_key = data_source.relative_path
                if dataset_key not in dataset_id_2_name.keys():
                    py_name = _sanitize_python_variable_name(data_source.name)
                    dataset_id_2_name[dataset_key] = py_name
            else:
                dataset_key = DataUtil.get_dataset_mapping_key(
                    data_source.id, data_source.saved_dataset_id, data_source.dataset_version_id)
                if dataset_key not in dataset_id_2_name.keys():
                    if data_source.id:
                        # registered dataset
                        py_name = _sanitize_python_variable_name(data_source.name)
                    else:
                        py_name = DataUtil.get_saved_dataset_py_name(data_source.saved_dataset_id)
                    dataset_id_2_name[dataset_key] = py_name

                    # hotfix for dataset parameter, for dataset parameter, there is saved dataset id in datasource,
                    # but no saved dataset id in parameter default value
                    if dataset_key == data_source.saved_dataset_id and data_source.id:
                        dataset_id_2_name[DataUtil.get_dataset_mapping_key(
                            data_source.id, None, data_source.dataset_version_id)] = py_name
        return dataset_id_2_name

    def _get_dataset_name_2_definition(self):
        global_dataset_name_2_def = {}
        user_dataset_name_2_def = {}
        for ds in self.data_sources:
            if _equal_to_enum_val(ds.data_source_type, DataSourceType.GLOBAL_DATASET):
                dataset_key = ds.relative_path
                py_name = self.dataset_id_2_name[dataset_key]
                global_dataset_name_2_def[py_name] = ds
            else:
                dataset_key = DataUtil.get_dataset_mapping_key(ds.id, ds.saved_dataset_id, ds.dataset_version_id)
                if dataset_key not in self.dataset_id_2_name.keys():
                    continue
                py_name = self.dataset_id_2_name[dataset_key]
                if ds.id:
                    # handle case when registered dataset with multiple versions
                    # TODO: validate this case
                    multi_version = len({d.saved_dataset_id for d in self.data_sources if d.id == ds.id}) > 1
                    if multi_version:
                        post_fix = f"_{DataUtil.get_dataset_name_postfix_by_version(ds.dataset_version_id)}"
                        py_name += post_fix
                user_dataset_name_2_def[py_name] = ds
        return global_dataset_name_2_def, user_dataset_name_2_def

    def _get_pipeline_param_2_actual_val(self):
        # mapping from python name to count
        py_name_count = {}
        # mapping from pipeline param to py name
        pipeline_param_2_py_name = {}
        # mapping from py name to actual val
        pipeline_params_2_actual_val = {}

        def get_unique_py_name(param_name):
            # Returns unique python name for param_name
            candidate = _sanitize_python_variable_name(param_name)
            if candidate not in py_name_count.keys():
                py_name_count[candidate] = 1
            else:
                count = py_name_count[candidate] + 1
                py_name_count[candidate] = count
                candidate += f"_{count}"
            pipeline_param_2_py_name[param_name] = candidate
            return candidate

        # parameters
        for param in get(self.graph.entity_interface, "parameters", []):
            py_name = get_unique_py_name(param.name)
            if param.default_value == "":
                # unprovided optional pipeline param's default value will be "", set None for that case
                pipeline_params_2_actual_val[py_name] = None
            elif _equal_to_enum_val(param.type, ParameterType.INT) or _equal_to_enum_val(
                    param.type, ParameterType.DOUBLE) or _equal_to_enum_val(param.type, ParameterType.BOOL):
                pipeline_params_2_actual_val[py_name] = param.default_value
            else:
                pipeline_params_2_actual_val[py_name] = _normalize_string_param_val(param.default_value)

        # data parameters
        for param in get(self.graph.entity_interface, "data_path_parameter_list", []):
            py_name = get_unique_py_name(param.name)
            dataset_id = get(param, "default_value.data_set_reference.id", None)
            dataset_version = get(param, "default_value.data_set_reference.version", None)
            saved_dataset_id = get(param, "default_value.saved_data_set_reference.id", None)
            relative_path = get(param, "default_value.literal_value.relative_path", None)
            if not saved_dataset_id:
                # the saved dataset id is not record in the DataPathParameterList, try to retrieve from DataSource
                if not dataset_version:
                    # the dataset version is also null, just find the dataset with the same Id
                    matched_datasource = next((d for d in self.graph.graph_data_sources if d.id == dataset_id), None)
                    if matched_datasource:
                        dataset_version = matched_datasource.dataset_version_id
                        saved_dataset_id = matched_datasource.saved_dataset_id
                else:
                    matched_datasource = next((
                        d for d in self.graph.graph_data_sources if (
                            d.id == dataset_id and d.dataset_version_id == dataset_version)), None)
                    if matched_datasource:
                        saved_dataset_id = matched_datasource.saved_dataset_id

            dataset_key = DataUtil.get_dataset_mapping_key(
                dataset_id, saved_dataset_id, dataset_version, relative_path)

            if dataset_key not in self.dataset_id_2_name.keys():
                if saved_dataset_id:
                    pipeline_params_2_actual_val[
                        py_name] = f"Dataset.get_by_id({self.workspace_name}, '{saved_dataset_id}')"
                    self.used_dataset = True
                elif dataset_id:
                    pipeline_params_2_actual_val[py_name] = f"Dataset.get_by_id({self.workspace_name}, '{dataset_id}')"
                    self.used_dataset = True
                else:
                    raise UnknownDataSetPathParameterError(param.name, dataset_id, saved_dataset_id, dataset_version)
            else:
                pipeline_params_2_actual_val[py_name] = self.dataset_id_2_name[dataset_key]

        # input ports
        inputs = get(self.graph.entity_interface, "ports.inputs", [])
        for input_port in inputs:
            py_name = get_unique_py_name(input_port.name)
            pipeline_params_2_actual_val[py_name] = None
        return pipeline_param_2_py_name, pipeline_params_2_actual_val

    def _normalize_input_type(self, val_type: list, is_optional):
        # Note: there is a known issue that the supported type name in
        # input/output is different from parameter type on graph.
        # parameter types will be like 'Int', 'Bool', 'Double', 'String'.
        supported_primitive_types = ["integer", "float", "boolean", "string"]
        if len(val_type) == 1 and val_type[0] in supported_primitive_types:
            self.used_dsl_types.add("Input")
            return f"Input(type={val_type[0]!r}, optional={is_optional})"
        else:
            # Do not generate annotation for regular input type,
            # to ensure the type of them could be inferred.
            return None

    def _normalize_parameter_type(self, val_type: ParameterType, is_optional):
        if val_type == ParameterType.INT:
            self.used_dsl_types.add("Integer")
            return f"Integer(optional={is_optional})"
        elif val_type == ParameterType.DOUBLE:
            self.used_dsl_types.add("Float")
            return f"Float(optional={is_optional})"
        elif val_type == ParameterType.BOOL:
            self.used_dsl_types.add("Boolean")
            return f"Boolean(optional={is_optional})"
        else:
            self.used_dsl_types.add("String")
            return f"String(optional={is_optional})"

    def _get_pipeline_param_2_default_val(self):
        pipeline_params_2_default = {}
        if not self.definition:
            # Top level pipeline does not have module dto
            pipeline_params_2_default = {key: (None, "None") for key in self.pipeline_param_2_actual_val.keys()}
        else:
            all_params = get(self.definition, "module_entity.structured_interface.parameters", [])
            param_key_2_definition = {param_def.name: param_def for param_def in all_params}
            all_inputs = get(self.definition, "module_entity.structured_interface.inputs", [])
            input_key_2_definition = {input_def.name: input_def for input_def in all_inputs}
            for pipeline_param, py_name in self.pipeline_param_2_py_name.items():
                if pipeline_param in param_key_2_definition.keys():
                    param_def = param_key_2_definition[pipeline_param]
                    param_type = _get_enum(param_def.parameter_type, ParameterType) or ParameterType.STRING
                    default_val = _normalize_param_val(param_def.default_value, param_type)
                    param_type = self._normalize_parameter_type(param_type, param_def.is_optional)
                    pipeline_params_2_default[py_name] = (param_type, default_val)
                else:
                    # won't generate default value for input
                    input_def = input_key_2_definition[pipeline_param]
                    input_type = input_def.data_type_ids_list
                    input_type = self._normalize_input_type(input_type, input_def.is_optional)
                    pipeline_params_2_default[py_name] = (input_type, "None")
        return pipeline_params_2_default

    def get_all_input_edges_to_node(self, node_id: str) -> List[GraphEdge]:
        return [edge for edge in self.graph.edges if edge.destination_input_port.node_id == node_id]

    def get_all_output_edges_from_node(self, node_id: str) -> List[GraphEdge]:
        return [edge for edge in self.graph.edges if edge.source_output_port.node_id == node_id]

    def get_input_port_arg_name(self, port: PortInfo):
        definition = self.node_id_2_module[port.node_id]
        # union inputs and parameters as a input port could be promoted from parameter
        input_port = next(
            (i for i in [*get(definition, "module_python_interface.inputs", []),
                         *get(definition, "module_python_interface.parameters", [])]
             if i.name == port.port_name), None
        )
        if not input_port:
            return _sanitize_python_variable_name(port.port_name)
        return input_port.argument_name

    def get_output_port_arg_name(self, port: PortInfo):
        definition = self.node_id_2_module[port.node_id]
        output_port = next(
            (i for i in get(definition, "module_python_interface.outputs", []) if i.name == port.port_name), None
        )
        if not output_port:
            return _sanitize_python_variable_name(port.port_name)
        return output_port.argument_name

    def get_param_argument_name(self, node_id, name):
        definition = self.node_id_2_module[node_id]

        py_name_mapping = next(
            (i for i in get(definition, "module_python_interface.parameters", []) if i.name == name), None
        )
        if not py_name_mapping:
            return _sanitize_python_variable_name(name)
        return py_name_mapping.argument_name

    def get_data_node_arg_val(self, node_id: str):
        """Returns python name for data node, if data node is global dataset, add it to global_datasets."""
        node: GraphDatasetNode = self.node_id_2_data[node_id]
        if DataUtil.is_global_dataset(node):
            # global dataset
            relative_path = node.data_set_definition.value.literal_value.relative_path
            py_name = self.dataset_id_2_name[relative_path]
            # add to used dataset nodes, global dataset used datastore
            self.used_datastore = True
            return py_name
        elif node.data_set_definition.parameter_name:
            # pipeline dataset parameter for top level pipeline
            py_name = self.pipeline_param_2_py_name[node.data_set_definition.parameter_name]
            return py_name
        elif DataUtil.inline_data_path_datastore_name(node, self.graph.entity_interface):
            # use data path directly
            datastore_name = DataUtil.inline_data_path_datastore_name(node, self.graph.entity_interface)
            relative_path = DataUtil.inline_data_path_relative_path(node, self.graph.entity_interface)
            self.used_datastore = True
            return f"Datastore({self.workspace_name}, name={datastore_name!r}).path({relative_path!r})"
        else:
            # user dataset
            dataset_id = get(node, "data_set_definition.value.data_set_reference.id", None)
            saved_dataset_id = get(node, "data_set_definition.value.saved_data_set_reference.id", None)
            if dataset_id:
                version = get(node, "data_set_definition.value.data_set_reference.version", None)
            else:
                version = DataUtil.get_aml_dataset_version(self.graph.entity_interface,
                                                           param_name=get(node, "data_set_definition.parameter_name"))
            dataset_key = DataUtil.get_dataset_mapping_key(dataset_id, saved_dataset_id, version)
            if dataset_key not in self.dataset_id_2_name.keys():
                # for draft, endpoint and published pipeline, we may not have saved datasetid filled in datanode
                # for registered dataset
                # in this case, we try to find the saved datasetid from datasources with registered dataset id and
                # it's version (if the version is not null)
                if saved_dataset_id:
                    # TODO(1549995): read saved dataset from datasource when backend returns.
                    # add saved dataset to user dataset mapping since currently we do not have it's data source.
                    dataset_name = DataUtil.get_saved_dataset_py_name(saved_dataset_id)
                    self.dataset_id_2_name[dataset_key] = dataset_name
                    dataset_def = node.data_set_definition.value
                    dataset_def.saved_dataset_id = dataset_def.saved_data_set_reference.id
                    self.user_dataset_py_name_2_def[dataset_name] = dataset_def
                else:
                    dataset_key = None
                    if dataset_id:
                        data_sources = self.graph.graph_data_sources
                        source = next(
                            (s for s in data_sources if not _equal_to_enum_val(
                                s.data_source_type, DataSourceType.GLOBAL_DATASET
                            ) and s.id == dataset_id and (not version or s.dataset_version_id == version)), None)
                        dataset_key = source.saved_dataset_id if source else None
                        if not dataset_key:
                            # TODO(1549995): read user dataset from datasource when backend returns.
                            dataset_key = DataUtil.get_dataset_mapping_key(dataset_id, saved_dataset_id, version)
                            dataset_name = _sanitize_python_variable_name(dataset_key)
                            self.dataset_id_2_name[dataset_key] = dataset_name
                            dataset_def = node.data_set_definition.value.data_set_reference
                            dataset_def.dataset_version_id = dataset_def.version
                            self.user_dataset_py_name_2_def[dataset_name] = dataset_def
            if not dataset_key or dataset_key not in self.dataset_id_2_name.keys():
                raise GraphStructureError(f"Unknown data node: {node.as_dict()}")
            py_name = self.dataset_id_2_name[dataset_key]
            # TODO: move user dataset definition collection in here? Need datasource
            return py_name

    def is_default_datastore(self, data_store_name: str, output_definition: StructuredInterfaceOutput):
        if data_store_name and data_store_name != output_definition.data_store_name and (
                data_store_name != get(self.default_datastore, "data_store_name")):
            return False
        return True


def _get_pipeline_identifier(run: Run):
    # Use experiment name + display name to uniquely define a pipeline
    try:
        identifier = _sanitize_python_variable_name(f"{run.display_name}")
    except AttributeError:
        # handle case when azureml-core does not support display name
        identifier = _sanitize_python_variable_name(f"{run.name}")
    return identifier
