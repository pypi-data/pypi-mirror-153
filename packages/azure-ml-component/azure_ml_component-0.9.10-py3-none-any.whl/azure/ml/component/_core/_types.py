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
import argparse
import copy
import functools
import math
import _thread
import pathlib
import sys
from collections import OrderedDict

from typing import Optional, Union, Sequence, Iterable, List
from enum import EnumMeta
from enum import Enum as PyEnum
from inspect import Parameter, signature

from azure.ml.component._util._attr_dict import _AttrDict
from azure.ml.component._util._loggerfactory import _LoggerFactory
from azure.ml.component._util._utils import _get_parameter_static_value
from azureml.exceptions import UserErrorException

from azure.ml.component._util._exceptions import RequiredParamParsingError, DSLComponentDefiningError

_logger = None


def _get_logger():
    global _logger
    if _logger is not None:
        return _logger
    _logger = _LoggerFactory.get_logger()
    return _logger


class _IOBase:
    """Define the base class of Input/Output/Parameter class."""

    def __init__(self, name=None, type=None, description=None):
        """Define the basic properties of io definition."""
        self._name = name
        self._type = type
        self._description = description
        # Indicate the annotation is auto generated or completely created by user.
        # If auto gen is True then the definition can be updated using component definition.
        self._auto_gen = False
        self._is_primitive_type = self._get_is_primitive_type(type)

    @staticmethod
    def _get_is_primitive_type(typ):
        typ = typ[0] if type(typ) is list else typ
        return typ in _Param._PARAM_TYPE_STRING_MAPPING

    @classmethod
    def _from_dict(cls, dct: dict):
        """Convert a dict to an Input object."""
        name = dct.pop('name')
        keys = signature(cls.__init__).parameters
        obj = cls(**{key: val for key, val in dct.items() if key in keys})
        obj._name = name
        return obj


class Input(_IOBase):
    """Define an input of a component."""

    def __init__(self, type='path', description=None, optional=None):
        """Define an input definition for a component.

        :param type: Type of the input.
        :type type: str
        :param description: Description of the input.
        :type description: str
        :param optional: If the input is optional.
        :type optional: bool
        """
        # As an annotation, it is not allowed to initialize the name.
        # The name will be updated by the annotated variable name.
        super().__init__(name=None, type=type, description=description)
        self._optional = optional
        self._default = None
        self._has_default = False

    @property
    def name(self) -> str:
        """Return the name of the input."""
        return self._name

    @property
    def type(self) -> Union[str, List]:
        """Return the type of the input."""
        return self._type

    @property
    def description(self) -> str:
        """Return the description of the input."""
        return self._description

    @property
    def optional(self) -> bool:
        """Return whether the input is optional."""
        if self._optional is None:
            return self._default is None and self._has_default
        return self._optional

    def _get_hint(self, new_line_style=False):
        comment_str = self.description.replace('"', '\\"') if self.description else self.type
        comment_str = str(comment_str)
        if self._optional is True:
            comment_str += '(optional)'
        return '"""%s"""' % comment_str if comment_str and new_line_style else comment_str

    def _to_dict(self, remove_name=True):
        """Convert the Input object to a dict."""
        keys = ['name', 'type', 'description', 'optional']
        if remove_name:
            keys.remove('name')
        result = {key: getattr(self, key) for key in keys}
        return _remove_empty_values(result)

    def _to_python_code(self):
        """Return the representation of this parameter in annotation code, used in code generation."""
        parameters = []
        if self._type is not None and self._type != 'path':
            parameters.append('type={!r}'.format(self._type))
        if self._description is not None:
            parameters.append('description={!r}'.format(self._description))
        if self._optional is not None:
            parameters.append('optional={}'.format(self._optional))
        return "{type_name}({parameters})".format(
            type_name=self.__class__.__name__, parameters=', '.join(parameters))

    def _update_default(self, default_value):
        """Update provided default values."""
        self._default = default_value
        self._has_default = True


class _Path(Input):
    """Define an input path of a component."""

    def __init__(self, description=None, optional=None):
        """Define an input path for a component."""
        super().__init__(type='path', description=description, optional=optional)


class _InputFile(Input):
    """InputFile indicates an input which is a file."""

    def __init__(self, description=None, optional=None):
        """Initialize an input file port Declare type to use your customized port type."""
        super().__init__(type='AnyFile', description=description, optional=optional)


class _InputFileList:

    def __init__(self, inputs: List[_Path]):
        self.validate_inputs(inputs)
        self._inputs = inputs
        for i in inputs:
            if i.arg_name is None:
                i.arg_name = i.name

    @classmethod
    def validate_inputs(cls, inputs):
        for i, port in enumerate(inputs):
            if not isinstance(port, (_InputFile, _Path)):
                msg = "You could only use Input in an input list, got '%s'." % type(port)
                raise DSLComponentDefiningError(msg)
            if port.name is None:
                raise DSLComponentDefiningError("You must specify the name of the %dth input." % i)
        if all(port.optional for port in inputs):
            raise DSLComponentDefiningError("You must specify at least 1 required port in the input list, got 0.")

    def add_to_arg_parser(self, parser: argparse.ArgumentParser):
        for port in self._inputs:
            port.add_to_arg_parser(parser)

    def load_from_args(self, args):
        """Load the input files from parsed args from ArgumentParser."""
        files = []
        for port in self._inputs:
            str_val = getattr(args, port.name, None)
            if str_val is None:
                if not port.optional:
                    raise RequiredParamParsingError(name=port.name, arg_string=port.arg_string)
                continue
            files += [str(f) for f in pathlib.Path(str_val).glob('**/*') if f.is_file()]
        return files

    def load_from_argv(self, argv=None):
        if argv is None:
            argv = sys.argv
        parser = argparse.ArgumentParser()
        self.add_to_arg_parser(parser)
        args, _ = parser.parse_known_args(argv)
        return self.load_from_args(args)

    @property
    def inputs(self):
        return self._inputs


