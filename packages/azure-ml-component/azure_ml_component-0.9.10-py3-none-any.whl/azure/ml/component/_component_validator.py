# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import os
import json
from enum import Enum
from typing import List, Callable, Union
from pathlib import Path

from azure.ml.component._parameter_assignment import _ParameterAssignment
from azure.ml.component._restclients.designer.models import StructuredInterfaceInput
from azure.ml.component._util._cache import DatastoreCache
from azureml.core import Datastore
from azureml.data.datapath import DataPath
from azureml.data.data_reference import DataReference
from azureml.data.dataset_consumption_config import DatasetConsumptionConfig
from azureml.data import TabularDataset, FileDataset
from azureml.exceptions import UserErrorException

from ._core import ComponentType
from ._core._types import _Param, Input
from .run_settings import _RunSettingsInterfaceParam, _get_compute_type
from ._dataset import _FeedDataset
from ._core._run_settings_definition import ParamStatus
from ._restclients.designer.models import StructuredInterfaceParameter, RunSettingParameterType, \
    StructuredInterfaceOutput
from ._restclients.designer.models._designer_service_client_enums import ParameterType
from ._module_dto import _type_code_to_python_type_name, IGNORE_PARAMS
from ._pipeline_parameters import PipelineParameter
from ._util._attr_dict import _AttrDict
from ._util._exceptions import ComponentValidationError
from ._util._utils import _get_name_in_mapping, _get_parameter_static_value, is_float_convertible, \
    is_bool_string, is_int_convertible, \
    _dumps_raw_json, basic_python_type, _is_json_string_convertible, is_hyper_parameter, _obj_in_list


class JsonSchemaType(str, Enum):
    object = "object"
    array = "array"
    string = "string"


