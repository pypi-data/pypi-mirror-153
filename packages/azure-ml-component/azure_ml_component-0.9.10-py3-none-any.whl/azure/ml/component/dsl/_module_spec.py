# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Module Spec python representation."""
import re
import itertools
import copy
from collections import OrderedDict

from azure.ml.component._core._types import Input, Output, _Param
from ruamel.yaml import Dumper
import logging
from pathlib import Path
from typing import List, Union, Optional
from platform import python_version

from azureml.core.environment import DEFAULT_CPU_IMAGE

from azure.ml.component._util._utils import _relative_to
from azure.ml.component._util._yaml_utils import YAML
from azure.ml.component._version import VERSION
from azureml.core.conda_dependencies import CondaDependencies
from azureml.core.container_registry import ContainerRegistry

SPEC_EXT = '.spec.yaml'


class _YamlFlowDict(dict):
    """This class is used to dump dict data with flow_style."""

    @classmethod
    def representer(cls, dumper: Dumper, data):
        return dumper.represent_mapping('tag:yaml.org,2002:map', data, flow_style=True)


class _YamlFlowList(list):
    """This class is used to dump list data with flow_style."""

    @classmethod
    def representer(cls, dumper: Dumper, data):
        return dumper.represent_sequence('tag:yaml.org,2002:seq', data, flow_style=True)


def _str_representer(dumper: Dumper, data):
    """Dump a string with normal style or '|' style according to whether it has multiple lines."""
    style = ''
    if '\n' in data:
        style = '|'
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style=style)


def _setup_yaml(typ):
    yaml = YAML(typ)
    yaml.default_flow_style = False
    yaml.allow_unicode = True
    yaml.encoding = 'utf-8'
    yaml.representer.add_representer(_YamlFlowDict, _YamlFlowDict.representer)
    yaml.representer.add_representer(_YamlFlowList, _YamlFlowList.representer)
    yaml.representer.add_representer(str, _str_representer)
    yaml.representer.add_representer(
        type(None), lambda dumper, value: dumper.represent_scalar(u'tag:yaml.org,2002:null', ''))

    # Setup to preserve order in yaml.dump, see https://stackoverflow.com/a/8661021
    def _represent_dict_order(self, data):
        return self.represent_mapping("tag:yaml.org,2002:map", data)

    yaml.representer.add_representer(OrderedDict, _represent_dict_order)
    return yaml


def _get_value_by_key_path(dct, key_path, default_value=None):
    """Given a dict, get value from key path.

    >>> dct = {
    ...     'Beijing': {
    ...         'Haidian': {
    ...             'ZipCode': '110108',
    ...         }
    ...     }
    ... }
    >>> _get_value_by_key_path(dct, 'Beijing/Haidian/ZipCode')
    '110108'
    """
    if not key_path:
        raise ValueError("key_path must not be empty")

    segments = key_path.split('/')
    final_flag = object()
    segments.append(final_flag)

    walked = []

    cur_obj = dct
    for seg in segments:
        # If current segment is final_flag,
        # the cur_obj is the object that the given key path points to.
        # Simply return it as result.
        if seg is final_flag:
            # return default_value if cur_obj is None
            return default_value if cur_obj is None else cur_obj

        # If still in the middle of key path, when cur_obj is not a dict,
        # will fail to locate the values
        if not isinstance(cur_obj, dict):
            # TODO: maybe add options to raise exceptions here in the future
            return default_value

        # Move to next segment
        cur_obj = cur_obj.get(seg)
        walked.append(seg)

    raise RuntimeError("Invalid key path: %s" % key_path)


def _to_ordered_dict(data: dict) -> OrderedDict:
    for key, value in data.items():
        if isinstance(value, dict):
            data[key] = _to_ordered_dict(value)
    return OrderedDict(data)


class _BaseParam:
    def __init__(self, name, type, description=None, arg_name=None, arg_string=None, optional=None):
        # if name and not name.isidentifier():
        #    raise DSLComponentDefiningError("The name must be a valid variable name, got '%s'." % name)

        self._name = name
        self._type = type
        self._description = description
        self._arg_name = arg_name
        self._arg_string = arg_string
        self._optional = optional

    @property
    def name(self) -> str:
        return self._name

    def arg_group(self):
        return [self.arg_string, self._arg_dict()]

    def arg_group_str(self):
        s = '%s %s' % (self.arg_string, self._arg_placeholder())
        return '[%s]' % s if self._optional else s

    @property
    def arg_string(self):
        return self._arg_string

    @property
    def arg_name(self):
        return self._arg_name

    @arg_name.setter
    def arg_name(self, value):
        self._arg_name = value

    def _arg_placeholder(self) -> str:
        raise NotImplementedError()

    def _arg_dict(self) -> dict:
        raise NotImplementedError()


