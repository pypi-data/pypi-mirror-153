# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import json
import os
import time
from uuid import uuid4
from azure.ml.component._util._loggerfactory import _LoggerFactory, track
from azure.ml.component._util._utils import enabled_subpipeline_registration
from ._visualize_server import ForwardRequestHandler
from ._visualize_server import VisualizeServer, FORWARD_ROUTE, GRAPH_ROUTE, RUNSTATUS_ROUTE,\
    GRAPH_NO_STATUS_ROUTE, PROFILE_ROUTE, PIPELINE_RUN_ROUTE, CHILDRUNS_ROUTE, STEPRUN_DETAILS_ROUTE,\
    ROOT_RUN_INFO_ROUTE

AZUREML_SDK_UI_VERSION_SET_ENV_NAME = "AZUREML_SDK_UI_VERSION_SET"
AZUREML_SDK_UI_URL_ENV_NAME = "AZUREML_SDK_UI_URL"

_logger = None
_component_version = None


def _get_logger():
    global _logger
    if _logger is not None:
        return _logger
    _logger = _LoggerFactory.get_logger()
    return _logger


def get_component_sdk_version():
    global _component_version
    if _component_version is not None:
        return _component_version
    _LoggerFactory._get_version_info()
    _component_version = _LoggerFactory._component_version
    return _component_version


def _visualize(graphyaml: dict, envinfo: dict = None, is_prod: bool = False,
               ignore_fallback: bool = False, show_validate: bool = False, pipeline_graph: dict = None):
    from IPython.display import Javascript, display, HTML

    visualize_id = str(uuid4())
    container_id = "container_id_{0}".format(visualize_id)
    widget_container_id = "{0}_widget".format(container_id)
    script_container_id = "{0}_script".format(container_id)
    # Todo: This blob storage is for demo only. Use real cdn endpoint for production.
    lib_url = _get_ux_lib_url(is_prod)

    js_filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "js/validation.js")
    widget_view_lib = Javascript(filename=js_filename)
    display(widget_view_lib)

    loading_html = read_loading_content(visualize_id=visualize_id)
    display(HTML(loading_html))

    graphjson = json.dumps(graphyaml)
    pipeline_graph_json = json.dumps(pipeline_graph)

    envinfo = envinfo if envinfo is not None else {}
    envinfo.setdefault("sdk_version", get_component_sdk_version())
    try:
        visualize_server = VisualizeServer(ForwardRequestHandler)
        server_address = visualize_server.get_server_address()
        envinfo['forward_server_url'] = server_address + FORWARD_ROUTE
        envinfo['graph_server_url'] = server_address + GRAPH_ROUTE
        envinfo['runstatus_server_url'] = server_address + RUNSTATUS_ROUTE
        envinfo['graph_no_status_server_url'] = server_address + GRAPH_NO_STATUS_ROUTE
        envinfo['profile_server_url'] = server_address + PROFILE_ROUTE
        envinfo['pipelinerun_server_url'] = server_address + PIPELINE_RUN_ROUTE
        envinfo['childruns_server_url'] = server_address + CHILDRUNS_ROUTE
        envinfo['steprundetails_server_url'] = server_address + STEPRUN_DETAILS_ROUTE
        envinfo['rootruninfo_server_url'] = server_address + ROOT_RUN_INFO_ROUTE
    except Exception:
        pass
    envjson = json.dumps(envinfo)

    display_widget = display_graph_by_widget(graphjson=graphjson, lib_url=lib_url, visualize_id=visualize_id,
                                             container_id=widget_container_id, envjson=envjson, is_prod=is_prod,
                                             show_validate=show_validate, pipeline_graph_json=pipeline_graph_json)
    display(display_widget)
    time.sleep(1)

    insert_html = display_graph_by_insert(graphjson=graphjson, lib_url=lib_url, visualize_id=visualize_id,
                                          container_id=script_container_id, envjson=envjson, is_prod=is_prod,
                                          is_fallback=not ignore_fallback, show_validate=show_validate,
                                          pipeline_graph_json=pipeline_graph_json)
    display(insert_html)

    from ._run_status import _RunStatusVisualizer, _WidgetMessageProxy, _ScriptMessageProxy
    visualizer = _RunStatusVisualizer([_WidgetMessageProxy(instance=display_widget),
                                       _ScriptMessageProxy(container_id=container_id)], visualize_server)
    return visualizer


