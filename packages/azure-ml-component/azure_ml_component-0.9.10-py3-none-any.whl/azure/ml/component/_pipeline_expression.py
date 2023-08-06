# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import inspect
import os
import shutil
import tempfile
import time
from copy import deepcopy

from azure.ml.component._core._types import _DATA_TYPE_NAME_MAPPING, _Param
from azure.ml.component._util._exceptions import UnsupportedError
from azure.ml.component._util._loggerfactory import _LoggerFactory

_logger = None


def _get_logger():
    global _logger
    if _logger is not None:
        return _logger
    _logger = _LoggerFactory.get_logger()
    return _logger


class OperableMixin:
    SUPPORTED_CONST_TYPES = (bool, int, float, str)

    def __hash__(self):
        return id(self)

    def _validate_operation(self, other, operator, allow_none=False):
        from azure.ml.component._pipeline_parameters import PipelineParameter
        from azure.ml.component.component import Output
        if other is None and not allow_none:
            msg = f"Not support operation '{operator}' with None."
            raise UnsupportedError(msg)
        if not isinstance(other, self.SUPPORTED_CONST_TYPES) and \
                not isinstance(other, (PipelineParameter, PipelineExpression, Output)):
            msg = f"Not support operation '{operator}' with {type(other)}; " \
                  f"only support operation between constant, PipelineParameter, PipelineExpression and Output."
            raise UnsupportedError(msg)

    def __add__(self, other):
        self._validate_operation(other, '+')
        return PipelineExpression._from_python_expression(self, other, '+')

    def __radd__(self, other):
        self._validate_operation(other, '+')
        return PipelineExpression._from_python_expression(other, self, '+')

    def __sub__(self, other):
        self._validate_operation(other, '-')
        return PipelineExpression._from_python_expression(self, other, '-')

    def __rsub__(self, other):
        self._validate_operation(other, '-')
        return PipelineExpression._from_python_expression(other, self, '-')

    def __mul__(self, other):
        self._validate_operation(other, '*')
        return PipelineExpression._from_python_expression(self, other, '*')

    def __rmul__(self, other):
        self._validate_operation(other, '*')
        return PipelineExpression._from_python_expression(other, self, '*')

    def __truediv__(self, other):
        self._validate_operation(other, '/')
        return PipelineExpression._from_python_expression(self, other, '/')

    def __rtruediv__(self, other):
        self._validate_operation(other, '/')
        return PipelineExpression._from_python_expression(other, self, '/')

    def __mod__(self, other):
        self._validate_operation(other, '%')
        return PipelineExpression._from_python_expression(self, other, '%')

    def __rmod__(self, other):
        self._validate_operation(other, '%')
        return PipelineExpression._from_python_expression(other, self, '%')

    def __pow__(self, other):
        self._validate_operation(other, '**')
        return PipelineExpression._from_python_expression(self, other, '**')

    def __rpow__(self, other):
        self._validate_operation(other, '**')
        return PipelineExpression._from_python_expression(other, self, '**')

    def __floordiv__(self, other):
        self._validate_operation(other, '//')
        return PipelineExpression._from_python_expression(self, other, '//')

    def __rfloordiv__(self, other):
        self._validate_operation(other, '//')
        return PipelineExpression._from_python_expression(other, self, '//')

    def __lt__(self, other):
        self._validate_operation(other, '<')
        return PipelineExpression._from_python_expression(self, other, '<')

    def __gt__(self, other):
        self._validate_operation(other, '>')
        return PipelineExpression._from_python_expression(self, other, '>')

    def __le__(self, other):
        self._validate_operation(other, '<=')
        return PipelineExpression._from_python_expression(self, other, '<=')

    def __ge__(self, other):
        self._validate_operation(other, '>=')
        return PipelineExpression._from_python_expression(self, other, '>=')

    def __eq__(self, other):
        self._validate_operation(other, '==', allow_none=True)
        return PipelineExpression._from_python_expression(self, other, '==')

    def __ne__(self, other):
        self._validate_operation(other, '!=', allow_none=True)
        return PipelineExpression._from_python_expression(self, other, '!=')

    def __bool__(self):
        """Python method, called to implement truth value testing and the built-in operation bool().

        This method is not supported. OperableMixin is designed to record operation history,
        while __bool__ only return False or True, leading to lineage breaks here. As overloadable
        boolean operators PEP (refer to: https://www.python.org/dev/peps/pep-0335/) was rejected,
        logical operations are also not supported here.
        """
        var_name = 'variable'
        if isinstance(self, PipelineExpression):
            var_name = self.expression  # show expression for PipelineExpression
        elif hasattr(self, '_name'):
            var_name = self._name
        elif hasattr(self, 'name'):
            var_name = self.name
        _get_logger().warning(f'Operation bool() is unsupported for {var_name!r} with type {type(self)}.')
        return True

    def __and__(self, other):
        self._validate_operation(other, '&')
        return PipelineExpression._from_python_expression(self, other, '&')

    def __or__(self, other):
        self._validate_operation(other, '|')
        return PipelineExpression._from_python_expression(self, other, '|')

    def __xor__(self, other):
        self._validate_operation(other, '^')
        return PipelineExpression._from_python_expression(self, other, '^')


