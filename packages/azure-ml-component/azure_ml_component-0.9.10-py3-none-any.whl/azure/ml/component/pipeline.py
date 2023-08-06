# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Contains classes for creating and managing reusable computational units of an Azure Machine Learning pipeline.

An Azure Machine Learning pipeline is an independently executable workflow of a complete machine learning task.
Azure Machine Learning pipelines help you build, optimize, and manage machine learning workflows with simplicity,
repeatability and quality assurance.

A pipeline can be composited by several Components.

These benefits become significant as soon as your machine learning project moves beyond pure exploration and into
iteration. Even simple one-step pipelines can be valuable. Machine learning projects are often in a complex state,
and it can be a relief to make the precise accomplishment of a single workflow a trivial process.

"""
import functools
import os
import copy
from inspect import Parameter
from pathlib import Path
import tempfile
import uuid
import concurrent.futures
from typing import List, Union, Mapping, Callable, Dict, Any, TypeVar, Generic

from azureml.core import Experiment
from azureml.data.data_reference import DataReference
from azureml.data.datapath import DataPath

from ._api._api import _DefinitionInterface
from ._core import ComponentType
from .component import Component, Output, Input, _InputsAttrDict, _OutputsAttrDict
from azure.ml.component._core._types import _GroupAttrDict
from .run import Run
from ._pipeline_parameters import PipelineParameter
from ._pipeline_component_definition_builder import PipelineComponentDefinitionBuilder, \
    _add_component_to_current_definition_builder, _definition_builder_stack, _build_pipeline_parameter
from ._dataset import _GlobalDataset, _FeedDataset
from ._execution._pipeline_run_orchestrator import PipelineRunOrchestrator
from ._execution._component_run_helper import RunMode
from ._execution._tracker import RunHistoryTracker
from ._graph import _GraphEntityBuilder, _GraphEntityBuilderContext
from ._component_validator import ComponentValidator, Diagnostic
from ._visible import Visible
from ._visualization_context import VisualizationContext
from ._pipeline_validator import PipelineValidator
from ._published_pipeline import PublishedPipeline
from ._restclients.service_caller_factory import _DesignerServiceCallerFactory
from ._restclients.designer.models import SubmitPipelineRunRequest, PipelineDraft, \
    CreatePublishedPipelineRequest, DataInfo, GraphDraftEntity, GeneratePipelineComponentRequest, \
    ModuleScope, CloudPrioritySetting, PriorityConfiguration
from ._parameter_assignment import _ParameterAssignment
from ._util._attr_dict import _AttrDict
from ._util._exceptions import PipelineValidationError, UserErrorException, wrap_azureml_exception_with_identifier
from ._util._loggerfactory import _LoggerFactory, _PUBLIC_API, track, timer
from ._util._telemetry import WorkspaceTelemetryMixin, _get_telemetry_value_from_pipeline_parameter
from ._util._utils import _get_short_path_name, _is_prod_workspace, trans_to_valid_file_name, \
    enabled_subpipeline_registration, resolve_pipeline_parameters, ensure_valid_experiment_name, \
    find_output_owner_in_current_pipeline, is_valid_component_name, _sanitize_python_variable_name, \
    COMPONENT_NAME_MAX_LEN, _get_parameter_static_value
from ._core._run_settings_definition import RunSettingsDefinition

_logger = None
ORIGINAL_NODE_ID = "_copied_id"
T = TypeVar('T')


def _get_logger():
    global _logger
    if _logger is not None:
        return _logger
    _logger = _LoggerFactory.get_logger()
    return _logger


class Pipeline(Component, Visible, WorkspaceTelemetryMixin, Generic[T]):
    """A Pipeline aggregates other Components and connects their inputs and outputs to form a pipeline."""

    def __init__(self, nodes: List[Union[Component, 'Pipeline']],
                 outputs: Mapping[str, Output] = None,
                 workspace=None, name=None, description=None,
                 default_compute_target=None, default_datastore=None, _use_dsl=False,
                 _definition=None, _init_params=None, _is_direct_child=True):
        """
        Initialize Pipeline.

        :param nodes: The nodes of component used to create the pipeline.
        :type nodes: list[azure.ml.component.Component
            or azure.ml.component.Pipeline]
        :param outputs: The pipeline outputs.
        :type outputs: dict
        :param workspace: The workspace of the pipeline
        :type workspace: azureml.core.Workspace
        :param name: The name of the pipeline
        :type name: str
        :param description: The description of the pipeline
        :type description: str
        :param default_compute_target: The compute target name of built pipeline.
            The priority of compute target assignment goes: module's run settings >
            sub pipeline's default compute target > parent pipeline's default compute target.
        :type default_compute_target: str
        :param default_datastore: The default datastore of pipeline.
        :type default_datastore: str or azureml.core.Datastore
        :param _use_dsl: Whether created by @dsl.pipeline
        :type _use_dsl: bool
        :param _definition: the definition of pipeline component
        :type _definition: _PipelineComponentDefinition
        :param _init_params: the pipeline parameters from input
        :type _init_params: dict
        :param _is_direct_child: If there is a pipeline component definition
            is_direct_child means whether the component is current definition's direct child.
        :type _is_direct_child: bool
        """
        if outputs is None:
            outputs = {}
        if _definition is None:
            _definition = PipelineComponentDefinitionBuilder.from_nodes(
                nodes=nodes, name=name, workspace=workspace, pipeline_outputs=outputs,
                description=description, default_compute_target=default_compute_target,
                default_datastore=default_datastore).create_definition()
        # Point to the condition component if self is control by it.
        self._control_by = None
        self._definition = _definition
        self._name_to_argument_name_mapping = {
            **{p.name: arg for arg, p in _definition.inputs.items()},
            **{p.name: arg for arg, p in _definition.parameters.items()},
            **{p.name: arg for arg, p in _definition.outputs.items()},
        }
        # If current pipeline not direct child from a definition component(child node of direct_child)
        # or definition stack is not empty, then it is a sub pipeline.
        self._is_sub_pipeline = not _is_direct_child or not _definition_builder_stack.is_empty()
        self._is_direct_child = _is_direct_child

        _init_params, _, _ = resolve_pipeline_parameters(_init_params)
        self._init_params = _init_params
        self._workspace = _definition.workspace
        self._description = description
        self._instance_id = str(uuid.uuid4())
        self._name = name if name is not None else self._definition.name
        self._node_name = None

        _copied_id_field = ORIGINAL_NODE_ID
        if not _use_dsl:
            # Tuple type to make nodes immutable
            self._nodes = (*self._definition.components.values(), )
            self._outputs_mapping = _OutputsAttrDict(outputs)
            self._inputs = _InputsAttrDict(_init_params)
        else:
            # Tuple type to make nodes immutable
            self._nodes = (*self._copy_nodes(
                nodes, _copied_id_field, **_init_params), )
            self._copy_outputs(outputs, _copied_id_field)

        if self._is_sub_pipeline:
            # Generate the sub pipeline output which dset owner is the pipeline.
            pipeline_outputs = {}
            for k, v in self._outputs_mapping.items():
                pipeline_outputs[k] = copy.copy(v)
                pipeline_outputs[k]._owner = self
                pipeline_outputs[k]._port_name = k
                pipeline_outputs[k]._name = k
            self._outputs = _OutputsAttrDict(pipeline_outputs)
        else:
            self._outputs = self._outputs_mapping

        # Note self.workspace is only available after self.nodes is set.
        WorkspaceTelemetryMixin.__init__(self, workspace=self.workspace)
        self._default_datastore = default_datastore
        self._default_compute_target = default_compute_target
        self._extra_input_settings = {}
        self._description = description
        self._parent = None
        self._resolve_node_id_variable_name_dict()
        if _is_direct_child:
            # If is copied node, skip parameter validation to avoid duplicate warning.
            self._validate_parameters(self._init_params)
        # Validate if all the input source(node/parameter) can be found in current pipeline context.
        self._validate_all_input_source()

        self._use_dsl = _use_dsl
        self._comment = None
        self._friendly_instance_name = None

        from ._sub_pipeline_info_builder import _build_sub_pipeline_definition
        all_parameters = list(_definition._parameters.values())
        all_parameters.extend(list(_definition.inputs.values()))
        self._pipeline_definition = _build_sub_pipeline_definition(
            name=self._name, description=self._description,
            default_compute_target=_definition._default_compute_target,
            default_data_store=default_datastore, id=_definition._id,
            parent_definition_id=_definition._parent_definition_id,
            from_module_name=_definition._from_module_name,
            parameters=all_parameters,
            func_name=_definition._pipeline_function_name)
        self._init_dynamic_method()

        # correct sub pipelines filed `is_sub_pipeline`
        for node in self.nodes:
            node._parent = self
            if isinstance(node, Pipeline):
                node._is_sub_pipeline = True

        self._regenerate_outputs = None
        # init structured interface for validation
        self._init_structured_interface()
        # whether workspace independent component exist in pipeline.
        # NOTE: There maybe some scenario pipeline has workspace but component not.
        self._workspace_independent_component_exists = any(
            node._workspace is None or (node._is_pipeline and node._workspace_independent_component_exists)
            for node in self.nodes)
        # Init runsettings
        self._runsettings = RunSettingsDefinition.build_interface_for_pipeline(self)
        if _is_direct_child:
            _add_component_to_current_definition_builder(self)

    @property
    def name(self):
        """
        Get or set the name of the Pipeline.

        :return: The name.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def description(self):
        """
        Get or set the description of the Pipeline.

        :return: The description.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        self._description = description

    @property
    def nodes(self):
        """
        Get the nodes of the Pipeline.

        :return: The nodes.
        :rtype: tuple(nodes)
        """
        return self._nodes

    @nodes.setter
    def nodes(self, nodes):
        raise UserErrorException("Immutable attribute 'nodes' can't be set.")

    @property
    def inputs(self) -> _AttrDict[str, Input]:
        """
        Get the inputs of the Pipeline.

        :return: pipeline inputs.
        :rtype: dict[str, Input]
        """
        # Note here we return component inputs and parameters
        # which is different from component definition
        return self._inputs

    @property
    def outputs(self) -> Union[T, _AttrDict[str, Output]]:
        """
        Get the outputs of the Pipeline.

        :return: pipeline outputs.
        :rtype: dict[str, Output]
        """
        return self._outputs

    @property
    def runsettings(self):
        """
        Get run settings of the Pipeline, overriding this for better type annotation for PipelineRunSettings.

        :return: The run settings.
        :rtype: azure.ml.component.PipelineRunSettings
        """
        return self._runsettings

    @property
    def workspace(self):
        """
        Get the workspace of the Pipeline.

        :return: The workspace.
        :rtype: azureml.core.Workspace
        """
        return self._definition.workspace

    def _get_instance_id(self):
        return self._id

    @property
    def default_compute_target(self):
        """
        Get the default compute target name of the Pipeline.

        :return: The compute target name of built pipeline.
            The priority of compute target assignment goes: module's run settings >
            sub pipeline's default compute target > parent pipeline's default compute target.
        :rtype: str
        """
        return self._get_default_compute_target()[0]

    @property
    def default_datastore(self):
        """
        Get the default datastore of the Pipeline.

        :return: the default datastore.
        :rtype: str
        """
        return self._default_datastore

    @property
    def _is_pipeline(self):
        """Return the component is a pipeline or not.

        :return: The result.
        :rtype: bool
        """
        return True

    @property
    def _input_ports(self):
        """Return the input ports of component.

        :return: The input ports.
        :rtype: dict
        """
        return {k: v for k, v in self._inputs.items() if k in self._definition.inputs}

    @property
    def _parameter_params(self):
        """Return the parameters of component.

        :return: The parameters.
        :rtype: dict
        """
        return {k: v for k, v in self._inputs.items() if k in self._definition.parameters}

    def _resolve_node_id_variable_name_dict(self):
        """
        Resolve node id to variable name dict.

        This dict is used to store variable name definied by user
            inside dsl.pipeline function, for example, `p1=pipeline()`,
            then p1 is the variable name of the pipeline node.
        """
        components_names = self._definition._components_variable_names
        self._node_id_variable_name_dict = {}
        # Assert number of unique node names generated and collected equals nodes number,
        # For the node name here will be used as the unique name of the node when build graph.
        # Generate function: _update_components_variable_names in pipeline component definition builder.
        if len(set(components_names)) != len(self.nodes):
            raise Exception(
                f'Number of components in pipeline {self.name} does not match the number of unique component names!')
        self._node_id_variable_name_dict = {
            node._id: components_names[idx]
            for idx, node in enumerate(self.nodes) if components_names[idx] is not None}

    def _copy_nodes(self, original_nodes, _copied_id_field, **kwargs):
        """
        Copy nodes of original nodes with new input kwargs.

        Direct child of pipeline is copied from definition component.
        Children of child is copied from definition components' nodes.
        """
        nodes = []
        # Add default parameter before build node
        # Create new if group parameter is from definition default
        # Wrap None with pipeline parameter to distinguish with input not set scenario(?)
        kwargs.update({
            name: copy.deepcopy(param._default) if isinstance(param._default, _GroupAttrDict) else param._default
            for name, param in self._definition.parameters.items()
            if name not in kwargs.keys() and param._default is not Parameter.empty})
        # Add parameters
        inputs_mapping = {_k: _v for _k, _v in kwargs.items() if _k in self._definition.parameters}

        # Attention: Do not change the owner of Input, because they may from component inputs.
        def _add_ports_to_inputs_mapping():
            # Note: If input data is None, it will be wrapped as PipelineParameter(None)
            # then wrapped again with Input because all input must be Input type
            inputs_mapping.update({
                _k: _v if isinstance(_v, Input) else Input(dset=_v, name=_k)
                for _k, _v in kwargs.items() if _k in self._definition.inputs})
            # Update default values from definition
            inputs_mapping.update({
                _k: Input(dset=_v.default_value, name=_k)
                for _k, _v in self._definition._pipeline_parameters.items()
                if _k in self._definition.inputs and _k not in inputs_mapping})
        _add_ports_to_inputs_mapping()
        self._inputs = _InputsAttrDict(inputs_mapping)

        # Wrap args with PipelineParameter/InputBuilder
        kwargs = _build_pipeline_parameter(func=None, kwargs=kwargs)

        def copy_params(_kwargs, param_dict, old_to_new_dict):
            """Copy params in param dict to kwargs, replace the input/output builder to the correct one."""
            def update_value(value):
                _value = value
                # Replace pipeline data with the new one
                if isinstance(_value, Output):
                    # Only dsl pipeline will reach here and nodes already topology sorted,
                    #   indicates that the inputs of node must exists inside(replace) or outside(not replace).
                    if _value._owner._id in old_to_new_dict.keys():
                        _value = old_to_new_dict[_value._owner._id].outputs[_value._name]
                elif isinstance(_value, Input):
                    if _value._owner is not None:
                        _value = old_to_new_dict[_value._owner._id]._input_ports[_value._name]
                elif isinstance(_value, Component):
                    # Only dsl pipeline will reach here and nodes already topology sorted,
                    #   indicates that the inputs of node must exists inside(replace) or outside(not replace).
                    if _value._id in old_to_new_dict.keys():
                        _value = old_to_new_dict[_value._id]
                elif isinstance(_value, _GroupAttrDict):
                    _value = copy.deepcopy(_value)
                return _value

            for _k, _v in param_dict.items():
                if _k in _kwargs.keys():
                    continue
                value = update_value(_v) if type(_v) is not dict \
                    else {key: update_value(val) for key, val in _v.items() if update_value(val) is not None}
                _kwargs[_k] = value

        def get_old_to_new_dict(comp):
            """Get the dict of original node id to copy node."""
            pipeline_nodes = comp._expand_pipeline_nodes()
            _dict = {
                getattr(node, _copied_id_field): node
                for node in pipeline_nodes if hasattr(node, _copied_id_field)}
            _dict.update({
                getattr(node, _copied_id_field): node
                for node in comp._expand_pipeline_to_pipelines() if hasattr(node, _copied_id_field)})
            return _dict

        def copy_component_init(node):
            """
            Create a component with new kwargs and the same _init_params of node.

            Notice that configuration added using .configure() includes
                runsetting, inputs and parameters will not be added here.
            """
            sub_definition = original_node._definition
            # Convert arg keys to new keys by using match dict in definition
            _kwargs = self._definition._convert_component_kwargs(kwargs, _index)

            # Add default parameter from component definition
            component_default_args = original_node._init_params
            copy_params(_kwargs, component_default_args, old_to_new_dict)
            if node._is_pipeline:
                _c = Pipeline(
                    nodes=node.nodes, outputs=node._outputs_mapping, name=node.name, description=node.description,
                    _definition=sub_definition, workspace=node.workspace, _use_dsl=True,
                    default_datastore=node._default_datastore, default_compute_target=node._default_compute_target,
                    _init_params=_kwargs, _is_direct_child=False)
                old_to_new_dict.update(get_old_to_new_dict(_c))
            else:
                _c = Component(sub_definition, _init_params=_kwargs, _is_direct_child=False)
            # Copy the real comment value
            _c._comment = node._comment
            # Resolve and get a new object if comment is an ParameterAssignment
            if isinstance(_c._comment, _ParameterAssignment):
                _c._comment = _ParameterAssignment.resolve(_c._comment.formatter, kwargs, print_warning=False)
            return _c

        def update_component_extra_settings(_pipeline_parameters, complete_node, unfinished_node):
            """
            Update extra input/parameter/run settings of new node.

            The complete_node is from pipeline definition components, the unfinished_node already
            copied initial config from it and now we are going to copy the runsettings and extra input settings,
            because runsettings are set after component created and so does extra_input_settings,
            extra inputs settings record the inputs and parameters using set_inputs function.
            """
            updated_inputs = {}
            # Replace inputs with the correct one of new node if output builder
            extra_input_settings = {** complete_node._extra_input_settings}
            # Append those different literal values set via `inputs.param=literal`,
            # which not pass through `set_inputs` and not be added into `extra_input_settings`
            ignored_types = (type(None), PipelineParameter, _ParameterAssignment, Input, _GroupAttrDict)
            current_inputs = {
                k: v for k, v in unfinished_node._parameter_params.items()
                if type(v) not in ignored_types}
            current_inputs.update({
                k: v._dset for k, v in unfinished_node._input_ports.items()
                if type(v._dset) not in ignored_types})
            diff_inputs = {
                k: v for k, v in complete_node._parameter_params.items()
                if type(v) not in ignored_types and id(v) != id(current_inputs.get(k))}
            diff_inputs.update({
                k: v._dset for k, v in complete_node._input_ports.items()
                if type(v._dset) not in ignored_types and id(v._dset) != id(current_inputs.get(k))})
            # Filter different literal values
            extra_input_settings.update(** diff_inputs)
            copy_params(updated_inputs, extra_input_settings, old_to_new_dict)
            # Update input value if is pipelineparameter auto wrapped
            # e.g.
            # @dsl.pipeline
            # def pipeline(param):
            #   comp = func()
            #   comp.set_inputs(a=param)
            # Here we will give param a default value None when build pipeline definition,
            #   so the comp._extra_input_settings will be PipelineParameter('param', None).
            # Then we build a real pipeline 'pipeline(param=1)',
            #   the comp._extra_input_settings should be updated to PipelineParameter('param', 1).
            for _k, _v in updated_inputs.items():
                value = _v._get_internal_data_source() if isinstance(_v, Input) else _v
                if isinstance(value, PipelineParameter) and value._auto_wrap_for_build:
                    updated_inputs[_k] = _pipeline_parameters[_v.name]
                elif isinstance(value, _ParameterAssignment):
                    updated_inputs[_k] = _ParameterAssignment.resolve(
                        value.formatter, {** value.assignments_values_dict, **kwargs})
            if len(updated_inputs) > 0:
                # If there are no updated inputs, parameter assignments shall not be
                # re-calculated with pipeline parameter
                unfinished_node._extra_input_settings = updated_inputs
                unfinished_node.set_inputs(**updated_inputs)

            # Copy special runsettings & k8s runsettings
            # If local run component without register, there will be no workspace binding and
            # the runsettings/k8srunsettings could be None.
            if complete_node._specify_runsettings:
                unfinished_node.runsettings._copy_and_update(
                    complete_node.runsettings, kwargs, pipeline_name=self.name)
            if not complete_node._is_pipeline and complete_node._specify_k8srunsettings:
                unfinished_node.k8srunsettings._copy_and_update(
                    complete_node._k8srunsettings, kwargs, pipeline_name=self.name)

            # Correct all assignments include inputs/runsettings/comment
            unfinished_node._update_parameter_assignments_with_pipeline_parameter(kwargs, print_warning=False)

            # Update inputs properties
            for name, input in complete_node._input_ports.items():
                unfinished_node.inputs[name]._configure(
                    mode=input.mode,
                    path_on_compute=input._path_on_compute
                )

            # Update outputs properties
            for name, output in complete_node.outputs.items():
                unfinished_node.outputs[name]._dataset_registration = output._dataset_registration
                unfinished_node.outputs[name]._dataset_output_options = output._dataset_output_options
                unfinished_node.outputs[name]._configure(
                    output_mode=output.mode, datastore=output.datastore,
                    path_on_compute=output._path_on_compute,
                )

            # Update regenerate output
            unfinished_node._regenerate_outputs = complete_node._regenerate_outputs

            # Copy the control by information
            if complete_node._control_by is not None:
                control_component, edge_type = complete_node._control_by
                if control_component._id not in old_to_new_dict:
                    raise UserErrorException(
                        f'The control component {control_component.name!r} of '
                        f'component {complete_node.name!r} not found in scope of current pipeline: {self.name!r}.')
                unfinished_node._set_control_by(old_to_new_dict[control_component._id], edge_type)

        # Used to replace component inside output builder to new component
        old_to_new_dict = {}
        for _index, original_node in enumerate(original_nodes):
            _id = original_node._id
            component = copy_component_init(original_node)
            setattr(component, _copied_id_field, _id)
            old_to_new_dict[_id] = component
            nodes += (component,)

        # Copy extra inputs/parameters config and run settings
        for original_node, node in zip(original_nodes, nodes):
            update_component_extra_settings(kwargs, original_node, node)

        return nodes

    def _validate_all_input_source(self):
        """Validate if all input source can be found in current pipeline context."""
        # Pipeline inputs already extracted.
        all_inputs = set(self.inputs.keys())

        def validate_input(source):
            # Resolve input from component which has exactly one output
            if isinstance(source, Component):
                # Size of output == 1 already checked when build Input before.
                source = list(source.outputs.values())[0]

            # Skip check assignment because a parameter not found warning will be print when resolving.
            if isinstance(source, PipelineParameter) or isinstance(source, Input):
                # Get group param name if is from group, else is source name
                source_name = source._groups[0] \
                    if isinstance(source, PipelineParameter) and source._groups else source.name
                # Check is current pipeline's parameter or not
                if source_name not in all_inputs:
                    raise UserErrorException(
                        f'Parameter {source_name!r} not found in scope of current pipeline: '
                        f'{self.name!r}. Please pass it as pipeline function parameter.')
            elif isinstance(source, Output):
                find_output_owner_in_current_pipeline(source, self.nodes, self.name)

        # Validate if inputs contains nodes/parameter outer pipeline
        for node in self.nodes:
            # Get original inputs before wrapper avoid extract from component inputs.
            node_inputs = {**node._init_params}
            node_inputs.update(node._extra_input_settings)
            node_inputs = list(node_inputs.values())
            if node_inputs is None:
                continue
            for _input in node_inputs:
                validate_input(_input)

    def _copy_outputs(self, _original_outputs, _copied_id_field):
        """Map original outputs to new to set pipeline inputs."""
        old_to_new_dict = {getattr(node, _copied_id_field): node
                           for node in self.nodes if hasattr(node, _copied_id_field)}
        for output in _original_outputs.values():
            if output._owner._id not in old_to_new_dict.keys():
                # Owner is not one of the pipeline's node
                raise UserErrorException(
                    f'Component of output \'{output.port_name}\' not found '
                    f'in scope of current pipeline: \'{self.name}\'.')
        # Use original outputs owner id to find new owners' outputs port
        outputs = {_k: old_to_new_dict[_v._owner._id]._outputs[_v._name]
                   for _k, _v in _original_outputs.items()}
        # Used to record the mapping of outputs of component in the pipeline and the pipeline outputs,
        # the dst owner is the component.
        self._outputs_mapping = _OutputsAttrDict(outputs)

    def _update_parameter_assignments_with_pipeline_parameter(self, pipeline_parameters, print_warning=True):
        """Update current parameter assignments with newly pipeline parameter."""
        # Update current pipeline's parameter assignments.
        super()._update_parameter_assignments_with_pipeline_parameter(pipeline_parameters, print_warning)
        # Update nodes parameter after self._parameter_params updated.
        # Wrap parameter with PipelineParameter to record the source parameter name.
        wrapped_parameter = {}
        for k, v in pipeline_parameters.items():
            if not isinstance(v, (PipelineParameter, Input, _GroupAttrDict)):
                v = Input(name=k, dset=v) if isinstance(v, _ParameterAssignment) \
                    else PipelineParameter(name=k, default_value=v)
            wrapped_parameter[k] = v
        for node in self.nodes:
            node._update_parameter_assignments_with_pipeline_parameter(wrapped_parameter, print_warning)

    @timer()
    def _get_default_compute_target(self, default_compute_target=None, ignore_runsettings=False,
                                    pipeline_parameters={}, workspace=None):
        """
        Try to resolve the default compute target to tuple(compute_name, compute_type).

        :param default_compute_target
        :type default_compute_target: str or AmlCompute or tuple(str, str)
        :param ignore_runsettings: indicate ignore runsettings.target or not. For pipeline component
        registration, we need to ignore runsettings, as it's not the default compute target in definition
        :type ignore_runsettings: bool
        :param pipeline_parameters: Only needed when ignore_runsettings is False, and runsettings.target is
        linked as pipeline parameter and it's changed when submission
        :type pipeline_parameters: dict
        :param workspace: Workspace
        :type workspace: azureml.core.Workspace
        :return: default compute target
        :rtype: tuple(str, str)
        """
        workspace = workspace or self.workspace
        if default_compute_target is None:
            default_compute_target = self._default_compute_target
            if not ignore_runsettings:
                # Check if runsettings.target is ParameterAssignment
                res = self.runsettings.target
                if isinstance(res, str):
                    res = _ParameterAssignment.resolve(res, {}, print_warning=False)
                if isinstance(res, _ParameterAssignment):
                    raise UserErrorException("ParameterAssignment is not supported for `runsetting.target`.")
                default_compute_target = _get_parameter_static_value(
                    res, pipeline_parameters) or default_compute_target

        if default_compute_target is None:
            return None, "AmlCompute"

        # try to resolve compute target
        if isinstance(default_compute_target, str):
            if workspace is None:
                # all nodes are workspace independent component in pipeline
                return default_compute_target, None
            target = self._get_compute_in_workspace_by_name(default_compute_target, workspace)
            if target is None:
                _get_logger().warning(default_compute_target + " not found in workspace, assume this is an AmlCompute")
                return default_compute_target, "AmlCompute"
            else:
                return target.name, target.compute_type
        elif isinstance(default_compute_target, tuple):
            if not len(default_compute_target) == 2:
                raise ValueError('Compute target tuple must have 2 elements (compute name, compute type)')
            return default_compute_target
        else:
            raise ValueError('Compute target must be a string')

    def _get_compute_in_workspace_by_name(self, compute_name: str, workspace=None):
        """
        Get compute by name. Return None if compute does not exist in current workspace.

        :param compute_name: The compute name
        :type compute_name: str
        :param workspace: Workspace
        :type workspace: azureml.core.Workspace
        :return: compute
        :rtype: ~designer.models.ExperimentComputeMetaInfo or None
        """
        service_caller = _DesignerServiceCallerFactory.get_instance(workspace or self.workspace)
        return service_caller.get_compute_by_name(compute_name)

    def set_inputs(self, *args, **kwargs) -> 'Component':
        """Update the inputs and parameters of the pipeline component.

        :return: The pipeline component itself.
        :rtype: azure.ml.component.Component
        """
        # Note that the argument list must be "*args, **kwargs" to make sure
        # vscode intelligence works when the signature is updated.
        # https://github.com/microsoft/vscode-python/blob/master/src/client/datascience/interactive-common/intellisense/intellisenseProvider.ts#L79
        # Parameters with default None will be added for method intelligence.
        kwargs, _, _ = resolve_pipeline_parameters(kwargs, remove_empty=True)
        if self._is_direct_child:
            # If is copied node, skip parameter validation to avoid duplicate warning.
            self._validate_parameters(kwargs)
        # The parameter will be updated first, then the nodes will be updated recursively.
        # After nodes updated, pipeline inputs will be resolved from nodes inputs.
        # Which means pipeline's inputs will not be updated by using kwargs directly.
        # Notice that None input value will be ignored.
        self._inputs.update(
            {_k: _v for _k, _v in kwargs.items() if _v is not None and _k in self._parameter_params})
        if self._is_direct_child:
            # Only leave valid kwargs to avoid duplicate warnings.
            self._extra_input_settings.update(kwargs)
            # Use current build's parameter to resolve assignments if exist.
            from ._pipeline_component_definition_builder import _try_resolve_assignments_and_update_parameters
            _try_resolve_assignments_and_update_parameters(self)
        # Use wrapped args update inputs
        # Attention: Do not change the owner of Input, because they may from component inputs.
        self._inputs.update({
            _k: _v if isinstance(_v, Input) else Input(dset=_v, name=_k)
            for _k, _v in kwargs.items() if _k in self._input_ports})
        # Wrap parameter args with PipelineParameter, add Inputs
        kwargs = _build_pipeline_parameter(func=None, kwargs=kwargs)
        all_parameters = _build_pipeline_parameter(func=None, kwargs=self._parameter_params)
        # Update node inputs
        for idx, node in enumerate(self.nodes):
            # Only convert kwargs to determine whether node.set_inputs is required.
            _kwargs = self._definition._convert_component_kwargs(kwargs, idx)
            if len(_kwargs) > 0:
                node.set_inputs(*args, **_kwargs)
            # Use updated current pipeline parameter update component's parameter assignment
            # Here we use full wrapped pipeline parameter.
            node._update_parameter_assignments_with_pipeline_parameter(all_parameters)
        self._validate_all_input_source()
        return self

    @track(activity_type=_PUBLIC_API, flush=True)
    def submit(self, experiment_name=None, default_compute_target=None, default_datastore=None, description=None,
               pipeline_parameters=None, tags=None, continue_on_step_failure=None, regenerate_outputs=None, *,
               skip_validation=False, display_name=None, workspace=None, force_rerun=None) \
            -> Run:
        """
        Submit current pipeline run to workspace.

        :param experiment_name: The experiment name, if experiment_name is None will default to pipeline name
        :type experiment_name: str
        :param default_compute_target: The default compute target used to run pipeline
        :type default_compute_target: str
        :param default_datastore: The default datastore.
        :type default_datastore: str
        :param description: The description of the submitted pipeline run
        :type description: str
        :param pipeline_parameters: An optional dictionary of pipeline parameter assignments for the PipelineDraft
        :type pipeline_parameters: dict
        :param tags: Tags to be added to the submitted run, {"tag": "value"}
        :type tags: dict
        :param continue_on_step_failure: Indicates whether to continue pipeline execution if a step fails.
            If True, only steps that have no dependency on the output of the failed step will continue execution.
        :type continue_on_step_failure: bool
        :param regenerate_outputs: Indicates whether to force regeneration of all step outputs and disallow data
            reuse for this run. If False, this run may reuse results from previous runs and subsequent runs may reuse
            the results of this run.
        :type regenerate_outputs: bool
        :param skip_validation: Set this parameter True to skip pipeline validation triggered before submit.
        :type skip_validation: bool
        :param display_name: The display name of the submitted pipeline run.
        :type display_name: str
        :param workspace: When workspace independent components exist in pipeline, workspace need to be specified.
                          It will use the workspace to register the workspace independent components.
        :type workspace: azureml.core.Workspace
        :param force_rerun: True to indicate force rerun all child runs under this root pipeline run, all child runs
            will not latch/reuse to any run and cannot be latched/reused by other runs, False to indicate set
            regenerate_output of all child runs to False and do common reuse logic. Default value is None.
        :type force_rerun: bool

        :return: The submitted run.
        :rtype: azure.ml.component.Run
        """
        if len(self._outputs_mapping) != len(set(self._outputs_mapping.values())):
            raise UserErrorException(
                "Pipeline submit does not support duplicate component output as pipeline output.")

        # Params validation
        self._validate_pipeline_tags(tags)
        workspace = workspace or self.workspace
        self._ensure_registered_in_workspace(workspace)
        data_path_assignments = {}
        if pipeline_parameters:
            pipeline_parameters, __, data_path_assignments = resolve_pipeline_parameters(
                pipeline_parameters,
                resolve_data_path=True,
                outputs=self.outputs.keys(),
                parameters_and_inputs=list(self._parameter_params.keys()) + list(self._input_ports.keys()),
            )

        default_compute_target = self._get_default_compute_target(default_compute_target, workspace=workspace)
        # _parameter_params should also added, or else component parameter will be treated as constants.
        pipeline_parameters = self._expand_default_pipeline_parameters(pipeline_parameters)

        enable_subpipeline_registration = enabled_subpipeline_registration()
        graph_entity_builder = self._get_graph_builder(pipeline_parameters=pipeline_parameters,
                                                       compute_target=default_compute_target,
                                                       default_datastore=default_datastore,
                                                       regenerate_outputs=regenerate_outputs,
                                                       workspace=workspace)

        if enable_subpipeline_registration:
            graph, module_node_run_settings = graph_entity_builder.build_graph_entity(
                enable_subpipeline_registration=enable_subpipeline_registration, default_datastore=default_datastore)
            sub_pipelines_info = None
            if not skip_validation:
                self._validate(pipeline_steps=None,
                               raise_error=True,
                               pipeline_parameters=pipeline_parameters,
                               default_compute=default_compute_target,
                               default_datastore=default_datastore,
                               workspace=workspace)
        else:
            graph, module_node_run_settings = graph_entity_builder.build_graph_entity(
                enable_subpipeline_registration=enable_subpipeline_registration, default_datastore=default_datastore)
            sub_pipelines_info = self._build_sub_pipeline_info(graph.module_node_to_graph_node_mapping,
                                                               pipeline_parameters)
            if not skip_validation:
                context = self._get_visualization_context(graph=graph,
                                                          sub_pipelines_info=sub_pipelines_info,
                                                          compute_target=default_compute_target,
                                                          pipeline_parameters=pipeline_parameters,
                                                          workspace=workspace)
                self._validate(pipeline_steps=context.step_nodes,
                               raise_error=True,
                               pipeline_parameters=pipeline_parameters,
                               default_compute=default_compute_target,
                               default_datastore=default_datastore,
                               workspace=workspace)

        compute_target_name, _ = default_compute_target
        experiment_name = ensure_valid_experiment_name(experiment_name, self._definition.display_name or self.name)
        data_path_assignments = {**graph_entity_builder.data_path_assignments, **data_path_assignments}

        if self.runsettings.priority.scope is not None:
            graph.default_cloud_priority = CloudPrioritySetting(
                scope_priority=PriorityConfiguration(cloud_priority=self.runsettings.priority.scope))

        if not description:
            description = self.description or self._definition.display_name or self.name
        request = SubmitPipelineRunRequest(
            experiment_name=experiment_name,
            description=description,
            compute_target=compute_target_name,
            display_name=display_name if display_name else self._definition.display_name,
            graph=graph,
            module_node_run_settings=module_node_run_settings,
            tags=tags,
            continue_run_on_step_failure=continue_on_step_failure,
            sub_pipelines_info=sub_pipelines_info,
            data_path_assignments=data_path_assignments,
            enforce_rerun=force_rerun
            # Pipeline parameters already resolved into graph, no need to added here.
        )

        run = self._submit_pipeline(request=request, workspace=workspace)

        module_nodes = self._expand_pipeline_nodes()
        input_to_data_info_dict = self._build_input_to_data_info_dict(module_nodes, pipeline_parameters)

        telemetry_value = self._get_telemetry_values(
            pipeline_parameters=pipeline_parameters,
            compute_target=default_compute_target,
            data_sources=input_to_data_info_dict.values(),
            sub_pipelines_info=sub_pipelines_info,
            additional_value={
                'run_id': run.id,
                'skip_validation': skip_validation
            },
            workspace=workspace)

        _LoggerFactory.add_track_dimensions(_get_logger(), telemetry_value)

        return run

    @timer()
    def _submit_pipeline(self, request: SubmitPipelineRunRequest, workspace=None) -> Run:
        submit_workspace = self.workspace or workspace
        service_caller = _DesignerServiceCallerFactory.get_instance(submit_workspace)
        # Special case for kubeflow
        draft_id = None
        compute_target_name = request.compute_target
        if compute_target_name is not None and "kubeflow" in compute_target_name:
            draft = self._save_pipeline_as_draft(_id=None, request=request, workspace=submit_workspace)
            draft_id = draft.id
            run_id = service_caller.submit_pipeline_draft_run(request=request, draft_id=draft_id)
        else:
            run_id = service_caller.submit_pipeline_run(request)

        print('Submitted PipelineRun', run_id)
        experiment = Experiment(submit_workspace, request.experiment_name)
        run = Run(experiment, run_id=run_id)
        print('Link to Azure Machine Learning Portal:', run.get_portal_url())
        return run

    def _anonymous_create(self, workspace=None, default_datastore=None):
        """
        Create as anonymous pipeline component.

        :param workspace: the register workspace when workspace independent component exists.
        :param default_datastore: The default datastore.
        :return the component dto of registered pipeline component
        :rtype ComponentDto
        """
        return self._create(anonymous_creation=True, workspace=workspace, default_datastore=default_datastore)

    @wrap_azureml_exception_with_identifier(key="Pipeline")
    def _create(self, *, anonymous_creation: bool = False, version: str = None, set_as_default_version: bool = None,
                skip_validation=False, workspace=None, default_datastore=None):
        """
        Create as pipeline component.

        :param anonymous_creation: if the pipeline is created anonymously
        :param version: the version to be registered
        :param set_as_default_version: bool flag indicate set or not set `version` as default version
        :param tags: string list to be set as tags
        :param workspace: the register workspace when workspace independent component exists.
        :return the component dto of registered pipeline component
        :param default_datastore: The default datastore.
        :type default_datastore: str
        :rtype ComponentDto
        """
        self._ensure_registered_in_workspace(workspace or self.workspace)
        # Validation
        if not skip_validation:
            self._validate_on_create(raise_error=True)

        graph_entity_builder = self._get_graph_builder(enable_subpipeline_registration=True,
                                                       workspace=workspace,
                                                       default_datastore=default_datastore)
        graph, module_node_run_settings = \
            graph_entity_builder.build_graph_entity(for_registration=True,
                                                    enable_subpipeline_registration=True,
                                                    anonymous_creation=anonymous_creation,
                                                    default_datastore=default_datastore)

        return self._register_pipeline_component(
            graph=graph, module_node_run_settings=module_node_run_settings, anonymous_creation=anonymous_creation,
            version=version, set_as_default_version=set_as_default_version, workspace=workspace)

    def _register_pipeline_component(self, graph: GraphDraftEntity,
                                     module_node_run_settings,
                                     anonymous_creation: bool = True,
                                     version: str = None,
                                     set_as_default_version: bool = None,
                                     workspace=None):
        if anonymous_creation is True:
            # use ModuleScope.anonymous mark anonymous creation
            scope = ModuleScope.ANONYMOUS
            # check if pipeline name is valid component name, normalize the name if it is not valid
            pipeline_component_name = self._name if is_valid_component_name(self._name) else \
                _sanitize_python_variable_name(self._name[0:COMPONENT_NAME_MAX_LEN])
        else:
            # use ModuleScope.workspace mark explicit creation
            scope = ModuleScope.WORKSPACE
            pipeline_component_name = self._name

        def _get_is_deterministic_for_registration():
            is_deterministic = self._definition.is_deterministic
            if is_deterministic:
                # Check the field on nodes
                incompatible_nodes = [node.name for node in self.nodes if node._definition.is_deterministic is False]
                if incompatible_nodes:
                    _get_logger().warning(
                        f"Nodes {incompatible_nodes} have 'is_deterministic=False' which is incompatible "
                        f"with 'is_deterministic=True' on pipeline component {self.name!r}.")
            return is_deterministic

        body = GeneratePipelineComponentRequest(
            name=pipeline_component_name,
            display_name=self._definition.display_name or self._name,
            description=self._description,
            module_scope=scope,
            is_deterministic=_get_is_deterministic_for_registration(),
            version=version,
            set_as_default_version=set_as_default_version,
            graph=graph,
            module_node_run_settings=module_node_run_settings,
            tags=self._definition._tags)
        register_workspace = self.workspace or workspace
        service_caller = _DesignerServiceCallerFactory.get_instance(register_workspace)
        registered = service_caller.register_pipeline_component(body=body)
        dct = _DefinitionInterface.construct_component_definition_basic_info_dict_by_dto(registered)
        self._definition.creation_context = dct.get('creation_context', None)
        self._definition.registration_context = dct.get('registration_context', None)
        if self._definition._workspace_independent and self._definition.registration_context:
            # If workspace independent component exists in pipeline, update the dict of workspace id and identifier.
            self._definition._workspace_identifier_dict[register_workspace._workspace_id] = \
                self._definition.registration_context.id

        if anonymous_creation is True:
            repr_dict = {
                "name": registered.module_name,
                "type": "PipelineComponent",
                "workspace": register_workspace.name,
                "subscriptionId": register_workspace.subscription_id,
                "resourceGroup": register_workspace.resource_group,
            }
            _get_logger().info("Created Anonymous Component: %s" % repr_dict)
        return registered

    @track(activity_type=_PUBLIC_API, activity_name="PipelineComponent_save")
    def _save(self, experiment_name=None, id=None, default_compute_target=None,
              pipeline_parameters=None, tags=None, properties=None, workspace=None):
        """
        Save pipeline as PipelineDraft.

        :param experiment_name: The experiment name for the PipelineDraft,
            if experiment_name is None will default to pipeline name
        :type experiment_name: str
        :param id: Existing pipeline draft id. If specified, pipeline will be save to that pipeline draft.
        :type id: str
        :param default_compute_target: the default compute target used to run pipeline
        :type default_compute_target: str
        :param pipeline_parameters: An optional dictionary of pipeline parameter assignments for the PipelineDraft.
        :type pipeline_parameters: dict({str:str})
        :param tags: Tags to be added to the submitted run, {"tag": "value"}
        :type tags: dict
        :param properties: Optional properties dictionary for the PipelineDraft,
            only needed when saving as a new PipelineDraft
        :type properties: dict({str:str})
        :param workspace: The specified workspace.
        :type workspace: azure.ml.core.Workspace

        :return: The created PipelineDraft.
        :rtype: azureml.pipeline.core.PipelineDraft
        """
        self._ensure_registered_in_workspace(workspace or self.workspace)
        default_compute_target = self._get_default_compute_target(default_compute_target, workspace=workspace)
        pipeline_parameters = self._expand_default_pipeline_parameters(pipeline_parameters)
        graph_entity_builder = self._get_graph_builder(pipeline_parameters=pipeline_parameters,
                                                       compute_target=default_compute_target,
                                                       workspace=workspace)
        experiment_name = ensure_valid_experiment_name(experiment_name, self.name)

        module_nodes = self._expand_pipeline_nodes()
        enable_subpipeline_registration = enabled_subpipeline_registration()
        graph, module_node_run_settings = \
            graph_entity_builder.build_graph_entity(enable_subpipeline_registration=enable_subpipeline_registration)

        input_to_data_info_dict = self._build_input_to_data_info_dict(module_nodes, pipeline_parameters)
        sub_pipelines_info = None if enable_subpipeline_registration else \
            self._build_sub_pipeline_info(graph.module_node_to_graph_node_mapping, pipeline_parameters)

        compute_target, _ = default_compute_target
        request = SubmitPipelineRunRequest(
            experiment_name=experiment_name,
            graph=graph,
            sub_pipelines_info=sub_pipelines_info,
            module_node_run_settings=module_node_run_settings,
            compute_target=compute_target,
            pipeline_parameters=pipeline_parameters,
            tags=tags,
            properties=properties
        )

        telemetry_value = self._get_telemetry_values(
            pipeline_parameters=pipeline_parameters,
            compute_target=default_compute_target,
            data_sources=input_to_data_info_dict.values(),
            sub_pipelines_info=sub_pipelines_info,
            additional_value={
                'draft_id': id if id is not None else ''
            })

        _LoggerFactory.add_track_dimensions(_get_logger(), telemetry_value)

        return self._save_pipeline_as_draft(_id=id, request=request, workspace=workspace)

    def _save_pipeline_as_draft(self, _id, request: SubmitPipelineRunRequest, workspace=None) -> PipelineDraft:
        save_workspace = self.workspace or workspace
        service_caller = _DesignerServiceCallerFactory.get_instance(save_workspace)
        if _id is None:
            pipeline_draft_id = service_caller.create_pipeline_draft(
                draft_name=self.name,
                draft_description=self.description,
                graph=request.graph,
                module_node_run_settings=request.module_node_run_settings,
                tags=request.tags,
                properties=request.properties,
                sub_pipelines_info=request.sub_pipelines_info)
            pipeline_draft = service_caller.get_pipeline_draft(pipeline_draft_id, include_run_setting_params=False)
        else:
            service_caller.save_pipeline_draft(
                draft_id=_id,
                draft_name=self.name,
                draft_description=self.description,
                graph=request.graph,
                sub_pipelines_info=request.sub_pipelines_info,
                module_node_run_settings=request.module_node_run_settings,
                tags=request.tags)
            pipeline_draft = service_caller.get_pipeline_draft(_id, include_run_setting_params=False)
        return pipeline_draft

    @track(activity_type=_PUBLIC_API, activity_name="PipelineComponent_publish")
    def _publish(self, experiment_name: str, name: str, description: str = None,
                 parameters=None, tags=None, workspace=None):
        """
        Publish a pipeline and make it available for rerunning.

        You can get the pipeline rest endpoint from the PublishedPipeline object returned by this function. With the
        rest endpoint, you can invoke the pipeline from external applications using REST calls. For information
        about how to authenticate when calling REST endpoints, see https://aka.ms/pl-restep-auth.

        The original pipeline associated with the pipeline run is used as the base for the published pipeline.

        :param experiment_name: The name of the published pipeline's experiment.
        :type experiment_name: str
        :param name: The name of the published pipeline.
        :type name: str
        :param description: The description of the published pipeline.
        :type description: str
        :param parameters: parameters of published pipeline.
        :type parameters: dict[str, str]
        :param tags: tags of pipeline to publish
        :type tags: dict[str, str]
        :param workspace: Workspace of published pipeline.
        :type workspace: azureml.core.Workspace

        :return: Created published pipeline.
        :rtype: azure.ml.component._published_pipeline.PublishedPipeline
        """
        workspace = workspace or self.workspace
        self._ensure_registered_in_workspace(workspace)
        parameters = self._expand_default_pipeline_parameters(parameters)
        experiment_name = ensure_valid_experiment_name(experiment_name, self.name)
        graph_entity_builder = self._get_graph_builder(pipeline_parameters=parameters, workspace=workspace)
        enable_subpipeline_registration = enabled_subpipeline_registration()
        graph, module_node_run_settings = graph_entity_builder.build_graph_entity(
            enable_subpipeline_registration=enable_subpipeline_registration)

        sub_pipelines_info = None if enable_subpipeline_registration else \
            self._build_sub_pipeline_info(graph.module_node_to_graph_node_mapping, parameters)

        request = CreatePublishedPipelineRequest(
            pipeline_name=name,
            experiment_name=experiment_name,
            pipeline_description=description,
            pipeline_endpoint_name=None,
            pipeline_endpoint_description=None,
            # Different from submit(), parameters is needed here
            # Or else SMT can't resolve graph and return 400.
            pipeline_parameters=parameters,
            tags=tags,
            graph=graph,
            sub_pipelines_info=sub_pipelines_info,
            module_node_run_settings=module_node_run_settings,
            data_path_assignments=graph_entity_builder.data_path_assignments,
            set_as_default_pipeline_for_endpoint=True,
            use_existing_pipeline_endpoint=False,
            use_pipeline_endpoint=False,
            properties=None
        )
        result = PublishedPipeline.create(workspace=workspace, request=request, pipeline=self)
        published_pipeline = PublishedPipeline._from_service_caller_model(workspace, result)

        telemetry_values = self._get_telemetry_values(pipeline_parameters=parameters)
        telemetry_values.update({
            'pipeline_id': result.id,
            'use_pipeline_endpoint': False,
        })
        _LoggerFactory.add_track_dimensions(_get_logger(), telemetry_values)
        return published_pipeline

    def _publish_to_endpoint(self, experiment_name, name: str, pipeline_endpoint_name: str,
                             description: str = None, pipeline_endpoint_description: str = None,
                             set_as_default: bool = True, use_existing_pipeline_endpoint: bool = True,
                             tags: dict = None, parameters=None, workspace=None):
        """
        Publish a pipeline to pipeline_endpoint.

        A pipeline enpoint is a :class:`azure.ml.component.Pipeline` workflow
         that can be triggered from a unique endpoint URL.

        :param experiment_name: The name of the published pipeline's experiment.
        :type experiment_name: str
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
        :param parameters: parameters of published pipeline.
        :type parameters: dict[str, str]
        :param workspace: Workspace of published pipeline.
        :type workspace: azureml.core.Workspace

        :return: Created published pipeline inside pipeline endpoint.
        :rtype: azure.ml.component._published_pipeline.PublishedPipeline
        """
        workspace = workspace or self.workspace
        self._ensure_registered_in_workspace(workspace)
        parameters = self._expand_default_pipeline_parameters(parameters)
        experiment_name = ensure_valid_experiment_name(experiment_name, self.name)
        graph_entity_builder = self._get_graph_builder(pipeline_parameters=parameters, workspace=workspace)
        enable_subpipeline_registration = enabled_subpipeline_registration()
        graph, module_node_run_settings = \
            graph_entity_builder.build_graph_entity(enable_subpipeline_registration=enable_subpipeline_registration)

        sub_pipelines_info = None if enable_subpipeline_registration else \
            self._build_sub_pipeline_info(graph.module_node_to_graph_node_mapping, parameters)

        request = CreatePublishedPipelineRequest(
            pipeline_name=name,
            experiment_name=experiment_name,
            pipeline_description=description,
            pipeline_endpoint_name=pipeline_endpoint_name,
            pipeline_endpoint_description=pipeline_endpoint_description,
            # Different from submit(), parameters is needed here
            # Or else SMT can't resolve graph and return 400.
            pipeline_parameters=parameters,
            tags=tags,
            graph=graph,
            sub_pipelines_info=sub_pipelines_info,
            data_path_assignments=graph_entity_builder.data_path_assignments,
            module_node_run_settings=module_node_run_settings,
            set_as_default_pipeline_for_endpoint=set_as_default,
            use_existing_pipeline_endpoint=use_existing_pipeline_endpoint,
            use_pipeline_endpoint=True,
            properties=None
        )
        result = PublishedPipeline.create(workspace=workspace, request=request, pipeline=self)
        published_pipeline = PublishedPipeline._from_service_caller_model(workspace, result)

        telemetry_values = self._get_telemetry_values(pipeline_parameters=parameters)
        telemetry_values.update({
            'pipeline_id': result.id,
            'use_pipeline_endpoint': True,
            'set_as_default': set_as_default,
            'use_existing_pipeline_endpoint': use_existing_pipeline_endpoint,
        })
        _LoggerFactory.add_track_dimensions(_get_logger(), telemetry_values)
        return published_pipeline

    def _validate_visualize_scenario(self):
        nodes = self._expand_pipeline_nodes()
        # Feature 1704211: [UX] Support output link as parameter in notebook visualize
        # https://msdata.visualstudio.com/Vienna/_workitems/edit/1704211
        if any(isinstance(param, Output) for node in nodes
               for param in node._parameter_params.values()):
            return True
        # Feature 1704212: [UX] Support condition If-Else in notebook visualize
        # https://msdata.visualstudio.com/Vienna/_workitems/edit/1704212
        if any(node.type == ComponentType.ControlComponent.value for node in nodes):
            return True
        # Bug 1681005: Notebook graph shows validation error while there is no error on pipeline
        # https://msdata.visualstudio.com/Vienna/_workitems/edit/1681005
        # Built-in modules have no 'sweep' section
        if any((node.type == ComponentType.CommandComponent.value and
                'sweep' in node.runsettings._sections_mapping and
                node.runsettings.sweep.enabled is True)
               for node in nodes):
            return True
        return False

    @track(activity_type=_PUBLIC_API, flush=True)
    def validate(self, raise_error=False, is_local=False, *, workspace=None, default_compute_target=None,
                 default_datastore=None):
        """
        Graph/component validation and visualization.

        .. remarks::

            Note that after execution of this method, it will print pipeline validation result in terminal and
            return validation result list which contains the error message and the location in pipelne.

            .. code-block:: python

                validate_result = pipeline.validate()
                print(result)
                # Check validation result
                if len(result) != 0:
                    print('pipeline validate failed')

        :param raise_error: Whether directly raises the error or just shows the error list.
        :type raise_error: bool
        :param is_local: Whether the validation is for local run in the host, false if it is for remote run in AzureML.
                         If is_local=True, TabularDataset not support and local path is supported as input.
        :type is_local: bool
        :param workspace: When workspace independent components exist in pipeline, workspace need to be specified.
                          It will use the workspace to register the workspace independent components.
        :type workspace: azureml.core.Workspace
        :param default_compute_target: The default compute target used to run pipeline
        :type default_compute_target: str
        :param default_datastore: The default datastore.
        :type default_datastore: str

        :return: List of validation error, contains error message and location in pipeline.
        :rtype: builtin.list
        """
        workspace = workspace or self.workspace
        self._ensure_registered_in_workspace(workspace)
        visualization_context = self._get_visualization_context(is_local=is_local, workspace=workspace)

        can_visualize = self._can_visualize()
        # Skip visualize for some scenario
        skip_visualize = self._validate_visualize_scenario()
        if skip_visualize:
            _get_logger().info(f'Visualize is not supported for pipeline {self.name!r}.')
        elif can_visualize:
            from ._widgets._visualize import _visualize
            is_prod = _is_prod_workspace(workspace or self.workspace)
            envinfo = WorkspaceTelemetryMixin._get_telemetry_value_from_workspace(workspace)

            graphyaml = self._build_visualization_dict(visualization_context)
            try:
                _visualize(graphyaml, envinfo=envinfo, is_prod=is_prod, ignore_fallback=True, show_validate=True)
            except Exception as e:
                _get_logger().warning(f'Pipeline {self.name!r} graph visualize failed with exception {e!r}.')
        else:
            self._visualize_not_support_warning()

        # validate internal component interface
        default_compute_target = self._get_default_compute_target(default_compute_target, workspace=workspace)
        validate_result = self._validate(pipeline_steps=visualization_context.step_nodes,
                                         raise_error=raise_error, is_local=is_local, workspace=workspace,
                                         default_compute=default_compute_target,
                                         default_datastore=default_datastore)

        self._add_visualize_telemetry_value(can_visualize)
        return validate_result

    @timer()
    def _get_validate_visualize_graph(self, is_local=False, workspace=None):
        """
        Get validate visualize graph dict for external dependency.

        :param is_local: Whether the validation is for local run in the host.
        :type is_local: bool
        :param workspace: Workspace when pipeline is workspace independent.
        :type workspace: azureml.core.Workspace
        :return: validate graph dict
        :rtype: dict
        """
        if workspace:
            self._ensure_registered_in_workspace(workspace)
        visualization_context = self._get_visualization_context(is_local=is_local, workspace=workspace)
        graphyaml = self._build_visualization_dict(visualization_context)
        return graphyaml

    @timer()
    def _validate(self, pipeline_steps,
                  raise_error=False, is_local=False, pipeline_parameters=None, default_compute=None,
                  default_datastore=None, workspace=None):
        errors = []

        def process_error(error):
            diagnostic = Diagnostic.create_diagnostic_by_component(self, error.message, error.error_type)
            errors.append(diagnostic)

        if enabled_subpipeline_registration():
            # validate pipeline components
            errors += self._validate_pipeline_component(
                is_local=is_local, pipeline_parameters=pipeline_parameters, default_compute=default_compute,
                workspace=workspace)
        else:
            # validate pipeline steps
            PipelineValidator.validate_empty_pipeline(pipeline_steps, process_error)
            PipelineValidator.validate_pipeline_steps(pipeline_steps, lambda e: errors.extend(e))
            PipelineValidator.validate_module_cycle(pipeline_steps, process_error)

        if len(errors) > 0:
            if raise_error:
                raise PipelineValidationError(
                    'Validation failed! Errors: {}'.format([str(error) for error in errors]),
                    error_type=PipelineValidationError.AGGREGATED,
                )

        self._trace_error_message(errors)

        return errors

    def _validate_pipeline_component(self, is_local, pipeline_parameters=None, default_compute=None, workspace=None):
        """Validate interface of pipeline components.

        :param is_local: Whether the validation is for local run in the host.
        :return List of errors.
        """
        from azure.ml.component._util._exceptions import ComponentValidationError

        if pipeline_parameters is None:
            pipeline_parameters = {}
        default_compute = self._get_default_compute_target(default_compute, workspace=workspace)[0]
        errors = []

        def validate_pipeline_component_local(pipeline, errors):
            """Update the input type and component type validation of local run."""
            def process_error(e: Exception, error_type, variable_name, variable_type,
                              component=None, graph_node=None):
                """Generate diagnostic for errors occourd in pipeline or pipeline component."""
                validation_error = ComponentValidationError(str(e), e, error_type)
                diagnostic = Diagnostic.create_diagnostic_by_component_definition(
                    definition=pipeline._definition, error_msg=validation_error.message, component=component,
                    error_var_name=variable_name, error_var_type=variable_type,
                    error_type=validation_error.error_type)
                if graph_node:
                    # When error occurs in pipeline component, getting component info from pipeline graph.
                    diagnostic.id += ".{}".format(graph_node.name)
                    diagnostic.location.component_name = graph_node.name
                    diagnostic.location.component_id = graph_node.module_id
                errors.append(diagnostic)

            if isinstance(pipeline, Pipeline):
                pipeline_nodes = pipeline._definition.components.values()
            elif pipeline._definition.type == ComponentType.PipelineComponent:
                pipeline._definition.generate_register_pipeline()
                pipeline_nodes = pipeline._definition._register_nodes.values()

            # Validate input dataset in pipeline
            for node in pipeline_nodes:
                provided_inputs, pipeline_parameters = {}, {}
                for k, v in node._input_ports.items():
                    provided_inputs[k] = v._get_internal_data_source()
                    if isinstance(provided_inputs[k], PipelineParameter):
                        pipeline_parameters[k] = provided_inputs[k]

                provided_inputs = {k: v._get_internal_data_source() for k, v in node._input_ports.items()}
                ComponentValidator.validate_component_inputs(workspace=pipeline._definition._workspace,
                                                             provided_inputs=provided_inputs,
                                                             interface_inputs=node._interface_inputs,
                                                             for_definition_validate=True,
                                                             pipeline_parameters=pipeline_parameters,
                                                             param_python_name_dict=self._module_dto.
                                                             module_python_interface.inputs_name_mapping,
                                                             process_error=functools.partial(process_error,
                                                                                             component=node),
                                                             is_local=True,
                                                             component_type=self.type)
            # Update component type validation of local run.
            for node in pipeline_nodes:
                ComponentValidator._validate_local_run_component_type(
                    node, functools.partial(process_error, component=node))

        def collect_pipeline_definition_errors(pipeline: Pipeline, is_local: bool):
            from azure.ml.component._component_validator import VariableType

            # Add validation info of pipeline to errors.
            if isinstance(pipeline, Pipeline):
                if is_local:
                    # Remove the error message about the input and re-validate the inputs.
                    errors.extend([error for error in pipeline._definition.validation_info
                                   if error.location.variable_type != VariableType.Input])
                else:
                    errors.extend(pipeline._definition.validation_info)
            if is_local:
                # Validate component type and input dataset type for local run.
                validate_pipeline_component_local(pipeline, errors)

            pipeline_nodes = pipeline.nodes if isinstance(pipeline, Pipeline) else \
                pipeline._definition._register_nodes.values()
            for node in pipeline_nodes:
                if node._definition.type == ComponentType.PipelineComponent:
                    if isinstance(node, Pipeline) and node._definition._id not in visited_definitions.keys():
                        collect_pipeline_definition_errors(node, is_local)
                        visited_definitions[node._definition._id] = node._definition
                    elif not isinstance(node, Pipeline):
                        collect_pipeline_definition_errors(node, is_local)

        def validate_datastore_compute(pipeline: Pipeline, default_datastore, default_compute, workspace):
            # Both datastore and compute can be overwrite after pipeline component's definition, so we validate
            # it after definition.
            for node in pipeline.nodes:
                if isinstance(node, Pipeline):
                    default_datastore = node._resolve_default_datastore() or default_datastore
                    default_compute = node.default_compute_target or default_compute

                    validate_datastore_compute(node, default_datastore, default_compute, workspace)
                else:
                    ComponentValidator._validate_compute_on_component(
                        component=node,
                        default_compute=default_compute,
                        workspace=workspace or self.workspace,
                        process_error=functools.partial(node._process_error, raise_error=False, errors=errors),
                        pipeline_parameters=pipeline_parameters
                    )
                ComponentValidator._validate_datastore(
                    component_type=node.type,
                    output_interfaces=node._module_dto.module_entity.structured_interface.outputs,
                    output_ports=node.outputs,
                    process_error=functools.partial(node._process_error, raise_error=False, errors=errors),
                    default_datastore=default_datastore,
                    param_python_name_dict=node._module_dto.module_python_interface.name_mapping,
                    workspace=workspace or self.workspace
                )

        # 1. collect pipeline definition meta errors
        visited_definitions = {}
        collect_pipeline_definition_errors(self, is_local)
        # 2. validate value assignment on current pipeline
        # update pipeline inputs & parameters here because they are not wrapped as pipeline parameters
        inputs = {**self._input_ports}
        parameters = {**self._parameter_params}
        for k, v in pipeline_parameters.items():
            if k in inputs.keys():
                inputs[k] = v
            elif k in parameters.keys():
                parameters[k] = v
        validation_info = self._validate_component(
            raise_error=False,
            is_local=is_local,
            default_compute=default_compute,
            inputs=inputs,
            parameters=parameters,
            skip_datastore_compute_validation=True,
            workspace=workspace
        )
        # 3. validate datastore & compute
        if not is_local:
            # skip datastore & compute validation as component validate did
            validate_datastore_compute(self, self._resolve_default_datastore(), default_compute, workspace)
        errors.extend(validation_info)
        return errors

    def _validate_on_create(self, raise_error=False):
        """Validate pipeline component on current layer, as creation is recursively, so validation is recursively."""
        errors = []
        errors.extend(self._definition.validation_info)
        if len(errors) > 0:
            if raise_error:
                raise PipelineValidationError(
                    'Validation failed! Errors: {}'.format([str(error) for error in errors]),
                    error_type=PipelineValidationError.AGGREGATED,
                )

        self._trace_error_message(errors)

        return errors

    def _trace_error_message(self, errors):
        telemetry_value = self._get_telemetry_values(additional_value={
            'validation_passed': len(errors) == 0
        })

        _LoggerFactory.add_track_dimensions(_get_logger(), telemetry_value)

        if len(errors) > 0:
            for error in errors:
                # Log pipeline level error
                if error.descriptor.type in \
                        [PipelineValidationError.EMPTY_PIPELINE, PipelineValidationError.MODULE_CYCLE]:
                    telemetry_value = self._get_telemetry_values()
                    telemetry_value.update({
                        'error_message': error.descriptor.message,
                        'error_type': error.descriptor.type
                    })
                    _LoggerFactory.trace(_get_logger(), "Pipeline_validate_error", telemetry_value,
                                         adhere_custom_dimensions=False)
                else:
                    # Log module level error
                    component_info = {
                        'component_id': error.location.component_id,
                        'component_version': error.location.component_version,
                        'error_message': error.descriptor.message,
                        'error_type': error.descriptor.type
                    }
                    telemetry_value = self._get_telemetry_values()
                    telemetry_value.update(component_info)
                    _LoggerFactory.trace(_get_logger(), "Pipeline_module_validate_error", telemetry_value,
                                         adhere_custom_dimensions=False)

    @track(activity_type=_PUBLIC_API, activity_name="PipelineComponent_export_yaml")
    def _export_yaml(self, directory=None):
        """
        Export pipeline to yaml files.

        This is an experimental function, will be changed anytime.

        :param directory: The target directory path. Default current working directory
            path will be used if not provided.
        :type directory: str
        :return: The directory path
        :rtype: str
        """
        from ._pipeline_export_provider import PipelineExportProvider

        if directory is None:
            directory = os.getcwd()
        if not os.path.exists(directory):
            raise UserErrorException('Target directory not exists, path {}'.format(directory))
        elif not os.path.isdir(directory):
            raise UserErrorException('Expected a directory path , got {}'.format(directory))

        module_nodes = self._expand_pipeline_nodes()
        pipelines = self._expand_pipeline_to_pipelines()
        input_to_data_info_dict = self._build_input_to_data_info_dict(
            module_nodes)

        return PipelineExportProvider(
            self, pipelines, module_nodes, input_to_data_info_dict.values(), directory).export_pipeline_entity()

    @track(activity_type=_PUBLIC_API, activity_name="PipelineComponent_get_graph_json")
    def _get_graph_json(self, pipeline_parameters=None, workspace=None):
        """
        Get pipeline graph json.

        Note that `default_compute` and `default_datastore` is different from the real graph,
        because some settings inside them can not be serialized to dictionary.

        :param pipeline_parameters: An optional dictionary of pipeline parameter assignments for the Pipeline
        :type pipeline_parameters: dict({str:str})
        :param workspace: Workspace when workspace independent component exists.
        :type workspace: azureml.core.Workspace
        :return: The graph json.
        :rtype: str
        """
        self._ensure_registered_in_workspace(workspace)
        parameters = self._expand_default_pipeline_parameters(pipeline_parameters)
        graph_entity_builder = self._get_graph_builder(pipeline_parameters=parameters, workspace=workspace)
        return graph_entity_builder.build_graph_json()

    def _get_telemetry_values(self, pipeline_parameters=None, compute_target=None, data_sources=None,
                              sub_pipelines_info=None, on_create=False, additional_value=None, workspace=None):
        """
        Get telemetry value out of a pipeline.

        The telemetry values include the following entries:

        * pipeline_id: A uuid generated for each pipeline created.
        * defined_by: The way the pipeline is created, using @dsl.pipeline or raw code.
        * node_count: The total count of all module nodes.
        * pipeline_parameters_count: The total count of all pipeline parameters.
        * data_pipeline_parameters_count: The total count of all pipeline parameters that are dataset.
        * literal_pipeline_parameters_count: The total count of all pipeline parameters that are literal values.
        * input_count: The total count of data sources.
        * compute_count: The total count of distinct computes.
        * compute_type_count: The total count of distinct compute types.
        * top_level_node_count: The total count of top level nodes & pipelines.
        * subpipeline_count: The total count of sub pipelines.

        :param pipeline_parameters: The pipeline parameters.
        :param compute_target: The compute target.
        :param data_sources: Data sources of the pipeline.
        :param sub_pipelines_info: Sub pipeline infos of the pipeline.
        :param on_create: Whether the pipeline was just created, which means compute target, pipeline parameters, etc
                       are not available.
        :param workspace: The specified workspace.
        :return: telemetry values.
        :rtype: dict
        """
        workspace = workspace or self.workspace
        telemetry_values = WorkspaceTelemetryMixin._get_telemetry_value_from_workspace(workspace)
        all_nodes = self._expand_pipeline_nodes()
        telemetry_values['pipeline_id'] = self._id
        telemetry_values['defined_by'] = "dsl" if self._use_dsl else "raw"
        telemetry_values['node_count'] = len(all_nodes)
        telemetry_values['top_level_node_count'] = len(self.nodes)
        telemetry_values['specify_comment'] = self._comment is not None
        if on_create:
            # We do not have enough information to populate all telemetry values.
            if additional_value is not None:
                telemetry_values.update(additional_value)
            return telemetry_values

        telemetry_values.update(
            _get_telemetry_value_from_pipeline_parameter(pipeline_parameters))

        if compute_target is not None:
            compute_tuples = [node._resolve_compute_for_telemetry(compute_target, workspace)[0] for node in all_nodes]
            # Filter and ignore (None, AmlCompute)
            compute_set = set(compute[0] for compute in compute_tuples if compute[0])
            # Filter and ignore (None, Amlcompute)
            compute_type_set = set(compute[1] for compute in compute_tuples if compute[0])
            telemetry_values['compute_count'] = len(compute_set)
            telemetry_values['compute_type_count'] = len(compute_type_set)

        if data_sources is not None:
            telemetry_values['input_count'] = len(data_sources)
        if sub_pipelines_info is not None:
            telemetry_values['subpipeline_count'] = len(
                sub_pipelines_info.sub_graph_info) - 1

        # TODO: Review interface parameter, find a more general way to record additional values.
        if additional_value is not None:
            telemetry_values.update(additional_value)

        return telemetry_values

    def _add_visualize_telemetry_value(self, can_visualize: bool):
        telemetry_value = self._get_telemetry_values(additional_value={
            'visualize': can_visualize
        })

        # We need to distinguish whether a call to validate will visualize ux or not.
        _LoggerFactory.add_track_dimensions(_get_logger(), telemetry_value)

    def _replace_module(self, old_module: Component, new_module: Component,
                        recursive: bool):
        if recursive:
            nodes = self._expand_pipeline_nodes()
        else:
            nodes = self.nodes
        for node in nodes:
            if isinstance(node, Component) and \
                    not isinstance(node, Pipeline) and \
                    node._is_replace_target(old_module):
                # replace target node's module_version
                node._replace(new_module)

    @track(activity_type=_PUBLIC_API, activity_name="PipelineComponent_replace_component_func")
    def _replace_component_func(self, old_component_func: Callable, new_component_func: Callable,
                                recursive=False, force=False):
        """
        Replace modules by module_function.

        :param old_component_func: A component function which can generate the old module you want to replace
        :type old_component_func: function
        :param new_component_func: A component function which can generate the new module to replace the old one
        :type new_component_func: function
        :param recursive: Indicates this function will replace the modules
                        in the specified pipeline and in all sub pipelines
        :type recursive: bool
        :param force: Whether to force replace, skip validation check
        :type force: bool

        :return: The pipeline itself
        :rtype: azure.ml.component.pipeline.Pipeline
        """
        old_module = old_component_func()
        new_module = new_component_func()
        if not force:
            errors = ComponentValidator.validate_compatibility(old_module, new_module)

            if len(errors) > 0:
                raise UserErrorException('Module incompatible! Errors:{0}'.format(errors))
        self._replace_module(old_module, new_module, recursive)
        return self

    def _expand_pipeline_to_pipelines(self):
        pipelines = []
        _expand_pipeline_to_pipelines(self, pipelines)
        return pipelines

    @timer()
    def _expand_pipeline_nodes(self):
        """
        Expand pipeline to node list.

        :return: node list
        :rtype: list
        """
        steps = []
        for node in self.nodes:
            if isinstance(node, Pipeline):
                sub_pipeline_steps = node._expand_pipeline_nodes()
                steps.extend(sub_pipeline_steps)
            elif isinstance(node, Component):
                step = node
                setattr(step, 'module_node', node)
                steps.append(step)
        return steps

    @timer()
    def _expand_default_pipeline_parameters(self, pipeline_parameters):
        """Add pipeline parameter with default value to pipeline_parameters."""
        if pipeline_parameters is None:
            pipeline_parameters = {}
        self._validate_parameters(pipeline_parameters)
        # Extract Enum value, handle group
        pipeline_parameters, _, _ = resolve_pipeline_parameters(pipeline_parameters)
        pipeline_parameters.update({
            _k: _v for _k, _v in self._parameter_params.items() if _k not in pipeline_parameters})
        return pipeline_parameters

    def _get_graph_builder(self, pipeline_parameters=None, compute_target=None, default_datastore=None,
                           regenerate_outputs=None, enable_subpipeline_registration=False, workspace=None):
        """Get the graph builder for current pipeline."""
        default_compute_target = self._get_default_compute_target(compute_target,
                                                                  ignore_runsettings=enable_subpipeline_registration,
                                                                  workspace=workspace)
        # _parameter_params should also added, or else component parameter will be treated as constants.
        pipeline_parameters = self._expand_default_pipeline_parameters(pipeline_parameters)

        module_nodes = self._expand_pipeline_nodes()
        default_datastore = default_datastore or self.default_datastore
        graph_builder_context = _GraphEntityBuilderContext(compute_target=default_compute_target,
                                                           pipeline_parameters=pipeline_parameters,
                                                           pipeline_regenerate_outputs=regenerate_outputs,
                                                           module_nodes=module_nodes,
                                                           workspace=workspace or self.workspace,
                                                           default_datastore=default_datastore,
                                                           outputs=self._outputs_mapping,
                                                           pipeline_nodes=self.nodes,
                                                           pipeline_component_definition=self._definition)

        return _GraphEntityBuilder(graph_builder_context)

    def _get_visualization_context(self, graph=None, pipeline_parameters=None, compute_target=None,
                                   sub_pipelines_info=None, skip_validation=False, is_local=False, workspace=None):
        if graph is None:
            graph_entity_builder = self._get_graph_builder(pipeline_parameters=pipeline_parameters,
                                                           compute_target=compute_target, workspace=workspace)
            graph, _ = graph_entity_builder.build_graph_entity(enable_subpipeline_registration=False)

        if sub_pipelines_info is None:
            sub_pipelines_info = self._build_sub_pipeline_info(graph.module_node_to_graph_node_mapping,
                                                               pipeline_parameters, build_large_pipeline=True,
                                                               workspace=workspace)

        context = VisualizationContext.from_pipeline_component(
            self,
            graph.module_node_to_graph_node_mapping,
            pipeline_parameters,
            sub_pipelines_info,
            compute_target=compute_target,
            skip_validation=skip_validation,
            is_local=is_local,
            workspace=workspace)

        return context

    @timer()
    def _build_visualization_dict(self, visualization_context=None):
        if visualization_context is None:
            visualization_context = self._get_visualization_context()

        from ._widgets._visualization_builder import VisualizationBuilder
        visualization_builder = VisualizationBuilder(step_nodes=visualization_context.step_nodes,
                                                     module_defs=visualization_context.module_defs,
                                                     data_nodes=visualization_context.data_nodes,
                                                     sub_pipelines_info=visualization_context.sub_pipelines_info)

        return visualization_builder.build_visualization_dict()

    @track(activity_type=_PUBLIC_API, record_inner_depth=5, activity_name="PipelineComponent_run")
    def _run(self, experiment_name=None, display_name=None, working_dir=None, mode=RunMode.Docker.value,
             track_run_history=True, show_output=False, show_graph=True, pipeline_parameters=None,
             continue_on_step_failure=None, max_workers=None, skip_validation=False,
             raise_on_error=True, workspace=None):
        """
        Run pipeline in local.

        Currently support basic/mpi/parallel components run in local environment.

        :param experiment_name: The experiment name, if experiment_name is None will default to pipeline name
        :type experiment_name: str
        :param display_name: The experiment name, if display_name is None, will use the pipeline name
        :type display_name: str
        :param working_dir: The path where pipeline run data and snapshot will be stored.
        :type working_dir: str
        :param mode: Currently support three modes to run pipeline.
                     docker: For each component, it will start a component container and execute command in it.
                     conda: For each component, it will build component conda environment and run command in it.
                     host: Directly run components in host environment.
        :type mode: str
        :param track_run_history: If track_run_history=True, will create azureml.Run and upload component output
                                  and log file to portal.
                                  If track_run_history=False, will not create azureml.Run to upload outputs
                                  and log file.
        :type track_run_history: bool
        :param show_output: Indicates whether to show the pipeline run status on sys.stdout.
        :type show_output: bool
        :param show_graph: Indicates whether to show the graph with run status on notebook.
            If not in notebook environment, overwrite this value to False
        :type show_graph: bool
        :param pipeline_parameters: An optional dictionary of pipeline parameter
        :type pipeline_parameters: dict({str:str})
        :param continue_on_step_failure: Indicates whether to continue pipeline execution if a step fails.
            If True, only steps that have no dependency on the output of the failed step will continue execution.
        :type continue_on_step_failure: bool
        :param max_workers:  The maximum number of threads that can be used to execute pipeline steps.
            If max_workers is None, it will decide depends on the number of processors on the machine.
        :type max_workers: int
        :param skip_validation: Set this parameter True to skip pipeline validation triggered before run.
        :type skip_validation: bool
        :param raise_on_error: Indicates whether to raise an error when the Run is in a failed state
        :type raise_on_error: bool
        :param workspace: The workspace is used to register environment when component is workspace independent.
        :type workspace: azureml.core.Workspace

        :return: The run status, such as, Completed and Failed.
        :rtype: RunStatus
        """
        pipeline_workspace = workspace or self.workspace
        # In the scenario that all components are loaded local without workspace, we cannot track run history.
        if track_run_history and pipeline_workspace is None:
            raise UserErrorException("The pipeline without workspace cannot track run history.")

        run_mode = RunMode.get_run_mode_by_str(mode)
        visualizer = None

        graph_entity_builder = self._get_graph_builder(workspace=pipeline_workspace)
        module_nodes = self._expand_pipeline_nodes()
        graph, _ = graph_entity_builder.build_graph_entity(enable_subpipeline_registration=False)

        input_to_data_info_dict = self._build_input_to_data_info_dict(module_nodes, pipeline_parameters)

        visualization_context = self._get_visualization_context(graph=graph,
                                                                pipeline_parameters=pipeline_parameters,
                                                                skip_validation=skip_validation,
                                                                is_local=True)

        if not skip_validation:
            self._validate(visualization_context.step_nodes, raise_error=True,
                           is_local=True, pipeline_parameters=pipeline_parameters)

        if show_graph:
            can_visualize = self._can_visualize()
            # Skip visualize for some scenario
            skip_visualize = self._validate_visualize_scenario()
            if skip_visualize:
                _get_logger().info(f'Visualize is not supported for pipeline {self.name!r}.')
            elif can_visualize:
                # in notebook show pipeline
                from ._widgets._visualize import _visualize
                is_prod = _is_prod_workspace(pipeline_workspace)
                envinfo = WorkspaceTelemetryMixin._get_telemetry_value_from_workspace(pipeline_workspace)
                graphyaml = self._build_visualization_dict(visualization_context)
                try:
                    visualizer = _visualize(graphyaml, envinfo=envinfo, is_prod=is_prod)
                except Exception as e:
                    _get_logger().warning(f'Pipeline {self.name!r} graph visualize failed with exception {e!r}.')
                self._add_visualize_telemetry_value(can_visualize)
            else:
                self._visualize_not_support_warning()

        # create experiment
        experiment_name = ensure_valid_experiment_name(experiment_name, self.name)
        display_name = display_name if display_name else self._definition.display_name

        with RunHistoryTracker.without_definition(pipeline_workspace, experiment_name, display_name,
                                                  track_run_history) as tracker:
            if not working_dir:
                working_dir = os.path.join(
                    tempfile.gettempdir(), trans_to_valid_file_name(experiment_name), tracker.get_run_id() or self._id)
            short_working_dir = _get_short_path_name(working_dir, is_dir=True, create_dir=True)

            print('Working dir:', working_dir)
            tracker.print_run_info()

            pipeline_run = PipelineRunOrchestrator.generate_orchestrator_by_pipeline(
                self, input_to_data_info_dict.keys(), visualization_context, pipeline_parameters, max_workers)
            pipeline_run_success = pipeline_run.start_orchestrate(working_dir=short_working_dir,
                                                                  tracker=tracker,
                                                                  visualizer=visualizer,
                                                                  show_output=show_output,
                                                                  continue_on_step_failure=continue_on_step_failure,
                                                                  mode=run_mode,
                                                                  raise_on_error=raise_on_error,
                                                                  workspace=workspace)
        return pipeline_run_success

    @timer()
    def _build_sub_pipeline_info(self, module_node_to_graph_node_mapping,
                                 pipeline_parameters=None, build_large_pipeline=False, workspace=None):
        """Build sub pipelines info for pipeline.

        For large pipeline which has more than 1000 nodes, return None if build_large_pipeline is False

        :param: module_node_to_graph_node_mapping: module node instance id to graph node id mapping.
        :type: module_node_to_graph_node_mapping: dict[str,str]
        :param: pipeline_parameters: pipeline parameters.
        :type: pipeline_parameters: dict[str, Any]
        :param: build_large_pipeline: whether to build sub pipeline info for large pipeline.
        :type: build_large_pipeline: bool
        :param workspace: Workspace when pipeline is workspace independent.
        :type workspace: azureml.core.Workspace
        """
        if not build_large_pipeline and len(module_node_to_graph_node_mapping) > 1000:
            return None

        from ._sub_pipeline_info_builder import SubPipelinesInfoBuilder
        return SubPipelinesInfoBuilder(self, module_node_to_graph_node_mapping,
                                       pipeline_parameters, workspace).build()

    @timer()
    def _build_input_to_data_info_dict(self, module_nodes, pipeline_parameters=None):
        all_data_inputs = [n._input_ports[input_name]._get_internal_data_source() for n in module_nodes
                           for input_name in n._input_ports if n._input_ports[input_name]._dset is not None]
        inputs = [i for i in all_data_inputs
                  if not isinstance(i, Output)]

        input_to_data_info_dict = {}

        for input in inputs:
            if isinstance(input, PipelineParameter) and isinstance(input.default_value, Output):
                continue
            input_to_data_info_dict[input] = _build_data_info_from_input(input, pipeline_parameters)

        return input_to_data_info_dict

    @timer()
    def _ensure_registered_in_workspace(self, workspace):
        """
        Use the workspace to register workspace independent component in the pipeline.

        1. Validate the workspace used to register workspace independent component.
        2. Get the list of unregister components.
        3. Register the component definition and update runsettings of the components.

        :param workspace: The workspace is used to register unregistered component in the pipeline.
        :type workspace: azureml.core.Workspace
        """
        if not self._workspace and not workspace:
            raise UserErrorException("Workspace independent asset exists in pipeline, please specify 'workspace'.")
        elif self.workspace:
            workspace = workspace or self._workspace
            if self.workspace._workspace_id != workspace._workspace_id:
                raise UserErrorException("Workspace in pipeline nodes, %s, are different from "
                                         "the workspace in parameter, %s." % (self.workspace, workspace))
        if not self._workspace_independent_component_exists:
            return

        # Update pipeline runsettings
        if not self._runsettings._workspace:
            runsettings = RunSettingsDefinition.build_interface_for_pipeline(self, workspace)
            runsettings.configure(**self._runsettings._get_values(ignore_none=True))
            self._runsettings = runsettings

        nodes = self._expand_pipeline_nodes()
        # Get the list of unregistered component definition.
        unregister_component_definition = set(
            [node._definition for node in nodes if node._definition._identifier_in_workspace(workspace) is None
             and not node._definition.registry_name])

        if unregister_component_definition:
            # Register components in the workspace.
            thread_pool = concurrent.futures.ThreadPoolExecutor()
            register_tasks = [
                thread_pool.submit(
                    definition._register_workspace_independent_component,
                    workspace=workspace,
                    package_zip=None,
                    anonymous_registration=True,
                    set_as_default=False,
                    amlignore_file=definition._additional_aml_ignore_file,
                    version=None,
                    registry_name=None)
                for definition in unregister_component_definition]
            concurrent.futures.wait(register_tasks, return_when=concurrent.futures.ALL_COMPLETED)
            exceptions = [task.exception() for task in register_tasks if task.exception()]
            if exceptions:
                raise PipelineValidationError(
                    'Register workspace independent component Failed! '
                    'Errors: {}'.format([str(error) for error in exceptions]),
                    error_type=PipelineValidationError.AGGREGATED,
                )

            # Update pipeline component definition.
            self._definition._update_pipeline_component_definition(workspace)
            # Update pipeline interface after workspace independent component registration.
            self._init_structured_interface()

            # Update runsettings and k8srunsettings of the non updated node by registered definition module dto.
            for node in nodes:
                if node._definition in unregister_component_definition and not node._runsettings._workspace:
                    # Get the node's direct parent pipeline parameter value.
                    # Wrap literal as PipelineParameter to use on component.
                    node_pipeline_parameter = _build_pipeline_parameter(
                        None, node._parent._expand_default_pipeline_parameters({}))
                    node._update_component_params_and_runsettings(
                        workspace, node_pipeline_parameter, pipeline_name=self.name)

                # MT may apply transform to port_name, we need to correct output port name
                outputs = node._module_dto.module_python_interface.outputs
                outputs_arg_name_mapping = {param.argument_name: param.name for param in outputs}
                for output in node.outputs.values():
                    output._port_name = outputs_arg_name_mapping.get(output._port_name, output._port_name)

    def _register_sub_pipelines(self, thread_pool, workspace=None, default_datastore=None):
        """
        Register the sub pipeline.

        :param thread_pool: The thread pool used to execute sub pipeline registration.
        :type thread_pool: concurrent.futures.ThreadPoolExecutor
        :param workspace: The workspace is used to register unregistered component in the pipeline.
        :type workspace: azureml.core.Workspace
        :param default_datastore: The default datastore.
        :type default_datastore: str
        :return: Sub pipeline register task.
        :rtype: concurrent.futures.Future
        """
        workspace = workspace or self.workspace
        if not workspace:
            raise UserErrorException("Workspace independent asset exists in pipeline, please specify 'workspace'.")
        workspace_id = workspace._workspace_id
        if workspace_id not in self._definition._register_task:
            register_task = thread_pool.submit(self._anonymous_create, workspace, default_datastore)
            # Because pipeline componnent with workspace independent component will be registered
            # in diff workspaces, it will use workspace id to identify register tasks.
            self._definition._register_task[workspace_id] = register_task
        return self._definition._register_task[workspace_id]

    @staticmethod
    def _validate_pipeline_tags(tags):
        if not tags:
            return
        error = UserErrorException(exception_message="Tags must in dict[str, str] format.")
        if not isinstance(tags, dict):
            raise error
        for k, v in tags.items():
            if not (isinstance(k, str) and isinstance(v, str)):
                raise error


def _expand_pipeline_to_pipelines(pipeline, pipelines):
    """Expand the pipeline into list."""
    pipelines.append(pipeline)
    for node in pipeline.nodes:
        if isinstance(node, Pipeline):
            _expand_pipeline_to_pipelines(node, pipelines)


def _build_data_info_from_input(input, pipeline_parameters: Dict[str, Any]):
    if isinstance(input, PipelineParameter):
        if input.default_value is not None:
            input = input.default_value
        else:
            # pipeline parameter which has not been assigned in pipeline initialization
            # try to find if the parameter is assigned after initialization
            if pipeline_parameters is not None and input.name in pipeline_parameters.keys():
                input = pipeline_parameters[input.name]
            else:
                return DataInfo(name=input.name, dataset_type='parameter')

    if isinstance(input, DataReference) or isinstance(input, _GlobalDataset):
        return DataInfo(aml_data_store_name=input.datastore.name,
                        relative_path=input.path_on_datastore,
                        name=input.data_reference_name)
    elif isinstance(input, _FeedDataset):
        return DataInfo(name=input.name, dataset_type='feed dataset')
    elif isinstance(input, DataPath):
        return DataInfo(aml_data_store_name=input.datastore_name,
                        relative_path=input.path_on_datastore,
                        name=input._name)
    elif hasattr(input, '_registration'):  # registered dataset
        # Filter FileDataset/Dataset
        reg = input._registration
        name = reg.name if reg.name is not None else 'saved_dataset_{}'.format(reg.saved_id)
        return DataInfo(id=reg.registered_id, saved_dataset_id=reg.saved_id, name=name)
    elif hasattr(input, 'dataset'):  # saved dataset
        # Filter DatasetConsumptionConfig
        return DataInfo(saved_dataset_id=input.dataset.id, name=input.name)
    elif isinstance(input, str) or isinstance(input, Path):
        # Verify that the input type is supported and the path exists in _component_validator.
        return DataInfo(name=str(input))
    else:
        raise UserErrorException("Invalid input type: {0}".format(type(input)))