class Output(_IOBase):
    """Define an output of a component."""

    def __init__(self, type='path', description=None, is_control=None):
        """Define an output of a component.

        :param type: Type of the output.
        :type type: str
        :param description: Description of the output.
        :type description: str
        :param is_control: Determine the Output is control or not.
        :type is_control: bool
        """
        # The name will be updated by the annotated variable name.
        super().__init__(name=None, type=type, description=description)
        self._is_control = is_control

    @property
    def name(self) -> str:
        """Return the name of the output."""
        return self._name

    @property
    def type(self) -> str:
        """Return the type of the output."""
        return self._type

    @property
    def description(self) -> str:
        """Return the description of the output."""
        return self._description

    @property
    def is_control(self):
        """Return the output is control output or not."""
        return self._is_control

    def _get_hint(self, new_line_style=False):
        comment_str = self.description.replace('"', '\\"') if self.description else self.type
        comment_str += ' (is_control)' if self.is_control else ''
        return '"""%s"""' % comment_str if comment_str and new_line_style else comment_str

    def _to_dict(self, remove_name=True):
        """Convert the Output object to a dict."""
        keys = ['name', 'type', 'description', 'is_control']
        if remove_name:
            keys.remove('name')
        result = {key: getattr(self, key) for key in keys}
        return _remove_empty_values(result)

    def _to_python_code(self):
        """Return the representation of this parameter in annotation code, used in code generation."""
        parameters = []
        if self._type is not None and self._type != 'path':
            parameters.append('type={!r}'.format(self._type))
        if self._description is not None:
            parameters.append('description={!r}'.format(self._description))
        if self._is_control is not None:
            parameters.append('is_control')
        return "{type_name}({parameters})".format(
            type_name=self.__class__.__name__, parameters=', '.join(parameters))


class _OutputFile(Output):
    """OutputFile indicates an output which is a file."""

    def __init__(self, description=None):
        """Initialize an output file port Declare type to use your custmized port type."""
        super().__init__(type='AnyFile', description=description)


