# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""This file includes the type annotations which could be used in dsl.pipeline.

.. remarks::
    This is a preview feature.
    The following pseudo-code shows how to create a pipeline with such annotations.

    .. code-block:: python

        @dsl.pipeline()
        def some_pipeline(
            int_param: Integer(min=0),
            str_param: String() = 'abc',
        ):
            pass

"""
from azure.ml.component._core._types import (
    Boolean,
    Enum,
    Float,
    Input,
    Integer,
    Output,
    String,
    is_parameter_group
)
from azure.ml.component._core._types import _parameter_group as parameter_group

__all__ = [
    'Boolean',
    'Enum',
    'Float',
    'Input',
    'Integer',
    'Output',
    'String',
    'parameter_group',
    'is_parameter_group',
]