class _Port(_BaseParam):
    pass


class InputPort(Input, _Port):
    """Input port for the module."""

    def __init__(self, name, type, description=None, optional=None, arg_name=None, arg_string=None):
        """Define an input port for the module."""
        Input.__init__(self, type=type, description=description, optional=optional)
        self._name = name
        _Port.__init__(
            self, name=name, type=type, description=description,
            arg_name=arg_name, arg_string=arg_string,
            optional=optional,
        )

    def _arg_placeholder(self):
        return "{inputs.%s}" % self.name

    def _arg_dict(self) -> dict:
        return {'inputValue': self.name}


class OutputPort(Output, _Port):
    """Output port for the module."""

    def __init__(self, name, type, description=None, arg_name=None, arg_string=None):
        """Define an output port for the module."""
        Output.__init__(self, type=type, description=description)
        self._name = name
        _Port.__init__(
            self, name=name, type=type, description=description,
            arg_name=arg_name, arg_string=arg_string,
        )
        self.optional = False

    def _arg_placeholder(self):
        return "{outputs.%s}" % self.name

    def _arg_dict(self) -> dict:
        return {'outputPath': self.name}


class Param(_Param, _BaseParam):
    """Parameter for the module."""
    PARAM_TYPES = {
        'String', 'Float', 'Integer', 'Boolean', 'Enum',
        # The following types are internal usage for built-in modules.
        'Script', 'ColumnPicker', 'Credential', 'ParameterRange',
    }

    def __init__(self, name, type, description=None,
                 default=None, enum=None, optional=False,
                 min=None, max=None,
                 arg_name=None, arg_string=None,
                 ):
        """Define a parameter for the module."""
        _Param.__init__(
            self, name=name, description=description, enum=enum,
            optional=optional, min=min, max=max,
        )
        self._type = type
        # Set _default directly instead of call _update_default because we don't want to change
        # optional field value here.
        self._default = default
        _BaseParam.__init__(self, name, type, description, arg_name=arg_name, arg_string=arg_string, optional=optional)

    def _arg_placeholder(self):
        return "{inputs.%s}" % self.name

    def _arg_dict(self) -> dict:
        return {'inputValue': self.name}


