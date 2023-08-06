# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import copy
import os
import re
import shutil
import inspect
from enum import Enum
from functools import partial
from pathlib import Path
from typing import Sequence, Dict, Callable, Union
from collections import OrderedDict
from tempfile import mkdtemp

from azure.ml.component._module_dto import ModuleDto
from azure.ml.component._pipeline_parameters import PipelineParameter, LinkedParametersMixedIn
from azure.ml.component._restclients.designer.models import StructuredInterfaceParameter, StructuredInterfaceInput
from azure.ml.component._parameter_assignment import _ParameterAssignment
from azure.ml.component._restclients.service_caller_factory import _DesignerServiceCallerFactory
from azure.ml.component._core._types import Input, Output, _Param, _Group, _GroupAttrDict, _remove_empty_values
from azure.ml.component._util._constants import LOCAL_PREFIX
from azure.ml.component._util._exceptions import ComponentValidationError, wrap_azureml_exception_with_identifier, \
    UnsupportedOutputAnnotationError, YamlLoadingError
from azureml.exceptions import UserErrorException
from azureml.core import Workspace
from azureml.core import Datastore
from azureml.data.data_reference import DataReference

from azure.ml.component._util._utils import _ensure_target_folder_exist, _sanitize_python_variable_name, \
    _get_param_in_group_from_pipeline_parameters, _download_snapshot_by_id, _relative_path, \
    _flatten_pipeline_parameters
from azure.ml.component._util._yaml_utils import YAML, YamlFlowList, YamlMultiLineStr, YamlFlowDict
from azure.ml.component._api._api import ModuleAPI, ComponentAPI, _definition_to_dto, _DefinitionInterface
from azure.ml.component._core._component_contexts import CreationContext, RegistrationContext
from azure.ml.component._core._environment import Conda as CoreConda, Docker as CoreDocker, \
    CURATED_ENV_DICT_FOR_EXPRESSION_COMPONENT
from ._core import Component
from ._launcher_definition import LauncherDefinition, LauncherType
from ._environment import Environment
from ._run_settings_definition import RunSettingsDefinition, RunSettingParamDefinition
from .._restclients.designer.models._designer_service_client_enums import SuccessfulCommandReturnCode
from .._util._loggerfactory import _LoggerFactory, track
from .._util._telemetry import TelemetryMixin

logger = _LoggerFactory.get_logger()


def _to_camel(s, first_lower=False):
    result = s.title().replace('_', '')
    if first_lower and len(result) > 1:
        result = result[0].lower() + result[1:]
    return result


def _to_ordered_dict(data: dict) -> OrderedDict:
    for key, value in data.items():
        if isinstance(value, dict):
            data[key] = _to_ordered_dict(value)
    return OrderedDict(data)


class ComponentType(Enum):
    """Represents all types of components."""

    Component = 'Component'
    CommandComponent = 'CommandComponent'
    PipelineComponent = 'PipelineComponent'
    DistributedComponent = 'DistributedComponent'
    ParallelComponent = 'ParallelComponent'
    HDInsightComponent = 'HDInsightComponent'
    ScopeComponent = 'ScopeComponent'
    DataTransferComponent = 'DataTransferComponent'
    SweepComponent = 'SweepComponent'
    ControlComponent = '_ControlComponent'

    @classmethod
    def get_component_type_by_str(cls, type_str, default=None):
        if type_str is None:
            return default
        for t in cls:
            # Support CommandComponent@2 => CommandComponent
            if type_str.lower().startswith(t.value.lower()):
                return t

        # The legacy mapping is to get the correct type from the job type in old style yaml.
        legacy_mapping = {
            'basic': cls.CommandComponent,
            'mpi': cls.DistributedComponent,
            'parallel': cls.ParallelComponent,
            'hdinsight': cls.HDInsightComponent,
            'mpicomponent': cls.DistributedComponent,  # It used to be MPIComponent.
        }
        return legacy_mapping.get(type_str.lower(), default)

    @classmethod
    def _get_step_type(cls, typ, dct, *, base_dir=None, return_dct=False):
        """Return step type by component type."""
        # If not found matched type, function will return None.
        step_type = ComponentType._get_step_name_mapping().get(typ)
        base_dir = os.getcwd() if not base_dir else base_dir
        launcher = dct.get('launcher', None)
        if typ == cls.SweepComponent and SweepComponentDefinition.TRIAL_KEY in dct:
            # Change typ to trail component type
            trial_component = SweepComponentDefinition._get_trial_component(
                dct.pop(SweepComponentDefinition.TRIAL_KEY), base_dir)
            typ = trial_component.type
            step_type = step_type.get(typ)
            if typ == ComponentType.DistributedComponent:
                launcher = trial_component.launcher  # type: MPILauncherDefinition
        if typ == cls.DistributedComponent and launcher:
            launcher_type = LauncherDefinition._from_dict(launcher).type \
                if isinstance(launcher, dict) else launcher.type
            step_type = step_type.get(launcher_type)
        if type(step_type) != str:
            # Resolve step type failed if not str
            step_type = None
        if not return_dct:
            return step_type
        return step_type, dct

    @classmethod
    def _get_step_name_mapping(cls):
        return {
            cls.CommandComponent: 'PythonScriptModule',
            cls.DistributedComponent: {
                LauncherType.MPI: 'MpiModule',
                LauncherType.TORCH_DISTRIBUTED: 'TorchDistributedModule'
            },
            cls.HDInsightComponent: 'HDInsightModule',
            cls.ParallelComponent: 'ParallelRunModule',
            cls.ScopeComponent: 'ScopeModule',
            cls.DataTransferComponent: 'DataTransferModule',
            cls.SweepComponent: {
                cls.CommandComponent: 'HyperDrivePythonScriptModule',
                cls.DistributedComponent: {
                    LauncherType.MPI: 'HyperDriveMpiModule',
                    LauncherType.TORCH_DISTRIBUTED: 'HyperDriveTorchDistributedModule'
                }
            },
            cls.PipelineComponent: 'SubGraphCloudModule'
        }

    def get_definition_class(self):
        mapping = {
            self.CommandComponent: CommandComponentDefinition,
            self.DistributedComponent: DistributedComponentDefinition,
            self.ParallelComponent: ParallelComponentDefinition,
            self.HDInsightComponent: HDInsightComponentDefinition,
            self.ScopeComponent: ScopeComponentDefinition,
            self.DataTransferComponent: DataTransferComponentDefinition,
            self.SweepComponent: SweepComponentDefinition,
            self.PipelineComponent: PipelineComponentDefinition,
            self.ControlComponent: ControlComponentDefinition
        }
        # For unknown types, we simply use ComponentDefinition in default which includes interface to be used.
        return mapping.get(self, ComponentDefinition)


class ControlComponentType(Enum):
    IfElse = "IfElse"

    @classmethod
    def get_control_function_name(cls, control_type):
        mapping = {
            cls.IfElse: 'dsl.condition'
        }
        if type(control_type) == str:
            control_type = cls.__members__.get(control_type)
        function_name = mapping.get(control_type)
        if not function_name:
            raise UserErrorException(
                f'Get control type {control_type!r} function name failed,'
                f'please upgrade your sdk version and try again.')
        return function_name

    @classmethod
    def get_control_type_edge_param_mapping(cls, control_type):
        mapping = {
            cls.IfElse: {
                True.__repr__().lower(): 'true_block',
                False.__repr__().lower(): 'false_block',
                'condition': 'condition',
            }
        }
        if type(control_type) == str:
            control_type = cls.__members__.get(control_type)
        edge_param_mapping = mapping.get(control_type)
        if not edge_param_mapping:
            raise UserErrorException(
                f'Get control type {control_type!r} edge parameter mapping failed,'
                f'please upgrade your sdk version and try again.')
        return edge_param_mapping


