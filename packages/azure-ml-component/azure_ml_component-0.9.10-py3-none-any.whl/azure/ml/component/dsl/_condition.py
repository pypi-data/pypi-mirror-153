# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""This module is used to create a dsl.condition component."""
from typing import Union

from azureml.exceptions import UserErrorException

from azure.ml.component import Component, Pipeline
from azure.ml.component._pipeline_expression import PipelineExpression
from azure.ml.component._pipeline_parameters import PipelineParameter
from azure.ml.component._util._yaml_utils import YAML
from azure.ml.component.component import Output


def _condition(
        *,
        condition: Union[Output, PipelineExpression, bool, PipelineParameter],
        true_block: Union[Component, Pipeline] = None,
        false_block: Union[Component, Pipeline] = None
) -> Component:
    """
    Create a dsl.condition component to provide runtime condition graph experience.

    Below is an example of using expression result to control which step is executed.
    If pipeline parameter 'int_param1' > 'int_param2', then 'true_step' will be executed,
    else, the 'false_step' will be executed.

    .. code-block:: python

    @dsl.pipeline(default_compute_target='aml-compute')
    def pipeline_func(int_param1: int, int_param2: int):
        true_step = component_func()
        false_step = another_component_func()
        dsl.condition(
            condition=int_param1 > int_param2,
            true_block=true_step,
            false_block=false_step
        )

    :param condition: The condition of the execution flow.
        The value could be a boolean type control output or a pipeline expression.
    :type condition: Union[azure.ml.component.component.Output,
        azure.ml.component._pipeline_expression.PipelineExpression,
        bool, azure.ml.component._pipeline_parameter.PipelineParameter]
    :param true_block: Block to be executed if condition resolved result is true.
    :type true_block: Union[azure.ml.component.Component, azure.ml.component.Pipeline]
    :param false_block: Block to be executed if condition resolved result is false.
    :type false_block: Union[azure.ml.component.Component, azure.ml.component.Pipeline]
    :return: The dsl.condition component.
    :rtype: azure.ml.component.Component
    """
    _validate_parameters(condition, true_block, false_block)
    condition_component = _create_condition_component(condition)
    if true_block:
        true_block._set_control_by(condition_component, True.__repr__().lower())
    if false_block:
        false_block._set_control_by(condition_component, False.__repr__().lower())
    return condition_component


def _create_condition_component(condition):
    from azure.ml.component._core._component_definition import ControlComponentDefinition
    condition_dct = YAML().safe_load(_condition_yaml_str)
    definition = ControlComponentDefinition._from_dict(condition_dct)
    return Component(definition=definition, _init_params={definition._control_parameter_name: condition})


def _validate_parameters(condition, true_block, false_block):
    if not isinstance(condition, (Output, PipelineExpression, PipelineParameter, bool)):
        raise UserErrorException(
            f"'condition' of dsl.condition must be an instance of "
            f"{Output}, {PipelineExpression}, {PipelineParameter} or "
            f"{bool.__name__}, got {type(condition)}.")
    if isinstance(condition, PipelineExpression):
        # Create expression node, give output as condition.
        condition = condition._create_dynamic_component().outputs.output
    # Check if output is a control output.
    if isinstance(condition, Output) and condition._owner is not None:
        output_definition = condition._owner._definition.outputs.get(condition._name)
        if output_definition and not output_definition.is_control:
            raise UserErrorException(
                f"'condition' of dsl.condition must have 'is_control' filed "
                f"with value 'True', got {output_definition.is_control}")
    block_type_error_msg = \
        f"'%s' of dsl.condition must be an instance of " \
        f"{Component} or {Pipeline}, got '%s'."
    if true_block is not None and not isinstance(true_block, Component):
        raise UserErrorException(block_type_error_msg % ('true_block', type(true_block)))
    if false_block is not None and not isinstance(false_block, Component):
        raise UserErrorException(block_type_error_msg % ('false_block', type(false_block)))
    if true_block is None and false_block is None:
        raise UserErrorException(
            "'true_block' and 'false_block' of dsl.condition cannot both be None.")
    if true_block == false_block:
        raise UserErrorException(
            "'true_block' and 'false_block' of dsl.condition cannot be the same object.")


_condition_yaml_str = """name: dsl_condition
display_name: Condition If-Else
version: 0.0.1
type: _ControlComponent
control_type: IfElse
control_parameter_name: condition
inputs:
  condition:
    type: boolean
    optional: false
outputs:
"""
