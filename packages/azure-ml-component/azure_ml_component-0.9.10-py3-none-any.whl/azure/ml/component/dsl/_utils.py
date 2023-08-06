# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import importlib
import inspect
import os
import shutil
import subprocess
import logging
import re
import sys
import contextlib
import tempfile
from ast import parse
from datetime import datetime
from functools import wraps
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

from azureml.exceptions import UserErrorException
from azureml.core.workspace import Workspace
from .._util._exceptions import _assert_frame_package_name
from .._util._utils import _relative_to

formatter = logging.Formatter('%(levelname)-8s - %(message)s')


class LogHandler(logging.StreamHandler):
    def __init__(self, stream=sys.stdout):
        super().__init__(stream)
        self.setFormatter(formatter)


logger = logging.getLogger(__name__)
logger.propagate = False
logger.setLevel(logging.INFO)
handler = LogHandler()
logger.addHandler(handler)

BACKUP_FOLDER = None
NOTEBOOK_EXT = '.ipynb'
WORKSPACE_ERROR_MSG = """
Get default workspace failed, please create config.json in current working directory and specify workspace info in it.
The format of config.json likes below:
{
    "subscription_id": <Your subscription id>,
    "resource_group": <Your resource group name>,
    "workspace_name": <Your workspace name>,
}
"""


def _print_step_info(info):
    if type(info) is not list:
        info = [info]
    step_info = [
        '-' * 80,
        *info,
        '-' * 80
    ]
    for _step_info in step_info:
        logger.info(_step_info)


def _log_file_create(file_name):
    logger.info('\t\tCreated \t %s' % file_name)


def _log_file_update(file_name):
    logger.info('\t\tUpdated \t %s' % file_name)


def _log_file_skip(file_name):
    logger.warning('\t\tSkipped: \t %s' % file_name)


def _log_with_new_format(message, new_formatter):
    handler.setFormatter(new_formatter)
    logger.info(message)
    handler.setFormatter(formatter)


def _log_without_dash(message):
    _log_with_new_format(message, logging.Formatter('%(levelname)-8s %(message)s'))


class FileExistProcessor:
    def __init__(self, working_dir: Path, force: bool, backup_folder: Path):
        self.working_dir = working_dir
        self.force = force
        self.backup_folder = backup_folder

    def process_or_skip(self, relative_path: str, func, *args, **kwargs):
        """Check the existence of target to decide whether call func(*args, **kwargs)"""
        target = (self.working_dir / relative_path)
        target_exist = target.exists()
        if target_exist:
            if self.force:
                os.makedirs((self.backup_folder / relative_path).parent, exist_ok=True)
                shutil.copy(target, self.backup_folder / relative_path)
            else:
                _log_file_skip(target)
                return
        result = func(*args, **kwargs)
        if kwargs.get('code_file', None) is not None:
            target = '{} -> {}'.format(kwargs['code_file'], target)
        if target_exist:
            _log_file_update(target)
        else:
            _log_file_create(target)
        return result


