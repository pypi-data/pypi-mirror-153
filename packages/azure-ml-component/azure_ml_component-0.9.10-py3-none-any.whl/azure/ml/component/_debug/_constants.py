# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

from pathlib import Path

CONDA_FILE_NAME = 'conda.yaml'
DOCKER_FILE_NAME = 'Dockerfile'
DATA_REF_PREFIX = '$AZUREML_DATAREFERENCE_'

SUBSCRIPTION_KEY = 'subscriptions'
RESOURCE_GROUP_KEY = 'resourcegroups'
WORKSPACE_KEY = 'workspaces'
EXPERIMENT_KEY = 'experiments'
ID_KEY = 'id'
DRAFT_KEY = 'Normal'
RUN_KEY = 'runs'

INPUT_DIR = Path(__file__).parent.parent / 'dsl' / 'data' / 'inputs'
VSCODE_DIR = '.vscode'
CONTAINER_DIR = '.devcontainer'
LAUNCH_CONFIG = 'launch.json'
CONTAINER_CONFIG = 'devcontainer.json'
OUTPUT_DIR = 'outputs'
DIR_PATTERN = r'[^a-zA-Z0-9]'
GIT_IGNORE = '.gitignore'
DEBUG_FOLDER = '.debug'

DOCKERFILE_TEMPLATE = '''
FROM {image_name}
ADD conda.yaml conda.yaml
RUN conda env create -f conda.yaml
'''