class _Param(_IOBase):
    """This is the base class of component parameters.

    The properties including name/type/default/options/optional/min/max will be dumped in component spec.
    When invoking a component, param.parse_and_validate(str_val) is called to parse the command line value.
    """

    DATA_TYPE = None  # This field is the corresponding python type of the class, e.g. str/int/float.
    TYPE_NAME = None  # This field is the type name of the parameter, e.g. string/integer/float.
    EMPTY = Parameter.empty

    _PARAM_VALIDATORS = {
        'String': None,
        'Float': None,
        'Integer': None,
        'Int': None,
        'Boolean': None,
        'Enum': None,
        'string': None,
        'float': None,
        'integer': None,
        'int': None,
        'boolean': None,
        'enum': None,

        # The following types are internal usage for built-in modules.
        'Script': None,
        'ColumnPicker': None,
        'Credential': None,
        'ParameterRange': None
    }  # These validators are used to validate parameter values.

    _PARAM_PARSERS = {
        'Float': float,
        'Integer': int,
        'Int': int,
        'Boolean': lambda v: v.lower() == 'true',
        'float': float,
        'integer': int,
        'int': int,
        'boolean': lambda v: v.lower() == 'true',
    }
    _PARAM_TYPE_MAPPING = {str: 'string', int: 'integer', float: 'float', bool: 'boolean'}
    _PARAM_TYPE_STRING_MAPPING = {'string': str, 'integer': int, 'int': int, 'float': float,
                                  'double': float, 'boolean': bool, 'enum': str}

    def __init__(
            self, name=None, description=None, enum=None, optional=None, min=None, max=None, is_control=None,
    ):
        """Define a parameter of a component."""
        super().__init__(name=name, type=self.TYPE_NAME, description=description)
        # _default None, optional False at first
        # _default None, optional True after call _update_default(None)
        self._default = None
        self._has_default = False
        self._enum = enum
        self._optional = optional
        self._min = min
        self._max = max
        self._is_control = is_control
        self._allowed_types = ()
        # TODO: Maybe a parameter could have several allowed types? For example, json -> List/Dict?
        if self.DATA_TYPE:
            self._allowed_types = (self.DATA_TYPE,)

    @property
    def name(self) -> str:
        return self._name

    @property
    def type(self) -> Optional[str]:
        return self._type

    @property
    def description(self) -> Optional[str]:
        return self._description

    @property
    def optional(self) -> bool:
        """Return whether the parameter is optional."""
        if self._optional is None:
            return self._default is None and self._has_default
        return self._optional

    @property
    def default(self) -> Optional[Union[str, int, float]]:
        """Return the default value of the parameter."""
        return self._default

    @property
    def enum(self) -> Optional[Sequence[str]]:
        """Return the enum values of the parameter for an enum parameter."""
        return self._enum

    @property
    def max(self) -> Optional[Union[int, float]]:
        """Return the maximum value of the parameter for a numeric parameter."""
        return self._max

    @property
    def min(self) -> Optional[Union[int, float]]:
        """Return the minimum value of the parameter for a numeric parameter."""
        return self._min

    @property
    def is_control(self):
        """Return the parameter is control output or not."""
        return self._is_control

    @classmethod
    def _from_dict(cls, dct: dict):
        """Convert a dict to an Parameter object."""
        keys = signature(cls.__init__).parameters
        if 'enum_values' in dct:
            dct['enum'] = dct.pop('enum_values')
        obj = cls(**{k: v for k, v in dct.items() if k in keys})
        obj._update_name(dct['name'])
        if 'type' in dct:
            obj._type = dct.pop('type')
        if 'default' in dct:
            # Do not call _update_default here
            # because we'd like to keep optional in yaml as it was
            obj._default = dct.pop('default')
        return obj

    @classmethod
    def _is_valid_type(cls, type):
        """Return whether the type is a valid parameter type."""
        # Special handle for type Int
        patch_types = ["Int"]
        if type in patch_types:
            _get_logger().warning(
                "{!r} is not supported type, assuming it's a parameter, "
                "reference https://aka.ms/azure-ml-component-specs for all supported input types.".format(type)
            )
            return True
        return isinstance(type, str) and type in cls._PARAM_VALIDATORS

    @classmethod
    def _parse_param(cls, type, str_value, raise_if_fail=True):
        """Parse the str value to param value according to the param type."""
        parser = cls._PARAM_PARSERS.get(type)
        if str_value is None or not parser:
            return str_value
        try:
            return parser(str_value)
        except ValueError:
            # For ValueError, if raise_if_fail, raise the exception, otherwise return the original value.
            if raise_if_fail:
                raise
            return str_value

    @classmethod
    def parse_param_type(cls, type):
        """Map python type to parameter type string."""
        return cls._PARAM_TYPE_MAPPING.get(type) if type in cls._PARAM_TYPE_MAPPING else type

    @classmethod
    def parse_param_type_string(cls, type_string):
        """Map parameter type string to python type name."""
        return cls._PARAM_TYPE_STRING_MAPPING.get(type_string).__name__\
            if type_string in cls._PARAM_TYPE_STRING_MAPPING else type_string

    def _get_hint(self, new_line_style=False):
        comment_str = self.description.replace('"', '\\"') if self.description else self.type
        hint_item = ['optional'] if self._optional is True else []
        hint_item.extend(['%s: %s' % (key, val) for key, val in
                          zip(['min', 'max', 'enum', 'is_control'],
                              [self._min, self._max, self._enum, self._is_control]) if val])
        hint_str = ', '.join(hint_item)
        comment_str += ' (%s)' % hint_str if hint_str else ''
        return '"""%s"""' % comment_str if comment_str and new_line_style else comment_str

    def _to_dict(self, remove_name=True) -> dict:
        """Convert the Param object to a dict."""
        keys = ['name', 'type', 'description', 'min', 'max', 'enum', 'default', 'optional', 'is_control']
        if remove_name:
            keys.remove('name')
        result = {key: getattr(self, key) for key in keys}
        return _remove_empty_values(result)

    def _parse(self, str_val: str):
        """Parse str value passed from command line.

        :param str_val: The input string value from the command line.
        :return: The parsed value.
        """
        return str_val

    def _parse_and_validate(self, str_val):
        """Parse the str_val passed from the command line and validate the value.

        :param str_val: The input string value from the command line.
        :return: The parsed value, an exception will be raised if the value is invalid.
        """
        str_val = self._parse(str_val) if isinstance(str_val, str) else str_val
        self._validate_or_throw(str_val)
        return str_val

    def _update_name(self, name):
        self._name = name

    def _update_default(self, default_value):
        """Update provided default values.

        Here we need to make sure the type of default value is allowed or it could be parsed..
        """
        if default_value is not None and not isinstance(default_value, self._allowed_types):
            try:
                default_value = self._parse(default_value)
            except Exception as e:
                if self.name is None:
                    msg = "Default value of %s cannot be parsed, got '%s', type = %s." % (
                        type(self).__name__, default_value, type(default_value)
                    )
                else:
                    msg = "Default value of %s '%s' cannot be parsed, got '%s', type = %s." % (
                        type(self).__name__, self.name, default_value, type(default_value)
                    )
                raise DSLComponentDefiningError(cause=msg) from e
        self._default = default_value
        self._has_default = True

    def _validate_or_throw(self, value):
        """Validate input parameter value, throw exception if not as expected.

        It will throw exception if validate failed, otherwise do nothing.
        """
        if not self.optional and value is None:
            raise ValueError("Parameter %s cannot be None since it is not optional." % self.name)
        if self._allowed_types and value is not None:
            if not isinstance(value, self._allowed_types):
                raise TypeError(
                    "Unexpected data type for parameter '%s'. Expected %s but got %s." % (
                        self.name, self._allowed_types, type(value)
                    )
                )

    def _to_python_code(self):
        """Return the representation of this parameter in annotation code, used in code generation."""
        parameters = []
        if self._optional:
            parameters.append('optional={}'.format(self._optional))
        if self._description is not None:
            parameters.append('description={!r}'.format(self._description))
        if self._min is not None:
            parameters.append('min={}'.format(self._min))
        if self._max is not None:
            parameters.append('max={}'.format(self._max))
        if self._is_control is not None:
            parameters.append('is_control={}'.format(self._is_control))

        return "{type_name}({parameters})".format(
            type_name=self.__class__.__name__, parameters=', '.join(parameters))


