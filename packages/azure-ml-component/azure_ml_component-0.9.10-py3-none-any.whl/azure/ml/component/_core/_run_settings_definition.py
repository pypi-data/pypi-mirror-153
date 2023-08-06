# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import json
from typing import Mapping, Sequence
from enum import Enum

from azure.ml.component._core._types import _Param
from azure.ml.component._module_dto import ModuleDto
from azure.ml.component._restclients.service_caller_factory import _DesignerServiceCallerFactory

from azure.ml.component._parameter_assignment import _ParameterAssignment
from .._restclients.designer.models import RunSettingParameter, RunSettingUIWidgetTypeEnum
from .._util._utils import _get_parameter_static_value
from .._pipeline_parameters import PipelineParameter
from ..run_settings import _RunSettingsParamSection, _RunSettingsInterfaceParam, _RunSettingsStore, \
    RunSettings, PipelineRunSettings

_deprecated_params_for_parallel_component = {
    'node_count', 'process_count_per_node', 'error_threshold', 'mini_batch_size', 'logging_level',
    'run_invocation_timeout', 'version', 'run_max_try', 'partition_keys'
}
_deprecated_params_for_distributed_component = {'node_count', 'process_count_per_node'}
_deprecated_params_for_hdinsight_component = {
    'queue', 'driver_memory', 'driver_cores', 'executor_memory', 'executor_cores', 'number_executors',
    'conf', 'name',
}


