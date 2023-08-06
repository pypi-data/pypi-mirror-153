# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import BinaryIO

from azureml.exceptions import UserErrorException
from azure.ml.component._restclients.service_caller_factory import _DesignerServiceCallerFactory
from azure.ml.component._restclients.designer.models import ModuleDtoFields


class ModuleAPICaller:
    """Implementation for CRUD operations for module.

    Actual operations are implemented via auto generated rest clients.
    # TODO: replace this class with auto generated CRUD implementation.
    """

    def __init__(self, workspace, from_cli=False):
        self._workspace = workspace
        self.service_caller = _DesignerServiceCallerFactory.get_instance(workspace, from_cli)

    def register(self, component_source_type: str, yaml_file: str = None,
                 snapshot_source_zip_file: BinaryIO = None, devops_artifacts_zip_url: str = None,
                 validate_only: bool = False, anonymous_registration: bool = True, set_as_default: bool = False,
                 version: str = None, snapshot_id: str = None):
        result = self.service_caller.register_module(
            anonymous_registration=anonymous_registration,
            validate_only=validate_only,
            module_source_type=component_source_type, yaml_file=yaml_file,
            snapshot_source_zip_file=snapshot_source_zip_file,
            devops_artifacts_zip_url=devops_artifacts_zip_url,
            set_as_default=set_as_default,
            overwrite_module_version=version
        )
        return result

    def parse(self, component_source_type: str, yaml_file: str = None,
              snapshot_source_zip_file: BinaryIO = None, devops_artifacts_zip_url: str = None):
        result = self.service_caller.parse_module(
            module_source_type=component_source_type,
            yaml_file=yaml_file,
            snapshot_source_zip_file=snapshot_source_zip_file,
            devops_artifacts_zip_url=devops_artifacts_zip_url
        )
        return result

    def list(self, include_disabled: bool, continuation_header: dict):
        result = self.service_caller.list_modules(
            active_only=not include_disabled,
            continuation_header=continuation_header,
        )
        return result

    def get(self, name, namespace, version=None):
        result = self.service_caller.get_module(
            module_name=name,
            module_namespace=namespace,
            version=version
        )
        return result

    def get_by_id(self, _id):
        return self.service_caller.get_module_by_id(_id)

    def batch_get(self, ids, identifiers):
        return self.service_caller.batch_get_modules(module_version_ids=ids,
                                                     name_identifiers=identifiers)

    def enable(self, name, namespace):
        body = {'ModuleUpdateOperationType': 'EnableModule'}
        return self.update(name, namespace, body)

    def disable(self, name, namespace):
        body = {'ModuleUpdateOperationType': 'DisableModule'}
        return self.update(name, namespace, body)

    def set_default_version(self, name, namespace, version):
        body = {'ModuleUpdateOperationType': 'SetDefaultVersion', 'ModuleVersion': version}
        return self.update(name, namespace, body)

    def update(self, name, namespace, body):
        result = self.service_caller.update_module(
            module_name=name,
            module_namespace=namespace,
            body=body
        )
        # The PATCH api will not return full data of the updated module,
        # so we do a GET operation here.
        result = self.service_caller.get_module(
            module_name=result.module_name,
            module_namespace=result.namespace,
        )
        return result

    def get_module_yaml(self, name, namespace, version):
        result = self.service_caller.get_module_yaml(module_namespace=namespace, module_name=name, version=version)
        return result

    def get_snapshot_url(self, name, namespace, version):
        snapshot_url = self.service_caller.get_module_snapshot_url(module_namespace=namespace, module_name=name,
                                                                   version=version)
        return snapshot_url

    def get_snapshot_url_by_id(self, component_id):
        snapshot_url = self.service_caller.get_module_snapshot_url_by_id(module_id=component_id)
        return snapshot_url


