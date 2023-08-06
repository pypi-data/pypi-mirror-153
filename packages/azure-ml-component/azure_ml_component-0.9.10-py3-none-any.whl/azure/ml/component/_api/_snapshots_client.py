# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import logging
import os
import json
import uuid
import tempfile
from functools import reduce
from uuid import UUID
import requests
from tqdm.auto import tqdm
import time

from azureml._common.async_utils import TaskQueue
from azureml._common.exceptions import AzureMLException
from azureml._file_utils import upload_blob_from_stream, download_file
from azureml.exceptions import SnapshotException, UserErrorException, ProjectSystemException
from azureml._base_sdk_common.snapshot_dto import SnapshotDto
from azureml._base_sdk_common.merkle_tree_differ import compute_diff
from azureml._base_sdk_common.tracking import global_tracking_info_registry
from azureml._base_sdk_common.common import get_http_exception_response_string
from azureml._base_sdk_common.merkle_tree import DirTreeJsonEncoder, create_merkletree, DirTreeNode
from azureml._restclient.clientbase import execute_func, ClientBase

from azure.ml.component._util._loggerfactory import track, _LoggerFactory
from azure.ml.component._util._telemetry import WorkspaceTelemetryMixin
from azure.ml.component._api._utils import create_session_with_retry
from azure.ml.component._util._utils import TimerContext, str2bool
from ._component_snapshot import ADDITIONAL_INCLUDES
from ._utils import _EMPTY_GUID
from ._snapshot_cache import SnapshotCache
from ._snapshots_client_core import (
    SnapshotsClient as BaseSnapshotsClient,
    MAX_FILES_SNAPSHOT_UPLOAD_PARALLEL,
    AZUREML_SNAPSHOT_DEFAULT_TIMEOUT,
    TIMEOUT,
    RETRY_LIMIT,
    BACKOFF_START,
    DirTreeJsonEncoderV2
)
from .._aml_core_dependencies import SNAPSHOT_MAX_FILES, ONE_MB

SNAPSHOT_MAX_SIZE_BYTES = 2 * 1024 * ONE_MB
AML_COMPONENT_SNAPSHOT_WITHOUT_DOWNLOAD_PROGRESS_BAR = "AML_COMPONENT_SNAPSHOT_WITHOUT_DOWNLOAD_PROGRESS_BAR"
_logger = None


def _get_logger():
    global _logger
    if _logger is not None:
        return _logger
    _logger = _LoggerFactory.get_logger()
    return _logger


def flatten_download_files(downloaded_files_json, path):
    """
    Flatten download files according to json response for asset store
    :param downloaded_files_json:
    :type downloaded_files_json: dict
    :param path: target directory
    :type path: str
    :return: flattened_download_files
    """
    flattened_download_files = []
    for file_name, file_info in downloaded_files_json.items():
        if file_info['type'] == "Directory":
            flattened_download_files.extend(flatten_download_files(file_info["children"],
                                                                   os.path.join(path, file_name)))
        else:
            sas_url = file_info["sasUrl"]
            temp_path = os.path.join(path, file_name)
            # exclude additional includes
            if not temp_path.endswith(ADDITIONAL_INCLUDES):
                flattened_download_files.append([temp_path, sas_url])
    return flattened_download_files


def validate_snapshot_size(size, component_file, raise_on_validation_failure, logger):
    """Validate size of snapshot.

    :param size: Size of component snapshot.
    :param component_file: The component spec file.
    :param raise_on_validation_failure: Raise error if validation failed.
    """
    if size > SNAPSHOT_MAX_SIZE_BYTES and not os.environ.get("AML_SNAPSHOT_NO_FILE_SIZE_LIMIT"):
        error_message = "====================================================================\n" \
                        "\n" \
                        "While attempting to take snapshot of {}\n" \
                        "Your total snapshot size exceeds the limit of {} MB.\n" \
                        "You can overwrite the size limit by specifying environment variable " \
                        "AML_SNAPSHOT_NO_FILE_SIZE_LIMIT, for example in bash: " \
                        "export AML_SNAPSHOT_NO_FILE_SIZE_LIMIT=True. \n" \
                        "Please see http://aka.ms/troubleshooting-code-snapshot on how to debug " \
                        "the creating process of component snapshots.\n" \
                        "\n" \
                        "====================================================================\n" \
                        "\n".format(component_file, SNAPSHOT_MAX_SIZE_BYTES / ONE_MB)
        if raise_on_validation_failure:
            raise SnapshotException(error_message)
        else:
            logger.warning(error_message)


def validate_snapshot_file_count(file_or_folder_path, file_number, raise_on_validation_failure, logger):
    if file_number > SNAPSHOT_MAX_FILES and not os.environ.get("AML_SNAPSHOT_NO_FILE_LIMIT"):
        error_message = "====================================================================\n" \
                        "\n" \
                        "While attempting to take snapshot of {}\n" \
                        "Your project exceeds the file limit of {}.\n" \
                        "Please see http://aka.ms/troubleshooting-code-snapshot on how to debug " \
                        "the creating process of component snapshots.\n" \
                        "\n" \
                        "====================================================================\n" \
                        "\n".format(file_or_folder_path, SNAPSHOT_MAX_FILES)
        if raise_on_validation_failure:
            raise SnapshotException(error_message)
        else:
            logger.warning(error_message)


