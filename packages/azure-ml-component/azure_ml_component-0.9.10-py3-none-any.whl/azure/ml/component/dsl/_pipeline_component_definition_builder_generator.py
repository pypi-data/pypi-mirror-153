# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from inspect import Parameter, signature
from .._pipeline_component_definition_builder import PipelineComponentDefinitionBuilder
from .._util._exceptions import UserErrorException


class PipelineComponentDefinitionBuilderGenerator:
    """The generator class of pipeline component definition builder, to support non pipeline parameters and reuse."""
    def __init__(self, non_pipeline_parameters: list=None, **builder_init_args):
        self._non_pipeline_parameter_names = non_pipeline_parameters or []
        self._builder_init_args = builder_init_args
        self._ensure_non_pipeline_parameters_correct()
        self._definition_builder_cache = {}

    def get_or_create_pipeline_definition_builder(
            self, user_init_args: dict = {}, dynamic_param_name=None, dynamic_param_value=None):
        # Build non pipeline parameter values dict
        default_values = self._get_func_defined_args()
        non_pipeline_parameters = {
            k: user_init_args[k] if k in user_init_args else default_values.get(k, None)
            for k in self._non_pipeline_parameter_names}
        # Add dynamic parameter into non pipeline parameters to get cached builder
        all_dynamic_parameters = {**non_pipeline_parameters}
        if dynamic_param_name:
            all_dynamic_parameters.update(dynamic_param_value)
        cached_builder = self._get_builder_from_cache(all_dynamic_parameters)
        if cached_builder is None:
            builder = PipelineComponentDefinitionBuilder.from_func(
                **self._builder_init_args,
                non_pipeline_parameters=non_pipeline_parameters,
                dynamic_param_name=dynamic_param_name,
                dynamic_param_value=dynamic_param_value)
            self._add_builder_to_cache(builder, all_dynamic_parameters)
            cached_builder = builder
        return cached_builder

    def _ensure_non_pipeline_parameters_correct(self):
        """This func is to ensure self._non_pipeline_parameter_names are in the params of dsl func.
        Since self._non_pipeline_parameter_names is directly from user, so it may contain some wrong param names
        by typo or other human errors. So this func will raise exception for unrecognized param names.
        """
        # non pipeline parameters type check
        if (not isinstance(self._non_pipeline_parameter_names, list)) or \
                (len([p for p in self._non_pipeline_parameter_names if not isinstance(p, str)]) > 0):
            raise UserErrorException("Type of 'non_pipeline_parameters' in dsl.pipeline should be a list of string.")
        # value check
        arg_definitions = self._get_func_defined_args()
        unrecognized_param_names = [v for v in self._non_pipeline_parameter_names if v not in arg_definitions]
        if len(unrecognized_param_names) > 0:
            if len(unrecognized_param_names) == 1:
                param_msg = f"'{unrecognized_param_names[0]}' is not a parameter"
            else:
                param_msg = f"{unrecognized_param_names} are not parameters"
            raise UserErrorException(
                f"non_pipeline_parameter: {param_msg} of func '{self._get_func().__name__}'"
            )

    def _get_func_defined_args(self):
        """Get the parameter definitions of dsl pipeline func."""
        func = self._get_func()
        func_params = signature(func).parameters
        return {p.name: None if p.default is Parameter.empty else p.default for p in func_params.values()}

    def _get_func(self):
        """Get the dsl pipeline func."""
        return self._builder_init_args.get('func')

    def _get_builder_from_cache(self, non_pipeline_parameters: dict):
        try:
            cache_key = self._get_builder_cache_key(non_pipeline_parameters)
        except TypeError:
            # Means the values of non pipeline parameters have unhashable items
            # Suppress the error and return None (means not reuse)
            return None
        return self._definition_builder_cache.get(cache_key, None)

    def _add_builder_to_cache(self, builder, non_pipeline_parameters: dict):
        try:
            cache_key = self._get_builder_cache_key(non_pipeline_parameters)
        except TypeError:
            # Catch hash error and do nothing, means not reuse
            return
        self._definition_builder_cache[cache_key] = builder

    @classmethod
    def _get_builder_cache_key(cls, non_pipeline_parameters: dict):
        """Calculate a hash key based on a non pipeline parameter key-value dict.
        Basic rule: return a hash key only when the items in `non_pipeline_parameters`'s value set
        are all hashable types. Otherwise throw a TypeError (for example: "TypeError: unhashable type: 'list'")
        (TODO: wrap a more meaningful error type)
        Special handling: if a value in `non_pipeline_parameters` is a list/dict contains only hashable items,
        also return a hash key. As by default, list/dict is unhashable type.

        :param non_pipeline_parameters: A dict of (param_name: str, param_value: any)
        :type non_pipeline_parameters: dict
        :return: hash key
        :rtype: int
        :raises:
         :class:`TypeError`
        """
        if len(non_pipeline_parameters) > 0:
            # Special handle for list/dict (just one layer, means list of list of hashable items is still unhashable)
            def hashable_list_or_dict(v):
                if isinstance(v, list):
                    return tuple(v)
                if isinstance(v, dict):
                    return tuple(v.items())
                return v

            values = {k: hashable_list_or_dict(v) for k, v in sorted(non_pipeline_parameters.items())}
            return hash((tuple(values.items())))
        return None