class _Dependencies:
    """A class wraps AzureML Service's CondaDependencies class."""

    DEFAULT_NAME = 'project_environment'
    DEFAULT_PIP_PACKAGES = ['azureml-defaults', 'azure-ml-component']
    COMPONENT_PACKAGES_PATTERN = re.compile('^azure-ml-component(\\[.*\\])?$')

    def __init__(self, conda_content: dict = None):
        if not conda_content:
            # Create an dummy dict if not specified.
            #
            # Cannot use `{}` or `None` here, because they will be ignored by CondaDependencies,
            # and will generate a default CondaDependencies instance containing packages
            # like 'azureml-defaults', which is not expected by our use case.
            # Thus, we make an dummy dict only contains 'name' here as a workaround.
            #
            # NOTE: We must create this dummy dict EVERY TIME, and cannot define as a global variable.
            #       Otherwise the instances of Dependencies will interfere with each other.
            conda_content = {'name': self.DEFAULT_NAME}

        self._underlying = CondaDependencies(_underlying_structure=conda_content)

    @classmethod
    def create_default(cls, job_type='basic', default_pip_packages=None):
        """Create default conda environment configuration.

        Yaml description is as follows:

        name: project_environment
        channels:
        - defaults
        dependencies:
        - python=YOUR_PYTHON_VERSION
        """
        d = _Dependencies()
        d.add_conda_packages(cls._get_python_version())
        d.add_pip_options(*cls._get_default_pip_options())
        d.add_pip_packages(*cls._normalize_default_pip_packages(default_pip_packages))
        d.add_pip_options()
        if job_type is not None and job_type.lower() == 'mpi':
            d.add_pip_packages('mpi4py')
        return d

    @classmethod
    def _get_python_version(cls):
        return 'python=%s' % python_version()

    @classmethod
    def _get_default_package_version(cls):
        my_version = VERSION
        # We may get a local debug version(0.1.0.0).
        # In such scenarios, we use a version of internal build as default.
        # TODO: change to stable version.
        if my_version is None or my_version == '0.1.0.0':
            # https://msdata.visualstudio.com/DefaultCollection/Vienna/_build/results?buildId=19432676&view=results
            my_version = '0.1.0.59812083'
        return my_version

    @classmethod
    def _get_default_pip_options(cls):
        my_version = cls._get_default_package_version()
        pip_options = []
        # Internal version, add extra.
        if my_version.startswith('0.1.0.'):
            pip_options.append('--extra-index-url=https://azuremlsdktestpypi.azureedge.net/modulesdkpreview')
        return pip_options

    @classmethod
    def _normalize_default_pip_packages(cls, default_pip_packages=None):
        default_pkgs = default_pip_packages if default_pip_packages else cls.DEFAULT_PIP_PACKAGES
        my_version = cls._get_default_package_version()
        is_private_version = my_version.startswith('0.1.0.')
        pkgs = []
        for i in range(len(default_pkgs)):
            pkg = default_pkgs[i]
            items = pkg.split('==')
            name = items[0]
            # If it's private version, update update the version of azureml related packages.
            # If it's public version, only update the version of azure-ml-component.
            update_package_version = name.startswith('azureml-') or name.startswith('azure-ml-') \
                if is_private_version else re.match(cls.COMPONENT_PACKAGES_PATTERN, name)
            if update_package_version:
                pkgs.append('%s==%s' % (name, my_version))
            else:
                pkgs.append(pkg)
        return pkgs

    @property
    def channels(self):
        result = sorted(self._underlying.conda_channels)
        if not result:
            result = ['defaults']
        return result

    @property
    def conda_packages(self):
        return sorted(self._underlying.conda_packages)

    def add_conda_packages(self, *packages):
        for package in packages:
            self._underlying.add_conda_package(package)

    @property
    def pip_options(self):
        def option_weight(option):
            if option.startswith('--index-url'):
                # Use this hack to make index url at top of the list
                # otherwise conda will failed to search extract index urls
                # if --extra-index-url is before --index-url.
                return '---'
            return option.lower()

        return sorted(self._underlying.pip_options, key=option_weight)

    def add_pip_options(self, *options):
        for option in options:
            self._underlying.set_pip_option(option)

    @property
    def pip_packages(self):
        return list(self._underlying.pip_packages)

    def add_pip_packages(self, *packages):
        for package in packages:
            self._underlying.add_pip_package(package)

    @property
    def conda_dependency_dict(self):
        """Merge raw data lists into a conda environment compatible dict, which will be dumped to a YAML file.

        For conda environment file format please refer to:
        https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-file-manually

        Rules for generating conda environment YAML file:
          1. Firstly, sort each of the lists alphabetically.
          2. Merge PipOptions and PipPackages lists into one list. PipOptions comes before PipPackages.
          3. Create a dictionary object with key 'pip', value is the list created in step 2.
          4. Append this dictionary to the end of CondaPackages. (Only if the list created in step 2 is not empty.)
          5. Create a dictionary with the following keys (make sure to keep the order):
             * 'name': is hard-coded 'project_environment'
             * 'channels': the CondaChannel list. if list is empty, set to a default list as ['defaults'].
             * 'dependencies': is the CondaPackages list with pip appended to the end (if any).
          6. Dump this dict to a yaml file.

        WARNING:
             Do NOT change this implementation.

             AzureML service will create a hash for the generated YAML file,
             which will be used as the key of the docker image cache.
             If the implementation changed, and the image cache may fail to match,
             causing performance problems.

        WARNING 2:
             There is also a C# version of this logic in the JES code base.

             ref: `ConstructCondaDependency` method in the following code:
             https://msdata.visualstudio.com/AzureML/_git/StudioCore?path=%2FProduct%2FSource%2FStudioCoreService%2FCommon%2FCommonHelper.cs&version=GBmaster

             Please keep the C# code synced in case the implementation here
             must be changed in the future.

        """
        dependencies = self.conda_packages
        pip_options_and_packages = self.pip_options + self.pip_packages
        if pip_options_and_packages:
            pip_entry = {'pip': self.pip_options + self.pip_packages}
            dependencies.append(pip_entry)

        return {
            'name': self.DEFAULT_NAME,
            'channels': self.channels,
            'dependencies': dependencies,
        }