def _upload_files_one_batch(worker_pool,
                            logger,
                            flush_timeout_seconds,
                            identity,
                            batch_nodes,
                            file_or_folder_path,
                            session,
                            timeout_env_var,
                            results,
                            revision_list,
                            blob_uri="blobUri"):
    """ Upload files in one batch.

    When timeout error happens, throw error with clear message to guide user overwrite it.

    :param flush_timeout_seconds: Task flush timeout in seconds.
    :param identity: Flush source name
    :param batch_nodes: Files in one batch
    :param file_or_folder_path: Snapshot file/folder path
    :param session: Request session
    :param timeout_env_var: Timeout environment variable
    :param results: Task list
    :param revision_list: Revision file list
    :param blob_uri: "blobUri" or "absoluteBlobUri"
    """
    with TaskQueue(worker_pool=worker_pool, flush_timeout_seconds=flush_timeout_seconds,
                   _ident=identity, _parent_logger=logger) as task_queue:

        def perform_upload(file_or_folder_path, file_name, upload_url, session):
            with open(os.path.join(file_or_folder_path, file_name), "rb") as data:
                return upload_blob_from_stream(data, upload_url, session=session, timeout=TIMEOUT,
                                               backoff=BACKOFF_START, retries=RETRY_LIMIT)

        for node in batch_nodes:
            file_name = node['fullName']
            upload_url = node[blob_uri]
            task = task_queue.add(perform_upload, file_or_folder_path, file_name, upload_url, session)
            results.append(task)

            file_size = os.path.getsize(os.path.join(file_or_folder_path, file_name))
            file_revision = {"FullName": file_name, "BlobUri": upload_url, "FileSize": file_size}
            revision_list.append(file_revision)

        try:
            task_queue.flush(source=identity)
        except AzureMLException as e:
            # Guide user overwrite AZUREML_SNAPSHOT_DEFAULT_TIMEOUT when timeout happens
            e.message += (
                "\nYou can overwrite the flush timeout by specifying corresponding value to "
                "environment variable {}, "
                "for example in bash: export {}=900. \n"
                "Please see http://aka.ms/troubleshooting-code-snapshot on how to debug "
                "the creating process of component snapshots.".format(timeout_env_var, timeout_env_var)
            )
            raise e


def _upload_files_batch(worker_pool, logger, file_nodes, file_or_folder_path, session,
                        component_name=None, blob_uri="blobUri"):
    """ Upload files in batch.

    When timeout error happens, throw error with clear message to guide user overwrite it.

    :param file_nodes: File nodes list.
    :param file_or_folder_path: Snapshot file/folder path
    :param session: Request session
    :param component_name: component_name in component yaml
    :param blob_uri: "blobUri" or "absoluteBlobUri"
    :return: Revision file list with blob URL, eg: [
            {"FullName": file_name1, "BlobUri": upload_url1, "FileSize": file_size1},
            {"FullName": file_name2, "BlobUri": upload_url2, "FileSize": file_size2},
            ...
        ], map from upload tasks to it's results
    """
    batch_size = MAX_FILES_SNAPSHOT_UPLOAD_PARALLEL
    results = []
    revision_list = []
    flush_timeout_seconds = AZUREML_SNAPSHOT_DEFAULT_TIMEOUT
    timeout_env_var = "AZUREML_SNAPSHOT_TIMEOUT_SECONDS"
    # get flush timeout, if user set AZUREML_SNAPSHOT_TIMEOUT_SECONDS in environment var, use it
    if os.environ.get(timeout_env_var):
        try:
            flush_timeout_seconds = float(os.environ.get(timeout_env_var))
        except ValueError:
            raise UserErrorException(
                "Environment variable {} with value {} set but failed to parse. "
                "Please reset the value to a number.".format(timeout_env_var, os.environ.get(timeout_env_var)))

    identity = "snapshot_upload_files"
    if str2bool(os.environ.get('AML_COMPONENT_SNAPSHOT_WITHOUT_UPLOAD_PROGRESS_BAR')):
        for i in range(0, len(file_nodes), batch_size):
            batch_nodes = file_nodes[i:i + batch_size]
            _upload_files_one_batch(worker_pool,
                                    logger,
                                    flush_timeout_seconds,
                                    identity,
                                    batch_nodes,
                                    file_or_folder_path,
                                    session,
                                    timeout_env_var,
                                    results,
                                    revision_list,
                                    blob_uri)
        logger.debug("Uploaded snapshot of component: '{}' with {} files".format(component_name, len(revision_list)))
    else:
        desc = "Uploading snapshot of component: '{}'".format(component_name)
        with tqdm(total=len(file_nodes), desc=desc, unit="files", position=0) as progress_bar:
            for i in range(0, len(file_nodes), batch_size):
                batch_nodes = file_nodes[i:i + batch_size]
                _upload_files_one_batch(worker_pool,
                                        logger,
                                        flush_timeout_seconds,
                                        identity,
                                        batch_nodes,
                                        file_or_folder_path,
                                        session,
                                        timeout_env_var,
                                        results,
                                        revision_list,
                                        blob_uri)

                progress_bar.update(len(batch_nodes))

    return revision_list, map(lambda task: task.wait(), results)


