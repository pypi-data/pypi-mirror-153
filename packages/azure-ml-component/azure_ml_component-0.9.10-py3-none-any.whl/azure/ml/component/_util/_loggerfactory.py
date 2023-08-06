# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import contextlib
import logging
import logging.handlers
import inspect
import uuid
import json
import os
from threading import currentThread
import time
from contextlib import contextmanager
from datetime import datetime
from functools import wraps
from typing import Callable, Any, TypeVar
from ._utils import _str_to_bool
from ._exceptions import get_error_category, ErrorCategory, UserErrorException, _is_wrong_func_call_traceback
from ._telemetry import TelemetryMixin, WorkspaceTelemetryMixin, RequestTelemetryMixin

_PUBLIC_API = 'PublicApi'

COMPONENT_NAME = 'azure.ml.component'
session_id = 'l_' + str(uuid.uuid4())
default_custom_dimensions = {}
ActivityLoggerAdapter = None
IS_IN_CI_PIPELINE = _str_to_bool(os.environ.get("IS_IN_CI_PIPELINE", 'False'))
IS_LONG_RUNNING = 'is_long_running'
TIMER_LOGGING_THRESHOLD = 10


try:
    from azureml.core import Workspace
    from azureml.telemetry import get_telemetry_log_handler
    from azureml.telemetry.activity import ActivityType, ActivityLoggerAdapter, ActivityCompletionStatus
    from azureml.telemetry.logging_handler import AppInsightsLoggingHandler
    from azureml.telemetry._customtraceback import format_exc
    from azureml._base_sdk_common import _ClientSessionId

    session_id = _ClientSessionId

    telemetry_enabled = True
    DEFAULT_ACTIVITY_TYPE = ActivityType.INTERNALCALL
except Exception:
    telemetry_enabled = False
    DEFAULT_ACTIVITY_TYPE = 'InternalCall'