class ComponentDefinition(Component, TelemetryMixin):
    r"""Represents a Component asset version.

    ComponentDefinition is immutable class.
    """
    SCHEMA_KEY = '$schema'
    SCHEMA = 'https://componentsdk.azureedge.net/jsonschema/CommandComponent.json'
    HELP_DOC_KEY = 'helpDocument'
    CONTACT_KEY = 'contact'
    CODE_GEN_BY_KEY = 'codegenBy'
    DSL_COMPONENT = 'dsl.component'
    TYPE = ComponentType.Component
    TYPE_VERSION_PATTERN = re.compile(r"(\S+)@.*$")
    DEFAULT_SPEC_FILE = 'spec.yaml'
    DEFAULT_CONDA_FILE = 'conda.yaml'

    def __init__(
        self, name, version=None, display_name=None,
        description=None, tags=None, is_deterministic=None,
        inputs=None, parameters=None, outputs=None,
        runsettings: RunSettingsDefinition = None,
        workspace=None,
        creation_context=None,
        registration_context=None,
        namespace=None,  # add namespace to be compatible with legacy usage
        snapshot_id=None,
        feed_name=None,
        registry_name=None
    ):
        super().__init__()
        """Initialize the component."""
        self._name = name
        self._namespace = namespace
        self._type = self.TYPE
        self._version = version
        self._display_name = display_name
        self._description = description
        self._tags = tags
        self._is_deterministic = is_deterministic
        self._feed_name = feed_name
        self._registry_name = registry_name
        inputs = inputs or {}
        parameters = parameters or {}
        outputs = outputs or {}
        # Here we accept two kinds of input/parameters/outputs.
        # 1. A Python dict, in this case, we use the dict to initialize definitions;
        # 2. A types defined in dsl.types or a definition,
        # which has correct interface and could be converted to component specification,
        # TODO: Use one centralized class from dsl.types instead of keeping both.
        # Currently we don't do that because it will introduce complicated imports.
        # We need to carefully redesign the whole package to avoid this.
        self._inputs = {
            name: data if not isinstance(data, dict) else Input._from_dict({'name': name, **data})
            for name, data in inputs.items()
        }
        self._parameters = ComponentDefinition._restore_parameters(parameters)
        self._outputs = {
            name: data if not isinstance(data, dict) else Output._from_dict({'name': name, **data})
            for name, data in outputs.items()
        }
        self._runsettings = runsettings
        self._workspace = workspace
        self._creation_context = creation_context
        self._registration_context = registration_context
        self._snapshot_id = snapshot_id
        self._snapshot_local_cache = None
        self._spec_file_path = None
        self._api_caller = None

        # Used to store the workspace and the corresponding identifier, key is workspace id, value is identifier.
        self._workspace_identifier_dict = {}
        # self._validate_input_output_duplicate()
        # additional AML ignore file
        self._additional_aml_ignore_file = None

    @property
    def name(self) -> str:
        """Return the name of the component."""
        if self._namespace is not None:
            # If self._namespace is not None, it's a legacy module, we combine namespace and name as it's name
            return '{}://{}'.format(self._namespace, self._name)
        return self._name

    @property
    def display_name(self) -> str:
        """
        Return the display_name of the component.
        If display_name is None, return name without namespace instead.
        """
        if self._display_name is not None:
            return self._display_name
        elif "://" in self.name:
            # if the name contains '://', component.run will fail with environment.register return 404
            return self.name.split("://")[-1]
        else:
            return self.name

    @property
    def version(self) -> str:
        """Return the version of the component."""
        return self._version

    @property
    def type(self) -> ComponentType:
        """Return the type of the component."""
        return self._type

    @property
    def inputs(self) -> Dict[str, Input]:
        """Return the inputs of the component."""
        return self._inputs

    @property
    def parameters(self) -> Dict[str, _Param]:
        """Return the parameters of the component."""
        return self._parameters

    @property
    def outputs(self) -> Dict[str, Output]:
        """Return the outputs of the component."""
        return self._outputs

    @property
    def description(self):
        """Return the description of the component."""
        return self._description

    @property
    def tags(self):
        """Return the tags of the component."""
        return self._tags or {}

    @property
    def contact(self):
        """Return the contact of the component."""
        return self.tags.get(self.CONTACT_KEY)

    @property
    def help_document(self):
        """Return the help document of the component."""
        return self.tags.get(self.HELP_DOC_KEY)

    @property
    def is_deterministic(self) -> bool:
        """Return whether the component is deterministic."""
        return self._is_deterministic

    @property
    def workspace(self) -> Workspace:
        """Return the workspace of the component."""
        return self._workspace

    @property
    def creation_context(self):
        # If component is not initialized from module dto, create an empty CreationContext.
        if self._creation_context is None:
            self._creation_context = CreationContext({})
        return self._creation_context

    @creation_context.setter
    def creation_context(self, val):
        """Set creation context for ComponentDefinition."""
        self._creation_context = val

    @property
    def registration_context(self):
        # If component is not initialized from module dto, create an empty RegistrationContext.
        if self._registration_context is None:
            self._registration_context = RegistrationContext({})
        return self._registration_context

    @registration_context.setter
    def registration_context(self, val):
        """Set registration context for ComponentDefinition."""
        self._registration_context = val

    @property
    def identifier(self):
        """Return the identifier of the component(unique in one workspace)."""
        return self.registration_context.id

    @property
    def runsettings(self) -> RunSettingsDefinition:
        """Return the run settings definition of the component."""
        return self._runsettings

    @property
    def snapshot_id(self) -> str:
        """Return the snapshot if of the component."""
        return self._snapshot_id

    @property
    def _is_pipeline_component_definition(self):
        return self._type == ComponentType.PipelineComponent

    @property
    def api_caller(self):
        """CRUD layer to call rest APIs."""
        if self._api_caller is None:
            self._api_caller = ComponentAPI(self.workspace, logger=logger, registry=self.registry_name)
        return self._api_caller

    @property
    def _workspace_independent(self) -> bool:
        """Return whether the component is workspace independent."""
        return self.workspace is None

    @property
    def registry_name(self) -> str:
        """Return the registry name of the component."""
        return self._registry_name

    @api_caller.setter
    def api_caller(self, api_caller):
        """Setter for api caller."""
        self._api_caller = api_caller

    @staticmethod
    def list(workspace=None, include_disabled=False, name=None, registry_name=None) -> Sequence['ComponentDefinition']:
        """Return a list of components in the workspace or registry.

        :param workspace: The workspace from which to list component definitions.
        :type workspace: azureml.core.workspace.Workspace
        :param include_disabled: Include disabled modules in list result
        :type include_disabled: bool
        :param name: List the specified component by component name
        :type name: str
        :param registry_name: Registry name. If both workspace and registry are passed in,
            it will use registry to list components.
        :type registry_name: str
        :return: A list of module objects.
        :rtype: builtin.list['ComponentDefinition']
        """
        if not workspace and not registry_name:
            raise UserErrorException("One of workspace and registry must be specified.")
        api_caller = ComponentAPI(workspace=workspace if not registry_name else None, logger=logger,
                                  registry=registry_name)
        if name:
            if registry_name:
                # For registry component, calling the list registry component api with the component name
                # can get the corresponding components.
                return api_caller.list(include_disabled=include_disabled, name=name)
            else:
                # For workspace component, calling get component versions api to get the corresponding components.
                return api_caller.get_versions(component_name=name).values()
        else:
            return api_caller.list(include_disabled=include_disabled)

    @staticmethod
    def get(
            workspace: Workspace, name: str, version: str = None, registry_name: str = None, **kwargs
    ) -> 'CommandComponentDefinition':
        """Get the component definition object from the workspace.

        :param workspace: The workspace that contains the component.
        :type workspace: azureml.core.workspace.Workspace
        :param name: The name of the component to return.
        :type name: str
        :param namespace: The namespace of the component to return.
        :type namespace: str
        :param version: The version of the component to return.
        :type version: str
        :param registry_name: The registry name of the component
        :type registry_name: str
        :return: The component definition object.
        :rtype: azure.ml.component.core.ComponentDefinition
        """
        api_caller = ComponentAPI(workspace=workspace, logger=logger, registry=registry_name)
        feed_name = kwargs.get("feed_name", None)
        component = api_caller.get(
            name=name,
            version=version,  # If version is None, this will get the default version
            feed_name=feed_name
        )
        component.api_caller = api_caller
        return component

    @staticmethod
    def register(workspace, spec_file, package_zip, anonymous_registration: bool,
                 set_as_default, amlignore_file, version):
        """Register the component to workspace.

        :param workspace: The workspace that contains the component.
        :type workspace: azureml.core.workspace.Workspace
        :param spec_file: The component spec file. Accepts either a local file path, a GitHub url,
                           or a relative path inside the package specified by --package-zip.
        :type spec_file: Union[str, None]
        :param package_zip: The zip package contains the component spec and implementation code.
                           Currently only accepts url to a DevOps build drop.
        :type package_zip: Union[str, None]
        :param anonymous_registration: Whether to register the component as anonymous.
        :type anonymous_registration: bool
        :param set_as_default: Whether to update the default version.
        :type set_as_default: Union[str, None]
        :param amlignore_file: The .amlignore or .gitignore file used to exclude files/directories in the snapshot.
        :type amlignore_file: Union[str, None]
        :param version: If specified, registered component will use specified value as version
                                           instead of the version in the yaml.
        :return: The component definition.
        :rtype: azure.ml.component.core.ComponentDefinition
        """
        raise NotImplementedError

    def validate(self):
        """Validate whether the component is valid."""
        raise NotImplementedError

    def enable(self):
        """Enable a component in the workspace.

        :return: The updated component object.
        :rtype: azure.ml.component.core.ComponentDefinition
        """
        raise NotImplementedError

    def disable(self):
        """Disable a component in the workspace.

        :return: The updated component object.
        :rtype: azure.ml.component.core.ComponentDefinition
        """
        raise NotImplementedError

    # This func is used by aml-ds, should be treated as public api
    # TODO: currently we don't support additional_includes
    # In future, we can leverage `ComponentSnapshot` class to do it.
    @classmethod
    def load(cls, yaml_file, *, _construct_local_runsettings=False) -> Union[
        'CommandComponentDefinition', 'ParallelComponentDefinition', 'DistributedComponentDefinition',
        'HDInsightComponentDefinition', 'ScopeComponentDefinition', 'SweepComponentDefinition',
        'DataTransferComponentDefinition'
    ]:
        """Load a component definition from a component yaml file."""
        try:
            with open(yaml_file, encoding='utf-8') as fin:
                data = YAML.safe_load_with_raw_enum_values(fin)
            if not isinstance(data, dict):
                raise UserErrorException('Load yaml data failed, data is None, please check yaml format.')
        except BaseException as e:
            raise YamlLoadingError(yaml_file, inner_exception=e)
        # Validate outputs in yaml file.
        if data.get("outputs"):
            for key, value in data["outputs"].items():
                if not value or not isinstance(value, dict) or not value.get("type"):
                    raise UserErrorException(f'Schema error of yaml file, '
                                             f'missing required properties "type" under outputs.{key}. '
                                             f'Please check if the schema of outputs.{key} is valid, '
                                             f'this may be caused by incorrect indentation.')
        type_str = data.get('type')
        # Add base dir to dct
        code = data.get('code') or '.'
        base_dir = (Path(yaml_file).parent / code).resolve().as_posix()
        definition_cls = ComponentType.get_component_type_by_str(
            type_str, default=ComponentType.CommandComponent).get_definition_class()
        definition = definition_cls._from_dict(
            data, base_dir=base_dir, is_local=True, _construct_local_runsettings=_construct_local_runsettings)
        # Record snapshot path and spec file path
        definition._snapshot_local_cache = base_dir
        definition._spec_file_path = _relative_path(Path(yaml_file).resolve(), base_dir)
        if not definition._spec_file_path:
            # can't get relative path, save the absolute path
            definition._spec_file_path = Path(yaml_file).resolve()
        return definition

    def _dump_to_stream(self, stream):
        """Dump the component definition to stream with specific style."""
        data = _to_ordered_dict(self._to_dict())
        YAML(typ='unsafe', with_additional_representer=True).dump(data, stream)

    def save(self, yaml_file):
        """Dump the component definition to a component yaml file.

        :param yaml_file: The target yaml file path
        :type yaml_file: str
        """
        with open(yaml_file, 'w') as fout:
            self._dump_to_stream(fout)

    @classmethod
    def _from_dict(
            cls, dct, ignore_unexpected_keywords=True, base_dir=None, is_local=False,
            _construct_local_runsettings=False
    ) -> ['ComponentDefinition', 'CommandComponentDefinition',
          'ParallelComponentDefinition', 'DistributedComponentDefinition']:
        """Load a component definition from a component yaml dict."""
        # TODO: Load the dict according to the schema version.
        if cls.SCHEMA_KEY in dct:
            dct.pop(cls.SCHEMA_KEY)

        component_type = None if 'type' not in dct else dct.pop('type')
        component_type = cls._extract_type(component_type)
        # If the component type exists in the ComponentType.
        # Check the component type defined in yaml is equal to the type defined in the component definition class.
        unknown_component_type = component_type and component_type not in ComponentType._value2member_map_
        if cls.TYPE not in {None, ComponentType.Component} \
                and component_type and component_type not in {None, cls.TYPE.value} \
                and not unknown_component_type:
            # Dict is from user yaml if is local.
            # Change error category as user error if read local yaml.
            ex = TypeError("The type must be %r." % cls.TYPE.value)
            raise UserErrorException(str(ex)) if is_local else ex

        # Distinguish inputs and parameters from original yaml dict if parameters is not specified.
        if not dct.get('parameters'):
            inputs = dct.pop('inputs') if 'inputs' in dct else {}
            if inputs is None:
                raise UserErrorException('Schema error of yaml file, Missing value under inputs')
            types = {k: data.get('type', None) if isinstance(data, dict) else getattr(data, 'type', None)
                     for k, data in inputs.items()}
            for key, val in types.items():
                if val is None:
                    raise UserErrorException(f'Schema error of yaml file, '
                                             f'Missing required properties "type" under inputs.{key}')
            dct['inputs'] = {
                k: data for k, data in inputs.items() if not _Param._is_valid_type(types[k])
            }
            dct['parameters'] = {
                k: data for k, data in inputs.items() if _Param._is_valid_type(types[k])
            }

        if not dct.get('runsettings') and _construct_local_runsettings:
            step_type, dct = ComponentType._get_step_type(cls.TYPE, dct, base_dir=base_dir, return_dct=True)
            if step_type:
                run_setting_parameters = _DesignerServiceCallerFactory.get_instance(None).\
                    get_component_run_setting_parameters_mapping().get(step_type)
                run_setting_parameters = ModuleDto.correct_run_settings(run_setting_parameters)
                dct['runsettings'] = RunSettingsDefinition.from_dto_runsettings(run_setting_parameters)

        valid_parameters = inspect.signature(cls).parameters
        for key in [k for k in dct]:
            if key not in valid_parameters:
                if ignore_unexpected_keywords or unknown_component_type:
                    dct.pop(key)
                else:
                    ex = KeyError("The dict contain an unexpected keyword '%s'." % key)
                    # Dict is from user yaml if is local.
                    # Change error category as user error if read local yaml.
                    raise UserErrorException(str(ex)) if is_local else ex
        component_definition = cls(**dct)
        if unknown_component_type:
            # Update component type of the definition when it not exist in ComponentType
            component_definition._type = Enum(component_type, {component_type: component_type})[component_type]
        return component_definition

    def _to_dict(self):
        """Convert the component definition to a python dict."""
        # Currently we combine inputs/parameters
        inputs = {
            **{key: val._to_dict(remove_name=True) for key, val in self.inputs.items()},
            **{key: val._to_dict(remove_name=True) for key, val in self.parameters.items()}
        }
        outputs = {key: val._to_dict(remove_name=True) for key, val in self.outputs.items()}
        result = {
            self.SCHEMA_KEY: self.SCHEMA,
            'name': self.name,
            'version': self.version,
            'display_name': self.display_name,
            'type': self.type.value,
            'description': self.description,
            'is_deterministic': self.is_deterministic,
            'tags': self.tags,
            'inputs': inputs,
            'outputs': outputs,
        }
        # We don't remove empty values of tags since it may contains the values like {tag: None}
        result = _remove_empty_values(result, ignore_keys={'tags'})
        # code: . is not supported by MT, the replacement is removing it
        if 'code' in result and result['code'] == '.':
            result['code'] = None
        return result

    VALID_NAME_CHARS = set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._-')

    @classmethod
    def is_valid_name(cls, name: str):
        """Indicate whether the name is a valid component name."""
        return all(c in cls.VALID_NAME_CHARS for c in name)

    @classmethod
    def _extract_type(cls, component_type):
        # To handle load unregistered component that component type version in component type.
        type_groups = re.match(cls.TYPE_VERSION_PATTERN, component_type) if component_type else None
        if type_groups:
            component_type = type_groups.group(1)
        return component_type

    @staticmethod
    def _restore_group_recursively(values):
        """Restore group with sub groups."""
        for key, val in values.items():
            if type(val) == dict:
                values[key] = ComponentDefinition._restore_group_recursively(val)
        return _Group(values)

    @staticmethod
    def _restore_parameters(parameters):
        definition_parameters = {}
        group_parameters = {}
        for name, data in parameters.items():
            if not isinstance(data, dict):
                definition_parameters[name] = data
                continue
            group_names = data.get('group_names', None)
            if not group_names:
                definition_parameters[name] = _Param._from_dict({'name': name, **data})
                continue
            # create or insert into dict value
            target_dict = group_parameters
            for group_name in group_names:
                if group_name not in target_dict:
                    target_dict[group_name] = {}
                target_dict = target_dict[group_name]
            # build group parameters values dict
            param_name = name.replace(f"{'_'.join(group_names)}_", '')
            target_dict[param_name] = _Param._from_dict({**data, 'name': param_name})
        # add group parameters into definition parameters dict
        for k, values in group_parameters.items():
            definition_parameters[k] = ComponentDefinition._restore_group_recursively(values)
            definition_parameters[k]._update_name(k)
        return definition_parameters

    def get_snapshot(self, target=None, overwrite=False) -> Path:
        """Get the snapshot in target folder, if target is None, the snapshot folder is returned."""
        if target is not None:
            target = _ensure_target_folder_exist(target, overwrite)
        if self._snapshot_local_cache and Path(self._snapshot_local_cache).exists():
            if target is None:
                return self._snapshot_local_cache
            shutil.copytree(str(self._snapshot_local_cache), str(target))
        else:
            # Make sure the snapshot id exists.
            if self.snapshot_id is None:
                raise UserErrorException(
                    "Given component {} does not have a snapshot id, so it doesn't support download.".format(
                        self.name))
            if target is None:
                target = mkdtemp()
            _download_snapshot_by_id(self.api_caller, self.snapshot_id, target, self.name, self._registry_name)
            self._snapshot_local_cache = target
            return target

    def get_snapshot_spec_file_path(self) -> Path:
        """Get the specification yaml file path in the snapshot folder by checking name and version."""
        snapshot_spec_file_path = None
        for filename in os.listdir(self._snapshot_local_cache):
            if not (filename.endswith('.yaml') or filename.endswith('.yml')):
                continue
            file_path = os.path.join(self._snapshot_local_cache, filename)
            with open(file_path, encoding='utf-8') as fin:
                data = YAML.safe_load_with_raw_enum_values(fin)
            if data['name'] == self.name and str(data['version']) == self.version:
                snapshot_spec_file_path = file_path
                break
        return Path(snapshot_spec_file_path)

    def _identifier_in_workspace(self, workspace=None):
        """Get the identifier of component, if component is workspace independent, workspace is required."""
        if self._workspace_independent:
            if not workspace:
                return None
            else:
                return self._workspace_identifier_dict.get(workspace._workspace_id, None)
        else:
            return self.identifier

    def _registered(self, workspace=None) -> bool:
        """Return whether the ComponentDefinition is registered in the workspace."""
        if self._workspace_independent:
            if workspace:
                return self._identifier_in_workspace(workspace) is not None
            else:
                return False
        else:
            return self.workspace is not None and self.identifier is not None

    def _register_workspace_independent_component(self, workspace, package_zip,
                                                  anonymous_registration: bool, set_as_default,
                                                  amlignore_file, version, registry_name=None):
        if not self._snapshot_local_cache or not self._spec_file_path:
            raise ValueError("Not find the spec file of component definition, "
                             "the workspace independent component cannot be registered.")
        spec_file = os.path.join(self._snapshot_local_cache, self._spec_file_path)
        if workspace._workspace_id not in self._workspace_identifier_dict:
            definition = CommandComponentDefinition.register(workspace=workspace, spec_file=spec_file,
                                                             package_zip=package_zip,
                                                             anonymous_registration=anonymous_registration,
                                                             set_as_default=set_as_default,
                                                             amlignore_file=amlignore_file,
                                                             version=version, registry_name=registry_name)
            if not self._workspace_identifier_dict:
                # When workspace independent component is first registered,
                # using the registered definition to update workspace independent component definition.
                self._module_dto = definition._module_dto
                self._creation_context = definition._creation_context
                self._registration_context = definition._registration_context
                self._runsettings = definition._runsettings
                self._inputs = definition.inputs
                self._parameters = definition.parameters
                # For sweep component, the output type is metrics or model, will be changed to AnyFile after registered
                self._outputs = definition.outputs
                if hasattr(definition, "_environment"):
                    self._environment = definition._environment
                if hasattr(definition, '_is_command'):
                    self._is_command = definition._is_command
            # Update the dict of workspace id and identifier.
            self._workspace_identifier_dict[workspace._workspace_id] = definition.identifier
        return self._workspace_identifier_dict[workspace._workspace_id]

    def _validate_input_output_duplicate(self):
        """Validate if there are duplicated names in inputs and outputs, raise error if yes."""
        input_names = set(self._inputs.keys()).union(set(self._parameters.keys()))
        output_names = set(self._outputs.keys())
        duplicate_port = input_names & output_names
        if duplicate_port:
            raise UserErrorException(
                f"{self.name!r} got duplicated name(s) {duplicate_port!r} between inputs and outputs.")

    def _save_to_code_folder(self, folder, spec_file=None):
        """Save the module spec to specific folder under the source directory."""
        pass

    def _get_telemetry_values(self):
        telemetry_values = super()._get_telemetry_values()
        if self._module_dto:
            telemetry_values.update(self._module_dto._get_telemetry_values(workspace=self.workspace))
        return telemetry_values

    @track(activity_name="ComponentDefinition_to_func")
    def to_component_func(self, component_creation_func) -> Callable:
        """Add this to track basic info from component definition."""
        from azure.ml.component._component_func import to_component_func_from_definition
        return to_component_func_from_definition(definition=self,
                                                 component_creation_func=component_creation_func)


