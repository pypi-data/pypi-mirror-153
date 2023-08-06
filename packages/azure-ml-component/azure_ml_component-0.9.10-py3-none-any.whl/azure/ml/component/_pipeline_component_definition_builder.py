# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import os
import sys
import uuid
import inspect
import dataclasses
from collections import OrderedDict
from inspect import Parameter, signature
from datetime import datetime
from bytecode import Label, Instr, Bytecode
from types import MethodType, FunctionType

from azure.ml.component._core._types import _GroupAttrDict, _Param
from azureml.data._dataset import _Dataset
from azureml.data.abstract_datastore import AbstractDatastore
from azureml.data.dataset_consumption_config import DatasetConsumptionConfig
from azureml.data.file_dataset import FileDataset
from azureml.exceptions import UserErrorException

from ._pipeline_expression import PipelineExpression
from ._util._utils import _change_profile

from .component import Component, Output, Input, _AttrDict
from ._core._component_definition import PipelineComponentDefinition
from ._core._types import Input as InputDefinition
from ._dataset import _GlobalDataset, _FeedDataset
from ._pipeline_validator import PipelineValidator
from ._pipeline_parameters import PipelineParameter
from ._parameter_assignment import _ParameterAssignment
from ._util._exceptions import PipelineValidationError
from ._util._loggerfactory import timer_context
from ._util._utils import _obj_in_list