class ComponentValidator(object):

    @staticmethod
    def validate_component_inputs(
            workspace, provided_inputs,
            interface_inputs, param_python_name_dict, process_error, definition_validator=None,
            is_local=False, for_definition_validate=False, pipeline_parameters=None,
            component_type=None):
        """
        It will verify required input is provided and whether input type is valid.
        Current support input types are DataReference, Dataset, DataPath, DatasetConsumptionConfig and Output.
        If is_local is True, tabular dataset is not support and it will support str and Path as input type and
        verify input path exists.
        If for_definition_validate is True, it validating pipeline definition and won't check input value.

        :param workspace: Component workspace
        :type workspace: azureml.core.Workspace
        :param provided_inputs: Inputs to be verified
        :type provided_inputs: dict[str, Input]
        :param interface_inputs: Input interface info
        :type interface_inputs: List[StructuredInterfaceInput]
        :param param_python_name_dict: Map of input name and python name
        :type param_python_name_dict: dict[str, str]
        :param process_error: Function to handle invalid situation
        :type process_error: Callable
        :param definition_validator: definition validator
        :type definition_validator: azure.ml.component._component_validator.DefinitionValidator
        :param is_local: Whether the validation is for local run in the host, false if it is for remote run in AzureML.
        :type is_local: bool
        :param for_definition_validate: If the validate is for pipeline definition validate.
        :type for_definition_validate: bool
        :param pipeline_parameters: Pipeline parameters in current validating layer
        :type pipeline_parameters: dict[str, Union[Input, PipelineParameters]]
        :param component_type: current component type
        :type component_type: str
        """
        if pipeline_parameters is None:
            pipeline_parameters = {}

        def process_input_error(e: Exception, error_type, input_name):
            process_error(e, error_type, input_name, VariableType.Input)

        def process_pipeline_param_error(e: Exception, error_type, input_name, pipeline_param=None):
            process_error(e, error_type, input_name, VariableType.Input, pipeline_param=pipeline_param)

        def is_pipeline_parameter(input):
            """All inputs for component are wrapped with Input/PipelineParameter, so we check if a input is pipeline
            parameter by checking if it's in pipeline parameter dict.
            """
            return _obj_in_list(input, pipeline_parameters.values())

        from .component import Input
        for _input in interface_inputs:
            formatted_input_name = \
                _get_name_in_mapping(_input.name, param_python_name_dict)
            provided_input_value = provided_inputs.get(formatted_input_name, None)

            is_pipeline_param = is_pipeline_parameter(provided_input_value)

            if is_pipeline_param and for_definition_validate and definition_validator:
                if len(_input.data_type_ids_list) == 0:
                    expected_type = None
                else:
                    expected_type = _input.data_type_ids_list
                definition_validator.validate_pipeline_parameter(
                    provided_input_value,
                    _input,
                    formatted_input_name,
                    expected_type,
                    process_pipeline_param_error,
                    component_type
                )

            # 1. extract pipeline parameter from input
            if isinstance(provided_input_value, Input):
                provided_input_value = provided_input_value._get_internal_data_source()
            # 2. extract default value from pipeline parameter
            if isinstance(provided_input_value, PipelineParameter):
                # for pipeline parameter, if default value provided, validate default value
                provided_input_value = provided_input_value.default_value

            if provided_input_value is not None:
                ComponentValidator._validate_input_port_type(
                    _input.name, provided_input_value, process_input_error, is_local)
                # Workspace will be none when component is not registered
                if workspace:
                    ComponentValidator._validate_input_dataset_workspace(_input.name, provided_input_value,
                                                                         process_input_error, workspace)
            elif not _input.is_optional:
                if is_pipeline_param and for_definition_validate:
                    # skip input None check for pipeline parameter in definition validate because
                    # the value is not available then
                    continue
                process_input_error(ValueError("Required input '%s' not provided." % formatted_input_name),
                                    ComponentValidationError.MISSING_INPUT, _input.name)

    @staticmethod
    def _validate_input_port_type(input_name, dset, process_error, is_local=False):
        """
        Validate input port type, if is_local=True, TabularDatset is not support and support str and Path as input.

        :param input_name: Input name
        :type input_name: str
        :param dset: Validate input dataset
        :type dset: object
        :param process_error: Function to handle invalid situation
        :type process_error: Callable
        :param is_local: Whether the validation is for local run, false if it is for remote run.
        :type is_local: bool
        """
        from .component import Output
        if isinstance(dset, DatasetConsumptionConfig):
            dset = dset.dataset
        # DataReference, Output, DataPath, FileDataset all work in local and in remote
        if isinstance(dset, (DataReference, Output, DataPath, FileDataset, _FeedDataset)):
            return
        if is_local:
            # Except for types both supported, local also support local path
            is_local_dataset = isinstance(dset, str) or isinstance(dset, Path)
            if is_local_dataset and not os.path.exists(dset):
                process_error(ValueError("Not found input '%s' path '%s' in local." % (input_name, dset)),
                              ComponentValidationError.INVALID_INPUT, input_name)
            if not is_local_dataset:
                process_error(ValueError("Input port '{0}' type is invalid for local run, expected type: "
                                         "'str, Path, DataReference, Output, DataPath, FileDataset', got '{1}'.".
                                         format(input_name, type(dset))),
                              ComponentValidationError.INVALID_INPUT, input_name)
        else:
            # Except for types both supported, remote also support tabular dataset
            if not isinstance(dset, TabularDataset):
                process_error(ValueError("Input port '{0}' type is invalid for remote execution, expected type: "
                                         "'DataReference, Output, DataPath, FileDataset, TabularDataset', got '{1}'.".
                                         format(input_name, type(dset))),
                              ComponentValidationError.INVALID_INPUT, input_name)

    @staticmethod
    def _validate_input_dataset_workspace(input_name, dset, process_error, workspace):
        """
        Validate input port workspace is same as component workspace.

        :param input_name: Input name
        :type input_name: str
        :param dset: Validate input dataset
        :type dset: object
        :param process_error: Function to handle invalid situation
        :type process_error: Callable
        :param workspace: Component workspace
        :type workspace: azureml.core.Workspace
        """
        from .component import Output
        if isinstance(dset, (str, Path, Output)):
            # Not validate local dataset.
            return
        if isinstance(dset, DatasetConsumptionConfig):
            dset = dset.dataset
        if isinstance(dset, DataReference) and hasattr(dset.datastore, "workspace"):
            workspace_id = dset.datastore.workspace._workspace_id
        elif isinstance(dset, DataPath) and hasattr(dset._datastore, "workspace"):
            workspace_id = dset._datastore.workspace._workspace_id
        elif (isinstance(dset, FileDataset) or isinstance(dset, TabularDataset)) and hasattr(
                dset, "_registration") and hasattr(dset._registration, "workspace"):
            workspace_id = dset._registration.workspace._workspace_id
        else:
            workspace_id = None
        # skip check for un-registered dataset
        if workspace_id and workspace_id != workspace._workspace_id:
            process_error(ValueError("Input port '{0}' dataset workspace is different from component workspace, "
                                     "expected workspace is subscription_id='{1}', resource_group='{2}', name='{3}'.".
                                     format(input_name, workspace.subscription_id,
                                            workspace.resource_group, workspace.name)),
                          ComponentValidationError.INVALID_INPUT, input_name)

    @staticmethod
    def validate_component_parameters(
            provided_parameters,
            interface_parameters,
            param_python_name_dict,
            process_error,
            definition_validator=None,
            for_definition_validate=False,
            component_type=None
    ):
        """It will verify required provided is provided and whether parameter type is valid.
        If for_definition_validate is True, it validating pipeline definition and won't check input value.

        :param provided_parameters: Parameters to be verified
        :type provided_parameters: dict[str, Parameter]
        :param interface_parameters: Parameter interface info
        :type interface_parameters: List[StructuredInterfaceParameter]
        :param param_python_name_dict: Map of input name and python name
        :type param_python_name_dict: dict[str, str]
        :param process_error: Function to handle invalid situation
        :type process_error: Callable
        :param definition_validator: definition validator
        :type definition_validator: azure.ml.component._component_validator.DefinitionValidator
        :param for_definition_validate: if the validate is for pipeline definition validate.
        :type for_definition_validate: bool
        :param component_type: indicate current component type.
        :type component_type: string
        """

        def process_parameter_error(e: Exception, error_type, parameter_name):
            process_error(e, error_type, parameter_name, VariableType.Parameter)

        def process_pipeline_param_error(e: Exception, error_type, parameter_name, pipeline_param=None):
            process_error(e, error_type, parameter_name, VariableType.Parameter, pipeline_param=pipeline_param)

        def type_mismatch(parameter_name, _type, param_value):
            type_string_mismatch(parameter_name, _type, type(param_value))

        def type_string_mismatch(parameter_name, expected_type, actual_type):
            process_parameter_error(ValueError("Parameter '{0}' type mismatched, expected type: '{1}', got '{2}'.".
                                               format(parameter_name, expected_type, actual_type)),
                                    ComponentValidationError.PARAMETER_TYPE_MISMATCH, parameter_name)

        def validate_numeric_parameter(parameter_name, _type, param_value):
            # Try to convert string parameter to int/float
            if isinstance(param_value, str) and parameter_type == ParameterType.INT.value \
                    and is_int_convertible(param_value):
                param_value = int(param_value)
            if isinstance(param_value, str) and parameter_type == ParameterType.DOUBLE.value \
                    and is_float_convertible(param_value):
                param_value = float(param_value)
            if isinstance(param_value, bool):
                type_mismatch(parameter_name, _type, param_value)
                return
            # Don't allow other types when int is required
            if parameter_type == ParameterType.INT.value and not isinstance(param_value, int):
                type_mismatch(parameter_name, _type, param_value)
                return
            # Allow int and float when float is required
            if parameter_type == ParameterType.DOUBLE.value and \
                    not (isinstance(param_value, int) or isinstance(param_value, float)):
                type_mismatch(parameter_name, _type, param_value)
                return

            lower_bound = parameter.lower_bound
            if lower_bound is not None and param_value < float(lower_bound):
                process_parameter_error(ValueError("Parameter '%s' range is invalid. " % parameter_name +
                                                   "Lower bound is %s, got %s." % (lower_bound, param_value)),
                                        ComponentValidationError.INVALID_PARAMETER, parameter_name)
            upper_bound = parameter.upper_bound
            if upper_bound is not None and param_value > float(upper_bound):
                process_parameter_error(ValueError("Parameter '%s' range is invalid. " % parameter_name +
                                                   "Upper bound is %s, got %s." % (upper_bound, param_value)),
                                        ComponentValidationError.INVALID_PARAMETER, parameter_name)

        def validate_enum_values_parameter(parameter_name, _type, param_value):
            enum_values = parameter.enum_values
            # Allow pass not str Enum parameter
            if enum_values and not isinstance(param_value, str):
                param_value = str(param_value)
            if not isinstance(param_value, str):
                type_mismatch(parameter_name, _type, param_value)
                return
            if enum_values and param_value not in enum_values:
                process_parameter_error(ValueError("Parameter '%s' is invalid. " % parameter_name +
                                                   "Options are %s, got '%s'." % (str(enum_values), param_value)),
                                        ComponentValidationError.INVALID_PARAMETER, parameter_name)

        def validate_output_values_parameter(parameter_name, _type, param_value):
            outputs = param_value._owner._definition.outputs
            output_def = outputs.get(param_value._name)
            if not output_def:
                raise UserErrorException(
                    f'Output {param_value._name!r} not found in outputs of component {param_value._owner.name!r}, '
                    f'found {list(outputs.keys())}.')
            output_python_type_string = _Param.parse_param_type_string(output_def.type)
            if _type != output_python_type_string:
                type_string_mismatch(parameter_name, _type, output_python_type_string)

        def _is_conditional_optional(parameter, provided_parameters):
            # this is to support build-in components' conditional required parameter
            # e.g. 'Split Data' has parameter named 'Stratification Key Column' which is configured
            # to be enabled by parameter 'Stratified split' with value set ['True']
            # so if parameter 'Stratified split' is provided with value equals to 'True'
            # we should consider 'Stratification Key Column' as a required parameter, otherwise as optional
            if parameter.enabled_by_parameter_name is None or parameter.enabled_by_parameter_values is None:
                return parameter.is_optional

            enabled_by = parameter.enabled_by_parameter_name
            enabled_by_values = parameter.enabled_by_parameter_values
            provided_value = provided_parameters.get(
                _get_name_in_mapping(enabled_by, param_python_name_dict), None)
            return not _obj_in_list(provided_value, enabled_by_values)

        # Validate params
        for parameter in interface_parameters:
            if parameter.name in IGNORE_PARAMS:
                continue

            formatted_parameter_name = \
                _get_name_in_mapping(parameter.name, param_python_name_dict)
            provided_param_value = provided_parameters.get(formatted_parameter_name, None)
            if is_hyper_parameter(provided_param_value):
                # Skip validation if provided parameter looks like hyper parameter.
                continue
            is_parameter_optional = _is_conditional_optional(parameter, provided_parameters)
            if (provided_param_value is None) or (
                    parameter.parameter_type == ParameterType.STRING and type(provided_param_value) is str
                    and provided_param_value == ''):
                if not is_parameter_optional:
                    process_parameter_error(
                        ValueError("Required parameter '%s' not provided." % formatted_parameter_name),
                        ComponentValidationError.MISSING_PARAMETER,
                        formatted_parameter_name)
                continue
            else:
                parameter_type = parameter.parameter_type
                required_parameter_type = _type_code_to_python_type_name(parameter_type)

                # Only validate type for definition validate
                if for_definition_validate:
                    # if provided param is pipeline parameter, only check meta
                    if isinstance(provided_param_value, PipelineParameter):
                        definition_validator.validate_pipeline_parameter(
                            provided_param_value, parameter, formatted_parameter_name, required_parameter_type,
                            process_pipeline_param_error, component_type
                        )
                        continue

                    # if provided param is parameter assignment, only check meta
                    if isinstance(provided_param_value, _ParameterAssignment):
                        definition_validator.validate_parameter_assignment(
                            provided_param_value, parameter, formatted_parameter_name, required_parameter_type,
                            process_parameter_error, component_type
                        )
                        continue

                    # When required parameter type is unknown, skip it's validation
                    if required_parameter_type is None:
                        continue

                # Validate value otherwise
                provided_param_value = _get_parameter_static_value(provided_param_value)
                if is_parameter_optional and provided_param_value is None:
                    continue

                from .component import Output
                # pipeline's parameter not support output as value.
                # only parameter port or component parameter is supported.
                # Banned case: param is output, assigned param is sub pipeline parameter
                # @dsl.pipeline()
                # def sub_pipeline_func(param: str):  # assigned param: not a port
                #     ...
                # @dsl.pipeline()
                # def pipeline_func():
                #     node = component_func()
                #     sub_pipeline_func(param=node.outputs.output)
                if isinstance(provided_param_value, Output) and \
                        component_type != ComponentType.PipelineComponent.value:
                    # Only check if the output definition type matches required type.
                    validate_output_values_parameter(
                        formatted_parameter_name, required_parameter_type, provided_param_value)
                    continue
                if parameter_type in [ParameterType.INT, ParameterType.DOUBLE]:
                    validate_numeric_parameter(formatted_parameter_name, required_parameter_type, provided_param_value)
                elif parameter_type == ParameterType.BOOL:
                    if not (isinstance(provided_param_value, bool) or is_bool_string(provided_param_value)):
                        type_mismatch(formatted_parameter_name, required_parameter_type, provided_param_value)
                elif parameter_type == ParameterType.STRING:
                    validate_enum_values_parameter(formatted_parameter_name, required_parameter_type,
                                                   provided_param_value)

    @staticmethod
    def validate_compatibility(old_component, new_component):
        """
        provided for replace a component in pipeline
        compare ports and params
        """
        errors = []
        ComponentValidator._validate_ports(old_component, new_component, errors)
        ComponentValidator._validate_parameters(old_component._interface_parameters,
                                                new_component._interface_parameters,
                                                errors)
        return errors

    @staticmethod
    def _validate_ports(old_component, new_component, errors: List):
        """
        validate input and output ports defined in component
        both name and mode, allow additional
        """

        def _input_provided(component, port_name: str):
            provided_inputs = component._input_ports
            formatted_input_name = _get_name_in_mapping(port_name,
                                                        component._module_dto.module_python_interface
                                                        .inputs_name_mapping)
            provided_input_value = provided_inputs.get(formatted_input_name, None)
            return provided_input_value is not None

        def _check_missing(ptype: str, old_ports: dict, new_ports: dict, errors: List):
            missing_ports = list(old_ports.keys() - new_ports.keys())
            if len(missing_ports) != 0:
                errors.append("Missing {0} ports in new component function, expected {1}, but not found.".
                              format(ptype, missing_ports))
            # only check inputs now
            if ptype == 'Output':
                return
            mismatched_ports = [[k, v.data_type_ids_list, new_ports[k].data_type_ids_list]
                                for k, v in old_ports.items() if k in new_ports.keys() and
                                _input_provided(old_component, k) and
                                len(set(v.data_type_ids_list) - set(new_ports[k].data_type_ids_list)) > 0]
            # flatten mismatched ports
            mismatched_ports = [mismatched_ports[i][j] for i in range(len(mismatched_ports))
                                for j in range(len(mismatched_ports[i]))]
            if len(mismatched_ports) != 0:
                errors.append("{0} ports '{1}' data type mismatched, expected type: '{2}', got '{3}'.".
                              format(ptype, mismatched_ports[0::3], mismatched_ports[1::3],
                                     mismatched_ports[2::3]))
            # check if required port added
            required_ports = {p.name: p.data_type_ids_list for p in new_ports.values()
                              if p.name not in old_ports.keys() and not p.is_optional}
            if len(required_ports) != 0:
                errors.append("New required ports {0} added in new component function, type {1}".
                              format(required_ports.keys(), required_ports.values()))

        old_inputs = {i.name: i for i in old_component._interface_inputs}
        new_inputs = {i.name: i for i in new_component._interface_inputs}
        _check_missing("Input", old_inputs, new_inputs, errors)

        old_outputs = {i.name: i for i in old_component._interface_outputs}
        new_outputs = {i.name: i for i in new_component._interface_outputs}
        _check_missing("Output", old_outputs, new_outputs, errors)
        return errors

    @staticmethod
    def _validate_parameters(old_params, new_params: List[StructuredInterfaceParameter],
                             errors: List):
        """
        validate parameters defined in component with new component's params
        type of interface parameter definition:  List[StructuredInterfaceParameter]

        only compare name and type now, allow additional params
        """
        old_param_dict = {p.name: p.parameter_type for p in old_params}
        new_param_dict = {p.name: p.parameter_type for p in new_params}

        if old_param_dict == new_param_dict:
            return
        # missing params: new function does not contains parameters in the old one
        # check at first to show more clear error message
        missing_params = {p.name: _type_code_to_python_type_name(p.parameter_type)
                          for p in old_params if p.name not in new_param_dict.keys()}
        if len(missing_params) != 0:
            errors.append("Missing parameter in new component function, expected: {0}, but not found.".
                          format(missing_params))

        # mismatched params: new function has some parameters that type mismatched with the old one
        # looks like this: [['name', 'str', 'int'][..]..]
        # the 2nd is type expected and the 3rd is type real
        mismatched_params = [[k, _type_code_to_python_type_name(v),
                              _type_code_to_python_type_name(new_param_dict[k])]
                             for k, v in old_param_dict.items() if k in new_param_dict.keys() and
                             v != new_param_dict[k]]
        # flatten mismatched params
        mismatched_params = [mismatched_params[i][j] for i in range(len(mismatched_params))
                             for j in range(len(mismatched_params[i]))]
        if len(mismatched_params) != 0:
            errors.append("Parameter '{0}' type mismatched, expected type: '{1}', got '{2}'.".
                          format(mismatched_params[0::3], mismatched_params[1::3],
                                 mismatched_params[2::3]))
        # check if new component includes required params which not exists in old component
        required_params = {p.name: _type_code_to_python_type_name(p.parameter_type) for p in new_params
                           if p.name not in old_param_dict.keys() and not p.is_optional}
        if len(required_params) != 0:
            errors.append("No such required params {0} provided in old component, type: {1}.".
                          format(required_params.keys(), required_params.values()))

    @staticmethod
    def _get_runsetting_advanced_validator_by_type(spec):
        validators = []
        # Validator by parameter type
        parameter_type = spec.parameter_type
        if parameter_type == RunSettingParameterType.INT or parameter_type == RunSettingParameterType.DOUBLE:
            validators.append(ComponentValidator._validate_numeric_runsetting_parameter)
        elif parameter_type == RunSettingParameterType.JSON_STRING:
            validators.append(ComponentValidator._validate_json_string_runsetting_parameter)
        elif spec.enum is not None:  # parameter_type is string
            # Enum validator
            validators.append(ComponentValidator._validate_mode_runsetting_parameter)
        return validators

    @staticmethod
    def _validate_compute_type(component, compute_name, compute_type, workspace, process_error):
        # For pipeline component, there's no run settings
        if hasattr(component, "runsettings"):
            spec = next((
                spec for spec in component.runsettings._params_mapping.values() if spec.is_compute_target), None)
        else:
            spec = None
        # Skip target selector type validation
        if spec is None or compute_name == component.runsettings._TARGET_SELECTOR_NAME:
            return
        if compute_type is None:
            compute_type = _get_compute_type(workspace, compute_name)
        if compute_type and compute_type not in spec.valid_compute_types:
            # Validate compute type
            process_error(
                ValueError("Compute '{}' with type '{}' is invalid for current component.".format(
                    compute_name, compute_type)),
                ComponentValidationError.INVALID_RUNSETTING_PARAMETER, spec.interface, VariableType.Runsetting)

    @staticmethod
    def _validate_compute_on_component(component, default_compute, workspace, process_error,
                                       pipeline_parameters={}):
        if hasattr(component, "runsettings"):
            # Only validate component has compute or not in this function.
            # Compute value in runsettings will be validate in _validate_compute_target as above.
            if not hasattr(component.runsettings, 'target') or workspace is None:
                return
            target_definition = next((
                v for v in component.runsettings._params_mapping.values() if v.is_compute_target), None)
            # Pipeline component target is optional.
            if not target_definition or target_definition.is_optional:
                return
            # Get target/target_selector name in component runsettings.
            compute_name = component.runsettings._get_target()
        else:
            compute_name = None
        compute_type = None
        if isinstance(compute_name, tuple):
            compute_name, compute_type = compute_name
        if compute_name is None:
            # If no target/target_selector specified on component, try resolve component compute.
            # Resolve valid compute(include pipeline's) by calling component._compute.
            # _compute return compute_name, compute_type, use_pipeline_default_compute.
            compute_name, compute_type, _ = component._resolve_compute(
                pipeline_parameters=pipeline_parameters, workspace=workspace)
        if compute_name is None:
            # Fall back to parent target
            if component._parent:
                compute_name = component._parent.runsettings.target
            # Fall back to default compute
            compute_name = compute_name if compute_name else default_compute
            if isinstance(default_compute, tuple):
                compute_name, compute_type = default_compute
        if compute_name is None:
            process_error(
                ValueError("Compute target for current component not specified."),
                ComponentValidationError.COMPUTE_TARGET_NOT_SPECIFIED, None, VariableType.Runsetting)
        else:
            ComponentValidator._validate_compute_type(
                component, compute_name, compute_type, workspace, process_error)

    @staticmethod
    def validate_runsetting_parameter(
            all_settings: dict,
            spec: _RunSettingsInterfaceParam,
            process_error,
            for_definition_validate=False,
            definition_validator=None,
            component_type=None
    ):

        def process_runsetting_error(e: Exception, error_type, runsetting_param_name):
            process_error(e, error_type, runsetting_param_name, VariableType.Runsetting)

        def process_pipeline_param_error(e: Exception, error_type, param_name, pipeline_param=None):
            process_error(e, error_type, param_name, VariableType.Runsetting, pipeline_param=pipeline_param)

        if spec.deprecated_hint is not None:
            # By pass deprecated interfaces
            return

        param = all_settings.get(spec.id)
        if for_definition_validate and isinstance(param, (PipelineParameter, _ParameterAssignment)):
            # For pipeline parameter in definition validation, won't extract real value
            # replace pipeline parameters inside run settings with original ones
            param_value = definition_validator.get_original_object_for_parameter(param)
        else:
            # Extract the real value for validation
            param_value = _get_parameter_static_value(param)

        from .component import Output
        if isinstance(param, Output):
            process_runsetting_error(ValueError(
                f'{type(param)} is not supported used as component runsettings. (name: {spec.interface})'
            ), ComponentValidationError.INVALID_RUNSETTING_PARAMETER, spec.interface)
            return

        status = spec._switch_definition_by_current_settings(all_settings)
        # skip enabled by check for definition validate, because we can not get actual value then
        if status == ParamStatus.NotEnabled and param_value is not None and not for_definition_validate:
            enabled_by_msg_items = []
            for name, values in spec.enabled_by.items():
                values = list(values)
                if len(values) > 1:
                    enabled_by_msg_items.append("'{}' in {}".format(name, values))
                else:
                    enabled_by_msg_items.append("'{}' to '{}'".format(name, values[0]))
            enabled_by_msg = ', or '.join(enabled_by_msg_items)
            process_runsetting_error(ValueError(
                "'{}' is not enabled in current runsettings. To enable it, please set {}.".format(
                    spec.interface, enabled_by_msg)),
                ComponentValidationError.INVALID_RUNSETTING_PARAMETER, spec.interface)
            return
        if status == ParamStatus.Disabled and param_value is not None:
            process_runsetting_error(ValueError(
                "'{}' is not enabled in current runsettings. To enable it, please set {} to None.".format(
                    spec.interface, spec.disabled_by)),
                ComponentValidationError.INVALID_RUNSETTING_PARAMETER, spec.interface)
            return

        # For any runsetting, active or disabled, we will link it to pipeline parameters to mark the parameter used
        # This will cause problem when a runsetting is disabled by some value passing in runtime, no validation error
        # will happen
        if for_definition_validate:
            if isinstance(param_value, PipelineParameter):
                definition_validator.validate_pipeline_parameter(
                    param_value,
                    spec.definition.definition,
                    spec.interface,
                    spec.parameter_type_in_py.__name__,
                    process_pipeline_param_error,
                    component_type
                )
                return
            elif isinstance(param_value, _ParameterAssignment):
                definition_validator.validate_parameter_assignment(
                    param_value,
                    spec.definition.definition,
                    spec.interface,
                    spec.parameter_type_in_py.__name__,
                    process_runsetting_error,
                    component_type
                )
                return

        if status == ParamStatus.Active:
            ComponentValidator._validate_runsetting_parameter(param_value, spec, process_runsetting_error)

    @staticmethod
    def _validate_runsetting_parameter(param_value, spec: _RunSettingsInterfaceParam, process_error):
        """Note, workspace cannot be None if skip_compute_validation is False."""
        if param_value is None:
            # Required parameter validation
            # But we skip validation for 'target' here, it can be None if pipeline has a default compute target
            # And we also skip this for deprecated param
            if not spec.is_optional and not spec.is_compute_target and spec.deprecated_hint is None:
                process_error(ValueError("Required parameter '%s' not provided." % spec.interface),
                              ComponentValidationError.MISSING_RUNSETTING_PARAMETER, spec.interface)
            return

        if spec.is_compute_target:
            # Compute target will be validate after runsettings validation
            return

        if spec.parameter_type != RunSettingParameterType.JSON_STRING and \
                not isinstance(param_value, spec.parameter_type_in_py):
            process_error(ValueError("Parameter '{0}' type mismatched, expected type: '{1}', got '{2}'.".
                                     format(spec.interface, spec.parameter_type_in_py.__name__,
                                            type(param_value).__name__)),
                          ComponentValidationError.INVALID_RUNSETTING_PARAMETER, spec.interface)
            return

        # Value validation
        advanced_validators = ComponentValidator._get_runsetting_advanced_validator_by_type(spec)
        for validator in advanced_validators:
            validator(spec.interface, param_value, spec, process_error)

    @staticmethod
    def _validate_numeric_runsetting_parameter(param_hint_name, param_value, spec, process_error):
        upper_bound = spec.parameter_type_in_py(spec.upper_bound) if spec.upper_bound is not None else None
        lower_bound = spec.parameter_type_in_py(spec.lower_bound) if spec.lower_bound is not None else None
        if upper_bound is not None and param_value > upper_bound:
            process_error(ValueError("Parameter '%s' is invalid, which should '<= %s', "
                                     % (param_hint_name, upper_bound) +
                                     "got '%s'" % param_value),
                          ComponentValidationError.INVALID_RUNSETTING_PARAMETER, param_hint_name)
        if lower_bound is not None and param_value < lower_bound:
            process_error(ValueError("Parameter '%s' is invalid, which should '>= %s', "
                                     % (param_hint_name, lower_bound) +
                                     "got '%s'" % param_value),
                          ComponentValidationError.INVALID_RUNSETTING_PARAMETER, param_hint_name)

    @staticmethod
    def _validate_json_string_runsetting_parameter(param_hint_name, param_value, spec, process_error):
        # get json_schema type
        json_schema_type = spec.json_schema.get("type") if spec.json_schema else None
        expected_type_name = "serializable JSON"
        if json_schema_type == JsonSchemaType.object:
            expected_type_name = "'dict'"
        elif json_schema_type == JsonSchemaType.array:
            expected_type_name = "'list' or 'tuple'"

        # serializable object or json string
        is_valid_value = _is_json_string_convertible(param_value) \
            if isinstance(param_value, str) else _dumps_raw_json(param_value)
        if not is_valid_value:
            process_error(ValueError(
                "Parameter '%s' with type '%s' is invalid, which is not JSON serializable, expected type: "
                "%s object or JSON string" % (spec.interface, type(param_value).__name__, expected_type_name)),
                ComponentValidationError.INVALID_RUNSETTING_PARAMETER, spec.interface)
            return

        def _validate_inner_object_type(inner_values):
            additional_prop = spec.json_schema.get("additionalProperties", None)
            value_type = additional_prop.get("type") if additional_prop else None
            # Check if dict value type is string.
            if value_type == JsonSchemaType.string:
                # Extract value if value type is Enum.
                param_values = [v.value if isinstance(v, Enum) else v for v in inner_values]
                error_type = [type(v).__name__ for v in param_values if type(v) not in basic_python_type]
                if len(error_type) > 0:
                    process_error(ValueError(
                        "Parameter type mismatched '%s', expected type: "
                        "%s with value type 'str', actually value type '%s'." % (
                            spec.interface, expected_type_name, "', '".join(error_type))),
                        ComponentValidationError.INVALID_RUNSETTING_PARAMETER, spec.interface)

        # load object if value is str
        param_value = json.loads(param_value) if isinstance(param_value, str) else param_value
        # Dictionary json type validation
        if json_schema_type == JsonSchemaType.object:
            if not isinstance(param_value, dict):
                process_error(ValueError("Parameter '{0}' type mismatched, expected type: 'dict', got '{1}'.".
                                         format(spec.interface, type(param_value).__name__)),
                              ComponentValidationError.INVALID_RUNSETTING_PARAMETER, spec.interface)
            else:
                _validate_inner_object_type(param_value.values())

        # List json type validation
        elif json_schema_type == JsonSchemaType.array:
            if not (isinstance(param_value, list) or isinstance(param_value, tuple)):
                process_error(ValueError("Parameter '{0}' type mismatched, expected type: 'list' or 'tuple', "
                                         "got '{1}'.".format(spec.interface, type(param_value).__name__)),
                              ComponentValidationError.INVALID_RUNSETTING_PARAMETER, spec.interface)
            else:
                _validate_inner_object_type(param_value)
        else:
            pass  # skip param_value type check if json_schema type is not given

    @staticmethod
    def _validate_mode_runsetting_parameter(param_hint_name, param_value, spec, process_error):
        enum_values = spec.enum
        if param_value not in enum_values:
            process_error(ValueError("Parameter '%s' is invalid, " % param_hint_name +
                                     "the value should in {}".format(enum_values)),
                          ComponentValidationError.INVALID_RUNSETTING_PARAMETER, spec.interface)

    @staticmethod
    def _validate_datastore(component_type: str,
                            output_interfaces: List[StructuredInterfaceOutput],
                            output_ports: _AttrDict,
                            process_error,
                            default_datastore=None,
                            param_python_name_dict=None,
                            workspace=None,
                            ):
        """
        Validate data store settings for specific component's output ports.
        Currently, only valid the CosmosStructureStream port for ScopeComponent.

        :param component_type: Component type of the component to be validated
        :type component_type: str
        :param output_interfaces: Output interface definition for the component
        :type output_interfaces: list of StructuredInterfaceOutput
        :param output_ports: Outputs for the component
        :type output_ports: _AttrDict
        :param process_error: Function to handle invalid situation
        :type process_error: Callable
        :param param_python_name_dict: Map of input name and python name
        :type param_python_name_dict: dict[str, str]
        :param workspace: Workspace used to get datastore
        :type workspace: azureml.core.Workspace
        """
        from azure.ml.component._core._component_definition import ComponentType
        from azureml.data.azure_data_lake_datastore import AzureDataLakeDatastore

        # make sure datastore exists in workspace, raise exception if not non and not exist
        def ensure_datastore_exist(_datastore: Union[str, Datastore]) -> Union[None, Datastore]:
            if isinstance(_datastore, str):
                if not workspace:
                    raise UserErrorException('Missing workspace for workspace independent component.')
                cached_datastore = DatastoreCache.get_item(workspace, _datastore)
                if not cached_datastore:
                    process_error(
                        ValueError("Configured datastore '{}' does not exist in workspace.".format(_datastore)),
                        ComponentValidationError.DATASTORE_NOT_EXIST, _datastore, VariableType.Runsetting)
                return cached_datastore
            return _datastore

        default_datastore = ensure_datastore_exist(default_datastore)
        # for all component types, validate if the configured datastore name is right
        for output in output_interfaces:
            if component_type == ComponentType.PipelineComponent.value:
                # For PipelineComponent, use output_ports key name to match since sub pipeline may rename outputs
                port = next((o for n, o in output_ports.items() if n == output.name), None)
            else:
                port = next((o for o in output_ports.values() if o.port_name == output.name), None)
            if port is None:
                continue
            ensure_datastore_exist(port.datastore)

        if component_type == ComponentType.ScopeComponent.value:
            # For ScopeComponent, if the output type is CosmosStructureStream,
            # then it's datastore should be AzureDataLakeDatastore
            for output in output_interfaces:
                # For scope we need to get the correct output name from dict
                output_name = _get_name_in_mapping(output.name, param_python_name_dict)
                port = output_ports.get(output_name, None)
                if port is None:
                    continue
                datastore = ensure_datastore_exist(port.datastore) or default_datastore
                datastore_name = datastore.name if datastore is not None else None
                if not isinstance(datastore, AzureDataLakeDatastore):
                    process_error(
                        TypeError(
                            'The datastore:{} of type:{} is not valid for output:{}.'
                            .format(datastore_name, type(datastore), output_name) +
                            'Because the ScopeComponent only supports AzureDataLakeDatastore.'),
                        ComponentValidationError.INVALID_DATASTORE_TYPE, datastore_name, VariableType.Runsetting)

    @staticmethod
    def _validate_local_run_component_type(component, process_error):
        """
        Validate component type is supported for local run.
        Currently, local run supports CommandComponent, ParallelComponent and MPI launcher of DistributeComponent.

        :param component: Local run component
        :type component: Component
        :param process_error: Function to handle invalid situation
        :type process_error: Callable
        """
        from azure.ml.component._core._component_definition import ComponentType
        from azure.ml.component._core._launcher_definition import LauncherType

        if component._definition.type in [ComponentType.CommandComponent, ComponentType.ParallelComponent,
                                          ComponentType.PipelineComponent]:
            return
        elif component._definition.type == ComponentType.DistributedComponent:
            if component._definition.launcher.type == LauncherType.MPI:
                return
            else:
                msg = "Launcher type '%r' of distributed component is not supported for local run." % \
                      component._definition.launcher.type
        else:
            msg = "Component type '%s' is not supported for local run." % component._definition.type
        process_error(NotImplementedError(msg), ComponentValidationError.NOT_IMPLEMENTED_ERROR, None, None)

    @staticmethod
    def validate_output(
            workspace, provided_outputs, output_interfaces, process_error, definition_validator=None,
            is_local=False, for_definition_validate=False, pipeline_parameters=None, param_python_name_dict=None,
            component_type=None):
        """
        :param workspace: Component workspace
        :type workspace: azureml.core.Workspace
        :param provided_outputs: Output parameters
        :type provided_outputs: List[Output]
        :param output_interfaces: Output interface definition for the component
        :type output_interfaces: list of StructuredInterfaceOutput
        :param process_error: Function to handle invalid situation
        :type process_error: Callable
        :param definition_validator:
        :param is_local: Whether the validation is for local run in the host, false if it is for remote run in AzureML.
        :type is_local: bool
        :param for_definition_validate: If the validate is for pipeline definition validate.
        :type for_definition_validate: bool
        :param pipeline_parameters: Pipeline parameters in current validating layer
        :type pipeline_parameters: dict[str, Union[Input, PipelineParameters]]
        :param param_python_name_dict: Map of input name and python name
        :type param_python_name_dict: dict[str, str]
        :param component_type: current component type
        :type component_type: str
        """

        def process_output_error(e: Exception, error_type, param_name):
            process_error(e, error_type, param_name, VariableType.Output)

        def process_pipeline_param_error(e: Exception, error_type, param_name, pipeline_param=None):
            process_error(e, error_type, param_name, VariableType.Output, pipeline_param=pipeline_param)

        def validate_link_parameter(output_interface, formatted_name, output, output_attr_name):
            output_attr = getattr(output, output_attr_name, None)
            if for_definition_validate and definition_validator:
                if isinstance(output_attr, PipelineParameter):
                    definition_validator.link_pipeline_parameter_and_assigned_parameter(
                        output_attr,
                        output_interface,
                        component_type=component_type)
                elif isinstance(output_attr, _ParameterAssignment):
                    setattr(output, output_attr_name,
                            definition_validator.get_original_object_for_parameter(output_attr))
                    definition_validator.validate_parameter_assignment(
                        output_attr,
                        output_interface,
                        formatted_name,
                        'str',
                        process_output_error,
                        component_type
                    )

        for _output in output_interfaces:
            formatted_name = _get_name_in_mapping(_output.name, param_python_name_dict)
            output = provided_outputs.get(formatted_name, None)
            output_link_attrs = output._get_link_parameter_attr()
            for output_instance, output_attr_name, _ in output_link_attrs:
                validate_link_parameter(
                    output_interface=_output,
                    formatted_name=formatted_name,
                    output=output_instance,
                    output_attr_name=output_attr_name
                )