class CommandComponentDefinition(ComponentDefinition):
    r"""represents a Component asset version.

    ComponentDefinition is immutable class.
    """
    SCHEMA = 'https://componentsdk.azureedge.net/jsonschema/CommandComponent.json'
    TYPE = ComponentType.CommandComponent

    def __init__(self, name, version=None, display_name=None,
                 description=None, tags=None, is_deterministic=None,
                 inputs=None, parameters=None, outputs=None,
                 runsettings: RunSettingsDefinition = None,
                 command=None, environment=None,
                 code=None,
                 workspace=None,
                 creation_context=None,
                 registration_context=None,
                 namespace=None,  # add namespace to be compatible with legacy usage
                 successful_return_code=SuccessfulCommandReturnCode.ZERO,
                 is_command=True,
                 snapshot_id=None,
                 feed_name=None,
                 registry_name=None
                 ):
        """Initialize a CommandComponentDefinition from the args."""
        super().__init__(
            name=name, namespace=namespace, version=version, display_name=display_name,
            description=description,
            tags=tags,
            is_deterministic=is_deterministic,
            inputs=inputs, parameters=parameters, outputs=outputs,
            runsettings=runsettings,
            workspace=workspace,
            creation_context=creation_context,
            registration_context=registration_context,
            snapshot_id=snapshot_id,
            feed_name=feed_name,
            registry_name=registry_name
        )
        self._command = command
        if isinstance(environment, dict):
            environment = Environment._from_dict(environment)
        self._environment = environment
        self._code = code
        self._snapshot_local_cache = None

        # This field is used for telemetry when loading the component from a workspace,
        # a new name may be required since the interface has been changed to `get` instead of `load`
        self._load_source = None

        # This property is a workaround to unblock the implementation of Component,
        # will be removed after all the implementations are ready.
        self._module_dto = None

        # Whether is a command component running a non-python command or python script.
        self._is_command = is_command

        # This property is used to specify how command return code is interpreted.
        self._successful_return_code = successful_return_code

    @property
    def command(self):
        """Return the command of the CommandComponentDefinition."""
        return self._command

    @property
    def environment(self) -> Environment:
        """Return the environment of the CommandComponentDefinition."""
        if self._environment is None:
            self._environment = Environment()
        return self._environment

    @property
    def code(self):
        """Return the source code directory of the CommandComponentDefinition."""
        return self._code or '.'

    @property
    def successful_return_code(self):
        """Return the successful return code that is used to specify how command return code is interpreted."""
        return self._successful_return_code

    @property
    def is_command(self) -> bool:
        """
        Return whether the component command is a non-python command.
        If true, it's a non-python command will directly exeucte command in subprocess,
        else it's python script style command and it will use runpy to invoke.
        """
        return self._is_command

    def _to_dict(self) -> dict:
        """Convert the component definition to a python dict."""
        result = super()._to_dict()
        values_to_update = {
            'command': self._reformat_command(self.command),
            'environment': self.environment._to_dict() if self.environment is not None else None,
            'code': self.code if self.code != '.' else None,
        }
        result.update(_remove_empty_values(values_to_update))
        return result

    @staticmethod
    def get_by_id(workspace: Workspace, _id: str):
        """Get the component definition object by its id from the workspace."""
        api_caller = ComponentAPI(workspace=workspace, logger=logger)
        component = api_caller.get_by_id(_id)
        component.api_caller = api_caller
        return component

    @staticmethod
    def batch_get(workspace: Workspace, module_version_ids, selectors):
        """Batch get component definition objects by their id or identifiers."""
        api_caller = ComponentAPI(workspace=workspace, logger=logger)
        result = api_caller.batch_get(module_version_ids, selectors)
        for d in result:
            d.api_caller = api_caller

        return result

    @staticmethod
    @wrap_azureml_exception_with_identifier()
    def register(workspace, spec_file, package_zip, anonymous_registration: bool,
                 set_as_default, amlignore_file, version, registry_name=None):
        """Register from yaml file or URL"""
        api_caller = ComponentAPI(workspace=workspace, logger=logger, registry=registry_name)
        definition = api_caller.register(spec_file=spec_file, package_zip=package_zip,
                                         anonymous_registration=anonymous_registration,
                                         set_as_default=set_as_default,
                                         amlignore_file=amlignore_file, version=version)
        if anonymous_registration:
            repr_dict = {
                "name": definition.name,
                "type": definition.type.value,
                "registry": definition.registry_name,
                "workspace": workspace.name,
                "subscriptionId": workspace.subscription_id,
                "resourceGroup": workspace.resource_group,
            }
            logger.info("Created Anonymous Component: %s" % repr_dict)
        return definition

    @staticmethod
    def _register_module(workspace, spec_file, package_zip, anonymous_registration: bool,
                         set_as_default, amlignore_file, version):
        """Only used for backward compatibility. Register from yaml file or URL"""
        api_caller = ModuleAPI(workspace=workspace, logger=logger)
        return api_caller.register(spec_file=spec_file, package_zip=package_zip,
                                   anonymous_registration=anonymous_registration,
                                   set_as_default=set_as_default,
                                   amlignore_file=amlignore_file, version=version)

    @classmethod
    def load(cls, yaml_file, *, _construct_local_runsettings=False) -> Union[
        'CommandComponentDefinition', 'ParallelComponentDefinition', 'DistributedComponentDefinition',
        'HDInsightComponentDefinition',
    ]:
        result = super().load(yaml_file=yaml_file)
        result._snapshot_local_cache = Path(Path(yaml_file).parent / result.code)
        result._spec_file_path = str(Path(yaml_file).relative_to(result._snapshot_local_cache))
        return result

    @classmethod
    def _from_dict(
            cls, dct, ignore_unexpected_keywords=True, base_dir=None, **kwargs
    ) -> 'CommandComponentDefinition':
        """Load a component definition from a component yaml dict."""
        # Create environment first
        if isinstance(dct.get('environment'), dict):
            from ._environment import Environment
            env = Environment._from_dict(dct['environment'], base_dir=base_dir)
            dct['environment'] = env
        return super()._from_dict(dct, ignore_unexpected_keywords=ignore_unexpected_keywords, **kwargs)

    @staticmethod
    def _reformat_command(command):
        """Reformat the command to make the output yaml clear."""
        if isinstance(command, str):
            return YamlMultiLineStr(command)
        if command is None:  # Parallel/HDI doesn't have command.
            return command
        # TODO: Remove the following logic since component yaml doesn't support list command anymore.
        # Here we call YamlFlowList and YamlFlowDict to have better representation when dumping args to yaml.
        result = []
        for arg in command:
            if isinstance(arg, list):
                arg = [YamlFlowDict(item) if isinstance(item, dict) else item for item in arg]
                arg = YamlFlowList(arg)
            result.append(arg)
        return result

    @classmethod
    def _module_yaml_convert_arg_item(cls, arg, inputs, parameters, outputs):
        """Convert one arg item in old style yaml to new style."""
        if isinstance(arg, (str, int, float)):
            return arg
        if isinstance(arg, list):
            return cls._module_yaml_convert_args(arg, inputs, parameters, outputs)
        if not isinstance(arg, dict) or len(arg) != 1:
            raise ValueError("Arg item is not valid: %r" % arg)
        key, value = list(arg.items())[0]
        for value_key in ['inputs', 'outputs', 'parameters']:
            items = locals()[value_key]
            # Parameters are also $inputs.xxx
            if value_key == 'parameters':
                value_key = 'inputs'
            for item in items:
                if item['name'] == value:
                    return '{%s.%s}' % (value_key, item['argumentName'])
        raise ValueError("%r is not in inputs and outputs." % value)

    @classmethod
    def _module_yaml_convert_args(cls, args, inputs, parameters, outputs):
        """Convert the args in old style yaml to new style."""
        return [cls._module_yaml_convert_arg_item(arg, inputs, parameters, outputs) for arg in args] if args else []

    @classmethod
    def _construct_dict_from_module_definition(cls, module):
        """Construct the component dict from an old style ModuleDefinition."""
        inputs, parameters, outputs = module.input_ports, module.params, module.output_ports
        for item in inputs + parameters + outputs:
            if 'argumentName' not in item:
                item['argumentName'] = _sanitize_python_variable_name(item['name'])
            if 'options' in item:
                # This field is different in old module definition and vNext definition.
                item['enum'] = item.pop('options')

        command = module.command or []
        command += cls._module_yaml_convert_args(module.args, inputs, parameters, outputs)
        # Convert the command from list to string
        command = ' '.join(arg if isinstance(arg, str) else '[%s %s]' % (arg[0], arg[1]) for arg in command)

        input_pairs = [(item.pop('argumentName'), item) for item in inputs]
        parameter_pairs = [(item.pop('argumentName'), item) for item in parameters]
        output_pairs = [(item.pop('argumentName'), item) for item in outputs]

        env = module.aml_environment or {}
        if env and 'python' in env:
            env['conda'] = env.pop('python')
        if module.image:
            env.update({'docker': {'image': module.image}})

        # Get tags according to the old yaml.
        tags = {key: None for key in module.tags} if module.tags else {}
        if module.help_document:
            tags[cls.HELP_DOC_KEY] = module.help_document
        if module.contact:
            tags[cls.CONTACT_KEY] = module.contact
        if cls.CODE_GEN_BY_KEY in module.annotations:
            tags[cls.CODE_GEN_BY_KEY] = module.annotations[cls.CODE_GEN_BY_KEY]

        # Convert the name to make sure only valid characters
        name = '%s://%s' % (module.namespace, module.name) if module.namespace else module.name
        name = name.lower().replace('://', '.').replace('/', '.').replace(' ', '_')
        new_dct = {
            'name': name,
            # This is a hard code rule.
            'version': module.version,
            'display_name': module.name,
            'is_deterministic': module.is_deterministic,
            'description': module.description,
            'tags': tags,
            'type': cls.TYPE.value,
            'inputs': {key: value for key, value in input_pairs},
            'parameters': {key: value for key, value in parameter_pairs},
            'outputs': {key: value for key, value in output_pairs},
            'command': command,
            'environment': env,
            'code': module.source_directory,
        }
        return new_dct

    @staticmethod
    def _from_module_yaml_dict(dct) -> 'CommandComponentDefinition':
        """Load the component from the old style module yaml dict."""
        from ..dsl._module_spec import _YamlModuleDefinition, _YamlParallelModuleDefinition, \
            _YamlHDInsightModuleDefinition
        definition_cls, cls = _YamlModuleDefinition, CommandComponentDefinition
        job_type = dct.get('jobType')
        if job_type is not None:
            if job_type.lower() == 'parallel':
                definition_cls, cls = _YamlParallelModuleDefinition, ParallelComponentDefinition
            elif job_type.lower() == 'hdinsight':
                definition_cls, cls = _YamlHDInsightModuleDefinition, HDInsightComponentDefinition
            elif job_type.lower() == 'mpi':
                definition_cls, cls = _YamlModuleDefinition, DistributedComponentDefinition
        module = definition_cls(dct)
        return cls._from_dict(cls._construct_dict_from_module_definition(module))

    @classmethod
    def _from_module_yaml_file(cls, f):
        """Load the component from the old style module yaml file."""
        with open(f) as fin:
            return cls._from_module_yaml_dict(YAML().load(fin))

    def _save_to_code_folder(self, folder, spec_file=None):
        """Save the module spec to specific folder under the source directory."""
        from ..dsl._module_spec import _Dependencies
        from .._util._utils import _relative_path

        if spec_file is None:
            spec_file = self.DEFAULT_SPEC_FILE
        source_directory = self.code if self.code else \
            Path(folder).resolve().absolute().as_posix()
        spec_file = (Path(folder) / spec_file).resolve()
        spec_dict = _to_ordered_dict(self._to_dict())

        spec_dict['code'] = _relative_path(source_directory, spec_file.parent)
        if not spec_dict['code']:
            # Reach here indicate source_directory and spec file path have different mount. like D:/ and C:/
            # Write code path as absolute path directly
            spec_dict['code'] = Path(source_directory).absolute()
        spec_dict['code'] = spec_dict['code'].as_posix()

        if spec_dict.get('code') == '.':
            spec_dict.pop('code')

        env = self.environment
        # Check whether we need to specify a default conda file in the folder containing the spec file.
        # The scenario is that conda_dependencies is not specified, while the conda is specified in dsl.component.
        if not env.name and not env.docker and not env.conda and \
                self._tags.get(self.CODE_GEN_BY_KEY) == self.DSL_COMPONENT:
            # if SDK is stable version, refer to default curated environment
            from azure.ml.component._version import VERSION
            if not VERSION.startswith('0.1'):
                spec_dict['environment'] = CURATED_ENV_DICT_FOR_EXPRESSION_COMPONENT
            else:
                spec_dict['environment']['conda'] = {
                    CoreConda.CONDA_DICT_KEY: _Dependencies.create_default().conda_dependency_dict}
                spec_dict['environment']['docker'] = CoreDocker(
                    image=CoreDocker.DEFAULT_CPU_IMAGE)._to_dict_in_vnext_format()

        YAML._dump_yaml_file(spec_dict, spec_file, unsafe=True, header=YAML.YAML_HELP_COMMENTS)


