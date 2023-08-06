# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from contextlib import contextmanager
from enum import Enum
from pathlib import Path
from typing import Dict, Any

from azure.ml.component._api._component_snapshot import ComponentSnapshot
from azure.ml.component._api._utils import _looks_like_a_url, _RE_GITHUB_URL, is_absolute, check_spec_file
from azureml.exceptions import UserErrorException


class ComponentWorkingMechanism(Enum):
    Normal = 'Normal'
    OutputToDataset = 'OutputToDataset'


class ComponentSourceType(Enum):
    Local = 'Local'
    GithubFile = 'GithubFile'
    GithubFolder = 'GithubFolder'
    DevopsArtifacts = 'DevopsArtifactsZip'


class ComponentSource:
    def __init__(
            self,
            source_type: ComponentSourceType,
            spec_file: str = None,
            package_zip: str = None,
            snapshot: ComponentSnapshot = None,
    ):
        self._source_type = source_type
        self._spec_file = spec_file
        self._package_zip = package_zip
        self._snapshot = snapshot

    @property
    def source_type(self):
        return self._source_type

    def is_local_source(self):
        return self._source_type == ComponentSourceType.Local

    @property
    def spec_file(self):
        return self._spec_file

    @property
    def package_zip(self):
        return self._package_zip

    @property
    def snapshot(self):
        return self._snapshot

    def is_invalid_entry(self, entry_file):
        # For sweep component which refers a registered component, always return False
        # As we don't have an entry in that case
        if self._snapshot and self._snapshot.trial_component:
            return False
        # We only check whether the entry file for local source, since we don't download snapshot for remote sources.
        if not self.is_local_source():
            return False

        # We don't check absolute path because it might be in the docker image which we are not able to check.
        if is_absolute(entry_file):
            return False

        # If the entry file cannot be found in snapshot, it is invalid.
        return not self.snapshot.file_exists(relative_path=entry_file)

    @staticmethod
    def from_source(spec_file, package_zip, amlignore_file=None, logger=None, from_cli=False,
                    params_override: Dict[str, Any]=None):
        if not logger:
            raise ValueError('logger must be set.')

        if not spec_file and not package_zip:
            raise UserErrorException('Either spec file or package zip need to be specified.')

        # Currently treat as devops build drop when package_zip is specified.
        if package_zip:
            # DevOps build drop currently can only specified with a url.
            if not _looks_like_a_url(package_zip):
                raise UserErrorException(
                    'Currently package zip only accepts url. \n'
                    'To create a component from local path, '
                    'Specify spec file to create, eg: /path/to/the/component/spec.yaml", '
                    'the folder containing the spec file(/path/to/the/component/) '
                    'will be zipped and uploaded automatically.')

            return ComponentSource(
                source_type=ComponentSourceType.DevopsArtifacts,
                spec_file=spec_file,
                package_zip=package_zip,
            )

        # If package_zip not specified, check whether spec_file is a url
        if _looks_like_a_url(spec_file):
            if not _RE_GITHUB_URL.match(spec_file):
                raise UserErrorException(
                    'Invalid url for spec file. Expects to be a url to the spec file in a GitHub repo.\n'
                    'e.g https://github.com/user/repo_name/blob/master/component_name/component_spec.yaml')

            return ComponentSource(
                source_type=ComponentSourceType.GithubFile,
                spec_file=spec_file,
            )

        # Otherwise, create component source from local path
        else:
            path = check_spec_file(spec_file)

            snapshot = ComponentSnapshot.from_spec(path, additional_amlignore_file=amlignore_file, logger=logger,
                                                   from_cli=from_cli, params_override=params_override)

            return ComponentSource(
                source_type=ComponentSourceType.Local,
                spec_file=snapshot.spec_file_relative_path.as_posix(),
                snapshot=snapshot,
            )


class ComponentSourceParams:
    """Create param dict for component register/parse according to component source type."""

    def __init__(self, source: ComponentSource):
        self._source = source
        self._params = {
            'component_source_type': self._source.source_type.value,
            'yaml_file': self._source.spec_file,
        }

    @contextmanager
    def create(self, spec_only=False, spec_folder: Path = None):
        # Used context manager here since the zip file for local component need to stay open.
        if self._source.source_type == ComponentSourceType.Local:
            snapshot = self._source.snapshot
            zip_file = snapshot.create_spec_snapshot(spec_folder=spec_folder) \
                if spec_only else snapshot.create_snapshot()
            if snapshot.sweep:
                self._params.update({'yaml_file': snapshot.sweep_spec_relative_path.as_posix()})
            with open(zip_file, 'rb') as f:
                self._params.update({'snapshot_source_zip_file': f})
                yield self._params
        elif self._source.source_type == ComponentSourceType.GithubFile:
            yield self._params
        elif self._source.source_type == ComponentSourceType.DevopsArtifacts:
            self._params.update({'devops_artifacts_zip_url': self._source._package_zip})
            yield self._params