class _ModuleDefinition:
    DEFAULT_BASE_DOCKER_IMAGE = DEFAULT_CPU_IMAGE
    DEFAULT_SPEC_FILE = 'module_spec.spec.yaml'

    @property
    def name(self) -> str:
        raise NotImplementedError()

    @property
    def namespace(self) -> Optional[str]:
        return None

    @property
    def version(self) -> str:
        raise NotImplementedError()

    @property
    def description(self) -> Optional[str]:
        return None

    @property
    def is_deterministic(self) -> Optional[bool]:
        return None

    @property
    def job_type(self) -> Optional[str]:
        return None

    @property
    def tags(self) -> Optional[List[str]]:
        return None

    @property
    def contact(self) -> Optional[str]:
        return None

    @property
    def help_document(self) -> Optional[str]:
        return None

    @property
    def annotations(self):
        return None

    @property
    def os(self) -> Optional[str]:
        return None

    @property
    def image(self) -> Optional[str]:
        return None

    @property
    def container_registry(self) -> Optional[ContainerRegistry]:
        return None

    @property
    def container_registry_dict(self) -> Optional[dict]:
        return None if not self.container_registry else {
            'address': self.container_registry.address,
            'username': self.container_registry.username,
            'password': self.container_registry.password,
        }

    @property
    def aml_environment(self) -> Optional[Union[str, dict]]:
        """Environment could be a string as a reference, or a dict including image and conda.

        In default, env returns None or dict according to self.conda_dependencies.
        By inheriting the class one could set environment with a string.
        """
        return self.gen_aml_environment_from_conda(self.conda_dependencies)

    @property
    def base_image(self):
        return self.DEFAULT_BASE_DOCKER_IMAGE

    @property
    def conda_dependencies(self) -> Optional[Union[str, dict]]:
        # Could be a string to indicate the file, or a dict to indicate the conda dependencies
        return None

    @property
    def command(self) -> List[str]:
        raise NotImplementedError()

    @property
    def args(self) -> List:
        return []

    @property
    def input_ports(self) -> List[InputPort]:
        return []

    @property
    def output_ports(self) -> List[OutputPort]:
        return []

    @property
    def params(self) -> List[Param]:
        return []

    @staticmethod
    def base_params_to_list(base_params):
        return [
            param._to_dict() if isinstance(param, (Input, Output, _Param))
            else param for param in base_params
        ]

    @property
    def implementation(self):
        return {
            'os': self.os,
            'container': {
                'amlEnvironment': self.aml_environment,
                'image': self.image,
                'imageRegistry': self.container_registry_dict if self.image else None,
                'command': self.command,
                'args': self.args,
            },
        }

    def _to_dict(self):
        return self.spec_dict

    @property
    def spec_dict(self):
        annotations = self.annotations if self.annotations else {}
        if self.tags:
            annotations['tags'] = self.tags
        if self.contact:
            annotations['contact'] = self.contact
        if self.help_document:
            annotations['helpDocument'] = self.help_document
        result = {
            'amlModuleIdentifier': {
                'moduleName': self.name,
                'moduleVersion': self.version,
                'namespace': self.namespace,
            },
            'jobType': self.job_type,
            'metadata': {
                'annotations': annotations,
            },
            'description': self.description,
            'isDeterministic': self.is_deterministic,
            'inputs': self.base_params_to_list(self.input_ports + self.params),
            'outputs': self.base_params_to_list(self.output_ports),
            'implementation': self.implementation
        }
        result = self.remove_empty_values(result)
        # TODO: handle image case in the future
        result = _to_ordered_dict(result)
        return result

    def remove_empty_values(self, data):
        if not isinstance(data, dict):
            return data
        return {k: self.remove_empty_values(v) for k, v in data.items() if v is not None}

    def gen_aml_environment_from_conda(self, conda) -> Optional[Union[str, dict]]:
        env = {}
        if self.base_image and self.base_image != self.DEFAULT_BASE_DOCKER_IMAGE:
            env['docker'] = {'baseImage': self.base_image}
            if self.container_registry:
                env['docker']['baseImageRegistry'] = self.container_registry_dict
        if conda is None:
            return env if env else None
        conda_key = 'condaDependenciesFile' if isinstance(conda, str) else 'condaDependencies'
        env['python'] = {conda_key: conda}
        return env

    def _save_to_code_folder(self, folder, spec_file=None):
        yaml = _setup_yaml(typ='rt')
        if spec_file is None:
            spec_file = self.DEFAULT_SPEC_FILE
        with open(Path(folder) / spec_file, 'w') as fout:
            yaml.dump(self.spec_dict, fout)