class PipelineComponentDefinitionBuilder:
    def __init__(self, name=None, version=None, display_name=None, description=None, workspace=None,
                 default_compute_target=None, default_datastore=None, tags=None,
                 parameters=None, from_module_name=None, pipeline_function_name=None,
                 parent_definition_id=None, non_pipeline_parameters=None, is_deterministic=None):
        """
        :param name: Definition name.
        :type name: str
        :param version: The version of pipeline component.
        :type version: str
        :param display_name: The display name of pipeline component.
        :type display_name: str
        :param description: Description of definition.
        :type description: str
        :param workspace: workspace of definition.
        :type workspace: Workspace
        :param default_compute_target: The resolved default compute target.
        :type default_compute_target: tuple(str, str)
        :param default_datastore: The default datastore.
        :type default_datastore: str
        :param tags: The tags of pipeline component.
        :type tags: dict[str, str]
        :param parameters: The pipeline parameters of function defined by dsl.pipeline.
        :type parameters: dict
        :param from_module_name: from module name.
        :type from_module_name: str
        :param pipeline_function_name: The pipeline function name.
        :type pipeline_function_name: str
        :param parent_definition_id: The parent definition id.
            Used to recover the definition of pipeline so that we can export graph to code.
            Notice that a sub pipeline has parent_definition_id only when sub pipeline defined inside parent pipeline.
            The sub pipeline which defined outside but created inside parent do not has parent_definition_id.
        :type parent_definition_id: str
        :param non_pipeline_parameters: The non pipeline parameters of function defined by dsl.pipeline.
        :type non_pipeline_parameters: dict
        :param is_deterministic: Specify whether the pipeline component can be reused or not. None value
            will be set as True before register. If False, the pipeline component will never be reused.
        :type is_deterministic: bool
        """
        self.id = str(uuid.uuid4())
        if name is None:
            name = pipeline_function_name
        if name is None:
            now = datetime.now()
            name = 'pipeline_created_on_{}_{}_{}'.format(now.month, now.day, now.year)
        self.name = name
        self.version = version
        self.display_name = display_name
        self.description = description
        # Id to components dict inside pipeline definition.
        self.components = OrderedDict({})
        # The variable names of pipeline's components.
        self.components_variable_names = []
        # A dict of outputs name to OutputDefinition.
        self.outputs = {}
        self.tags = tags
        # Used to update inputs and parameters, re-order the inputs and parameters order.
        # Note: if user specify inputs without annotation, it will be infer as _Param by us and will be updated later.
        # pipeline parameters
        parameters = {} if parameters is None else parameters
        # non pipeline parameters
        self._non_pipeline_parameters = non_pipeline_parameters or {}
        self.original_function_parameters = parameters
        # A dict of inputs name to InputDefinition.
        self.inputs = {}
        self.parameters = {**parameters}
        # A dict of outputs name to OutputBuilder on Component.
        self.outputs_mapping = {}
        self._default_wrapped_build_args = {}
        self.default_compute_target = default_compute_target
        self.default_datastore = default_datastore
        self.workspace = workspace
        # A list of dictionaries used to convert pipeline parameter kwargs to
        # nodes with replaced keys. Dict key is the nodes parameter keys, value is parent pipeline
        # parameter name(direct assign) or _ParameterAssignment(partial assign).
        # e.g.
        # @dsl.pipeline()
        # def parent(str1, str2):
        #   component1(string_param=str1)
        #   component2(str=str2)
        # Then the dict_list on pipeline 'parent' is [{'string_param', 'str1'}, {'str':'str2'}]
        self.components_args_matched_dict_list = []
        self.parent_definition_id = parent_definition_id
        self.from_module_name = from_module_name
        self.pipeline_function_name = pipeline_function_name
        self.is_deterministic = is_deterministic
        self._component_definition = None

    def _update_components_args_matched_dict_list(self):
        # Build default pipeline parameters from original function parameters dict.
        pipeline_parameters = self._get_default_wrapped_pipeline_parameters()
        for component in self.components.values():
            # Resolve parameter assignments again after set_inputs.
            component._update_parameter_assignments_with_pipeline_parameter(pipeline_parameters)
            self.components_args_matched_dict_list.append(_get_component_args_matched_dict(self, component))

    def _update_components_variable_names(self, _locals_data):
        """
        Record component variable names defined by user.

        e.g.
        def pipeline():
            module1 = module_func()
            m2 = module_func()
            no_name = module_func()
            module_func()

        The components_variable_names will be ['module1', 'm2', 'no_name', None]
        Component without name will not in locals data.
        """
        id_name_dict = {}
        name_count_dict = {}
        compname_udfname_dict = {}
        local_names = set()
        # Add user given name from locals data
        for k, v in _locals_data.items():
            if isinstance(v, PipelineExpression):
                v = v._created_component
            if not isinstance(v, Component):
                continue
            if v._id not in self.components:
                continue
            name_original = k if v.node_name is None else v.node_name
            name = name_original.lower()
            if name in local_names:
                raise UserErrorException(
                    f'Duplicate node name found in pipeline: {self.name!r}, '
                    f'node name: {name_original!r}. Duplicate check is case-insensitive.'
                )
            local_names.add(name)
            id_name_dict[v._id] = name
            name_count_dict[name] = 1

        # Find the last user-defined name for a same type of components
        for _id, component in self.components.items():
            if _id in id_name_dict:
                compname_udfname_dict[component.name] = id_name_dict[_id]

        # Refine and fill default name.
        # If component name is same, append '_{count}' suffix.
        for _id, component in self.components.items():
            if _id in id_name_dict:
                continue
            target_name = component.name
            if component.node_name is not None:
                target_name = component.node_name
            elif component.name in compname_udfname_dict:
                target_name = compname_udfname_dict[component.name]
            if target_name not in name_count_dict:
                name_count_dict[target_name] = 0
            name_count_dict[target_name] += 1
            suffix = '' if name_count_dict[target_name] == 1 else '_{}'.format(name_count_dict[target_name] - 1)
            id_name_dict[_id] = '{}{}'.format(target_name, suffix)
        self.components_variable_names = [id_name_dict[_k] for _k in self.components]

    def _update_nodes_runsettings(self):
        """Resolve ParameterAssignment in nodes runsettings."""
        # Use pipeline parameter resolve parameter assignments
        # Build default pipeline parameters from original function parameters dict.
        pipeline_parameters = self._get_default_wrapped_pipeline_parameters()
        for component in self.components.values():
            component._update_parameter_assignments_with_pipeline_parameter(pipeline_parameters)

    def _update_outputs(self, outputs):
        """
        Set method to set pipeline definition outputs.

        It will check if right type of outputs is passed,
            then find the original port definition from it's owner.

        :param outputs: Outputs of component
        :type outputs: Mapping[str, azure.ml.component.component.Output]
        """
        error_msg = "The return type of dsl.pipeline decorated function should be a mapping from dataset name to " \
                    "azure.ml.component.component.Output"
        if dataclasses.is_dataclass(outputs):
            outputs = {field.name: getattr(outputs, field.name) for field in dataclasses.fields(outputs)}
        is_type_valid = isinstance(outputs, dict)
        if not is_type_valid:
            raise UserErrorException(error_msg)
        for key, value in outputs.items():
            is_key_type_value = isinstance(key, str)
            is_value_type_valid = isinstance(value, Output)
            if not is_key_type_value or not is_value_type_valid:
                raise UserErrorException(error_msg)
            owner = value._owner
            if owner is not None and owner._definition is not None:
                self.outputs.update({
                    key: _v._to_dict() for _k, _v in owner._definition.outputs.items() if _k == value._name})
        self.outputs_mapping = outputs if outputs is not None else {}

    def _correct_default_compute_target(self):
        self.default_compute_target = self._get_default_compute_target()

    def _correct_default_data_store(self):
        if isinstance(self.default_datastore, AbstractDatastore):
            self.default_datastore = self.default_datastore.name

    def _get_default_compute_target(self):
        """Try to resolve the default compute target to tuple(compute_name, compute_type)."""
        # Note that if all nodes are workspace independent, return compute_type is None.
        default_compute_target = self.default_compute_target

        if default_compute_target is None:
            return None, "AmlCompute"

        # try to resolve compute target
        if isinstance(default_compute_target, str):
            if self.workspace is None:
                # all nodes are workspace independent component in pipeline
                return default_compute_target, None
            from ._restclients.service_caller_factory import _DesignerServiceCallerFactory
            service_caller = _DesignerServiceCallerFactory.get_instance(self.workspace)
            target = service_caller.get_compute_by_name(default_compute_target)
            if target is None:
                print(default_compute_target + " not found in workspace, assume this is an AmlCompute")
                return default_compute_target, "AmlCompute"
            else:
                return target.name, target.compute_type
        elif isinstance(default_compute_target, tuple):
            if not len(default_compute_target) == 2:
                raise ValueError('Compute target tuple must have 2 elements (compute name, compute type)')
            return default_compute_target
        else:
            raise ValueError('Compute target must be a string')

    def _get_default_wrapped_pipeline_parameters(self):
        return {_k: _wrap_pipeline_parameter(_k, _v._default, _groups=[_k])
                for _k, _v in self.original_function_parameters.items()}

    @classmethod
    def _save_type_annotation(cls, parameter_mapping, annotation_mapping):
        for pipeline_parameter_name, pipeline_parameter in parameter_mapping.items():
            if pipeline_parameter_name not in annotation_mapping:
                continue
            annotation = annotation_mapping[pipeline_parameter_name]
            if isinstance(annotation, InputDefinition):
                pipeline_parameter._user_annotation = annotation.type
            elif isinstance(annotation, _Param) and annotation.DATA_TYPE is not None:
                pipeline_parameter._user_annotation = annotation.TYPE_NAME
            elif isinstance(pipeline_parameter, _GroupAttrDict):
                cls._save_type_annotation(pipeline_parameter, annotation.values)

    def _sort_inputs(self):
        # Sort inputs order as original parameter order.
        self.inputs = {_k: self.inputs[_k] for _k in self.original_function_parameters if _k in self.inputs}
        # Sort parameters order as original parameter order.
        self.parameters = {
            _k: self.parameters[_k] for _k in self.original_function_parameters if _k in self.parameters}

    def add_component(self, component):
        """
        Add a component into pipeline component definition builder.

        :param component: other component
        :type component: Component
        """
        if component._id in self.components.keys():
            raise UserErrorException('Component already exists.')
        if self.workspace is None:
            self.workspace = component._workspace
        elif component._workspace:
            is_same_workspace = \
                self.workspace._workspace_id == component._workspace._workspace_id
            if not is_same_workspace:
                raise UserErrorException(
                    'Not all pipeline nodes are from the same workspace: {}, {}'.format(
                        self.workspace, component
                    ))

        # Use pipeline parameter resolve parameter assignments
        # Build default pipeline parameters from original function parameters dict.
        pipeline_parameters = self._get_default_wrapped_pipeline_parameters()
        component._update_parameter_assignments_with_pipeline_parameter(pipeline_parameters)

        self.components.update({component._id: component})

    def resolve_component_parameter_and_update(self, component):
        # Build default pipeline parameters from original function parameters dict.
        pipeline_parameters = self._get_default_wrapped_pipeline_parameters()
        # Resolve parameter assignments again after set_inputs.
        component._update_parameter_assignments_with_pipeline_parameter(pipeline_parameters)

    def build(self) -> 'PipelineComponentDefinition':
        """
        Build a pipeline component definition using current pipeline definition builder.

        This function will build recursively if there is sub pipeline inside, notice that
            current builder need an attribute named `func` to get the function defined by dsl.pipeline.
        e.g.
        # Now we just create a definition builder but not build.
        @dsl.pipeline
        def sub():
            ...
        @dsl.pipeline
        def parent():
            sub()
        # We build pipeline definition when you want to get a real pipeline instance.
        pipeline = parent()
        #
        """
        if self._component_definition is not None:
            return self._component_definition
        func = self.__getattribute__('func')
        if func is None:
            raise Exception('Pipeline component definition builder call build() without function inside!')
        default_args = {k: v._default for k, v in self.original_function_parameters.items()}
        # Wrap args with PipelineParameter or InputBuilder to record where the parameter came from.
        # args has mapped into kwargs, so it is no use now.
        _kwargs = _build_pipeline_parameter(func, default_args, self._non_pipeline_parameters)
        # assign type annotation to pipeline parameters
        self._save_type_annotation(_kwargs, self.original_function_parameters)
        self._default_wrapped_build_args = _kwargs
        # Join non pipeline parameters
        _all_kwargs = {**_kwargs, ** self._non_pipeline_parameters}
        # We use this stack to store the dsl pipeline definition hierarchy
        _definition_builder_stack.push(self)
        _definition_id_now_build.append(self.id)
        # set default value of _locals_data here in case the func get exceptions
        _locals_data = {}
        try:
            if isinstance(func, FunctionType):
                # Use bytecode injection to add try...finally around code to persistent the locals in the function.
                persistent_func = persistent_locals(func)
                with timer_context(activity_name='user_code_duration'):
                    if inspect.ismethod(func):
                        # When func is the method of class, it will set the object to params.
                        outputs = persistent_func(func.__self__, **_all_kwargs)
                    else:
                        outputs = persistent_func(**_all_kwargs)
                _locals_data = persistent_func._locals
            else:
                # When type of pipeline func is not function type, such as callable class, using sys.setprofile to
                # get the variable name inside pipeline
                disable_profile = os.getenv('DISABLE_SETPROFILE', 'false').lower() == 'true'
                if disable_profile:
                    outputs = func(**_all_kwargs)
                else:
                    outputs, _locals_data = _get_func_outputs(func, [], _all_kwargs)
            self._update_components_variable_names(_locals_data)
        finally:
            # pop current pipeline definition builder out of stack
            _definition_builder_stack.pop()
            _definition_id_now_build.pop()
        if outputs is None:
            outputs = {}
        self._update_nodes_runsettings()
        self._update_outputs(outputs)
        self._update_components_args_matched_dict_list()
        self._sort_inputs()
        self._correct_default_compute_target()
        self._correct_default_data_store()
        # store pipeline parameters to definition for future validation
        definition = self.create_definition(_use_dsl=True)
        self._component_definition = definition

        return definition

    def create_definition(self, _use_dsl=False) -> PipelineComponentDefinition:
        """Create pipeline component definition from pipeline component definition builder fields.

        :param _use_dsl: If this definition is for dsl.pipeline
        """
        return PipelineComponentDefinition(
            id=self.id, name=self.name, version=self.version, display_name=self.display_name,
            components=self.components, components_variable_names=self.components_variable_names,
            workspace=self.workspace, inputs=self.inputs, outputs=self.outputs,
            parameters=self.parameters, tags=self.tags,
            outputs_mapping=self.outputs_mapping, description=self.description,
            components_args_matched_dict_list=self.components_args_matched_dict_list,
            parent_definition_id=self.parent_definition_id, from_module_name=self.from_module_name,
            pipeline_function_name=self.pipeline_function_name, default_compute_target=self.default_compute_target,
            default_datastore=self.default_datastore, pipeline_parameters=self._default_wrapped_build_args,
            non_pipeline_parameters=self._non_pipeline_parameters, is_deterministic=self.is_deterministic
        )

    @staticmethod
    def from_func(
            name, version, display_name, description, default_compute_target,
            default_datastore, tags, func, parent_def_id=None, non_pipeline_parameters: dict = None,
            dynamic_param_name: str = None, dynamic_param_value: dict = None, is_deterministic: bool = None
    ) -> 'PipelineComponentDefinitionBuilder':
        """Create a pipeline component definition builder from a func defined by dsl.pipeline.

        :param name: The name of pipeline.
        :type name: str
        :param version: The version of pipeline.
        :type version: str
        :param display_name: The display name of pipeline.
        :type display_name: str
        :param description: The description of pipeline.
        :type description: str
        :param default_compute_target: The default compute target on pipeline.
        :type default_compute_target: str
        :param default_datastore: The default datastore on pipeline
        :type default_datastore: str
        :param tags: The tags of pipeline.
        :type tags: dict[str, str]
        :param func: The pipeline function defined.
        :type func: Callable
        :param parent_def_id: The parent definition id of current pipeline.
        :type parent_def_id: str
        :param non_pipeline_parameters: The non pipeline parameters dict.
        :type non_pipeline_parameters: dict[str, Any]
        :param dynamic_param_name: The dynamic parameter name, e.g. 'kwargs'.
        :type dynamic_param_name: str
        :param dynamic_param_value: The value of dynamic parameter.
        :type dynamic_param_value: dict[str, Union[str, int, bool, float, None, azureml.core.Dataset]]
        :param is_deterministic: Specify whether the pipeline component can be reused or not. None value
            will be set as True before register. If False, the pipeline component will never be reused.
        :type is_deterministic: bool
        """
        # _get_param_with_standard_annotation will standardize function parameter annotations to dsl.types
        from azure.ml.component._core._types import _get_param_with_standard_annotation
        parameters = _get_param_with_standard_annotation(
            func, is_func=True, non_pipeline_parameter_names=non_pipeline_parameters.keys(),
            dynamic_param_name=dynamic_param_name, dynamic_param_value=dynamic_param_value)

        if hasattr(func, '__name__'):
            function_name = func.__name__
        elif hasattr(func, '__code__'):
            function_name = func.__code__.co_name
        else:
            function_name = type(func).__name__

        PipelineComponentDefinition.detect_output_annotation(function_name, parameters)
        builder = PipelineComponentDefinitionBuilder(
            name=name, version=version, display_name=display_name, description=description,
            parameters=parameters, non_pipeline_parameters=non_pipeline_parameters,
            default_compute_target=default_compute_target, default_datastore=default_datastore, tags=tags,
            from_module_name=func.__module__, pipeline_function_name=function_name,
            parent_definition_id=parent_def_id, is_deterministic=is_deterministic)
        # Use set attr to avoid pass self as func parameter incorrectly.
        builder.__setattr__('func', func)
        return builder

    @staticmethod
    def from_nodes(
            nodes=None, name=None, version=None, display_name=None,
            workspace=None, pipeline_outputs=None, description=None,
            default_compute_target=None, default_datastore=None, tags=None) -> 'PipelineComponentDefinitionBuilder':
        """Create a pipeline component definition builder from several child component nodes."""
        if len(nodes) != len(set(nodes)):
            raise UserErrorException('Could not add duplicate nodes to pipeline.')

        builder = PipelineComponentDefinitionBuilder(
            name=name, version=version, display_name=display_name, description=description, workspace=workspace,
            default_compute_target=default_compute_target, default_datastore=default_datastore, tags=tags)
        all_node_has_definition = True
        for node in nodes:
            builder.add_component(node)
            if node._definition is None:
                all_node_has_definition = False

        inputs_mapping = _resolve_node_inputs(nodes)
        builder.outputs_mapping = pipeline_outputs if pipeline_outputs is not None else {}
        builder.outputs = {}
        builder.inputs = {}
        builder._update_components_variable_names(_locals_data={})
        builder._update_components_args_matched_dict_list()
        if all_node_has_definition:
            builder.outputs = {
                _k: _v._owner._definition.outputs[_v._name]._to_dict()
                for _k, _v in builder.outputs_mapping.items()}
            builder.inputs = {
                _k: _v._owner._definition.inputs[_v._name]._to_dict()
                for _k, _v in inputs_mapping.items()}

        return builder