class DistributedComponentDefinition(CommandComponentDefinition):
    """The component definition of a MPI component,
    currently there is no difference with CommandComponentDefinition.
    """

    SCHEMA = 'https://componentsdk.azureedge.net/jsonschema/DistributedComponent.json'
    TYPE = ComponentType.DistributedComponent

    def __init__(self, name, version=None, display_name=None,
                 description=None, tags=None, is_deterministic=None,
                 inputs=None, parameters=None, outputs=None,
                 runsettings: RunSettingsDefinition = None,
                 launcher=None, environment=None,
                 code=None,
                 workspace=None,
                 creation_context=None,
                 registration_context=None,
                 successful_return_code=SuccessfulCommandReturnCode.ZERO,
                 is_command=True,
                 snapshot_id=None,
                 feed_name=None,
                 registry_name=None
                 ):
        super().__init__(
            name=name, version=version, display_name=display_name, description=description, tags=tags,
            is_deterministic=is_deterministic, inputs=inputs, parameters=parameters, outputs=outputs,
            runsettings=runsettings, environment=environment, code=code, workspace=workspace,
            creation_context=creation_context, registration_context=registration_context,
            successful_return_code=successful_return_code, is_command=is_command, snapshot_id=snapshot_id,
            feed_name=feed_name,
            registry_name=registry_name
        )
        if isinstance(launcher, dict):
            launcher = LauncherDefinition._from_dict(launcher)
        self._launcher = launcher

    @property
    def launcher(self) -> LauncherDefinition:
        return self._launcher

    def _to_dict(self) -> dict:
        dct = super()._to_dict()
        dct['launcher'] = self.launcher._to_dict()
        return dct

    @classmethod
    def _construct_dict_from_module_definition(cls, module):
        dct = super()._construct_dict_from_module_definition(module)
        dct['launcher'] = {
            'type': 'mpi',  # module definition only supports MPI
            'additional_arguments': dct.pop('command'),
        }
        return dct


class ParallelComponentDefinition(CommandComponentDefinition):
    """The component definition of a parallel component."""

    SCHEMA = 'https://componentsdk.azureedge.net/jsonschema/ParallelComponent.json'
    TYPE = ComponentType.ParallelComponent

    def __init__(self, name, version=None, display_name=None,
                 description=None, tags=None, is_deterministic=None,
                 inputs=None, parameters=None, outputs=None,
                 runsettings: RunSettingsDefinition = None,
                 input_data=None, output_data=None,
                 entry=None,
                 args=None, environment=None,
                 code=None,
                 workspace=None,
                 creation_context=None,
                 registration_context=None,
                 successful_return_code=SuccessfulCommandReturnCode.ZERO,
                 is_command=True,
                 snapshot_id=None,
                 feed_name=None,
                 registry_name=None):
        super().__init__(
            name=name, version=version, display_name=display_name,
            description=description, tags=tags,
            is_deterministic=is_deterministic, inputs=inputs, parameters=parameters, outputs=outputs,
            command=None, environment=environment, runsettings=runsettings,
            code=code,
            workspace=workspace, creation_context=creation_context, registration_context=registration_context,
            successful_return_code=successful_return_code, is_command=is_command, snapshot_id=snapshot_id,
            feed_name=feed_name, registry_name=registry_name
        )
        input_data_list = input_data if isinstance(input_data, list) else [input_data]
        self._input_data = None if not input_data else [self._extract_input_name(data) for data in input_data_list]
        self._output_data = None if not output_data else self._extract_output_name(output_data)
        self._entry = entry
        self._args = args
        if args is not None and not isinstance(args, str):
            raise TypeError("Args must be type str, got %r" % (type(args)))
        self._job_type = 'parallel'

    @property
    def input_data(self) -> Sequence[str]:
        return self._input_data

    @property
    def output_data(self) -> str:
        return self._output_data

    @property
    def entry(self) -> str:
        return self._entry

    @property
    def args(self) -> str:
        return self._args

    @classmethod
    def _construct_dict_from_module_definition(cls, module):
        dct = super()._construct_dict_from_module_definition(module)
        # Use name mapping to make sure input_data/output_data are correct
        # since the component definition uses argument name as the key
        name_mapping = {}
        for item in module.input_ports + module.output_ports:
            name_mapping[item['name']] = item.get('argumentName', _sanitize_python_variable_name(item['name']))
        input_data = module.input_data if isinstance(module.input_data, list) else [module.input_data]
        dct['parallel'] = {
            'input_data': [name_mapping[i] for i in input_data],
            'output_data': name_mapping[module.output_data],
            'entry': module.entry,
            'args': dct.pop('command'),
        }
        return dct

    @classmethod
    def _from_dict(cls, dct, **kwargs) -> 'ParallelComponentDefinition':
        component_type = dct.pop('type') if 'type' in dct else None
        if component_type != cls.TYPE.value:
            raise ValueError("The type must be %r, got %r." % (cls.TYPE.value, component_type))
        if 'parallel' in dct:
            parallel = dct.pop('parallel')
            dct['input_data'] = parallel.get('input_data')
            dct['output_data'] = parallel.get('output_data')
            dct['entry'] = parallel.get('entry')
            if 'args' in parallel:
                dct['args'] = parallel['args']
        return super()._from_dict(dct, **kwargs)

    def _to_dict(self) -> dict:
        result = super()._to_dict()
        if not self.input_data:
            raise ValueError("Parallel component should have at least one input data, got 0.")
        parallel_section = {
            'parallel': {
                'input_data': YamlFlowList(['inputs.%s' % i for i in self.input_data]),
                'output_data': 'outputs.%s' % self.output_data,
                'entry': self.entry,
                'args': self._reformat_command(self.args),
            }}
        result.update(_remove_empty_values(parallel_section))
        return result

    def _extract_input_name(self, data: str):
        """Extract input name from inputs.xx"""
        format_err = ValueError("Input data %r of the parallel component is not 'inputs.xx' format." % data)
        if not isinstance(data, str) or data == '':
            raise format_err
        items = data.split('.')
        if (len(items) > 1 and (items[0] != 'inputs' or len(items) > 2)) or not data:
            raise format_err
        input_name = items[-1]  # Here we support two cases: 'inputs.xx' or 'xx'
        if input_name not in self._inputs:
            raise KeyError("Input data %r is not one of valid inputs, valid inputs: %r." % (
                input_name, set(self._inputs.keys())))
        return input_name

    def _extract_output_name(self, data: str):
        """Extract output name from outputs.xx"""
        format_err = ValueError("Output data %r of the parallel component is not 'outputs.xx' format." % data)
        if not isinstance(data, str) or data == '':
            raise format_err
        items = data.split('.')
        if len(items) > 1 and (items[0] != 'outputs' or len(items) > 2):
            raise format_err
        output_name = items[-1]  # Here we support two cases: 'outputs.xx' or 'xx'
        if output_name not in self._outputs:
            raise KeyError("Output data %r is not one of valid outputs, valid outputs: %r." % (
                output_name, set(self._outputs.keys())))
        return output_name