class _LoggerFactory:
    _component_version = None
    _core_version = None
    _dataprep_version = None

    @staticmethod
    def get_logger(name=COMPONENT_NAME, verbosity=logging.INFO):
        logger = logging.getLogger(name)
        logger.propagate = False
        # Set the logger level to debug to avoid not handling the app insight logs.
        logger.setLevel(logging.DEBUG)
        if not _LoggerFactory._find_handler(logger, logging.StreamHandler):
            # Expose component SDK log to terminal.
            handler = logging.StreamHandler()
            formatter = logging.Formatter("[%(asctime)s][%(name)s][%(levelname)s] - %(message)s")
            handler.setFormatter(formatter)
            handler.setLevel(verbosity)
            logger.addHandler(handler)
        if telemetry_enabled:
            if not _LoggerFactory._find_handler(logger, AppInsightsLoggingHandler):
                handler = get_telemetry_log_handler(component_name=COMPONENT_NAME)
                # Set the handler level to debug to avoid not handling the app insight logs.
                handler.setLevel(logging.DEBUG)
                logger.addHandler(handler)
        return logger

    @staticmethod
    def track_activity(logger, activity_name, activity_full_name=None,
                       activity_type=DEFAULT_ACTIVITY_TYPE, input_custom_dimensions=None,
                       flush=False, record_inner_depth=1):
        _LoggerFactory._get_version_info()

        if input_custom_dimensions is not None:
            custom_dimensions = default_custom_dimensions.copy()
            custom_dimensions.update(input_custom_dimensions)
        else:
            custom_dimensions = default_custom_dimensions
        custom_dimensions.update({
            'source': COMPONENT_NAME,
            'version': _LoggerFactory._component_version,
            'dataprepVersion': _LoggerFactory._dataprep_version,
            'coreVersion': _LoggerFactory._core_version,
        })
        if telemetry_enabled:
            return _log_activity(
                logger, activity_name, activity_full_name, activity_type, custom_dimensions, flush, record_inner_depth)
        else:
            return _log_local_only(logger, activity_name, activity_full_name, activity_type, custom_dimensions)

    @staticmethod
    def trace(logger, message, custom_dimensions=None, adhere_custom_dimensions=True):
        # Put custom_dimensions inside logger for future use
        if adhere_custom_dimensions:
            _LoggerFactory.add_track_dimensions(logger, custom_dimensions=custom_dimensions)
        payload = dict(pid=os.getpid())
        payload.update(custom_dimensions or {})
        payload['version'] = _LoggerFactory._component_version
        payload['source'] = COMPONENT_NAME

        if ActivityLoggerAdapter:
            activity_logger = ActivityLoggerAdapter(logger, payload)
            activity_logger.debug(message)
        else:
            logger.debug('Message: {}\nPayload: {}'.format(message, json.dumps(payload)))

    @staticmethod
    def add_track_dimensions(logger, custom_dimensions):

        """
        Add custom dimensions for logger to use when using @track.
        By using `@track` we are limited to extract custom dimensions from parameters or static values.
        If we need to add more dimensions inside the method being tracked, we need to add custom dimensions manually.
        Here is an example:
        .. code-block:: python
            @track(_get_logger, activity_type=_PUBLIC_API)
            def submit(self, ...):
                # submit the pipeline
                run_id = ...
                # record the run id
                _LoggerFactory.add_track_dimension({"run_id": run_id})
        :param logger: The logger.
        :param custom_dimensions: The custom dimensions needed.
        """
        assert logger is not None
        update_stackframe_info(custom_dimensions=custom_dimensions)

    @staticmethod
    def _find_handler(logger, handler_type):
        for log_handler in logger.handlers:
            if isinstance(log_handler, handler_type):
                return log_handler
        return None

    @staticmethod
    def _get_version_info():
        if _LoggerFactory._core_version is not None and _LoggerFactory._dataprep_version is not None \
                and _LoggerFactory._component_version is not None:
            return

        core_ver = _get_package_version('azureml-core')
        if core_ver is None:
            # only fallback when the approach above fails, as azureml.core.VERSION has no patch version segment
            try:
                from azureml.core import VERSION as core_ver
            except Exception:
                core_ver = ''
        _LoggerFactory._core_version = core_ver

        dprep_ver = _get_package_version('azureml-dataprep')
        if dprep_ver is None:
            try:
                from azureml.dataprep import __version__ as dprep_ver
            except Exception:
                # data-prep may not be installed
                dprep_ver = ''
        _LoggerFactory._dataprep_version = dprep_ver

        component_ver = _get_package_version('azure-ml-component')
        if component_ver is None:
            try:
                from azure.ml.component._version import VERSION as component_ver
            except Exception:
                component_ver = ''
        _LoggerFactory._component_version = component_ver


# hint vscode intellisense
_TFunc = TypeVar("_TFunc", bound=Callable[..., Any])


_telemetry_logger = None


def _get_telemetry_logger():
    """Get logger to log telemetry, returned logger only log to AppInsight."""

    global _telemetry_logger
    if _telemetry_logger is not None:
        return _telemetry_logger
    _telemetry_logger = _LoggerFactory.get_logger()
    return _telemetry_logger


def format_trace_back():
    try:
        return format_exc()
    except BaseException as e:
        return f"Failed to format trace back due to {e}"


