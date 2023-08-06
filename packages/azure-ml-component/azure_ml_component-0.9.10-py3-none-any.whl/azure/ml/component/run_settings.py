# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Defines classes for run settings."""

import os
import copy
from inspect import Parameter
from functools import partial
from typing import List, Sequence
import types

from azureml._base_sdk_common.field_info import _FieldInfo
from azureml.core.runconfig import RunConfiguration
from azureml.exceptions._azureml_exception import UserErrorException
from ._dynamic import KwParameter, create_kw_method_from_parameters
from ._pipeline_parameters import PipelineParameter
from ._restclients.service_caller_factory import _DesignerServiceCallerFactory
from ._run_settings_contracts import try_convert_obj_to_dict, try_convert_obj_to_value
from ._util._utils import _get_param_in_group_from_pipeline_parameters, _get_parameter_static_value
from ._util._exceptions import InvalidTargetSpecifiedError, ComponentValidationError, UnexpectedAttributeError
from ._util._loggerfactory import _LoggerFactory
from ._util._telemetry import WorkspaceTelemetryMixin

_logger = None


def _azureml_component_populate_default_runsettings():
    return os.environ.get('AZUREML_COMPONENT_POPULATE_DEFAULT_RUNSETTINGS', 'False').lower() == 'true'


def _get_logger():
    global _logger
    if _logger is not None:
        return _logger
    _logger = _LoggerFactory.get_logger()
    return _logger


class _RunSettingsStore:
    """Dict store used by RunSettings."""

    def __init__(self):
        """Initialize store with an empty dictionary."""
        self._user_provided_values = {}

    def set_value(self, param_id, value):
        """Set parameter value by parameter id."""
        self._user_provided_values[param_id] = value

    def delete_value(self, param_id):
        """Delete the value by parameter id."""
        if param_id in self._user_provided_values:
            self._user_provided_values.pop(param_id)

    def get_value(self, param_id):
        """Get parameter value by parameter id."""
        return self._user_provided_values.get(param_id, None)

    @property
    def values(self):
        """Return the copy of parameter values dict."""
        return copy.copy(self._user_provided_values)

    @property
    def _is_specified(self):
        return len(self._user_provided_values) > 0


class _RunSettingsInterfaceParam:
    """Display wrapper for RunSettingParam."""

    def __init__(self, definition, interface, deprecated_hint=None, is_compute_param=False):
        """Initialize from RunSettingParam.

        :param definition: The definition of this parameter.
        :type definition: RunSettingParam
        :param interface: The interface path of this parameter. For example, interface of
        'target' is 'runsettings.target', interface of 'node_count' is 'runsettings.resource_layout.node_count'.
        This is for generating the hint message to customer.
        :type interface: str
        :param deprecated_hint: Hint message for deprecated parameter.
        :type deprecated_hint: str
        :param is_compute_param: Indicate this parameter is k8s runsettings parameter or not.
        :type is_compute_param: bool
        """
        self.definition = definition
        self.deprecated_hint = deprecated_hint
        if self.definition.is_compute_target:
            # Here we use a common name for compute target param
            # In backend contract, HDI uses 'compute_name', others use 'target'
            self.display_name = 'Target'
            self.display_argument_name = 'target'
        else:
            self.display_name = self.definition.name
            self.display_argument_name = self.definition.argument_name
        self.is_compute_param = is_compute_param
        self.interface = interface

    def __getattr__(self, name):
        """For properties not defined in this class, retrieve from RunSettingParam."""
        return getattr(self.definition, name)

    def _switch_definition_by_current_settings(self, settings: dict):
        """
        Switch to the right definition according to current settings for multi-definition parameter.

        :param settings: current runsettings in format of dict.
        :type settings: dict
        :return: parameter status in current settings.
        :rtype: ParamStatus
        """
        return self.definition._switch_definition_by_current_settings(settings)

    def __repr__(self):
        """Return str(self)."""
        return self.__str__()

    def __str__(self):
        """Return the description of a Output object."""
        return "{}".format(self.interface)


