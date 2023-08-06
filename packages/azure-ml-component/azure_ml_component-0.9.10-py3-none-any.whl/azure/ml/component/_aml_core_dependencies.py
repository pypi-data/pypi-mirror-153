# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

try:
    from azureml._base_sdk_common._docstring_wrapper import experimental
    from azureml._restclient.constants import SNAPSHOT_MAX_FILES, SNAPSHOT_BATCH_SIZE, ONE_MB, SNAPSHOT_MAX_SIZE_BYTES
    from azureml._project.project_manager import _get_tagged_image
except BaseException:
    from azureml.exceptions import UserErrorException

    raise UserErrorException('Failed to import azureml-core dependencies. '
                             'Try run "pip install \'azureml-core>=1.19.0\'" to update azureml-core.')
# TODO: move all azureml-core dependencies here