def track(
        get_logger=_get_telemetry_logger,
        activity_type=DEFAULT_ACTIVITY_TYPE,
        activity_name=None,
        flush=False,
        record_inner_depth=1,
        is_long_running=False):

    def monitor(func: _TFunc) -> _TFunc:
        @wraps(func)
        def wrapper(*args, **kwargs):
            custom_dimensions = {}
            # Here we try to get necessary context info from the actual parameters passed in
            # This is kind of dangerous because @track might be used in various ways. And we do not really
            # have enough information to determine the actual context. The best we can do is to guess
            # based on the first parameter passed in.
            _self = None
            if len(args) > 0:
                _self = args[0]
            # Special handling for workspace
            if len(kwargs) > 0 and 'workspace' in kwargs.keys():
                _self = kwargs['workspace']

            extracted_dimension = {}
            if _self is not None:
                # 1. When used in a instance method, we check if the class is instance of `TelemetryMixin` and get
                #    the context we need. This is the most common use case. For example:
                #
                #       @track(...)
                #       def submit(self, ...):
                #           pass
                if isinstance(_self, TelemetryMixin):
                    # If the class is an instance of RequestTelemetryMixin, refresh the request id.
                    if isinstance(_self, RequestTelemetryMixin):
                        _self._refresh_request_id_for_telemetry()

                    extracted_dimension.update(_self._get_telemetry_values())
                    # Loop through MRO to collect all telemetry values
                    for _cls in _self.__class__.__mro__:
                        if issubclass(_cls, TelemetryMixin) and _cls != TelemetryMixin:
                            from azure.ml.component import Pipeline
                            if _cls == Pipeline:
                                extracted_dimension.update(
                                    WorkspaceTelemetryMixin._get_telemetry_value_from_workspace(_self.workspace))
                            else:
                                extracted_dimension.update(super(_cls, _self)._get_telemetry_values())
                # 2. When used with a @staticmethod or just a plain function, _self is the first parameter and we can
                #    safely get the context from it. Right now `azureml.core.Workspace` is the most used type,
                #    so we will extract context from it. For example:
                #
                #       @staticmethod
                #       @track(...)
                #       def list(workspace: Workspace):
                #           pass
                elif isinstance(_self, Workspace):
                    _most_recent_context.update({'workspace': _self})
                    extracted_dimension.update(WorkspaceTelemetryMixin._get_telemetry_value_from_workspace(_self))
                # 3. When used with a @classmethod, _self will be the class it's called from. We can not get anything
                #    useful in this case. For example:
                #       @classmethod
                #       @track(...)
                #       def some_class_method(cls, ...):
                #           pass
                elif inspect.isclass(_self):
                    pass

            # If we fail to get any dimension, try recently used context.
            if len(extracted_dimension) == 0 and _most_recent_context.get('workspace') is not None:
                extracted_dimension.update(WorkspaceTelemetryMixin._get_telemetry_value_from_workspace(
                    _most_recent_context.get('workspace')))
                extracted_dimension.update({'env_from_recent_context': True})

            custom_dimensions.update(extracted_dimension)
            custom_dimensions[IS_LONG_RUNNING] = is_long_running
            logger = get_logger()
            _activity_name = activity_name if activity_name is not None else func.__qualname__.replace('.', '_')
            _activity_full_name = '{}.{}'.format(func.__module__, func.__qualname__)
            with _LoggerFactory.track_activity(logger, _activity_name, _activity_full_name,
                                               activity_type, custom_dimensions, flush, record_inner_depth) as al:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if 'request_id' in extracted_dimension:
                        # Attach request_id to exception to propagate it
                        e.request_id = extracted_dimension['request_id']

                    # If the exception is raised due to the wrong use of the function.(e.g. f(unexpected_keyword=xx))
                    # We should convert it to a UserErrorException
                    original = e
                    if _is_wrong_func_call_traceback():
                        e = UserErrorException(exception_message=str(e), inner_exception=e)

                    al.activity_info['exception_type'] = type(e).__name__
                    # Note that only when telemetry_enabled we could use format_exc
                    if telemetry_enabled:
                        al.activity_info['exception_traceback'] = format_trace_back()
                    try:
                        category = get_error_category(e)
                        exception_detail = json.dumps(_get_exception_detail(e))
                    except Exception as inner_exception:
                        # For the case that an exception is raised when getting error category or serializing exception
                        # details, we treat it as an InternalSDKError and update the traceback with the full trace.
                        category = ErrorCategory.InternalSDKError
                        # In order to ensure the key-value pair of the inner exception detail is string,
                        # inner exception will be directly converted to string.
                        exception_detail = json.dumps({'error_message': str(inner_exception)})
                        al.activity_info['exception_traceback'] = format_trace_back()
                    al.activity_info['error_category'] = category.value
                    al.activity_info['exception_detail'] = exception_detail
                    # All the internal errors except for NotImplementedError will be wrapped with a new exception.
                    if IS_IN_CI_PIPELINE and category == ErrorCategory.InternalSDKError and \
                            not isinstance(e, NotImplementedError):
                        raise Exception('Got InternalSDKError', e) from original
                    # If a new exception is provided, raise it from the original one.
                    elif e != original:
                        raise e from original
                    else:
                        raise

        return wrapper

    return monitor