class PipelineDefinitionValidator(object):
    def __init__(self, component_node_name, pipeline_parameters, process_error):
        """Init a pipeline definition validator.

        :param component_node_name: Name of the validated component node
        :type component_node_name: str
        :param pipeline_parameters: The pipeline parameters provided.
        :type pipeline_parameters: dict
        :param process_error: Function to handle invalid situation
        :type process_error: Callable
        """
        self.component_node_name = component_node_name
        self.pipeline_parameters = pipeline_parameters
        self.process_error = process_error

    def get_original_object_for_parameter(self, param):
        # Replace PipelineParameter in provided_parameters with objects in pipeline_parameters.
        # We are doing this because we have multiple objects for same pipeline parameter
        if isinstance(param, _ParameterAssignment):
            # for parameter assignment, replace pipeline parameters in it with original pipeline parameters
            for param_key in param.assignments_values_dict.keys():
                if param_key in self.pipeline_parameters.keys():
                    param.assignments_values_dict[param_key] = self.pipeline_parameters[param_key]
        elif isinstance(param, PipelineParameter) and param.name in self.pipeline_parameters.keys():
            param = self.pipeline_parameters[param.name]
        return param

    def validate_pipeline_parameter(
            self,
            param: PipelineParameter,
            assigned_param: StructuredInterfaceParameter,
            assigned_param_name: str,
            expected_type: Union[str, List[str]],
            process_parameter_error: Callable,
            component_type,
    ):
        """Validate if a pipeline parameter's type/range matches assigned component when building pipeline definition.

        Link the assigned parameter to pipeline parameter.
        Rules: parameter type mismatch, parameter range mismatch

        :param param: pipeline parameter to validate.
        :param assigned_param: pipeline parameter assigned parameter
        :param assigned_param_name: pipeline parameter assigned parameter name
        :param expected_type: assigned parameter expected type in string, eg: str, int, float
        :param process_parameter_error: function to process parameter error
        :param component_type: indicate current node component type
        """
        from azure.ml.component._core._types import _get_annotation_type_str

        # add linked param to pipeline parameter for future validation/infer
        self.link_pipeline_parameter_and_assigned_parameter(param, assigned_param, component_type=component_type)

        if param._annotation and expected_type:
            annotation_type = _get_annotation_type_str(param._annotation)
            type_match = False
            param_is_input_port = isinstance(param._annotation, Input)
            assigned_param_is_input_port = False
            if isinstance(assigned_param, StructuredInterfaceInput):
                assigned_param_is_input_port = True
                inner_type = expected_type
                # Extract primitive type if expected is like ['boolean']
                # Change others to 'input'
                if type(inner_type) is list:
                    inner_type = inner_type[0] if len(inner_type) == 1 else 'input'
                inner_type = _Param.parse_param_type_string(inner_type)\
                    if inner_type in _Param._PARAM_TYPE_STRING_MAPPING else 'input'
                if not param_is_input_port:
                    # Invalid case: pipeline parameter link to sub pipeline port
                    # Change pipeline port expected_type to 'input' for exception
                    expected_type = 'input' \
                        if component_type == ComponentType.PipelineComponent.value else expected_type
                elif inner_type == annotation_type:
                    # if input is not primitive type, it just need to be a dsl.input
                    # if input is primitive type, check type
                    type_match = True
            else:
                # Invalid case: parameter port link to sub pipeline parameter
                #
                # @dsl.pipeline()
                # def sub_pipeline_func(param: str):  # assigned param: not a port
                #     ...
                # @dsl.pipeline()
                # def pipeline_func(param: Input(type='string')):  # param: a port
                #     sub_pipeline_func(param=param)  # invalid
                #     another_component_func(parameter=param)  # valid
                if param._annotation and param_is_input_port and \
                        component_type == ComponentType.PipelineComponent.value:
                    # change annotation type to input for exception
                    # if param is input port and link to sub pipeline parameter
                    annotation_type = 'input'

                # if param/run settings is annotated, it should match with linked param
                if annotation_type == expected_type:
                    type_match = True
            if not type_match:
                process_parameter_error(
                    ValueError("Parameter '{}' type mismatched, expected type: '{}', got '{}'.".format(
                        assigned_param_name, expected_type, annotation_type
                    )),
                    ComponentValidationError.INVALID_PARAMETER,
                    assigned_param_name,
                    param
                )
                return
            if param_is_input_port or assigned_param_is_input_port:
                # only check type for input port
                return
            if expected_type == "int" or expected_type == "float":
                # check range for numeric types
                expected_min = float(assigned_param.lower_bound) if assigned_param.lower_bound is not None else None
                expected_max = float(assigned_param.upper_bound) if assigned_param.upper_bound is not None else None
                actual_min = param._annotation.min
                actual_max = param._annotation.max

                def _min_violate(actual, expected):
                    if actual is not None:
                        if expected is not None:
                            return actual < expected
                        else:
                            # actual: [None, xxx], expected: [1, xxx] is not violating because the actual value
                            # usually don't have a min val, we will use the expected value to infer it
                            return False
                    else:
                        # actual: [1, xxx], expected: [None, xxx] is not violating because the actual range is smaller
                        return False

                def _max_violate(actual, expected):
                    if actual is not None:
                        if expected is not None:
                            return actual > expected
                        else:
                            return False
                    else:
                        return False
                # param._annotation.min/max will be None when user not specifying it
                if _min_violate(actual_min, expected_min) or _max_violate(actual_max, expected_max):
                    actual_range = '[{}, {}]'.format(param._annotation.min, param._annotation.max)
                    expected_range = '[{}, {}]'.format(assigned_param.lower_bound, assigned_param.upper_bound)
                    process_parameter_error(
                        ValueError("Parameter '{}' range mismatched, expected: '{}', got '{}'.".format(
                            assigned_param_name, expected_range, actual_range
                        )),
                        ComponentValidationError.INVALID_PARAMETER,
                        assigned_param_name,
                        param
                    )
                return
            elif expected_type == "str":
                # check str and enum
                expected_enum = set(assigned_param.enum_values) if assigned_param.enum_values else None
                actual_enum = set(param._annotation.enum) if param._annotation.enum else None
                # actual_enum will be None when user not specifying it
                if actual_enum and expected_enum != actual_enum:
                    process_parameter_error(
                        ValueError("Parameter '{}' enum mismatched, expected: '{}', got '{}'.".format(
                            assigned_param_name, assigned_param.enum_values, param._annotation.enum
                        )),
                        ComponentValidationError.INVALID_PARAMETER,
                        assigned_param_name,
                        param
                    )

    def validate_parameter_assignment(
            self,
            param: _ParameterAssignment,
            assigned_param: StructuredInterfaceParameter,
            assigned_param_name: str,
            expected_type: str,
            process_parameter_error: Callable,
            component_type: str
    ):
        """Validate parameter assignment, check if it contains input and if the assigned parameter is string.

        Link the assigned parameter to pipeline parameters in parameter assignment.
        Rules: parameter assignment type mismatch, input in parameter assignment

        :param param: parameter assignment to validate
        :param assigned_param: parameter assignment assigned parameter
        :param assigned_param_name: pipeline parameter assigned parameter name
        :param expected_type: assigned parameter expected type in string, eg: str, int, float
        :param process_parameter_error: function to process parameter error
        :param component_type: the component type
        """
        if expected_type != 'str':
            process_parameter_error(
                ValueError("Parameter '{}' type mismatched, expected type: '{}', got 'str'.".format(
                    assigned_param_name, expected_type
                )),
                ComponentValidationError.INVALID_PARAMETER,
                assigned_param_name
            )

        # add linked param to all pipeline parameters in parameter assignment
        for pipeline_param in param.assignments_values_dict.values():
            if isinstance(pipeline_param, PipelineParameter):
                if pipeline_param._annotation:
                    from azure.ml.component._core._types import _get_annotation_type_str
                    annotation_type = _get_annotation_type_str(pipeline_param._annotation)
                    if annotation_type == "input":
                        process_parameter_error(
                            ValueError(
                                "Only parameter can be referenced in parameter assignment, got input: {}".format(
                                    pipeline_param.name
                                )
                            ),
                            ComponentValidationError.INVALID_PARAMETER,
                            assigned_param_name
                        )

                # store a special link for parameter assignment so we won't use it to infer type
                self.link_pipeline_parameter_and_assigned_parameter(
                    pipeline_param, assigned_param, link_as_parameter_assignment=True, component_type=component_type)

    def link_pipeline_parameter_and_assigned_parameter(
            self,
            param: PipelineParameter,
            assigned_param: StructuredInterfaceParameter,
            link_as_parameter_assignment=False,
            component_type=None
    ):
        """Add linked param to pipeline parameter for future validation

        :param param: provided pipeline parameter or input
        :param assigned_param: assigned parameter
        :param link_as_parameter_assignment: if link assigned_param as parameter assignment
        :param component_type: the linked parameters owner type
        """
        param_key = ":".join([self.component_node_name, assigned_param.name])
        if link_as_parameter_assignment:
            param.linked_param_assignments[param_key] = assigned_param
        else:
            param.linked_params[param_key] = assigned_param
        param.linked_param_owner_type[param_key] = component_type

    def mark_pipeline_parameter_used(self, param: Union[PipelineParameter, List, dict]):
        """Mark pipeline param used so there won't have warnings on pipeline parameter unused.

        :param param: The param need to mark used.
        """
        if isinstance(param, List):
            for element in param:
                self.mark_pipeline_parameter_used(element)
        elif isinstance(param, dict):
            for val in param.values():
                self.mark_pipeline_parameter_used(val)
        elif isinstance(param, PipelineParameter):
            param.used_in_definition = True


