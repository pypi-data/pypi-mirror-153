# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import os
import json
import time
import tempfile
import hashlib
from threading import Lock
from pathlib import Path
from abc import ABC, abstractmethod
from azureml.core import Datastore
from azure.ml.component._util._loggerfactory import _LoggerFactory
from azure.ml.component._version import VERSION

COMPONENT_CACHE_ENV_VARIABLE = "AZUREML_COMPONENT_ANONYMOUS_COMPONENT_CACHE"
COMPONENT_EXPIRE_ENV_VARIABLE = "AZUREML_COMPONENT_ANONYMOUS_COMPONENT_CACHE_EXPIRE_SECONDS"
_logger = _LoggerFactory.get_logger()


class _CachedItem:

    def __init__(self, item, expired_time_in_seconds=60):
        """CachedItem.

        :param item: The instance of cached object
        :type item: obj
        :param expired_time_in_seconds: expired time in seconds
        :type expired_time_in_seconds: int
        """
        self.item = item
        self.expired_time_in_seconds = expired_time_in_seconds
        self.cache_time = time.time()

    def is_expired(self):
        return time.time() - self.cache_time > self.expired_time_in_seconds


class _GeneralCache:
    """General cache for internal use."""
    _cache_dict = {}

    @classmethod
    def set_item(cls, key, item, expired_time_in_seconds=60):
        cls._cache_dict[key] = _CachedItem(item, expired_time_in_seconds)

    @classmethod
    def get_item(cls, key):
        cached = cls._cache_dict.get(key, None)

        if cached is None:
            return None

        if cached.is_expired():
            del cls._cache_dict[key]
            return None
        else:
            return cached

    @classmethod
    def delete_item(cls, key):
        if key in cls._cache_dict:
            del cls._cache_dict[key]


class DatastoreCache:
    """Datastore cache for internal use."""
    datastore_cache_expires_in_seconds = 3600
    # for None item, we only cache it for 1 minute
    datastore_cache_expires_in_seconds_for_none = 60

    @classmethod
    def _cache_key(cls, workspace, datastore_name):
        return 'datastore_{}_{}'.format(workspace._workspace_id, datastore_name)

    @classmethod
    def set_item(cls, workspace, datastore, datastore_name, expired_time_in_seconds=None):
        cache_key = cls._cache_key(workspace, datastore_name)
        if expired_time_in_seconds is None:
            if datastore is None:
                expired_time_in_seconds = cls.datastore_cache_expires_in_seconds_for_none
            else:
                expired_time_in_seconds = cls.datastore_cache_expires_in_seconds
        _GeneralCache.set_item(cache_key, datastore, expired_time_in_seconds)

    @classmethod
    def get_item(cls, workspace, datastore_name):
        cache_key = cls._cache_key(workspace, datastore_name)
        cached_item = _GeneralCache.get_item(cache_key)
        if cached_item is None:
            try:
                datastore = Datastore(workspace, datastore_name)
            except Exception:
                datastore = None
            cls.set_item(workspace, datastore, datastore_name)
            return datastore
        else:
            return cached_item.item


class ComputeTargetCache:
    """Compute target cache for internal use."""
    compute_cache_expires_in_seconds = 3600
    # for None item, we only cache it for 1 minute
    compute_cache_expires_in_seconds_for_none = 60

    @classmethod
    def _cache_key(cls, workspace, compute_name):
        return 'compute_{}_{}'.format(workspace._workspace_id, compute_name)

    @classmethod
    def set_item(cls, workspace, compute, compute_name, expired_time_in_seconds=None):
        cache_key = cls._cache_key(workspace, compute_name)
        if expired_time_in_seconds is None:
            if compute_name is None:
                expired_time_in_seconds = cls.compute_cache_expires_in_seconds_for_none
            else:
                expired_time_in_seconds = cls.compute_cache_expires_in_seconds
        _GeneralCache.set_item(cache_key, compute, expired_time_in_seconds)

    @classmethod
    def get_item(cls, workspace, compute_name):
        cache_key = cls._cache_key(workspace, compute_name)
        return _GeneralCache.get_item(cache_key)

    @classmethod
    def delete_item(cls, workspace, compute_name):
        cache_key = cls._cache_key(workspace, compute_name)
        _GeneralCache.delete_item(cache_key)

    @classmethod
    def get_cached_item_count(cls, workspace):
        prefix = cls._cache_key(workspace, '')
        return len([key for key in _GeneralCache._cache_dict.keys() if key.startswith(prefix)])