def get_user_func_tracer(_locals_data, func_code):
    """
    Get a tracer to recognize and trace user pipeline function.

    :param _locals_data: A dict to save locals data.
    :type _locals_data: dict
    :param func_code: An code object to compare if current frame is inside user function.
    :type func_code: code
    """
    def tracer(frame, event, arg):
        # If frame is not user function frame, skip
        if event != 'return' or frame.f_code != func_code:
            return
        # Capture the locals of user's dsl function, added to builder.
        _locals_data.update(frame.f_locals.copy())
    return tracer


def _get_func_outputs(func, args, kwargs):
    _locals_data = {}
    # Set profile to get the variable name inside pipeline given by user.
    with _change_profile(get_user_func_tracer(_locals_data, func.__code__)):
        with timer_context(activity_name='user_code_duration'):
            outputs = func(*args, **kwargs)
    return outputs, _locals_data


_BUILDER_STACK_MAX_DEPTH = 100


class _PipelineComponentDefinitionBuilderStack:
    def __init__(self):
        self.items = []

    def top(self):
        if self.is_empty():
            return None
        return self.items[-1]

    def pop(self):
        if self.is_empty():
            return None
        return self.items.pop()

    def push(self, item):
        error_msg = "_PipelineComponentDefinitionBuilderStack only " \
                    "allows pushing `PipelineComponentDefinition` element"
        assert isinstance(item, PipelineComponentDefinitionBuilder), error_msg

        cycles = PipelineValidator.validate_pipeline_cycle(self)
        if cycles:
            raise PipelineValidationError(
                message="Detected pipeline recursion, pipelines: {}".format(cycles),
                error_type=PipelineValidationError.PIPELINE_RECURSION)
        if self.size() >= _BUILDER_STACK_MAX_DEPTH:
            raise UserErrorException('Depth of pipeline \'{}\' exceeds limit {}'.format(
                self.top().name, _BUILDER_STACK_MAX_DEPTH))

        return self.items.append(item)

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)