class DiagnosticDescriptor(object):
    """Provides a description about a Diagnostic."""

    def __init__(self, message: str, type: str):
        """
        Create description about a Diagnostic.

        :param message: Error message of diagnostic.
        :type message: str
        :param type: Error type of diagnostic.
        :type type: str
        """
        self.message = message
        self.type = type


class VariableType(Enum):
    """Represents all type of component variables."""
    Input = 'Input'
    Output = 'Output'
    Parameter = 'Parameter'
    Runsetting = 'Runsetting'


class DiagnosticLocation(object):
    """The location of diagnostic in Pipeline or Component."""

    def __init__(self, pipeline_name: str = None, component_name: str = None,
                 variable_type: VariableType = None, variable_name: str = None,
                 component_id: str = None, component_version: str = None):
        """
        Create diagnostic location of a validation result.

        :param pipeline_name: Pipeline friendly name
        :type pipeline_name: str
        :param component_name: Component friendly name
        :type component_name: str
        :param variable_type: Type of invlidate variable
        :type variable_type: VariableType
        :param variable_name: Invlidate variable name
        :type variable_name: str
        :param component_id: Version of invlidate component
        :type component_id: str
        :param component_version: Invalidate component id
        :type component_version: str
        """
        self.pipeline_name = pipeline_name
        self.component_name = component_name
        self.variable_type = variable_type
        self.variable_name = variable_name
        self.component_id = component_id
        self.component_version = component_version


