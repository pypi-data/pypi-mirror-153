# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import os
import uuid
import tempfile
import shutil
from datetime import datetime
from pathlib import Path

from azure.ml.component._util._loggerfactory import _LoggerFactory, track

_logger = None


def _get_logger():
    global _logger
    if _logger is not None:
        return _logger
    _logger = _LoggerFactory.get_logger()
    return _logger


class ComponentSnapshotCache(object):
    """
    Cache component snapshot

    Cache component snapshot in snapshot_cache_dir by component_id, and clean up snapshots
    which not be accessed for max unused time when exceed max number of caches
    """

    def __init__(self, snapshot_cache_dir, max_cache_snapshot, max_unused_time):
        """
        Init ComponentSnapshotCache

        :param snapshot_cache_dir: Snapshot cache dir
        :type snapshot_cache_dir: str
        :param max_cache_snapshot: max num of snapshot exists in snapshot_cache_dir
        :type max_cache_snapshot: int
        :param max_unused_time: max unused time of snapshot, if snapshot not be accessed for max unused time
                                and exceed max number of caches, will remove this snapshot.
        :type max_unused_time: int
        """
        self.snapshot_cache_dir = snapshot_cache_dir
        self.max_cache_snapshot = max_cache_snapshot
        self.max_unused_time = max_unused_time
        Path(self.snapshot_cache_dir).mkdir(parents=True, exist_ok=True)

    @track()
    def prepare_snapshot_from_cache(self, component_id, target_dir):
        """
        Copy snapshot that exists in cache to target_dir

        If snapshot exists in cache, avoiding multi operation same snapshot at same time,
        will rename it to temp folder and copy to target_dir and update snapshot modify time.
        If snapshot not exists in cache, will return false.

        :param component_id: component id
        :type component_id: str
        :param target_dir: snapshot target path
        :type target_dir: str
        :return command_result: If snapshot exists in cache and move to target_dir
                                success return True, else return False.
        :rtype bool
        """
        snapshot_path = os.path.join(self.snapshot_cache_dir, component_id)
        if self.snapshot_exist_in_cache(component_id):
            if os.path.exists(target_dir):
                shutil.rmtree(target_dir, ignore_errors=True)
            # copy snapshot from cache to target dir
            try:
                # Copy snapshot to target_dir, and update snapshot modify time.
                os.utime(snapshot_path, (datetime.now().timestamp(), datetime.now().timestamp()))
                shutil.copytree(snapshot_path, target_dir)
                _LoggerFactory.add_track_dimensions(_get_logger(), {"cached": True})
                return True
            except FileNotFoundError:
                # If raise FileNotFoundError, means snapshot was cleaned up when copy to target dir,
                # then will down load snapshot to target_dir.
                _LoggerFactory.add_track_dimensions(_get_logger(), {"cached": False})
                return False
        _LoggerFactory.add_track_dimensions(_get_logger(), {"cached": False})
        return False

    def cache_snapshot(self, component_id, target_dir):
        """
        Cache snapshot

        Copying target_dir to snapshot dir, to avoid multi operation for same snapshot at same time,
        will copy target_dir to temp folder and rename it.

        :param component_id: component id
        :type component_id: str
        :param target_dir: snapshot store path
        :type target_dir: str
        """
        # copy snapshot to snapshot cache dir.
        try:
            # Copying snapshot to temp dir than using os.rename move to snapshot cache dir.
            # It avoids multi-thread/process operating on same snapshot in snapshot cache dir at same time.
            # If os.rename raise FileExistsError, it means the same snapshots is in cache, so delete temp snapshot.
            # If os.rename raise PermissionError, snapshot dir is not access avaliable.
            snapshot_dir = os.path.join(self.snapshot_cache_dir, component_id)
            temp_path = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))
            shutil.copytree(target_dir, temp_path)
            os.rename(temp_path, snapshot_dir)
        except (FileExistsError, PermissionError, OSError):
            # On Windows, if dst exists a FileExistsError is always raised.
            # On Unix, if dst is a non-empty directory, an OSError is raised.
            # If dst is being used by another process will raise PermissionError.
            # https://docs.python.org/3/library/os.html#os.rename
            if os.path.exists(temp_path):
                shutil.rmtree(temp_path, ignore_errors=True)

    def clean_up_snapshot_cache(self):
        """
        Clean up snapshot cache

        If exceed max number of caches, will clean up snapshot which not accessed for max unused time.
        """
        # Get dir list sorted by modify time.
        delete_time = datetime.now().timestamp() - self.max_unused_time
        limit = len(self.list_snapshots()) - self.max_cache_snapshot
        if limit <= 0:
            return
        dir_list = self.list_oldest_snapshots_before(timestamp=delete_time, limit=limit)
        for delete_snapshot in dir_list:
            # The snapshot which before delete_time will be deleted
            # to avoid deleting snapshots which cached during cache delete.
            if os.path.getmtime(delete_snapshot) <= delete_time:
                self._atomic_remove_folder(delete_snapshot)

    def list_snapshots(self):
        """
        List snapshots in cache

        Return list of snapshot path in cache.
        """
        dir_list = [os.path.join(self.snapshot_cache_dir, snapshot)
                    for snapshot in os.listdir(self.snapshot_cache_dir)]
        return dir_list

    def list_oldest_snapshots_before(self, timestamp, limit):
        """
        List oldest snapshots before timestamp

        :param timestamp: list snapshots which modify time before timestamp
        :type timestamp: float
        :param limit: Number of the oldest snapshots before timestamp
        :type limit: int
        :return oldest_snapshots: List of oldest snapshots before timestamp
        :rtype List
        """
        dir_list = self.list_snapshots()
        if limit <= 0:
            return []
        before_timestamp_snapshots = [snapshot for snapshot in dir_list if os.path.getctime(snapshot) <= timestamp]
        oldest_snapshots = sorted(before_timestamp_snapshots, key=lambda x: os.path.getmtime(x))[0: limit]
        return oldest_snapshots

    def get_snapshot_path_by_component_id(self, component_id):
        if self.snapshot_exist_in_cache(component_id):
            return os.path.join(self.snapshot_cache_dir, component_id)
        else:
            return None

    def snapshot_exist_in_cache(self, component_id):
        component_cache_path = os.path.join(self.snapshot_cache_dir, component_id)
        if os.path.exists(component_cache_path):
            if os.listdir(component_cache_path):
                return True
            else:
                self._atomic_remove_folder(component_cache_path)
        return False

    @staticmethod
    def _atomic_remove_folder(delete_folder):
        # Using os.rename to move snapshot to temp dir and delete,
        # avoiding multi operations on same snapshot at same time.
        try:
            # https://docs.python.org/3/library/tempfile.html#tempfile.TemporaryFile
            # It's said, code should not rely on a temporary file created using this function having
            # or not having a visible name in the file system. So, using uuid to create tempdir name.
            temp_path = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))
            os.rename(delete_folder, temp_path)
            shutil.rmtree(temp_path, ignore_errors=True)
        except FileNotFoundError:
            # If raise FileNotFoundError, delete_snapshot may be deleted.
            pass
