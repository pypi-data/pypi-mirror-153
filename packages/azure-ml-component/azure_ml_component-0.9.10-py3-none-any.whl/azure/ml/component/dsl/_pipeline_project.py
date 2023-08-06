# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""A helper class which builds a pipeline project skeleton."""
import argparse
import inspect
import json
import os
import platform
import shutil
import sys
from pathlib import Path
from typing import Union, List
from enum import Enum

from azure.ml.component._util._yaml_utils import YAML
from azureml.core import Workspace
from azureml.exceptions import UserErrorException

from azure.ml.component.dsl._component_local_param_builder import _ComponentLocalParamBuilderFromSpec
from azure.ml.component.dsl._argparse import gen_component_by_argparse
from azure.ml.component._version import VERSION
from azure.ml.component.dsl._utils import _sanitize_python_class_name, logger, BackUpFiles, _log_file_skip, \
    _log_file_update, _log_file_create, _log_without_dash, to_literal_str, _find_py_files_in_target, \
    _split_path_into_list, _change_working_dir, _is_function, _get_func_def, _import_component_with_working_dir, \
    _has_dsl_component_str, _get_component_path_and_name_from_source, timer_decorator, _source_exists, \
    _is_notebook, NOTEBOOK_EXT, _try_to_get_relative_path, is_py_file
from azure.ml.component.dsl._component import ComponentExecutor
from azure.ml.component.dsl._module_spec import SPEC_EXT
from azure.ml.component._util._loggerfactory import track, _LoggerFactory, _PUBLIC_API, _most_recent_context, \
    _get_exception_detail
from azure.ml.component._util._telemetry import WorkspaceTelemetryMixin
from azure.ml.component._util._utils import _sanitize_python_variable_name, \
    _sanitize_python_variable_name_with_value_check, _str_to_bool, _try_to_get_workspace, _relative_to
from azure.ml.component._util._exceptions import CustomerCodeError, TooManyDSLComponentsError
from azure.ml.component._restclients.designer.exceptions import AggregatedComponentError

_logger = None


def _get_telemetry_logger():
    global _logger
    if _logger is not None:
        return _logger
    _logger = _LoggerFactory.get_logger()
    return _logger


_most_recent_context.update({'workspace': _try_to_get_workspace()})

# TODO: make this a param of DSLComponentConfigBase
DATA_PATH = Path(__file__).resolve().parent / 'data'
COMPONENT_NAME_CONST = 'COMPONENT_NAME'
COMPONENT_ENTRY_CONST = 'COMPONENT_ENTRY'
FUNCTION_NAME_CONST = 'FUNCTION_NAME'
COMPONENT_CLASS_NAME_CONST = 'COMPONENT_CLASS_NAME'
PIPELINE_NAME_CONST = 'PIPELINE_NAME'
EXPERIMENT_NAME = 'EXPERIMENT_NAME'
DSL_PARAM_DICT_CONST = "'DSL_PARAM_DICT'"

FILE_ENCODING = 'utf-8'


def get_template_file(template_name, job_type='basic'):
    path = DATA_PATH / '{}_component'.format(job_type) / template_name
    if path.is_file():
        return path
    if job_type == 'basic':
        raise FileNotFoundError("The template of basic component is not found: %r" % path)
    # If job_type specific template file doesn't exist, return the default template of basic component.
    return get_template_file(template_name)


class _ComponentObject:
    """Wraps component executor and provides params according to it."""

    def __init__(self, component: ComponentExecutor):
        # TODO: refine this class provide template needed values
        self.component_executor = component
        self.spec = component.spec

        # code path: absolute path of component entry
        self.component_entry_path = Path(inspect.getfile(component._func)).absolute()
        # source directory is current folder
        self.source_directory = Path(os.getcwd())
        # component entry: source dir -> component entry func
        component_entry = str(_relative_to(self.component_entry_path, self.source_directory,
                                           raises_if_impossible=True))
        if component_entry.endswith('.py'):
            component_entry = component_entry[:-3]
        self.component_entry = '.'.join(_split_path_into_list(component_entry))

        # use file name as built resource name prefix
        self.sanitized_entry_name = _sanitize_python_variable_name(self.component_entry_path.stem)
        self.sanitized_component_name = _sanitize_python_variable_name(component.name)
        self.function_name = component._func.__name__

        # generate default input/output, param and command.
        self.component_param_builder = _ComponentLocalParamBuilderFromSpec(
            component.spec, self.source_directory, self.component_entry_path.stem)
        self.component_param_builder.build(dry_run=True)


class _ComponentResourceBase:
    INPUTS_CONST = 'INPUTS_TEMPLATE'
    OUTPUTS_CONST = 'OUTPUTS_TEMPLATE'
    PARAMETERS_CONST = 'PARAMETERS_TEMPLATE'

    def __init__(self, folder: Path, path, type, template, source_dir=None):
        if source_dir is None:
            source_dir = folder
        self.folder = folder
        self.path = folder / path
        self.type = type
        self.template = template
        self.source_directory = source_dir

    @property
    def path(self):
        return Path(self._path)

    @path.setter
    def path(self, path):
        self._path = path

    @property
    def file_info(self):
        return _try_to_get_relative_path(self.path)

    def create(self):
        # default behavior: copy template to path
        os.makedirs(self.path.parent, exist_ok=True)
        shutil.copyfile(self.template, self.path)

    def update(self):
        # call create if file not exist, perform according to strategy if exist.
        pass

    def skip(self):
        _log_file_skip(self.file_info)

    @classmethod
    def _to_literal_items(cls, data: dict, formatter: str, is_path=True):
        literal_items = []
        for key, value in data.items():
            if is_path:
                path_parts = ["'{}'".format(part) for part in value.split('/')]
                value = ' / '.join(path_parts)
            else:
                # to literal str
                if isinstance(value, str):
                    value = "'{}'".format(value)
            literal_items.append(
                formatter.format(key, value))

        return literal_items


class _ComponentResourceWithBackupStrategy(_ComponentResourceBase):
    """Update strategy: Back up resource into backup folder."""

    def __init__(self, folder, path, type, template, backup_folder: Path, source_dir=None):
        super().__init__(folder, path, type, template, source_dir)
        self._backup_folder = backup_folder

    def update(self):
        # back up original file when trying to update it.
        file_exist = self.path.exists()
        if file_exist:
            relative_path = _relative_to(self.path, self.folder, raises_if_impossible=True)
            os.makedirs((self._backup_folder / relative_path).parent, exist_ok=True)
            shutil.copy(self.path, self._backup_folder / relative_path)
        self.create()
        if file_exist:
            _log_file_update(self.file_info)
        else:
            _log_file_create(self.file_info)


class _ComponentResourceWithPreserveStrategy(_ComponentResourceBase):
    """Update strategy: won't update if file exists."""

    def update(self):
        # preserve the original file when trying to update it.
        if self.path.exists():
            self.skip()
        else:
            self.create()
            _log_file_create(self.file_info)


class _ComponentResourceWithExceptionStrategy(_ComponentResourceBase):
    """Update strategy: throw exception if file exists."""

    def update(self):
        # raise exception when trying to trying to update existing file.
        if self.path.exists():
            raise FileExistsError("Target file '{}' already exists.".format(self.path))
        else:
            self.create()
            _log_file_create(self.file_info)