class ComponentAPICaller:
    """Implementation for CRUD operations for component, by using MT component APIs.

    Actual operations are implemented via auto generated rest clients.
    """

    def __init__(self, workspace, from_cli=False, region=None):
        self._workspace = workspace
        self._region = region
        self.service_caller = _DesignerServiceCallerFactory.get_instance(workspace, from_cli, region)

    def register(self, component_source_type: str, yaml_file: str = None,
                 snapshot_source_zip_file: BinaryIO = None, devops_artifacts_zip_url: str = None,
                 validate_only: bool = False, anonymous_registration: bool = True, set_as_default: bool = False,
                 version: str = None, snapshot_id: str = None, registry_name: str = None):
        if registry_name is None:
            result = self.service_caller.register_component(
                anonymous_registration=anonymous_registration,
                validate_only=validate_only,
                module_source_type=component_source_type, yaml_file=yaml_file,
                snapshot_source_zip_file=snapshot_source_zip_file,
                devops_artifacts_zip_url=devops_artifacts_zip_url,
                set_as_default_version=set_as_default,
                overwrite_component_version=version,
                snapshot_id=snapshot_id
            )
        else:
            result = self.service_caller.register_registry_component(
                validate_only=validate_only,
                set_as_default_version=set_as_default,
                overwrite_component_version=version,
                registry_name=registry_name,
                snapshot_id=snapshot_id,
                module_source_type=component_source_type,
                yaml_file=yaml_file,
                snapshot_source_zip_file=snapshot_source_zip_file,
                devops_artifacts_zip_url=devops_artifacts_zip_url,
            )
        return result

    def parse(self, component_source_type: str, yaml_file: str = None,
              snapshot_source_zip_file: BinaryIO = None, devops_artifacts_zip_url: str = None):
        result = self.service_caller.parse_component(
            module_source_type=component_source_type,
            yaml_file=yaml_file,
            snapshot_source_zip_file=snapshot_source_zip_file,
            devops_artifacts_zip_url=devops_artifacts_zip_url
        )
        return result

    def list(self, include_disabled: bool, continuation_header: dict,
             module_scope=None, feed_names=None, module_dto_fields=ModuleDtoFields.MINIMAL,
             registry_names=None, name=None):
        if registry_names is None:
            if name:
                raise UserErrorException("The list workspace components api doesn't have name parameter.")
            result = self.service_caller.list_components(
                active_only=not include_disabled,
                continuation_header=continuation_header,
                module_scope=module_scope, feed_names=feed_names, module_dto_fields=module_dto_fields
            )
        else:
            result = self.service_caller.list_registry_components(
                name=name,
                registry_names=registry_names,
                active_only=not include_disabled,
                continuation_header=continuation_header,
                module_dto_fields=module_dto_fields,
            )
        return result

    def get(self, name, version=None, feed_name=None, registry_name=None):
        if self._workspace:
            result = self.service_caller.get_component(
                component_name=name,
                version=version,
                feed_name=feed_name,
                registry_name=registry_name
            )
        elif registry_name:
            # Get registry component
            result = self.service_caller.get_registry_component(
                component_name=name,
                version=version,
                registry_name=registry_name
            )
        else:
            raise UserErrorException("Workspace or registry must be specified when get component.")
        return result

    def get_by_id(self, _id):
        return self.service_caller.get_component_by_id(_id)

    def batch_get(self, ids, identifiers):
        return self.service_caller.batch_get_components(version_ids=ids,
                                                        name_identifiers=identifiers)

    def enable(self, name):
        body = {'ModuleUpdateOperationType': 'EnableModule'}
        return self.update(name, body)

    def disable(self, name):
        body = {'ModuleUpdateOperationType': 'DisableModule'}
        return self.update(name, body)

    def set_default_version(self, name, version):
        body = {'ModuleUpdateOperationType': 'SetDefaultVersion', 'ModuleVersion': version}
        return self.update(name, body)

    def set_display_name(self, name, display_name):
        body = {'ModuleUpdateOperationType': 'UpdateDisplayName', 'display_name': display_name}
        return self.update(name, body)

    def set_description(self, name, description):
        body = {'ModuleUpdateOperationType': 'UpdateDescription', 'description': description}
        return self.update(name, body)

    def set_tags(self, name, tags):
        body = {'ModuleUpdateOperationType': 'UpdateTags', 'tags': tags}
        return self.update(name, body)

    def update(self, name, body):
        result = self.service_caller.update_component(
            component_name=name,
            body=body
        )
        # The PATCH api will not return full data of the updated module,
        # so we do a GET operation here.
        result = self.service_caller.get_component(
            component_name=result.module_name,
        )
        return result

    def get_module_yaml(self, name, version, feed_name=None, registry_name=None):
        result = self.service_caller.get_component_yaml(component_name=name, version=version, feed_name=feed_name,
                                                        registry_name=registry_name)
        return result

    def get_snapshot_url(self, name, version):
        snapshot_url = self.service_caller.get_component_snapshot_url(component_name=name, version=version)
        return snapshot_url

    def get_snapshot_url_by_id(self, component_id):
        # get_component_snapshot_url_by_id is not ready yet, use module API instead
        snapshot_url = self.service_caller.get_module_snapshot_url_by_id(module_id=component_id)
        return snapshot_url

    def get_versions(self, name):
        result = self.service_caller.get_component_versions(component_name=name)
        return result