_definition_builder_stack = _PipelineComponentDefinitionBuilderStack()
# This collection is used to record the id of definition in building,
#   so that we can get the value of parent definition id.
# Notice that a sub pipeline has parent_definition_id only when sub pipeline defined inside parent pipeline.
#   The sub pipeline which defined outside but created inside parent do not has parent_definition_id.
_definition_id_now_build = []


def _add_component_to_current_definition_builder(component):
    if _definition_builder_stack.size() > 0:
        _builder = _definition_builder_stack.top()
        _builder.add_component(component)


def _try_resolve_assignments_and_update_parameters(component):
    if _definition_builder_stack.size() > 0:
        _builder = _definition_builder_stack.top()
        _builder.resolve_component_parameter_and_update(component)


def _wrap_pipeline_parameter(key, value, _groups=None, create_new=False):
    # Append parameter path in group
    _groups = [*_groups] if _groups else []
    # return value if it's already pipeline parameter
    if isinstance(value, PipelineParameter):
        return value if not create_new else \
            PipelineParameter(key, value.default_value, _auto_wrap_for_build=True, _groups=_groups)
    if isinstance(value, _GroupAttrDict):
        _groups.append(key)
        # Create new if value already pipeline parameter and update groups value,
        # because the parameter name may be changed when pass parameter to sub pipeline.
        return _GroupAttrDict({
            k: _wrap_pipeline_parameter(k, v, _groups=_groups, create_new=True) for k, v in value.items()})
    return PipelineParameter(key, value, _auto_wrap_for_build=True, _groups=_groups)


