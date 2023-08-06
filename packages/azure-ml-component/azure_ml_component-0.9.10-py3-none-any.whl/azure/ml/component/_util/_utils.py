# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import logging
import requests
import os
import sys
import json
import re
import time
from enum import Enum
from inspect import Parameter
from typing import Union, List, Tuple
from threading import Thread, Event
from functools import wraps

import docker
import zipfile
import functools
import shutil
import uuid
import jwt
from os import name as os_name
from shlex import quote
from datetime import datetime
from pathlib import Path, PureWindowsPath
from uuid import UUID
from unittest import mock
from collections import namedtuple
from contextlib import contextmanager

from azureml.core import Workspace
from azureml.data.datapath import DataPath
from azureml.data.data_reference import DataReference
from azureml.data.abstract_dataset import AbstractDataset
from azureml.data._dataset import _Dataset
from azure.ml.component._restclients.designer.models import EntityStatus, DataInfo, \
    DataSetDefinition, RegisteredDataSetReference, SavedDataSetReference, \
    StructuredInterfaceParameter, StructuredInterfaceInput, \
    DataSetDefinitionValue, LegacyDataPath, DataPath as DataPathModel
from azureml.exceptions import WebserviceException, UserErrorException

TIMEOUT_SECONDS = 60 * 30
COMPONENT_NAME_MAX_LEN = 254


def _is_empty_dir(path):
    path = Path(path)
    return path.is_dir() and next(path.iterdir(), None) is None


def copytree(src, dst, symlinks=False, ignore=None, exist_ok=False):
    """Copy the folder to dst with the parameter exist_ok."""
    # If exist_ok is False, keep the behavior of shutil.copytree.
    if not exist_ok:
        shutil.copytree(src, dst, symlinks, ignore)
        return
    # Otherwise recursively copy the files in src to dst.
    os.makedirs(dst, exist_ok=True)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copytree(s, d, symlinks, ignore, exist_ok)
        else:
            _copy2(s, d)


def _extract_zip(zip_file, target_dir):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(target_dir)


def _ensure_target_folder_exist(target, overwrite=False):
    """Check target folder exists, if not it will create it."""
    target = Path(target)
    if target.exists() and not _is_empty_dir(target) and not overwrite:
        raise FileExistsError("Target '%s' can only be an empty folder when overwrite=False." % target)
    if target.exists():
        try:
            # Remove the empty folder to store snapshot.
            shutil.rmtree(target)
        except Exception as e:
            # Raise error when the target is used in other processor.
            raise UserErrorException(f"Remove {target} failed, Error detail: {e}")
    # Make sure the parent folder exists.
    target.parent.mkdir(exist_ok=True, parents=True)
    return target


def _download_snapshot_by_id(component_api_caller, snapshot_id, target, component_name=None, registry_name=None):
    """
    Download snapshot by snapshot_id
    :param component_api_caller: Api caller for component operation.
    :type component_api_caller: azure.ml.component._api.ComponentAPI
    :param snapshot_id: Snapshot id
    :type snapshot_id: str
    :param target: Local path to store the snapshot.
    :type target: str
    :param component_name: component name.
    :type component_name: str
    :param registry_name: The registry name of component.
    :type registry_name: str
    """
    component_api_caller.download_snapshot_by_id(snapshot_id, target, component_name=component_name,
                                                 registry_name=registry_name)


def _normalize_name(name):
    normalized_name = name.lower()
    normalized_name = re.sub(r'[\W_]', ' ', normalized_name)  # No non-word characters
    normalized_name = re.sub(' +', ' ', normalized_name).strip()  # No double spaces, leading or trailing spaces
    return normalized_name


def _normalize_identifier_name(name):
    normalized_name = _normalize_name(name)
    if re.match(r'\d', normalized_name):
        normalized_name = 'n' + normalized_name  # No leading digits
    return normalized_name


def _sanitize_name(name):
    return _normalize_name(name).replace(' ', '_')


def _sanitize_folder_name(name):
    pattern = r'[<>:"\\/|?*]'
    normalized_name = re.sub(pattern, '_', name)
    return normalized_name


def _sanitize_python_variable_name(name: str):
    return _normalize_identifier_name(name).replace(' ', '_')


def _sanitize_python_variable_name_with_value_check(name: str):
    sanitized_name = _sanitize_python_variable_name(name)
    if sanitized_name == '':
        raise ValueError('Given name {} could not be normalized into python variable name.'.format(name))
    return sanitized_name


basic_python_type = [str, int, float, bool, type(None)]


def _value_type_json_serializable(obj):
    """Check if an object is JSON serializable recursively."""
    # Inheriting from dict is the only way to make class JSON serializable
    # in circumstance of calling `dumps` with neither encoder nor jsonpickle.
    obj_id_set = set()

    def _is_valid_type(obj):
        # Extract value if obj is Enum
        if isinstance(obj, Enum):
            obj = obj.value
        if type(obj) in basic_python_type:
            return True
        valid_type = True
        obj_id = id(obj)
        if obj_id in obj_id_set:
            # Circular reference detected
            return False
        obj_id_set.add(obj_id)
        if type(obj) in [tuple, list]:
            for val in obj:
                valid_type &= _is_valid_type(val)
                if not valid_type:
                    break
        elif isinstance(obj, dict):
            for k, v in obj.items():
                valid_type &= _is_valid_type(k) & _is_valid_type(v)
                if not valid_type:
                    break
        else:
            valid_type = False
        obj_id_set.remove(obj_id)
        return valid_type

    return _is_valid_type(obj)