class AssetSnapshotsClient(WorkspaceTelemetryMixin):
    """
    Asset snapshot client class, extended from azureml._restclient.clientbase.ClientBase.
    This client is used to upload snapshot to asset.

    :param workspace: Workspace for this client
    :type workspace: azureml.core.Workspace
    :param base_url: Base url of client
    :type base_url: str
    :param auth: Authentication classes in Azure Machine Learning.
    :type auth: azureml.core.authentication.AbstractAuthentication
    :param logger: the logger used to log info and warning happened during uploading snapshot
    :type logger: logging.Logger
    """

    def __init__(self, workspace, base_url, auth, logger=None):
        super(AssetSnapshotsClient, self).__init__(workspace=workspace)
        self.base_url = base_url
        self.auth = auth
        self._cache = SnapshotCache(workspace._service_context) if workspace else None
        if not logger:
            self.logger = logging.getLogger('snapshot')
        else:
            self.logger = logger

    def validate_snapshot_size(self, size, component_file, raise_on_validation_failure):
        """Validate size of snapshot.

        :param size: Size of component snapshot.
        :param component_file: The component spec file.
        :param raise_on_validation_failure: Raise error if validation failed.
        """
        validate_snapshot_size(size, component_file, raise_on_validation_failure, self.logger)

    def _validate_snapshot_file_count(self, file_or_folder_path, file_number, raise_on_validation_failure):
        validate_snapshot_file_count(file_or_folder_path, file_number, raise_on_validation_failure, self.logger)

    def _upload_asset_store_snapshot_files(self, entries_to_send, asset_id, curr_root, snapshot_folder,
                                           component_name=None, blob_uri="absoluteBlobUri"):
        headers = {'Content-Type': 'application/json; charset=UTF-8'}
        headers.update(self.auth.get_authentication_header())

        file_list = [entry.node_path for entry in entries_to_send]
        file_names = {"FileList": {"FileNames": file_list}, "DirTreeNode": curr_root,
                      "AssetId": asset_id}

        data = json.dumps(file_names, cls=DirTreeJsonEncoderV2)
        encoded_data = data.encode('utf-8')

        # set pool size to max threads to improve performance
        with create_session_with_retry(pool_maxsize=MAX_FILES_SNAPSHOT_UPLOAD_PARALLEL) as session:
            url = self.base_url + "/content/v2.0/snapshots/assetStoreWriteSases"

            response = execute_func(session.post, url, data=encoded_data, headers=headers)

            # raise SnapshotException when get blob response fails
            if response.status_code != 200:
                raise SnapshotException(get_http_exception_response_string(response))

            response_data = response.content.decode('utf-8')
            blob_uri_dict = json.loads(response_data)
            try:
                file_nodes = blob_uri_dict['fileNodes']
            except KeyError:
                raise SnapshotException(
                    "fileNodes not found in blob response, blob response {}".format(blob_uri_dict))

            revision_list = _upload_files_batch(ClientBase._get_worker_pool(),
                                                self.logger,
                                                file_nodes,
                                                snapshot_folder,
                                                session,
                                                component_name,
                                                blob_uri=blob_uri)[0]
            return revision_list

    @track()
    def create_asset_store_snapshot(self,
                                    snapshot_folder,
                                    size,
                                    registry="testFeed",
                                    version=1,
                                    component_file=None,
                                    retry_on_failure=True,
                                    raise_on_validation_failure=True,
                                    component_name=None):
        """Create assert store snapshot on given merkle tree root and snapshot size.

        :param component_file: Component base folder, used to calculate cache file location
        :param snapshot_folder: Snapshot base folder.
        :param size: snapshot size
        :param registry: registry name
        :param version: version number
        :param retry_on_failure: if set "True", retry when failure
        :param raise_on_validation_failure: if set "True", raise validation failure
        :param component_name: component name
        :return: asset id
        """
        if component_file is None:
            component_file = snapshot_folder

        # add extra dimensions(eg: snapshot size, upload time) to logger
        track_dimensions = {}

        self.validate_snapshot_size(size, component_file, raise_on_validation_failure)

        # Compute the dir tree for the current working set
        # The folder passed here has already excluded ignored files, so we do not need to check that
        def _is_file_excluded(file):
            return False

        curr_root = create_merkletree(snapshot_folder, _is_file_excluded)

        # Compute the diff between the two dirTrees
        entries = compute_diff(DirTreeNode(), curr_root)
        dir_tree_file_contents = json.dumps(curr_root, cls=DirTreeJsonEncoder)

        # get new snapshot id
        snapshot_id = str(uuid.uuid4())

        entries_to_send = [entry for entry in entries if entry.is_file]
        self._validate_snapshot_file_count(component_file, len(entries_to_send), raise_on_validation_failure)

        # Git metadata
        snapshot_properties = global_tracking_info_registry.gather_all(snapshot_folder)

        with create_session_with_retry() as session:
            self.logger.debug("Uploading asset store snapshot files")
            with TimerContext() as timer_context:
                try:
                    asset_id = "azureml://feeds/{registry}/codes/{snapshot_id}/versions/{version}".format(
                        registry=registry, snapshot_id=snapshot_id, version=version)
                    track_dimensions.update({'asset_id': asset_id})
                    revision_list = self._upload_asset_store_snapshot_files(entries_to_send, asset_id,
                                                                            curr_root, snapshot_folder,
                                                                            component_name)
                except AzureMLException as e:
                    # when uploading snapshot fails, record snapshot info from upload request
                    total_size = 0
                    try:
                        for entry in entries_to_send:
                            if hasattr(entry, 'node_path'):
                                total_size += os.path.getsize(os.path.join(snapshot_folder, entry.node_path))
                    except BaseException:
                        pass
                    track_dimensions.update({
                        'files_to_send': len(entries_to_send),
                        'total_size': total_size
                    })
                    # log files to send and total size here so we can have that when uploading failed
                    _LoggerFactory.add_track_dimensions(_get_logger(), track_dimensions)
                    raise e
                else:
                    # otherwise, record snapshot file info from upload result
                    total_size = reduce((lambda s, x: s + x['FileSize']), revision_list, 0)
                    total_size = total_size / 1024
                    track_dimensions.update({
                        'files_to_send': len(revision_list),
                        'total_size': total_size
                    })
                    _LoggerFactory.add_track_dimensions(_get_logger(), track_dimensions)

                # log uploaded files
                for entry in entries_to_send:
                    self.logger.debug("\t{} {}".format(
                        str(entry.operation_type).capitalize(), entry.node_path))

                collect_duration_seconds = timer_context.get_duration_seconds()
                track_dimensions.update({
                    'upload_duration_seconds': collect_duration_seconds
                })
                self.logger.debug(
                    'Uploaded {} files in {:.2f} seconds, total size {:.2f} KB'.format(
                        len(revision_list), collect_duration_seconds, total_size))

            create_data = {"AssetId": asset_id, "Tags": None, "Properties": snapshot_properties}
            create_data.update({"DirTreeNode": curr_root})
            create_data.update({"FileRevisionList": {"FileNodes": revision_list}})

            data = json.dumps(create_data, cls=DirTreeJsonEncoderV2)
            encoded_data = data.encode('utf-8')

            url = self.base_url + "/content/v2.0/snapshots/createInAssetStore"

            headers = {'Content-Type': 'application/json; charset=UTF-8'}
            headers.update(self.auth.get_authentication_header())
            # record time spent when uploading snapshot
            with TimerContext() as timer_context:
                response = execute_func(
                    session.post, url, data=encoded_data, headers=headers)
                upload_duration_seconds = timer_context.get_duration_seconds()
                track_dimensions.update({
                    'create_duration_seconds': upload_duration_seconds
                })
                self.logger.debug('Created asset snapshot in {:.2f} seconds.'.format(upload_duration_seconds))

            response_content = response.content
            response_json = json.loads(response_content.decode('utf-8'))

            if response.status_code == 202:
                location = response_json["location"]
                self._get_snapshot_sas(asset_id, location)

            if response.status_code >= 400:
                if retry_on_failure:
                    if self._cache:
                        # The cache may have been corrupted, so clear it and try again.
                        self._cache.remove_latest()
                    return self.create_asset_store_snapshot(
                        snapshot_folder=snapshot_folder, size=size, registry=registry, version=version,
                        component_file=component_file, retry_on_failure=False,
                        raise_on_validation_failure=raise_on_validation_failure, component_name=component_name)
                else:
                    raise SnapshotException(get_http_exception_response_string(response))

        snapshot_dto = SnapshotDto(dir_tree_file_contents, asset_id)

        if self._cache:
            # Update the cache
            self._cache.update_cache(snapshot_dto, snapshot_folder)
        # update tracked dimensions
        _LoggerFactory.add_track_dimensions(_get_logger(), track_dimensions)
        return asset_id

    def _get_snapshot_sas(self, snapshot_id, location):
        self.logger.debug("Start polling until complete for creating asset store snapshot")
        headers = self.auth.get_authentication_header()
        status = 202
        timeout_seconds = AZUREML_SNAPSHOT_DEFAULT_TIMEOUT
        timeout_env_var = "AZUREML_SNAPSHOT_TIMEOUT_SECONDS"
        # get timeout env var, if user set AZUREML_SNAPSHOT_TIMEOUT_SECONDS in environment var, use it
        if os.environ.get(timeout_env_var):
            try:
                timeout_seconds = float(os.environ.get(timeout_env_var))
            except ValueError:
                raise UserErrorException(
                    "Environment variable {} with value {} set but failed to parse. "
                    "Please reset the value to a number.".format(timeout_env_var, os.environ.get(timeout_env_var)))
        time_run = 0
        sleep_period = 5

        while status == 202:
            if time_run + sleep_period > timeout_seconds:
                message = "Timeout on Get sas for snapshot : {}\n" \
                          "You can overwrite the timeout by specifying corresponding value to " \
                          "environment variable {}, " \
                          "for example in bash: export {}=900.\n".format(snapshot_id, timeout_env_var, timeout_env_var)
                raise Exception(message)
            time_run += sleep_period
            time.sleep(sleep_period)
            with create_session_with_retry() as session:
                response = execute_func(session.get, location, headers=headers)
                # This returns a sas url to blob store
                response.raise_for_status()
                status = response.status_code
                if status not in (200, 202, 204):
                    message = "Error Get snapshot sas. Code: {}\n: {}".format(status, response.text)
                    raise Exception(message)
        self.logger.debug("Complete polling for creating asset store snapshot")


