# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import os
import json
import shutil
from azureml._base_sdk_common.merkle_tree import DirTreeNode
from azureml._base_sdk_common.project_snapshot_cache import ContentSnapshotCache
from ._utils import _EMPTY_GUID, get_file_path_hash

PROJECT_CONTENT_CACHE_LATEST_SNAPSHOT_FILE = "latestsnapshot"


class SnapshotCache(ContentSnapshotCache):
    def __init__(self, service_context):
        self.service_context = service_context

    def _get_snapshot_cache_file(self, file_or_folder_path):
        return os.path.join(
            self.get_cache_directory_by_path(file_or_folder_path),
            PROJECT_CONTENT_CACHE_LATEST_SNAPSHOT_FILE)

    def get_latest_snapshot_by_path(self, file_or_folder_path):
        """Return the latest cache of file_or_folder_path in local, if no cache, return an empty snapshot object
        """
        snapshot_cache_file = self._get_snapshot_cache_file(file_or_folder_path)
        if not os.path.isfile(os.path.abspath(snapshot_cache_file)):
            # return an empty snapshot
            return DirTreeNode(), _EMPTY_GUID
        else:
            with open(snapshot_cache_file, 'r') as json_data:
                d = json.load(json_data)
                root = d['root']
                snapshot_id = d['snapshot_id']
                node = DirTreeNode()
                node.load_root_object_from_json_string(root)
        return node, snapshot_id

    def update_cache(self, snapshot_dto, file_or_folder_path):
        directory_path = self.get_cache_directory_by_path(file_or_folder_path)
        try:
            if not os.path.exists(directory_path):
                os.makedirs(directory_path)
            snapshot_cache_file = self._get_snapshot_cache_file(file_or_folder_path)
            with open(snapshot_cache_file, 'w+') as f:
                json.dump(snapshot_dto.__dict__, f)
        except FileExistsError:
            # concurrent snapshots competing for file, first can update cache
            pass

    def get_cache_directory_by_path(self, file_or_folder_path):
        return os.path.join(
            self.get_cache_directory(),
            get_file_path_hash(file_or_folder_path))

    def clear_all_cache(self):
        """This will remove all the cached snapshots in current workspace.
        """
        cache_dir = self.get_cache_directory()
        if os.path.exists(cache_dir):
            shutil.rmtree(cache_dir)

    def remove_cache(self, file_or_folder_path):
        latest_snapshot_cache_file = self._get_snapshot_cache_file(file_or_folder_path)
        if os.path.exists(latest_snapshot_cache_file):
            os.remove(latest_snapshot_cache_file)