class HDInsightComponentDefinition(CommandComponentDefinition):
    """The component definition of a HDInsight component."""

    SCHEMA = 'https://componentsdk.azureedge.net/jsonschema/HDInsightComponent.json'
    TYPE = ComponentType.HDInsightComponent

    def __init__(self, name, version=None, display_name=None,
                 description=None, tags=None, is_deterministic=None,
                 inputs=None, parameters=None, outputs=None,
                 runsettings: RunSettingsDefinition = None,
                 command=None, environment=None,
                 file=None, files=None, class_name=None, jars=None,
                 py_files=None, archives=None, args=None,
                 code=None,
                 workspace=None,
                 creation_context=None,
                 registration_context=None,
                 snapshot_id=None,
                 feed_name=None,
                 registry_name=None):
        super().__init__(
            name=name, version=version, display_name=display_name, description=description, tags=tags,
            is_deterministic=is_deterministic, inputs=inputs, parameters=parameters, outputs=outputs,
            command=command, environment=environment, runsettings=runsettings,
            code=code,
            workspace=workspace, creation_context=creation_context, registration_context=registration_context,
            snapshot_id=snapshot_id, feed_name=feed_name, registry_name=registry_name
        )
        self._file = file
        self._files = files
        self._class_name = class_name
        self._jars = jars
        self._py_files = py_files
        self._archives = archives
        self._args = args

    @property
    def file(self) -> str:
        return self._file

    @property
    def files(self) -> Sequence[str]:
        return self._files

    @property
    def class_name(self) -> str:
        return self._class_name

    @property
    def jars(self) -> Sequence[str]:
        return self._jars

    @property
    def py_files(self) -> Sequence[str]:
        return self._py_files

    @property
    def archives(self) -> Sequence[str]:
        return self._archives

    @property
    def args(self) -> str:
        return self._args

    @property
    def environment(self) -> Environment:
        """This section does not work for HDI"""
        return None

    @classmethod
    def _construct_dict_from_module_definition(cls, module):
        dct = super()._construct_dict_from_module_definition(module)
        dct['hdinsight'] = {
            'file': module.file,
            'files': module.files,
            'class_name': module.class_name,
            'jars': module.jars,
            'py_files': module.py_files,
            'archives': module.archives,
            'args': dct.pop('command'),
        }
        return dct

    @classmethod
    def _from_dict(cls, dct, **kwargs) -> 'HDInsightComponentDefinition':
        job_type = None if 'jobType' not in dct else dct.pop('jobType')
        component_type = None if 'type' not in dct else dct.pop('type')
        if component_type is None:
            if job_type is None or job_type.lower() != 'hdinsight':
                raise ValueError("The job type must be hdinsight, got '%s'." % job_type)
        else:
            if component_type != ComponentType.HDInsightComponent.value:
                raise ValueError("The type must be '%s', got '%s'." %
                                 (ComponentType.HDInsightComponent, component_type))
        if 'hdinsight' in dct:
            hdinsight = dct.pop('hdinsight')
            dct['file'] = hdinsight.get('file')
            dct['files'] = hdinsight.get('files')
            dct['class_name'] = hdinsight.get('class_name')
            dct['jars'] = hdinsight.get('jars')
            dct['py_files'] = hdinsight.get('py_files')
            dct['archives'] = hdinsight.get('archives')
            dct['args'] = hdinsight.get('args')
        return super()._from_dict(dct, **kwargs)

    def _to_dict(self) -> dict:
        result = super()._to_dict()
        hdinsight_section = {
            'hdinsight': {
                'file': self._file,
                'files': self._files,
                'class_name': self._class_name,
                'jars': self._jars,
                'py_files': self._py_files,
                'archives': self._archives,
                'args': self._reformat_command(self.args),
            }}
        result.update(_remove_empty_values(hdinsight_section))
        return result


class ScopeComponentDefinition(ComponentDefinition):
    """The component definition of a Scope component."""

    SCHEMA = 'https://componentsdk.azureedge.net/jsonschema/ScopeComponent.json'
    TYPE = ComponentType.ScopeComponent

    def __init__(self, name, version=None, display_name=None,
                 description=None, tags=None, is_deterministic=None,
                 inputs=None, parameters=None, outputs=None,
                 runsettings: RunSettingsDefinition = None,
                 script=None,
                 args=None,
                 code=None,
                 workspace=None,
                 creation_context=None,
                 registration_context=None,
                 snapshot_id=None,
                 feed_name=None,
                 registry_name=None):
        super().__init__(
            name=name, version=version, display_name=display_name, description=description, tags=tags,
            is_deterministic=is_deterministic, inputs=inputs, parameters=parameters, outputs=outputs,
            runsettings=runsettings,
            workspace=workspace, creation_context=creation_context, registration_context=registration_context,
            snapshot_id=snapshot_id, feed_name=feed_name, registry_name=registry_name
        )
        self._code = code
        self._script = script
        self._args = args

    @property
    def code(self):
        """Return the source code directory of the ScopeComponentDefinition."""
        return self._code or '.'

    @property
    def script(self) -> str:
        return self._script

    @classmethod
    def _from_dict(cls, dct, base_dir=None, **kwargs) -> 'ScopeComponentDefinition':
        component_type = None if 'type' not in dct else dct.pop('type')
        if component_type != cls.TYPE.value:
            raise ValueError("The type must be %r, got %r." % (cls.TYPE.value, component_type))

        if 'scope' in dct:
            scope = dct.pop('scope')
            dct['script'] = scope.get('script')
            dct['args'] = scope.get('args')

        return super()._from_dict(dct, **kwargs)

    def _to_dict(self) -> dict:
        result = super()._to_dict()
        scope_section = {
            'scope': {
                'script': self.script,
                'args': self._args
            }}
        result.update(_remove_empty_values(scope_section))
        return result


class DataTransferComponentDefinition(ComponentDefinition):
    """The component definition of a DataTransfer component."""

    SCHEMA = 'https://componentsdk.azureedge.net/jsonschema/DataTransferComponent.json'
    TYPE = ComponentType.DataTransferComponent


class SweepComponentDefinition(ComponentDefinition):
    """The component definition of a Sweep component."""

    SCHEMA = 'https://componentsdk.azureedge.net/jsonschema/SweepComponent.json'
    TYPE = ComponentType.SweepComponent

    TRIAL_KEY = 'trial'
    TRIAL_COMPONENT_SPEC_FILE = 'trial_component.spec.yaml'

    @staticmethod
    def _is_conditional_hyperparameter(expr):
        """Reference from azure.ml.component._graph._is_sweep_conditional_hyperparameter."""
        for model in expr:
            if not isinstance(model, dict):
                return False
            for k in model:
                if isinstance(model[k], list):
                    return True
        return False

    @staticmethod
    def _parse_choice_type_expression(options):
        """Parse choice type hyperparameter expression."""
        if SweepComponentDefinition._is_conditional_hyperparameter(options):
            spec_dict = {'type': 'choice', 'values': options}
            for model in spec_dict['values']:
                for k in model:
                    if isinstance(model[k], list):
                        model[k] = SweepComponentDefinition.parse_hyperparameter_expression(model[k])
        else:
            options = [option.value if isinstance(option, Enum) else option for option in options]  # option is enum
            options = [str(option) if isinstance(option, bool) else option for option in options]  # option is string
            spec_dict = {'type': 'choice', 'values': options}
        return spec_dict

    @staticmethod
    def parse_hyperparameter_expression(param_expr):
        """Parse hyperparameter expression to specification dictionary

        :param param_expr: hyperparameter expression, generated by azureml.train.hyperdrive.parameter_expressions
        :type param_expr: list, first is type and second is expression
        :return: hyperparameter_spec_dict
        :rtype: dict, in hyperparameter specification
        """
        typ, expr = param_expr
        hyperparameter_spec_dict = {'type': typ}
        if typ == 'choice':
            hyperparameter_spec_dict.update(SweepComponentDefinition._parse_choice_type_expression(expr[0]))
        elif typ == 'lognormal' or typ == 'normal':
            mu, sigma = expr
            hyperparameter_spec_dict.update({'mu': mu, 'sigma': sigma})
        elif typ == 'loguniform' or typ == 'uniform':
            min_value, max_value = expr
            hyperparameter_spec_dict.update({'min_value': min_value, 'max_value': max_value})
        elif typ == 'qlognormal' or typ == 'qnormal':
            mu, sigma, q = expr
            hyperparameter_spec_dict.update({'mu': mu, 'sigma': sigma, 'q': q})
        elif typ == 'qloguniform' or typ == 'quniform':
            min_value, max_value, q = expr
            hyperparameter_spec_dict.update({'min_value': min_value, 'max_value': max_value, 'q': q})
        elif typ == 'randint':
            hyperparameter_spec_dict.update({'upper': expr[0]})
        else:
            raise UserErrorException(f"Invalid hyperparameter type '{typ}', generate using 'parameter_expression'.")
        return hyperparameter_spec_dict

    def __init__(self, name, version=None, display_name=None, description=None, tags=None, is_deterministic=None,
                 inputs=None, parameters=None, outputs=None, runsettings: RunSettingsDefinition = None,
                 workspace=None, creation_context=None, registration_context=None, namespace=None,
                 snapshot_id=None, feed_name=None, registry_name=None,
                 trial_definition=None, trial_spec_file=None, _is_dsl_component=None,
                 algorithm=None, search_space=None, objective=None, limits=None, early_termination=None):
        super().__init__(name, version, display_name, description, tags, is_deterministic,
                         inputs, parameters, outputs, runsettings, workspace,
                         creation_context, registration_context,
                         namespace, snapshot_id, feed_name, registry_name)
        self._trial_definition = trial_definition
        self._trial_spec_file = trial_spec_file
        self._is_dsl_component = _is_dsl_component
        self._algorithm = algorithm
        self._search_space = search_space
        self._objective = objective
        self._limits = limits
        self._early_termination = early_termination

    @property
    def search_space(self):
        search_space_dict = {}
        for hyperparameter, expression in self._search_space.items():
            # If expression is a list, it should be generated by azureml.train.hyperdrive.parameter_expressions,
            #   else it will be a dict as hyperparameter specification, just use it.
            if isinstance(expression, list):
                search_space_dict[hyperparameter] = self.parse_hyperparameter_expression(expression)
            else:
                search_space_dict[hyperparameter] = expression
        return search_space_dict

    @property
    def objective(self):
        objective_dict = {
            'primary_metric': {
                'default': self._objective['primary_metric'],
                'enum': [self._objective['primary_metric']]
            },
            'goal': self._objective['goal']
        }
        return objective_dict

    @property
    def early_termination(self):
        """Convert early termination policy object to python dict, and extract properties from nested dict."""
        if self._early_termination is None:
            return {}
        if isinstance(self._early_termination, dict):
            return self._early_termination
        early_termination_dict = self._early_termination.to_json()
        early_termination_dict['policy_type'] = early_termination_dict.pop('name').lower()
        if 'properties' in early_termination_dict:
            early_termination_dict.update(early_termination_dict.pop('properties'))
        return early_termination_dict

    @property
    def _is_from_dsl_sweep_component(self):
        """Judge current sweep component definition is from 'dsl.sweep_component' or ModuleDto."""
        return self._trial_definition is not None

    def _to_dict(self):
        """Convert sweep component definition to a python dict."""
        result = super()._to_dict()
        if not self._is_from_dsl_sweep_component:
            return result
        # Definition comes from 'dsl.sweep_component', adjust base specification to sweep component,
        #   remove `inputs` and `outputs`,
        #   add `trial`, `algorithm`, `search_space`, `objective`, `early_termination` and `limits`.
        for key_to_pop in ['inputs', 'outputs']:
            result.pop(key_to_pop)
        result.update({
            'trial': f'file:{self.TRIAL_COMPONENT_SPEC_FILE}',
            'algorithm': self._algorithm,
            'search_space': self.search_space,
            'objective': self.objective,
            'early_termination': self.early_termination,
            'limits': self._limits
        })
        if not result['early_termination']:
            result.pop('early_termination')
        return result

    @classmethod
    def _get_trial_component(cls, trial_pattern, base_dir):
        """Get type of trail component defined in local yaml."""
        if not trial_pattern.startswith(LOCAL_PREFIX):
            raise UserErrorException(f'Can not determine component type for non-local trial {trial_pattern}.')
        file_path = trial_pattern[len(LOCAL_PREFIX):]
        return ComponentDefinition.load(Path(base_dir).absolute() / file_path)

    @classmethod
    def _from_dict(cls, dct, ignore_unexpected_keywords=True, base_dir=None, **kwargs) -> 'SweepComponentDefinition':
        if base_dir:
            # When component load from yaml, generate component dict by sweep and trail component file.
            trial_yaml_file = dct.get(cls.TRIAL_KEY, None)
            if not trial_yaml_file:
                raise UserErrorException(f"Trail doesn't specify in sweep component yaml.")
            if not trial_yaml_file.startswith(LOCAL_PREFIX):
                raise UserErrorException(f'Can not determine component type for non-local trail {trial_yaml_file}.')
            trail_yaml_file = trial_yaml_file[len(LOCAL_PREFIX):]
            # Load trail component spec file.
            try:
                with open(os.path.join(base_dir, trail_yaml_file)) as fin:
                    trail_component_data = YAML.safe_load(fin)
            except BaseException as e:
                raise YamlLoadingError(trial_yaml_file, inner_exception=e)

            # Add trial component definition to sweep component definition
            dct['trial_definition'] = copy.deepcopy(trail_component_data)
            # Merge inputs and outputs of sweep component and trail component
            dct['inputs'] = {**(dct.get('inputs') or {}), **(trail_component_data.get('inputs') or {})}
            dct['outputs'] = {**(dct.get('outputs') or {}), **(trail_component_data.get('outputs') or {})}

        return super()._from_dict(
            dct, ignore_unexpected_keywords=ignore_unexpected_keywords, base_dir=base_dir, **kwargs)

    def _save_to_code_folder(self, folder, spec_file=None):
        """Save trial and sweep component specs to specific folder."""
        # if '_trial_snapshot_folder' is not None, copy the snapshot folder to current temp spec folder
        #   and rename original trial component spec for sweep.
        if self._is_dsl_component is False:
            shutil.rmtree(folder)
            shutil.copytree(self._trial_spec_file.parent.absolute(), folder)
            trial_component_spec_file = os.path.join(folder, self.TRIAL_COMPONENT_SPEC_FILE)
            if os.path.exists(trial_component_spec_file):
                os.remove(trial_component_spec_file)
            os.rename(os.path.join(folder, self._trial_spec_file), trial_component_spec_file)
        else:
            # save trial component spec from definition, using default filename
            self._trial_definition._save_to_code_folder(folder, self.TRIAL_COMPONENT_SPEC_FILE)
        # save sweep component spec from dict
        if spec_file is None:
            spec_file = self.DEFAULT_SPEC_FILE
        spec_file = (Path(folder) / spec_file).resolve()
        spec_dict = _to_ordered_dict(self._to_dict())
        YAML._dump_yaml_file(spec_dict, spec_file, unsafe=True, header=YAML.YAML_HELP_COMMENTS)