# activity_log_callstack type is {thread_id: callstack}, and each stackframe in callstack is decorated by track.
activity_log_callstack = {}


@contextlib.contextmanager
def timer_context(activity_name, is_long_running=False, force_record=False):
    start_time = datetime.utcnow()
    try:
        yield
    finally:
        end_time = datetime.utcnow()
        duration_ms = round((end_time - start_time).total_seconds() * 1000, 2)

        # only log the inner duration longer than 10ms to avoid long logging message
        if duration_ms > TIMER_LOGGING_THRESHOLD or force_record:
            inner_duration = {
                IS_LONG_RUNNING: is_long_running,
                'activity_name': activity_name,
                'duration_ms': duration_ms,
                'inner_durations': []}
            update_stackframe_inner_durations(inner_duration)


def timer(activity_name=None, is_long_running=False, force_record=False):
    # this decorator used to track function call's duration
    # and update the duration to the upper stack frame if any
    # do not decorate function with both track and timer at the same time
    def decorator(func: _TFunc) -> _TFunc:
        @wraps(func)
        def wrapper(*args, **kwargs):
            _activity_name = activity_name if activity_name is not None else func.__qualname__.replace('.', '_')
            with timer_context(_activity_name, is_long_running, force_record):
                return func(*args, **kwargs)
        return wrapper
    return decorator


def push_stackframe(activity_name):
    # Add new stackframe in current thread callstack
    # This method is thread-safe. Different threads will use different keys in activity_log_callstack,
    # so only one thread can update this callstack.
    thread_id = currentThread().ident
    if thread_id not in activity_log_callstack:
        activity_log_callstack[thread_id] = []
    activity_log_callstack[thread_id].append({'activity_name': activity_name})


def update_stackframe_info(**kwargs):
    """
    Update current stackframe info. The kwargs are update stackframe info such as inner_durations, custom_dimensions.
    This method is thread-safe. Different threads will use different keys in activity_log_callstack,
    so only one thread can update this callstack.
    """
    thread_id = currentThread().ident
    if thread_id in activity_log_callstack and len(activity_log_callstack[thread_id]) > 0:
        activity_log_callstack[thread_id][-1].update(kwargs)


def get_current_stackframe_info(key, default_value=None):
    thread_id = currentThread().ident
    if thread_id in activity_log_callstack:
        current_stackframe = activity_log_callstack[thread_id][-1]
        return current_stackframe[key] if key in current_stackframe else default_value
    else:
        return default_value


def pop_stackframe():
    # remove last stackframe and return its info
    # Each stackframe in callstack will store previous stackframe inner track, after popping
    # previous stackframe, will using previous stackframe inner track to update current stackframe.
    thread_id = currentThread().ident
    completed_activity_info = activity_log_callstack[thread_id].pop()
    if len(activity_log_callstack[thread_id]) == 0:
        activity_log_callstack.pop(thread_id)
    return completed_activity_info


def update_stackframe_inner_durations(pre_inner_durations):
    '''
    Update inner_durations which calls previous stackframe
    Here is an example:
    .. code-block:: python
        @track
        def f():
            g1()
            g2()
            g3()

        @track
        def g1():
            def @track
            def h1():
                pass
            h1()

        @track
        def g2():
            pass

        @timer()
        def g3():
            g4()

        @timer()
        def g4():
            pass

    inner durations of f will like this:
    [
        {
            activity_name: g1,
            duration: xxx,
            inner_durations: [{activity_name: h1, duration: xxx, inner_durations: []}]
        },
        {
            activity_name: g2,
            duration: xxx,
            inner_durations: []
        },
        {
            activity_name: g3,
            duration: xxx
        },
        {
            activity_name: g4,
            duration: xxx
        }
    ]
    :param pre_inner_durations: inner_durations of previous stackframe
    :type pre_inner_durations: list
    '''
    inner_durations = get_current_stackframe_info('inner_durations', [])
    if inner_durations is not None:
        inner_durations.append(pre_inner_durations)
        update_stackframe_info(inner_durations=inner_durations)


