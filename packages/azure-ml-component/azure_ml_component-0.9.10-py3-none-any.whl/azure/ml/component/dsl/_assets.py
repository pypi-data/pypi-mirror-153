# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from azure.ml.component._util._loggerfactory import _PUBLIC_API, track
from azure.ml.component._dataset import _FeedDataset
from azure.ml.component._restclients.service_caller_factory import _DesignerServiceCallerFactory

from typing import Callable


@track(activity_type=_PUBLIC_API, activity_name="dsl_load_component")
def load_component(workspace, name, *, version=None, feed=None, registry_name=None) -> Callable[..., 'Component']:
    """Load component to workspace from a specified feed.

    :param workspace: The target workspace to load component to.
    :type workspace: azureml.core.Workspace
    :param name: The name of the component.
    :type name: str
    :param version: The version of the component.
    :type version: str
    :param feed: The name of the feed you want to load component from.
    :type feed: str
    :param registry_name: The registry name of component.
    :type registry_name: str

    :return: A function that can be called with parameters to get a :class:`azure.ml.component.Component`
    :rtype: function
    """
    from azure.ml.component._core._component_definition import CommandComponentDefinition
    from azure.ml.component import Component
    from azure.ml.component.component import _ComponentLoadSource

    definition = CommandComponentDefinition.get(workspace, name, version, feed_name=feed, registry_name=registry_name)
    definition._load_source = _ComponentLoadSource.REGISTERED

    return Component._component_func_from_definition(definition)


@track(activity_type=_PUBLIC_API, activity_name="dsl_load_dataset")
def load_dataset(workspace, name, *, version=None, feed=None) -> _FeedDataset:
    """Load data to workspace from a specified feed.

    :param workspace: The target workspace to load data to.
    :type workspace: azureml.core.Workspace
    :param name: The name of the data.
    :type name: str
    :param version: The version of the data.
    :type version: str
    :param feed: The name of the feed you want to load data from.
    :type feed: str

    :return: feed data
    :rtype: azure.ml.component._FeedDataset
    """
    service_caller = _DesignerServiceCallerFactory.get_instance(workspace)
    data_info = service_caller._get_data_set_by_name(name, version, feed)
    return _FeedDataset(data_info)


@track(activity_type=_PUBLIC_API, activity_name="dsl_load_model")
def load_model(workspace, name, *, version=None, feed=None) -> _FeedDataset:
    """Load model to workspace from a specified feed.

    :param workspace: The target workspace to load model to.
    :type workspace: azureml.core.Workspace
    :param name: The name of the model.
    :type name: str
    :param version: The version of the model.
    :type version: str
    :param feed: The name of the feed you want to load model from.
    :type feed: str

    :return: feed model
    :rtype: azure.ml.component._FeedDataset
    """
    service_caller = _DesignerServiceCallerFactory.get_instance(workspace)
    model_info = service_caller._get_model_by_name(name, version, feed)
    return _FeedDataset(model_info)
