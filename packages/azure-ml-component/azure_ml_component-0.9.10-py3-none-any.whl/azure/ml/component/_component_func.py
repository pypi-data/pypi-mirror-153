# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import logging
from typing import Callable

from azure.ml.component._restclients.service_caller_factory import _DesignerServiceCallerFactory
from azure.ml.component._core._types import _Param
from azureml.core import Workspace

from ._core._component_definition import ComponentDefinition
from ._dynamic import create_kw_function_from_parameters, KwParameter
from ._module_dto import ModuleDto
from ._util._utils import _get_name_in_mapping


def _get_module_yaml(workspace: Workspace, module_version_id: str):
    """
    Display yaml of component.

    :return: yaml of component
    :rtype: str
    """
    try:
        service_caller = _DesignerServiceCallerFactory.get_instance(workspace)
        result = service_caller.get_module_yaml_by_id(module_version_id)
        return str(result)
    except Exception as e:
        logging.warning("get component yaml meet exception : %s" % str(e))
        return None


def to_component_func(module_dto: ModuleDto, return_yaml: bool,
                      component_creation_func) -> Callable:
    func_docstring_lines = []
    module_description = module_dto.description.strip() if module_dto.description else ""
    func_docstring_lines.append(module_description)

    transformed_inputs, transformed_parameters, all_outputs = module_dto.get_module_inputs_outputs(
        return_yaml)
    all_params = transformed_inputs + transformed_parameters

    namespace = module_dto.namespace
    if namespace is None:
        func_name = "[component] {}".format(module_dto.module_name)
    else:
        func_name = "[component] {} (namespace: {})".format(
            module_dto.module_name, namespace)

    yaml = module_dto.yaml_str
    if yaml:
        # Use ```yaml\n{1}\n``` to make the yaml part readable in markdown.
        doc_string = '{0}\n\nComponent yaml:\n```yaml\n{1}\n```'.format(
            module_description, yaml)
    else:
        doc_string = '{0}\n\n{1}'.format(
            module_description,
            '\n'.join(_get_docstring_lines(all_params, all_outputs,
                                           module_dto.module_python_interface.outputs_name_mapping)))
    dynamic_func = create_kw_function_from_parameters(
        component_creation_func,
        documentation=doc_string,
        parameters=all_params,
        func_name=func_name,
    )

    return dynamic_func


def to_component_func_from_definition(definition: ComponentDefinition,
                                      component_creation_func) -> Callable:
    func_name = "[component] {}".format(definition.display_name)

    func_docstring_lines = []
    if definition.description is not None:
        func_docstring_lines.append(definition.description.strip())

    if definition.help_document is not None:
        func_docstring_lines.append(definition.help_document)

    all_params = get_dynamic_input_parameter(definition) + get_dynamic_param_parameter(definition)

    # TODO: Revert this change after pipeline component schema defined
    if not definition._is_pipeline_component_definition and \
            getattr(definition, '_module_dto', None) and definition._module_dto.yaml_str:
        doc_string = '{0}\n\nComponent yaml:\n```yaml\n{1}\n```'.format(
            definition.description, definition._module_dto.yaml_str)
    else:
        func_docstring_lines = []
        if definition.description is not None:
            func_docstring_lines.append(definition.description.strip())

        if definition.help_document is not None:
            func_docstring_lines.append(definition.help_document)

        all_outputs = definition.outputs

        if len(all_params) > 0:
            func_docstring_lines.append("\n")
        for param in all_params:
            func_docstring_lines.extend(_get_single_parameter_docstring_lines(param))

        if len(all_outputs) > 0:
            func_docstring_lines.append("\n")

        for k, v in all_outputs.items():
            output_name = k
            func_docstring_lines.append(":output {}: {}".format(
                output_name, v.description if v.description is not None else v.name))
            func_docstring_lines.append(":type: {}: {}".format(output_name, str(v.type)))
        doc_string = '\n'.join(func_docstring_lines)

    dynamic_func = create_kw_function_from_parameters(
        component_creation_func,
        documentation=doc_string,
        parameters=all_params,
        func_name=func_name,
    )

    dynamic_func._definition = definition

    return dynamic_func


def get_dynamic_input_parameter(self: ComponentDefinition):
    """Return the dynamic parameter of the definition's input ports."""
    return [KwParameter(name=name, annotation=str(input.type), default=None, _type=str(input.type),
                        _description=input._get_hint())
            for name, input in self.inputs.items()]


def get_dynamic_param_parameter(self: ComponentDefinition):
    """Return the dynamic parameter of the definition's input parameters."""
    return [KwParameter(name=name, annotation=_Param.parse_param_type_string(param.type), default=param.default,
                        _type=_Param.parse_param_type_string(param.type), _optional=param.optional,
                        _description=param._get_hint())
            for name, param in self.parameters.items()]


def _get_docstring_lines(all_params, all_outputs, param_name_dict):
    docstring_lines = []
    if len(all_params) > 0:
        docstring_lines.append("\n")
    for param in all_params:
        docstring_lines.extend(_get_single_parameter_docstring_lines(param))

    if len(all_outputs) > 0:
        docstring_lines.append("\n")
    for o in all_outputs:
        output_name = \
            _get_name_in_mapping(o.name, param_name_dict)
        docstring_lines.append(":output {}: {}".format(output_name,
                                                       o.description if o.description is not None else o.name))
        docstring_lines.append(":type: {}: {}".format(
            output_name, str(o.data_type_id)))
    return docstring_lines


def _get_single_parameter_docstring_lines(param: KwParameter):
    return [':param %s: %s' % (param.name, param._description),
            ':type %s: %s' % (param.name, param.annotation)]