def _build_pipeline_parameter(func, kwargs, non_pipeline_parameters=None):
    def wrap_arg_value(arg_name, arg):
        if isinstance(arg, PipelineParameter):
            return _wrap_pipeline_parameter(arg_name, arg, create_new=True)
        elif isinstance(arg, _ParameterAssignment):
            # Convert pipeline parameter from outer pipeline to constant
            return _wrap_pipeline_parameter(arg_name, arg.value)
        else:
            return _wrap_pipeline_parameter(arg_name, arg)

    transformed_kwargs = {key: wrap_arg_value(key, value) for key, value in kwargs.items()}

    if func is None:
        return transformed_kwargs

    def all_p(parameters):
        for value in parameters.values():
            yield value

    parameters = all_p(signature(func).parameters)
    # transform default values
    for left_args in parameters:
        if non_pipeline_parameters and left_args.name in non_pipeline_parameters:
            continue
        if left_args.name not in transformed_kwargs.keys() and left_args.default is not Parameter.empty:
            transformed_kwargs[left_args.name] = wrap_arg_value(left_args.name, left_args.default)
    return transformed_kwargs


def _get_component_args_matched_dict(builder, empty_input_component):
    """
    Convert input param name from a pipeline parameter to component param name.

    e.g.
    def pipeline(param):
      pipeline2(param)
    def pipeline2(parameter): xxx
    then input param from args need to converted to parameter: param instead of param: param
    This dict will be used when `_convert_component_kwargs`

    :return: Component matched args.
    :rtype: dict
    """
    _params = {_k: _v._dset for _k, _v in empty_input_component._input_ports.items()}
    _params.update({_k: _v for _k, _v in empty_input_component._parameter_params.items() if _k not in _params.keys()})
    match_dict = {}
    from azure.ml.component._core._types import _GroupAttrDict
    for _k, _v in _params.items():
        if isinstance(_v, Input):
            match_dict[_k] = _v.name
        elif isinstance(_v, (PipelineParameter, dict, list, tuple, _ParameterAssignment, _GroupAttrDict)):
            match_dict[_k] = _v
    return match_dict


