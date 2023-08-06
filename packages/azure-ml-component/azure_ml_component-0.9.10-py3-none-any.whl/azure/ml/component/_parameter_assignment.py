# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from azureml.exceptions._azureml_exception import UserErrorException
from ._pipeline_parameters import PipelineParameter
from ._restclients.designer.models import ParameterValueType
from ._util._utils import _flatten_pipeline_parameters
from ._util._loggerfactory import _LoggerFactory


class _ParameterAssignment:
    """
    Resolve parameter reference embedded in string.

    Usage:
        - Format function with str, int, float and boolean.
            ```
            @dsl.pipeline(name='sample-pipeline', default_compute_target='aml-compute')
            def sample_pipeline(str1, int1, float1):
                component = print_string_component_func(
                    string_parameter='format_str1_{}_int1_{}_float1_{}'.format(str1, int1, float1))
            ```
        - '+' operation with explicit 'str()' wrap around the PipelineParameter.
            ```
            @dsl.pipeline(name='sample-pipeline')
            def sample_pipeline(str1):
                component = print_string_component_func(
                    string_parameter='format_str1_' + str(str1))
            ```
        - f'' operation with str, int, float and boolean.
            ```
            @dsl.pipeline(name='sample-pipeline')
            def sample_pipeline(str1, int1, float1):
                component = print_string_component_func(
                    string_parameter=f'format_str1_{str1} {int1} {float1}')
            ```
        - % operation with '%s' embedded in string.
            ```
            @dsl.pipeline(name='sample-pipeline')
            def sample_pipeline(str1, int1, float1):
                component = print_string_component_func(
                    string_parameter='format_str1_%s_int1_%s_float1_%s' % (str1, int1, float1))
            ```

        - Component.set_inputs function instead of direct assignment.
            ```
            @dsl.pipeline(name='sample-pipeline')
            def sample_pipeline(str1, int1, float1):
                component = print_string_component_func()
                component.set_inputs(string_parameter='format_str1_%s_int1_%s_float1_%s' % (str1, int1, float1))
            ```
        - Use parameter assignment as input or partial input of sub pipeline.
            ```
            @dsl.pipeline(name='sample-sub-pipeline')
            def sample_sub_pipeline(str1, str2):
                component = print_string_component_func(
                    string_parameter='format str1 {}'.format(str1),
                    string_parameter2=str2)

            @dsl.pipeline(name='sample-pipeline')
            def sample_pipeline(param1, param2):
                sample_sub_pipeline(str1='param1 {}'.format(param1), str2='param2 is {}'.format(param2))
            ```

    Note:
        - Single '@' will not make a difference to result.
            - 'prefix@@@mail_server@@.com' will be separate to ['prefix@', 'mail_server', '.com']
        - Unrecognized parameter name will cause a warning.
            - 'prefix@@@mail_server@@.com' given without a PipelineParameter named 'mail_server'
                will be separate to ['prefix@', 'mail_server', '.com'], and the assignment.value is
                'prefix@@@mail_server@@.com'.
        - Content embedded does not match python variable naming rules ([a-zA-Z][a-zA-Z0-9]*) will be a constant.
            - 'prefix@@@mail server@@.com' 'prefix@@@mail.server@@.com' 'prefix@@@123mail_server@@.com'
        - Content will be matched only **once**. (?)
            - '@@key1@@key2@@' with dict {'key2': 'val'} will **NOT** be resolved as '@@key1val', because we split
                it as '@@key1@@' and 'key2@@', we are not going to try another split ('@@key1' and '@@key2@@) even if
                we can't find 'key1' in the assignments values dictionary.
        - A warning will be print if there is a part with pipeline parameter type
            but can not be found in the given assignments values dictionary.
            - e.g. '@@key1@@' with an empty dictionary.

    Invalid case:
        - An input port(path/directory) instead of parameter.
        - '+' operation without 'str()' wrap around the PipelineParameter
            - string_parameter='format_str1_' + str1
        - % operation with '%d', '%f' in string.
            - string_parameter='format_str1_%s_int1_%d_float1_%f' % (str1, int1, float1)
        - Call some string functions not belongs to PipelineParameter.
            ```
            @dsl.pipeline(name='sample-pipeline')
            def sample_pipeline(str1):
                component = print_string_component_func(
                    string_parameter=str1.format('some-string'))
            ```

    """
    SEPARATOR = '@@'
    LITERAL = ParameterValueType.literal.value
    PIPELINE_PARAMETER = ParameterValueType.graph_parameter_name.value
    CONCATENATE = ParameterValueType.concatenate.value

    class _ParameterAssignmentPart:
        def __init__(self, _str, _type):
            self.str = _str
            self.type = _type

    def __init__(self, formatter, assignments, assignments_values_dict=None):
        """
        Initiate a _ParameterAssignment.

        :param formatter: A string with @@name@@ as placeholder inside to format values.
        :type formatter: str
        :param assignments: Separate parts and type of formatter.
        :type assignments: builtin.list[_ParameterAssignment._ParameterAssignmentPart]
        :param assignments_values_dict: A dict with parameter name as key and PipelineParameter as value.
            Note that part in assignments may not appear in values dict even if it has PIPELINE_PARAMETER part type.
        :type assignments_values_dict: dict[str, Union(PipelineParameter, _ParameterAssignment)]
        """
        self.formatter = formatter
        self.assignments = assignments
        self.assignments_values_dict = assignments_values_dict if assignments_values_dict is not None else {}
        # To cache the calculated value
        self._value = None

    def __setattr__(self, key, value):
        if key in ['assignments', 'formatter', 'assignments_values_dict'] and hasattr(self, key):
            raise UserErrorException('Attribute {} can not be set after initiate assignment, '
                                     'use _ParameterAssignment.resolve() to have a next try.'.format(key))
        object.__setattr__(self, key, value)

    @staticmethod
    def resolve(str_value, init_params_dict, print_warning=True):
        """
        Resolve a reference like @@name@@ embedded string to PipelineParameter.

        :param str_value: Original string value.
        :type str_value: str
        :param init_params_dict: The parameters key value dict.
        :type init_params_dict: dict
        :param print_warning: Print warning if a matched parameter part is treated as constant.
        :type print_warning: bool
        :return: The resolved value.
        :rtype: _ParameterAssignment
        """

        def resolve_parts(str_value):
            import re
            parts = []
            regex_str = '{}([a-zA-Z_][0-9a-zA-Z_]*){}'.format(SEPARATOR, SEPARATOR)
            ref = re.compile(regex_str)
            last_end = 0
            for match in re.finditer(ref, str_value):
                start = match.start()
                end = match.end()
                if start < last_end:
                    # Only save full match parts.
                    continue
                if last_end != start:
                    # Append value between two matched parts as constant.
                    parts.append(_ParameterAssignment._ParameterAssignmentPart(str_value[last_end:start], LITERAL))
                parts.append(_ParameterAssignment._ParameterAssignmentPart(
                    str_value[start:end].replace(SEPARATOR, ''), PIPELINE_PARAMETER))
                last_end = end
            if last_end != len(str_value):
                # Append the last constant.
                parts.append(_ParameterAssignment._ParameterAssignmentPart(
                    str_value[last_end:len(str_value)], LITERAL))
            return parts

        def correct_with_values_dict(_parts, _dict):
            """
            Correct split part str and type.

            Change part type as ASSIGNMENT if value is instance of _ParameterAssignment.
            :param _parts: all the assignment parts.
            :type _parts: list
            :param _dict: the assignment values dict.
            :type _dict: dict
            """
            if _dict is None:
                _dict = {}
            # Record used parameter name to update dict
            for part in _parts:
                if part.type == PIPELINE_PARAMETER:
                    if part.str in _dict:
                        # values of part could be PipelineParameter or another assignment.
                        value = _dict[part.str]
                        from .component import Input
                        if isinstance(value, Input):
                            value = value._get_internal_data_source()
                        if isinstance(value, _ParameterAssignment):
                            part.type = CONCATENATE
                            continue
                        elif isinstance(value, PipelineParameter):
                            continue
                    if print_warning:
                        _LoggerFactory.get_logger().warning(
                            'The part \'{}\' in \'{}\' can not be matched by PipelineParameter.'.format(
                                part.str, str_value))
            return _parts

        SEPARATOR = _ParameterAssignment.SEPARATOR
        LITERAL = _ParameterAssignment.LITERAL
        PIPELINE_PARAMETER = _ParameterAssignment.PIPELINE_PARAMETER
        CONCATENATE = _ParameterAssignment.CONCATENATE
        if not isinstance(str_value, str) or SEPARATOR not in str_value:
            return str_value
        values_dict = {**_flatten_pipeline_parameters(init_params_dict)}
        parts = resolve_parts(str_value)
        parts = correct_with_values_dict(parts, values_dict)
        values_dict = {part.str: values_dict[part.str] for part in parts
                       if part.type in [PIPELINE_PARAMETER, CONCATENATE] and
                       part.str in values_dict}
        return _ParameterAssignment(
            formatter=str_value, assignments=parts, assignments_values_dict=values_dict)

    @property
    def value(self):
        """Get method to get the actual value of assignment."""
        if self._value is None:
            self._value = self.get_value_with_pipeline_parameters()
        return self._value

    def flatten(self):
        """
        Flatten all the assignments with only LITERAL type or PIPELINE PARAMETER type.
        :return: the flattened assignment.
        :rtype: _ParameterAssignment
        """
        assignments = []
        values_dict = {}
        for part in self.assignments:
            # Append if is LITERAL
            if part.type == self.LITERAL:
                assignments.append(_ParameterAssignment._ParameterAssignmentPart(part.str, self.LITERAL))
                continue
            # part is pipeline parameter name / assignment
            if part.str in self.assignments_values_dict:
                value = self.assignments_values_dict[part.str]
                from .component import Input
                # Value inside values dict could be Input. PipelineParameter. Assignment.
                if isinstance(value, Input):
                    value = value._get_internal_data_source()
                if isinstance(value, PipelineParameter):
                    # Parameter default value must be LITERAL
                    assignments.append(
                        _ParameterAssignment._ParameterAssignmentPart(value._full_name, self.PIPELINE_PARAMETER))
                    values_dict[value._full_name] = value
                elif isinstance(value, _ParameterAssignment):
                    # Expand as real LITERAL value if value is parameter assignment.
                    flatten_part = value.flatten()
                    assignments.extend(flatten_part.assignments)
                    values_dict.update(flatten_part.assignments_values_dict)
                else:
                    # Unrecognized type.
                    # Convert part with pipeline parameter type to a constant.
                    part_value = '{}{}{}'.format(self.SEPARATOR, part.str, self.SEPARATOR)
                    assignments.append(_ParameterAssignment._ParameterAssignmentPart(part_value, self.LITERAL))
            else:
                # Convert part with pipeline parameter type to a constant.
                part_value = '{}{}{}'.format(self.SEPARATOR, part.str, self.SEPARATOR)
                assignments.append(_ParameterAssignment._ParameterAssignmentPart(part_value, self.LITERAL))

        return _ParameterAssignment(
            formatter=self.formatter, assignments=assignments, assignments_values_dict=values_dict)

    def get_value_with_pipeline_parameters(self, pipeline_parameters=None):
        """
        Resolve value with pipeline parameters from input.

        Note that original resolved part and value will not be changed,
        assignments value will be expand and updated if is _ParameterAssignment(recursively).

        :param pipeline_parameters: pipeline parameters value must be basic python type
        (not PipelineParameter or Assignment).
        :type pipeline_parameters: dict[(str, str)]
        :return: the resolved value.
        :rtype: str
        """
        pipeline_parameters = _flatten_pipeline_parameters(pipeline_parameters)
        resolved_parts = []
        flattened_assignment = self.flatten()
        for part in flattened_assignment.assignments:
            # part value is LITERAL or pipeline parameter
            if part.type == self.LITERAL or part.str not in flattened_assignment.assignments_values_dict:
                part_value = part.str
            else:
                part_value = pipeline_parameters[part.str] if part.str in pipeline_parameters else \
                    flattened_assignment.assignments_values_dict[part.str]
                # part_value in assignments values dict always has PipelineParameter type.
                # part_value in pipeline parameter is literal when on top level pipeline.
                # part_value in pipeline parameter has PipelineParameter type when on sub pipeline.
                if isinstance(part_value, PipelineParameter):
                    part_value = part_value.default_value
            resolved_parts.append(str(part_value))
        return ''.join(resolved_parts)

    def update(self, **kwargs):
        """Update parameter assignment values dict, clear cached value and resolve parts again."""
        self.assignments_values_dict.update(**_flatten_pipeline_parameters(kwargs))
        # Clean original value.
        self._value = None
        # Resolve again and set value to current object.
        resolve_result = _ParameterAssignment.resolve(
            self.formatter, self.assignments_values_dict, print_warning=False)
        object.__setattr__(self, 'assignments', resolve_result.assignments)
        # Remove not used key in dict
        object.__setattr__(self, 'assignments_values_dict', resolve_result.assignments_values_dict)

    def expand_all_parameter_name_set(self):
        """
        Expand all values and return the pipeline parameter name set.

        This function is added to get all the pipeline parameter name,
         so we can add the parameter used in pipeline when easily build pipeline graph.
        """
        parameter_names = set()
        for value in self.assignments_values_dict.values():
            from .component import Input
            if isinstance(value, Input):
                value = value._get_internal_data_source()
            if isinstance(value, PipelineParameter):
                parameter_names.add(value._full_name)
            elif isinstance(value, _ParameterAssignment):
                parameter_names.update(value.expand_all_parameter_name_set())
        return parameter_names

    def _get_code_str(self):
        """
        Return the representative sdk code for the parameter_assignments, used for export code.
        """
        prefix = '\''
        paras = []
        postfix = '.format('
        for assignment in self.assignments:
            if assignment.type == self.LITERAL:
                prefix = prefix + assignment.str
            else:
                prefix = prefix + '{}'
                paras.append(assignment.str)
        prefix = prefix + '\''
        postfix = postfix + ', '.join(paras) + ')'
        return prefix + postfix