class _SpecFile(_ComponentResourceWithBackupStrategy):
    def __init__(self, component: _ComponentObject, spec_path: Path, backup_folder: Path, source_dir: Path):
        self.component_object = component
        super().__init__(
            spec_path.parent,
            spec_path,
            self.__class__.__name__,
            None,
            backup_folder,
            source_dir)

    @property
    def file_info(self):
        return '{} -> {}'.format(
            _try_to_get_relative_path(self.component_object.component_entry_path),
            _try_to_get_relative_path(self.path)
        )

    def create(self):
        os.makedirs(self.path.parent, exist_ok=True)
        self.component_object.component_executor.to_spec_yaml(
            folder=self.folder,
            spec_file=self.path.name)


class _NotebookFile(_ComponentResourceWithPreserveStrategy):
    NOTEBOOK_TEMPLATE_NAME = 'notebook_sample_code.template'
    RUNSETTINGS_CONST = 'RUNSETTINGS'
    REQUIRED_INPUTS_CONST = 'REQUIRED_INPUTS'

    def __init__(self, component: _ComponentObject, folder: Path, job_type='basic'):
        self.component_object = component
        path = '{}_test.ipynb'.format(component.component_entry_path.stem)
        self.notebook_template = get_template_file(
            self.NOTEBOOK_TEMPLATE_NAME,
            job_type)
        self.job_type = job_type
        super().__init__(folder, path, self.__class__.__name__, self.notebook_template)

    def create(self):
        os.makedirs(self.path.parent, exist_ok=True)
        if self.job_type == 'mpi' or self.job_type == 'parallel':
            runsettings = "component1.runsettings.configure(node_count=1, process_count_per_node=1)"
        else:
            runsettings = ""
        required_inputs_dict = self._build_required_inputs(self.component_object.spec)
        if required_inputs_dict:
            required_inputs = self._to_literal_param(required_inputs_dict, formatter='{}={}', is_path=False)
            required_input_list = ['# Please fill required inputs here\\n"', f'    "        # {required_inputs}']
            required_inputs = ',\n'.join(required_input_list)
        else:
            required_inputs = ""
        with open(self.template, encoding=FILE_ENCODING) as file:
            notebook_content = file.read()
            notebook_content = notebook_content.replace(
                COMPONENT_ENTRY_CONST, self.component_object.component_entry).replace(
                FUNCTION_NAME_CONST, self.component_object.function_name).replace(
                COMPONENT_NAME_CONST, self.component_object.sanitized_component_name).replace(
                EXPERIMENT_NAME, '{}_experiment'.format(self.component_object.sanitized_component_name)).replace(
                PIPELINE_NAME_CONST, '{}_pipeline'.format(self.component_object.sanitized_component_name)).replace(
                self.INPUTS_CONST,
                self._to_literal_param(self.component_object.component_param_builder.inputs)).replace(
                self.PARAMETERS_CONST,
                self._to_literal_param(self.component_object.component_param_builder.parameters, formatter='{}={}',
                                       is_path=False)).replace(
                self.RUNSETTINGS_CONST, runsettings).replace(
                self.REQUIRED_INPUTS_CONST, required_inputs)

            with open(self.path, 'w', encoding=FILE_ENCODING) as out_file:
                out_file.write(notebook_content)

    @classmethod
    def _build_required_inputs(cls, spec):
        # TODO: refine this logic, maybe move to param builder
        result = {}
        for port in spec.inputs.values():
            if not port.optional:
                result[_sanitize_python_variable_name(port.name)] = None
        return result

    @classmethod
    def _to_literal_param(cls, data: dict, formatter="{}=str(Path('data') / {})", is_path=True):
        literal_items = super()._to_literal_items(data, formatter=formatter, is_path=is_path)
        return ', '.join(literal_items)


class _UnittestFile(_ComponentResourceWithPreserveStrategy):
    UT_TEMPLATE_NAME = 'unittest_sample_code.template'

    def __init__(self, component: _ComponentObject, folder: Path, job_type='basic'):
        self.component_object = component
        path = '{}_test.py'.format(component.component_entry_path.stem)
        self.ut_template = get_template_file(self.UT_TEMPLATE_NAME, job_type)
        super().__init__(folder, path, self.__class__.__name__, self.ut_template)

    def create(self):
        os.makedirs(self.path.parent, exist_ok=True)
        with open(self.template, encoding=FILE_ENCODING) as file:
            ut_code = file.read()
            component_class_name = _sanitize_python_class_name(self.component_object.sanitized_entry_name)
            ut_code = ut_code.replace(
                COMPONENT_ENTRY_CONST, self.component_object.component_entry).replace(
                FUNCTION_NAME_CONST, self.component_object.function_name).replace(
                COMPONENT_NAME_CONST, self.component_object.sanitized_component_name).replace(
                COMPONENT_CLASS_NAME_CONST, component_class_name).replace(
                self.INPUTS_CONST,
                self._to_literal_path(self.component_object.component_param_builder.inputs)).replace(
                self.OUTPUTS_CONST,
                self._to_literal_path(self.component_object.component_param_builder.outputs)).replace(
                self.PARAMETERS_CONST, str(self.component_object.component_param_builder.parameters))

            # use mode=conda for test env
            if '_TEST_ENV' in os.environ:
                ut_code = ut_code.replace("mode='docker'", "mode='conda'")

        with open(self.path, 'w', encoding=FILE_ENCODING) as out_file:
            out_file.write(ut_code)

    @classmethod
    def _to_literal_path(cls, data: dict):
        literal_items = super()._to_literal_items(data, formatter="'{}': str(self.base_path / {})", is_path=True)
        return '{' + ','.join(literal_items) + '}'


class _InitFile(_ComponentResourceWithPreserveStrategy):
    def __init__(self, folder):
        path = '__init__.py'
        super().__init__(folder, path, self.__class__.__name__, None)

    def create(self):
        open(self.path, 'a').close()


class _VSCodeFile(_ComponentResourceWithPreserveStrategy):
    VSCODE_DIR = '.vscode'


class _VSCodeLaunch(_VSCodeFile):
    VSCODE_LAUNCH_CONFIG = 'launch.json'
    VSCODE_LAUNCH_CONFIG_TEMPLATE = DATA_PATH / 'inputs' / VSCODE_LAUNCH_CONFIG

    def __init__(self, folder: Path, arguments: list):
        super().__init__(folder, os.path.join(self.VSCODE_DIR, self.VSCODE_LAUNCH_CONFIG), self.__class__.__name__,
                         self.VSCODE_LAUNCH_CONFIG_TEMPLATE)
        # arguments: list of  program -> args dict
        configurations = []
        for argument in arguments:
            args = []
            for arg in argument.get('args', []):
                # corner case in windows: empty string couldn't pass to program in vscode, escape it
                if arg == "" and platform.system() == 'Windows':
                    args.append("\"\"")
                else:
                    args.append(arg)
            name = argument.get('name', None)
            program = argument.get('program', None)
            configurations.append({
                "name": name,
                "type": "python",
                "request": "launch",
                "args": args,
                "console": "integratedTerminal",
                "env": {
                    "PYTHONPATH": "${workspaceFolder}"
                },
                "program": str((Path('${workspaceFolder}') / program).as_posix())
            })
        self.configurations = configurations

    def create(self):
        with open(self.template, encoding=FILE_ENCODING) as file:
            data = json.load(file)
            data['configurations'] = self.configurations
            with open(self.path, 'w', encoding=FILE_ENCODING) as out_file:
                json.dump(data, out_file, indent=4, ensure_ascii=False)


