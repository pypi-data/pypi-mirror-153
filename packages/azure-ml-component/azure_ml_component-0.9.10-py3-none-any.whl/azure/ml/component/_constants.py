# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from enum import Enum


class DataStoreMode(str, Enum):
    """DataStore mode Enum class."""

    MOUNT = "mount"
    DOWNLOAD = "download"
    UPLOAD = "upload"
    DIRECT = "direct"
    LINK = "link"
    HDFS = "hdfs"
