# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from azure.ml.component._core import ComponentDefinition


def component_tag_repr(tags):
    """Get string representation of tags."""
    return ', '.join("{}:{}".format(k, v) for k, v in tags.items()) if tags else ""


def update_result_dict(component, result_dict, to_component_dict=True, update_status=False, update_created_by=False):
    """Update component/module result dict with namespace + name or just name, update status, etc"""
    # update namespace & name
    if to_component_dict:
        name_dict = {
            'name': component.name
        }
    else:
        name_dict = {
            'name': component._name,
            'namespace': component._namespace
        }
    result_dict.update(name_dict)

    # update status
    if update_status:
        context = component.registration_context
        status_code = context.status_code
        status_dict = {
            'status': context._convert_entry_status_code(status_code, to_component_dict)
        }
        result_dict.update(status_dict)

    # update created by
    if update_created_by:
        if to_component_dict:
            created_by_dict = {
                'createdBy': component.creation_context.created_by,
                'createdOn': component.creation_context.created_date,
            }
        else:
            created_by_dict = {
                'registeredBy': component.creation_context.created_by,
                'registeredOn': component.creation_context.created_date,
            }
        result_dict.update(created_by_dict)
    return result_dict


def component_definition_to_detail_dict(component: ComponentDefinition, to_component_dict=True):
    """Dumps a component definition object into a dict representation, display detail information."""
    result = {
        'versions': component.registration_context.all_versions,
        'displayName': component.display_name,
        'ID': component.identifier,
        'description': component.description,
        'version': component.version,
        'type': component.type.value,
        'lastUpdatedOn': component.creation_context.last_modified_date,
        'yamlLink': component.registration_context.yaml_link,
        'tags': component_tag_repr(component.tags)
    }
    update_result_dict(component, result, to_component_dict, update_status=True, update_created_by=True)
    return result


def component_definition_to_validation_result_dict(component: ComponentDefinition, to_component_dict=True):
    """Dumps a component definition object into a dict representation, display for validation result."""
    result = {
        'displayName': component.display_name,
        'description': component.description,
        'version': component.version,
        'type': component.type.value,
        'yamlLink': component.registration_context.yaml_link,
        'tags': component_tag_repr(component.tags),
    }
    update_result_dict(component, result, to_component_dict)
    return result


def component_definition_to_summary_dict(component: ComponentDefinition, to_component_dict=False):
    """Dumps a component definition object into a dict representation, display only summary information."""
    result = {
        'name': component.name,
        'displayName': component.display_name,
        'defaultVersion': component.registration_context.default_version,
        'tags': component_tag_repr(component.tags),
        'registry': component.registry_name
    }
    update_result_dict(component, result, to_component_dict, update_status=True)
    return result


def component_definition_to_versions_dict(component: ComponentDefinition):
    """Dumps a component definition object into a dict representation, display version information like UX did."""
    if component.version == component.registration_context.default_version:
        version = '{}(default)'.format(component.version)
    else:
        version = component.version
    result = {
        'version': version,
        'ID': component.identifier,
        'displayName': component.display_name,
        'description': component.description,
        'createdBy': component.creation_context.created_by,
        'lastUpdatedOn': component.creation_context.last_modified_date,
        'tags': component_tag_repr(component.tags),
        'registry': component.registry_name,
    }
    return result