class _VSCodeSetting(_VSCodeFile):
    VSCODE_SETTINGS_CONFIG = 'settings.json'
    VSCODE_SETTINGS_CONFIG_TEMPLATE = DATA_PATH / 'inputs' / VSCODE_SETTINGS_CONFIG

    def __init__(self, folder: Path):
        super().__init__(folder, os.path.join(self.VSCODE_DIR, self.VSCODE_SETTINGS_CONFIG), self.__class__.__name__,
                         self.VSCODE_SETTINGS_CONFIG_TEMPLATE)


class _GitIgnore(_ComponentResourceWithPreserveStrategy):
    GIT_IGNORE = '.gitignore'
    GIT_IGNORE_TEMPLATE = DATA_PATH / GIT_IGNORE

    def __init__(self, folder: Path):
        super().__init__(folder, self.GIT_IGNORE, self.__class__.__name__, self.GIT_IGNORE_TEMPLATE)


class _AMLIgnore(_ComponentResourceWithPreserveStrategy):
    AML_IGNORE = '.amlignore'
    AML_IGNORE_TEMPLATE = DATA_PATH / AML_IGNORE

    def __init__(self, folder: Path):
        super().__init__(folder, self.AML_IGNORE, self.__class__.__name__, self.AML_IGNORE_TEMPLATE)


class _WorkspaceConfig(_ComponentResourceWithPreserveStrategy):
    from azureml._base_sdk_common.common import AZUREML_DIR, CONFIG_FILENAME
    WORKSPACE_CONFIG = os.path.join(AZUREML_DIR, CONFIG_FILENAME)
    WORKSPACE_CONFIG_TEMPLATE = DATA_PATH / CONFIG_FILENAME

    def __init__(self, folder: Path):
        super().__init__(folder, self.WORKSPACE_CONFIG, self.__class__.__name__, self.WORKSPACE_CONFIG_TEMPLATE)

    def create(self):
        try:
            from azureml.core import Workspace
            current_workspace = Workspace.from_config()
            current_workspace.write_config(str(self.folder))
            # TODO: add debug log here when we support set log level from cli
        except Exception:
            super().create()


class _BasicComponentEntryFromTemplate(_ComponentResourceWithExceptionStrategy):
    CODE_TEMPLATE = DATA_PATH / 'basic_component' / 'basic_component.template'

    def __init__(self, folder: Path, name):
        self.component_name = name
        self.sanitized_name = _sanitize_python_variable_name(name)
        path = '{}.py'.format(self.sanitized_name)
        super().__init__(folder, path, self.__class__.__name__, self.CODE_TEMPLATE)

    def create(self):
        if self.component_name != self.sanitized_name:
            logger.warning(
                'Your component name: {} was transformed to {} in order to use as a function name in python.'.format(
                    self.component_name, self.sanitized_name
                )
            )
        dsl_param_dict = {'display_name': self.component_name}
        dsl_param_dict_str = ',\n    '.join(
            ['%s=%s' % (key, to_literal_str(value)) for key, value in dsl_param_dict.items()])
        os.makedirs(self.path.parent, exist_ok=True)
        with open(self.template, encoding=FILE_ENCODING) as file:
            sample_code = file.read()
            sample_code = sample_code. \
                replace(DSL_PARAM_DICT_CONST, dsl_param_dict_str). \
                replace(COMPONENT_NAME_CONST, self.sanitized_name)

        with open(self.path, 'w', encoding=FILE_ENCODING) as out_file:
            out_file.write(sample_code)

    @classmethod
    def entry_from_type(cls, job_type, name):
        job_type = job_type.lower().strip()
        type_to_entry_class = {
            'basic': _BasicComponentEntryFromTemplate,
            'mpi': _MpiComponentEntryFromTemplate,
            'parallel': _ParallelComponentEntryFromTemplate,
        }
        if job_type not in type_to_entry_class:
            raise RuntimeError('Job type: %r not supported.' % job_type)
        return type_to_entry_class[job_type](Path(os.getcwd()), name)


class _MpiComponentEntryFromTemplate(_BasicComponentEntryFromTemplate):
    CODE_TEMPLATE = DATA_PATH / 'mpi_component' / 'mpi_component.template'


class _ParallelComponentEntryFromTemplate(_BasicComponentEntryFromTemplate):
    CODE_TEMPLATE = DATA_PATH / 'parallel_component' / 'parallel_component.template'


class _BasicComponentEntryFromFunction(_ComponentResourceWithExceptionStrategy):
    CODE_TEMPLATE = DATA_PATH / 'function_sample_code.template'

    def __init__(self, folder: Path, name, function):
        self.component_path, self.func_name = '.'.join(function.split('.')[:-1]), function.split('.')[-1]
        if name is None:
            name = self.func_name
        else:
            name = _sanitize_python_variable_name(name)

        if self.component_path == '':
            raise UserErrorException(
                "Invalid function: %s, please make sure the format is 'some_component.func_name'" % function)
        try:
            component = _import_component_with_working_dir(self.component_path, str(folder))
            self.func = getattr(component, self.func_name)
        except Exception as e:
            # Exceptions happen when importing user code should be user error.
            raise CustomerCodeError(
                "Import function '%s' failed at target folder '%s'\n" % (function, folder), inner_exception=e
            ) from e
        # gen component entry to function's folder
        entry_folder = Path(inspect.getfile(component)).parent
        path = '{}.py'.format(name)
        super().__init__(entry_folder, path, self.__class__.__name__, self.CODE_TEMPLATE, folder)

    def create(self):
        with open(self.template, encoding=FILE_ENCODING) as fin:
            code = fin.read()
            code = code.replace(COMPONENT_NAME_CONST, self.component_path). \
                replace('FUNC_NAME', self.func_name). \
                replace('FUNC_DEF', _get_func_def(self.func))
        with open(self.path, 'w', encoding=FILE_ENCODING) as fout:
            fout.write(code)
        io_hint = "Please use Input/Output" + \
                  " in function annotation to hint inputs/outputs."
        logger.info(('Generated entry file: %s.\n' + io_hint) % self.path)


