# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
SLEEP_INTERVAL = 5
MODULE_PROPERTY_NAME = 'azureml.moduleid'
MOCK_PARALLEL_DRIVER = '_mock_parallel_driver.py'
COMMAND_DRIVER = '_command_driver.py'

# File/folder name
OUTPUT_DIR_NAME = 'outputs'
IMAGE_DIR_NAME = 'image_logs'
CONDA_DIR_NAME = 'conda_logs'
SCRIPTE_DIR_NAME = 'scripts'
EXECUTION_LOGFILE = 'excutionlogs.txt'

# Input/output/script path in container
LINUX_CONTAINER_MOUNT_PATH = '/mnt/'
LINUX_CONTAINER_INPUT_PATH = '/mnt/input'
LINUX_CONTAINER_OUTPUT_PATH = '/mnt/{}'.format(OUTPUT_DIR_NAME)
LINUX_CONTAINER_MOUNT_SCRIPTS_PATH = '/mnt/scripts'

WINDOWS_CONTAINER_MOUNT_PATH = 'c:\\'
WINDOWS_CONTAINER_INPUT_PATH = 'c:\\input'
WINDOWS_CONTAINER_OUTPUT_PATH = 'c:\\{}'.format(OUTPUT_DIR_NAME)
WINDOWS_CONTAINER_MOUNT_SCRIPTS_PATH = 'c:\\scripts'

# Prefix of component run log
RUN_PREPARE_LOG = 'Run prepare stage'
RUN_EXEC_LOG = 'Run execute stage'
RUN_RELEASE_LOG = 'Run release stage'
USER_ERROR_MSG = 'Executing script failed with a non-zero exit code; see the %s for details.'

# Keyword of visualizer
PARENT_NODE_ID = '@parent'
NODE_LOG_KEY = '70_driver_log.txt'
PARENT_LOG_KEY = 'logs/azureml/executionlogs.txt'

# Pipeline run keyword
NODE_ID = 'node_id'
STEP_PREFIX = 'prefix'
WORKING_DIR = 'working_dir'
RUN_ID = 'run_id'

# It's a flag for CommandExecution to test execution environment is wsl/container.
# If it in os.environ, CommandExecution will think current environment is wsl/container.
TEST_COMMAND_EXECUTE_IN_WSL_OR_CONTAINER = 'test_in_wsl_or_container'