class String(_Param):
    """String parameter passed the parameter string with its raw value."""

    DATA_TYPE = str
    TYPE_NAME = 'string'

    def __init__(
            self,
            description=None,
            optional=None,
            is_control=None,
    ):
        """Initialize a string parameter.

        :param description: Description of the param.
        :type description: str
        :param optional: If the param is optional.
        :type optional: bool
        :param is_control: Determine the String is control or not.
        :type is_control: bool
        """
        _Param.__init__(
            self,
            description=description,
            optional=optional,
            is_control=is_control,
        )


class _Numeric(_Param):
    """Numeric Parameter is an intermediate type which is used to validate the value according to min/max."""

    def _validate_or_throw(self, val):
        super()._validate_or_throw(val)
        if self._min is not None and val < self._min:
            raise ValueError("Parameter '%s' should not be less than %s." % (self.name, self._min))
        if self._max is not None and val > self._max:
            raise ValueError("Parameter '%s' should not be greater than %s." % (self.name, self._max))


class Integer(_Numeric):
    """Int Parameter parse the value to a int value."""

    DATA_TYPE = int
    TYPE_NAME = 'integer'

    def __init__(
            self,
            min=None,
            max=None,
            description=None,
            optional=None,
            is_control=None,
    ):
        """Initialize an integer parameter.

        :param min: Minimal value of the param.
        :type min: int
        :param max: Maximum value of the param.
        :type max: int
        :param description: Description of the param.
        :type description: str
        :param optional: If the param is optional.
        :type optional: bool
        :param is_control: Determine the Integer is control or not.
        :type is_control: bool
        """
        _Numeric.__init__(
            self,
            optional=optional,
            description=description,
            min=min,
            max=max,
            is_control=is_control,
        )

    def _parse(self, val) -> int:
        """Parse the integer value from a string value."""
        return int(val)


class Float(_Numeric):
    """Float Parameter parse the value to a float value."""

    DATA_TYPE = float
    TYPE_NAME = 'float'

    def __init__(
            self,
            min=None,
            max=None,
            description=None,
            optional=None,
            is_control=None,
    ):
        """Initialize a float parameter.

        :param min: Minimal value of the param.
        :type min: float
        :param max: Maximum value of the param.
        :type max: float
        :param description: Description of the param.
        :type description: str
        :param optional: If the param is optional.
        :type optional: bool
        :param is_control: Determine the Float is control or not.
        :type is_control: bool
        """
        _Numeric.__init__(
            self,
            optional=optional,
            description=description,
            min=min,
            max=max,
            is_control=is_control,
        )

    def _parse(self, val) -> float:
        """Parse the float value from a string value."""
        return float(val)

    def _update_default(self, default_value):
        """Update the default value of a float parameter, note that values such as nan/inf is not allowed."""
        if isinstance(default_value, float) and not math.isfinite(default_value):
            # Since nan/inf cannot be stored in the backend, just ignore them.
            _get_logger().warning("Float default value %r is not allowed, ignored." % default_value)
            return
        return super()._update_default(default_value)


class Boolean(_Param):
    """Bool Parameter parse the value to a bool value."""

    DATA_TYPE = bool
    TYPE_NAME = 'boolean'

    def __init__(
            self,
            description=None,
            optional=None,
            is_control=None,
    ):
        """Initialize a bool parameter.

        :param description: Description of the param.
        :type description: str
        :param optional: If the param is optional.
        :type optional: bool
        :param is_control: Determine the Boolean is control or not.
        :type is_control: bool
        """
        _Param.__init__(
            self,
            name=None,
            optional=optional,
            description=description,
            is_control=is_control,
        )

    def _parse(self, val) -> bool:
        """Parse the bool value from a string value."""
        lower_val = str(val).lower()
        if lower_val not in {'true', 'false'}:
            raise ValueError("Boolean parameter '%s' only accept True/False, got %s." % (self.name, val))
        return True if lower_val == 'true' else False