class PipelineComponentDefinition(ComponentDefinition):
    r"""represents a Component asset version.

    ComponentDefinition is immutable class.
    """
    SCHEMA = 'https://componentsdk.azureedge.net/jsonschema/PipelineComponent.json'
    TYPE = ComponentType.PipelineComponent

    def __init__(self, name, id=None, components: dict = None, components_variable_names=None, description=None,
                 version=None, display_name=None, inputs=None, outputs=None, parameters=None, workspace=None,
                 parent_definition_id=None, from_module_name=None, pipeline_function_name=None,
                 outputs_mapping=None, default_compute_target=None, default_datastore=None,
                 tags=None, components_args_matched_dict_list=None, snapshot_id=None, creation_context=None,
                 registration_context=None, pipeline_parameters=None, non_pipeline_parameters=None,
                 feed_name=None, _module_dto=None, registry_name=None, is_deterministic=None):
        """
        :param name: Definition name.
        :type name: str
        :param id: Definition id.
        :type id: str
        :param components: Id to components dict inside pipeline definition.
        :type components: OrderedDict[str, Component]
        :param components_variable_names: The variable names of pipeline's components.
        :type components_variable_names: list[str]
        :param description: Description of definition.
        :type description: str
        :param version: The version of pipeline component.
        :type version: str
        :param display_name: The display name of pipeline component.
        :type display_name: str
        :param inputs: A dict of inputs name to definition.
        :type inputs: dict[str, InputDefinition]
        :param outputs: A dict of outputs name to definition.
        :type outputs: dict[str, OutputDefinition]
        :param parameters: Parameters of function defined by dsl.pipeline.
        :type parameters: dict
        :param workspace: workspace of definition.
        :type workspace: Workspace
        :param parent_definition_id: parent definition id.
        :type parent_definition_id: str
        :param from_module_name: from module name.
        :type from_module_name: str
        :param pipeline_function_name: The pipeline funtion name.
        :type pipeline_function_name: str
        :param outputs_mapping: A dict of outputs name to OutputBuilder on Component.
            Different from outputs, the outputs mapping is the real outputs of a pipeline,
             the _owner of dict value(OutputBuilder) is the component of definition.
            This mapping is used to record dsl.pipeline function's output
             and create a pipeline component instance from definition.
        :type outputs_mapping: dict[str, _OutputBuilder]
        :param default_compute_target: The resolved default compute target.
        :type default_compute_target: tuple(str, str)
        :param default_datastore: The default datastore.
        :type default_datastore: str
        :param tags: The tags of pipeline component.
        :type tags: dict[str, str]
        :param components_args_matched_dict_list: A list of dictionaries used to convert pipeline parameter kwargs to
            nodes with replaced keys. Dict key is the nodes parameter keys, value is parent pipeline
            parameter name(direct assign) or _ParameterAssignment(partial assign).
            e.g.
            @dsl.pipeline()
            def parent(str1, str2):
                component1(string_param=str1)
                component2(str=str2)
            Then the dict_list on pipeline 'parent' is [{'string_param', 'str1'}, {'str':'str2'}]
        :type components_args_matched_dict_list: list(dict[(str, Any)])
        :param snapshot_id: The component snapshot id.
        :type snapshot_id: str
        :param creation_context: The component creation context.
        :type creation_context: CreationContext
        :param registration_context: The component registration context.
        :type registration_context: RegistrationContext
        :param pipeline_parameters: Dictionary of pipeline parameters names and objects.
        :type pipeline_parameters: dict[str, Union[PipelineParameters, Input]]
        :param non_pipeline_parameters: Dictionary of non pipeline parameters names and objects.
        :type non_pipeline_parameters: dict[str, Union[PipelineParameters, Input]]
        :param feed_name: The feed name
        :type feed_name: str
        :param registry_name: The registry name of the component
        :type registry_name: str
        :param _module_dto: The module dto if calling from _dto_2_definition.
        :type _module_dto: ModuleDto
        :param registry_name: The registry name.
        :type registry_name: str
        :param is_deterministic: Specify whether the pipeline component can be reused or not. None value
            will be set as True before register. If False, the pipeline component will never be reused.
        :type is_deterministic: bool
        """
        super().__init__(
            name=name, display_name=display_name, description=description, is_deterministic=None, version=version,
            inputs=inputs, outputs=outputs, parameters=parameters, workspace=workspace,
            tags=tags, snapshot_id=snapshot_id, creation_context=creation_context,
            registration_context=registration_context, feed_name=feed_name, registry_name=registry_name)
        self._components = components if components else {}
        self._components_variable_names = components_variable_names if components_variable_names else []
        if len(self._components) != len(self._components_variable_names):
            raise RuntimeError(
                "While building pipeline definition, collected component node count is different "
                "from component variable names. Components: {}, variable names: {}".format(
                    self._components, self._components_variable_names))
        # components_variable_names preserves same order as components
        self._node_id_variable_name_dict = {
            node._id: self._components_variable_names[idx]
            for idx, node in enumerate(self._components.values()) if self._components_variable_names[idx] is not None}
        self._id = id
        self._outputs_mapping = outputs_mapping
        self._default_compute_target = default_compute_target
        self._default_datastore = default_datastore
        self._components_args_matched_dict_list = components_args_matched_dict_list
        self._parent_definition_id = parent_definition_id
        self._is_deterministic = is_deterministic
        # There are tests of the two field so we shall keep them in definition
        self._from_module_name = from_module_name
        self._pipeline_function_name = pipeline_function_name
        # record group flattened parameter definition and pipeline parameter object
        self._flattened_parameters = None
        self._pipeline_parameters = pipeline_parameters if pipeline_parameters else {}
        self._non_pipeline_parameters = non_pipeline_parameters if non_pipeline_parameters else {}
        # add annotations to pipeline parameters
        all_annotations = {**self.inputs, **self.parameters}
        for k, v in self._pipeline_parameters.items():
            # only set user defined annotations
            if k in all_annotations.keys() and type(all_annotations[k]) != _Param:
                if isinstance(all_annotations[k], _Group):
                    # set annotation for group parameter
                    if isinstance(v, _GroupAttrDict):
                        v._set_annotation(all_annotations[k])
                else:
                    v._annotation = all_annotations[k]
        self.validation_info = self.generate_interface()
        # set module dto for validation
        self._module_dto = _module_dto if _module_dto else _definition_to_dto(self)
        # Record the task of registering pipeline component. The key is workspace id and value is future.
        self._register_task = {}

        # Pipeline graph of registered pipeline component.
        self._pipeline_graph = None
        # Input dataset in the registered pipeline graph.
        self._pipeline_input_datasets = None
        # Nodes of registered pipeline component.
        self._register_nodes = OrderedDict({})
        # Generate runsettings
        self._generate_runsettings_definition()

    @property
    def components(self):
        """
        Get the components of a pipeline component definition.

        The components are shared by all the pipeline component created by same definition.

        :return: Id to component dict inside pipeline component definition.
        :rtype: dict[str, azure.ml.Component]
        """
        return self._components

    def get_variable_name_for_component(self, component) -> str:
        """Return variable name for component."""
        return _sanitize_python_variable_name(self._node_id_variable_name_dict[component._id])

    @property
    def flattened_parameters(self):
        """Return flattened pipeline parameters used when build."""
        if self._flattened_parameters is not None:
            return self._flattened_parameters
        # Flatten group parameters in pipeline definition.
        self._flattened_parameters = {}
        for k, v in self.parameters.items():
            if isinstance(v, _Group):
                self._flattened_parameters.update(v.flatten(group_parameter_name=k))
            else:
                self._flattened_parameters[k] = v
        return self._flattened_parameters

    def _flatten_pipeline_parameters_for_node(self, pipeline_parameters, component_idx=None):
        """
        Get group flattened pipeline parameter for node.

        Note that parameter name may changed when pass them through pipelines.
        :param pipeline_parameters: the original pipeline parameters
        :type pipeline_parameters: dict
        :param component_idx: component index to update pipeline parameter names, leave as they are if None
        :type component_idx: int
        :return: flattened pipeline parameters
        :rtype: dict
        """
        pipeline_parameters = {**pipeline_parameters}
        # Flatten group parameters in pipeline definition.
        if component_idx is not None:
            # Update the group parameter name if flatten parameter for node
            for k, v in self._components_args_matched_dict_list[component_idx].items():
                if isinstance(v, str) and v in pipeline_parameters and k != v:
                    pipeline_parameters[k] = pipeline_parameters[v]
                    del pipeline_parameters[v]
        return _flatten_pipeline_parameters(pipeline_parameters)

    def get_registered_pipeline_graph(self):
        """Get pipeline component graph by graph id.

        :return: Pipeline graph info.
        :rtype: ~designer.models.PipelineGraph
        """
        if self.identifier:
            # For registered pipeline component, getting pipeline graph by graph id.
            if not self._pipeline_graph:
                graph_id = self._module_dto.module_entity.cloud_settings.sub_graph_config.graph_id
                self._pipeline_graph = self.api_caller.imp.service_caller._get_pipeline_component_graph(
                    graph_id=graph_id)
                self._node_id_variable_name_dict = {node.id: node.name for node in self._pipeline_graph.module_nodes +
                                                    self._pipeline_graph.sub_graph_nodes}
            return self._pipeline_graph
        else:
            return None

    def get_dataset_in_registered_pipeline(self):
        """Generate the dataset in the pipeline component by the dataset definition.

        :return: The dic of input dataset in the pipeline component. The key is dataset node id,
                 value is dataset or data reference.
        :rtype: Dict[str, Dataset or DataReference]
        """
        if not self._pipeline_input_datasets:
            if self.identifier:
                pipeline_graph = self.get_registered_pipeline_graph()
                pipeline_dataset = {}
                for dataset_node in pipeline_graph.dataset_nodes:
                    dataset_definition_value = dataset_node.data_set_definition.value
                    if dataset_definition_value.data_set_reference:
                        from azureml.data.file_dataset import FileDataset
                        pipeline_dataset[dataset_node.id] = FileDataset.get_by_id(
                            workspace=self._workspace, id=dataset_definition_value.data_set_reference.id)
                    elif dataset_definition_value.literal_value:
                        datastore = Datastore.get(
                            self._workspace, dataset_definition_value.literal_value.data_store_name)
                        pipeline_dataset[dataset_node.id] = DataReference(
                            datastore=datastore,
                            path_on_datastore=dataset_definition_value.literal_value.relative_path)
                self._pipeline_input_datasets = pipeline_dataset
        return self._pipeline_input_datasets

    def create_pure_component_for_registration(self):
        """
        Create pure component from definition with empty input.

        :return: The pure component.
        :rtype: Component
        """
        default_args = {k: v._default for k, v in self._parameters.items()}
        default_args.update({k: None for k in self.inputs})

        from azure.ml.component import Pipeline
        return Pipeline(
            nodes=list(self.components.values()), outputs=self._outputs_mapping,
            workspace=self.workspace, name=self.name, description=self.description,
            default_compute_target=self._default_compute_target,
            default_datastore=self._default_datastore,
            _use_dsl=True, _definition=self, _init_params=default_args)

    def generate_register_pipeline(self):
        def set_param_value(component_node, module_parameters):
            """Set param to component node."""
            params = {}
            for param_name in component_node._definition.parameters:
                parameter_assignment = next(filter(lambda item: item.name == param_name, module_parameters), None)
                if parameter_assignment and parameter_assignment.value and \
                        parameter_assignment.value_type == str(_ParameterAssignment.LITERAL):
                    params[param_name] = parameter_assignment.value
            component_node.set_inputs(**params)

        def update_components_input_by_graph(
                pipeline_node_dict, graph_info, dataset_in_pipeline_component, node_idx_dict):
            """Update the component input by pipeline component graph.

            :param pipeline_node_dict: Dict of node id and component.
            :type pipeline_node_dict: dict[str, azure.ml.component.Component]
            :param graph_info: Pipeline graph info.
            :type graph_info: ~designer.models.PipelineGraph
            :param dataset_in_pipeline_component: Dataset in the registered pipeline component. The key is dataset
                                                  node id, value is dataset or data reference.
            :type dataset_in_pipeline_component: dict[str, Dataset or DataReference]
            """
            for edge in graph_info.edges:
                if edge.source_output_port.node_id in dataset_in_pipeline_component:
                    # When dataset in the pipeline component
                    input_dataset = dataset_in_pipeline_component[edge.source_output_port.node_id]
                    pipeline_node_dict[edge.destination_input_port.node_id].set_inputs(**{
                        edge.destination_input_port.port_name: input_dataset})
                elif edge.source_output_port.node_id is None:
                    # Input dataset is pipeline parameter.
                    pipeline_parameter = PipelineParameter(name=edge.source_output_port.graph_port_name,
                                                           default_value=None)
                    input_name = edge.destination_input_port.port_name.lower()
                    pipeline_node_dict[edge.destination_input_port.node_id].set_inputs(
                        **{input_name: pipeline_parameter})
                    node_idx = node_idx_dict[edge.destination_input_port.node_id]
                    self._components_args_matched_dict_list[node_idx].update({input_name: pipeline_parameter.name})
                elif edge.destination_input_port.node_id and edge.source_output_port.node_id:
                    # Connect components by input/output ports.
                    pipeline_node_dict[edge.destination_input_port.node_id].set_inputs(**{
                        edge.destination_input_port.port_name:
                            pipeline_node_dict[edge.source_output_port.node_id].outputs[
                                edge.source_output_port.port_name]})

        if self.identifier:
            pipeline_graph = self.get_registered_pipeline_graph()

            if not self._register_nodes:
                from azure.ml.component import Component

                # Initial nodes in pipeline
                self._components_args_matched_dict_list = []
                node_idx_dict = {}
                for idx, node in enumerate(pipeline_graph.module_nodes + pipeline_graph.sub_graph_nodes):
                    # Generate component in pipeline component.
                    component_node = Component.load(workspace=self._workspace, id=node.module_id)()
                    node_idx_dict[node.id] = idx
                    set_param_value(component_node, node.module_parameters)
                    # Update the component instance id to node id of the graph.
                    component_node._instance_id = node.id
                    self._register_nodes[node.id] = component_node
                    self._node_id_variable_name_dict[node.id] = node.name
                    # Update parameter link to matched dict
                    from azure.ml.component._graph import _GraphEntityBuilder
                    # Note: here contains only parameter, inputs will be updated later.
                    self._components_args_matched_dict_list.append(
                        {parameter.name: parameter.value for parameter in node.module_parameters
                         if parameter.value_type == _GraphEntityBuilder.GRAPH_PARAMETER_NAME})

                dataset_in_pipeline_component = self.get_dataset_in_registered_pipeline()
                update_components_input_by_graph(
                    self._register_nodes, pipeline_graph, dataset_in_pipeline_component, node_idx_dict)

    def generate_interface(self):
        """Validate & generated the interface according to the inferred data, return list of validation errors.

        Validate inputs/parameters/run settings of all components inside pipeline.
        For pipeline parameter, who's value has not determined yet, we validate it's type.

        :return: List of validation errors
        :rtype: List[Diagnostic]
        """
        from azure.ml.component._visualization_context import _build_step_node_from_pipeline_definition
        from azure.ml.component._component_validator import PipelineDefinitionValidator
        from azure.ml.component._component_validator import Diagnostic, VariableType
        from azure.ml.component._pipeline_validator import PipelineValidator

        errors = []

        def collect_error(validation_error, variable_name=None, variable_type=None, component=None):
            error = Diagnostic.create_diagnostic_by_component_definition(
                definition=self,
                error_msg=validation_error.message,
                error_type=validation_error.error_type,
                error_var_name=variable_name,
                error_var_type=variable_type,
                component=component
            )
            errors.append(error)

        def process_definition_error(
                e: Exception, error_type, variable_name, variable_type, component=None, pipeline_param=None):
            validation_error = ComponentValidationError(str(e), e, error_type)
            # record error on pipeline parameter to skip infer
            if pipeline_param is not None and isinstance(pipeline_param, LinkedParametersMixedIn):
                pipeline_param.errors.append(validation_error)
            # collect validation error
            collect_error(validation_error, variable_name, variable_type, component)

        # 1. validate components meta
        for idx, component in enumerate(self.components.values()):
            # skip validation for component which don't have dto
            if component._module_dto is None:
                continue
            pipeline_parameters = self._flatten_pipeline_parameters_for_node(self._pipeline_parameters, idx)
            definition_validator = PipelineDefinitionValidator(
                component_node_name=self.get_variable_name_for_component(component),
                pipeline_parameters=pipeline_parameters,
                process_error=partial(process_definition_error, component=component)
            )
            validation_info = component._validate_component(
                raise_error=False,
                pipeline_parameters=pipeline_parameters,
                is_local=False,
                # won't validate datastore here, because it can be updated after the pipeline definition built
                for_definition_validate=True,
                definition_validator=definition_validator
            )
            component.validation_info = validation_info
            errors.extend(validation_info)

        # 2. validate annotation & infer unknown fields
        for param_name, param in _flatten_pipeline_parameters(self._pipeline_parameters).items():
            # 2.1 If a param linked to no parameter, warning and continue
            if len(param.linked_params) + len(param.linked_param_assignments) == 0 and not param.used_in_definition \
                    and param_name not in self._non_pipeline_parameters:
                logger.warning(
                    f'Parameter {param_name!r} was not effectively used in pipeline {self.name!r}.')
                param.is_used_param = False
                continue

            # 2.2 Infer meta for pipeline parameter according to linked parameters, type None for unknown
            inferred_meta_dict = {"optional": True, "type": None}

            # Infer optional, if optional param linked to required params, record error
            required_params = {}
            for linked_param_name, linked_param in param.linked_params.items():
                if not getattr(linked_param, 'is_optional', None):
                    inferred_meta_dict["optional"] = False
                    required_params[linked_param_name] = linked_param
            if param._annotation and param._annotation.optional and not inferred_meta_dict["optional"]:
                process_definition_error(
                    e=ValueError(
                        "Pipeline parameter '{}' set optional in definition but linked to "
                        "required parameters: {}.".format(
                            param_name, LinkedParametersMixedIn.repr_linked_params(required_params))
                    ),
                    error_type=ComponentValidationError.REQUIRED_PARAMETER_OPTIONAL,
                    variable_name=param_name,
                    variable_type=VariableType.Parameter
                )

            # Infer description
            if len(param.linked_params) == 1:
                linked_param = next(iter(param.linked_params.values()))
                if getattr(linked_param, "description", None):
                    inferred_meta_dict["description"] = linked_param.description

            if param._annotation and len(param.errors) > 0:
                # Skip infer if there's validation error on param
                continue
            # Infer type/range/enum
            self._infer_meta_based_on_linked_params(
                param, param_name, inferred_meta_dict, process_definition_error)

        # update inputs according to annotated/inferred type
        for param_name, param in self.parameters.items():
            if isinstance(param, Input):
                self.inputs[param_name] = param

        self._parameters = {k: v for k, v in self.parameters.items() if not isinstance(v, Input)}

        # 3. validate graph structure
        PipelineValidator.validate_empty_pipeline(self.components, collect_error)
        PipelineValidator.validate_module_cycle(_build_step_node_from_pipeline_definition(self), collect_error)
        return errors

    def _delete_unused_pipeline_parameter(self, pipeline_parameters):
        """
        Optimized out unused pipeline parameter

        :param pipeline_parameters: the original pipeline parameters
        :type pipeline_parameters: dict
        """
        pipeline_parameters = {**pipeline_parameters}
        for k, v in pipeline_parameters.items():
            if not isinstance(v, _GroupAttrDict) and not v.is_used_param:
                self._pipeline_parameters.pop(k)
                self._parameters.pop(k)

    def _infer_meta_based_on_linked_params(
            self,
            param: PipelineParameter,
            param_name: str,
            inferred_meta_dict: dict,
            process_definition_error: Callable
    ):
        """Infer pipeline parameter meta based on it's linked parameters.

        :param param: pipeline parameter to infer meta
        :param param_name: pipeline parameter name
        :param inferred_meta_dict: inferred meta dictionary
        :param process_definition_error: function to process definition error
        """
        from azure.ml.component._component_validator import VariableType

        def set_attr_if_unique(meta_dict: dict, attr: str, value):
            """Set value to attr in meta_dict, if different value for attr already exists, raise error."""
            original_value = meta_dict.get(attr, None)
            if original_value is not None and original_value != value:
                meta_name = "range" if attr == "min" or attr == "max" else attr
                # record meta mismatch
                raise ValueError(
                    "Pipeline parameter '{}' assigned to multiple parameters with mismatched {}: {}".format(
                        param_name, meta_name, LinkedParametersMixedIn.repr_linked_params(param.linked_params)
                    )
                )
            else:
                # set value
                meta_dict[attr] = value

        input_types_list = set()
        unknown_linked_param = False
        try:
            for key, linked_param in param.linked_params.items():
                linked_param_owner_type = param.linked_param_owner_type[key]
                if isinstance(linked_param, StructuredInterfaceInput):
                    if linked_param.data_type_ids_list:
                        port_type = linked_param.data_type_ids_list[0] \
                            if len(linked_param.data_type_ids_list) == 1 else 'input'
                        # Fall back other type to Input
                        port_type = port_type if port_type in _Param._PARAM_TYPE_STRING_MAPPING else 'input'
                        # set type if primitive type, else 'input'
                        set_attr_if_unique(inferred_meta_dict, "type", port_type)
                        set_attr_if_unique(inferred_meta_dict, "is_input_port", True)
                        # record all linked input types
                        input_types_list = input_types_list.union(linked_param.data_type_ids_list)
                    else:
                        # if linked unknown parameter, record and skip adding it
                        unknown_linked_param = True
                elif isinstance(linked_param, (StructuredInterfaceParameter, RunSettingParamDefinition)):
                    if linked_param.parameter_type:
                        if isinstance(linked_param, StructuredInterfaceParameter):
                            parameter_type = _DefinitionInterface._structured_interface_parameter_type(linked_param)
                            # treat string and enum equally, to allow a parameter linked to string and enum
                            if parameter_type == "enum":
                                parameter_type = "string"
                        else:
                            parameter_type = _Param.parse_param_type(linked_param.type_in_py)
                        set_attr_if_unique(inferred_meta_dict, "type", parameter_type)
                        if linked_param_owner_type == ComponentType.PipelineComponent.value:
                            # if link to sub pipeline parameter, current param must be a parameter.
                            # if link to component parameter, current param could be both parameter or port.
                            set_attr_if_unique(inferred_meta_dict, "is_input_port", False)
                    else:
                        # if linked unknown parameter, record and skip adding it
                        unknown_linked_param = True
                    if inferred_meta_dict["type"] == "integer":
                        _type = int
                    else:
                        _type = float
                    lower_bound = _type(linked_param.lower_bound) if linked_param.lower_bound is not None else None
                    upper_bound = _type(linked_param.upper_bound) if linked_param.upper_bound is not None else None

                    # if param has one of min/max, skip inferring it
                    if not isinstance(param._annotation, _Param)\
                            or param._annotation.min is None and param._annotation.max is None:
                        set_attr_if_unique(inferred_meta_dict, "min", lower_bound)
                        set_attr_if_unique(inferred_meta_dict, "max", upper_bound)
                    if not isinstance(param._annotation, _Param) or not param._annotation.enum:
                        # allow case when a pipeline parameter linked to string and enum
                        if linked_param.enum_values:
                            set_attr_if_unique(inferred_meta_dict, "enum", linked_param.enum_values)
            # for parameter assignment, we infer its type as str since it's used converted aether and it does not
            # have annotations
            if not param._annotation or not param._annotation.type:
                if param.linked_param_assignments and inferred_meta_dict["type"] is None:
                    inferred_meta_dict["type"] = "str"
                    logger.warning(
                        "Can not determine the type of parameter {!r} of pipeline {!r}, setting it as string.".format(
                            param_name, self.name)
                    )
        except ValueError as e:
            process_definition_error(
                e=e,
                error_type=ComponentValidationError.MULTIPLE_TYPES_ASSIGNMENT,
                variable_name=param_name,
                variable_type=VariableType.Parameter
            )
        else:
            # if linked unknown param, won't set annotation
            if not unknown_linked_param:
                if param._annotation:
                    # update annotation
                    if "min" in inferred_meta_dict:
                        param._annotation._min = inferred_meta_dict["min"]
                    if "max" in inferred_meta_dict:
                        param._annotation._max = inferred_meta_dict["max"]
                    if "enum" in inferred_meta_dict:
                        param._annotation._enum = inferred_meta_dict["enum"]
                    if "description" in inferred_meta_dict:
                        param._annotation._description = inferred_meta_dict["description"]
                else:
                    # set annotation
                    is_input_port = inferred_meta_dict.pop('is_input_port') \
                        if 'is_input_port' in inferred_meta_dict else False
                    if is_input_port:
                        # if inferred meta is path, change it's type to Input
                        # sort for better test
                        input_types_list = sorted(list(input_types_list))
                        if len(input_types_list) == 0:
                            # Should not go here: when inferred as input, input types should at least have 1 item
                            raise ValueError(
                                "Inferred param {} as input but input types is empty, meta: {}".format(
                                    param, inferred_meta_dict
                                )
                            )
                        elif len(input_types_list) == 1:
                            input_types_list = input_types_list[0]
                        inferred_meta_dict["type"] = input_types_list
                        valid_keys = ["type", "description", "optional"]
                        annotation = Input(**{k: v for k, v in inferred_meta_dict.items() if k in valid_keys})
                    else:
                        inferred_type = inferred_meta_dict.pop("type")
                        annotation = _Param(**inferred_meta_dict)
                        # set type(None for unknown) for inferred meta
                        annotation._type = inferred_type
                    annotation._name = param_name
                    param._annotation = annotation
                    if param_name in self.parameters.keys():
                        self.parameters[param_name] = annotation

    def _convert_component_kwargs(self, pipeline_parameters, component_idx):
        """
        Convert pipeline parameters to the matched input of components.

        :param pipeline_parameters: the original pipeline parameters
        :type pipeline_parameters: dict
        :param component_idx: the component index in pipeline nodes.
        :type component_idx: int
        """
        component_args_matched_dict = self._components_args_matched_dict_list[component_idx]
        updated_kwargs = {}

        def _update_nested_parameter_value(obj):
            if isinstance(obj, PipelineParameter):
                updated_value = _get_param_in_group_from_pipeline_parameters(
                    obj.name, pipeline_parameters, obj._groups, pipeline_name=self.name)
                if updated_value is not inspect.Parameter.empty:
                    obj = updated_value
            elif isinstance(obj, _GroupAttrDict):
                obj = _GroupAttrDict({_k: _update_nested_parameter_value(_v) for _k, _v in obj.items()})
            return obj

        from azure.ml.component._core._types import _GroupAttrDict
        for k, v in component_args_matched_dict.items():
            if isinstance(v, str) and v in pipeline_parameters:
                updated_kwargs[k] = pipeline_parameters[v]
            elif isinstance(v, PipelineParameter):
                # Pipeline parameter direct assign to node or parameter from group
                value = _get_param_in_group_from_pipeline_parameters(
                    v.name, pipeline_parameters, v._groups, pipeline_name=self.name)
                if value is inspect.Parameter.empty:
                    continue
                updated_kwargs[k] = value
            elif isinstance(v, _ParameterAssignment):
                # Pipeline parameter partial assign as _ParameterAssignment to node
                # Update values dict by pipeline parameter
                updated_kwargs[k] = _ParameterAssignment.resolve(
                    v.formatter, {**v.assignments_values_dict, **pipeline_parameters}, print_warning=False)
            elif isinstance(v, _GroupAttrDict):
                # Update single updated parameter in group from pipeline parameter
                updated_kwargs[k] = _GroupAttrDict(_update_nested_parameter_value(v))
            elif isinstance(v, dict):
                # Copy the dict and update values dict by pipeline parameter
                value = copy.copy(v)
                updated_kwargs[k] = {
                    value_k: _update_nested_parameter_value(value_v) for value_k, value_v in value.items()}
            elif type(v) in [list, tuple]:
                # Copy the dict and update values dict by pipeline parameter
                value = copy.copy(v)
                updated_kwargs[k] = [_update_nested_parameter_value(value_v) for value_v in value]

        return updated_kwargs

    def _generate_runsettings_definition(self):
        from .._restclients.designer.models import RunSettingParameter, RunSettingParameterType, \
            RunSettingUIParameterHint, UIComputeSelection, RunSettingUIWidgetTypeEnum

        target = RunSettingParameter(
            argument_name='target',
            description='The compute target to use',
            is_optional=False,
            label='Target',
            name='Target',
            parameter_type=RunSettingParameterType.STRING,
            run_setting_ui_hint=RunSettingUIParameterHint(
                anonymous=False,
                ux_ignore=False,
                ui_widget_type=RunSettingUIWidgetTypeEnum.compute_selection,
                compute_selection=UIComputeSelection(
                    compute_run_settings_mapping={
                        'AmlCompute': [],
                        'HDInsight': [],
                        'CmAks': [],
                        'Cmk8s': [],
                        'Itp': [],
                        'Kubernetes': [],
                        'DataFactory': []
                    },
                    compute_types=["AmlCompute", "HDInsight", "CmAks", "Cmk8s", "Itp", "Kubernetes", "DataFactory"]
                )
            )
        )
        target.id = 'target'
        target.is_compute_target = True
        target.parameter_type_in_py = str
        # TODO(nana): we may change to leverage MT API to get the runsettings definition
        self._runsettings = RunSettingsDefinition.from_dto_runsettings([target])

    def _update_pipeline_component_definition(self, workspace):
        """Update the params of pipeline definition after workspace independent component registered."""
        from azure.ml.component import Pipeline

        def _update_pipeline_definition(pipeline_definition):
            """Update validation info and module dto of pipeline definition"""
            # Regenerate parameter annotation.
            # Flatten parameters in groups here to get all pipeline parameter.
            flattened_parameters = _flatten_pipeline_parameters(
                pipeline_definition._pipeline_parameters)
            for v in flattened_parameters.values():
                # Remove annotation, linked_params and linked_param_assignments of pipeline parameter.
                # They will be regenerate by generate_interface().
                v.linked_params, v.linked_param_assignments = {}, {}
                # Reset inferred annotation type
                if type(v._annotation) == _Param:
                    v._annotation = None
            pipeline_definition.validation_info = pipeline_definition.generate_interface()
            pipeline_definition._flattened_parameters = None
            pipeline_definition._module_dto = _definition_to_dto(pipeline_definition)

            # For sweep component, the output type is metrics or model, should be changed to AnyFile after registered.
            # Update sweep component output in the pipeline outputs.
            for k, v in pipeline_definition.outputs.items():
                component_output = pipeline_definition._outputs_mapping[k]
                output_owner = component_output._owner
                if output_owner.type == ComponentType.SweepComponent.value:
                    # Get the matched component output definition key.
                    # Note: here 'k' is pipeline output name, which may be different from component output name.
                    component_output_key = next((
                        k for k, v in output_owner.outputs.items() if id(v) == id(component_output)), k)
                    pipeline_definition._outputs[k] = output_owner._definition.outputs[component_output_key]

        def _update_nodes_runsettings(node_list):
            # Update runsettings of component in the pipeline definition.
            for node in node_list:
                if isinstance(node, Pipeline) and node._workspace_independent_component_exists:
                    _update_nodes_runsettings(node._definition.components.values())
                    # Update validation info and module dto of pipeline definition
                    _update_pipeline_definition(node._definition)
                elif not isinstance(node, Pipeline) and not node._runsettings._workspace:
                    node._update_component_params_and_runsettings(workspace, pipeline_name=self.name)

        _update_nodes_runsettings(self.components.values())
        # Update validation info and module dto of pipeline definition
        _update_pipeline_definition(self)

    @staticmethod
    def detect_output_annotation(func_name, annotations: dict):
        """Collect and raise exception if there are pipeline parameters with annotation 'Output'."""
        # Note: parameter in group already be asserted when define group
        invalid_annotation_names = [k for k, v in annotations.items() if isinstance(v, Output)]
        if invalid_annotation_names:
            raise UnsupportedOutputAnnotationError(func_name, invalid_annotation_names)


class ControlComponentDefinition(ComponentDefinition):
    """Control component definition.

    Note: _ControlComponent only be used in SDK side, will not be registered.
    """
    CONTROL_TYPE_KEY = 'control_type'
    TYPE = ComponentType.ControlComponent

    def __init__(
            self, name, version=None, display_name=None, inputs=None,
            parameters=None, outputs=None, control_type=None,
            control_parameter_name=None, **kwargs
    ):
        super(ControlComponentDefinition, self).__init__(
            name=name, version=version, display_name=display_name,
            inputs=inputs, parameters=parameters, outputs=outputs, **kwargs
        )
        self._control_type = control_type
        self._control_parameter_name = control_parameter_name
        self._module_dto = _definition_to_dto(self)

    def _register_workspace_independent_component(self, **kwargs):
        """Skip register for control component."""
        return

    @classmethod
    def _from_dict(cls, dct, **kwargs) -> 'ControlComponentDefinition':
        if cls.CONTROL_TYPE_KEY in dct:
            control_type = dct[cls.CONTROL_TYPE_KEY]
            dct[cls.CONTROL_TYPE_KEY] = ControlComponentType._value2member_map_.get(control_type, control_type)
        return super()._from_dict(dct=dct)