class _YamlModuleDefinition(_ModuleDefinition):
    def __init__(self, dct):
        self._dct = dct

    @property
    def module_identifier(self):
        return self._dct['amlModuleIdentifier']

    @property
    def name(self) -> str:
        return self.module_identifier['moduleName']

    @property
    def namespace(self) -> Optional[str]:
        return self.module_identifier.get('namespace')

    @property
    def version(self) -> str:
        return self.module_identifier.get('moduleVersion')

    @property
    def description(self) -> Optional[str]:
        return self._dct.get('description')

    @property
    def is_deterministic(self) -> Optional[bool]:
        return self._dct.get('isDeterministic')

    @property
    def source_directory(self) -> str:
        return self.container.get('sourceDirectory') if self.container else None

    @property
    def job_type(self) -> Optional[str]:
        return self._dct.get('jobType')

    @property
    def metadata(self):
        return self._dct.get('metadata') or {}

    @property
    def annotations(self):
        return self.metadata.get('annotations', {})

    @property
    def tags(self) -> Optional[List[str]]:
        return self.annotations.get('tags')

    @property
    def contact(self) -> Optional[str]:
        return self.annotations.get('contact')

    @property
    def help_document(self) -> Optional[str]:
        return self.annotations.get('helpDocument')

    @property
    def os(self):
        return _get_value_by_key_path(self._dct, 'implementation/os')

    @property
    def container(self):
        return _get_value_by_key_path(self._dct, 'implementation/container')

    @property
    def image(self) -> Optional[str]:
        return None if self.container is None else self.container.get('image')

    @property
    def container_registry_dict(self) -> Optional[ContainerRegistry]:
        return self.container.get('imageRegistry') if self.image else self.aml_environment.get('baseImageRegistry')

    @property
    def aml_environment(self) -> Optional[Union[str, dict]]:
        return self.container.get('amlEnvironment') if self.container else None

    @property
    def base_image(self):
        env = self.aml_environment
        return None if env is None else _get_value_by_key_path(env, 'docker/baseImage')

    @property
    def conda_dependencies(self) -> Optional[Union[str, dict]]:
        env = self.aml_environment
        return None if env is None \
            else _get_value_by_key_path(env, 'python/condaDependencies') \
            or _get_value_by_key_path(env, 'python/condaDependenciesFile')

    @property
    def command(self) -> List[str]:
        return self.container.get('command') if self.container else None

    @property
    def args(self) -> List:
        return self.container.get('args') or [] if self.container else None

    def enumerate_args(self):
        if self.args is None:
            return
        for arg_item in self.args:
            if isinstance(arg_item, list):
                yield from arg_item
            else:
                yield arg_item

    def get_arg_type_by_name(self, name):
        for arg_item in self.enumerate_args():
            if isinstance(arg_item, dict):
                key, value = next(item for item in arg_item.items())
                if value == name:
                    return key
        return None

    def is_input_port(self, name):
        arg_type = self.get_arg_type_by_name(name)
        # Here we assume the input port must have arg item {inputPath: port_name}.
        if arg_type is not None:
            return 'inputPath' == arg_type
        # If there is no arg item, we check whether the type is parameter type.
        for i in self._dct.get('inputs') or []:
            if i['name'] == name:
                return not isinstance(i['type'], str) or i['type'] not in Param.PARAM_TYPES
        return False

    def _yield_inputs(self, inputs):
        """Recursively yield inputs from the input list."""
        for i in inputs:
            i = copy.copy(i)
            options = []
            if 'options' in i:
                options = i['options']
                i['options'] = [option if not isinstance(option, dict) else list(option.keys())[0]
                                for option in options]
            # Yield the current input first
            yield i

            # Then yield the input in options
            for option in options:
                # By design, option could be a simple string or a dict which only contain one item,
                # the key is the option name, the value is the list of the child parameters.
                # For example: {'Some Option': [{'name': 'Child Param1', type: 'Int'}, {'name': 'Child Param2'}]}
                # Thus for the case that the option is a dict, we need to yield the child parameters,
                if not isinstance(option, dict):
                    continue
                for option_input in self._yield_inputs(list(option.values())[0]):
                    option_input['optional'] = True  # All the input in options are optional.
                    yield option_input

    def _get_all_inputs(self):
        """Get all inputs including the inputs in enum values."""
        return [i for i in self._yield_inputs(self._dct.get('inputs', []))]

    @property
    def input_ports(self) -> List[InputPort]:
        inputs = self._dct.get('inputs') or []
        return [port for port in inputs if self.is_input_port(port['name'])]

    @property
    def output_ports(self) -> List[OutputPort]:
        return self._dct.get('outputs') or []

    @property
    def params(self) -> List[Param]:
        inputs = self._get_all_inputs()
        return inputs if not inputs else [param for param in inputs if not self.is_input_port(param['name'])]

    @classmethod
    def from_dict(cls, dct):
        return cls(dct)


class _YamlParallelModuleDefinition(_YamlModuleDefinition):

    def is_input_port(self, name):
        return super().is_input_port(name) or name in self.input_data

    @property
    def container(self):
        return _get_value_by_key_path(self._dct, 'implementation/parallel')

    @property
    def input_data(self):
        return self.container['inputData']  # inputData is a required field

    @property
    def output_data(self):
        return self.container.get('outputData')

    @property
    def entry(self):
        return self.container['entry']

    @property
    def command(self) -> List[str]:
        return []