class _RunSettingsParamSection:
    """A section of parameters which will dynamically generate a configure function in runtime."""

    def __init__(self, display_name: str, description: str, sub_sections=[],
                 parameters: List[_RunSettingsInterfaceParam]=[], path=None):
        """Initialize from a list of _RunSettingsInterfaceParam, display name and description.

        :param display_name: The argument name of this section.
        :type display_name: str
        :param description: The description of this section.
        :type description: str
        :param sub_sections: The sub sections of this section.
        :type sub_sections: List[_RunSettingsParamSection]
        :param parameters: The parameters of this section.
        :type parameters: List[_RunSettingsInterfaceParam]
        :param path: The interface path of this parameter.
        :type path: str
        """
        self.display_name = display_name
        self.path = path
        self.description = description
        self.sub_sections = sub_sections
        self.parameters = parameters
        # Params and doc string cache for generating `configure` function
        self._conf_func_cache = None

    def get_conf_func(self, original_conf_func):
        """Return the `configure` function of runsettings."""
        if not self._conf_func_cache:
            params, func_docstring = self._get_conf_func_params_and_docstring()
            conf_func = create_kw_method_from_parameters(
                original_conf_func,
                parameters=params,
                documentation=func_docstring,
            )
            # Set doc string in self
            original_conf_func.__self__.__doc__ = func_docstring
            # Add to cache
            self._conf_func_cache = conf_func
            return conf_func
        else:
            # Here we re-bind the cached conf func to new runsetting instance, to improve perf
            new_func = types.MethodType(self._conf_func_cache.__func__, original_conf_func.__self__)
            # Set doc string in self
            original_conf_func.__self__.__doc__ = self._conf_func_cache.__doc__
            return new_func

    def _get_conf_func_params_and_docstring(self):
        """Return the params and docstring of `configure` func in format of tuple."""
        func_docstring_lines = []
        if self.description is not None:
            func_docstring_lines.append(self.description)
        if len(self.parameters) > 0:
            func_docstring_lines.append("\n")
        params, _doc_string = _format_params(self.parameters, self.sub_sections)
        func_docstring_lines.extend(_doc_string)
        func_docstring = '\n'.join(func_docstring_lines)
        return params, func_docstring