def generate_current_call_inner_durations(activity_name, custom_dimensions, inner_durations, duration_ms):
    """Generate inner durations of current call and update it to stack."""
    # Add is_long_running tag
    is_long_running = custom_dimensions.get(IS_LONG_RUNNING, False) or \
        any([item.get(IS_LONG_RUNNING, False) for item in inner_durations])

    current_call_inner_durations = {
        IS_LONG_RUNNING: is_long_running,
        'activity_name': activity_name,
        'duration_ms': duration_ms,
        'inner_durations': inner_durations}

    # Remove current stackframe from stack
    pop_stackframe()
    # Update inner_durations which calls this stackframe
    update_stackframe_inner_durations(current_call_inner_durations)
    return current_call_inner_durations


@contextmanager
def _log_activity(logger, activity_name, activity_full_name=None,
                  activity_type=DEFAULT_ACTIVITY_TYPE, custom_dimensions=None,
                  flush=False, record_inner_depth=1):
    activity_info = dict(activity_id=str(uuid.uuid4()), activity_name=activity_name, activity_type=activity_type)
    if activity_full_name is not None:
        activity_info.update({'activity_full_name': activity_full_name})

    custom_dimensions = custom_dimensions or {}
    activity_info.update(custom_dimensions)

    start_time = datetime.utcnow()
    completion_status = ActivityCompletionStatus.SUCCESS

    message = "ActivityStarted, {}".format(activity_name)
    activityLogger = ActivityLoggerAdapter(logger, activity_info)
    activityLogger.debug(message)
    exception = None

    # add activity to stack of activity_log_callstack
    push_stackframe(activity_name)

    try:
        yield activityLogger
    except Exception as e:
        exception = e
        completion_status = ActivityCompletionStatus.FAILURE
        raise
    finally:
        end_time = datetime.utcnow()
        duration_ms = round((end_time - start_time).total_seconds() * 1000, 2)

        # Add additional dimensions from logger and clear it after use.
        update_custom_dimensions = get_current_stackframe_info('custom_dimensions', None)
        if update_custom_dimensions:
            activityLogger.activity_info.update(update_custom_dimensions)

        # Common properties use camel case to name in AML SDK, such as completionStatus.
        # For other custom dimensions, will be named by snake case.
        activityLogger.activity_info["completionStatus"] = completion_status
        activityLogger.activity_info["durationMs"] = duration_ms
        inner_durations = get_inner_durations_by_depth(
            record_inner_depth,
            get_current_stackframe_info('inner_durations', []))
        activityLogger.activity_info["inner_durations"] = json.dumps(inner_durations)

        inner_durations = generate_current_call_inner_durations(
            activity_name, custom_dimensions, inner_durations, duration_ms)
        activityLogger.activity_info[IS_LONG_RUNNING] = inner_durations[IS_LONG_RUNNING]

        message = "ActivityCompleted: Activity={}, HowEnded={}, Duration={} [ms]".format(
            activity_name, completion_status, duration_ms)
        if exception:
            message += ", Exception={}".format(type(exception).__name__)
            activityLogger.debug(message)
        else:
            activityLogger.debug(message)

        if flush:
            # Get the AppInsightsLoggingHandler in logger.
            handler = _LoggerFactory._find_handler(logger, AppInsightsLoggingHandler)

            if handler:
                # Here flush() is an asynchronous method, which starts a thread that waits and sends
                # entries in the queue.
                handler.flush()
                # We sleep for one send_time(the timespan after which the worker thread will shutdown if receives
                # no entry) and one send_interval(the timespan at which the worker thread will check the queue for
                # entries) in order to flush the logging entries.
                # In case the handler is not what we expect, we surround this with a try-catch.
                try:
                    send_time = handler._default_client._channel.queue.sender.send_time
                    send_interval = handler._default_client._channel.queue.sender.send_interval
                    time.sleep(send_time + send_interval)
                except:
                    pass


