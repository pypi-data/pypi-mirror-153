# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Contains classes for creating and managing reusable computational units of an Azure Machine Learning pipeline.

Modules allow you to create computational units in a :class:`azureml.pipeline.wrapper.Pipeline`, which can have
inputs, outputs, and rely on parameters and an environment configuration to operate.

Modules are designed to be reused in several pipelines and can evolve to adapt a specific computation logic
to different use cases. A step in a pipeline can be used in fast iterations to improve an algorithm,
and once the goal is achieved, the algorithm is usually published as a module to enable reuse.
"""

import importlib
import inspect
from pathlib import Path
import types
from typing import Callable, List

from azure.ml.component._restclients.service_caller_factory import _DesignerServiceCallerFactory
from azureml.core import Workspace
from azureml.exceptions._azureml_exception import UserErrorException

from azure.ml.component._core._component_definition import CommandComponentDefinition
from azure.ml.component.component import Input, _ComponentLoadSource, Component
from azure.ml.component._dynamic import KwParameter, create_kw_method_from_parameters
from azure.ml.component._component_func import to_component_func, get_dynamic_param_parameter, \
    get_dynamic_input_parameter
from azure.ml.component._module_dto import ModuleDto
from azure.ml.component._util._loggerfactory import _LoggerFactory, _PUBLIC_API, track
from azure.ml.component._util._telemetry import WorkspaceTelemetryMixin
from azure.ml.component._api._api import _dto_2_definition

_logger = None


def _get_logger():
    global _logger
    if _logger is not None:
        return _logger
    _logger = _LoggerFactory.get_logger()
    return _logger


class Module(Component):
    """THIS CLASS REPRESENTS A DEPRECATED CONCEPT AND IS ONLY USED FOR BACKWARD COMPATIBILITY."""

    @property
    def name(self):
        """Return the display name of the component name as the module name for backward compatibility."""
        return self.display_name

    @staticmethod
    def _from_func(
            workspace: Workspace,
            func: types.FunctionType,
            force_reload=True,
            load_source=_ComponentLoadSource.UNKNOWN
    ):
        def _reload_func(f: types.FunctionType):
            """Reload the function to make sure the latest code is used to generate yaml."""
            module = importlib.import_module(f.__module__)
            # if f.__name__ == '__main__', reload will throw an exception
            if f.__module__ != '__main__':
                from azure.ml.component.dsl._utils import _force_reload_module
                _force_reload_module(module)
            return getattr(module, f.__name__)

        if force_reload:
            func = _reload_func(func)
        # Import here to avoid circular import.
        from azure.ml.component.dsl._component import ComponentExecutor
        from azure.ml.component.dsl._module_spec import SPEC_EXT
        from azure.ml.component.dsl._utils import _temporarily_remove_file
        # If a ComponentExecutor instance is passed, we directly use it,
        # otherwise we construct a ComponentExecutor with the function
        executor = func if isinstance(func, ComponentExecutor) else ComponentExecutor(func)
        # Use a temp spec file to register.
        temp_spec_file = Path(inspect.getfile(func)).absolute().with_suffix(SPEC_EXT)
        temp_conda_file = temp_spec_file.parent / 'conda.yaml'
        conda_exists = Path(temp_conda_file).is_file()
        # the conda may be the notebook gen conda, cannot temporarily remove if exists
        with _temporarily_remove_file(temp_spec_file):
            try:
                temp_spec_file = executor.to_spec_yaml(
                    folder=temp_spec_file.parent,
                    spec_file=temp_spec_file.name)
                return Module._from_module_spec(workspace=workspace, yaml_file=str(temp_spec_file),
                                                load_source=load_source)
            finally:
                if not conda_exists and Path(temp_conda_file).is_file():
                    Path(temp_conda_file).unlink()

    @staticmethod
    def _from_module_spec(
            workspace: Workspace,
            yaml_file: str,
            load_source: str
    ):
        definition = CommandComponentDefinition._register_module(workspace, spec_file=yaml_file,
                                                                 package_zip=None, anonymous_registration=True,
                                                                 set_as_default=False,
                                                                 amlignore_file=None, version=None)
        definition._load_source = load_source

        return Module._module_func(workspace, definition._module_dto, definition._load_source)

    @staticmethod
    def _module_func(
            workspace: Workspace,
            module_dto: ModuleDto,
            load_source: str = _ComponentLoadSource.UNKNOWN,
            return_yaml=True
    ) -> Callable[..., 'Module']:
        """
        Get module func from ModuleDto.

        :param workspace: The workspace object this module will belong to.
        :type workspace: azureml.core.Workspace
        :param module_dto: ModuleDto instance
        :type module_dto: azure.ml.component._module_dto
        :param load_source: The source which the component is loaded.
        :type load_source: str
        :return: a function that can be called with parameters to get a `azure.ml.component.Module`
        :rtype: function
        """
        def create_module_func(**kwargs) -> 'Module':
            definition = _dto_2_definition(module_dto, workspace)
            definition._load_source = load_source
            return Module(definition, kwargs)

        return to_component_func(module_dto=module_dto, return_yaml=return_yaml,
                                 component_creation_func=create_module_func)

    def set_inputs(self, *args, **kwargs) -> 'Module':
        """Update the inputs of the module."""
        # Note that the argument list must be "*args, **kwargs" to make sure
        # vscode intelligence works when the signature is updated.
        # https://github.com/microsoft/vscode-python/blob/master/src/client/datascience/interactive-common/intellisense/intellisenseProvider.ts#L79
        self._inputs.update({k: Input(v, k, owner=self) for k, v in kwargs.items() if v is not None})
        self._extra_input_settings.update(kwargs)
        return self

    def set_parameters(self, *args, **kwargs) -> 'Module':
        """Update the parameters of the module."""
        # Note that the argument list must be "*args, **kwargs" to make sure
        # vscode intelligence works when the signature is updated.
        # https://github.com/microsoft/vscode-python/blob/master/src/client/datascience/interactive-common/intellisense/intellisenseProvider.ts#L79
        self._inputs.update({k: v for k, v in kwargs.items() if v is not None})
        self._extra_input_settings.update(kwargs)
        return self

    @staticmethod
    @track(activity_type=_PUBLIC_API)
    def load(workspace: Workspace, namespace: str = None, name: str = None,
             version: str = None, id: str = None) -> Callable[..., 'Module']:
        """
        Get module function from workspace.

        :param workspace: The workspace object this module will belong to.
        :type workspace: azureml.core.Workspace
        :param namespace: Namespace
        :type namespace: str
        :param name: The name of module
        :type name: str
        :param version: Version
        :type version: str
        :param id: str : The module version id of an existing module
        :type id: str
        :return: a function that can be called with parameters to get a `azure.ml.component.Module`
        :rtype: function
        """
        service_caller = _DesignerServiceCallerFactory.get_instance(workspace)
        if id is None:
            module_dto = ModuleDto(service_caller.get_module(
                module_namespace=namespace,
                module_name=name,
                version=version,  # If version is None, this will get the default version
                include_run_setting_params=False
            ))
        else:
            module_dto = ModuleDto(service_caller.get_module_by_id(module_id=id, include_run_setting_params=False))

        module_dto.correct_module_dto()

        return Module._module_func(workspace,
                                   module_dto,
                                   _ComponentLoadSource.REGISTERED,
                                   return_yaml=True)

    @staticmethod
    @track(activity_type=_PUBLIC_API)
    def batch_load(workspace: Workspace, ids: List[str] = None, identifiers: List[tuple] = None) -> \
            List[Callable[..., 'Module']]:
        """
        Batch load modules by identifier list.

        If there is an exception with any module, the batch load will fail. Partial success is not allowed.

        :param workspace: The workspace object this module will belong to.
        :type workspace: azureml.core.Workspace
        :param ids: module version ids
        :type ids: list[str]
        :param identifiers: list of tuple(name, namespace, version)
        :param identifiers: list of tuple(name, version)
        :type identifiers: list[tuple]

        :return: a tuple of module functions
        :rtype: tuple(function)
        """
        service_caller = _DesignerServiceCallerFactory.get_instance(workspace)
        refined_module_dtos = \
            service_caller.batch_get_modules(module_version_ids=ids,
                                             name_identifiers=identifiers)
        module_number = len(refined_module_dtos)
        module_dtos = [ModuleDto(item) for item in refined_module_dtos]
        telemetry_values = WorkspaceTelemetryMixin._get_telemetry_value_from_workspace(workspace)
        telemetry_values.update({
            'count': module_number,
        })
        _LoggerFactory.add_track_dimensions(_get_logger(), telemetry_values)
        module_funcs = (Module._module_func(workspace=workspace,
                                            module_dto=module_dto,
                                            load_source=_ComponentLoadSource.REGISTERED,
                                            return_yaml=False
                                            )
                        for module_dto in module_dtos)
        if module_number == 1:
            module_funcs = next(module_funcs)
        return module_funcs

    @staticmethod
    @track(activity_type=_PUBLIC_API)
    def from_func(workspace: Workspace, func: types.FunctionType, force_reload=True) -> Callable[..., 'Module']:
        """Register an anonymous component from a wrapped python function and return the registered module func.

        :param workspace: The workspace object this module will belong to.
        :type workspace: azureml.core.Workspace
        :param func: A wrapped function to be loaded or a ComponentExecutor instance.
        :type func: types.FunctionType
        :param force_reload: Whether reload the function to make sure the code is the latest.
        :type force_reload: bool
        """
        return Module._from_func(workspace=workspace, func=func,
                                 force_reload=force_reload, load_source=_ComponentLoadSource.FROM_FUNC)

    @staticmethod
    @track(activity_type=_PUBLIC_API)
    def from_yaml(workspace: Workspace, yaml_file: str) -> Callable[..., 'Module']:
        """Register an anonymous module from yaml file to workspace and return the registered module func.

        Assumes source code is in the same directory with yaml file. Then return the registered module func.

        :param workspace: The workspace object this module will belong to.
        :type workspace: azureml.core.Workspace
        :param yaml_file: Module spec file. The spec file could be located in local or Github.
                          For example:

                          * "custom_module/module_spec.yaml"
                          * "https://github.com/zzn2/sample_modules/blob/master/3_basic_module/basic_module.yaml"
        :type yaml_file: str
        :return: a function that can be called with parameters to get a `azure.ml.component.Module`
        :rtype: function
        """
        return Module._from_module_spec(workspace=workspace, yaml_file=yaml_file,
                                        load_source=_ComponentLoadSource.FROM_YAML)

    @staticmethod
    @track(activity_type=_PUBLIC_API)
    def register(workspace: Workspace, yaml_file: str, amlignore_file: str = None, set_as_default: bool = False,
                 version: str = None) -> \
            Callable[..., 'Module']:
        """
        Register a module from yaml file to workspace.

        Assumes source code is in the same directory with yaml file. Then return the registered module func.

        :param workspace: The workspace object this module will belong to.
        :type workspace: azureml.core.Workspace
        :param yaml_file: Module spec file. The spec file could be located in local or Github.
                          For example:

                          * "custom_module/module_spec.yaml"
                          * "https://github.com/zzn2/sample_modules/blob/master/3_basic_module/basic_module.yaml"
        :type yaml_file: str
        :param amlignore_file: The .amlignore or .gitignore file path used to exclude files/directories in the snapshot
        :type amlignore_file: str
        :param set_as_default: By default false, default version of the module will not be updated
                                when registering a new version of module. Specify this flag to set
                                the new version as the module's default version.
        :type set_as_default: bool
        :param version: If specified, registered module will use specified value as version
                                            instead of the version in the yaml.
        :type version: str
        :return: a function that can be called with parameters to get a `azure.ml.component.Module`
        :rtype: function
        """
        if version is not None:
            if not isinstance(version, str):
                raise UserErrorException('Only string type of supported for param version.')
            elif version == "":
                # Hint user when accidentally set empty string to set_version
                raise UserErrorException('Param version does not allow empty value.')
        definition = CommandComponentDefinition._register_module(workspace, spec_file=yaml_file,
                                                                 package_zip=None,
                                                                 anonymous_registration=False,
                                                                 set_as_default=set_as_default,
                                                                 amlignore_file=amlignore_file,
                                                                 version=version)
        definition._load_source = _ComponentLoadSource.FROM_YAML

        return Module._module_func(workspace, definition._module_dto, definition._load_source)

    def _init_dynamic_method(self):
        """Update methods set_inputs/set_parameters according to the component input/param definitions."""
        self.set_inputs = create_kw_method_from_parameters(
            self.set_inputs, get_dynamic_input_parameter(self._definition),
        )
        transformed_parameters = [
            # Here we set all default values as None to avoid overwriting the values by default values.
            KwParameter(name=param.name, default=None, annotation=param.annotation, _type=param._type)
            for param in get_dynamic_param_parameter(self._definition)
        ]
        self.set_parameters = create_kw_method_from_parameters(
            self.set_parameters, transformed_parameters,
        )