def timer_decorator(f):
    """Decorates a function and calculate it's running time.

    :param f: decorated function
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        result = f(*args, **kwargs)
        logger.info("Time Elapsed {}".format(datetime.now() - start_time))
        return result

    return wrapper


class BackUpFiles(object):
    def __init__(self, target):
        time_stamp = datetime.now().strftime("%d-%b-%Y-%H-%M")
        if target is None:
            target = Path(os.getcwd())
        target = Path(target)
        self.target_folder = target if target.is_dir() else target.parent
        self.backup_folder = self.target_folder / time_stamp
        self.backup_folder.mkdir(exist_ok=True)
        self.default_backup_folder_name = '.backup'

    def __enter__(self):
        return self.backup_folder

    def __exit__(self, exc_type, exc_val, exc_tb):
        # If Backup folder is not empty, replace it to default backup folder
        if os.listdir(self.backup_folder):
            default_backup_folder = self.target_folder / self.default_backup_folder_name
            if default_backup_folder.exists():
                shutil.rmtree(default_backup_folder)
            self.backup_folder.rename(default_backup_folder)
            logger.info('Original files are backed up to folder: %s' % default_backup_folder.as_posix())

        if self.backup_folder.exists():
            shutil.rmtree(self.backup_folder)


@contextlib.contextmanager
def _temporarily_remove_file(fname):
    """Remove the target file temporarily and recover it after the end of the context."""
    if Path(fname).is_dir():
        raise ValueError("Input path %s cannot be a folder." % fname)
    data = None  # Use data to store the existing file.
    # If a file exists, we load the data and remove it.
    if Path(fname).is_file():
        with open(fname, 'rb') as fin:
            data = fin.read()
        Path(fname).unlink()
    try:
        yield
    finally:
        # If there was a file before, recover it.
        if data is not None:
            with open(fname, 'wb') as fout:
                fout.write(data)
        # Otherwise if some new file is created, we remove it to recover the folder.
        else:
            if Path(fname).exists():
                Path(fname).unlink()


@contextlib.contextmanager
def _change_working_dir(path, mkdir=True):
    """Context manager for changing the current working directory"""

    saved_path = os.getcwd()
    if mkdir:
        os.makedirs(path, exist_ok=True)
    os.chdir(str(path))
    try:
        yield
    finally:
        os.chdir(saved_path)


def _run_command(command):
    output = subprocess.check_output(command, shell=True)
    # remove ANSI characters
    output = re.sub(b'\x1b\\[[0-9;]*m', b'', output).decode()
    return output


def _sanitize_python_class_name(snake_name: str):
    """Change variable name from snake to camel case."""
    components = snake_name.split('_')
    return ''.join(component.title() for component in components)


def to_literal_str(value):
    if isinstance(value, str):
        return '"%s"' % value
    return value


def _find_py_files_in_target(target: Path, depth=1):
    result = []
    if depth < 0:
        return result
    if target.is_file():
        if target.suffix == '.py':
            result.append(str(target))
    elif target.is_dir():
        for file in target.iterdir():
            result += _find_py_files_in_target(file, depth - 1)
    return result


def _split_path_into_list(path):
    path = path.strip('\\/')
    result = []
    while path != '':
        path, tail = os.path.split(path)
        result.insert(0, tail)
    return result


def _is_function(source):
    """Check if source is function."""
    logger.info('Determining if source {} is function...'.format(source))
    # always treat xxx.py as file
    if not isinstance(source, str):
        return False
    if re.match(r'[A-Za-z0-9_]+.py', source):
        return False
    if re.match(r'^[A-Za-z0-9_]+(\.[A-Za-z0-9_]+)+$', source):
        # use loose match on variable and let importlib to do rest work
        try:
            module, func = source.rsplit('.', 1)
            with _import_module_with_reloading(os.getcwd(), module):
                module = importlib.import_module(module)
                func = getattr(module, func)
                return callable(func)
        except BaseException:
            logger.info('Failed to load source {} as function.'.format(source))
            return False
    return False


def is_notebook_file(entry: str):
    """Check whether the file is a notebook file."""
    return entry.endswith(NOTEBOOK_EXT)


def _is_notebook(source):
    """Check if source is notebook."""
    logger.info('Determining if source {} is notebook...'.format(source))
    if not isinstance(source, str):
        return False
    return is_notebook_file(source)


def _get_func_def(func):
    """Get definition of function."""
    src = inspect.getsource(func)
    module_node = parse(src)
    func_node = module_node.body[0]
    body_node = func_node.body[0]
    result = '\n'.join(src.split('\n')[:body_node.lineno - func_node.lineno])
    return result


@contextlib.contextmanager
def inject_sys_path(path):
    original_sys_path = sys.path.copy()
    sys.path.insert(0, str(path))
    try:
        yield
    finally:
        sys.path = original_sys_path


@contextlib.contextmanager
def _import_module_with_reloading(path, module_name):
    module_name = str(module_name)
    with inject_sys_path(path):
        # Note: if module_name doesn't exist, it won't be unload.
        # reload module in case module with same name already loaded.
        if module_name in sys.modules.keys():
            importlib.reload(sys.modules[module_name])
        yield


def _force_reload_module(module):
    # Reload the module except the case that module.__spec__ is None.
    # In the case module.__spec__ is None (E.g. module is __main__), reload will raise exception.
    if module.__spec__ is None:
        return module
    path = Path(module.__spec__.loader.path).parent
    with inject_sys_path(path):
        return importlib.reload(module)


def _import_component_with_working_dir(module_name, working_dir=None, force_reload=False):
    if working_dir is None:
        working_dir = os.getcwd()
    working_dir = str(Path(working_dir).resolve().absolute())

    with _change_working_dir(working_dir, mkdir=False), inject_sys_path(working_dir):
        try:
            py_module = importlib.import_module(module_name)
        except Exception as e:
            files = [f for _, _, files in os.walk(working_dir) for f in files]
            logger.warning('Import Module {} with working dir failed, '
                           'current directory {}, files {}, sys path {}'.
                           format(module_name, os.getcwd(), files, sys.path))
            raise e
        except BaseException as e:
            # raise base exception like system.exit as normal exception
            files = [f for _, _, files in os.walk(working_dir) for f in files]
            logger.warning('Import Module {} with working dir failed, '
                           'current directory {}, files {}, sys path {}'.
                           format(module_name, os.getcwd(), files, sys.path))
            raise Exception(str(e)) from e
        loaded_module_file = Path(py_module.__file__).resolve().absolute().as_posix()
        posix_working_dir = Path(working_dir).absolute().as_posix()
        if _relative_to(loaded_module_file, posix_working_dir) is None:
            if force_reload:
                # If force_reload is True, reload the module instead of raising exception.
                # This is used when we don't care the original module with the same name.
                return importlib.reload(py_module)
            raise RuntimeError(
                "Could not import module: '{}' because module with the same name has been loaded.\n"
                "Path of the module: {}\n"
                "Working dir: {}".format(module_name, loaded_module_file, posix_working_dir))
        return py_module


def _get_source_path(source):
    # Get path of source
    source = str(source)
    if is_py_file(source):
        file_path = source
    else:
        file_path = source.replace('.', '/') + '.py'
    return file_path


def _has_dsl_component_str(source):
    # Check if module/file has dsl.component.
    file_path = _get_source_path(source)
    with contextlib.suppress(BaseException), open(file_path) as fout:
        content = fout.read()
        if any(f'dsl.{decorator}' in content for decorator in [
                'module', '_component', 'component', 'command_component', 'sweep_component']):
            return True
    return False


def _get_component_path_and_name_from_source(source, suffix='.py'):
    if source is None:
        raise KeyError('Source could not be None.')
    module_path = Path(source).as_posix()
    if module_path.endswith(suffix):
        module_path = module_path[:-len(suffix)]
    module_path = module_path.replace('/', '.')
    module_name = module_path.split('.')[-1]
    module_path = '/'.join(module_path.split('.')[:-1])
    if module_path == '':
        module_path = '.'
    return module_path, module_name


def _source_exists(source):
    # Check if source exists
    # pathlib.Path.exists throws exception when special char in path, use os.path.exists instead
    return os.path.exists(_get_source_path(source))


def _try_to_get_relative_path(path):
    """Tries to get a relative path from os.getcwd() to path.

    :param path: Path to get relative to.
    :return: Returns relative path in posix style, returns original path in posix style if couldn't.
    """
    try:
        result = _relative_to(path, os.getcwd(), raises_if_impossible=True)
    except ValueError:
        result = Path(path)
    return result.as_posix()


def is_py_file(entry: str):
    """Check whether the file is a python file."""
    return entry.endswith('.py')


def _to_camel_case(s):
    """Get the name in spec according to variable name."""
    s = s.replace('_', ' ')
    return s[0].upper() + s[1:]


def _sanitize_python_variable_name(s):
    """Get the variable name according to the name in spec, it should be the inverse of _to_camel_case."""
    return s.lower().replace(' ', '_')


def _resolve_source_directory():
    """Resolve source directory as last customer frame's module file dir position."""
    source_file = _resolve_source_file()
    # Fall back to current working directory if not found
    return Path(os.getcwd()) if not source_file else Path(os.path.dirname(source_file)).absolute()


