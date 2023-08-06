# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import json
import hashlib
from pathlib import Path
from typing import Union
from azureml.core.environment import DEFAULT_CPU_IMAGE, Environment as CoreEnvironment
from azure.ml.component._util._constants import LOCAL_PREFIX
from ._core import AssetVersion
from .._util._yaml_utils import YAML
from .._util._exceptions import UserErrorException

# exclusive curated environment for CommandComponent created by PipelineExpression
CURATED_ENV_NAME_FOR_EXPRESSION_COMPONENT = 'AzureML-Component'
CURATED_ENV_DICT_FOR_EXPRESSION_COMPONENT = {'name': CURATED_ENV_NAME_FOR_EXPRESSION_COMPONENT}


class Environment(AssetVersion):
    """This is a simple implementation of environment, will be replaced by the finalized one."""

    _environment_cache = {}

    def __init__(self, name: str = None, version: str = None, conda: Union[dict, 'Conda'] = None,
                 docker: Union[dict, 'Docker'] = None, os: str = None):
        """Initialize an environment object with conda, docker and os.

        :param name: Registered environment name.
        :param version: Registered environment version.
        :param conda: A conda environment dict to represent the python dependencies.
        :param docker: A docker section which contain a docker image to run the component.
        :param os: Indicate which os could run the component. Could be Linux/Windows.
        """
        self._name = name
        self._version = version
        self._os = os if os else "Linux"
        if isinstance(conda, dict):
            conda = Conda._from_dict(conda)
        self._conda = conda
        if isinstance(docker, dict):
            docker = Docker._from_dict(docker)
        self._docker = docker

    @property
    def name(self):
        return self._name

    @property
    def version(self):
        return self._version

    @property
    def docker(self):
        return self._docker

    @property
    def conda(self):
        return self._conda

    @property
    def os(self):
        return self._os

    @classmethod
    def _from_dict(cls, dct, base_dir=None, raise_on_non_exist_error=False):
        if isinstance(dct.get('conda'), dict):
            conda = Conda._from_dict(dct['conda'], base_dir=base_dir,
                                     raise_on_non_exist_error=raise_on_non_exist_error)
            dct['conda'] = conda
        if isinstance(dct.get('docker'), dict):
            docker = Docker._from_dict(dct['docker'], base_dir=base_dir,
                                       raise_on_non_exist_error=raise_on_non_exist_error)
            dct['docker'] = docker
        return cls(**dct)

    def _to_dict(self):
        if self.name:
            return {
                'name': self.name,
                'version': self.version
            }
        else:
            return {
                'docker': self._docker._to_dict() if self._docker else None,
                'conda': self._conda._to_dict() if self._conda else None,
                'os': self.os,
            }

    def _to_aml_sdk_env(self):
        from azureml.core.environment import Environment, CondaDependencies as CoreCondaDependencies
        env = Environment(name=self.name, _skip_defaults=True)
        env.version = self.version
        if self.conda and self.conda.conda_dependencies:
            env.python.conda_dependencies = CoreCondaDependencies(
                _underlying_structure=self.conda.conda_dependencies._to_dict())
        else:
            # If conda is not set, use the user's custom image.
            env.python.user_managed_dependencies = True
        if self._docker:
            env.docker.base_image = self._docker.image
            env.docker.base_dockerfile = self._docker.base_dockerfile
            env.docker.platform.os = self.os
        return env

    def _get_or_register(self, workspace):
        """
        Get or register environment in the workspace.

        :param workspace: The workspace to get or register environment
        :type workspace: azureml.core.workspace.Workspace
        :return: The environment in the workspace.
        :rtype: azureml.core.environment.Environment
        """
        env_cache_key = json.dumps(self._to_dict(), sort_keys=True)
        workspace_id = workspace._workspace_id
        if self._environment_cache.get(env_cache_key, {}).get(workspace_id):
            return self._environment_cache[env_cache_key][workspace_id]
        else:
            # When component is initialized by ComponentDefinition, using _definition to get environment.
            aml_sdk_env = self._to_aml_sdk_env()
            # If component using curated environment, definition environment name and version not be None.
            # If not using curated environment, environment not set name and version, only contains
            # python and docker info.
            if aml_sdk_env.name:
                aml_sdk_env = CoreEnvironment.get(
                    workspace=workspace, name=aml_sdk_env.name, version=aml_sdk_env.version)
            else:
                # When register environment, it need to set environment name and will generate conda env name by hash
                # env info, except name. Since environments with same env info and diff name, have same conda env name.
                # Because component name may contain strange character, using the environment definition hash
                # as env name to avoid registering failure.
                aml_sdk_env.name = hashlib.md5(env_cache_key.encode()).hexdigest()
                aml_sdk_env = aml_sdk_env.register(workspace)
            if env_cache_key not in self._environment_cache:
                self._environment_cache[env_cache_key] = {}
            self._environment_cache[env_cache_key][workspace_id] = aml_sdk_env
            return aml_sdk_env


