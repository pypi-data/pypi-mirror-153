# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import os
import re

from azure.ml.component._restclients.service_caller_factory import _DesignerServiceCallerFactory
from azureml.core import Workspace
from azureml.exceptions import UserErrorException
from ._util._loggerfactory import track


def _find_content_disposition_filename(headers):
    if 'Content-Disposition' in headers.keys():
        fname = re.findall("filename=(.+);", headers['Content-Disposition'])
        if len(fname) > 0:
            return fname[0]
    return None


def _get_base_name_without_ext(filename):
    base_name = os.path.basename(filename)
    return os.path.splitext(base_name)[0]


def _get_default_output_file_name(export_format: str, draft_id=None, run_id=None):
    prefix = "run_{}".format(run_id) if draft_id is None else "draft_{}".format(draft_id)
    postfix = ""
    ext = ".py"
    if export_format == "Python":
        ext = ".py"
    elif export_format == "JupyterNotebook":
        ext = ".ipynb"
    else:
        raise ValueError("Invalid export format: {}".format(export_format))
    exist_count = 0
    default_name = prefix + postfix + ext
    while os.path.isfile(default_name):
        exist_count += 1
        postfix = "({})".format(exist_count)
        default_name = prefix + postfix + ext
    return default_name


def _save_graph_sdk_code(result, path, default_output_file_name):
    """
    save graph sdk code result according to response and user specified path and file name
    return the code saved full path
    """
    saved_code_path = None
    response_filename = _find_content_disposition_filename(result.headers)

    if response_filename is None or not response_filename.endswith(".zip"):
        saved_code_path = os.path.join(path, default_output_file_name)
        with open(saved_code_path, 'wb') as f:
            f.write(result.content)
    else:
        # first download the zip file
        zipFileFullName = os.path.join(path, response_filename)
        with open(zipFileFullName, 'wb') as f:
            f.write(result.content)
        internal_folder = _get_base_name_without_ext(response_filename)
        internal_folder = os.path.join(path, internal_folder)
        saved_code_path = internal_folder
        exist_count = 0
        while os.path.isdir(saved_code_path):
            exist_count += 1
            postfix = "({})".format(exist_count)
            saved_code_path = internal_folder + postfix
        from zipfile import ZipFile
        with ZipFile(zipFileFullName, 'r') as zip:
            zip.extractall(saved_code_path)
        os.remove(zipFileFullName)

    return saved_code_path


def _parse_designer_url(url: str):
    """
    assume there are only 7 kinds of valid url
    draft: /Normal/{draft_id}?wsid=/subscriptions/{sub_id}/resourcegroups/{rg}/workspaces/{ws}
    run: /pipelineruns/id/{exp_id}/{run_id}?wsid=/subscriptions/{sub_id}/resourcegroups/{rg}/workspaces/{ws}
    run: /pipelineruns/{exp_name}/{run_id}?wsid=/subscriptions/{sub_id}/resourcegroups/{rg}/workspaces/{ws}
    run: /runs/{run_id}?wsid=/subscriptions/{run_id}/resourcegroups/{rg}/workspaces/{ws}
    sub_graph: /runs/{run_id}?subscriptions/{run_id}/resourcegroups/{rg}/workspaces/{ws}/{node_id}?graphid={graphid}
    endpoint: /endpoint/{endpoint_id}/xxx
    published pipeline: /endpoint/{endpoint_id}/xxx/publishedpipeline/{published_pipeline_id}
    """
    entries = re.split(r'[/&?]', url)
    subscription_id = None
    resource_group = None
    workspace_name = None
    draft_id = None
    run_id = None
    endpoint_id = None
    published_pipeline_id = None

    def _get_entry_index_value(entries, index):
        if len(entries) >= index + 1:
            return entries[index]
        else:
            return None

    for i, entry in enumerate(entries):
        entry = entry.lower()
        if entry == "runs":
            run_id = _get_entry_index_value(entries, i + 1)
        elif entry == "pipelineruns":
            if _get_entry_index_value(entries, i + 1) == "id":
                run_id = _get_entry_index_value(entries, i + 3)
            else:
                run_id = _get_entry_index_value(entries, i + 2)
        elif entry == "normal":
            draft_id = _get_entry_index_value(entries, i + 1)
        elif entry == "subscriptions":
            subscription_id = _get_entry_index_value(entries, i + 1)
        elif entry == "resourcegroups":
            resource_group = _get_entry_index_value(entries, i + 1)
        elif entry == "workspaces":
            workspace_name = _get_entry_index_value(entries, i + 1)
        elif entry == "endpoint":
            endpoint_id = _get_entry_index_value(entries, i + 1)
        elif entry == "publishedpipeline":
            published_pipeline_id = _get_entry_index_value(entries, i + 1)

    if draft_id is None and run_id is None and endpoint_id is None and published_pipeline_id is None:
        raise UserErrorException("Invalid url. No draft_id, run_id, endpoint_id, published_pipeline_id found.")

    if subscription_id is None or resource_group is None or workspace_name is None:
        raise UserErrorException("Invalid url. No subscription_id, resource_group or workspace_name found")

    graph_id = re.findall("graphid=([^/&?]+)", url.lower())
    graph_id = graph_id[0] if graph_id else None

    return (subscription_id, resource_group, workspace_name,
            draft_id, run_id, endpoint_id, published_pipeline_id, graph_id)


@track(activity_name="_export_pipeline_draft_to_code")
def _export_pipeline_draft_to_code(workspace: Workspace, draft_id: str, path: str,
                                   export_format: str):
    # This API are only called from CLI currently.
    service_caller = _DesignerServiceCallerFactory.get_instance(workspace, from_cli=True)
    result = service_caller.get_pipeline_draft_sdk_code(draft_id=draft_id, target_code=export_format)

    default_out_file_name = _get_default_output_file_name(export_format=export_format, draft_id=draft_id)
    return _save_graph_sdk_code(result, path, default_out_file_name)


@track(activity_name="_export_pipeline_run_to_code")
def _export_pipeline_run_to_code(workspace: Workspace, pipeline_run_id: str, path: str,
                                 export_format: str, experiment_name: str, experiment_id: str):
    # This API are only called from CLI currently.
    service_caller = _DesignerServiceCallerFactory.get_instance(workspace, from_cli=True)
    result = service_caller.get_pipeline_run_sdk_code(pipeline_run_id=pipeline_run_id, target_code=export_format,
                                                      experiment_id=experiment_id, experiment_name=experiment_name)

    default_out_file_name = _get_default_output_file_name(export_format=export_format, run_id=pipeline_run_id)
    return _save_graph_sdk_code(result, path, default_out_file_name)