class _PipelineProjectProperties(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.update({
            'NotebookFolder': 'notebooks',
            'TestsFolder': 'tests',
            'DataFolder': 'data'
        })

    @property
    def entry_folder(self):
        return self.get('EntryFolder', 'entries')

    @property
    def spec_folder(self):
        return self.get('SpecFolder', 'specs')

    @property
    def notebook_folder(self):
        return self.get('NotebookFolder', 'notebooks')

    @property
    def tests_folder(self):
        return self.get('TestsFolder', 'tests')

    @property
    def data_folder(self):
        return self.get('DataFolder', 'data')


class _VSCodeResource:
    def __init__(self, folder: Path, arguments: list):
        self.folder = folder
        self.launch = _VSCodeLaunch(folder, arguments)
        self.setting = _VSCodeSetting(folder)

    def init(self):
        logger.info('Initializing vscode settings...')
        os.makedirs(str(self.folder / _VSCodeFile.VSCODE_DIR), exist_ok=True)
        self.launch.update()
        self.setting.update()


class ComponentConfigBase:
    """Configurations for a component."""
    COMPONENT_ENTRY_FILE_CONST = 'entry'
    COMPONENT_SPEC_CONST = 'spec'
    SOURCE_DIR_CONST = 'sourceDirectory'

    def __init__(self, spec_path):
        self._spec_path = spec_path

    @property
    def spec_path(self):
        return self._spec_path

    @property
    def dict(self) -> dict:
        spec_path = str(_relative_to(self.spec_path, os.getcwd()).as_posix())
        result = {self.COMPONENT_SPEC_CONST: spec_path}
        return result

    @classmethod
    def load(cls, config) -> 'ComponentConfigBase':
        raise NotImplemented("Load not overridden.")

    def build(self):
        logger.info('\t\tBuilding: \t {}.'.format(_try_to_get_relative_path(self.spec_path)))
        # No need to build spec for ComponentConfigBase's build

    def register(self, workspace, version: str = None):
        """Build spec then register it

        :param workspace: The workspace object this component will belong to.
        :param version: If specified, registered component will use specified value as version instead of the version
        in the yaml.
        """
        self.build()
        logger.info('\t\tRegistering: \t {}.'.format(_try_to_get_relative_path(self.spec_path)))
        from azure.ml.component._core._component_definition import CommandComponentDefinition
        CommandComponentDefinition.register(
            workspace=workspace, spec_file=str(self.spec_path),
            package_zip=None, anonymous_registration=False,
            set_as_default=False,
            amlignore_file=None, version=version
        )

    @staticmethod
    def validate_absolute(config_key, path):
        if Path(path).is_absolute():
            raise UserErrorException(f'Value of key {config_key} should be a relative file. Got {path} instead.')

    @staticmethod
    def validate_extension(config_key, path, ext):
        if not path.endswith(ext):
            raise UserErrorException(f'Value of key {config_key} should ends with {ext}. Got {path} instead.')

    @staticmethod
    def validate_file_exist(config_key, path):
        if not (os.path.exists(path) and Path(path).is_file()):
            raise UserErrorException(f'Value of key {config_key} should be an existing file. Got {path} instead.')

    @staticmethod
    def validate_folder_exist(config_key, path):
        if not (os.path.exists(path) and Path(path).is_dir()):
            raise UserErrorException(
                f'Value of key {config_key} should be an existing folder. Got {path} instead.')

    @staticmethod
    def validate_outside_of_config(config_key, path):
        try:
            _relative_to(path, basedir='.', raises_if_impossible=True)
        except ValueError as e:
            raise UserErrorException(
                f'Value of key {config_key} should be inside of {PipelineProject.COMPONENT_PROJECT_FILE_NAME}. '
                f'Got {path} instead.') from e

    @staticmethod
    def validate_outside_of_source_dir(config_key, path, source_dir):
        try:
            _relative_to(path, basedir=source_dir, raises_if_impossible=True)
        except ValueError as e:
            raise UserErrorException(
                f'Value of key {config_key} should be inside of {source_dir}. '
                f'Got {path} instead.') from e


class YamlComponentConfig(ComponentConfigBase):
    """Configurations for a component defined by module spec."""

    def __init__(self, spec_path):
        """ Init a YamlComponentConfig

        :param spec_path: could be path or URL.
        """
        super().__init__(spec_path)

    def __eq__(self, other):
        # YamlComponentConfig is the same if spec_path is the same
        return isinstance(other, YamlComponentConfig) and str(self.spec_path) == str(other.spec_path)

    def __hash__(self):
        return hash(self.spec_path)

    @property
    def spec_path(self):
        return Path(self._spec_path).resolve().absolute()

    @classmethod
    def validate(cls, config: dict):
        """Verify yaml component config

        :param config: Config dict.
        :return: Component path, spec path, source dit in relative path format.
        """

        spec_path = config.get(cls.COMPONENT_SPEC_CONST, None)

        # validate spec
        if spec_path is None:
            raise UserErrorException(f'{cls.COMPONENT_SPEC_CONST} is required.')
        else:
            cls.validate_file_exist(cls.COMPONENT_SPEC_CONST, spec_path)
            cls.validate_absolute(cls.COMPONENT_SPEC_CONST, spec_path)
            # Only validate yaml here to align with old yaml
            cls.validate_extension(cls.COMPONENT_SPEC_CONST, spec_path, '.yaml')
            cls.validate_outside_of_config(cls.COMPONENT_SPEC_CONST, spec_path)

        valid_keys = {cls.COMPONENT_SPEC_CONST}
        for key, val in config.items():
            if key not in valid_keys:
                raise UserErrorException(f'Unsupported key {key}.')

        return spec_path

    @classmethod
    def load(cls, config: dict) -> 'YamlComponentConfig':
        """Load yaml component config from config.

        :param config: Config dict.
        :return: Loaded component config
        """
        spec_path = cls.validate(config)
        return YamlComponentConfig(spec_path)


class DSLComponentConfig(ComponentConfigBase):
    """Configurations for a component defined by dsl.component."""

    def __init__(self, component_entry, spec_path=None, source_dir=None):
        if source_dir is None:
            source_dir = '.'
        if spec_path is None:
            # default generate spec into component entry's folder
            spec_path = Path(component_entry).parent / (Path(component_entry).stem + SPEC_EXT)
        super().__init__(spec_path)
        self._component_entry = component_entry
        self._source_dir = source_dir
        self._dsl_component = None
        self._backup_folder = None

    def __eq__(self, other):
        # DSLComponentConfig is the same if component entry is the same
        return isinstance(other, DSLComponentConfig) and str(self.component_entry) == str(other.component_entry)

    def __hash__(self):
        return hash(self.component_entry)

    @property
    def source_dir(self):
        return Path(self._source_dir).resolve().absolute()

    @property
    def component_entry(self):
        return Path(self._component_entry).resolve().absolute()

    @property
    def spec_path(self):
        return Path(self._spec_path).resolve().absolute()

    @property
    def dsl_component(self) -> _ComponentObject:
        if self._dsl_component is not None:
            return self._dsl_component
        try:
            component_executor = DSLComponentConfig.collect_component_from_source(
                self.component_entry, self.source_dir)
        except Exception as e:
            # If we failed to collect component from component entry, it should be a user error
            raise CustomerCodeError(
                'Failed to load dsl component from {}'.format(self.component_entry), inner_exception=e)
        component = _ComponentObject(component_executor)
        logger.info('\t\tLoaded: \t {}.'.format(_try_to_get_relative_path(self.component_entry)))
        self._dsl_component = component
        return self._dsl_component

    @property
    def dict(self) -> dict:
        entry_path = str(_relative_to(self.component_entry, os.getcwd()).as_posix())
        spec_path = str(_relative_to(self.spec_path, os.getcwd()).as_posix())
        source_dir = str(_relative_to(self.source_dir, os.getcwd()).as_posix())
        result = {
            self.COMPONENT_ENTRY_FILE_CONST: entry_path,
            self.COMPONENT_SPEC_CONST: spec_path,
            self.SOURCE_DIR_CONST: source_dir
        }
        return result

    @property
    def backup_folder(self) -> Path:
        if self._backup_folder is None:
            # Our logic should not go here, remove this when test covers here?
            raise ValueError('Backup folder referenced before assignment.')
        return self._backup_folder

    @backup_folder.setter
    def backup_folder(self, backup_folder):
        self._backup_folder = backup_folder

    def build(self):
        # Build spec in source directory
        logger.info('\t\tBuilding: \t {}.'.format(_try_to_get_relative_path(self.spec_path)))
        spec_file = _SpecFile(self.dsl_component, Path(self.spec_path), self.backup_folder, Path(self.source_dir))
        spec_file.update()

    def init(self, entry_only=False):
        if entry_only:
            return

        self.build()

        # init resources
        job_type = self.dsl_component.component_executor.type
        # TODO: make this constant
        source_dir = Path(self.source_dir)
        test_folder = source_dir / 'tests'
        init_resources = [
            _NotebookFile(self.dsl_component, source_dir, job_type),
            _UnittestFile(self.dsl_component, test_folder, job_type),
            _GitIgnore(source_dir),
            _AMLIgnore(source_dir),
            _WorkspaceConfig(source_dir)
        ]
        for resource in init_resources:
            resource.update()

        # init data
        self.dsl_component.component_param_builder.build()

        # init vscode resources
        launch_config_name = self.dsl_component.component_param_builder.component_file_name

        argument = {'name': launch_config_name,
                    'args': self.dsl_component.component_param_builder.arguments,
                    'program': str(
                        _relative_to(self.dsl_component.component_entry_path, self.source_dir,
                                     raises_if_impossible=True))
                    }
        vscode_resource = _VSCodeResource(source_dir, [argument])
        vscode_resource.init()

    @classmethod
    def is_dsl_component_config(cls, config: dict):
        if not isinstance(config, dict):
            return False
        return cls.COMPONENT_ENTRY_FILE_CONST in config.keys()

    @classmethod
    def validate(cls, config: dict):
        """Verify component config

        :param config: Config dict.
        :return: Component path, spec path, source dit in relative path format.
        """

        component_entry = config.get(cls.COMPONENT_ENTRY_FILE_CONST, None)
        spec_path = config.get(cls.COMPONENT_SPEC_CONST, None)
        source_dir = config.get(cls.SOURCE_DIR_CONST, '.')

        # validate source dir
        cls.validate_absolute(cls.SOURCE_DIR_CONST, source_dir)
        cls.validate_folder_exist(cls.SOURCE_DIR_CONST, source_dir)
        cls.validate_outside_of_config(cls.SOURCE_DIR_CONST, source_dir)

        # validate entry
        if component_entry is None:
            raise UserErrorException(f'{cls.COMPONENT_ENTRY_FILE_CONST} is required.')
        else:
            cls.validate_file_exist(cls.COMPONENT_ENTRY_FILE_CONST, component_entry)
            cls.validate_absolute(cls.COMPONENT_ENTRY_FILE_CONST, component_entry)
            cls.validate_extension(cls.COMPONENT_ENTRY_FILE_CONST, component_entry, '.py')
            cls.validate_outside_of_config(cls.COMPONENT_ENTRY_FILE_CONST, component_entry)
            cls.validate_outside_of_source_dir(cls.COMPONENT_ENTRY_FILE_CONST, component_entry, source_dir)

        # validate spec
        if spec_path is not None:
            cls.validate_absolute(cls.COMPONENT_SPEC_CONST, spec_path)
            cls.validate_extension(cls.COMPONENT_SPEC_CONST, spec_path, '.spec.yaml')
            cls.validate_outside_of_config(cls.COMPONENT_SPEC_CONST, spec_path)

        valid_keys = {cls.COMPONENT_ENTRY_FILE_CONST, cls.COMPONENT_SPEC_CONST, cls.SOURCE_DIR_CONST}
        for key, val in config.items():
            if key not in valid_keys:
                raise UserErrorException(f'Unsupported key {key}.')

        return component_entry, spec_path, source_dir

    @classmethod
    def load(cls, config: dict) -> 'DSLComponentConfig':
        """Load component config from config.

        Note: This method only load/validates config, actual component executor won't load until it's used.

        :param config: Config dict.
        :return: Loaded component config
        """
        component_entry, spec_path, source_dir = cls.validate(config)
        return DSLComponentConfig(component_entry, spec_path, source_dir)

    @classmethod
    def load_from_file(cls, file_path) -> Union[None, 'DSLComponentConfig']:
        """Load component config from file, returns None if none dsl component found in the file.

        Note: This method loads actual component executor since we need to make sure dsl component exists in file.

        :param file_path: File path
        :return: Loaded component config or None.
        """
        component_executor = DSLComponentConfig.collect_component_from_source(file_path)
        # TODO: maybe we need to raise exception when no dsl component is found
        if component_executor is None:
            return None
        component = _ComponentObject(component_executor)
        component_config = DSLComponentConfig(file_path)
        component_config._dsl_component = component
        return component_config

    @staticmethod
    def collect_component_from_source(source, source_dir=None) -> Union[None, ComponentExecutor]:
        """Collect dsl component from component entry.

        :param source: Component entry or component
        :param source_dir: Source directory
        :return: ComponentExecutor if collect succeed,
        none if collect failed but exception was translated into warning.
        :raises: Exception if importing dsl.component failed.
        """
        source = str(source)
        if source_dir is None:
            source_dir = os.getcwd()
        # Only treat source as file if it's a python file. Otherwise,
        # treat it as a component and let importlib help.
        if is_py_file(source):
            component = ComponentExecutor.collect_component_from_file(source, source_dir)
        else:
            component = ComponentExecutor.collect_component_from_py_module(source, source_dir)
        if component is None:
            raise RuntimeError('Failed to load dsl.component from {}'.format(source))
        return component


class _ComponentFailureInfo:
    """Info of a component failed to load."""

    def __init__(self, source, exception):
        """

        :param source: Source component load from
        :param exception: Exception when load the component
        """
        self.source = source
        self.exception = exception


class ComponentActions(Enum):
    """Actions a component project can take."""
    Load = 'load'
    Build = 'build'
    Register = 'register'


class PipelineProject:
    """A helper class which builds a pipeline project skeleton."""

    class InitMode(Enum):
        Template = 'template'
        Function = 'function'
        DSL_Component = 'dsl_component'
        Argparse = 'argparse'
        Notebook = 'notebook'

    # TODO: align with file name and class name
    COMPONENT_PROJECT_FILE_NAME = '.componentproj'
    COMPONENTS_KEY = 'components'

    def __init__(self, components: List[ComponentConfigBase], properties=None):
        """Build a pipeline project skeleton."""
        self.components = components
        if properties is None:
            properties = _PipelineProjectProperties()
        self.properties = properties

    @property
    def dict(self):
        """Transform a pipeline project to dictionary."""
        return {
            self.COMPONENTS_KEY: [component.dict for component in self.components],
        }

    def dump(self):
        """Dump a pipeline project into file."""
        if len(self.components) == 0:
            return
        else:
            logger.info('Dumping configurations into {}'.format(Path(self.COMPONENT_PROJECT_FILE_NAME).absolute()))
            if Path(self.COMPONENT_PROJECT_FILE_NAME).exists():
                existing_project, _ = PipelineProject.execute_from_config(Path('.'), None)
                PipelineProject.merge(self, existing_project)
            yaml = YAML(typ='unsafe', with_additional_representer=True)
            with open(self.COMPONENT_PROJECT_FILE_NAME, 'w', encoding=FILE_ENCODING) as file:
                yaml.dump(self.dict, file)

    @staticmethod
    def version_hint():
        """Show the version info of current ComponentProject and python environment."""
        return "Component project builder version: %s Python executable: %s" % (VERSION, sys.executable)

    @staticmethod
    @track(activity_name="DSLComponent_init", activity_type=_PUBLIC_API)
    @timer_decorator
    def init(source=None, name=None, job_type='basic', source_dir=None, inputs=None, outputs=None, entry_only=False):
        """Init a Pipeline project skeleton which contains component file, component spec and jupyter notebook.

        :param source: Source for specific mode, could be pacakge.function or path/to/python_file.py
        :param name: The name of component. eg: Select Columns.
        :param job_type: Job type of the component. Could be basic, mpi, hdinsight, parallel.
            Defaults to basic if not specified, which refers to run job on a single compute node.
        :param source_dir: Source directory.
        :param inputs: Inputs for argparse mode.
        :param outputs: Outputs for argparse mode.
        :param entry_only: If set to true, only component entry will be generated.
        :return: Created component project.
        :rtype: PipelineProject
        """
        logger.info(PipelineProject.version_hint())
        if source_dir is None:
            source_dir = os.getcwd()
        if source is None:
            # When initiating from template, source dir is separate folder.
            if name is not None:
                try:
                    sanitized_name = _sanitize_python_variable_name_with_value_check(name)
                except ValueError as e:
                    raise UserErrorException(
                        'Component name: {} could not be normalized into python variable name.'.format(name)) from e
                source_dir = Path(source_dir) / sanitized_name
            else:
                raise UserErrorException('Name and source can not be empty at the same time.')
        with _change_working_dir(source_dir), BackUpFiles(os.getcwd()) as backup_folder:
            _log_without_dash('========== Init started: {} =========='.format(os.getcwd()))

            mode, resource = PipelineProject.collect_or_gen_dsl_component(
                source, name, job_type,
                inputs=inputs, outputs=outputs)
            resource.backup_folder = backup_folder

            # log trace
            telemetry_values = WorkspaceTelemetryMixin._get_telemetry_value_from_workspace(_try_to_get_workspace())
            telemetry_values.update({'mode': mode.value, 'job_type': job_type})
            _LoggerFactory.trace(_get_telemetry_logger(), "DSLComponent_init", telemetry_values)

            logger.info('Initializing {}...'.format(resource.component_entry))
            resource.init(entry_only=entry_only)

            _log_without_dash('========== Init succeeded ==========')
            pipeline_project = PipelineProject([resource])
            pipeline_project.dump()
            return pipeline_project

    @staticmethod
    @track(activity_name="DSLComponent_build", activity_type=_PUBLIC_API)
    @timer_decorator
    def build(target=None, source_dir=None):
        """Build module spec for dsl.component.

        :param target: could be a dsl.component entry file or folder, will be os.getcwd() if not set.
        :param source_dir: Source directory.
        """
        logger.info(PipelineProject.version_hint())
        if target is None:
            target = os.getcwd()
        if not os.path.exists(target):
            raise UserErrorException('Target {} does not exist.'.format(target))

        _log_without_dash('========== Build started: {} =========='.format(os.getcwd()))
        target = Path(target)
        with BackUpFiles(target) as backup_folder:
            if PipelineProject.is_project(target):
                if source_dir is not None:
                    raise UserErrorException('Specify source directory for config target is not supported.')
                logger.info('Building dsl.components from config...')
                pipeline_project, failed_components = PipelineProject.execute_from_config(target, backup_folder,
                                                                                          ComponentActions.Build)
            elif target.is_file() and is_py_file(str(target)):
                logger.info('Building dsl.components from file...')
                pipeline_project, failed_components = PipelineProject.execute_from_py_file(target, source_dir,
                                                                                           backup_folder,
                                                                                           ComponentActions.Build)
            elif target.is_dir():
                if source_dir is not None:
                    raise UserErrorException('Specify source directory for folder target is not supported.')
                logger.info('Building dsl.components from folder...')
                pipeline_project, failed_components = PipelineProject.execute_from_folder(target, backup_folder,
                                                                                          ComponentActions.Build)
            else:
                raise UserErrorException('Target %s not valid.' % str(target))

        # log
        # TODO: scrub exception
        telemetry_values = WorkspaceTelemetryMixin._get_telemetry_value_from_workspace(_try_to_get_workspace())
        for component in pipeline_project.components:
            if isinstance(component, DSLComponentConfig):
                job_type = component.dsl_component.component_executor.type
            else:
                job_type = 'UNKNOWN'
            telemetry_values.update({
                'job_type': job_type,
                'load_exception': None
            })
            _LoggerFactory.trace(_get_telemetry_logger(), "DSLComponent_build", telemetry_values)
        for component in failed_components:
            telemetry_values.update({
                'job_type': None,
                # should not put exception object directly into telemetry, here we dump it as @track did
                'load_exception': json.dumps(_get_exception_detail(component.exception))
            })
            _LoggerFactory.trace(_get_telemetry_logger(), "DSLComponent_build", telemetry_values)

        _log_without_dash(
            '========== Build: {} succeeded, {} failed =========='.format(len(pipeline_project.components),
                                                                          len(failed_components)))

        exceptions = [component.exception for component in failed_components]
        # raise if build failed
        if exceptions:
            if len(exceptions) == 1:
                # if only one build failed, raised
                raise exceptions[0]
            else:
                raise AggregatedComponentError(exceptions)
        return pipeline_project

    @staticmethod
    @track(activity_name="DSLComponent_register", activity_type=_PUBLIC_API)
    @timer_decorator
    def register(target: str, workspace_name: str, resource_group: str, subscription_id: str, version: str = None):
        # TODO: register in sync
        logger.info(PipelineProject.version_hint())
        workspace = Workspace(subscription_id, resource_group, workspace_name)
        target = Path(target)
        with BackUpFiles(target) as backup_folder:
            register_params = {'workspace': workspace, 'version': version}
            _log_without_dash('========== Register started: {} =========='.format(os.getcwd()))
            if PipelineProject.is_project(target):
                logger.info('Registering dsl.components from config...')
                pipeline_project, failed_components = PipelineProject.execute_from_config(target, backup_folder,
                                                                                          ComponentActions.Register,
                                                                                          register_params)
            elif target.is_file() and is_py_file(str(target)):
                logger.info('Registering dsl.components from file...')
                # TODO: support source dir
                pipeline_project, failed_components = PipelineProject.execute_from_py_file(target, None,
                                                                                           backup_folder,
                                                                                           ComponentActions.Register,
                                                                                           register_params)
            elif target.is_dir():
                logger.info('Registering dsl.components from folder...')
                pipeline_project, failed_components = PipelineProject.execute_from_folder(target, backup_folder,
                                                                                          ComponentActions.Register,
                                                                                          register_params)
            else:
                raise UserErrorException('Target %s not valid.' % str(target))
        # TODO: add log trace
        _log_without_dash(
            '========== Register: {} succeeded, {} failed =========='.format(len(pipeline_project.components),
                                                                             len(failed_components)))
        return pipeline_project

    @staticmethod
    def collect_or_gen_dsl_component(
            source, name, job_type,
            inputs=None, outputs=None
    ) -> (InitMode, DSLComponentConfig):
        """Collect or generate DSLComponentConfig, raises exception if multi dsl.components are collected.

        :param source: Source for specific mode, could be package.function or path/to/python_file.py
        :param name: Name for component.
        :param job_type: Job type of the component.
        :param inputs: Inputs for argparse.
        :param outputs: Outputs for argparse.
        :return: Init mode and initialized dsl.component.
        """
        # collect
        if source is not None and _has_dsl_component_str(source):
            mode = PipelineProject.InitMode.DSL_Component
            # Skip import if no dsl component str in component to prevent potential import errors.
            logger.info('Attempting to load dsl.components from source...')
            try:
                component = DSLComponentConfig.collect_component_from_source(source)
                if component is not None:
                    component_object = _ComponentObject(component)
                    component = DSLComponentConfig(source)
                    component._dsl_component = component_object
                    return mode, component
            except TooManyDSLComponentsError as e:
                # Only TooManyDSLComponentsError will be raised
                # If other exception happens, that means we failed to load dsl component
                raise e
            except BaseException:
                pass
        # generate
        if source is None:
            mode = PipelineProject.InitMode.Template
            logger.info('Attempting to generate dsl.component from template...')
            file = PipelineProject.gen_dsl_component_from_name(name, job_type)
        elif _is_function(source):
            mode = PipelineProject.InitMode.Function
            logger.info('Attempting to generate dsl.component from function...')
            if job_type != 'basic':
                raise UserErrorException('Unsupported job-type {} when init from {}'.format(job_type, source))
            file = PipelineProject.gen_dsl_component_from_func(name, source)
        elif _is_notebook(source):
            mode = PipelineProject.InitMode.Notebook
            logger.info('Attempting to generate dsl.component from notebook...')
            file = PipelineProject.gen_dsl_component_from_notebook(
                name,
                job_type,
                source)
        else:
            mode = PipelineProject.InitMode.Argparse
            logger.info('Attempting to generate dsl.component from arg parser...')
            if not _source_exists(source):
                raise UserErrorException('Source: {} does not exist as file.'.format(source))
            file = PipelineProject.gen_dsl_component_from_argparse(name, job_type, source,
                                                                   inputs=inputs, outputs=outputs)

        component_error = RuntimeError('Failed to resolve generated dsl.component file: {}'.format(file))
        try:
            component_resource = DSLComponentConfig.load_from_file(str(file))
        except Exception as e:
            # Should be SDK error if we failed to load a generated dsl.component
            raise component_error from e
        if component_resource is None:
            raise component_error
        return mode, component_resource

    @staticmethod
    def gen_dsl_component_from_name(name, job_type):
        """Generate a start up dsl.component file."""
        code_template = _BasicComponentEntryFromTemplate.entry_from_type(job_type=job_type, name=name)
        code_template.update()
        return code_template.path

    @staticmethod
    def gen_dsl_component_from_func(name, function):
        """Generate a dsl.component file from function."""
        code_template = _BasicComponentEntryFromFunction(Path(os.getcwd()), name, function)
        code_template.update()
        return code_template.path

    @staticmethod
    def gen_dsl_component_from_notebook(name, job_type, source):
        """Generate a dsl.component file from notebook."""
        # Import _component_from_notebook here because azure-ml-component doesn't have papermill dependency
        # The papermill dependency is in azure-ml-component[notebook].
        from azure.ml.component.dsl._component_from_notebook import gen_component_by_notebook
        component_path, component_name = _get_component_path_and_name_from_source(source, NOTEBOOK_EXT)
        entry_path = str(Path(component_path) / '{}_entry.py'.format(component_name))
        gen_component_by_notebook(
            entry=source, target_file=entry_path
        )
        return entry_path

    @staticmethod
    def gen_dsl_component_from_argparse(name, job_type, source, inputs=None, outputs=None):
        """Generate a dsl.component from arg parse."""
        component_path, component_name = _get_component_path_and_name_from_source(source)
        entry_path = str(Path(component_path) / '{}_entry.py'.format(component_name))
        gen_component_by_argparse(
            entry=source, target_file=entry_path, inputs=inputs, outputs=outputs,
            # Here we hard-coded set job_type=None if it is 'basic'
            # because 'basic' is the default value even we don't set --type.
            # TODO: Refine the logic to distinguish the case that --type not set and --type basic.
            component_meta={'name': name, 'job_type': None if job_type == 'basic' else job_type},
        )
        return entry_path

    @classmethod
    def is_project(cls, target: Path) -> bool:
        """If target is a component project."""
        # pathlib.Path.exists throws exception when special char in path, use os.path.exists instead
        if target is None or not os.path.exists(target):
            return False
        if target.is_file() and target.name == PipelineProject.COMPONENT_PROJECT_FILE_NAME:
            # If a .pipelineproj file is passed, target is it's parent.
            target = target.parent
        if target.is_dir() and (target / PipelineProject.COMPONENT_PROJECT_FILE_NAME).exists():
            return True
        return False

    @classmethod
    def load_config_2_dict(cls) -> dict:
        with open(cls.COMPONENT_PROJECT_FILE_NAME, encoding=FILE_ENCODING) as file:
            try:
                data = YAML.safe_load(file)
                # Avoid None is loaded from file
                if not isinstance(data, dict):
                    raise RuntimeError(
                        f'Data {data} in {cls.COMPONENT_PROJECT_FILE_NAME} could not be loaded as a dict.')
                return data
            except Exception as e:
                raise UserErrorException(f'Failed to load {cls.COMPONENT_PROJECT_FILE_NAME}.') from e

    @classmethod
    def get_component_config_instance(cls, component_config, backup_folder):
        """Load component config to different instance."""
        if DSLComponentConfig.is_dsl_component_config(component_config):
            component_resource = DSLComponentConfig.load(component_config)
            component_resource.backup_folder = backup_folder
        else:
            component_resource = YamlComponentConfig.load(component_config)
        return component_resource

    @classmethod
    def execute_from_config(cls, config_path: Path, backup_folder,
                            action=ComponentActions.Load, kw_params: dict = None):
        """Load component project from project file then execute action.

        :param config_path: path of config file
        :param backup_folder: Backup folder
        :param action: action to execute, eg: build/register
        :param kw_params: parameters for action.
        :return: Returns a PipelineProject and list of component names failed to load.
        :rtype: (PipelineProject, List[_ComponentFailureInfo])
        """
        if kw_params is None:
            kw_params = {}
        failed_components = []
        handled_component_config = set()
        succeed_components = []
        if config_path.is_file():
            config_path = config_path.parent
        with _change_working_dir(config_path):
            data = cls.load_config_2_dict()
            components = data.get(cls.COMPONENTS_KEY, [])

            for component_config in components:
                # load from component_config
                try:
                    component_resource = cls.get_component_config_instance(component_config, backup_folder)

                    if component_resource in handled_component_config:
                        logger.warning('Skipped duplicated component config: {}'.format(component_resource))
                        continue

                    handled_component_config.add(component_resource)

                    # no action need to take when action is load since we already loaded the component
                    if action != ComponentActions.Load:
                        function = getattr(component_resource, action.value)
                        function(**kw_params)

                    succeed_components.append(component_resource)
                except BaseException as e:
                    error_msg = 'Failed to {} component from config: {}'.format(action.value, component_config,)
                    logger.warning('\t\t{} due to error: {}'.format(error_msg, e))

                    # We are loading dsl.component from user's code, should be user error if failed.
                    failed_components.append(
                        _ComponentFailureInfo(component_config, CustomerCodeError(error_msg, inner_exception=e)))

            pipeline_project = PipelineProject(succeed_components)
            return pipeline_project, failed_components

    @classmethod
    def execute_from_py_file_list(cls, py_files: List, backup_folder, action=ComponentActions.Load,
                                  kw_params: dict = None):
        """Load component project from list of py files then execute action.

        :param py_files: list of python files
        :param backup_folder: Backup folder
        :param action: action to execute, eg: build/register
        :param kw_params: parameters for action.
        :return: Returns a PipelineProject and list of component names failed to load.
        :rtype: (PipelineProject, List[_ComponentFailureInfo])
        """
        if kw_params is None:
            kw_params = {}
        failed_components = []
        components = []
        for file in py_files:
            try:
                component_resource = DSLComponentConfig.load_from_file(file)
                # TODO: maybe we need to raise exception when no dsl component is found
                if component_resource is not None:

                    component_resource.backup_folder = backup_folder
                    # no action need to take when action is load since we already loaded the component
                    if action != ComponentActions.Load:
                        function = getattr(component_resource, action.value)
                        function(**kw_params)

                    components.append(component_resource)

            except BaseException as e:
                error_msg = 'Failed to {} {}.'.format(action.value, file)
                logger.warning('\t\t{} due to error: {}.'.format(error_msg, e))
                # We are loading dsl.component from user's code, should be user error if failed.
                failed_components.append(
                    _ComponentFailureInfo(file, CustomerCodeError(error_msg, inner_exception=e)))
        pipeline_project = PipelineProject(components)
        return pipeline_project, failed_components

    @classmethod
    def execute_from_py_file(cls, py_file, source_dir, backup_folder, action=ComponentActions.Load,
                             kw_params: dict = None):
        """Load component project from file then execute action.

        :return: Returns a PipelineProject and list of component names failed to load.
        :rtype: (PipelineProject, List[_ComponentFailureInfo])
        """
        # TODO: this case need to fail if no dsl component is built
        # Check if target is valid file/dir when loading it.
        if source_dir is None:
            # when absolute path is passed, default value for source dir is it's parent
            if py_file.is_absolute():
                source_dir = py_file.parent
            else:
                source_dir = os.getcwd()
        if not os.path.exists(source_dir):
            raise UserErrorException('Source directory {} does not exist.'.format(source_dir))
        elif not Path(source_dir).is_dir():
            raise UserErrorException('Source directory {} should be a folder'.format(source_dir))

        try:
            py_file = _relative_to(py_file, source_dir, raises_if_impossible=True)
        except ValueError as e:
            raise UserErrorException(
                'Target should be inside source directory. Got {} and {} instead.'.format(py_file, source_dir)) from e

        with _change_working_dir(source_dir):
            py_files = [py_file]
            return cls.execute_from_py_file_list(py_files, backup_folder, action, kw_params)

    @classmethod
    def execute_from_folder(cls, folder, backup_folder, action=ComponentActions.Load, kw_params: dict = None):
        """Load component project from folder then execute action.

        :return: Returns a PipelineProject and list of component names failed to load.
        :rtype: (PipelineProject, List[_ComponentFailureInfo])
        """
        py_files = _find_py_files_in_target(folder)
        return cls.execute_from_py_file_list(py_files, backup_folder, action, kw_params)

    @staticmethod
    def merge(first: 'PipelineProject', second: 'PipelineProject'):
        """Merge 2 component project, update first according to second."""
        first.components = list(set(first.components + second.components))


def _entry(argv):
    """CLI tool for component creating."""
    parser = argparse.ArgumentParser(
        prog="python -m azure.ml.component.dsl.pipeline_project",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""A CLI tool for component project creating"""
    )

    subparsers = parser.add_subparsers()

    # create component folder parser
    create_parser = subparsers.add_parser(
        'init',
        description='Add a dsl.component and resources into a pipeline project.'
                    'Specify name and type param to add a start up dsl.component and resources.'
                    'Specify function to build dsl.component and resources according to the function.'
                    'Specify file or component to build resources for existing dsl.component file.'
    )
    create_parser.add_argument(
        "--source",
        type=str,
        help="Source for specific mode, could be pacakge.function or path/to/python_file.py "
             "or path/to/jupyter_notebook.ipynb."
    )
    create_parser.add_argument(
        '--name', type=str,
        help="Name of the component."
    )
    create_parser.add_argument(
        '--type', type=str, default='basic', choices=['basic', 'mpi', 'parallel'],
        help="Job type of the component. Could be basic and mpi. "
             "Defaults to basic if not specified, which refers to run job on a single compute node."
    )
    create_parser.add_argument(
        '--source_dir', type=str,
        help="Source directory to init environment, all resources will be generated there, "
             "will be os.cwd() if not set."
    )
    create_parser.add_argument(
        '--inputs', type=str, default=[], nargs='+',
        help="Input ports of the component from argparse.",
    )
    create_parser.add_argument(
        '--outputs', type=str, default=[], nargs='+',
        help="Output ports of the component from argparse.",
    )
    create_parser.add_argument(
        "--entry_only", type=_str_to_bool,
        help="If specified, only component entry will be generated."
    )
    create_parser.set_defaults(func=PipelineProject.init)

    # build dsl.component into specs parser
    build_parser = subparsers.add_parser(
        'build',
        description='A CLI tool to build dsl.component into module specs in folder.'
    )
    build_parser.add_argument(
        '--target', type=str,
        help="Target component project or component file. Will use current working directory if not specified."
    )
    build_parser.add_argument(
        '--source_dir', type=str,
        help="Source directory to build spec, will be os.cwd() if not set."
    )
    build_parser.set_defaults(func=PipelineProject.build)

    # This command is used for the case that one has a valid python entry with argparse,
    # but doesn't want to rely on dsl.component to register as a component.
    # Internal users may use this feature to build built-in components.
    build_argparse_parser = subparsers.add_parser(
        'build-argparse',
        description="A CLI tool to build an entry with argparse into a module spec file."
    )
    build_argparse_parser.add_argument(
        '--target', type=str,
        help="Target entry file 'xx/yy.py' or target entry component 'xx.yy', file must be relative path.",
    )
    build_argparse_parser.add_argument(
        '--spec-file', type=str, default='spec.yaml',
        help="Module spec file name, the default name is 'spec.yaml', must be relative path",
    )
    build_argparse_parser.add_argument(
        '--source-dir', type=str, default='.',
        help="Source directory of the target file and spec file, the default path is '.'.",
    )
    build_argparse_parser.add_argument(
        '--inputs', type=str, default=[], nargs='+',
        help="Input ports of the component.",
    )
    build_argparse_parser.add_argument(
        '--outputs', type=str, default=[], nargs='+',
        help="Output ports of the component.",
    )
    build_argparse_parser.add_argument(
        '--force', action='store_true',
        help="Force generate spec file if exists, otherwise raises.",
    )
    build_argparse_parser.set_defaults(func=gen_component_by_argparse)

    # register components inside component project parser
    register_parser = subparsers.add_parser(
        'register',
        description='A CLI tool to register components inside component project.'
    )
    register_parser.add_argument(
        '--target', type=str,
        help="Target component project. Will use current working directory if not specified."
    )
    register_parser.add_argument(
        '--subscription_id', '-s', type=str,
        help="Subscription id."
    )
    register_parser.add_argument(
        '--resource_group', '-r', type=str,
        help="Resource group."
    )
    register_parser.add_argument(
        '--workspace_name', '-w', type=str,
        help="Workspace name."
    )
    register_parser.add_argument(
        "--version", type=str,
        help="If specified, registered component's version will be overwritten to specified value "
             "instead of the version in the yaml."
    )
    register_parser.set_defaults(func=PipelineProject.register)

    args, rest_args = parser.parse_known_args(argv)
    if args.func == PipelineProject.init:
        PipelineProject.init(
            source=args.source, name=args.name, job_type=args.type,
            source_dir=args.source_dir,
            inputs=args.inputs, outputs=args.outputs,
            entry_only=args.entry_only
        )
    elif args.func == PipelineProject.build:
        PipelineProject.build(target=args.target, source_dir=args.source_dir)
    elif args.func == gen_component_by_argparse:
        gen_component_by_argparse(
            entry=args.target, spec_file=args.spec_file, working_dir=args.source_dir,
            force=args.force, inputs=args.inputs, outputs=args.outputs,
        )
    elif args.func == PipelineProject.register:
        PipelineProject.register(target=args.target, workspace_name=args.workspace_name,
                                 resource_group=args.resource_group, subscription_id=args.subscription_id,
                                 version=args.version)


def main():
    """Use as a CLI entry function to use ComponentProject."""
    _entry(sys.argv[1:])


if __name__ == '__main__':
    main()
