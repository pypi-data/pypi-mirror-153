# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import json
from threading import Thread, Lock
from socketserver import ThreadingMixIn
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import parse
from azure.ml.component._util._utils import get_pipeline_response_content
from ._utils import _get_run_from_content, _get_graph_from_query_dict, _get_run_status_from_query_dict, \
    _get_graph_no_staus_from_query_dict, _get_step_run_details_from_run, _get_child_runs_from_query_dict, \
    _get_pipeline_run_from_query_dict, _get_designer_service_caller_from_dict, _get_root_run_info_from_query_dict

FORWARD_ROUTE = '/forward'
GRAPH_ROUTE = '/graph'
RUNSTATUS_ROUTE = '/runstatus'
GRAPH_NO_STATUS_ROUTE = '/graphnostatus'
PROFILE_ROUTE = '/profile'
PIPELINE_RUN_ROUTE = '/pipelinerun'
CHILDRUNS_ROUTE = '/childruns'
STEPRUN_DETAILS_ROUTE = '/steprundetails'
ROOT_RUN_INFO_ROUTE = '/rootruninfo'


class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass


class BaseVisualizeRequestHandler(BaseHTTPRequestHandler):
    """Handle the requests that arrive at the server."""

    def end_headers(self):
        # To handle CORS issue
        self.send_header('Access-Control-Allow-Credentials', True)
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Access-Control-Allow-Methods', '*')
        self.send_header('Access-Control-Allow-Origin', '*')
        BaseHTTPRequestHandler.end_headers(self)

    def _set_response(self):
        self.send_response(200)
        self.end_headers()