def _resolve_source_file():
    """Resolve source file as last customer frame's module file position."""
    try:
        frame_list = inspect.stack()
        # We find the last frame which is in SDK code instead of customer code or dependencies code
        # by checking whether the package name of the frame belongs to azure.ml.component.
        pattern = r'(^azure\.ml\.component(?=\..*|$).*)'
        for frame, last_frame in zip(frame_list, frame_list[1:]):
            if _assert_frame_package_name(pattern, frame.frame) and \
                    not _assert_frame_package_name(pattern, last_frame.frame):
                module = inspect.getmodule(last_frame.frame)
                return Path(module.__file__).absolute() if module else None
    except Exception:
        return None


def _dsl_custom_aml_ignore(patterns):
    """Create custom .amlignore for dsl."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tfp:
        tfp.writelines(patterns)
        return Path(tfp.name).resolve()


def is_dsl_func(function):
    return is_dsl_component(function) or is_dsl_pipeline(function)


def is_dsl_component(function):
    return hasattr(function, '_is_dsl_component')


def is_dsl_pipeline(function):
    return hasattr(function, '_is_dsl_pipeline')


def get_workspace(path=None):
    try:
        return Workspace.from_config(path=path)
    except Exception:
        raise UserErrorException(WORKSPACE_ERROR_MSG)


@dataclass
class ComponentReferenceConfig:
    yaml: Optional[str] = None
    name: Optional[str] = None
    version: Optional[str] = None
    id: Optional[str] = None


@dataclass
class ComponentLoaderConfig:
    default_version: Optional[str] = None  # noqa: E704
    force_version: Optional[str] = None  # noqa: E701
    post_load: Optional[str] = None
    use_local: Optional[str] = '*'