class _YamlHDInsightModuleDefinition(_YamlModuleDefinition):

    @property
    def container(self):
        return _get_value_by_key_path(self._dct, 'implementation/hdinsight')

    @property
    def jars(self) -> Optional[List[str]]:
        return self.container.get('jars')

    @property
    def py_files(self) -> Optional[List[str]]:
        return self.container.get('pyFiles')

    @property
    def file(self):
        return self.container['file']

    @property
    def files(self) -> Optional[List[str]]:
        return self.container.get('files')

    @property
    def class_name(self) -> Optional[str]:
        return self.container.get('className')

    @property
    def archives(self) -> Optional[List[str]]:
        return self.container.get('archives')


class BaseModuleSpec(_ModuleDefinition):
    """A module spec class which defines basic/MPI Module."""

    DEFAULT_CONDA_FILE = 'conda.yaml'
    IMPLEMENTATION_KEY = 'container'

    def __init__(
            self, name, version=None, namespace=None,
            description=None, is_deterministic=None,
            job_type=None, tags=None, contact=None,
            help_document=None, base_image=None, conda_dependencies=None,
            custom_image=None,
            container_registry=None,
            os=None,
            command=None, args=None,
            inputs=None, outputs=None, params=None,
            source_directory=None,
            annotations=None,
    ):
        """Define a basic/MPI module spec."""

        if custom_image:
            if conda_dependencies:
                raise ValueError("Conda dependencies must be None when the custom image is not None.")
            if base_image:
                raise ValueError("Base image must be None when the custom image is not None.")

        self._image = custom_image
        if container_registry is not None and not isinstance(container_registry, ContainerRegistry):
            raise TypeError(
                "Container registry must be type azureml.core.container_registry.ContainerRegistry, got '%s'" %
                container_registry)
        self._container_registry = container_registry

        if isinstance(conda_dependencies, dict):
            self._conda_dependencies = _Dependencies(conda_dependencies)
        else:
            self._conda_dependencies = conda_dependencies

        self._base_image = base_image

        self._name = name
        if version is None:
            version = '0.0.1'
        self._version = version
        self._namespace = namespace

        self._command = command
        self._args = args
        self._os = os

        self._inputs = inputs
        self._outputs = outputs
        self._params = params

        self._description = description
        self._is_deterministic = is_deterministic
        self._job_type = job_type
        self._tags = tags
        self._contact = contact
        self._help_document = help_document

        self._source_directory = str(Path(source_directory).resolve().absolute().as_posix()) \
            if source_directory else None

        self._annotations = annotations if annotations else None

    @property
    def name(self) -> str:
        """Name of module."""
        return self._name

    @property
    def version(self) -> str:
        """Version of the module.

        Could be arbitrary text, but it is recommended to follow the Semantic Versioning specification.
        """
        return self._version

    @property
    def namespace(self) -> Optional[str]:
        """Namespace of module.

        Namespace is used to avoid naming conflicts of modules created by different teams or organizations.
        """
        return self._namespace

    @property
    def annotations(self) -> Optional[Union[str, dict]]:
        """Annotations of the module, put any user defined data in this field."""
        return self._annotations

    @property
    def command(self) -> List[str]:
        """Specify the command to start to run the module code."""
        return self._command

    @property
    def description(self) -> Optional[str]:
        """Detailed description of the module. Could be multiple lines."""
        return self._description

    @property
    def base_image(self):
        """Specify the docker base image to build image with the conda dependency."""
        return self._base_image

    @property
    def image(self):
        """Specify the user provided docker image when the module doesn't use conda."""
        return self._image

    @property
    def container_registry(self) -> Optional[ContainerRegistry]:
        return self._container_registry

    @property
    def is_deterministic(self) -> Optional[bool]:
        """Specify whether the module will always generate the same result when given the same input data.

        Defaults to True if not specified. Typically for modules which will load data from external resources, e.g.
        Import data from a given url, should set to False since the data to where the url points to may be updated.
        """
        return self._is_deterministic

    @property
    def job_type(self) -> Optional[str]:
        """Job type of the module.

        Could be basic, mpi.
        Defaults to basic if not specified, which refers to run job on a single compute node.
        """
        return self._job_type

    @property
    def tags(self) -> Optional[List[str]]:
        """Add a list of tags to the module to describe the category of the module."""
        return self._tags

    @property
    def contact(self) -> Optional[str]:
        """Contact info of this module's author team.

        Typically contains user or organization's name and email.
        An example:AzureML Studio Team <stcamlstudiosg@microsoft.com>
        """
        return self._contact

    @property
    def help_document(self) -> Optional[str]:
        """Url of the module's documentation.

        Will be shown as a link on AML Designer's page.
        """
        return self._help_document

    @property
    def conda_dependencies(self) -> Optional[Union[str, dict]]:
        """Could be a string to indicate the file, or a _Dependencies object to indicate the conda dependencies,
        returns None if not set."""
        if isinstance(self._conda_dependencies, _Dependencies):
            return self._conda_dependencies.conda_dependency_dict
        else:
            return self._conda_dependencies

    @property
    def os(self):
        """Specify the operating system where the module will run. Could be Windows/Linux."""
        return self._os

    @property
    def args(self) -> List:
        """Specify the arguments used along with command.

        This list may consist place holders of Inputs and Outputs.
        See [CLI Argument Place Holders](#CLI Argument Place Holders) for details.
        """
        if not self._args:
            return []
        # Here we call YamlFlowList and YamlFlowDict to have better representation when dumping args to yaml.
        result = []
        for arg in self._args:
            if isinstance(arg, list):
                arg = [_YamlFlowDict(item) if isinstance(item, dict) else item for item in arg]
                arg = _YamlFlowList(arg)
            result.append(arg)
        return result

    @property
    def input_ports(self) -> List[InputPort]:
        """Input ports of the module."""
        return self._inputs if self._inputs else []

    @property
    def output_ports(self) -> List[OutputPort]:
        """Output ports of the module."""
        return self._outputs if self._outputs else []

    @property
    def params(self) -> List[Param]:
        """Parameters of the module."""
        return self._params if self._params else []

    def _save_to_code_folder(self, folder, spec_file=None):
        """Save the module spec to specific folder under the source directory."""
        if spec_file is None:
            spec_file = self.DEFAULT_SPEC_FILE
        source_directory = self._source_directory if self._source_directory else \
            Path(folder).resolve().absolute().as_posix()
        spec_file = (Path(folder) / spec_file).resolve()
        spec_dict = self.spec_dict
        # Check whether the spec path is valid and set sourceDirectory to spec_dict.
        try:
            source_dir_2_spec_folder = _relative_to(spec_file.parent, source_directory, raises_if_impossible=True)
        except ValueError as e:
            raise ValueError("Target spec file '%s' is not under the source directory '%s'." % (
                spec_file.absolute().as_posix(), source_directory
            )) from e
        relative_path = source_dir_2_spec_folder.as_posix()
        if relative_path != '.':
            relative_path = ''.join(['../'] * len(relative_path.split('/')))  # aa/bb => ../../
            spec_dict['implementation'][self.IMPLEMENTATION_KEY]['sourceDirectory'] = relative_path

        # If conda dependencies is not set, set it to spec file's folder and relative path to sourceDirectory
        conda = self.conda_dependencies
        if conda is None and self.image is None:
            conda = (source_dir_2_spec_folder / self.DEFAULT_CONDA_FILE).as_posix()
            aml_environment = self.gen_aml_environment_from_conda(conda)
            spec_dict['implementation'][self.IMPLEMENTATION_KEY]['amlEnvironment'] = aml_environment
            spec_dict = self.remove_empty_values(spec_dict)

        # Dump a default conda dependencies to the folder if the conda file doesn't exist.
        # The scenario that the initialized conda is a file need to be refined
        # because we don't know where is the conda.
        if isinstance(conda, str) and not (Path(source_directory) / conda).exists():
            logging.info("Conda file %s doesn't exist in the folder %s, a default one is dumped." % (conda, folder))
            YAML._dump_yaml_file(
                _Dependencies.create_default(self.job_type).conda_dependency_dict,
                Path(source_directory) / conda
            )

        YAML._dump_yaml_file(spec_dict, spec_file, unsafe=True, header=YAML_HELP_COMMENTS)

    @classmethod
    def _from_dict(cls, dct: dict):
        if 'type' in dct:
            dct.pop('type')  # Only job_type is in the dct.
        if 'parameters' in dct:
            dct['params'] = dct.pop('parameters')
        for key in ['inputs', 'outputs', 'params']:
            if key in dct:
                dct[key] = list(dct[key].values())
        if 'command' in dct and 'args' not in dct:
            command = dct['command']
            dct['command'], dct['args'] = command[:2], command[2:]
        return cls(**dct)

    def save(self, path):
        path = Path(path)
        return self._save_to_code_folder(folder=path.parent, spec_file=path.name)