def _resolve_node_inputs(nodes):
    """Setter method to set pipeline inputs."""
    all_pipeline_node_outputs = [output for node in nodes for output_name, output in node.outputs.items()]
    # append all nodes, since node with one output could be used as input as well
    all_pipeline_node_outputs.extend([node for node in nodes])
    # append all nodes' outputs, since node's outputs _AttrDict with one output could be used as input as well
    all_pipeline_node_outputs.extend([node.outputs for node in nodes])

    inputs = {}
    for node in nodes:
        for input_name, input in node._input_ports.items():
            if input._dset is None:
                continue
            if not _obj_in_list(input._dset, all_pipeline_node_outputs) and \
                    not isinstance(input._dset, _GlobalDataset) and \
                    not isinstance(input._dset, _FeedDataset) and \
                    not isinstance(input._dset, _Dataset) and \
                    not isinstance(input._dset, DatasetConsumptionConfig) and \
                    not isinstance(input._dset, FileDataset):
                instance_id = node._id
                inputs[_unify_input_port_name(node.name, instance_id, input_name, input)] = \
                    _extract_input_port_value(input)
    return _AttrDict(**inputs)


def _unify_input_port_name(node_name, node_id, port_name, port_value):
    """Get input port's unified name.

    if the port is corresponded to a subgraph's pipeline parameter, take it as the parameter name
    otherwise, take it as {node_name}:{port_name}

    :param node_name: name of the node where the port is
    :type node_name: str
    :param node_id: id of the node where the port is
    :type node_id: str
    :param port_name: port's name
    :type port_name: str
    :param port_value: the port's input
    :type: obj
    """
    if isinstance(port_value, Input):
        # if it is _InputBuilder type, that means it comes from a subgraph's pipeline parameter
        if isinstance(port_value._dset, Input):
            return port_value._dset.name
        elif isinstance(port_value._dset, _GlobalDataset):
            return '{}_{}'.format(port_value._dset.data_reference_name, node_id)
        elif isinstance(port_value._dset, _Dataset):
            return '{}_{}'.format(port_value._dset.name, node_id)
        elif isinstance(port_value._dset, PipelineParameter):
            return port_value._dset.name
        else:
            return '{}:{}'.format(node_name, port_name)
    else:
        return '{}:{}'.format(node_name, port_name)