class Docker:
    """Docker environment settings for running a component."""

    DEFAULT_CPU_IMAGE = DEFAULT_CPU_IMAGE

    def __init__(self, image: str = None, base_dockerfile: str = None):
        """Initialize docker environment with image or dockerfile.

        :param image: The base image.
        :param base_dockerfile: Path of the base dockerfile.
        """
        self._image = image
        self._base_dockerfile = base_dockerfile

    @property
    def image(self):
        return self._image

    @property
    def base_dockerfile(self):
        return self._base_dockerfile

    @classmethod
    def _from_dict(cls, dct, base_dir=None, raise_on_non_exist_error=False):
        old_key_mapping = {
            'baseImage': 'image'
        }
        for k, v in old_key_mapping.items():
            if k in dct:
                dct[v] = dct.pop(k)
        if dct.get('image', None):
            return cls(image=dct['image'])
        dockerfile = dct.get('base_dockerfile', None) or dct.get('build', {}).get('dockerfile', None)
        if dockerfile:
            # In case base_dockerfile is in 'file:xxx' format
            file_path = _parse_file_path(dockerfile)
            if file_path:
                file_path = _resolve_file_path(file_path, base_dir)
                return _init_from_file(cls._from_dockerfile, file_path,
                                       raise_on_non_exist_error=raise_on_non_exist_error)
            return cls(base_dockerfile=dockerfile)
        return cls()

    def _to_dict(self):
        docker_dict = {}
        if self._image:
            docker_dict['image'] = self._image
        if self._base_dockerfile:
            docker_dict['base_dockerfile'] = self._base_dockerfile
        return docker_dict

    def _to_dict_in_vnext_format(self):
        if self._image:
            return {
                'image': self._image
            }
        return {
            'build': {
                'dockerfile': self._base_dockerfile
            }
        }

    @classmethod
    def _from_dockerfile(cls, file_path):
        with open(file_path) as fin:
            dockerfile = fin.read()
            return cls(base_dockerfile=dockerfile)


class CondaDependencies:
    def __init__(self, name: str = None, channels: [str] = None, dependencies: [str] = None, variables: dict = None):
        """Initialize conda environment with name, channels and dependencies.

        :param name: Conda environment name.
        :param channels: A list of conda channel.
        :param dependencies: A list of Python dependency.
        :param variables: A dict of environment variables.
        """
        self._name = name
        self._channels = channels
        self._dependencies = dependencies
        self._variables = variables
        # For dsl component
        self._file_path = None

    @property
    def name(self):
        return self._name

    @property
    def channels(self):
        return self._channels

    @property
    def dependencies(self):
        return self._dependencies

    @property
    def variables(self):
        return self._variables

    @classmethod
    def _from_dict(cls, dct):
        return cls(**dct)

    def _to_dict(self):
        dct = {}
        if self.name:
            dct["name"] = self.name
        if self.channels:
            dct["channels"] = self.channels
        if self.dependencies:
            dct["dependencies"] = self.dependencies
        if self.variables:
            dct["variables"] = self.variables
        return dct

    @classmethod
    def _from_file(cls, file_path):
        with open(file_path) as fin:
            dct = YAML.safe_load(fin)
            result = cls._from_dict(dct)
            result._file_path = file_path
            return result

    @classmethod
    def _from_pip_requirements_file(cls, file_path):
        with open(file_path) as fin:
            pip_requirements = fin.read().splitlines()
            dct = {
                "name": "project_environment",
                "dependencies": [
                    "python=3.6.2",
                    {
                        "pip": pip_requirements
                    }
                ]
            }
            return cls._from_dict(dct)


class Conda:
    """Conda environment settings for running a component."""

    CONDA_FILE_KEY = 'conda_dependencies_file'
    CONDA_DICT_KEY = 'conda_dependencies'
    PIP_REQUIREMENTS_KEY = 'pip_requirements_file'

    def __init__(self, conda_dependencies: CondaDependencies = None):
        self._conda_dependencies = conda_dependencies

    @property
    def conda_dependencies(self):
        return self._conda_dependencies

    @classmethod
    def _from_dict(cls, dct, base_dir=None, raise_on_non_exist_error=False):
        old_key_mapping = {
            'condaDependencies': cls.CONDA_DICT_KEY,
            'condaDependenciesFile': cls.CONDA_FILE_KEY,
            'pipRequirementsFile': cls.PIP_REQUIREMENTS_KEY,
        }
        for k, v in old_key_mapping.items():
            if k in dct:
                dct[v] = dct.pop(k)
        if dct.get(cls.CONDA_DICT_KEY, None):
            return cls(CondaDependencies(**dct[cls.CONDA_DICT_KEY]))
        if dct.get(cls.CONDA_FILE_KEY, None):
            file_path = _resolve_file_path(dct[cls.CONDA_FILE_KEY], base_dir)
            conda_dependencies = _init_from_file(CondaDependencies._from_file, file_path,
                                                 raise_on_non_exist_error=raise_on_non_exist_error)
            return cls(conda_dependencies)
        if dct.get(cls.PIP_REQUIREMENTS_KEY, None):
            file_path = _resolve_file_path(dct[cls.PIP_REQUIREMENTS_KEY], base_dir)
            conda_dependencies = _init_from_file(CondaDependencies._from_pip_requirements_file, file_path,
                                                 raise_on_non_exist_error=raise_on_non_exist_error)
            return cls(conda_dependencies)
        return cls()

    def _to_dict(self):
        return {
            self.CONDA_DICT_KEY: self._conda_dependencies._to_dict() if self._conda_dependencies else None
        }


def _parse_file_path(value: str):
    return value[len(LOCAL_PREFIX):]  \
        if value and value.startswith(LOCAL_PREFIX) else None


def _resolve_file_path(relative_file_path, base_dir):
    if base_dir:
        return Path(base_dir, relative_file_path).resolve().as_posix()
    return relative_file_path


def _init_from_file(init_func, file_path, raise_on_non_exist_error=False):
    try:
        return init_func(file_path)
    except FileNotFoundError as e:
        err_msg = f"File with path {file_path!r} does not exist."
        if raise_on_non_exist_error:
            raise UserErrorException(err_msg) from e
        else:
            # Suppress for now
            # logging.warning(err_msg)
            return None
    except Exception as e:
        raise UserErrorException(f"File with path {file_path!r} is not parsable.") from e