class Enum(_Param):
    """Enum parameter parse the value according to its enum values."""

    TYPE_NAME = 'enum'

    def __init__(
            self,
            enum: Union[EnumMeta, Sequence[str]] = None,
            description=None,
            optional=None,
    ):
        """Initialize an enum parameter, the options of an enum parameter are the enum values.

        :param enum: Enum values.
        :type Union[EnumMeta, Sequence[str]]
        :param description: Description of the param.
        :type description: str
        :param optional: If the param is optional.
        :type optional: bool
        """
        enum_values = self._assert_enum_valid(enum)
        # This is used to parse enum class instead of enum str value if a enum class is provided.
        if isinstance(enum, EnumMeta):
            self._enum_class = enum
            self._str2enum = {v: e for v, e in zip(enum_values, enum)}
        else:
            self._enum_class = None
            self._str2enum = {v: v for v in enum_values}
        super().__init__(
            name=None,
            optional=optional,
            description=description,
            enum=enum_values,
        )
        self._allowed_types = (str,) if not self._enum_class else (self._enum_class, str,)

    @classmethod
    def _assert_enum_valid(cls, enum):
        """Check whether the enum is valid and return the values of the enum."""
        if isinstance(enum, EnumMeta):
            enum_values = [str(option.value) for option in enum]
        elif isinstance(enum, Iterable):
            enum_values = list(enum)
        else:
            raise ValueError("enum must be a subclass of Enum or an iterable.")

        if len(enum_values) <= 0:
            raise ValueError("enum must have enum values.")

        if any(not isinstance(v, str) for v in enum_values):
            raise ValueError("enum values must be str type.")

        return enum_values

    def _parse(self, str_val: str):
        """Parse the enum value from a string value or the enum value."""
        if str_val is None:
            return str_val

        if self._enum_class and isinstance(str_val, self._enum_class):
            return str_val  # Directly return the enum value if it is the enum.

        if str_val not in self._str2enum:
            raise ValueError("Not a valid enum value: '%s', valid values: %s" % (str_val, ', '.join(self.enum)))
        return self._str2enum[str_val]

    def _update_default(self, default_value):
        """Enum parameter support updating values with a string value."""
        enum_val = self._parse(default_value)
        if self._enum_class and isinstance(enum_val, self._enum_class):
            enum_val = enum_val.value
        self._default = enum_val
        self._has_default = True


# Attribute on customer group class to mark a value type is parameter group.
_GROUP_ATTR_NAME = '__parameter_group__'


def _parameter_group(_cls):
    """
    Parameter group decorator to make user-defined class as a parameter group.

    Usage:
        Group a set of component parameters make component configuration easier.

        e.g. Define a parameter group

        .. code-block:: python

            # define a parameter group
            @dsl.parameter_group
            class ParamClass:
                str_param: str
                int_param: int = 1

            # see the help of auto-gen __init__ function
            help(ParamClass.__init__)

        e.g. Define a multi-level parameter group

        .. code-block:: python

            # define a sub parameter group
            @dsl.parameter_group
            class SubGroupClass:
                str_param: str
                int_param: int = 1

            @dsl.parameter_group
            class ParentClass:
                param_group1: SubGroupClass
                param_group2: SubGroupClass = SubGroupClass('test')  # declare a sub group field with default

            # see the help of auto-gen __init__ function
            help(ParentClass.__init__)

        e.g. Link and assign Parameter Group

        .. code-block:: python

            # create a sub group value
            my_param_group = SubGroupClass(dataset, int_param=2)

            # create a parent group value
            my_parent_group = ParentClass(param_group1=my_param_group)

            # option 1. use annotation to declare the parameter is a parameter group.
            @dsl.pipeline()
            def pipeline_func(params: SubGroupClass):
                component = component_func(string_parameter=params.str_param,
                                           int_parameter=params.int_param)
                return component.outputs
            # create a pipeline instance
            pipeline = pipeline_func(my_param_group)

            # option 2. use default of parameter to declare itself a parameter group.
            @dsl.pipeline()
            def pipeline_func(params=my_param_group):
                component = component_func(string_parameter=params.str_param,
                                           int_parameter=params.int_param)
                return component.outputs
            # create a pipeline instance
            pipeline = pipeline_func()

            # use multi-level parameter group in pipeline.
            @dsl.pipeline()
            def parent_func(params: ParentClass):
                # pass sub group to sub pipeline.
                pipeline = pipeline_func(params.param_group1)
                return pipeline.outputs

    Supported Types:
        * For int, str, float, bool
            * Declare with python type annotation: `param: int`
            * Declare with dsl type annotation: `param: Integer` or `param: Integer(min=1, max=5)`

        * For Enum
            * Declare with user-defined enum class annotation: `param: MyEnumClass`
            * Declare with complete dsl type annotation: `param: Enum(enum=MyEnumClass)`

        * For sub group class
            * Sub group class should be decorated with `dsl.parameter_group`
            * Default value with sub group type will be presented as dict for readability

    Restrictions:
        * Each group member's name must be public (not start with '_').
        * Each group member **MUST** have annotation to keep their original defined order.
        * Customer class definition should follow 'Non-default argument follows default argument' rule.
        * If use parameter group as a pipeline parameter, user **MUST** write the type annotation
          or give it a non-None default value to infer the parameter group class.

    """
    def _create_fn(name, args, body, *, globals=None, locals=None,
                   return_type):
        """To generate function in class."""
        # Reference: Source code of dataclasses.dataclass
        # Doc link: https://docs.python.org/3/library/dataclasses.html
        # Reference code link:
        # https://github.com/python/cpython/blob/17b16e13bb444001534ed6fccb459084596c8bcf/Lib/dataclasses.py#L412
        # Note that we mutate locals when exec() is called
        if locals is None:
            locals = {}
        if 'BUILTINS' not in locals:
            import builtins
            locals['BUILTINS'] = builtins
        locals['_return_type'] = return_type
        return_annotation = '->_return_type'
        args = ','.join(args)
        body = '\n'.join(f'  {b}' for b in body)
        # Compute the text of the entire function.
        txt = f' def {name}({args}){return_annotation}:\n{body}'
        local_vars = ', '.join(locals.keys())
        txt = f"def __create_fn__({local_vars}):\n{txt}\n return {name}"
        ns = {}
        exec(txt, globals, ns)
        return ns['__create_fn__'](**locals)

    def _create_init_fn(cls, fields):
        """Generate the __init__ function for user-defined class."""
        # Reference code link:
        # https://github.com/python/cpython/blob/17b16e13bb444001534ed6fccb459084596c8bcf/Lib/dataclasses.py#L523
        def _get_data_type_from_annotation(anno):
            # Get Input(min, max) object class Input
            if isinstance(anno, EnumMeta):
                return anno
            k_type = anno if type(anno) is type else type(anno)
            # Get data type if annotation is dsl.types, special logic for Enum
            if k_type is Enum:
                return anno._enum_class if anno._enum_class else str
            return k_type.DATA_TYPE if issubclass(k_type, _Param) else k_type

        init_func_annotation = {}
        for k, v in getattr(cls, '__annotations__', {}).items():
            init_func_annotation[k] = _get_data_type_from_annotation(v)
        locals = {f'_type_{key}': init_func_annotation[key] for key, val in fields.items()}
        # Collect field defaults if val is parameter and is optional
        default_keys = set({key for key, val in fields.items() if val._has_default})
        defaults = {f'_dlft_{key}': fields[key].default for key in default_keys}
        locals.update(defaults)
        _init_param = ['self']
        for key in fields:
            param = f'{key}:_type_{key}=_dlft_{key}' if key in default_keys else f'{key}:_type_{key}'
            _init_param.append(param)
        body_lines = [f'self.{key}={key}' for key in fields]
        # If no body lines, use 'pass'.
        if not body_lines:
            body_lines = ['pass']
        return _create_fn('__init__', _init_param, body_lines, locals=locals, return_type=None)

    def _create_repr_fn(fields):
        """Generate the __repr__ function for user-defined class."""
        # Reference code link:
        # https://github.com/python/cpython/blob/17b16e13bb444001534ed6fccb459084596c8bcf/Lib/dataclasses.py#L582
        fn = _create_fn('__repr__', ('self',),
                        ['return self.__class__.__qualname__ + f"(' +
                         ', '.join([f"{k}={{self.{k}!r}}" for k in fields]) + ')"'], return_type=str)

        # This function's logic is copied from "recursive_repr" function in
        # reprlib module to avoid dependency.
        def _recursive_repr(user_function):
            # Decorator to make a repr function return "..." for a recursive
            # call.
            repr_running = set()

            @functools.wraps(user_function)
            def wrapper(self):
                key = id(self), _thread.get_ident()
                if key in repr_running:
                    return '...'
                repr_running.add(key)
                try:
                    result = user_function(self)
                finally:
                    repr_running.discard(key)
                return result
            return wrapper
        return _recursive_repr(fn)

    def _process_class(cls, all_fields):
        """Generate some functions into class."""
        setattr(cls, '__init__', _create_init_fn(cls, all_fields))
        setattr(cls, '__repr__', _create_repr_fn(all_fields))
        return cls

    def _wrap(cls):
        all_fields = _get_param_with_standard_annotation(cls)
        # Set group info on cls
        setattr(cls, _GROUP_ATTR_NAME, _Group(all_fields))
        # Add init, repr, eq to class with user-defined annotation type
        return _process_class(cls, all_fields)

    return _wrap(_cls)