def _visualize_diff(graphyaml: dict, graphyaml_to_compare: dict, envinfo: dict = None, is_prod: bool = False):
    from IPython.display import display

    visualize_id = str(uuid4())
    container_id = "container_id_{0}".format(visualize_id)
    script_container_id = "{0}_script".format(container_id)

    lib_url = _get_ux_lib_url(is_prod)

    graphjson = json.dumps(graphyaml)
    graphjson_to_compare = json.dumps(graphyaml_to_compare)

    envinfo = envinfo if envinfo is not None else {}
    envinfo.setdefault("sdk_version", get_component_sdk_version())
    envjson = json.dumps(envinfo)
    loading_html = read_loading_content(visualize_id=visualize_id)

    insert_html = display_graph_by_insert(graphjson=graphjson, graphjson_to_compare=graphjson_to_compare,
                                          lib_url=lib_url, visualize_id=visualize_id,
                                          container_id=script_container_id, envjson=envjson,
                                          loading_html=loading_html, is_prod=is_prod)
    display(insert_html)


def _visualize_profiling(graphyaml: dict, profiling: dict, envinfo: dict = None, is_prod: bool = False):
    from IPython.display import display

    visualize_id = str(uuid4())
    container_id = "container_id_{0}".format(visualize_id)
    script_container_id = "{0}_script".format(container_id)

    lib_url = _get_ux_lib_url(is_prod)

    graphjson = json.dumps(graphyaml)
    profiling_json = json.dumps(profiling) if profiling is not None else 'null'

    envinfo = envinfo if envinfo is not None else {}
    envinfo.setdefault("sdk_version", get_component_sdk_version())
    envjson = json.dumps(envinfo)
    loading_html = read_loading_content(visualize_id=visualize_id)

    insert_html = display_graph_by_insert(graphjson=graphjson, profiling_json=profiling_json,
                                          lib_url=lib_url, visualize_id=visualize_id,
                                          container_id=script_container_id, envjson=envjson,
                                          loading_html=loading_html, is_prod=is_prod)
    display(insert_html)


def display_graph_by_widget(graphjson, lib_url, container_id, envjson, visualize_id, is_prod,
                            show_validate: bool, pipeline_graph_json="null"):
    from ._validation import ValidateView
    return ValidateView(graph_json=graphjson, env_json=envjson, lib_url=lib_url, container_id=container_id,
                        visualize_id=visualize_id, is_prod=is_prod, show_validate=show_validate,
                        pipeline_graph_json=pipeline_graph_json)


def read_loading_content(visualize_id):
    loading_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "js/loading.html")
    with open(loading_file) as f:
        loading_html = f.read()
    return '''
    <div id="loading-{visualize_id}">
        {loading_html}
    </div>
    '''.format(visualize_id=visualize_id, loading_html=loading_html)


def display_graph_by_insert(graphjson, lib_url, container_id, envjson, visualize_id, is_prod,
                            graphjson_to_compare="null", profiling_json="null", loading_html="",
                            is_fallback=False, show_validate: bool = False, pipeline_graph_json="null"):
    from IPython.display import HTML
    return HTML(
        '''
        <style>
        #{container_id} svg.react-dag-editor-svg-container {{
            height: 800px;
        }}
        </style>
        <div id="{container_id}"></div>
        <script>
            (function () {{
                if (!window._renderLock) {{
                    window._renderLock = {{}}
                }}
                if (window._renderLock["{visualize_id}"]) {{
                    return
                }}
                window._renderLock["{visualize_id}"] = "script"
                console.log("load as script", Date.now())
                window.render_container_id="{container_id}";
                window.graph_json={graphjson};
                window.graph_json_to_compare={graphjson_to_compare};
                window.profiling_json={profiling_json};
                window.env_json={envjson};
                window.is_prod={is_prod};
                window.is_fallback={is_fallback};
                window.show_validate={show_validate};
                window.pipeline_graph_json={pipeline_graph_json};
                window.before_script=performance.now();
                var script=document.createElement('script')
                script.onload=hideLoading
                script.src="{lib_url}"
                document.getElementById("{container_id}").appendChild(script)

                function hideLoading () {{
                    var style = document.createElement('style')
                    style.innerHTML = "#loading-{visualize_id} .ms-Spinner-root {{ display: none !important }}"
                    var container = document.getElementById("{container_id}");
                    if (container) {{
                        container.appendChild(style)
                    }}
                }}
            }})()
        </script>
        {loading_html}
        '''.format(graphjson=graphjson, graphjson_to_compare=graphjson_to_compare,
                   lib_url=lib_url, container_id=container_id, envjson=envjson,
                   visualize_id=visualize_id, profiling_json=profiling_json,
                   loading_html=loading_html, is_prod=int(is_prod),
                   is_fallback=int(is_fallback), show_validate=int(show_validate),
                   pipeline_graph_json=pipeline_graph_json)
    )