def _get_name_in_mapping(name: str, name_map: dict):
    return name_map[name] if name_map and name in name_map.keys() else name


def is_float_convertible(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


def is_int_convertible(string):
    try:
        int(string)
        return True
    except ValueError:
        return False


def is_bool_string(string):
    if not isinstance(string, str):
        return False
    return string == 'True' or string == 'False'


hyper_parameter_type_names = [
    'choice', 'lognormal', 'loguniform', 'normal', 'qlognormal',
    'qloguniform', 'qnormal', 'quniform', 'randint', 'uniform'
]


def is_hyper_parameter(obj):
    """Return True is object seems like [{hyper_parameter_type}, [...]]"""
    if type(obj) != list or len(obj) != 2:
        return False
    global hyper_parameter_type_names
    if obj[0] in hyper_parameter_type_names and type(obj[1]) is list:
        return True
    return False


def _is_uuid(str):
    try:
        UUID(hex=str)
    except ValueError:
        return False
    return True


def int_str_to_pipeline_status(str):
    if str == '0':
        return EntityStatus.ACTIVE.value
    elif str == '1':
        return EntityStatus.DEPRECATED.value
    elif str == '2':
        return EntityStatus.DISABLED.value
    else:
        return 'Unknown'


def _unique(elements, key):
    return list({key(element): element for element in elements}.values())


def _is_prod_workspace(workspace):
    if workspace is None:
        return True

    return workspace.location != "eastus2euap" and workspace.location != "centraluseuap" and \
        workspace.subscription_id != "4faaaf21-663f-4391-96fd-47197c630979" and \
        workspace.subscription_id != "74eccef0-4b8d-4f83-b5f9-fa100d155b22"


def _can_visualize():
    """Return true if the platform widget can be visualized in jupyter notebook, otherwise return false."""
    try:
        from IPython import get_ipython
        from traitlets import Unicode
        from ipywidgets import DOMWidget

        if Unicode and DOMWidget:
            pass

        # ContainerClient only exists for azure.storage.blob >= 12.0.0
        # we will fallback to BlockBlobService if ContainerClient not exist
        try:
            from azure.storage.blob import ContainerClient
            if ContainerClient:
                pass
        except:
            from azure.storage.blob import BlockBlobService
            if BlockBlobService:
                pass

        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True  # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except (NameError, ModuleNotFoundError, ImportError):
        return False  # Probably standard Python interpreter


def _is_in_notebook():
    try:
        from IPython import get_ipython
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True
    except:
        return False
    return False


def _is_json_string_convertible(string):
    try:
        json.loads(string)
    except ValueError:
        return False
    return True


def _dumps_raw_json(obj):
    try:
        json_string = json.dumps(obj)
    except TypeError:
        return False
    return json_string


def _is_json_string_in_type(val, types):
    try:
        obj = json.loads(val)
    except json.decoder.JSONDecodeError:
        return False
    for t in types:
        if isinstance(obj, t):
            return True
    return False


def _get_short_path_name(path, is_dir, create_dir=False):
    '''
        https://docs.microsoft.com/en-us/windows/win32/fileio/naming-a-file#short-vs-long-names
        Maximum length for a path may defined by 260 characters in Windows.
        So need to trans path to shorten path to avoid filename too long.
        Example short/long path in windows:
            dir path: C:\\pipeline-local_run\\67a8bfde-9014-45c0-acc7-1db02d422302\\A dummy pipeline
            dir short path: C:\\PIPELI~2\\67A8BF~1\\ADUMMY~1
            file path: C:\\pipeline-local_run\\67a8bfde-9014-45c0-acc7-1db02d422302\\A dummy pipeline\\long_name.txt
            file short path: 'C:\\PIPELI~1\\67A8BF~1\\ADUMMY~1\\LONG_N~1.TXT'
        :param path: need to be shorten path
        :type path: str
        :param is_dir: Path is dir or file
        :type is_dir: bool
        :param create_dir: If create_dir=True, when create dirs before get shorten name
        :type create_dir: bool
        :return: short path form. If path is a short path, will no change.
        :rtype: str
    '''
    if os.name == 'nt':
        try:
            # win32api is an additional module for windows in pywin32
            # https://docs.python.org/3/using/windows.html#additional-modules
            import win32api
            path_list = Path(path).absolute().parts
            short_path = win32api.GetShortPathName(os.path.join(path_list[0]))
            for item in path_list[1: None if is_dir else -1]:
                if create_dir:
                    Path(os.path.join(short_path, item)).mkdir(parents=True, exist_ok=True)
                short_path = win32api.GetShortPathName(os.path.join(short_path, item))
            if not is_dir:
                short_path = win32api.GetShortPathName(os.path.join(short_path, path_list[-1]))
            return short_path
        except Exception as e:
            # If path is not exist will raise error.
            logging.warning(f"When get the short path of {path} raise exception, {e}.")
            if create_dir:
                if is_dir:
                    Path(path).mkdir(parents=True, exist_ok=True)
                else:
                    Path(path).parent.mkdir(parents=True, exist_ok=True)
            return str(PureWindowsPath(Path(path).absolute()))
    else:
        short_path = Path(path)
        if not short_path.exists() and create_dir:
            if is_dir:
                short_path.mkdir(parents=True)
            elif not short_path.parent.exists():
                # On Linux, if exist_ok is true, FileExistError will be raised if the last path component is a file
                # So we check the existence first
                short_path.parent.mkdir(parents=True, exist_ok=True)
        return path


def _flatten_pipeline_parameters(pipeline_parameters):
    if pipeline_parameters is None:
        return {}
    flattened_pipeline_parameters = {}
    from azure.ml.component._core._types import _GroupAttrDict
    for k, v in pipeline_parameters.items():
        if isinstance(v, _GroupAttrDict):
            flattened_pipeline_parameters.update(v._flatten(group_parameter_name=k))
        else:
            flattened_pipeline_parameters[k] = v
    return flattened_pipeline_parameters


def _get_parameter_static_value(obj, pipeline_parameters=None):
    from azure.ml.component.component import Input
    from azure.ml.component._pipeline_parameters import PipelineParameter
    from azure.ml.component._parameter_assignment import _ParameterAssignment
    pipeline_parameters = {} if pipeline_parameters is None else pipeline_parameters
    #  If obj is Input, get internal data source first
    if isinstance(obj, Input):
        obj = obj._get_internal_data_source()

    if isinstance(obj, PipelineParameter):
        return pipeline_parameters[obj.name] if obj.name in pipeline_parameters else obj.default_value
    elif isinstance(obj, _ParameterAssignment):
        return obj.value if len(pipeline_parameters) == 0 else \
            obj.get_value_with_pipeline_parameters(pipeline_parameters)

    obj = obj.value if isinstance(obj, Enum) else obj
    return obj


def _get_valid_directory_path(directory_path):
    suffix = 1
    valid_path = directory_path
    while os.path.exists(valid_path):
        valid_path = '{}({})'.format(directory_path, suffix)
        suffix += 1
    return valid_path


def _scrubbed_exception(exception_type, msg: str, args):
    """
    Return the exception with scrubbed error message. Use this to add scrubbed message to exceptions
    that we don't want the record the full message in because it may contains sensitive information.

    :param exception_type: The exception type to create.
    :param msg: The message format.
    :param args: The original args for message formatting.
    :return: The created exception.
    """
    scrubbed_data = '[Scrubbed]'
    e = exception_type(msg.format(args))
    e.scrubbed_message = msg.replace("{}", scrubbed_data)
    return e


def _get_data_info_hash_id(data_info: DataInfo):
    if data_info.saved_dataset_id is not None:
        identifier = data_info.saved_dataset_id
    elif data_info.relative_path is not None:
        identifier = _sanitize_python_variable_name(data_info.relative_path)
    elif data_info.id is not None:
        identifier = data_info.id
    elif data_info.name is not None:
        identifier = data_info.name
    else:
        raise ValueError('Invalid data source {}'.format(data_info.as_dict()))

    return str(uuid.uuid3(uuid.NAMESPACE_DNS, identifier))


def pull_docker_image(docker_client, image_location, username, password, stop_event=None):
    """
    Pulls the docker image from the ACR
    :param docker_client:
    :type docker_client: docker.DockerClient
    :param image_location:
    :type image_location: str
    :param username:
    :type username: str
    :param password:
    :type password: str
    :return:
    :rtype: None
    """
    try:
        print('Pulling image from ACR (this may take a few minutes depending on image size)...\n')
        for message in docker_client.api.pull(image_location, stream=True, decode=True, auth_config={
            'username': username,
            'password': password
        }):
            if stop_event and stop_event.isSet():
                print('Cancel pull image.')
                break
            prefix = '{}: '.format(message['id']) if 'id' in message else ''
            status = message['status']
            progress = message.get('progressDetails', {}).get('progress', '')
            print(prefix + status + progress)
    except docker.errors.APIError as e:
        raise WebserviceException('Error: docker image pull has failed:\n{}'.format(e))
    except Exception as exc:
        raise WebserviceException('Error with docker pull {}'.format(exc))


def deprecated(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logging.warning('This method has been deprecated and will be removed in the future release.')
        return func(*args, **kwargs)

    return wrapper


def trans_to_valid_file_name(file_name):
    return re.sub('[/?<>\\\\:*|"]', '_', file_name)


def print_to_terminal(msg):
    from azure.ml.component._execution._component_run_logger import Logger
    if isinstance(sys.stdout, Logger):
        sys.stdout.print_to_terminal(msg)
    else:
        print(msg)


def get_dataset_def_from_dataset(workspace, dataset):
    # Resolve dataset def as value assignments if parameter is dataset
    dataset_def = None
    from .._dataset import _GlobalDataset
    if isinstance(dataset, _GlobalDataset) or isinstance(dataset, DataReference):
        dataset_def = _get_dataset_def_from_dataset(dataset)
    elif isinstance(dataset, _Dataset):
        _ensure_dataset_saved_in_workspace(dataset, workspace)
        dataset_def = _get_dataset_def_from_dataset(dataset)
    return dataset_def


def resolve_datasets_from_parameter(workspace, _param):
    _dataset_param = {}
    _other_param = {}
    # Resolve dataset def as value assignments if parameter is dataset
    for _k, _v in _param.items():
        dataset_def = get_dataset_def_from_dataset(workspace, _v)
        if dataset_def is not None:
            _dataset_param[_k] = dataset_def.value
        else:
            _other_param[_k] = _v
    return _other_param, _dataset_param


def resolve_data_path_assignments_from_parameter(_param, outputs=None, parameters_and_inputs=None):
    if outputs:
        return _resolve_pipeline_submit_data_path_assignments(_param, outputs, parameters_and_inputs)
    else:
        return _resolve_published_and_endpoint_submit_data_path_assignments(_param)


def resolve_pipeline_parameters(pipeline_parameters: dict, flatten: bool = False,
                                resolve_dataset: bool = False, workspace: Workspace = None,
                                resolve_data_path: bool = False, outputs=None,
                                parameters_and_inputs=None, remove_empty=False) -> Tuple[dict, dict, dict]:
    """ Resolve pipeline parameters.

    1. Extract enum to string.
    2. Resolve Component and OutputsAttrDict type to Output.
    3. Convert customer group class object to group attr dict.
    4. Remove empty value (optional).
    5. Flatten group parameters (optional).
    6. Resolve dataset from parameters (optional).
    7. Resolve data path from parameters (optional).
    """
    if pipeline_parameters is None:
        return {}, {}, {}
    dataset_def_value_assignments, data_path_assignments = {}, {}
    if not isinstance(pipeline_parameters, dict):
        raise UserErrorException("pipeline_parameters must in dict {parameter: value} format.")
    from azure.ml.component._pipeline_expression import PipelineExpression
    from azure.ml.component.component import _OutputsAttrDict, Component
    from azure.ml.component._core._types import _Group
    # extract enum values and convert group value to attrdict
    updated_parameters = {}
    for k, v in pipeline_parameters.items():
        if isinstance(v, PipelineExpression):
            # For the case use a PipelineExpression as the input,
            #   dynamically generate code block of component function from PipelineExpression,
            #   declare using exec() and call with eval().
            v = v._create_dynamic_component()
        if isinstance(v, Component):
            # For the case use a component/pipeline as the input, we use its only one output as the real input.
            # Here we set dset = dset.outputs, then the following logic will get the output object.
            v = v.outputs
        if isinstance(v, Enum):
            v = v.value
        if isinstance(v, _OutputsAttrDict):
            # For the case that use the outputs of another component as the input,
            # we use the only one output as the real input,
            # if multiple outputs are provided, an exception is raised.
            output_len = len(v)
            if output_len != 1:
                raise UserErrorException('%r output(s) found of specified outputs when setting input %r,'
                                         ' exactly 1 output required.' % (output_len, k))
            v = list(v.values())[0]
        if v is None and remove_empty:
            continue
        updated_parameters[k] = _Group._customer_class_value_to_attr_dict(v)
    pipeline_parameters = updated_parameters
    if flatten:
        pipeline_parameters = _flatten_pipeline_parameters(pipeline_parameters)
    if resolve_dataset:
        if not workspace:
            raise UserErrorException("resolving dataset from pipeline_parameters needs workspace as parameter.")
        pipeline_parameters, dataset_def_value_assignments = resolve_datasets_from_parameter(workspace,
                                                                                             pipeline_parameters)
    if resolve_data_path:
        pipeline_parameters, data_path_assignments = resolve_data_path_assignments_from_parameter(
            pipeline_parameters,
            outputs,
            parameters_and_inputs
        )
    return pipeline_parameters, dataset_def_value_assignments, data_path_assignments


def _resolve_pipeline_submit_data_path_assignments(_param, outputs, parameters_and_inputs):
    data_path_assignments = {}
    for k in outputs:
        v = _param.get(k, None)
        if not v:
            continue
        if not isinstance(v, DataPath):
            if k in parameters_and_inputs:
                continue
            raise UserErrorException("Invalid datatype for datapath re-assignments of output '{0}', should be "
                                     "'azureml.data.datapath.DataPath', got '{1}'.".format(k, type(v)))
        data_path_assignments[k] = \
            LegacyDataPath(data_store_name=v.datastore_name, relative_path=v.path_on_datastore)
        del _param[k]
    return _param, data_path_assignments


def _resolve_published_and_endpoint_submit_data_path_assignments(_param):
    _data_key = []
    data_path_assignments = {}
    for k, v in _param.items():
        if isinstance(v, DataPath):
            data_path_assignments[k] = \
                LegacyDataPath(data_store_name=v.datastore_name, relative_path=v.path_on_datastore)
            _data_key.append(k)
    if _data_key:
        for k in _data_key:
            del _param[k]
    return _param, data_path_assignments


def _get_dataset_def_from_dataset(dataset):
    def _get_dataset_def_from_data_path(data_path, data_type):
        dataset_def_val = DataSetDefinitionValue(literal_value=data_path)
        dataset_def = DataSetDefinition(
            data_type_short_name=data_type,
            value=dataset_def_val
        )
        return dataset_def

    from .._dataset import _GlobalDataset
    if isinstance(dataset, _GlobalDataset):
        data_path = DataPathModel(data_store_name=dataset.data_store_name, relative_path=dataset.relative_path)
        return _get_dataset_def_from_data_path(data_path, 'DataFrameDirectory')

    if isinstance(dataset, DataReference):
        data_path = DataPathModel(data_store_name=dataset.datastore.name, relative_path=dataset.path_on_datastore)
        return _get_dataset_def_from_data_path(data_path, 'AnyDirectory')

    # Either data_set_reference or saved_data_set_reference shall be not None in dataset_def.
    saved_dataset_ref = None
    if dataset._registration and dataset._registration.registered_id:
        dataset_ref = RegisteredDataSetReference(
            id=dataset._registration.registered_id if dataset._registration else None,
            version=dataset._registration.version if dataset._registration else None,
            name=dataset._registration.name if dataset._registration else None
        )
    else:
        dataset_ref = None
        if dataset.id:
            saved_id = dataset.id
            saved_dataset_ref = SavedDataSetReference(id=saved_id)

    dataset_def_val = DataSetDefinitionValue(data_set_reference=dataset_ref,
                                             saved_data_set_reference=saved_dataset_ref)

    dataset_def = DataSetDefinition(
        data_type_short_name='AnyDirectory',
        value=dataset_def_val
    )
    return dataset_def


def _registry_discovery(registry_name, auth_header):
    from azureml._restclient.clientbase import ClientBase
    from azureml._execution._commands import _raise_request_error, _get_common_headers

    base_url = "https://southcentralus.api.azureml.ms"
    discovery_url = base_url + f"/registrymanagement/v1.0/registries/{registry_name}/discovery"

    headers = _get_common_headers()
    headers.update(auth_header)

    response = ClientBase._execute_func(requests.get, discovery_url, headers=headers)
    _raise_request_error(response, "Registry discovery")

    content = response.content
    if isinstance(content, bytes):
        content = content.decode('utf-8')
    content = json.loads(content)
    return content


def _ensure_dataset_saved_in_workspace(dataset: AbstractDataset, ws: Workspace):
    """Ensure the dataset is saved in the target workspace.

    This is an alternative function for dataset._ensure_saved,
    since dataset._ensure_saved only check whether it is saved in 'some workspace' not the "target workspace".
    It will introduce unexpected behavior if we use this method twice for two different workspaces.
    This function make sure that it is always correct even it is called in multiple workspaces.
    """
    if dataset.name is not None:
        return  # The dataset with a name is a registered dataset, it doesn't need to take action
    if dataset._registration is not None and dataset._registration.workspace == ws:
        return  # If the dataset is registered in the target workspace, no need to take action.
    dataset._registration = None  # Set the registration as None to make sure it will be registered.
    dataset._ensure_saved(workspace=ws)


def _str_to_bool(s):
    """Returns True if literal 'true' is passed, otherwise returns False.

    Can be used as a type for argument in argparse, return argument's boolean value according to it's literal value.
    """
    if not isinstance(s, str):
        return False
    return s.lower() == 'true'


def _try_to_get_workspace():
    """Try to get workspace from config, returns None if not exist."""
    try:
        from azureml.core import Workspace
        return Workspace.from_config()
    except Exception:
        return None


def _copy2(src, dst):
    """Wraps shutil.copy2 and work around possible "Function not implemented" exception thrown by it.

    Background: shutil.copy2 will throw OSError when dealing with Azure File.
    See https://stackoverflow.com/questions/51616058 for more information.
    """
    if hasattr(os, 'listxattr'):
        # always shadow shutil._copyxattr is exist to avoid error "Function not implemented" on Azure
        # since we don't need to copy them
        # we shadow shutil._copyxattr because we still seeing transient errors in telemetry when shadowing
        # os.listxattr
        with mock.patch('shutil._copyxattr', return_value=[]):
            shutil.copy2(src, dst)
    else:
        shutil.copy2(src, dst)


def _relative_to(path, basedir, raises_if_impossible=False):
    """Compute the relative path under basedir.

    This is a wrapper function of Path.relative_to, by default Path.relative_to raises if path is not under basedir,
    In this function, it returns None if raises_if_impossible=False, otherwise raises.

    """
    # The second resolve is to resolve possible win short path.
    path = Path(path).resolve().absolute().resolve()
    basedir = Path(basedir).resolve().absolute().resolve()
    try:
        return path.relative_to(basedir)
    except ValueError:
        if raises_if_impossible:
            raise
        return None


def _relative_path(path, basedir, raises_if_impossible=False):
    """Compute the path relative to basedir.

    Note: this function allow all path as input even if it's not under basedir.
    """
    # Note: here we call os.path.relpath instead of Path.relative_to
    # Exception raised if path and basedir have different mount. like D:// and C://
    try:
        return Path(os.path.relpath(path, basedir))
    except ValueError:
        if raises_if_impossible:
            raise
        return None


def _convert_to_shell_execution_command(command, conda_environment_name=None):
    """
    Convert command to shell execution command. If set conda_environment_name, it will add conda activate command
    before execute command. For linux, converted command will be str command. For windows, it depends on command type.
    For example, set list command as ['echo', 'space \'value'], str command as 'echo space \'value':
        In Windows, it only connect conda command and command:
            1) For list command, it will return ['conda', 'activate', conda_name, '&&', 'echo', 'space \'value'].
            2) For str command, it will return 'conda activate conda_name && echo space \'value'.
        In Linux, it will turn command to shell-escape version.
            1) For list command, it will return ". $(conda info --base)/etc/profile.d/conda.sh;conda activate conda
               conda_name;echo 'space \'value'".
            2) For str command, it will return ". $(conda info --base)/etc/profile.d/conda.sh;conda activate conda
               conda_name;'echo space \'value'".

    :return converted_command: Converted command
    :rtype converted_command: str or list[str]
    """
    converted_command = command
    conda_command = []
    if os_name == 'nt':
        if conda_environment_name:
            # Add conda activate command before command.
            conda_command = ['conda', 'activate', conda_environment_name, '&&']
        if isinstance(converted_command, str):
            # When command is string, to avoid translate original command,
            # need to connect conda command and command to string.
            converted_command = ' '.join(conda_command + [converted_command])
        else:
            # When command is list, subprocess will translate a sequence of arguments into a command line.
            # To avoid translate conda command as args, split conda command to list and add to command.
            converted_command[0:0] = conda_command
    else:
        if conda_environment_name:
            # In linux, conda may be not available in subshells, need to enable conda before use it.
            # https://github.com/conda/conda/issues/7980#issuecomment-441358406
            conda_command = [
                '. $(conda info --base)/etc/profile.d/conda.sh',
                'conda activate %s' % conda_environment_name]
        if isinstance(converted_command, list):
            # Convert args contains specail character to string that safely be used in shell.
            converted_command = ' '.join([quote(item) for item in converted_command])
        converted_command = ';'.join(conda_command + [converted_command])
    return converted_command


class TimerContext(object):
    """A context manager calculates duration when executing inner block."""

    def __init__(self):
        self.start_time = None

    def get_duration_seconds(self):
        """Get the duration from context manger start to this function call.
        Result will be format to two decimal places.

        """
        duration = datetime.utcnow() - self.start_time
        return round(duration.total_seconds(), 2)

    def __enter__(self):
        self.start_time = datetime.utcnow()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def fetch_user_id_from_aad_token(token) -> (str, bool):
    """Fetch user object id from aad token and check if the user is service principle.

    :param token: aad token
    :return: user object id and if this user is service principle.
    """
    # We set verify=False, as we don't have keys to verify signature, and we also don't need to
    # verify signature, we just need the user object id.
    decode_json = jwt.decode(token, options={'verify_signature': False, 'verify_aud': False})
    # For an access tokens generated by service principal, 'name' does not exist in the token.
    is_service_principle = False if 'name' in decode_json.keys() else True
    return decode_json['oid'], is_service_principle


def _get_enum(value, enum_class, raise_unknown=False):
    """Return the enum according to the string value from backend."""
    if isinstance(value, enum_class):  # If an expected enum is passed, we simply return it.
        return value
    value = str(value)
    for i, s in enumerate(enum_class):
        if str(i) == value or s.value == value:
            return s
    # When the status is not in the enum, we raise exception if raise_unknown
    if raise_unknown:
        msg = "Got unknown value %s for enum %r," % (value, enum_class) + \
              " you may update the SDK/CLI to the latest version to resolve this issue."
        raise ValueError(msg)
    # otherwise we create a fake enum which has such value to avoid breaking.
    # We should try to make sure this branch is not reached.
    FakeStatus = namedtuple('FakeEnum', ['name', 'value'])
    return FakeStatus(name=value, value=value)


def _get_string_id_from_enum(enum, enum_class):
    """Return the order string according to given enum."""
    for i, s in enumerate(enum_class):
        if s == enum:
            return str(i)
    raise ValueError("Enum {} not found in class {}.".format(enum, enum_class))


def _get_param_in_group_from_pipeline_parameters(
        param_name, pipeline_parameters, param_groups=None, pipeline_name=None):
    """Get the single parameter value in group from pipeline parameters."""
    value_name = param_groups[0] if param_groups else param_name
    if value_name not in pipeline_parameters:
        return Parameter.empty
    value = pipeline_parameters[value_name]
    missing_property_msg = 'Value of group parameter %r missing property %r'
    missing_property_msg += f' in pipeline {pipeline_name!r}.' if pipeline_name else '.'
    if param_groups:
        # Extract the real value from group
        for path in param_groups[1:]:
            if not hasattr(value, path):
                logging.warning(missing_property_msg % (value_name, path))
                return None
            value = getattr(value, path)
        if not hasattr(value, param_name):
            logging.warning(missing_property_msg % (value_name, param_name))
            return None
        value = getattr(value, param_name)
    return value


def _camel_to_snake_case(s):
    """Convert camel name to snake name.
    E.g. CamelToSnakeCase -> camel_to_snake_case.
    """
    return re.sub(r'(?<!^)(?=[A-Z])', '_', s).lower()


def is_valid_component_name(name):
    """
    Validate a component name.
    Name must be between 1 to 255 characters, start with letters or numbers.
    Valid characters are letters, numbers, ".", "-" and "_".

    :param name: Component name
    :type name: str
    :return: Boolean.
    """
    if name is None or (not isinstance(name, str)) or name == '':
        return False
    pattern = '^[a-zA-Z0-9][a-zA-Z0-9\-_.]{0,' + str(COMPONENT_NAME_MAX_LEN) + '}$'
    pattern = re.compile(pattern)
    return True if pattern.match(name) is not None else False


def is_valid_experiment_name(name):
    """
    Validate experiment name.
    Experiment name must be 1-256 characters,
    start with a letter or a number, and can only contain letters, numbers, underscores, and dashes.

    :param name: Experiment name
    :type name: str
    :return: Boolean.
    """
    if name is None or (not isinstance(name, str)) or name == '':
        return False
    pattern = re.compile('^[0-9a-zA-Z][0-9a-zA-Z_-]*$')
    return True if pattern.match(name) is not None else False


def is_valid_node_name(name):
    """
    Validate user defined node name.
    Node name must be 1-255 characters,
    start with a letter or underscore, and can only contain letters, numbers, underscores.

    :param name: Node name
    :type name: str
    :return: Boolean.
    """
    if name is None or (not isinstance(name, str)) or name == '' or len(name) > 255:
        return False
    return name.isidentifier()


def transform_default_experiment_name(name):
    """
    transform default experiment_name to be valid: start with a letter or a number, and can only contain
    letters, numbers, underscores, and dashes

    :param name: default experiment name
    :type name: str
    :return: experiment_name.
    :rtype: str
    """
    experiment_name = re.sub("[^\\w-]", "_", name)
    experiment_name = experiment_name.lstrip('-_')
    return experiment_name


def ensure_valid_experiment_name(experiment_name, default_name):
    """
    Validate user_defined experiment_name or make default experiment name conform to the naming rule.

    Experiment name must start with a letter or a number, and can only contain letters, numbers,
    underscores, and dashes. When the name is not valid, an exception will be raised.

    :param experiment_name: Experiment name
    :type experiment_name: str
    :param default_name: Default experiment name
    :type default_name: str

    :return: experiment_name
    :rtype: str
    """
    if not experiment_name:
        experiment_name = transform_default_experiment_name(default_name)
    # validate experiment_name
    if not is_valid_experiment_name(experiment_name):
        raise UserErrorException("Experiment name must start with a letter or a number, and can only contain "
                                 "letters, numbers, underscores, and dashes.")
    return experiment_name


def enabled_subpipeline_registration() -> bool:
    """Return True if user enabled sub pipeline registration in environment variable."""
    if os.getenv('ENABLE_SUBPIPELINE_REGISTER', 'true').lower() == 'false':
        raise UserErrorException('Disable sub-pipeline register is no longer supported!')
    return True


DSL_COMPONENT_EXECUTION = 'DSL_COMPONENT_EXECUTION'


def dsl_component_execution() -> bool:
    """Return True if dsl component is executing."""
    if os.getenv(DSL_COMPONENT_EXECUTION, 'false').lower() == 'true':
        return True
    return False


def repr_parameter(
        param: Union[StructuredInterfaceParameter, StructuredInterfaceInput, 'RunSettingParamDefinition']) -> str:
    from azure.ml.component._core._types import _Param
    from azure.ml.component._api._api import _DefinitionInterface
    from azure.ml.component._core._run_settings_definition import RunSettingParamDefinition

    result = {
        "optional": param.is_optional
    }

    if isinstance(param, StructuredInterfaceInput):
        result["type"] = "input"
    elif isinstance(param, StructuredInterfaceParameter):
        if param.parameter_type is not None:
            result["type"] = _DefinitionInterface._structured_interface_parameter_type(param)
        else:
            result["type"] = "unknown"
    elif isinstance(param, RunSettingParamDefinition):
        result["type"] = _Param.parse_param_type(param.type_in_py)

    if getattr(param, "lower_bound", None):
        result["min"] = param.lower_bound
    if getattr(param, "upper_bound", None):
        result["max"] = param.upper_bound
    if getattr(param, "enum_values", None):
        result["enum"] = param.enum_values
    return str(result)


@contextmanager
def environment_variable_overwrite(key, val):
    if key in os.environ.keys():
        backup_value = os.environ[key]
    else:
        backup_value = None
    os.environ[key] = val

    try:
        yield
    finally:
        if backup_value:
            os.environ[key] = backup_value
        else:
            os.environ.pop(key)


@contextmanager
def _change_profile(profile):
    """Context manager for profile change."""
    original_profile = sys.getprofile()
    if profile != original_profile:
        sys.setprofile(profile)
    try:
        yield
    finally:
        if profile != original_profile:
            sys.setprofile(original_profile)


class CatchExceptionThread(Thread):

    def run(self):
        self.exec = None
        try:
            Thread.run(self)
        except Exception as e:
            # Used to store the exception
            self.exec = e

    def join(self, timeout=None):
        Thread.join(self, timeout=timeout)
        # Since join() returns in caller thread, it will re-raise the caught exception
        if self.exec:
            raise self.exec


def timeout(timeout_msg, prompt_msg=None, timeout_seconds=TIMEOUT_SECONDS):
    """
    Limit execution time of a function. If the call is timeout, it will raise TimeoutError.

    :param timeout_msg: The error message when raising TimeoutError.
    :type timeout_msg: str
    :param prompt_msg: The prompt message displays every 30 seconds.
    :type prompt_msg: str
    :param timeout_seconds: The limit execution time of a function, the default value is 30 min.
    :type timeout_seconds: float
    """
    from azure.ml.component.dsl._utils import logger

    if '_TEST_ENV' in os.environ:
        timeout_seconds = min(timeout_seconds, 60 * 5)

    def wrap_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = []

            def function():
                # Execute the function and get the result.
                result.append(func(*args, **kwargs))

            def show_wait_message(wait_msg, stop_event):
                while not stop_event.isSet():
                    if wait_msg:
                        logger.info(wait_msg)
                    time.sleep(30)

            thread = CatchExceptionThread(target=function)
            # Start a thread used to print prompt message every 30 seconds.
            stop_event = Event()
            prompt_thread = Thread(target=show_wait_message, args=(prompt_msg, stop_event))

            thread.start()
            prompt_thread.start()
            try:
                thread.join(timeout_seconds)
            except Exception as e:
                raise e
            finally:
                # Stop the prompt thread.
                stop_event.set()
            if thread.isAlive():
                # As join() always returns None, calling is_alive() after join() to decide whether a timeout happened.
                # https://docs.python.org/3/library/threading.html#threading.Thread.join
                raise TimeoutError(timeout_msg)
            return result[0]

        return wrapper
    return wrap_decorator


def find_output_owner_in_current_pipeline(output, nodes: List, pipeline_name: str):
    """Return output's owner in nodes, raise error if not found."""
    # find all the parent check if it is current pipeline's node.
    if output._owner._is_pipeline:
        # Find the output owner of the pipeline generated by dsl
        if output._owner in nodes:
            return output._owner
        component_output = output
        while component_output._owner._is_pipeline:
            component_output = component_output._owner._outputs_mapping[component_output.port_name]
            if component_output._owner in nodes:
                return component_output._owner
    else:
        # Find the output owner of the pipeline generated without dsl
        owner = output._owner
        while owner is not None:
            if owner in nodes:
                return owner
            owner = owner._parent
    # Owner is not one of the pipeline's node
    raise UserErrorException(
        f'Component of output \'{output.port_name}\' not found in scope of current pipeline: \'{pipeline_name}\'.')


def str2bool(v):
    if v is None:
        return False
    else:
        if isinstance(v, bool):
            return v
        if v.lower() in ("yes", "true", "t", "y", "1"):
            return True
        elif v.lower() in ("no", "false", "f", "n", "0"):
            return False
        else:
            raise UserErrorException("{} is not allowed, Boolean value expected.".format(v))


def get_new_dir_name_if_exists(path: Path):
    """Returns a new directory name if current one exists."""
    name = path.name
    folder = path.parent
    i = 1
    name_candidate = name
    while (folder / name_candidate).exists():
        name_candidate = f"{name}_{i}"
        i += 1
    return folder / name_candidate


def _obj_in_list(obj, arr):
    """Check whether object is an element of a sequence.

    Operator overload for PipelineParameter, Output and PipelineExpression, this will lead to
    exception raised when using Python keyword 'in'. This function checks type first and execute
    comparison with id() for custom class.
    """
    for item in arr:
        if type(obj) != type(item):
            continue
        if type(obj) in basic_python_type:
            if obj == item:
                return True
        else:
            if id(obj) == id(item):
                return True
    return False


def get_pipeline_response_content(pipeline_response):
    """Returns PipelineResponse object content. In swagger 3.0, we wrap response and deserialized as a PipelineResponse
    obj if cls is not None. This is similar to raw=True in swagger 2.0. And then we parse response content which is
    parsed implicitly in ClientRawResponse in swagger 2.0.

    :param pipeline_response: PipelineResponse object.
    :type pipeline_response: PipelineResponse
    """
    return pipeline_response.http_request.http_response.internal_response.content


def start_a_local_run(workspace, experiment_name, files, run_id=None):
    import urllib3
    from azureml._restclient.clientbase import ClientBase
    from azureml._execution._commands import _raise_request_error, _get_common_headers

    service_context = workspace.service_context
    service_arm_scope = "{}/experiments/{}".format(service_context._get_workspace_scope(), experiment_name)
    service_address = service_context._get_execution_url()

    headers = _get_common_headers()
    auth_header = workspace._auth_object.get_authentication_header()
    headers.update(auth_header)

    uri = service_address + "/execution/v1.0" + service_arm_scope + "/localrun"

    # Unfortunately, requests library does not take Queryparams nicely.
    # Appending run_id_query to the url for service to extract from it.
    run_id_query = urllib3.request.urlencode({"runId": run_id})
    uri += "?" + run_id_query

    response = ClientBase._execute_func(requests.post, uri, files=files, headers=headers)
    _raise_request_error(response, "starting run")
    return response