def is_parameter_group(obj):
    """Return True if obj is a parameter group or an instance of a parameter group class."""
    return hasattr(obj, _GROUP_ATTR_NAME)


class _Group(_Param):
    """Group type to record the values in user defined parameter group class."""

    TYPE_NAME = 'group'

    def __init__(self, values: dict):
        super().__init__()
        self.assert_group_value_valid(values)
        self.values = values
        # Create empty default by values
        # Note Output do not have default so just set a None
        self._default = _GroupAttrDict({
            k: v._default if hasattr(v, '_default') else None for k, v in self.values.items()})
        # Only when user specify group = MyGroup(), has default is True
        self._has_default = False

    @classmethod
    def assert_group_value_valid(cls, values):
        """Check if all value in group is _Param type with unique name."""
        names = set()
        for key, value in values.items():
            if not _is_dsl_types(value):
                raise ValueError(f'Unsupported type {value} in parameter group.')
            if isinstance(value, (Input, Output)):
                raise UserErrorException(
                    f'Parameter {value.name!r} with type {type(value)} is not supported in parameter group.')
            if key in names:
                raise ValueError(f'Duplicate parameter name {value.name!r} found in Group values.')
            names.add(key)

    def flatten(self, group_parameter_name):
        """Flatten and return all parameters."""
        all_parameters = {}
        group_parameter_name = group_parameter_name if group_parameter_name else ''
        for key, value in self.values.items():
            flattened_name = '_'.join([group_parameter_name, key])
            if isinstance(value, _Group):
                all_parameters.update(value.flatten(flattened_name))
            else:
                all_parameters[flattened_name] = value
        return all_parameters

    def _to_dict(self, remove_name=True) -> dict:
        attr_dict = super()._to_dict(remove_name)
        attr_dict['values'] = {k: v._to_dict() for k, v in self.values.items()}
        return attr_dict

    @staticmethod
    def _customer_class_value_to_attr_dict(value):
        if not is_parameter_group(value):
            return value
        attr_dict = {}
        for k, v in value.__dict__.items():
            if is_parameter_group(v):
                attr_dict[k] = _Group._customer_class_value_to_attr_dict(v)
            elif isinstance(v, PyEnum):
                attr_dict[k] = v.value
            else:
                attr_dict[k] = v
        return _GroupAttrDict(attr_dict)

    def _update_default(self, default_value=None):
        default_cls = type(default_value)
        # Assert '__parameter_group__' must in the class of default value
        if default_cls == _GroupAttrDict:
            self._default = default_value
            self._optional = False
            self._has_default = True
            return
        if default_value and not is_parameter_group(default_cls):
            raise ValueError(f'Default value must be instance of parameter group, got {default_cls}')
        if hasattr(default_value, '__dict__'):
            # Convert default value with customer type to _AttrDict
            self._default = _Group._customer_class_value_to_attr_dict(default_value)
            # Update item annotation
            for key, annotation in self.values.items():
                if not hasattr(default_value, key):
                    continue
                annotation._update_default(getattr(default_value, key))
        self._optional = default_value is None
        self._has_default = True