class DiskCache(ABC):
    """
    Base disk cache class represents a disk and file backend cache.
    As a Cache, it supports a familiar Python mapping interface with additional cache
    """
    DEFAULT_DISK_CACHE_DIRECTORY = os.path.join(tempfile.gettempdir(), "azure-ml-component", VERSION)
    # Expired time in seconds
    EXPIRE = None
    # Max cached item in disk
    MAX_LIMIT = None
    _CACHE_ENV_VARIABLE = None
    _EXPIRE_ENV_VARIABLE = None
    _UNSPECIFIED = object()
    _instance_lock = Lock()
    _instance = None
    _cache_in_memory = {}

    def __new__(cls, *args, **kwargs):
        """Singleton creation disk cache"""
        if cls._instance is None:
            with cls._instance_lock:
                if cls._instance is None:
                    cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, cache_directory=None):
        self._cache_directory = cache_directory or self.DEFAULT_DISK_CACHE_DIRECTORY
        Path(self._cache_directory).mkdir(exist_ok=True, parents=True)
        self._remove_expire()

    @property
    def cache_directory(self):
        """Cache directory path."""
        return self._cache_directory

    @property
    def expire(self):
        """Expire time in seconde."""
        if self._EXPIRE_ENV_VARIABLE and self._EXPIRE_ENV_VARIABLE in os.environ:
            expire = os.environ.get(self._EXPIRE_ENV_VARIABLE, None)
            try:
                expire = int(expire)
                return expire
            except Exception as e:
                _logger.debug("Failed to convert the environment variable {self._EXPIRE_ENV_VARIABLE} to int, {e}.")
                return self.EXPIRE
        else:
            return self.EXPIRE

    @classmethod
    def get_disk_cache(cls, cache_directory=None):
        if not cls._CACHE_ENV_VARIABLE or os.environ.get(cls._CACHE_ENV_VARIABLE, "true").lower() == "true":
            return cls(cache_directory=cache_directory)
        else:
            return None

    def _load_disk_cache(self, key):
        """Load disk cache to memory"""
        if key not in os.listdir(self.cache_directory):
            _logger.debug(f"Cannot find {key} in {self.cache_directory}.")
            return None

        with open(os.path.join(self.cache_directory, key), 'r') as f:
            try:
                self._cache_in_memory[key] = f.read()
                return self._cache_in_memory[key]
            except Exception as e:
                _logger.debug(f"When load the disk cache in {self.cache_directory} failed, {e}")
                return None

    def _dump_disk_cache(self, key, value):
        """Dump disk cache to memory"""
        with open(os.path.join(self.cache_directory, key), 'w') as f:
            f.write(value)

    @abstractmethod
    def _serialize(self, data):
        """Serialize the object."""

    @abstractmethod
    def _deserialize(self, data):
        """Parse a str to object."""

    def set(self, key, value):
        """Set `key` and `value` item in cache."""
        cache_value = self._serialize(value)
        self._cache_in_memory[key] = cache_value
        self._dump_disk_cache(key, cache_value)
        return value

    def __setitem__(self, key, value):
        """Set corresponding `value` for `key` in disk cache."""
        return self.set(key, value)

    def get(self, key, default=None):
        """Retrieve value from cache. If `key` is missing, return `default`"""
        cache_item = self._cache_in_memory.get(key, None) or self._load_disk_cache(key)
        if cache_item:
            try:
                if self.expire and \
                        time.time() > os.path.getmtime(os.path.join(self.cache_directory, key)) + self.expire:
                    _logger.debug(
                        f"{key} in {self.__class__.__name__} is expired, return the default value {default}.")
                    return default
                _logger.debug(f"Use {key} in the {self.__class__.__name__}.")
                return self._deserialize(cache_item)
            except Exception as e:
                _logger.debug(f"Failed using {key} in the {self.__class__.__name__}, {e}")
                self._cache_in_memory.pop(key, None)
                return default
        else:
            return default

    def __getitem__(self, key):
        """Return corresponding value for `key` from cache."""
        value = self.get(key, default=self._UNSPECIFIED)
        if value is self._UNSPECIFIED:
            raise KeyError(key)
        return value

    def _remove_cache_item(self, key):
        try:
            file_path = Path(self.cache_directory, key)
            if file_path.exists() and file_path.is_file():
                file_path.unlink()
        except Exception as e:
            _logger.debug(f"Remove the cache item {key} failed, {e}")

    def _remove_expire(self):
        """Remove expired items from cache."""

        def get_file_modify_time(file_path):
            """Return modify time of file, if file not exist return None."""
            try:
                return os.path.getmtime(file_path)
            except Exception:
                # When file does not exist, os.path.getmtime raise error.
                return None

        if not self.expire and not self.MAX_LIMIT:
            return
        now = time.time()
        removed_cache_item = []
        file_mtime_mapping = {item: get_file_modify_time(os.path.join(self.cache_directory, item))
                              for item in os.listdir(self.cache_directory)}
        file_mtime_mapping = {k: v for k, v in file_mtime_mapping.items() if v is not None}
        ordered_cached_list = dict(sorted(file_mtime_mapping.items(), key=lambda kv: kv[1])).keys()
        if self.MAX_LIMIT and len(ordered_cached_list) > self.MAX_LIMIT:
            removed_cache_item = ordered_cached_list[self.MAX_LIMIT:]
            ordered_cached_list = ordered_cached_list[0: self.MAX_LIMIT]
        if self.expire:
            removed_cache_item.extend(
                [item for item in ordered_cached_list if file_mtime_mapping[item] + self.expire < now])
        for item in removed_cache_item:
            self._remove_cache_item(item)
            self._cache_in_memory.pop(item, None)

    def clean(self):
        """Remove all items from cache."""
        # Remove cache in memory
        self._cache_in_memory = {}
        # Remove cache in disk
        for item in os.listdir(self.cache_directory):
            self._remove_cache_item(item)


