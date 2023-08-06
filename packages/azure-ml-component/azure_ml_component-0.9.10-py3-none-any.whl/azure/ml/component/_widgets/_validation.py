# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from traitlets import Unicode, Int
import json
import os

from ipywidgets import DOMWidget, register
from azure.ml.component._util._utils import get_pipeline_response_content
from ._utils import _get_run_from_content, _get_graph_from_query_dict, _get_run_status_from_query_dict, \
    _get_graph_no_staus_from_query_dict, _get_step_run_details_from_run, _get_child_runs_from_query_dict, \
    _get_pipeline_run_from_query_dict, _get_root_run_info_from_query_dict


@register
class ValidateView(DOMWidget):
    """ A widget for the pipeline validate visualization.

    Especially, the widget accept message to update running status.
    And return the latest status into view.
    """

    _view_name = Unicode('ValidateView').tag(sync=True)
    _view_module = Unicode('validate_widget').tag(sync=True)
    _view_module_version = Unicode('0.0.0').tag(sync=True)

    graph_json = Unicode().tag(sync=True)
    pipeline_graph_json = Unicode().tag(sync=True)
    env_json = Unicode().tag(sync=True)
    lib_url = Unicode().tag(sync=True)
    container_id = Unicode().tag(sync=True)
    visualize_id = Unicode().tag(sync=True)
    is_prod = Int().tag(sync=True)
    show_validate = Int().tag(sync=True)

    def __init__(self, **kwargs):
        """Create a ValidateView widget."""
        super(DOMWidget, self).__init__(**kwargs)
        self.graph_json = kwargs.get("graph_json")
        self.pipeline_graph_json = kwargs.get("pipeline_graph_json")
        self.env_json = kwargs.get("env_json")
        self.lib_url = kwargs.get("lib_url")
        self.container_id = kwargs.get("container_id")
        self.visualize_id = kwargs.get("visualize_id")
        self.is_prod = kwargs.get("is_prod")
        self.show_validate = kwargs.get("show_validate")

        def handle_msg(instance, message, params):
            try:
                if message.get("message") == "log_query:request":
                    self.handle_log_query_request(message.get("body"))
                if message.get("message") == "fetch_profiling:request":
                    self.handle_fetch_profiling_request(message.get("body"))
                if message.get("message") == "graph:request":
                    self.handle_graph_request(message.get("body"))
                if message.get("message") == "runstatus:request":
                    self.handle_runstatus_request(message.get("body"))
                if message.get("message") == "graphnostatus:request":
                    self.handle_graph_no_status_request(message.get("body"))
                if message.get("message") == "pipelinerun:request":
                    self.handle_pipeline_run_request(message.get("body"))
                if message.get("message") == "steprundetails.request":
                    self.handle_steprun_details_request(message.get("body"))
                if message.get("message") == "childruns:request":
                    self.handle_childruns_request(message.get("body"))
                if message.get("message") == "rootruninfo:request":
                    self.handle_root_run_info_request(message.get("body"))
            except Exception as e:
                self.send_message("messageprocess:exception", e.message)

        self.on_msg(handle_msg)

    def handle_log_query_request(self, body):
        uid = body.get("uid")
        content = body.get("content")
        text = _get_url_content(content.get("url"))
        self.send_message("log_query:response", {
            "uid": uid,
            "result": text
        })

    def handle_fetch_profiling_request(self, body):
        uid = body.get("uid")
        content = body.get("content")

        run = _get_run_from_content(content)
        profile_data = run._get_profile_data_dict()

        self.send_message("fetch_profiling:response", {
            "uid": uid,
            "profiling": profile_data
        })

    def handle_graph_request(self, body):
        graph = _get_graph_from_query_dict(body.get("content"))
        self.send_message("graph_request:response", {
            "uid": body.get("uid"),
            "graph": json.loads(get_pipeline_response_content(graph))
        })

    def handle_runstatus_request(self, body):
        runstatus = _get_run_status_from_query_dict(body.get("content"))
        self.send_message("runstatus:response", {
            "uid": body.get("uid"),
            "runstatus": json.loads(get_pipeline_response_content(runstatus))
        })

    def handle_graph_no_status_request(self, body):
        graphnostatus = _get_graph_no_staus_from_query_dict(body.get("content"))
        self.send_message("graphnostatus:response", {
            "uid": body.get("uid"),
            "graphnostatus": json.loads(get_pipeline_response_content(graphnostatus))
        })

    def handle_steprun_details_request(self, body):
        content = body.get("content")
        run = _get_run_from_content(content)
        details = _get_step_run_details_from_run(run, body)
        self.send_message("steprundetails:response", {
            "uid": body.get("uid"),
            "steprundetails": details
        })

    def handle_childruns_request(self, body):
        childruns = _get_child_runs_from_query_dict(body.get("content"))
        self.send_message("childruns:response", {
            "uid": body.get("uid"),
            "childruns": json.loads(get_pipeline_response_content(childruns))
        })

    def handle_pipeline_run_request(self, body):
        pipelinerun = _get_pipeline_run_from_query_dict(body.get("content"))
        self.send_message("pipelinerun:response", {
            "uid": body.get("uid"),
            "pipelinerun": json.loads(get_pipeline_response_content(pipelinerun))
        })

    def handle_root_run_info_request(self, body):
        info = _get_root_run_info_from_query_dict(body.get("content"))
        self.send_message("rootruninfo:response", {
            "uid": body.get("uid"),
            "rootruninfo": info
        })

    def send_message(self, message: str, content: dict):
        self.send({
            "message": message,
            "body": content
        })


def _get_url_content(url):
    """
    Get url content
    If url in a web link, will response content of url request.
    If url is a local file path, will response file content.
    """
    import requests
    try:
        content = ''
        if url.lstrip().lower().startswith('http'):
            content = requests.get(url).text
        elif os.path.exists(url):
            with open(url, 'r') as f:
                content = f.read()
        return content
    except requests.exceptions.RequestException as e:
        # Catch request.get exception
        return 'Cannot get content from {}, raise exception: {}'.format(url, str(e))
    except FileNotFoundError:
        # Catch read log file error
        return 'Cannot get content from {}, because it not exist.'.format(url)