class _GroupAttrDict(_AttrDict):
    """This class is used to standardized user-defined group type values."""

    def __init__(self, dct):
        super().__init__(dct)

    def _flatten(self, group_parameter_name):
        # Return the flatten result of self
        group_parameter_name = group_parameter_name if group_parameter_name else ''
        flattened_parameters = {}
        for k, v in self.items():
            flattened_name = '_'.join([group_parameter_name, k])
            if isinstance(v, _GroupAttrDict):
                flattened_parameters.update(v._flatten(flattened_name))
            else:
                flattened_parameters[flattened_name] = v
        return flattened_parameters

    def _set_annotation(self, annotation: _Group):
        """Set annotation for all pipeline parameters inside group."""
        for k, v in self.items():
            if k not in annotation.values.keys():
                continue
            v_annotation = annotation.values[k]
            if isinstance(v, _GroupAttrDict):
                if isinstance(v_annotation, _Group):
                    v._set_annotation(v_annotation)
            else:
                v._annotation = v_annotation


_DATA_TYPE_MAPPING = {
    v.DATA_TYPE: v
    for v in globals().values() if isinstance(v, type) and issubclass(v, _Param) and v.DATA_TYPE
}

_DATA_TYPE_NAME_MAPPING = {
    **{
        v.DATA_TYPE.__name__: v
        for v in globals().values() if isinstance(v, type) and issubclass(v, _Param) and v.DATA_TYPE
    },
    **{
        v.__name__: v
        for v in globals().values() if isinstance(v, type) and issubclass(v, _Param) and v.DATA_TYPE
    }
}


def _get_annotation_by_value(val):
    def _is_dataset(data):
        from azureml.core import Dataset
        from azureml.data.data_reference import DataReference
        from azureml.data.datapath import DataPath
        from azureml.data.abstract_dataset import AbstractDataset
        from azureml.data.dataset_consumption_config import DatasetConsumptionConfig
        DATASET_TYPES = (Dataset, DataReference, DataPath, AbstractDataset, DatasetConsumptionConfig)
        return isinstance(data, DATASET_TYPES)

    if _is_dataset(val):
        annotation = Input
    elif val is Parameter.empty or val is None:
        # If no default value or default is None, create val as the basic parameter type,
        # it could be replaced using component parameter definition.
        annotation = _Param
    elif isinstance(val, PyEnum):
        # Handle enum values
        annotation = Enum(enum=val.__class__)
        annotation._auto_gen = True
    elif is_parameter_group(val):
        return copy.deepcopy(getattr(val, _GROUP_ATTR_NAME))
    else:
        annotation = _get_annotation_cls_by_type(type(val), raise_error=False)
        if not annotation:
            # Fall back to _Param
            annotation = _Param
    return annotation


def _get_annotation_cls_by_type(t: type, raise_error=False):
    cls = _DATA_TYPE_MAPPING.get(t)
    if cls is None and raise_error:
        raise UserErrorException(f"Can't convert type {t} to dsl.types")
    return cls


def _get_annotation_cls_by_type_name(type_name: str, raise_error=False):
    cls = _DATA_TYPE_NAME_MAPPING.get(type_name)
    if cls is None and raise_error:
        raise UserErrorException(f"Can't find type name {type_name!r} in dsl.types")
    return cls