class RunSettings(WorkspaceTelemetryMixin):
    """A RunSettings aggregates the run settings of a component."""

    # Set a flag here, so we could use it in __setattr__ to init private attrs in naive way.
    _initialized = False

    def __init__(self, display_section: _RunSettingsParamSection, store: _RunSettingsStore, workspace):
        """
        Initialize RunSettings.

        :param display_section: The display section.
        :type display_section: _RunSettingsParamSection
        :param store: The store which is used to hold the param values of RunSettings.
        :type store: _RunSettingsStore
        :param workspace: Current workspace.
        :type workspace: Workspace
        """
        self._store = store
        self._workspace = workspace
        self._params_mapping = {p.display_argument_name: p for p in display_section.parameters}
        self._sections_mapping = {}
        self._path = display_section.path
        self._name = display_section.display_name
        self._generate_configure_func_and_properties(display_section)
        if not self._workspace:
            # Not validate argument of configure.
            self.configure = partial(RunSettings.configure, self)
        WorkspaceTelemetryMixin.__init__(self, workspace=workspace)
        self._initialized = True

    def _generate_configure_func_and_properties(self, display_section: _RunSettingsParamSection):
        # Generate configure function
        self.configure = display_section.get_conf_func(self.configure)
        # Generate section properties
        for sub_display_section in display_section.sub_sections:
            sub_section = RunSettings(sub_display_section, self._store, self._workspace)
            self._sections_mapping[sub_display_section.display_name] = sub_section

    def configure(self, *args, **kwargs):
        """
        Configure the runsettings.

        Note that this method will be replaced by a dynamic generated one at runtime with parameters
        that corresponds to the runsettings of the component.
        """
        # Note that the argument list must be "*args, **kwargs" to make sure
        # vscode intelligence works when the signature is updated.
        # https://github.com/microsoft/vscode-python/blob/master/src/client/datascience/interactive-common/intellisense/intellisenseProvider.ts#L79
        # Filter None values since it's the default value
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        for k, v in kwargs.items():
            self._set_param_or_section(k, v)

    def validate(
            self, raise_error=False, process_error=None, for_definition_validate=False, definition_validator=None,
            component_type=None
    ):
        """
        Validate RunSettings parameter values for current component.

        :param raise_error: Whether to raise exceptions on error.
        :type raise_error: bool
        :param process_error: The error process function to be used.
        :type process_error: function
        :param for_definition_validate: If the validate is for pipeline definition validate.
        :type for_definition_validate: bool
        :param definition_validator: definition validator
        :type definition_validator: azure.ml.component._component_validator.DefinitionValidator
        :param component_type: indicate current node type.
        :type component_type: str

        :return: The errors found during validation.
        :rtype: builtin.list
        """
        all_settings = self._get_flat_values()
        return self._validate(
            all_settings, raise_error, process_error, for_definition_validate, definition_validator, component_type
        )

    def _validate(
            self,
            all_settings,
            raise_error=False,
            process_error=None,
            for_definition_validate=False,
            definition_validator=None,
            component_type=None
    ):
        errors = []

        from ._component_validator import ComponentValidator, Diagnostic

        def process_runsetting_error(e: Exception, error_type, variable_name, variable_type):
            ve = ComponentValidationError(str(e), e, error_type)
            if raise_error:
                raise ve
            else:
                errors.append(Diagnostic.create_diagnostic(ve.message, ve.error_type, variable_name, variable_type))

        if process_error is None:
            process_error = process_runsetting_error
        # Validate top-level parameters
        for spec in self._params_mapping.values():
            ComponentValidator.validate_runsetting_parameter(
                all_settings, spec, process_error, for_definition_validate, definition_validator, component_type)
        # Validate sections
        for section in self._sections_mapping.values():
            section._validate(all_settings, raise_error, process_error, for_definition_validate, definition_validator)
        return errors

    def __setattr__(self, key, value):
        """Override base function to set parameter values to store, and do validation before set."""
        if not self._initialized or key == '_store':
            # bypass setattr in __init__ and in copy runsettings (_store)
            super().__setattr__(key, value)
        else:
            self._set_param_or_section(key, value)

    def _set_param_or_section(self, key, value):
        if key in self._params_mapping.keys():
            self._set_parameter(key, value)
        elif key in self._sections_mapping.keys():
            section = self._sections_mapping[key]
            section._set_section(value)
        elif not self._workspace:
            if isinstance(value, dict):
                # Generate section in run settings.
                section = self._sections_mapping.get(key, None)
                if not section:
                    section = self.__getattr__(key)
                section._set_section(value)
            else:
                if key not in self._params_mapping:
                    from ._core._run_settings_definition import RunSettingParam, RunSettingParamDefinition
                    interface = "{}.{}".format(self._path or "", key).strip(".")
                    static_value = _get_parameter_static_value(value)
                    self._params_mapping[key] = _RunSettingsInterfaceParam(
                        definition=RunSettingParam(
                            definition_list=[RunSettingParamDefinition(
                                name=key, argument_name=key,
                                section_argument_name=self._path,
                                type=type(static_value).__name__ if static_value else None,
                                type_in_py=type(static_value))]),
                        interface=interface)
                self._set_parameter(key, value)
        else:
            all_available_keys = sorted(
                set(self._params_mapping.keys()).union(set(self._sections_mapping.keys())))
            raise UserErrorException(
                "'{}' is not an expected key, all available keys are: {}.".format(key, all_available_keys))

    def _set_parameter(self, key, value):
        spec = self._params_mapping[key]
        if spec.deprecated_hint is not None:
            _get_logger().warning('{} is {}'.format(spec.interface, spec.deprecated_hint))
        value = try_convert_obj_to_value(spec.id, value, spec.parameter_type_in_py)
        # We use a store here, which is a component-level instance.
        # This is for support old interfaces and new interfaces work together.
        self._store.set_value(self._params_mapping[key].id, value)

    def _has_param(self, param):
        """Test if a runsetting param has been set."""
        return param in self._params_mapping

    def __getattr__(self, key):
        """Override base function to get parameter values from store."""
        if key in self._params_mapping:
            # For top-level parameters, we get the value from store.
            return self._store.get_value(self._params_mapping[key].id)
        if key in self._sections_mapping:
            return self._sections_mapping[key]
        if self._workspace:
            # Raise exception for unknown keys when workspace exists.
            all_available_keys = sorted(
                set(self._params_mapping.keys()).union(set(self._sections_mapping.keys())))
            raise UnexpectedAttributeError(
                "'{}' is not an expected key, all available keys are: {}.".format(key, all_available_keys))
        else:
            sub_section_path = "{}.{}".format(self._path or "", key).strip(".")
            sub_section = RunSettings(
                _RunSettingsParamSection(
                    display_name=key, description=None,
                    path=sub_section_path),
                self._store,
                self._workspace
            )

            self._sections_mapping[key] = sub_section
            return sub_section

    def __repr__(self):
        """Customize for string representation."""
        return repr(self._get_values())

    def _get_values(self, ignore_none=False):
        # Here we skip deprecated parameters, generate the values with new interfaces.
        json_dict = {k: getattr(self, k) for k, v in self._params_mapping.items() if v.deprecated_hint is None}
        if ignore_none:
            json_dict = {k: v for k, v in json_dict.items() if v is not None}
        for section_name, section in self._sections_mapping.items():
            section_dict = section._get_values(ignore_none=ignore_none)
            if len(section_dict) > 0:
                json_dict[section_name] = section_dict
        return json_dict

    def _get_user_assigned_flat_values(self):
        return self._store.values

    def _get_flat_values(self):
        user_provided_values = self._get_user_assigned_flat_values()
        default_values = self._populate_default_values(user_provided_values)
        if _azureml_component_populate_default_runsettings():
            return {**user_provided_values, **default_values}
        else:
            return user_provided_values

    def _copy_and_update(self, source_setting, pipeline_parameters, pipeline_name=None):
        """
        Copy and update settings from source_setting to self with pipeline parameters.

        :param source_setting:
        :type source_setting: RunSettings
        :param pipeline_parameters: pipeline parameters
        :type pipeline_parameters: dict
        :param pipeline_name: the runsettings' component's pipeline name.
        :type pipeline_name: str
        """
        def _update_pipeline_parameters_runsetting(obj):
            """Replace PipelineParameter in runsettings with parameter from input."""
            if pipeline_parameters is None:
                return obj
            from azure.ml.component.component import Input
            if isinstance(obj, PipelineParameter) or isinstance(obj, Input):
                obj = _get_param_in_group_from_pipeline_parameters(
                    obj.name, pipeline_parameters, obj._groups if isinstance(obj, PipelineParameter) else None,
                    pipeline_name=pipeline_name)
                if obj is Parameter.empty:
                    raise Exception(f'Runsetting {param_id!r} not found in pipeline parameters!')
            elif isinstance(obj, dict):
                obj = {k: _update_pipeline_parameters_runsetting(v) for k, v in obj.items()}
            elif type(obj) in [list, tuple]:
                obj = type(obj)([_update_pipeline_parameters_runsetting(i) for i in obj])
            return obj

        if source_setting is None:
            return
        if not self._workspace:

            def _update_params_and_section(origin_setting, destination_setting):
                for k, v in origin_setting._params_mapping.items():
                    if v.deprecated_hint:
                        continue
                    destination_setting._set_param_or_section(k, None)
                for k, v in origin_setting._sections_mapping.items():
                    sub_section_setting = getattr(destination_setting, k)
                    for sub_k in v._params_mapping:
                        sub_section_setting._set_param_or_section(sub_k, None)

            # When runsetting without workspace, generate the param and section to current runsettings.
            _update_params_and_section(source_setting, self)
        for param_id, param_value in source_setting._store._user_provided_values.items():
            self._store.set_value(param_id, _update_pipeline_parameters_runsetting(param_value))

    _TARGET_SELECTOR_NAME = 'target_selector'
    _TARGET_NAME = 'target'

    def _get_target(self):
        """
        Get the compute target of component.

        Return `target_selector` in format of ('target_selector', compute_type) if specified, otherwise
        return `target`.
        """
        # Check target_selector
        if hasattr(self, self._TARGET_SELECTOR_NAME):
            compute_type = _get_parameter_static_value(self.target_selector.compute_type)
            if compute_type is not None:
                return (self._TARGET_SELECTOR_NAME, compute_type)
        # Return target
        if not hasattr(self, self._TARGET_NAME):
            return None
        return _get_parameter_static_value(self.target)

    def _populate_default_values(self, user_provided_values, default_values=None):
        if default_values is None:
            default_values = {}
        # Get default values for parameters without enabled_by, disabled_by, and no user-provided values
        default_values.update({p.id: p.default_value for p in self._params_mapping.values()
                               if p.enabled_by is None and p.disabled_by is None and
                               p.id not in user_provided_values})
        for spec in self._params_mapping.values():
            param_id = spec.id
            if spec.deprecated_hint is not None or \
                    param_id in user_provided_values or param_id in default_values:
                # By pass deprecated, user-assigned and processed parameters
                continue

            # Use `user_provided_values` + `default_values` to calculate the status of parameter
            status = spec._switch_definition_by_current_settings({**user_provided_values, **default_values})
            # Only when status is active, and user-provided value is none
            from ._core._run_settings_definition import ParamStatus
            if status == ParamStatus.Active:
                default_values[param_id] = spec.default_value

        # Iteratly populate sub sections
        for section in self._sections_mapping.values():
            section._populate_default_values(user_provided_values, default_values)
        return default_values

    def _clear_section_values(self):
        for v in self._params_mapping.values():
            self._store.delete_value(v.id)

    def _set_section_by_dict(self, obj):
        self._clear_section_values()
        for k, v in obj.items():
            self._set_param_or_section(k, v)

    def _set_section(self, obj):
        # Convert object to dict first, then set section by dict
        obj_dict = try_convert_obj_to_dict(self._name, obj)
        if obj_dict:
            self._set_section_by_dict(obj_dict)
        else:
            raise UserErrorException(
                "'{}' is an unsupported type for runsetting '{}'.".format(type(obj).__name__, self._name))


