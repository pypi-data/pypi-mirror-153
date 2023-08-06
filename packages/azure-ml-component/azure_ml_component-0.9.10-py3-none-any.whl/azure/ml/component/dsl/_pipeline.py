# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""A decorator which builds a :class:azure.ml.component.Pipeline."""
import sys
from collections import OrderedDict
from functools import wraps
from inspect import Parameter, signature
from typing import Callable, Any, TypeVar

from azure.ml.component._core._types import _GroupAttrDict
from .._util._exceptions import MissingPositionalArgsError, MultipleValueError, TooManyPositionalArgsError, \
    UnexpectedKeywordError, UnsupportedParameterKindError, KeywordError
from .._util._loggerfactory import _PUBLIC_API, track
from .._util._utils import _change_profile


# hint vscode intellisense
_TFunc = TypeVar("_TFunc", bound=Callable[..., Any])


def pipeline(name=None, version=None, display_name=None, description=None,
             default_compute_target=None, default_datastore=None, tags=None,
             non_pipeline_parameters=None, is_deterministic=None):
    """Build a pipeline which contains all nodes and sub-pipelines defined in this function.

    .. remarks::
        Note that a dsl.pipeline can be used to create pipelines with a complex layered structure.
        The following pseudo-code shows how to create a nested pipeline using this decorator.

        .. code-block:: python

            # A sub-pipeline defined with decorator
            @dsl.pipeline(name='sub pipeline', description='sub-pipeline description')
            def sub_pipeline(pipeline_parameter1, pipeline_parameter2):
                # component1 and component2 will be added into the current sub pipeline
                component1 = component1_func(xxx, xxx)
                component2 = component2_func(xxx, xxx)
                # A decorated pipeline function needs to return outputs.
                # In this case, the sub_pipeline has two outputs: component1's output1 and component2's output1, and
                # let's rename them to 'renamed_output1' and 'renamed_output2'
                return {'renamed_output1': component1.outputs.output1, 'renamed_output2': component2.outputs.output1}

            # Assign values to parameters. "xxx" is the real value of the parameter, it might be a Dataset or other
            # hyperparameters.
            param1 = xxx
            param2 = xxx

            # A parent pipeline defined with the decorator
            @dsl.pipeline(name='pipeline', description='parent pipeline description')
            def parent_pipeline(pipeline_parameter1):
                # component3 and sub_pipeline1 will be added into the current parent pipeline
                component3 = component3_func(xxx, xxx)
                # the sub_pipeline is called in the pipeline decorator, this call will return a pipeline with
                # nodes=[component1, component2] and its outputs=component2.outputs
                sub_pipeline1 = sub_pipeline(pipeline_parameter1=param1, pipeline_parameter2=param2)
                # The outputs of the components in the pipeline are not exposed.

            # E.g.: This call returns a pipeline with nodes=[component1, component2], outputs=component2.outputs.
            sub_pipeline2 = sub_pipeline(pipeline_parameter1=param1, pipeline_parameter2=param2)

            # E.g.: This call returns a pipeline with nodes=[sub_pipeline1, component3], outputs={}.
            pipeline1 = parent_pipeline(pipeline_parameter1=param1)

        Note: Parameters in pipeline decorator functions will be stored as a substitutable part of the pipeline,
        which means you can change them directly in the re-submit or other operations in the future without
        re-construct a new pipeline.
        E.g.: change pipeline_parameter1 of parent_pipeline when submit it.

        .. code-block:: python

            pipeline1.submit(parameters={"pipeline_parameter1": changed_param})

        Besides, If there are nested pipelines decorators, as illustrated below, only the outermost pipeline
        parameters, i.e. outer_parameter in this example, will be transformed to a changeable parameter for this
        pipeline.
        E.g.:

        .. code-block:: python

            @dsl.pipeline(name='nested pipeline', description='nested-pipeline description')
            def outer_pipeline(outer_parameter):
                component1 = component1_func(xxx, xxx)
                @dsl.pipeline(name='inner pipeline', description='inner-pipeline description')
                    def inner_pipeline(inner_parameter):
                        component2 = component2_func(xxx, xxx)

    :param name: The name of pipeline component.
    :type name: str
    :param version: The version of pipeline component.
    :type version: str
    :param display_name: The display name of pipeline component.
    :type display_name: str
    :param description: The description of the built pipeline.
    :type description: str
    :param default_compute_target: The compute target of the built pipeline.
        Could be a compute target object or the string name of a compute target in the workspace.
        The priority of the compute target assignment: the component's runsettings > the sub pipeline's default compute
        target > the parent pipeline's default compute target.
        Optionally, if the compute target is not available at pipeline creation time, you may specify a tuple of
        ('compute target name', 'compute target type') to avoid fetching the compute target object (AmlCompute
        type is 'AmlCompute' and RemoteCompute type is 'VirtualMachine').
    :type: default_compute_target: azureml.core.compute.DsvmCompute
                        or azureml.core.compute.AmlCompute
                        or azureml.core.compute.RemoteCompute
                        or azureml.core.compute.HDInsightCompute
                        or str
                        or tuple
    :param default_datastore: The default datastore of pipeline.
    :type default_datastore: str or azureml.core.Datastore
    :param tags: The tags of pipeline component.
    :type tags: dict[str, str]
    :param non_pipeline_parameters: The names of non pipeline parameters in dsl function parameter list.
    :type non_pipeline_parameters: list[str]
    :param is_deterministic: Specify whether the pipeline component can be reused or not.
    :type is_deterministic: bool
    """
    def pipeline_decorator(func: _TFunc) -> _TFunc:
        # Local reference to resolve circular reference
        from .._pipeline_component_definition_builder import _definition_builder_stack, _definition_id_now_build
        from ._pipeline_component_definition_builder_generator import PipelineComponentDefinitionBuilderGenerator
        parent_def_id = None if len(_definition_id_now_build) == 0 else _definition_id_now_build[-1]
        _definition_builder_generator = PipelineComponentDefinitionBuilderGenerator(
            non_pipeline_parameters=non_pipeline_parameters,
            name=name, version=version, display_name=display_name, description=description,
            default_compute_target=default_compute_target, default_datastore=default_datastore,
            tags=tags, func=func, parent_def_id=parent_def_id, is_deterministic=is_deterministic)
        from ..pipeline import Pipeline
        _original_profiler = sys.getprofile()

        @wraps(func)
        def wrapper(*args, **kwargs) -> Pipeline:
            # Default args will be added here.
            # dynamic_param_name is the name of var keyword args, like **kwargs has param name 'kwargs'
            # dynamic_param_value is a dict indicate the value of var keyword args
            provided_positional_args, dynamic_param_name, dynamic_param_value = _validate_args(func, args, kwargs)
            # Convert args to kwargs
            kwargs.update(provided_positional_args)

            @track(activity_type=_PUBLIC_API, activity_name="pipeline_definition_build")
            def build_top_pipeline_definition():
                """
                Build pipeline definition.

                This function was extracted to ensure log behavior
                    perform only once even if there are sub pipeline inside function.
                """
                return _definition_builder.build()

            _definition_builder = _definition_builder_generator.get_or_create_pipeline_definition_builder(
                user_init_args=kwargs, dynamic_param_name=dynamic_param_name, dynamic_param_value=dynamic_param_value
            )
            # Remove non pipeline parameters from `kwargs` if needed
            if non_pipeline_parameters:
                for p_name in non_pipeline_parameters:
                    if p_name in kwargs:
                        kwargs.pop(p_name)
            _definition = _definition_builder._component_definition
            if _definition is None:
                # 1. Avoid duplicate track generated by recursive build same pipeline.
                # 2. Avoid track inner sub_pipeline definition build.
                #   a. Defined inner
                #       @dsl.pipeline()
                #       def parent():
                #           @dsl.pipeline()
                #               def sub(): # sub's definition will NOT be tracked
                #                   ...
                #   b. Defined outer but no independent call or call after parent definition built
                #       @dsl.pipeline()
                #       def sub():
                #          ...
                #       @dsl.pipeline()
                #       def parent():
                #           sub()
                #       pipeline = parent()
                #       pipeline2 = sub() # sub's definition will NOT be tracked
                #   c. Defined outer with independent call first
                #       @dsl.pipeline()
                #       def sub():
                #          ...
                #       @dsl.pipeline()
                #       def parent():
                #           sub()
                #       pipeline1 = sub() # sub's definition will BE tracked
                #       pipeline2 = parent()
                _definition = build_top_pipeline_definition() if _definition_builder_stack.is_empty() \
                    else _definition_builder.build()

            # Track the real pipeline creation elapse time without build definition here.
            @track(activity_type=_PUBLIC_API, activity_name="pipeline_creation")
            def construct_top_pipeline():
                """
                Construct top pipeline function.

                This function was extracted to ensure log behavior
                    perform only once even if there are sub pipeline inside function.
                """
                top_pipeline = construct_sub_pipeline()
                return top_pipeline

            def construct_sub_pipeline():
                # Skip trace inner variables during pipeline creation.
                # We just need variable name in dsl.pipeline function.
                with _change_profile(_original_profiler):
                    return Pipeline(
                        nodes=list(_definition.components.values()), outputs=_definition._outputs_mapping,
                        workspace=_definition.workspace, name=_definition.name, description=_definition.description,
                        default_compute_target=_definition._default_compute_target,
                        default_datastore=_definition._default_datastore,
                        _use_dsl=True, _definition=_definition, _init_params=kwargs)
            return construct_top_pipeline() if _definition_builder_stack.is_empty() else construct_sub_pipeline()

        wrapper._is_dsl_pipeline = True
        return wrapper

    return pipeline_decorator


