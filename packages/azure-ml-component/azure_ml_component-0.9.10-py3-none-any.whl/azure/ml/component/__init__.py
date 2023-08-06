# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Contains core functionality for Azure Machine Learning components.

Azure Machine Learning components allow you to create reusable machine learning workflows that can be used as a
template for your machine learning scenarios. This package contains the core functionality for working with
Azure ML components.

A machine learning components can also be constructed by a collection of :class:`azure.ml.component.Component` object
that can sequenced and parallelized, or be created with explicit dependencies.

You can create and work with components in a Jupyter Notebook or any other IDE with the Azure ML SDK installed.
"""
import logging

from .component import Component
from .pipeline import Pipeline
# from .endpoint import PipelineEndpoint
from .run import Run
from .run_settings import RunSettings, PipelineRunSettings
from .environment import Environment
from ._version import VERSION

# We are not using __name__ since all logger starts with "azure" will be recognized as azure CLI and
# we don't want this error shown in CLI.
module_logger = logging.getLogger("azureml.component")

__all__ = [
    'Component',
    'Pipeline',
    'Run',
    'RunSettings',
    'PipelineRunSettings',
    'Environment'
]

if VERSION.startswith("0.1"):
    # preview version will start with 0.1, print a warning for user
    module_logger.warning("You are using a preview version {} of azure-ml-component package, which might "
                          "contain unstable features. Please use following guidance here: "
                          "http://aka.ms/azureml-component-getting-started. "
                          "You can run `pip install azure-ml-component --upgrade` to get "
                          "latest stable version.".format(VERSION))