class SnapshotsClient(BaseSnapshotsClient, WorkspaceTelemetryMixin):
    """
    Snapshot client class, extended from azureml._restclient.snapshots_client.SnapshotsClient.
    Add snapshot cache per component.

    :param workspace: Workspace for this client
    :type workspace: azureml.core.Workspace
    :param logger: the logger used to log info and warning happened during uploading snapshot
    :type logger: logging.Logger
    """

    def __init__(self, workspace, logger=None):
        # the mro of this class is BaseSnapshotsClient -> WorkspaceClient -> ClientBase -> ChainedIdentity
        # -> WorkspaceTelemetryMixin -> TelemetryMixin -> object
        super(SnapshotsClient, self).__init__(workspace.service_context, workspace=workspace)
        self._cache = SnapshotCache(self._service_context)
        if not logger:
            self.logger = logging.getLogger('snapshot')
        else:
            self.logger = logger

    def validate_snapshot_size(self, size, component_file, raise_on_validation_failure):
        """Validate size of snapshot.

        :param size: Size of component snapshot.
        :param component_file: The component spec file.
        :param raise_on_validation_failure: Raise error if validation failed.
        """
        validate_snapshot_size(size, component_file, raise_on_validation_failure, self.logger)

    def _validate_snapshot_file_count(self, file_or_folder_path, file_number, raise_on_validation_failure):
        validate_snapshot_file_count(file_or_folder_path, file_number, raise_on_validation_failure, self.logger)

    @track()
    def create_snapshot(
            self, snapshot_folder, size,
            component_file=None, retry_on_failure=True, raise_on_validation_failure=True, component_name=None):
        """Create snapshot on given merkle tree root and snapshot size.
        support cache and incrementally update based on latest snapshot

        :param component_file: Component base folder, used to calculate cache file location
        :param snapshot_folder: Snapshot base folder.
        :param size: snapshot size
        :param retry_on_failure:
        :param raise_on_validation_failure:
        :param component_name: component name
        :return:
        """
        if component_file is None:
            component_file = snapshot_folder

        # add extra dimensions(eg: snapshot size, upload time) to logger
        track_dimensions = {}

        self.validate_snapshot_size(size, component_file, raise_on_validation_failure)

        # Get the previous snapshot for this project
        try:
            parent_root, parent_snapshot_id = self._cache.get_latest_snapshot_by_path(component_file)
        except json.decoder.JSONDecodeError:
            # Removing the cache file if found corrupted
            self._cache.remove_cache(component_file)
            parent_root, parent_snapshot_id = self._cache.get_latest_snapshot_by_path(component_file)

        # Compute the dir tree for the current working set
        # The folder passed here has already excluded ignored files, so we do not need to check that
        def _is_file_excluded(file):
            return False

        curr_root = create_merkletree(snapshot_folder, _is_file_excluded)

        # Compute the diff between the two dirTrees
        entries = compute_diff(parent_root, curr_root)
        dir_tree_file_contents = json.dumps(curr_root, cls=DirTreeJsonEncoder)

        # If there are no changes, just return the previous snapshot_id
        if not len(entries):
            self.logger.debug("The snapshot did not change compared to local cached one, "
                              "reused local cached snapshot.")
            track_dimensions.update({'local_cache': True})
            _LoggerFactory.add_track_dimensions(_get_logger(), track_dimensions)
            return parent_snapshot_id

        # get new snapshot id by snapshot hash
        snapshot_id = str(UUID(curr_root.hash[::4]))
        track_dimensions.update({'snapshot_id': snapshot_id})

        # Check whether the snapshot with new id already exists
        with TimerContext() as timer_context:
            snapshot_dto = self.get_snapshot_metadata_by_id(snapshot_id)
            get_snapshot_metadata_duration_seconds = timer_context.get_duration_seconds()
            track_dimensions.update({'get_snapshot_metadata_duration_seconds': get_snapshot_metadata_duration_seconds})
        if snapshot_dto is None:
            entries_to_send = [entry for entry in entries if (entry.operation_type == 'added' or
                                                              entry.operation_type == 'modified') and entry.is_file]
            self._validate_snapshot_file_count(component_file, len(entries_to_send), raise_on_validation_failure)

            # Git metadata
            snapshot_properties = global_tracking_info_registry.gather_all(snapshot_folder)

            headers = {'Content-Type': 'application/json; charset=UTF-8'}
            headers.update(self.auth.get_authentication_header())

            with create_session_with_retry() as session:
                self.logger.debug(
                    "Uploading snapshot files, only added or modified files will be uploaded.")
                with TimerContext() as timer_context:

                    try:
                        revision_list = self._upload_snapshot_files(
                            entries_to_send, snapshot_folder, _is_file_excluded, component_name)
                    except AzureMLException as e:
                        # when uploading snapshot fails, record snapshot info from upload request
                        total_size = 0
                        try:
                            for entry in entries_to_send:
                                if hasattr(entry, 'node_path'):
                                    total_size += os.path.getsize(os.path.join(snapshot_folder, entry.node_path))
                        except BaseException:
                            pass
                        track_dimensions.update({
                            'files_to_send': len(entries_to_send),
                            'total_size': total_size
                        })
                        # log files to send and total size here so we can have that when uploading failed
                        _LoggerFactory.add_track_dimensions(_get_logger(), track_dimensions)
                        raise e
                    else:
                        # otherwise, record snapshot file info from upload result
                        total_size = reduce((lambda s, x: s + x['FileSize']), revision_list, 0)
                        total_size = total_size / 1024
                        track_dimensions.update({
                            'files_to_send': len(revision_list),
                            'total_size': total_size
                        })
                        _LoggerFactory.add_track_dimensions(_get_logger(), track_dimensions)

                    # only log uploaded files when snapshot cache exists
                    if parent_snapshot_id != _EMPTY_GUID:
                        for entry in entries_to_send:
                            self.logger.debug("\t{} {}".format(
                                str(entry.operation_type).capitalize(), entry.node_path))

                    collect_duration_seconds = timer_context.get_duration_seconds()
                    track_dimensions.update({
                        'upload_duration_seconds': collect_duration_seconds
                    })
                    self.logger.debug(
                        'Uploaded {} files in {:.2f} seconds, total size {:.2f} KB'.format(
                            len(revision_list), collect_duration_seconds, total_size))

                create_data = {"ParentSnapshotId": parent_snapshot_id, "Tags": None, "Properties": snapshot_properties}
                create_data.update({"DirTreeNode": curr_root})
                create_data.update({"FileRevisionList": {"FileNodes": revision_list}})

                data = json.dumps(create_data, cls=DirTreeJsonEncoderV2)
                encoded_data = data.encode('utf-8')

                url = self._service_context._get_project_content_url() + "/content/v2.0" + \
                    self._service_context._get_workspace_scope() + "/snapshots/" + snapshot_id

                # record time spent when uploading snapshot
                with TimerContext() as timer_context:
                    response = self._execute_with_base_arguments(
                        session.post, url, data=encoded_data, headers=headers)
                    upload_duration_seconds = timer_context.get_duration_seconds()
                    track_dimensions.update({
                        'create_duration_seconds': upload_duration_seconds
                    })
                    self.logger.debug('Created snapshot in {:.2f} seconds.'.format(upload_duration_seconds))

                if response.status_code >= 400:
                    if retry_on_failure:
                        # The cache may have been corrupted, so clear it and try again.
                        self._cache.remove_latest()
                        return self.create_snapshot(
                            snapshot_folder, size, component_file, retry_on_failure=False)
                    else:
                        raise SnapshotException(get_http_exception_response_string(response))

            snapshot_dto = SnapshotDto(dir_tree_file_contents, snapshot_id)
        else:
            self.logger.debug("Found remote cache of snapshot, reused remote cached snapshot.")
            track_dimensions.update({'workspace_cache': True})

        # Update the cache
        self._cache.update_cache(snapshot_dto, component_file)
        # update tracked dimensions
        _LoggerFactory.add_track_dimensions(_get_logger(), track_dimensions)
        return snapshot_id

    def get_snapshot_metadata_by_id(self, snapshot_id):
        """
        200 indicates the snapshot with this id exists, 404 indicates not exists
        If other status codes returned, by default we will retry 3 times until we get 200 or 404
        """
        auth_headers = self.auth.get_authentication_header()
        url = self._service_context._get_project_content_url() + "/content/v1.0" + \
            self._service_context._get_workspace_scope() + "/snapshots/" + \
            snapshot_id + "/metadata"
        with create_session_with_retry() as session:
            response = self._execute_with_base_arguments(
                session.get, url, headers=auth_headers)
            if response.status_code == 200:
                response_data = response.content.decode('utf-8')
                snapshot_dict = json.loads(response_data)
                root_dict = snapshot_dict['root']
                snapshot_id = snapshot_dict['id']
                node = DirTreeNode()
                node.load_object_from_dict(root_dict)
                root = json.dumps(node, cls=DirTreeJsonEncoder)
                return SnapshotDto(root, snapshot_id)
            elif response.status_code == 404:
                return None
            else:
                raise SnapshotException(get_http_exception_response_string(response))

    def _upload_snapshot_files(self, entries_to_send, file_or_folder_path, exclude_function, component_name=None):
        headers = {'Content-Type': 'application/json; charset=UTF-8'}
        headers.update(self.auth.get_authentication_header())

        file_list = [entry.node_path for entry in entries_to_send]
        file_names = {"FileNames": file_list}

        data = json.dumps(file_names)
        encoded_data = data.encode('utf-8')

        # set pool size to max threads to improve performance
        with create_session_with_retry(pool_maxsize=MAX_FILES_SNAPSHOT_UPLOAD_PARALLEL) as session:
            get_blobs_url = self._service_context._get_project_content_url() + "/content/v2.0" + \
                self._service_context._get_workspace_scope() + "/snapshots/getblob"
            get_blobs_response = self._execute_with_base_arguments(
                session.post, get_blobs_url, data=encoded_data, headers=headers)

            # raise SnapshotException when get blob response fails
            if get_blobs_response.status_code != 200:
                raise SnapshotException(get_http_exception_response_string(get_blobs_response))

            response_data = get_blobs_response.content.decode('utf-8')
            blob_uri_dict = json.loads(response_data)
            try:
                file_nodes = blob_uri_dict['fileNodes']
            except KeyError:
                raise SnapshotException("fileNodes not found in blob response, blob response {}".format(blob_uri_dict))

            revision_list = _upload_files_batch(self._pool, self.logger, file_nodes, file_or_folder_path,
                                                session, component_name)
            return revision_list[0]

    @track()
    def restore_asset_store_snapshot(self, asset_id, path=None, component_name=None):
        """Restore asset store snapshot on given asset_id.

        :param asset_id: Asset id
        :param path: Local target storage path.
        :param component_name: Component name.
        :return: Absolute  local target storage path
        """
        track_dimensions = {}

        headers = {'Content-Type': 'application/json; charset=UTF-8'}
        headers.update(self.auth.get_authentication_header())

        with create_session_with_retry() as session:
            self.logger.debug("Downloading asset store snapshot files")

            with TimerContext() as timer_context:
                url = self._service_context._get_project_content_url() + "/content/v1.0" + \
                    self.get_workspace_uri_path() + "/feed/consume/sas"

                data = {"AssetId": asset_id, "ConsumptionContext": None}
                data = json.dumps(data)
                encoded_data = data.encode('utf-8')
                # This returns sas urls to blob store
                response = self._execute_with_base_arguments(session.post, url, data=encoded_data, headers=headers)
                response.raise_for_status()

                if response.status_code != 200:
                    message = "Error building asset store snapshot. Code: {}\n: {}".format(response.status_code,
                                                                                           response.text)
                    raise Exception(message)

                response_content = response.content
                response_json = json.loads(response_content.decode('utf-8'))
                if path is None:
                    path = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))
                get_sas_url_duration_seconds = timer_context.get_duration_seconds()
                track_dimensions.update({
                    'get_asset_sas_url_duration_seconds': get_sas_url_duration_seconds
                })
                self.logger.debug('Get asset sas url response in {:.2f} seconds.'.format(get_sas_url_duration_seconds))

            with TimerContext() as timer_context:
                downloaded_files_json = response_json["children"]
                flattened_download_files = flatten_download_files(downloaded_files_json, path)
                self._download_files_batch(flattened_download_files, session, component_name)
                download_duration_seconds = timer_context.get_duration_seconds()
                track_dimensions.update({
                    'download_asset_duration_seconds': download_duration_seconds
                })
                self.logger.debug('Downloaded asset snapshot in {:.2f} seconds.'.format(download_duration_seconds))

        _LoggerFactory.add_track_dimensions(_get_logger(), track_dimensions)
        return os.path.abspath(path)

    @track()
    def restore_snapshot_by_sas(self, snapshot_id, path=None, component_name=None):
        """Restore snapshot on given snapshot_id by sas url.

        :param snapshot_id: Snapshot id
        :param path: Local target storage path.
        :param component_name: Component name.
        :return: Absolute  local target storage path
        """
        track_dimensions = {}

        headers = self.auth.get_authentication_header()

        with create_session_with_retry() as session:
            self.logger.debug("Downloading asset store snapshot files")

            with TimerContext() as timer_context:
                url = self._service_context._get_project_content_url() + "/content/v1.0" + \
                    self.get_workspace_uri_path() + "/snapshots/" + snapshot_id + "/sas"

                # This returns sas urls to blob store
                response = self._execute_with_base_arguments(session.get, url, headers=headers)
                response.raise_for_status()

                if response.status_code != 200:
                    message = "Error building asset store snapshot. Code: {}\n: {}".format(response.status_code,
                                                                                           response.text)
                    raise Exception(message)

                response_content = response.content
                response_json = json.loads(response_content.decode('utf-8'))
                if path is None:
                    path = os.path.join(tempfile.gettempdir(), str(snapshot_id))
                get_sas_url_duration_seconds = timer_context.get_duration_seconds()
                track_dimensions.update({
                    'get_sas_url_duration_seconds': get_sas_url_duration_seconds
                })
                self.logger.debug('Get sas url response in {:.2f} seconds.'.format(get_sas_url_duration_seconds))

            with TimerContext() as timer_context:
                downloaded_files_json = response_json["children"]
                flattened_download_files = flatten_download_files(downloaded_files_json, path)
                self._download_files_batch(flattened_download_files, session, component_name)
                download_duration_seconds = timer_context.get_duration_seconds()
                track_dimensions.update({
                    'download_duration_seconds': download_duration_seconds
                })
                self.logger.debug('Downloaded snapshot in {:.2f} seconds.'.format(download_duration_seconds))

        _LoggerFactory.add_track_dimensions(_get_logger(), track_dimensions)
        return os.path.abspath(path)

    def _download_files_batch(self, file_nodes, session, component_name=None):
        """ Download files in batch.

        When timeout error happens, throw error with clear message to guide user overwrite it.

        :param file_nodes: File nodes list.
        :param session: Request session.
        :param component_name: Component name.
        """
        results = []
        batch_size = MAX_FILES_SNAPSHOT_UPLOAD_PARALLEL
        flush_timeout_seconds = AZUREML_SNAPSHOT_DEFAULT_TIMEOUT
        timeout_env_var = "AZUREML_SNAPSHOT_TIMEOUT_SECONDS"
        # get flush timeout, if user set AZUREML_SNAPSHOT_TIMEOUT_SECONDS in environment var, use it
        if os.environ.get(timeout_env_var):
            try:
                flush_timeout_seconds = float(os.environ.get(timeout_env_var))
            except ValueError:
                raise UserErrorException(
                    "Environment variable {} with value {} set but failed to parse. "
                    "Please reset the value to a number.".format(timeout_env_var, os.environ.get(timeout_env_var)))

        identity = "snapshot_download_files"
        if str2bool(os.environ.get(AML_COMPONENT_SNAPSHOT_WITHOUT_DOWNLOAD_PROGRESS_BAR)):
            for i in range(0, len(file_nodes), batch_size):
                batch_nodes = file_nodes[i:i + batch_size]
                self._download_files_one_batch(flush_timeout_seconds,
                                               identity,
                                               batch_nodes,
                                               session,
                                               timeout_env_var,
                                               results
                                               )
            self.logger.debug("Downloaded snapshot of component: '{}' with {} files".format(component_name,
                                                                                            len(file_nodes)))
        else:
            desc = "Downloading snapshot of component: '{}'".format(component_name)
            with tqdm(total=len(file_nodes), desc=desc, unit="files", position=0) as progress_bar:
                for i in range(0, len(file_nodes), batch_size):
                    batch_nodes = file_nodes[i:i + batch_size]
                    self._download_files_one_batch(flush_timeout_seconds,
                                                   identity,
                                                   batch_nodes,
                                                   session,
                                                   timeout_env_var,
                                                   results
                                                   )

                    progress_bar.update(len(batch_nodes))
        return map(lambda task: task.wait(), results)

    def _download_files_one_batch(self,
                                  flush_timeout_seconds,
                                  identity,
                                  batch_nodes,
                                  session,
                                  timeout_env_var,
                                  results
                                  ):
        """ Download files in one batch.

        When timeout error happens, throw error with clear message to guide user overwrite it.

        :param flush_timeout_seconds: Task flush timeout in seconds.
        :param identity: Flush source name
        :param batch_nodes: Files in one batch
        :param session: Request session
        :param timeout_env_var: Timeout environment variable
        :param results: Task list
        """
        with TaskQueue(worker_pool=self._pool, flush_timeout_seconds=flush_timeout_seconds,
                       _ident=identity, _parent_logger=self._logger) as task_queue:

            def perform_download(file_path, download_url, session):
                try:
                    download_file(source_uri=download_url, path=file_path, session=session)
                except requests.HTTPError as http_error:
                    raise ProjectSystemException(http_error.strerror)

            for node in batch_nodes:
                file_path = node[0]
                download_url = node[1]
                task = task_queue.add(perform_download, file_path, download_url, session)
                results.append(task)
            try:
                task_queue.flush(source=identity)
            except AzureMLException as e:
                # Guide user overwrite AZUREML_SNAPSHOT_DEFAULT_TIMEOUT when timeout happens
                e.message += (
                    "\nYou can overwrite the flush timeout by specifying corresponding value to "
                    "environment variable {}, "
                    "for example in bash: export {}=900. \n"
                    "Please see http://aka.ms/troubleshooting-code-snapshot on how to debug "
                    "the restore process of component snapshots.".format(timeout_env_var, timeout_env_var)
                )
                raise e