def _get_ux_lib_url(is_prod: bool):
    env_defined_url = os.getenv(AZUREML_SDK_UI_URL_ENV_NAME)
    if env_defined_url is not None:
        return env_defined_url
    return _get_ux_prod_lib_url() if is_prod else _get_ux_test_lib_url()


def _get_ux_test_lib_url():
    return 'https://yucongj-test.azureedge.net/libs/test/index.js?t={}'.format(int(time.time()))


def _get_ui_version_set():
    env_defined_version = os.getenv(AZUREML_SDK_UI_VERSION_SET_ENV_NAME)
    if enabled_subpipeline_registration():
        default_version = "~=0.2.0"
    else:
        default_version = "~=0.1.0"

    if env_defined_version is not None:
        print("get ui version set from environment:", env_defined_version)
        return env_defined_version
    else:
        return default_version


@track(activity_name='_get_ux_prod_lib_url')
def _get_ux_prod_lib_url():
    try:
        from packaging.version import parse
        from packaging.specifiers import SpecifierSet
    except ImportError as e:
        print("Couldn't import {0}. Please ensure {0} is installed."
              "Try install azure-ml-component[notebooks].".format(e.name))
        raise e

    # update specifier every time release
    specifier_set = SpecifierSet(_get_ui_version_set())

    account_name = "yucongjteststorage"
    prod_prefix = "prod"
    container_name = "libs"
    blobs_list = try_get_blobs_list(account_name=account_name,
                                    container_name=container_name,
                                    prod_prefix=prod_prefix)

    result_version = None
    for blob in blobs_list:
        path_list = _split_all(blob)

        if len(path_list) >= 2 and path_list[0] == prod_prefix:
            version_str = path_list[1]
            version = parse(version_str)

            result_version = version if version in specifier_set and \
                (result_version is None or version > result_version) else result_version

    if result_version is None:
        raise Exception("cannot find target version")

    result_version_str = str(result_version)
    _LoggerFactory.trace(_get_logger(), "Pipeline_fetch_ux_production_bundle", {
        'result_version': result_version_str
    })

    return 'https://yucongj.azureedge.net/libs/prod/{0}/index.js'.format(result_version_str)


def try_get_blobs_list(account_name: str, container_name: str, prod_prefix: str):
    try:
        try:
            return get_blobs_list_by_v12(account_name=account_name,
                                         container_name=container_name,
                                         prod_prefix=prod_prefix)
        except ImportError:
            return get_blobs_list_by_v2(account_name=account_name,
                                        container_name=container_name,
                                        prod_prefix=prod_prefix)
    except ImportError as e:
        print("Couldn't import expected version of 'azure-storage-blob'."
              "Please ensure 'azure-storage-blob' is installed."
              "Try install azure-ml-component[notebooks].".format(e.name))
        raise e


def get_blobs_list_by_v12(account_name: str, container_name: str, prod_prefix: str):
    from azure.storage.blob import ContainerClient

    container_url = "https://{}.blob.core.windows.net/{}".format(account_name, container_name)
    container_client = ContainerClient.from_container_url(container_url)
    blobs_list = container_client.list_blobs(name_starts_with=prod_prefix)
    return [blob.name for blob in blobs_list]


def get_blobs_list_by_v2(account_name: str, container_name: str, prod_prefix: str):
    from azure.storage.blob import BlockBlobService

    block_blob_service = BlockBlobService(account_name=account_name)
    blobs_list = list(block_blob_service.list_blob_names(container_name=container_name, prefix=prod_prefix))
    return blobs_list


# copy from https://www.oreilly.com/library/view/python-cookbook/0596001673/ch04s16.html
def _split_all(path):
    allparts = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == path:  # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])
    return allparts