class PipelineExpression(OperableMixin):
    # python built-in types
    TYPE_BOOLEAN = bool.__name__
    TYPE_INTEGER = int.__name__
    TYPE_FLOAT = float.__name__
    TYPE_STRING = str.__name__
    # type for operator
    TYPE_OPERATOR = 'operator'
    # supported operators
    SUPPORTED_NUMERICAL_OPERATORS = ('+', '-', '*', '/', '%', '**', '//')
    SUPPORTED_COMPARISON_OPERATORS = ('<', '>', '<=', '>=', '==', '!=')
    SUPPORTED_BITWISE_OPERATORS = ('&', '|', '^')
    SUPPORTED_OPERATORS = SUPPORTED_NUMERICAL_OPERATORS + SUPPORTED_COMPARISON_OPERATORS + SUPPORTED_BITWISE_OPERATORS
    # operator priority for infix to postfix
    SUPPORTED_OPERATORS_PRIORITY = {'+': 4, '-': 4, '*': 5, '/': 5, '%': 5, '**': 6, '//': 5,
                                    '<': 0, '>': 0, '<=': 0, '>=': 0, '==': 0, '!=': 0,
                                    '&': 3, '|': 1, '^': 2}
    # templates for dynamically generating components
    DEFAULT_RETURN_TYPE_FROM_PYTHON_EXPRESSION = 'Any'  # not important, will infer when evaluate
    IMPORT_DSL_LINE = 'from azure.ml.component import dsl'
    IMPORT_DSL_TYPES_LINE = 'from azure.ml.component.dsl.types import Input, Output, @@component_return_type@@\n\n'
    DSL_DECORATOR_LINE = \
        '@dsl.command_component(display_name="Expression: @@infix_notation@@", ' \
        'version="@@expression_version@@", environment={"name": "AzureML-Component"})'
    COMPONENT_FUNC_NAME = 'expression_generated_component'
    COMPONENT_FUNC_DECLARATION_LINE = f'def {COMPONENT_FUNC_NAME}(@@component_parameters@@)' \
                                      f' -> Output(type=@@component_return_type@@.TYPE_NAME, is_control=True):'
    # __pycache__ folder constant
    PYCACHE_FOLDER_NAME = '__pycache__'

    def __init__(self, expression, inputs, return_type):
        """Define an expression in a pipeline execution.

        Use PipelineExpression to support simple and trivial parameter transformations tasks.
        Expression will be saved after several process, which can be recovered if needed.

        :param expression: Expression doing trivial parameter transformations tasks, in the form of infix notation.
        :type expression: str
        :param inputs: Dictionary of PipelineParameters, PipelineExpressions and Outputs appeared in expression.
        :type inputs: dict
        :param return_type:
        :type return_type: Union[str, type]
        """
        self._created_component = None  # cache for created component
        self._expression = expression  # infix notation
        self._return_type = return_type
        self._inputs = inputs.copy()

    @staticmethod
    def _infix_to_postfix(infix):
        """Convert infix notation (a string) to postfix notation (a list)."""
        postfix = []
        stack = []
        priority = PipelineExpression.SUPPORTED_OPERATORS_PRIORITY
        i = 0
        while i < len(infix):
            if infix[i] == ' ':
                i += 1
            if infix[i] == '(':
                stack.append('(')
                i += 1
            elif infix[i] == ')':
                while stack and stack[-1] != '(':
                    postfix.append(stack.pop())
                stack.pop()
                i += 1
            else:
                j = i
                while j < len(infix) and infix[j] != ' ' and infix[j] != ')':
                    j += 1
                token = infix[i:j]
                if token not in PipelineExpression.SUPPORTED_OPERATORS:
                    postfix.append(token)
                else:
                    while stack and stack[-1] != '(' and priority[token] <= priority[stack[-1]]:
                        postfix.append(token)
                    stack.append(token)
                i = j
        while stack:
            postfix.append(stack.pop())
        return postfix

    @staticmethod
    def _postfix_to_infix(postfix):
        """Convert postfix notation (a list) to infix notation (a string)."""
        stack = list()
        for token in postfix:
            if token not in PipelineExpression.SUPPORTED_OPERATORS:
                stack.append(token)
                continue
            operand2, operand1 = stack.pop(), stack.pop()
            stack.append(f'({operand1} {token} {operand2})')
        return stack.pop()

    @staticmethod
    def _process_operand_in_python_expression(rpn, operand, inputs):
        from azure.ml.component._pipeline_parameters import PipelineParameter
        from azure.ml.component.component import Output

        def _update_rpn(_rpn, _old, _new):
            return [_new if _token == _old else _token for _token in _rpn]

        def _get_or_create_input_name(_inputs, _input, _original_name):
            _existing_id_to_name = {id(_v): _k for _k, _v in _inputs.items()}
            if id(_input) in _existing_id_to_name:
                return _existing_id_to_name[id(_input)]
            _name, _counter = _original_name, 0
            while _name in _inputs:
                _name, _counter = f'{_original_name}_{_counter}', _counter + 1
            return _name

        def _process_pipeline_parameter(_rpn, _pipeline_parameter, _inputs):
            _name = _pipeline_parameter.name
            if _pipeline_parameter._user_annotation is None:
                raise UnsupportedError(f"PipelineParameter '{_name}' is not annotated with type.")
            if _pipeline_parameter._user_annotation not in _Param._PARAM_TYPE_STRING_MAPPING:
                raise UnsupportedError(
                    f"PipelineParameter '{_name}' is annotated with "
                    f"unsupported type {_pipeline_parameter._user_annotation}.")
            if _name in _inputs:
                _previous_input = _inputs[_name]
                if isinstance(_previous_input, PipelineParameter):
                    # if previous parameter is PipelineParameter, update name with counter
                    _name = _get_or_create_input_name(_inputs, _pipeline_parameter, _name)
                else:
                    # if previous parameter is Output, update by adding component's name as prefix
                    _inputs.pop(_name)
                    _new_name = f'{_previous_input._owner._definition.name}__{_previous_input.port_name}'
                    _rpn = _update_rpn(_rpn, _name, _new_name)
                    _inputs[_new_name] = _previous_input
            _rpn.append(_name)
            _inputs[_name] = _pipeline_parameter
            return _rpn, _inputs

        def _process_component_output(_rpn, _component_output, _inputs):
            output_definition = _component_output._owner._definition.outputs.get(_component_output._name)
            if not output_definition.is_control:
                raise UnsupportedError(
                    f"Output {_component_output._name!r} in PipelineExpression must have "
                    f"'is_control' filed with value 'True', got {output_definition.is_control}")
            component_output_type = output_definition._type
            if component_output_type not in _Param._PARAM_TYPE_STRING_MAPPING:
                raise UnsupportedError(
                    f"Output '{_component_output._name}' is annotated with "
                    f"unsupported type {component_output_type}.")
            # default name is component port name and its flag
            _name, _has_prefix = _component_output.port_name, False
            # if default name is 'output', add component's name as prefix to avoid same name with current output
            if _name == 'output':
                _name, _has_prefix = f'{_component_output._owner._definition.name}__{_name}', True
            while _name in _inputs:
                # this loop is expected to be run at most twice
                _previous_input = _inputs[_name]
                if isinstance(_previous_input, PipelineParameter):
                    # previous parameter is PipelineParameter,
                    #   first time try using name with component's name prefix
                    #   second time update name with counter
                    if not _has_prefix:
                        _name = f'{_component_output._owner._definition.name}__{_component_output.port_name}'
                        _has_prefix = True
                        continue
                    _name = _get_or_create_input_name(_inputs, _component_output, _name)
                    break
                else:
                    # previous parameter is Output,
                    #   first time try using name with component's name prefix for both duplications
                    #   second time update name with counter
                    if not _has_prefix:
                        _inputs.pop(_name)
                        _new_name = f'{_previous_input._owner._definition.name}__{_previous_input.port_name}'
                        _rpn = _update_rpn(_rpn, _name, _new_name)
                        _inputs[_new_name] = _previous_input
                        _name = f'{_component_output._owner._definition.name}__{_component_output.port_name}'
                        _has_prefix = True
                        continue
                    _name = _get_or_create_input_name(_inputs, _component_output, _name)
                    break
            _rpn.append(_name)
            _inputs[_name] = _component_output
            return _rpn, _inputs

        if isinstance(operand, PipelineParameter):
            rpn, inputs = _process_pipeline_parameter(rpn, operand, inputs)
        elif isinstance(operand, Output):
            rpn, inputs = _process_component_output(rpn, operand, inputs)
        elif isinstance(operand, PipelineExpression):
            rpn.extend(deepcopy(operand._postfix_notation))
            inputs.update(operand._inputs.copy())
        elif isinstance(operand, PipelineExpression.SUPPORTED_CONST_TYPES) or operand is None:
            rpn.append(repr(operand))
        return rpn, inputs

    @staticmethod
    def _from_python_expression(operand1, operand2, operator):
        """Construct PipelineExpression from python expression.

        :param operand1: First operand of the expression. Valid type includes simple constant
            (currently bool, int, float and str), PipelineParameter and PipelineExpression.
        :type operand1: Union[bool, int, float, str, PipelineParameter, PipelineExpression, Output]
        :param operand2: Second operand of the expression. Same valid type as operand1.
        :type operand2: Union[bool, int, float, str, PipelineParameter, PipelineExpression, Output]
        :param operator: Operator of the expression.
        :type operator: str
        """
        if operator not in PipelineExpression.SUPPORTED_OPERATORS:
            msg = f"'{operator}' is not supported operator for PipelineParameter and PipelineExpression, " \
                  f"currently supported operators include {', '.join(PipelineExpression.SUPPORTED_OPERATORS)}."
            raise UnsupportedError(msg)

        rpn, inputs = list(), dict()
        rpn, inputs = PipelineExpression._process_operand_in_python_expression(rpn, operand1, inputs)
        rpn, inputs = PipelineExpression._process_operand_in_python_expression(rpn, operand2, inputs)
        rpn.append(operator)
        return PipelineExpression(expression=PipelineExpression._postfix_to_infix(rpn), inputs=inputs,
                                  return_type=PipelineExpression.DEFAULT_RETURN_TYPE_FROM_PYTHON_EXPRESSION)

    def __repr__(self):
        return f'PipelineExpression(expression={repr(self._expression)}, ' \
               f'inputs={repr(self._inputs)}, return_type={repr(self._inputs)})'

    @property
    def expression(self):
        return self._expression

    @property
    def _infix_notation(self):
        return self.expression

    @property
    def _postfix_notation(self):
        return self._infix_to_postfix(self._infix_notation)

    @staticmethod
    def _infer_op_res_type(operand1_type, operator, operand2_type):
        def _raise_not_supported_operation_exception():
            msg = f"'{operator}' not supported between instances of '{operand1_type}' and '{operand2_type}'."
            raise UnsupportedError(msg)

        if operator in PipelineExpression.SUPPORTED_NUMERICAL_OPERATORS:
            if operand1_type == PipelineExpression.TYPE_STRING or operand2_type == PipelineExpression.TYPE_STRING:
                if operand1_type == PipelineExpression.TYPE_STRING and \
                        operand2_type == PipelineExpression.TYPE_STRING and operator != '+':
                    _raise_not_supported_operation_exception()
                return PipelineExpression.TYPE_STRING
            if operand1_type == PipelineExpression.TYPE_FLOAT or operand2_type == PipelineExpression.TYPE_FLOAT:
                return PipelineExpression.TYPE_FLOAT
            else:
                return PipelineExpression.TYPE_INTEGER
        if operator in PipelineExpression.SUPPORTED_COMPARISON_OPERATORS:
            if operand1_type == PipelineExpression.TYPE_STRING or operand2_type == PipelineExpression.TYPE_STRING:
                if not (operand1_type == PipelineExpression.TYPE_STRING and
                        operand2_type == PipelineExpression.TYPE_STRING):
                    _raise_not_supported_operation_exception()
            return PipelineExpression.TYPE_BOOLEAN
        if operator in PipelineExpression.SUPPORTED_BITWISE_OPERATORS:
            if operand1_type in (PipelineExpression.TYPE_FLOAT, PipelineExpression.TYPE_STRING) or \
                    operand2_type in (PipelineExpression.TYPE_FLOAT, PipelineExpression.TYPE_STRING):
                _raise_not_supported_operation_exception()
            if operand1_type == PipelineExpression.TYPE_BOOLEAN and operand2_type == PipelineExpression.TYPE_BOOLEAN:
                return PipelineExpression.TYPE_BOOLEAN
            else:
                return PipelineExpression.TYPE_INTEGER

    @staticmethod
    def _to_dsl_type(typ):
        return _DATA_TYPE_NAME_MAPPING[typ].__name__

    @staticmethod
    def _to_python_type(typ):
        return _Param._PARAM_TYPE_STRING_MAPPING[typ].__name__

    def _get_token_type(self, token_name):
        if token_name in self.SUPPORTED_OPERATORS:
            return self.TYPE_OPERATOR
        if token_name not in self._inputs:
            return type(eval(token_name)).__name__
        from azure.ml.component._pipeline_parameters import PipelineParameter
        from azure.ml.component.component import Output
        token = self._inputs[token_name]
        if isinstance(token, PipelineParameter):
            return self._to_python_type(token._user_annotation)
        elif isinstance(token, Output):
            return self._to_python_type(token._owner._definition.outputs.get(token.port_name)._type)
        else:
            msg = f"Unsupported type of input '{token_name}', got type '{type(token)}'."
            raise UnsupportedError(msg)

    @property
    def _component_func_code_block(self):
        code = []
        # RPN calculator
        stack = []
        intermediate_id = 0
        expression_recorder = {}
        for token in [(token, self._get_token_type(token)) for token in self._postfix_notation]:
            token_name, token_type = token
            if token_type != self.TYPE_OPERATOR:
                stack.append(token)
                continue
            operand2_name, operand2_type = stack.pop()
            operand1_name, operand1_type = stack.pop()
            python_expression = f'{operand1_name} {token_name} {operand2_name}'
            if python_expression not in expression_recorder:
                intermediate_param = f'intermediate_param_{intermediate_id}'
                intermediate_id += 1
                intermediate_param_type = self._infer_op_res_type(operand1_type, token_name, operand2_type)
                code.append(f'    {intermediate_param} = {python_expression}')
                expression_recorder[python_expression] = (intermediate_param, intermediate_param_type)
            else:
                intermediate_param, intermediate_param_type = expression_recorder[python_expression]
            stack.append((intermediate_param, intermediate_param_type))
        ret_name, ret_type = stack.pop()
        code.append(f'    return {ret_name}')
        self._return_type = self._to_dsl_type(ret_type)
        # construct parameters name and type
        parameters = []
        for parameter_name in sorted(self._inputs.keys()):
            parameter = self._inputs[parameter_name]
            # get Output type from owner's definition; get PipelineParameter type from user's annotation
            from azure.ml.component.component import Output
            if isinstance(parameter, Output):
                parameter_type = parameter._owner._definition.outputs.get(parameter._name)._type
            else:
                parameter_type = parameter._user_annotation
            parameter_type = self._to_python_type(parameter_type)
            parameters.append(f'{parameter_name}: {parameter_type}')
        component_func_declaration_line = self.COMPONENT_FUNC_DECLARATION_LINE\
            .replace('@@component_parameters@@', ', '.join(parameters))\
            .replace('@@component_return_type@@', self._return_type)
        decorator_line = self.DSL_DECORATOR_LINE.replace('@@infix_notation@@', self.expression)
        decorator_line = decorator_line.replace('@@expression_version@@', str(time.time()))
        code = [self.IMPORT_DSL_LINE,
                self.IMPORT_DSL_TYPES_LINE.replace('@@component_return_type@@', self._return_type),
                decorator_line,
                component_func_declaration_line] + code
        return '\n'.join(code) + '\n'  # extra newline for blank line at end of file

    def _create_dynamic_component(self):
        if self._created_component is None:
            # need to dump generated code to file for snapshot (dsl.command_component logic)
            tmp_py_folder = tempfile.mkdtemp()
            module_name = self.COMPONENT_FUNC_NAME
            tmp_filename = module_name + '.py'
            with open(os.path.join(tmp_py_folder, tmp_filename), 'w') as fp:
                fp.write(self._component_func_code_block)
            from azure.ml.component.dsl._utils import _import_component_with_working_dir
            module = _import_component_with_working_dir(module_name, working_dir=tmp_py_folder, force_reload=True)
            # remove __pycache__ if exists, otherwise it will be uploaded in snapshot
            pycache_folder = os.path.join(tmp_py_folder, self.PYCACHE_FOLDER_NAME)
            if os.path.exists(pycache_folder):
                shutil.rmtree(pycache_folder)
            component_func = {
                k: v for k, v in inspect.getmembers(module, inspect.isfunction)}[self.COMPONENT_FUNC_NAME]
            component_kwargs = {k: v for k, v in self._inputs.items()}
            self._created_component = component_func(**component_kwargs)
        return self._created_component