class PipelineRunSettingsPriority:
    """For strong type intellisense of 'runsettings.priority.scope'."""

    _SCOPE_FIELD_NAME = 'scope'

    def __init__(self, priority_section, workspace):
        """
        Initialize priority runsetting.

        :param priority_section: Priority section of PipelineRunSettings.
        :type priority_section: RunSettings
        :param workspace: Current workspace.
        :type workspace: Workspace
        """
        self._priority_section = priority_section
        self._workspace = workspace
        # if scope not exists, manually create it and set its type as integer;
        #   otherwise PipelineParameter scenario will break.
        if self._SCOPE_FIELD_NAME not in self._priority_section._params_mapping.keys():
            from ._core._run_settings_definition import RunSettingParam, RunSettingParamDefinition
            interface = f'{self._priority_section._path}.{self._SCOPE_FIELD_NAME}'.strip('.')
            self._priority_section._params_mapping[self._SCOPE_FIELD_NAME] = _RunSettingsInterfaceParam(
                definition=RunSettingParam(
                    definition_list=[
                        RunSettingParamDefinition(
                            name=self._SCOPE_FIELD_NAME,
                            argument_name=self._SCOPE_FIELD_NAME,
                            section_argument_name=self._priority_section._path,
                            type=int.__name__,
                            type_in_py=int
                        )
                    ]
                ),
                interface=interface
            )

    @property
    def scope(self):
        """For strong type intellisense of 'runsettings.priority.scope'."""
        return self._priority_section.scope

    @scope.setter
    def scope(self, value):
        self._priority_section.scope = value

    def _set_param_or_section(self, key, value):
        setattr(self._priority_section, key, value)