class RunsettingParametersDiskCache(DiskCache):
    """Disk cache of runsetting parameters. The expire time of the run settings parameters is 1 day."""
    DEFAULT_DISK_CACHE_DIRECTORY = os.path.join(DiskCache.DEFAULT_DISK_CACHE_DIRECTORY, "runsetting_parameters")
    KEY = "runsetting_parameters"
    EXPIRE = 60 * 60 * 24

    def _serialize(self, data):
        # The type of runsetting_parameters is dict{list[RunSettingParameter]}
        serialized = {}
        for k, v in data.items():
            serialized[k] = []
            for item in v:
                serialized[k].append(item.serialize())
        return json.dumps(serialized)

    def _deserialize(self, data):
        from azure.ml.component._restclients.designer.models._models_py3 import RunSettingParameter

        deserialized = {}
        for k, v in json.loads(data).items():
            deserialized[k] = []
            for item in v:
                deserialized[k].append(RunSettingParameter.deserialize(item))
        return deserialized

    def get(self):
        """Get run setting parameters from disk cache."""
        return super(RunsettingParametersDiskCache, self).get(key=self.KEY, default=None)

    def set(self, value):
        """Set run setting parameters to disk cache."""
        return super(RunsettingParametersDiskCache, self).set(key=self.KEY, value=value)


class RegisteredComponentDiskCache(DiskCache):
    """Disk cache of registered pipeline component dto. The expire time of the component dto is 1 week."""
    DEFAULT_DISK_CACHE_DIRECTORY = os.path.join(DiskCache.DEFAULT_DISK_CACHE_DIRECTORY, "registered_component")
    EXPIRE = 7 * 24 * 60 * 60
    _CACHE_ENV_VARIABLE = COMPONENT_CACHE_ENV_VARIABLE
    _EXPIRE_ENV_VARIABLE = COMPONENT_EXPIRE_ENV_VARIABLE

    @staticmethod
    def _convert_register_params_to_cache_key(register_params):
        return hashlib.sha1(json.dumps(register_params, sort_keys=True).encode("utf-8")).hexdigest()

    def _serialize(self, data):
        return json.dumps(data.serialize())

    def _deserialize(self, data):
        from azure.ml.component._restclients.service_caller_factory import _DesignerServiceCallerFactory
        caller = _DesignerServiceCallerFactory.get_instance(workspace=None)
        return caller._caller.component._deserialize('ModuleDto', json.loads(data))

    def get(self, key, default=None):
        """Get registered component from disk cache."""
        key = self._convert_register_params_to_cache_key(key)
        return super(RegisteredComponentDiskCache, self).get(key=key, default=default)

    def set(self, key, value):
        """Set registered component to disk cache."""
        key = self._convert_register_params_to_cache_key(key)
        return super(RegisteredComponentDiskCache, self).set(key=key, value=value)


class RegisteredPipelineComponentDiskCache(DiskCache):
    """Disk cache of registered component dto. The expire time of the component dto is 1 week."""
    DEFAULT_DISK_CACHE_DIRECTORY = os.path.join(DiskCache.DEFAULT_DISK_CACHE_DIRECTORY,
                                                "registered_pipeline_component")
    EXPIRE = 7 * 24 * 60 * 60
    _CACHE_ENV_VARIABLE = COMPONENT_CACHE_ENV_VARIABLE
    _EXPIRE_ENV_VARIABLE = COMPONENT_EXPIRE_ENV_VARIABLE

    @staticmethod
    def _convert_register_params_to_cache_key(workspace, generate_request):
        cache_key = {
            "subscription_id": workspace._subscription_id,
            "resource_group_name": workspace._resource_group,
            "workspace_name": workspace.name,
            "generate_request": generate_request.serialize()
        }
        return hashlib.sha1(json.dumps(cache_key, sort_keys=True).encode("utf-8")).hexdigest()

    def _serialize(self, data):
        return json.dumps(data.serialize())

    def _deserialize(self, data):
        from azure.ml.component._restclients.service_caller_factory import _DesignerServiceCallerFactory
        caller = _DesignerServiceCallerFactory.get_instance(workspace=None)
        return caller._caller.pipeline_component._deserialize('ModuleDto', json.loads(data))

    def get(self, workspace, generate_request, default=None):
        """Get registered component from disk cache."""
        key = self._convert_register_params_to_cache_key(workspace, generate_request)
        return super(RegisteredPipelineComponentDiskCache, self).get(key=key, default=default)

    def set(self, workspace, generate_request, value):
        """Set registered component to disk cache."""
        key = self._convert_register_params_to_cache_key(workspace, generate_request)
        return super(RegisteredPipelineComponentDiskCache, self).set(key=key, value=value)
