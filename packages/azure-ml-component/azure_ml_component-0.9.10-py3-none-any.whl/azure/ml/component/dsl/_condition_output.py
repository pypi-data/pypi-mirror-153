# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from pathlib import Path
from typing import Union

from azureml.exceptions import UserErrorException

from azure.ml.component._pipeline_expression import PipelineExpression
from azure.ml.component._pipeline_parameters import PipelineParameter
from azure.ml.component.component import Output, Component, DataStoreMode

_DATA_PATH = Path(__file__).resolve().parent / 'data'
_COMPONENT_PATH = _DATA_PATH / 'condition_output' / 'component_spec.yaml'


def _condition_output(
        *,
        condition: Union[Output, PipelineExpression, bool, PipelineParameter],
        input_a: Output = None,
        input_b: Output = None
) -> Component:
    """
    Create a dsl.condition_output component to link output to input_a or input_b depends on condition.

    Below is an example of using expression result to control which step is executed.
    If pipeline parameter 'int_param1' > 'int_param2', then 'input_a' will be linked as output,
    else, the 'input_b' will be linked.

    .. code-block:: python

    @dsl.pipeline(default_compute_target='aml-compute')
    def pipeline_func(int_param1: int, int_param2: int):
        step1 = component_func()
        step2 = another_component_func()
        condition_output_step = dsl.condition_output(
            condition=int_param1 > int_param2,
            input_a=true_step.outputs.output,
            input_b=false_step.outputs.output
        )
        # use 'step.outputs.output' to reference the output.
        post_process_component(
            input=condition_output_step.outputs.output
        )

    :param condition: The condition of the execution flow.
        The value could be a boolean type control output or a pipeline expression.
    :type condition: Union[azure.ml.component.component.Output,
        azure.ml.component._pipeline_expression.PipelineExpression,
        bool, azure.ml.component._pipeline_parameter.PipelineParameter]
    :param input_a: Output linked if condition resolved result is true.
    :type input_a: azure.ml.component.component.Output
    :param input_b: Output linked if condition resolved result is false.
    :type input_b: azure.ml.component.component.Output
    :return: The dsl.condition component.
    :rtype: azure.ml.component.Component
    """
    _validate_parameters(condition, input_a, input_b)
    condition_output_component_func = Component.from_yaml(yaml_file=_COMPONENT_PATH)
    component = condition_output_component_func(
        condition=condition, input_a=input_a, input_b=input_b
    )
    component.inputs.input_a.configure(mode=DataStoreMode.DIRECT)
    component.inputs.input_b.configure(mode=DataStoreMode.DIRECT)
    component.outputs.output.configure(mode=DataStoreMode.LINK)
    return component


def _validate_parameters(condition, input_a, input_b):
    if not isinstance(condition, (Output, PipelineExpression, PipelineParameter, bool)):
        raise UserErrorException(
            f"'condition' of dsl.condition_output must be an instance of "
            f"{Output}, {PipelineExpression}, {PipelineParameter} "
            f"or {bool.__name__}, got {type(condition)}.")
    if isinstance(condition, PipelineExpression):
        # Create expression node, give output as condition.
        condition = condition._create_dynamic_component().outputs.output
    # Check if output is a control output.
    if isinstance(condition, Output) and condition._owner is not None:
        output_definition = condition._owner._definition.outputs.get(condition._name)
        if output_definition and not output_definition.is_control:
            raise UserErrorException(
                f"'condition' of dsl.condition_output must have 'is_control' filed "
                f"with value 'True', got {output_definition.is_control}")
    # Note: We don't validate input_a and input_b's type here,
    # make them be validated as general command component input.
    if input_a is None and input_b is None:
        raise UserErrorException(
            "'input_a' and 'input_b' of dsl.condition_output cannot both be None.")