class PipelineRunSettings(RunSettings):
    """A RunSettings aggregates the run settings of a pipeline."""

    _PRIORITY_FIELD_NAME = 'priority'
    _PRIORITY_DEFAULT_VALUE = {'scope': None}

    def __init__(self, display_section: _RunSettingsParamSection, store: _RunSettingsStore, workspace):
        """
        Initialize Pipeline RunSettings.

        :param display_section: The display section.
        :type display_section: _RunSettingsParamSection
        :param store: The store which is used to hold the param values of RunSettings.
        :type store: _RunSettingsStore
        :param workspace: Current workspace.
        :type workspace: Workspace
        """
        super(PipelineRunSettings, self).__init__(display_section, store, workspace)

    @property
    def priority(self) -> PipelineRunSettingsPriority:
        """For strong type intellisense of 'runsettings.priority'."""
        return PipelineRunSettingsPriority(self.__getattr__(self._PRIORITY_FIELD_NAME), self._workspace)

    @priority.setter
    def priority(self, value):
        self._set_param_or_section(self.PRIORITY_FIELD_NAME, value)


def _get_compute_type(ws, compute_name):
    if compute_name is None:
        return None
    service_caller = _DesignerServiceCallerFactory.get_instance(ws)
    compute = service_caller.get_compute_by_name(compute_name)
    if compute is None:
        raise InvalidTargetSpecifiedError(message="Cannot find compute '{}' in workspace.".format(compute_name))
    return compute.compute_type


