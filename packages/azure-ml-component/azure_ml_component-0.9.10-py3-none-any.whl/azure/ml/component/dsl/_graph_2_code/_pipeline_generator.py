# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import os
from collections import OrderedDict

from azure.ml.component.dsl._graph_2_code._component_node_generator import ComponentCodeGenerator, \
    ControlCodeGenerator
from azure.ml.component.dsl._graph_2_code._file_header_generator import CodeFileHeaderGenerator
from azureml.core import Run
from azure.ml.component._restclients.designer.models import (
    PipelineGraph, ModuleDto, ModuleScope
)
from azure.ml.component._util._utils import _get_enum, _sanitize_python_variable_name
from azure.ml.component.dsl._graph_2_code._base_generator import CodeBaseGenerator
from azure.ml.component.dsl._graph_2_code._utils import GraphPackageUtil, GraphUtil, _get_module_file_name, \
    PIPELINE_DEF_TEMPLATE, _is_pipeline_component, GraphStructureError, process_error, _get_pipeline_identifier


class PipelineCodeGenerator(CodeBaseGenerator):
    DEFAULT_PIPELINE_NAME = "generated_pipeline"
    DEFAULT_MODULE_NAME = "root_pipeline"
    DEFAULT_EXPERIMENT_NAME = "sample-experiment-name"
    BATCH_LOAD_THRESHOLD = 5

    def __init__(
            self,
            graph: PipelineGraph,
            pkg_util: GraphPackageUtil,
            logger,
            definition: ModuleDto = None,
            is_root=False,
            module_name=None,
            run: Run = None,
            header: str = None,
            **kwargs
    ):
        super(PipelineCodeGenerator, self).__init__(logger=logger, **kwargs)
        # TODO(1548752): change interface, url, install commands, module name, display name, etc

        self.util = GraphUtil(graph, pkg_util, definition)
        self.pkg_util = pkg_util
        self._is_root = is_root
        self._experiment_name = self.DEFAULT_EXPERIMENT_NAME if not run else run.experiment.name
        self.header = header if header else CodeFileHeaderGenerator(logger=logger).to_component_entry_code()
        if is_root:
            self.definition = None
            self.name = self.DEFAULT_PIPELINE_NAME if not run else _get_pipeline_identifier(run)
            self.description = None
            self.module_name = self.DEFAULT_MODULE_NAME if not module_name else module_name
            self._pipeline_func_name = _sanitize_python_variable_name(self.name)
            self.target_file = _get_module_file_name(self.module_name)
        else:
            if not definition:
                raise RuntimeError("Definition is required for sub pipeline.")
            self.definition = definition
            self.name = definition.module_name
            self.description = definition.description
            self.module_name = self.pkg_util.component_id_2_module_name[self.definition.module_version_id]
            self._pipeline_func_name = self.pkg_util.component_id_2_func_name[self.definition.module_version_id]
            # sub graphs will be generated in Subgraph folder
            self.target_file = os.path.join(
                self.pkg_util.SUBGRAPH_PACKAGE_NAME, _get_module_file_name(self.module_name))

        self._workspace_name = self.util.workspace_name

        self._node_generators = [
            *[ComponentCodeGenerator(node, self.util, self.logger) for node in self.util.sorted_nodes],
            *[ControlCodeGenerator(node, self.util, self.logger) for node in self.util.node_id_2_control.values()]
        ]

        # Mapping from global dataset name to def
        self._global_datasets = self.util.global_dataset_py_name_2_def

        # Mapping from user dataset name to def
        self._user_datasets = self.util.user_dataset_py_name_2_def

        # Mapping from component func name to module version id
        self._anonymous_components_2_def = OrderedDict()
        # Mapping from component func name to component definition
        self._global_components_2_def = OrderedDict()
        # Mapping from component func name to component definition
        self._custom_components_2_def = OrderedDict()
        # Mapping from component func name to it's module name
        self._sub_pipeline_func_name_2_module = OrderedDict()
        # Mapping from generated component func name to it's module name
        self._generated_component_func_2_module = OrderedDict()
        self._get_components()

    @property
    def tpl_file(self):
        return PIPELINE_DEF_TEMPLATE

    @property
    def entry_template_keys(self):
        return [
            "used_dsl_types",
            "used_dataset",
            "used_workspace",
            "used_early_termination_policies",
            "generated_component_func_2_module",
            "used_datastore",
            "sub_pipelines",
            "workspace_name",
            "batch_load",
            "batch_component_funcs",
            "batch_component_ids",
            "batch_anon_component_funcs",
            "batch_anon_component_ids",
            "custom_components",
            "global_components",
            "anonymous_components",
            "global_datasets",
            "user_datasets",
            "dsl_pipeline_params",
            "pipeline_func_name",
            "pipeline_params",
            "component_node_strs",
            "pipeline_outputs",
            "header",
            "dsl_pipeline_param_assignments",
            "pipeline_param_defines",
            "is_root",
            "pipeline_func_name",
            "pipeline_param_assignments",
        ]

    def _get_components(self):
        for module_id in self.util.module_id_2_module.keys():
            func_name = self.pkg_util.component_id_2_func_name[module_id]
            module_name = self.pkg_util.component_id_2_module_name[module_id]
            component_def = self.util.module_id_2_module[module_id]
            component_type = _get_enum(component_def.module_scope, ModuleScope)
            if component_type == ModuleScope.ANONYMOUS and _is_pipeline_component(component_def):
                # handle pipeline imports
                sub_graph_prefix = f"{self.pkg_util.PIPELINE_PACKAGE_NAME}.{self.pkg_util.SUBGRAPH_PACKAGE_NAME}"
                self._sub_pipeline_func_name_2_module[func_name] = f"{sub_graph_prefix}.{module_name}"
            else:
                # all other component func will be imported from generated components folder
                self._generated_component_func_2_module[func_name] = self.pkg_util.COMPONENT_PACKAGE_NAME

    @property
    def used_dsl_types(self):
        return sorted(self.util.used_dsl_types)

    @property
    def used_dataset(self):
        return self.util.used_dataset or self.user_datasets or self.global_datasets

    @property
    def used_workspace(self):
        return self.used_datastore or self.used_dataset

    @property
    def used_datastore(self):
        return self.util.used_datastore

    @property
    def used_early_termination_policies(self):
        used_early_termination_policies = set()
        for node_generator in self._node_generators:
            used_early_termination_policies |= node_generator.util.used_early_termination_policies
        return sorted(used_early_termination_policies)

    @property
    def workspace_name(self):
        return self._workspace_name

    @property
    def sub_pipelines(self):
        return OrderedDict(sorted(self._sub_pipeline_func_name_2_module.items(), key=lambda i: i[0]))

    @property
    def batch_load(self):
        return len(self.util.module_id_2_module) > self.BATCH_LOAD_THRESHOLD

    @property
    def batch_component_funcs(self):
        return list(self._global_components_2_def.keys()) + list(self._custom_components_2_def.keys())

    @property
    def batch_component_ids(self):
        global_component_ids = [repr(c.module_name) for c in self._global_components_2_def.values()]
        custom_component_ids = [
            repr(f"{c.module_name}:{c.module_version}") for c in self._custom_components_2_def.values()]
        return global_component_ids + custom_component_ids

    @property
    def batch_anon_component_funcs(self):
        return list(self._anonymous_components_2_def.keys())

    @property
    def batch_anon_component_ids(self):
        return [repr(c.module_version_id) for c in self._anonymous_components_2_def.values()]

    @property
    def custom_components(self):
        return self._custom_components_2_def

    @property
    def global_components(self):
        return self._global_components_2_def

    @property
    def anonymous_components(self):
        return self._anonymous_components_2_def

    @property
    def generated_component_func_2_module(self):
        return OrderedDict(sorted(self._generated_component_func_2_module.items(), key=lambda i: i[0]))

    @property
    def global_datasets(self):
        return self._global_datasets

    @property
    def user_datasets(self):
        return self._user_datasets

    @property
    def dsl_pipeline_params(self):
        params = {"name": self.name}
        if self.description:
            params["description"] = self.description
        if self.util.graph.default_datastore and self.util.graph.default_datastore.data_store_name:
            params["default_datastore"] = self.util.graph.default_datastore.data_store_name
        if self.util.graph.default_compute and self.util.graph.default_compute.name:
            params["default_compute_target"] = self.util.graph.default_compute.name
        return params

    @property
    def pipeline_func_name(self):
        return self._pipeline_func_name

    @property
    def pipeline_params(self):
        return self.util.pipeline_param_2_actual_val

    @property
    def component_node_strs(self):
        return [g.to_component_entry_code() for g in self._node_generators]

    @property
    def pipeline_outputs(self):
        outputs_dict = {}
        out_edges = [e for e in self.util.graph.edges if e.destination_input_port.graph_port_name]
        for edge in out_edges:
            source_node_id = edge.source_output_port.node_id
            graph_port_name = _sanitize_python_variable_name(edge.destination_input_port.graph_port_name)
            if source_node_id in self.util.node_id_2_var_name.keys():
                arg_name = self.util.get_output_port_arg_name(edge.source_output_port)
                outputs_dict[graph_port_name] = f"{self.util.node_id_2_var_name[source_node_id]}.outputs.{arg_name}"
            else:
                process_error(GraphStructureError(
                    f"Failed to find edge {edge}'s source node in source node list: {self.util.node_id_2_var_name}"))
        return outputs_dict

    @property
    def is_root(self):
        return self._is_root

    @property
    def dsl_pipeline_param_assignments(self):
        return {name: repr(val) for name, val in self.dsl_pipeline_params.items()}

    @property
    def pipeline_param_defines(self):
        return self.util.pipeline_param_2_default_val

    @property
    def pipeline_param_assignments(self):
        # Skip None val
        return {name: val for name, val in self.pipeline_params.items() if val}