def _get_param_with_standard_annotation(
        cls_or_func, is_func=False, non_pipeline_parameter_names=None,
        dynamic_param_name=None, dynamic_param_value=None):
    """Standardize function parameters or class fields with dsl.types annotation."""
    non_pipeline_parameter_names = non_pipeline_parameter_names or []

    def _get_fields(annotations):
        """Return field names to annotations mapping in class."""
        annotation_fields = OrderedDict()
        for name, annotation in annotations.items():
            # Skip return type
            if name == 'return':
                continue
            # Handle EnumMeta annotation
            if isinstance(annotation, EnumMeta):
                annotation = Enum(enum=annotation)
                annotation._auto_gen = True
            # Try create annotation by type when got like 'param: int'
            annotation = copy.deepcopy(getattr(annotation, _GROUP_ATTR_NAME))\
                if is_parameter_group(annotation) else annotation
            if not _is_dsl_type_cls(annotation) and not _is_dsl_types(annotation):
                annotation = _get_annotation_cls_by_type(annotation, raise_error=False)
                if not annotation:
                    # Fall back to _Param
                    annotation = _Param
            annotation_fields[name] = annotation
        return annotation_fields

    def _merge_field_keys(annotation_fields, defaults_dict):
        """Merge field keys from annotations and cls dict to get all fields in class."""
        anno_keys = list(annotation_fields.keys())
        dict_keys = defaults_dict.keys()
        if not dict_keys:
            return anno_keys
        # Fields with default values must follow those without defaults, so find the first key with
        # annotation that appear in the class dict, the previous keys must be in the front of the key list
        all_keys = []
        # Use this flag to guarantee all fields with defaults following fields without defaults.
        seen_default = False
        for key in anno_keys:
            if key in dict_keys:
                seen_default = True
            else:
                if seen_default:
                    raise UserErrorException(f'Non-default argument {key!r} follows default argument.')
                all_keys.append(key)
        # Append all keys in dict
        all_keys.extend(dict_keys)
        return all_keys

    def _update_annotation_with_default(anno, name, default):
        """Create annotation if is type class and update the default."""
        # Create instance if is type class
        complete_annotation = anno
        if _is_dsl_type_cls(anno):
            complete_annotation = anno()
            complete_annotation._auto_gen = True
        complete_annotation._name = name
        if default is _Param.EMPTY:
            return complete_annotation
        if isinstance(complete_annotation, (_Param, Input)):
            complete_annotation._update_default(default)
        return complete_annotation

    def _update_fields_with_default(annotation_fields, defaults_dict):
        """Use public values in class dict to update annotations."""
        all_fields = OrderedDict()
        all_filed_keys = _merge_field_keys(annotation_fields, defaults_dict)
        for name in all_filed_keys:
            # Get or create annotation
            annotation = annotation_fields[name] if name in annotation_fields \
                else _get_annotation_by_value(defaults_dict.get(name, _Param.EMPTY))
            # Create annotation if is class type and update default
            annotation = _update_annotation_with_default(
                annotation, name, defaults_dict.get(name, _Param.EMPTY))
            all_fields[name] = annotation
        return all_fields

    def _filter_pipeline_parameters(dct):
        """Filter out non pipeline parameters and dynamic parameter key."""
        return {k: v for k, v in dct.items() if k not in non_pipeline_parameter_names and k != dynamic_param_name}

    def _get_dynamic_parameters_annotation(values_dict):
        """Get annotations for value in **kwargs."""
        values_annotation = {
            key: _get_annotation_by_value(_get_parameter_static_value(val)) for key, val in values_dict.items()
        }
        # Note: here we do not set the args value as default because it could be dataset then cause some problem.
        # And we will keep the `None` value as default in case user would like to specify optional parameter in dict.
        values_annotation = {
            key: _update_annotation_with_default(
                anno, key, default=_Param.EMPTY if values_dict[key] is not None else None)
            for key, anno in values_annotation.items()}
        return values_annotation

    # From annotations get field with type
    annotations = _filter_pipeline_parameters(getattr(cls_or_func, '__annotations__', {}))
    annotation_fields = _get_fields(annotations)
    # Flatten and add dynamic parameter with annotation
    if dynamic_param_name:
        annotation_fields.update(_get_dynamic_parameters_annotation(dynamic_param_value))
    # Update fields use class field with defaults from class dict or signuration(func).paramters
    if not is_func:
        # Only consider public fields in class dict
        defaults_dict = {key: val for key, val in cls_or_func.__dict__.items() if not key.startswith('_')}
        defaults_dict = _filter_pipeline_parameters(defaults_dict)
        # Restrict each field must have annotation(in annotation dict)
        if any(key not in annotation_fields for key in defaults_dict):
            raise UserErrorException(f'Each field in parameter group {cls_or_func!r} must have an annotation.')
    else:
        # Infer parameter type from value if is function
        defaults_dict = {key: val.default for key, val in signature(cls_or_func).parameters.items()}
        defaults_dict = _filter_pipeline_parameters(defaults_dict)
        # add default value for dynamic parameters
        if dynamic_param_value is not None:
            defaults_dict.update(dynamic_param_value)
    all_fields = _update_fields_with_default(annotation_fields, defaults_dict)
    return all_fields


def _is_dsl_type_cls(t: type):
    if type(t) is not type:
        return False
    # param: Integer
    return issubclass(t, (_Param, Input, Output))


def _is_dsl_types(o: object):
    # param: Integer(min=1, max=5)
    return _is_dsl_type_cls(type(o))


def _remove_empty_values(data, ignore_keys=None):
    if not isinstance(data, dict):
        return data
    ignore_keys = ignore_keys or {}
    return {k: v if k in ignore_keys else _remove_empty_values(v)
            for k, v in data.items() if v is not None or k in ignore_keys}


def _get_annotation_type_str(annotation: Union[_Param, Input]) -> str:
    if isinstance(annotation, Input):
        # return python type name if is primitive type, else return as input
        return _Param.parse_param_type_string(annotation.type)\
            if annotation._is_primitive_type else "input"
    elif isinstance(annotation, Enum):
        return str.__name__
    else:
        return annotation.DATA_TYPE.__name__