_RESERVED_KEYS = ['self']


def _validate_args(func, args, kwargs):
    # Positional arguments validate
    all_parameters = [param for _, param in signature(func).parameters.items()]
    # Implicit parameter are *args and **kwargs
    if any(param.kind in {param.VAR_POSITIONAL} for param in all_parameters):
        raise UnsupportedParameterKindError(func.__name__)
    dynamic_param_name = next((param.name for param in all_parameters if param.kind == param.VAR_KEYWORD), None)
    dynamic_param_value = {}
    all_parameter_keys = [param.name for param in all_parameters if param.kind != param.VAR_KEYWORD]
    if any(key in _RESERVED_KEYS for key in all_parameter_keys):
        raise KeywordError(
            f'Reserved parameter key occurs in pipeline function {func.__name__!r}, '
            f'reserved keys: {_RESERVED_KEYS}.')
    empty_parameters = {
        param.name: param for param in all_parameters
        if param.default is Parameter.empty and param.kind != param.VAR_KEYWORD}
    min_num = len(empty_parameters)
    max_num = len(all_parameter_keys)
    if len(args) > max_num:
        raise TooManyPositionalArgsError(func.__name__, min_num, max_num, len(args))

    provided_args = OrderedDict({
        param.name: args[idx] for idx, param in enumerate(all_parameters) if idx < len(args)})
    for _k in kwargs.keys():
        if _k not in all_parameter_keys:
            if dynamic_param_name:
                dynamic_param_value[_k] = kwargs[_k]
                continue
            raise UnexpectedKeywordError(func.__name__, _k, all_parameter_keys)
        if _k in provided_args.keys():
            raise MultipleValueError(func.__name__, _k)
        provided_args[_k] = kwargs[_k]

    if len(provided_args) < len(empty_parameters):
        missing_keys = empty_parameters.keys() - provided_args.keys()
        raise MissingPositionalArgsError(func.__name__, missing_keys)
    return provided_args, dynamic_param_name, _GroupAttrDict(dynamic_param_value)