class RunSettingParamDefinition(_Param):
    """This class represent the definition of one run setting parameter which will be set when run a component."""

    def __init__(
        self, argument_name, name, type, type_in_py,
        description=None, optional=False, default=None, min=None, max=None,
        is_compute_target=False, valid_compute_types=None, json_editor=None,
        section_name=None, section_argument_name=None, section_description=None,
        enum=None, enabled_by_parameter_name=None, enabled_by_parameter_values=None,
        linked_parameters=None, disabled_by=None, module_run_setting_type=None,
        examples=None
    ):
        """Initialize a run setting parameter.

        :param argument_name: The argument name of the parameter which is used to set value in SDK.
        :type argument_name: str
        :param name: The display name of the parameter which is shown in UI.
        :type name: str
        :param type: The type of the parameter.
        :type type: str
                    TODO: Currently the type is not align to the type in InputDefinition, need to be aligned.
        :param type_in_py: The type represented as a python type, used in validation.
        :type type_in_py: type
                          TODO: Refine the validation logic to avoid two types here.
        :param description: The description of the parameter.
        :type description: str
        :param optional: Whether the parameter is optional.
        :type optional: bool
        :param default: The default value of the parameter.
        :type default: Any
        :param min: The min value for a numeric parameter.
        :type min: Union[float, int]
        :param max: The max value for a numeric parameter.
        :type max: Union[float, int]
        :param is_compute_target: Whether the run setting parameter is a compute target parameter or not.
        :type is_compute_target: bool
        :param valid_compute_types: Valid compute types for compute target parameter.
        :type valid_compute_types: [str]
        :param json_editor: Json Editor of the parameter.
        :type json_editor: UIJsonEditor
        :param section_name: Section name of the parameter.
        :type section_name: str
        :param section_argument_name: Section name in python variable style of the parameter.
        :type section_argument_name: str
        :param section_description: Section description of the parameter.
        :type section_description: str
        :param enabled_by_parameter_name: The name of parameter which enables this parameter.
        :type enabled_by_parameter_name: str
        :param enabled_by_parameter_values: The values which enables this parameter.
        :type enabled_by_parameter_values: [str]
        :param linked_parameters: The linked input parameters of this parameter.
        :type linked_parameters: [str]
        :param disabled_by: The parameters which disable this parameter.
        :type disabled_by: [str]
        :param module_run_setting_type: Possible values include: 'Default', 'All',
            'Released', 'Testing', 'Legacy', 'Full'
        :type module_run_setting_type: ModuleRunSettingTypes
        :param examples: An array of examples of this parameter.
        :type examples: [str]
        """
        self._argument_name = argument_name
        self._type_in_py = type_in_py
        self._is_compute_target = is_compute_target
        self._valid_compute_types = valid_compute_types
        self._json_editor = json_editor
        self._section_name = section_name
        self._section_argument_name = section_argument_name
        self._section_description = section_description
        self._id = argument_name if section_argument_name is None else "{}.{}".format(
            section_argument_name, argument_name)
        self._enabled_by_parameter_name = enabled_by_parameter_name
        self._enabled_by_parameter_values = enabled_by_parameter_values
        self._linked_parameters = linked_parameters
        self._disabled_by = disabled_by
        self._module_run_setting_type = module_run_setting_type
        self._examples = examples
        super().__init__(
            name=name, description=description, optional=optional, min=min, max=max,
            enum=enum
        )
        self._type = type
        self._update_default(default)

    @property
    def id(self):
        """Unique name for the run setting parameter."""
        return self._id

    @property
    def is_compute_target(self):
        """Return whether the run setting parameter is a compute target parameter or not."""
        return self._is_compute_target

    @property
    def valid_compute_types(self):
        """Return the valid compute types for compute target."""
        return self._valid_compute_types

    @property
    def type_in_py(self):
        """Return the type represented as a python type, used in validation."""
        return self._type_in_py

    @property
    def argument_name(self):
        """Return the argument name of the parameter."""
        return self._argument_name

    # The following properties are used for backward compatibility
    # TODO: Update such places to use the new names in the spec then remove there properties.
    @property
    def is_optional(self):
        return self.optional

    @property
    def default_value(self):
        return self.default

    @property
    def parameter_type(self):
        return self.type

    @property
    def parameter_type_in_py(self):
        return self.type_in_py

    @property
    def upper_bound(self):
        return self.max

    @property
    def lower_bound(self):
        return self.min

    @property
    def enum_values(self):
        """This property is to align with Rest client's Structured interface parameter."""
        return self.enum

    @property
    def json_schema(self):
        if self._json_editor is not None:
            json_schema = json.loads(self._json_editor.json_schema)
            return json_schema
        return None

    @property
    def section_name(self):
        return self._section_name

    @property
    def section_argument_name(self):
        return self._section_argument_name

    @property
    def section_description(self):
        return self._section_description

    @property
    def enabled_by_parameter_name(self):
        """Represent which parameter enables this parameter."""
        return self._enabled_by_parameter_name

    @property
    def enabled_by_parameter_values(self):
        """Represent which value of `enabled_by_parameter_name` enables this parameter."""
        return self._enabled_by_parameter_values

    @property
    def linked_parameters(self):
        """Represent which parameters in inputs are linked with this parameter."""
        return self._linked_parameters

    @property
    def disabled_by(self):
        """Represent which parameter disables this parameter."""
        return self._disabled_by

    @property
    def module_run_setting_type(self):
        """Represent the parameter type."""
        return self._module_run_setting_type

    @property
    def examples(self):
        """An array of examples of this parameter."""
        return self._examples

    @classmethod
    def from_dto_run_setting_parameter(cls, p: RunSettingParameter):
        """Convert a run setting parameter the ModuleDto from API result to this class."""
        is_compute_target = p.run_setting_ui_hint.ui_widget_type == RunSettingUIWidgetTypeEnum.COMPUTE_SELECTION
        return cls(
            argument_name=p.argument_name,
            name=p.name,
            type=p.parameter_type,
            type_in_py=p.parameter_type_in_py,
            description=p.description,
            optional=p.is_optional, default=p.default_value,
            min=p.lower_bound, max=p.upper_bound,
            is_compute_target=is_compute_target,
            json_editor=p.run_setting_ui_hint.json_editor,
            section_name=p.section_name,
            section_argument_name=p.section_argument_name,
            section_description=p.section_description,
            enum=p.enum_values,
            enabled_by_parameter_name=p.enabled_by_parameter_name,
            enabled_by_parameter_values=p.enabled_by_parameter_values,
            linked_parameters=p.linked_parameter_default_value_mapping,
            disabled_by=p.disabled_by_parameters,
            module_run_setting_type=p.module_run_setting_type,
            examples=p.examples  # TODO: verify when backend supports
        )


class ParamStatus(Enum):
    """Represent current status of RunSettingParameter."""

    Active = 'Active'
    NotEnabled = 'NotEnabled'
    Disabled = 'Disabled'