def _extract_input_port_value(port_value):
    """Extract the underlying _InputBuilder.

    This is needed when the input comes from sub graph's pipeline parameter

    :param port_value: the port's input
    :type port_value: obj
    """
    if isinstance(port_value, Input):
        if isinstance(port_value._dset, Input):
            return port_value._dset
        else:
            return port_value
    else:
        return port_value


def persistent_locals(func):
    """
    Use bytecode injection to add try...finally statement around code to persistent the locals in the function.

    It will change the func bytecode like this:
        def func(__self, *func_args):
            try:
               the func code...
            finally:
               __self._locals = locals().copy()
               del __self._locals['__self']

    You can get the locals in func by this code:
        persistent_locals_func = persistent_locals(your_func)
        # Execute your func
        result = persistent_locals_func(*args)
        # Get the locals in the func.
        func_locals = persistent_locals_func._locals
    """
    bytecode = Bytecode.from_code(func.__code__)

    # Add `try` at the begining of the code
    finally_label = Label()
    bytecode.insert(0, Instr("SETUP_FINALLY", finally_label))
    # Add `final` at the end of the code
    added_param = '__self'

    copy_locals_instructions = [
        # __self._locals = locals().copy()
        Instr("LOAD_GLOBAL", 'locals'),
        Instr("CALL_FUNCTION", 0),
        Instr("LOAD_ATTR", 'copy'),
        Instr("CALL_FUNCTION", 0),
        Instr("LOAD_FAST", added_param),
        Instr("STORE_ATTR", '_locals'),
    ]

    remove_param_instructions = [
        # del __self._locals['__self']
        Instr("LOAD_FAST", added_param),
        Instr("LOAD_ATTR", '_locals'),
        Instr("LOAD_CONST", added_param),
        Instr("DELETE_SUBSCR"),
    ]

    if sys.version_info < (3, 8):
        # python 3.6 and 3.7
        bytecode.extend([finally_label] + copy_locals_instructions + remove_param_instructions +
                        [Instr("END_FINALLY"), Instr("LOAD_CONST", None), Instr("RETURN_VALUE")])
    elif sys.version_info < (3, 9):
        # In python 3.8, add new instruction CALL_FINALLY
        # https://docs.python.org/3.8/library/dis.html?highlight=call_finally#opcode-CALL_FINALLY
        bytecode.insert(-1, Instr("CALL_FINALLY", finally_label))
        bytecode.extend(
            [finally_label] + copy_locals_instructions + remove_param_instructions +
            [Instr("END_FINALLY"), Instr("LOAD_CONST", None), Instr("RETURN_VALUE")])
    elif sys.version_info < (3, 10):
        # In python 3.9, add new instruction RERAISE and CALL_FINALLY is removed.
        # https://docs.python.org/3.9/library/dis.html#opcode-RERAISE
        raise_error = Label()
        extend_instructions = \
            copy_locals_instructions + remove_param_instructions + \
            [Instr("JUMP_FORWARD", raise_error), finally_label] + \
            copy_locals_instructions + remove_param_instructions + [Instr("RERAISE"), raise_error]
        bytecode[-1:-1] = extend_instructions
    else:
        # python 3.10
        bytecode[-1:-1] = copy_locals_instructions + remove_param_instructions
        bytecode.extend([finally_label] + copy_locals_instructions + remove_param_instructions + [Instr("RERAISE", 0)])
    # Add __self to function args
    bytecode.argnames.insert(0, added_param)
    bytecode.argcount = bytecode.argcount + 1
    code = bytecode.to_code()
    func = FunctionType(code, func.__globals__, func.__name__, func.__defaults__, func.__closure__)
    return PersistentLocalsFunction(func)


class PersistentLocalsFunction(object):
    """Wrapper class for the 'persistent_locals' decorator.

    Refer to the docstring of instances for help about the wrapped
    function.
    """

    def __init__(self, func):
        self._locals = {}
        # make function an instance method
        self._func = MethodType(func, self)

    def __call__(self, *args, **kwargs):
        return self._func(*args, **kwargs)