class Diagnostic(object):
    """Represents a diagnostic of a component validate error with the location info."""

    def __init__(self, id: str, location: DiagnosticLocation, descriptor: DiagnosticDescriptor):
        """
        Init Diagnostic.

        :param id: Pipeline or component friendly name
        :type id: str
        :param location: The location of diagnostic in Pipeline or Component.
        :type location: DiagnosticLocation
        :param descriptor: Description about a Diagnostic.
        :type descriptor: DiagnosticDescriptor
        """
        self.id = id
        self.location = location
        self.descriptor = descriptor

    @classmethod
    def create_diagnostic_by_component(cls, component, error_msg: str,
                                       error_type: str, error_var_name: str=None,
                                       error_var_type: str=None):
        """
        Create diagnostic by component and set component friendly name as diagnostic id.

        :param component: Invalidate Component or pipeline.
        :type component: azure.ml.Component
        :param error_msg: Error message
        :type error_msg: str
        :param error_type: Error type
        :type error_type: str
        :param error_var_name: Invalidate variable name
        :type error_var_name: str
        :param error_var_type: Type of invlidate variable
        :type error_var_type: VariableType
        :return: A diagnostic of a component validate error
        :rtype: Diagnostic
        """
        from azure.ml.component._core._component_definition import ComponentType
        if component._definition._type == ComponentType.PipelineComponent:
            pipeline_name = component._graph_path
            component_name = None
        else:
            pipeline_name, component_name = component._parse_graph_path()
        location = DiagnosticLocation(pipeline_name=pipeline_name,
                                      component_name=component_name,
                                      variable_name=error_var_name,
                                      variable_type=error_var_type,
                                      component_id=component._identifier,
                                      component_version=component.version)

        descriptor = DiagnosticDescriptor(error_msg, error_type)
        return cls(id=component._graph_path,
                   location=location,
                   descriptor=descriptor)

    @classmethod
    def create_diagnostic_by_component_definition(cls, definition, error_msg: str,
                                                  error_type: str, error_var_name: str=None,
                                                  error_var_type: str=None,
                                                  component=None):
        """
        Create diagnostic by pipeline definition. Will generate diagnostic per definition and mark it with definition
        id.

        :param definition: Invalidate PipelineComponentDefinition.
        :type definition: azure.ml._core._component_definition.PipelineComponentDefinition
        :param error_msg: Error message
        :type error_msg: str
        :param error_type: Error type
        :type error_type: str
        :param error_var_name: Invalidate variable name
        :type error_var_name: str
        :param error_var_type: Type of invalid variable
        :type error_var_type: VariableType
        :param component: Invalid component, None means the error happens on pipeline parameter.
        :param component: azure.ml.Component
        :return: A diagnostic of a component validate error
        :rtype: Diagnostic
        """
        # the error happens when constructing component definition from bottom to top,
        # parent pipeline name is not available
        if component is not None:
            component_name = definition.get_variable_name_for_component(component)
        else:
            component_name = None
        location = DiagnosticLocation(pipeline_name=definition.name,
                                      component_name=component_name,
                                      variable_name=error_var_name,
                                      variable_type=error_var_type,
                                      component_id=component._identifier if component else None,
                                      component_version=component.version if component else None)
        descriptor = DiagnosticDescriptor(error_msg, error_type)
        error_id = definition.name
        if component_name:
            error_id += ".{}".format(component_name)
        return cls(id=error_id,
                   location=location,
                   descriptor=descriptor)

    @classmethod
    def create_diagnostic(cls, error_msg: str, error_type: str,
                          error_var_name: str = None, error_var_type: VariableType = None):
        """
        Create diagnostic by error message and set error variable name as deagnostic id.

        :param error_msg: Error message
        :type error_msg: str
        :param error_type: Error type
        :type error_type: str
        :param error_var_name: Invalidate variable name
        :type error_var_name: str
        :param error_var_type: Type of invlidate variable
        :type error_var_type: VariableType

        :return: A diagnostic of error message
        :rtype: Diagnostic
        """
        location = DiagnosticLocation(variable_name=error_var_name,
                                      variable_type=error_var_type)
        descriptor = DiagnosticDescriptor(error_msg, error_type)
        return cls(id=error_var_name, location=location, descriptor=descriptor)

    def __repr__(self):
        """Return the component friendly name and error message."""
        return '{}: {}'.format(self.id, self.descriptor.message)