class RunSettingParam:

    def __init__(self, definition_list: [RunSettingParamDefinition]):
        """
        A wrapper of RunSettingParamDefinition, to support multiple param definitions with the same id.
        For example, `evaluation_interval` in test sweep component is enabled by policy_type, and with
        different default value for different value of policy_type. So MT will return 2 specs for this param,
        we will merge specs here into enabled_by. For most of params, there only one spec in the list.
        `slack_factor` and `slack_amount` are disabled by each other, and they also enabled by policy_type with
        value `bandit`.

        :param definition_list: The param defitions which share the same param id.
        :type definition_list: [RunSettingParamDefinition]
        """
        # Always get the first one, since most params only have one in the list
        # Sweep parameters may have more than one. We will switch to right definition if needed
        self.definition = definition_list[0]
        self.enabled_by = None
        if self.definition.enabled_by_parameter_name is not None:
            # Generate enabled-by mapping in format of {param_name: {param_value: definition}}
            enabled_by_dict = {}
            for definition in definition_list:
                enabled_by_param = definition.enabled_by_parameter_name
                if enabled_by_param not in enabled_by_dict:
                    enabled_by_dict[enabled_by_param] = {}
                for value in definition.enabled_by_parameter_values:
                    enabled_by_dict[enabled_by_param][value] = definition
            self.enabled_by = enabled_by_dict
        self.linked_parameters = next(
            (p.linked_parameters for p in definition_list if p.linked_parameters is not None and
             len(p.linked_parameters) > 0), None)
        self.disabled_by = next(
            (p.disabled_by for p in definition_list if p.disabled_by is not None), None)

    def __getattr__(self, name):
        """For properties not defined in RunSettingParam, retrieve from RunSettingParamDefinition."""
        return getattr(self.definition, name)

    def _switch_definition_by_current_settings(self, settings: dict) -> ParamStatus:
        """
        Switch to the right definition according to current settings for multi-definition parameter.

        :param settings: current runsettings in format of dict.
        :type settings: dict
        :return: parameter status in current settings.
        :rtype: ParamStatus
        """
        # TODO(wanhan): skip this check for definition validation
        if self.enabled_by is not None:
            definition = None
            for param_name in self.enabled_by:
                current_value = settings.get(param_name, None)
                if isinstance(current_value, (PipelineParameter, _ParameterAssignment)):
                    current_value = _get_parameter_static_value(current_value)
                if current_value in self.enabled_by[param_name]:
                    definition = self.enabled_by[param_name][current_value]
                    self.definition = definition
                    break
            if definition is None:
                return ParamStatus.NotEnabled

        # Check disabled by
        if self.disabled_by is not None:
            for name in self.disabled_by:
                current_value = settings.get(name, None)
                if current_value is not None:
                    return ParamStatus.Disabled

        return ParamStatus.Active