YAML_HELP_COMMENTS = """#  This is an auto generated module spec yaml file.
#  For more details, please refer to https://aka.ms/azureml-module-specs
"""


class ParallelRunModuleSpec(BaseModuleSpec):
    """A module spec class which defines parallel run Module."""

    IMPLEMENTATION_KEY = 'parallel'

    def __init__(
            self, name, version=None, namespace=None,
            description=None, is_deterministic=None,
            tags=None, contact=None,
            help_document=None, base_image=None, conda_dependencies=None,
            args=None,
            inputs=None, outputs=None, params=None,
            entry=None, input_data=None, output_data=None,
            **kwargs
    ):
        """Define a parallel run module spec."""
        BaseModuleSpec.__init__(self, name=name, version=version, namespace=namespace,
                                description=description, is_deterministic=is_deterministic,
                                job_type='parallel', tags=tags, contact=contact,
                                help_document=help_document, base_image=base_image,
                                conda_dependencies=conda_dependencies,
                                command=None, args=args,
                                inputs=inputs, outputs=outputs, params=params,
                                **kwargs,
                                )
        self._entry = entry
        self._input_data = input_data
        self._output_data = output_data

    @property
    def entry(self):
        """User script to process mini_batches."""
        return self._entry

    @property
    def input_data(self):
        """Input(s) provide the data to be splitted into mini_batches for parallel execution.

        Specify the name(s) of the corresponding input(s) here.
        """
        return self._input_data

    @property
    def output_data(self):
        """Output for the summarized result that generated by the user script.

        Specify the name of the corresponding output here.
        """
        return self._output_data

    @property
    def implementation(self):
        """Module's implementation.

        Defines how and where to run the module code.
        """
        return {
            'os': self.os,
            self.IMPLEMENTATION_KEY: {
                'amlEnvironment': self.aml_environment,
                'image': self.image,
                'imageRegistry': self.container_registry_dict if self.image else None,
                'inputData': self.input_data,
                'outputData': self.output_data,
                'entry': self.entry,
                'args': self.args,
            },
        }