class ForwardRequestHandler(BaseVisualizeRequestHandler):
    """Handle the forward requests that arrive at the server."""
    designer_service_caller = None

    def do_POST(self):
        """
        Handle POST request.
        If url in request content is a web link, will response content of url request.
        If url is a local file path, will response file content.
        """
        if self.path == FORWARD_ROUTE:
            # Get forward url from request
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                request_json = json.loads(post_data.decode('utf-8'))
            except json.decoder.JSONDecodeError:
                self.send_error(400, 'Request content is not json format')
                return
            if 'url' not in request_json:
                self.send_error(400, 'Can not get url from request content')
                return

            from ._validation import _get_url_content

            # Get forward request content
            content = _get_url_content(request_json['url'])
            self._set_response()
            content = json.dumps({'result': content})
            self.wfile.write(content.encode('utf-8'))
        else:
            self.send_error(404, '{} not found!'.format(self.path))

    def do_OPTIONS(self):
        """
        Handle OPTIONS request
        Handling cross-domain requests and set Access-Control-Allow in response header.
        """
        # In CORS, a preflight request is sent with the OPTIONS method so that the server can respond
        # if it is acceptable to send the request. It sets some Access-Control-Allow headers in response
        # and no need to write content in response.
        self._set_response()

    def do_GET(self):
        """
        Handle GET request
        """
        parse_result = parse.urlsplit(self.path)
        query = parse_result.query
        query_dict = dict(parse.parse_qsl(query))
        designer_service_caller = _get_designer_service_caller_from_dict(query_dict)

        try:
            if designer_service_caller is None:
                self.send_error(400, 'designer_service_caller could not set up!')
            elif parse_result.path == GRAPH_ROUTE:
                if 'graphId' not in query_dict:
                    self.send_error(400, 'missing required parameter graphId!')

                run_graph = _get_graph_from_query_dict(designer_service_caller, query_dict)

                self._set_response()
                self.wfile.write(get_pipeline_response_content(run_graph))
            elif parse_result.path == RUNSTATUS_ROUTE:
                if 'runId' not in query_dict or 'experimentId' not in query_dict:
                    self.send_error(400, 'missing required parameter runId or experimentId')

                run_status = _get_run_status_from_query_dict(designer_service_caller, query_dict)

                self._set_response()
                self.wfile.write(get_pipeline_response_content(run_status))
            elif parse_result.path == GRAPH_NO_STATUS_ROUTE:
                if 'runId' not in query_dict:
                    self.send_error(400, 'missing required parameter runId')

                graph_no_status = _get_graph_no_staus_from_query_dict(designer_service_caller, query_dict)

                self._set_response()
                self.wfile.write(get_pipeline_response_content(graph_no_status))
            elif parse_result.path == PROFILE_ROUTE:
                if 'runId' not in query_dict:
                    self.send_error(400, 'missing required parameter runId')
                run_id = query_dict['runId']
                profiling = designer_service_caller.get_pipeline_run_profile(pipeline_run_id=run_id)
                self._set_response()
                self.wfile.write(get_pipeline_response_content(profiling))
            elif parse_result.path == CHILDRUNS_ROUTE:
                if 'runId' not in query_dict:
                    self.send_error(400, 'missing required parameter runId')
                result = _get_child_runs_from_query_dict(designer_service_caller, query_dict)
                self._set_response()
                self.wfile.write(get_pipeline_response_content(result))
            elif parse_result.path == PIPELINE_RUN_ROUTE:
                if 'runId' not in query_dict:
                    self.send_error(400, 'missing required parameter runId')
                run = _get_pipeline_run_from_query_dict(designer_service_caller, query_dict)
                self._set_response()
                self.wfile.write(get_pipeline_response_content(run))
            elif parse_result.path == STEPRUN_DETAILS_ROUTE:
                if 'runId' not in query_dict or 'experimentName' not in query_dict:
                    self.send_error(400, 'missing required parameter runId or experimentName')
                run = _get_run_from_content(query_dict)
                if run._type != 'azureml.StepRun':
                    self.send_error(400, 'not a step run')

                step_details = _get_step_run_details_from_run(designer_service_caller, run)

                self._set_response()
                content = json.dumps(step_details)
                self.wfile.write(content.encode('utf-8'))
            elif parse_result.path == ROOT_RUN_INFO_ROUTE:
                if 'runId' not in query_dict or 'experimentName' not in query_dict:
                    self.send_error(400, 'missing required parameter runId or experimentName')

                root_info = _get_root_run_info_from_query_dict(query_dict)

                self._set_response()
                content = json.dumps(root_info)
                self.wfile.write(content.encode('utf-8'))
            else:
                self.send_error(404, 'Invalid url!')
        except Exception as e:
            self.send_error(500, e.message)

    def log_message(self, format, *args):
        # Overwrite BaseHTTPRequestHandler.log_message to avoid logging handler info.
        pass


class VisualizeServer:
    """Handle requests in a separate thread."""

    _instance_lock = Lock()
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Singleton creation visualize server
        """
        # VisualizeServer is used to handle CORS when getting run logs in jupyter. To handle requests from all
        # visualizer in process, life cycle of VisualizeServer is the entire process. And creating VisualizeServer
        # with singleton to avoid creating services repeatedly.
        if cls._instance is None:
            with cls._instance_lock:
                if cls._instance is None:
                    cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, request_handler):
        """
        Init and start visualize server in thread

        :param request_handler: RequestHandlerClass
        :type request_handler: http.server.BaseHTTPRequestHandler
        """
        # For first initialization, VisualizeServer._instance doesn't has attribute server.
        # To avoid create multi servers, will check attribute server exist.
        if not hasattr(self, 'server'):
            # OS will pick up an availabe port if not bind to specific port or port 0.
            self.server = ThreadingSimpleServer(('localhost', 0), request_handler)
            # Start server in thread.
            self.server_thread = Thread(target=self.server.serve_forever)
            self.server_thread.setDaemon(True)
            self.server_thread.start()

    def get_server_address(self):
        if hasattr(self, 'server'):
            address = self.server.server_address
            return 'http://{}:{}'.format(address[0], address[1])

    def server_avaliable(self):
        # Check server is avaliable.
        return self.server_thread.is_alive()