@contextmanager
def _log_local_only(logger, activity_name, activity_full_name,
                    activity_type, custom_dimensions):
    activity_info = dict(activity_id=str(uuid.uuid4()), activity_name=activity_name, activity_type=activity_type)
    if activity_full_name is not None:
        activity_info.update({'activity_full_name': activity_full_name})

    custom_dimensions = custom_dimensions or {}
    activity_info.update(custom_dimensions)

    start_time = datetime.utcnow()
    completion_status = 'Success'

    message = 'ActivityStarted, {}'.format(activity_name)
    logger.debug(message)
    exception = None
    push_stackframe(activity_name)

    try:
        yield logger
    except Exception as e:
        exception = e
        completion_status = 'Failure'
        raise
    finally:
        end_time = datetime.utcnow()
        duration_ms = round((end_time - start_time).total_seconds() * 1000, 2)

        update_custom_dimensions = get_current_stackframe_info('custom_dimensions', None)
        if update_custom_dimensions and hasattr(logger, 'activity_info'):
            logger.activity_info.update(update_custom_dimensions)

        custom_dimensions['completionStatus'] = completion_status
        custom_dimensions['durationMs'] = duration_ms
        inner_durations = get_current_stackframe_info('inner_durations', [])
        message = '{} | ActivityCompleted: Activity={}, HowEnded={}, Duration={} [ms], Info = {}, ' \
            'InnerDurations = {}'.format(
                start_time, activity_name, completion_status, duration_ms, repr(activity_info), inner_durations)

        inner_durations = generate_current_call_inner_durations(
            activity_name, custom_dimensions, inner_durations, duration_ms)

        if exception:
            message += ', Exception={}; {}'.format(type(exception).__name__, str(exception))
            logger.debug(message)
        else:
            logger.debug(message)


def _get_package_version(package_name):
    import pkg_resources
    try:
        return pkg_resources.get_distribution(package_name).version
    except Exception:
        # Azure CLI exception loads azureml-* package in a special way which makes get_distribution not working
        try:
            all_packages = pkg_resources.AvailableDistributions()  # scan sys.path
            for name in all_packages:
                if name == package_name:
                    return all_packages[name][0].version
        except Exception:
            # In case this approach is not working neither
            return None


def _get_exception_detail(e: Exception):
    exception_detail = {}
    from azureml._restclient.models.error_response import ErrorResponseException

    # Handle HTTP error
    if isinstance(e, ErrorResponseException):
        if e.response is not None:
            exception_detail['http_status_code'] = e.response.status_code
        exception_detail['http_error_message'] = e.message

    # Handle exceptions with inner exception
    # msrest.exceptions.ClientRequestError & azureml._common.exception.AzureMLException
    if getattr(e, 'inner_exception', None):
        exception_detail['inner_exception_type'] = type(e.inner_exception).__name__
        if hasattr(e.inner_exception, 'message'):
            exception_detail['inner_exception_error_message'] = e.inner_exception.message

    # azureml._common.exception.AzureMLException
    if hasattr(e, '_error_code'):
        exception_detail['error_code'] = e._error_code
    if hasattr(e, 'request_id'):
        exception_detail['request_id'] = e.request_id

    # Other exceptions
    if hasattr(e, 'scrubbed_message'):
        exception_detail['error_message'] = e.scrubbed_message
    elif hasattr(e, 'message'):
        exception_detail['error_message'] = str(e.message)
    else:
        exception_detail['error_message'] = str(e)
    return exception_detail


_most_recent_context = {}


def get_inner_durations_by_depth(record_inner_depth, inner_durations):
    if record_inner_depth == 0 or not inner_durations:
        return []
    else:
        for item in inner_durations:
            item['inner_durations'] = get_inner_durations_by_depth(record_inner_depth - 1, item['inner_durations'])
    return inner_durations