class RunSettingsDefinition:
    """This class represent a definition of all run settings which need to be set when run a component."""

    def __init__(self, params: Mapping[str, RunSettingParam]):
        """Initialize a run settings definition with a list of run setting parameters."""
        self._valid_compute_types = []
        self._compute_types_with_settings = [],
        self._compute_params = {}
        self._params = params
        self._algorithm = None
        self._search_space_params = {}
        self._linked_parameters = {}
        # Cache for display info
        self._display_info = None

    @property
    def valid_compute_types(self):
        """This indicates which computes could enable this definition."""
        return self._valid_compute_types

    @property
    def compute_types_with_settings(self):
        """This indicates which computes types have compute runsettings."""
        # For now, ['Cmaks', 'Cmk8s', 'Itp'] have compute runsettings.
        return self._compute_types_with_settings

    @property
    def params(self) -> Mapping[str, RunSettingParam]:
        """The runsetting parameters in dictionary, key is parameter id."""
        return self._params

    @property
    def algorithm(self) -> RunSettingParam:
        return self._algorithm

    @property
    def search_space_params(self) -> Mapping[str, RunSettingParam]:
        """The search space parameters in dictionary, key is parameter id."""
        return self._search_space_params

    @property
    def linked_parameters(self) -> [str]:
        """The linked parameters in inputs for search space."""
        return self._linked_parameters

    @property
    def compute_params(self) -> Mapping[str, RunSettingParam]:
        """The compute parameters in dictionary, key is parameter id."""
        return self._compute_params

    @classmethod
    def from_dto_runsettings(cls, dto_runsettings: Sequence[RunSettingParameter]):
        """Convert run settings parameter in ModuleDto from API result to the definition."""
        # Runsettings parameters
        params = {}
        for p in dto_runsettings:
            if p.id not in params:
                params[p.id] = []
            params[p.id].append(RunSettingParamDefinition.from_dto_run_setting_parameter(p))
        # Sort, and merge specs with same id here
        params = {k: RunSettingParam(v) for k, v in sorted(params.items())}
        # Search space parameters for sweep component
        search_space_params = {k: v for k, v in params.items() if 'sweep.search_space' in k}
        # Filter search space
        params = {k: v for k, v in params.items() if 'sweep.search_space' not in k}
        # Get the algorithm runsetting
        algorithm = next((v for k, v in params.items() if 'sweep.algorithm' in k), None)
        linked_parameters = next(
            (p.linked_parameters.keys() for p in params.values()
             if p.linked_parameters is not None), None)
        result = cls(params=params)
        result._algorithm = algorithm
        result._search_space_params = search_space_params
        result._linked_parameters = linked_parameters
        # Compute runsettings parameters
        valid_compute_types, setting_types, compute_runsettings_params = cls._build_compute_runsettings_parameters(
            dto_runsettings)
        if compute_runsettings_params is not None:
            result._valid_compute_types = valid_compute_types
            result._compute_types_with_settings = setting_types
            result._compute_params = {p.id: RunSettingParam([p]) for p in compute_runsettings_params}
            # Sort by id
            result._compute_params = {k: v for k, v in sorted(result._compute_params.items())}
            # Set valid compute types to compute target param
            target_param = next((p for p in params.values() if p.is_compute_target), None)
            target_param.definition._valid_compute_types = valid_compute_types
        return result

    @classmethod
    def _build_compute_runsettings_parameters(cls, dto_runsettings: Sequence[RunSettingParameter]):
        """Return compute runsettings in format of
        (valid_compute_types, compute_types_have_runsettings, compute_runsettings_parameters)."""
        compute_types , setting_types, compute_params = None, None, None
        # Find out the compute target section.
        target = next((
            p for p in dto_runsettings
            if p.run_setting_ui_hint.ui_widget_type == RunSettingUIWidgetTypeEnum.COMPUTE_SELECTION
        ), None)
        if target is None:
            return compute_types , setting_types, compute_params
        # Compute settings info
        compute_selection = target.run_setting_ui_hint.compute_selection
        # Get valid compute types
        compute_types = compute_selection.compute_types
        # Get compute runsetting parameters
        compute_run_settings_mapping = target.run_setting_ui_hint.compute_selection.compute_run_settings_mapping or {}
        # Get compute types which have compute runsettings
        setting_types = sorted({
            compute_type for compute_type, params in compute_run_settings_mapping.items() if len(params) > 0})
        # Get the first not none compute param list since all computes share the same settings.
        params = [] if len(setting_types) == 0 else compute_run_settings_mapping[next(iter(setting_types))]
        compute_params = [RunSettingParamDefinition.from_dto_run_setting_parameter(p) for p in params]

        return compute_types, setting_types, compute_params

    def _get_display_sections(self, component_type, component_name='component'):
        if self._display_info:
            return self._display_info
        # runsettings
        _runsettings = _RunSettingsParamSection(
            display_name='_runsettings',
            description='Run setting configuration for component [{}]'.format(component_name),
            sub_sections=[],  # Fill later
            parameters=[],  # Fill later
        )
        params = self.params.values()
        # For command, parallel, distributed, hdi components, generate deprecated params for keeping old interfaces
        # We use hard-code here, because new parameters are adding to these components, no need deprecate these,
        # like instance_type, instance_count
        deprecated_params = set()
        from ._component_definition import ComponentType
        if component_type == ComponentType.DistributedComponent:
            deprecated_params = set(_deprecated_params_for_distributed_component)
        elif component_type == ComponentType.ParallelComponent:
            deprecated_params = set(_deprecated_params_for_parallel_component)
        elif component_type == ComponentType.HDInsightComponent:
            deprecated_params = set(_deprecated_params_for_hdinsight_component)

        runsettings_params = []
        # RunSettings sections {section name: section param list}
        runsettings_section_params = {}
        # Section names
        runsettings_sections = {}
        for p in params:
            if p.section_argument_name is None:
                # Parameters for component.runsettings.configure
                runsettings_params.append(_RunSettingsInterfaceParam(
                    p, interface='runsettings.{}'.format(p.argument_name)))
                continue
            # Section params
            section_name = p.section_argument_name
            if section_name not in runsettings_sections:
                runsettings_sections[section_name] = p.section_description
                runsettings_section_params[section_name] = []
            # Append to section params
            interface = 'runsettings.{}.{}'.format(section_name, p.argument_name)
            runsettings_section_params[section_name].append(_RunSettingsInterfaceParam(
                p, interface=interface))
            # Append to params if is deprecated param
            if p.argument_name in deprecated_params:
                old_param = _RunSettingsInterfaceParam(
                    p, interface='runsettings.{}'.format(p.argument_name),
                    deprecated_hint='deprecated, please use {}'.format(interface))
                runsettings_params.append(old_param)
        # Generate section and sub section display objects
        for section_name, section_description in sorted(runsettings_sections.items()):
            sub_section_names = section_name.split('.')
            parent = _runsettings
            for name in sub_section_names:
                section = next((s for s in parent.sub_sections if s.display_name == name), None)
                if section is None:
                    section = _RunSettingsParamSection(display_name=name, description=None, sub_sections=[])
                    parent.sub_sections.append(section)
                parent = section
            parent.description = section_description
            parent.parameters = runsettings_section_params.get(section_name, [])

        _runsettings.parameters = runsettings_params

        # Compute settings
        _compute_runsettings = None
        compute_params = [
            _RunSettingsInterfaceParam(
                p,
                interface='k8srunsettings.{}.{}'.format(p.section_argument_name, p.argument_name),
                is_compute_param=True) for p in self.compute_params.values()]
        if len(compute_params) > 0:
            compute_settings_sections = {
                p.section_argument_name: p.section_description for p in compute_params}
            compute_settings_sub_sections = [
                _RunSettingsParamSection(
                    display_name=section_name,
                    description=section_description,
                    parameters=[p for p in compute_params if p.section_argument_name == section_name],
                ) for section_name, section_description in compute_settings_sections.items()
            ]
            _compute_runsettings = _RunSettingsParamSection(
                display_name='_k8srunsettings',
                description='The compute run settings for Component, only take effect when compute type is in {}.\n'
                            'Configuration sections: {}.'.format(self.compute_types_with_settings,
                                                                 str([s for s in compute_settings_sections])),
                sub_sections=compute_settings_sub_sections,
            )

        self._display_info = _runsettings, _compute_runsettings
        return _runsettings, _compute_runsettings

    @staticmethod
    def _get_pipeline_component_runsettings_parameters(workspace):
        """Get PipelineComponent RunSettings from MT."""
        from azure.ml.component._core._component_definition import ComponentType
        pipeline_component_step_name = ComponentType._get_step_name_mapping()[ComponentType.PipelineComponent]
        runsettings_parameters = _DesignerServiceCallerFactory.get_instance(workspace). \
            get_component_run_setting_parameters_mapping().get(pipeline_component_step_name)
        runsettings_parameters = ModuleDto.correct_run_settings(runsettings_parameters)
        return RunSettingsDefinition.from_dto_runsettings(runsettings_parameters)

    @classmethod
    def build_interface(cls, component, workspace=None):
        """Return the runsettings interface for component in format of (runsettings, compute_runsettings)."""
        workspace = component._workspace or workspace
        _runsettings, _compute_runsettings = None, None
        definition = component._definition
        if definition.runsettings is None:
            # no runsettings definition for condition node
            component_definition_runsettings = RunSettingsDefinition(params={})
        else:
            component_definition_runsettings = definition.runsettings
        _runsettings_display, _compute_runsettings_display = component_definition_runsettings._get_display_sections(
            definition.type, component.display_name)
        _runsettings_store = _RunSettingsStore()
        _compute_runsettings_store = _RunSettingsStore()
        _runsettings = RunSettings(_runsettings_display, _runsettings_store, workspace)
        if _compute_runsettings_display is not None:
            _compute_runsettings = RunSettings(_compute_runsettings_display, _compute_runsettings_store, workspace)
        return _runsettings, _compute_runsettings

    @classmethod
    def build_interface_for_pipeline(cls, pipeline, workspace=None):
        """Return the runsettings interface for component in format of (runsettings, compute_runsettings)."""
        workspace = pipeline._workspace or workspace
        _runsettings = None
        definition = pipeline._definition
        pipeline_definition_runsettings_params = {k: v for k, v in definition.runsettings.params.items()}
        if workspace is not None:
            # update RunSettings with PipelineComponent part
            for k, v in RunSettingsDefinition._get_pipeline_component_runsettings_parameters(workspace).params.items():
                if k in pipeline_definition_runsettings_params:
                    continue
                pipeline_definition_runsettings_params[k] = v
        pipeline_definition_runsettings = RunSettingsDefinition(params=pipeline_definition_runsettings_params)
        definition._runsettings = pipeline_definition_runsettings
        _runsettings_display, __ = pipeline_definition_runsettings._get_display_sections(
            definition.type, pipeline.display_name)
        _runsettings_store = _RunSettingsStore()
        _runsettings = PipelineRunSettings(_runsettings_display, _runsettings_store, workspace)
        return _runsettings