class _DtoParam(Param):
    """Param built from _ModuleDto, all properties are provided from it."""
    def __init__(self, name, arg_name, data_type, cli_option, default_value=None, options=None):
        self._cli_option = cli_option
        super(_DtoParam, self).__init__(
            name=name, arg_name=arg_name, type=data_type, default=default_value, enum=options)

    def to_cli_option_str(self):
        return self._cli_option


def _python_type_to_spec_type(python_type) -> str:
    if python_type is int:
        return 'Integer'
    elif python_type is float:
        return 'Float'
    elif python_type is bool:
        return 'Boolean'
    elif python_type is str:
        return 'String'
    # default to string
    return 'String'


def _get_io_spec_from_component(module):
    """Get input_ports, output_ports and params from module dto.

    :param module: wrapped module
    :type module: azure.ml.component.Component
    """
    from azure.ml.component._module_dto import _type_code_to_python_type
    # name -> input/output/param python interface, used to get arg name and cli option.
    name_to_input_python_interface = {}
    python_interface_dict_list = [
        module._module_dto.module_python_interface.inputs,
        module._module_dto.module_python_interface.outputs,
        module._module_dto.module_python_interface.parameters
    ]
    python_interface_dict_list = list(itertools.chain.from_iterable(python_interface_dict_list))
    for element in python_interface_dict_list:
        name_to_input_python_interface[element.name] = element

    def build_param(
            name, is_param=False, data_type_ids_list=None, data_type_id=None, parameter_type=None, default_value=None,
            **kwargs):
        python_interface_dict = name_to_input_python_interface[name]
        cli_option = python_interface_dict.command_line_option
        arg_name = python_interface_dict.argument_name
        # Get data_type
        if is_param:
            # Parameter
            data_type = _python_type_to_spec_type(_type_code_to_python_type(parameter_type))
        else:
            # Input/Output port
            data_type = None
            if data_type_ids_list is not None:
                # If multiple data types are specified, pick the first one, since we can only gen one type of input
                if len(data_type_ids_list) > 0:
                    data_type = data_type_ids_list[0]
            elif data_type_id is not None:
                data_type = data_type_id

        return _DtoParam(name=name, arg_name=arg_name, data_type=data_type, cli_option=cli_option,
                         default_value=default_value)

    dto_inputs = module._module_dto.module_entity.structured_interface.inputs
    inputs = [build_param(**input.as_dict()) for input in dto_inputs]

    dto_outputs = module._module_dto.module_entity.structured_interface.outputs
    outputs = [build_param(**output.as_dict()) for output in dto_outputs]

    dto_params = module._module_dto.module_entity.structured_interface.parameters
    params = [
        build_param(is_param=True, **param.as_dict())
        for param in dto_params if param.name in name_to_input_python_interface.keys()
    ]
    return inputs, outputs, params