def _has_specified_runsettings(runsettings: RunSettings) -> bool:
    return runsettings is not None and runsettings._store._is_specified


def _format_params(source_params: Sequence[_RunSettingsInterfaceParam],
                   section_params: Sequence[_RunSettingsParamSection]):
    target_params = []
    func_docstring_lines = []
    for param in source_params:
        # For the compute run settings,
        # the default value in spec is not match the value in description,
        # so we remove "default value" part in doc string for this case.
        param_line = ":param {}: {}".format(param.display_argument_name, param.description)
        if param.is_optional:
            param_line = "{} (optional{})".format(
                param_line, '' if param.is_compute_param else ', default value is {}'.format(param.default_value))
        if param.deprecated_hint is not None:
            param_line = "{} ({})".format(param_line, param.deprecated_hint)
        func_docstring_lines.append(param_line)

        func_docstring_lines.append(":type {}: {}".format(param.display_argument_name, param.parameter_type))
        target_params.append(KwParameter(
            param.display_argument_name,
            annotation=param.description,
            # Here we set all default values as None to avoid overwriting the values by default values.
            default=None,
            _type=param.parameter_type))
    for section in section_params:
        target_params.append(KwParameter(
            section.display_name,
            annotation=section.description,
            # Here we set all default values as None to avoid overwriting the values by default values.
            default=None,
            _type='object'))
    return target_params, func_docstring_lines


def _update_run_config(component, run_config: RunConfiguration, compute_type='Cmk8s'):
    """Use the settings in k8srunsettings to update RunConfiguration class."""
    if component._definition.runsettings is None:
        # For local-run components, no runsettings definition here
        return
    compute_params_spec = component._definition.runsettings.compute_params
    if compute_params_spec is None:
        return
    compute_field_map = {'Cmk8s': 'cmk8scompute', 'CmAks': 'cmakscompute'}
    if compute_type in compute_field_map:
        field_name = compute_field_map[compute_type]
        aks_config = {'configuration': dict()}
        k8srunsettings = component._k8srunsettings._get_flat_values()
        for param_id, param in compute_params_spec.items():
            value = k8srunsettings.get(param_id)
            if value is not None:
                aks_config['configuration'][param.argument_name] = value
        run_config._initialized = False
        setattr(run_config, field_name, aks_config)
        run_config._initialized = True
        RunConfiguration._field_to_info_dict[field_name] = _FieldInfo(dict,
                                                                      "{} specific details.".format(field_name))
        run_config.history.output_collection = True
