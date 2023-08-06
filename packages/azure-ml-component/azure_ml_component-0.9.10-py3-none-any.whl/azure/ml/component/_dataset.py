# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import Union

from azure.ml.component._restclients.service_caller_factory import _DesignerServiceCallerFactory
from azure.ml.component._restclients.designer.models import DataInfo, ModelDto
from azure.ml.component._util._cache import DatastoreCache
from azureml.core import Workspace
from azureml.data.data_reference import DataReference
from ._util._utils import _sanitize_python_variable_name

_cached_global_dataset = None


class _GlobalDataset(DataReference):
    """
    A class that represents a global dataset provided by AzureML.
    """
    def __init__(self, workspace: Workspace, data_store_name: str, relative_path: str):
        self.data_store_name = data_store_name
        self.relative_path = relative_path
        super().__init__(datastore=DatastoreCache.get_item(workspace, datastore_name=data_store_name),
                         data_reference_name=_sanitize_python_variable_name(relative_path),
                         path_on_datastore=relative_path)


def get_global_dataset_by_path(workspace: Workspace, name, path):
    """
    Retrieve global dataset provided by AzureML using name and path.

    This is intended only for internal usage and *NOT* part of the public APIs.
    Please be advised to not rely on its current behaviour.
    """
    service_caller = _DesignerServiceCallerFactory.get_instance(workspace)
    global _cached_global_dataset
    if _cached_global_dataset is None:
        all_dataset = service_caller.list_datasets()
        _cached_global_dataset = [d for d in all_dataset if d.aml_data_store_name == 'azureml_globaldatasets']
    dataset = next((x for x in _cached_global_dataset if x.relative_path == path), None)
    if dataset is None:
        raise ValueError('dataset not found with path: {}'.format(path))
    return _GlobalDataset(workspace, dataset.aml_data_store_name, dataset.relative_path)


class _FeedDataset(object):
    """
    A class that represents a dataset load from feed.
    """

    def __init__(self, data_info: Union[DataInfo, ModelDto]):
        self.name = data_info.name
        self.feed = data_info.feed_name
        self.arm_id = data_info.arm_id
