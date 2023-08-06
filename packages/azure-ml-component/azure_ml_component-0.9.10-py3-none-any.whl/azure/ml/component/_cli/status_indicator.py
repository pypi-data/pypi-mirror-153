# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

from threading import Thread
from functools import wraps
import time


class ThreadWithReturnValue(Thread):
    """A Thread that returns the result of the target function.
    Thanks to:
        - https://stackoverflow.com/a/6894023
        - https://stackoverflow.com/a/31614591
    """
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}):
        # always pass daemon=True to catch keyboardInterrupt signal.
        Thread.__init__(self, group, target, name, args, kwargs, daemon=True)
        self._return = None
        self._exc = None

    def run(self):
        try:
            if self._target is not None:
                self._return = self._target(*self._args, **self._kwargs)
        except BaseException as e:
            self._exc = e

    def join(self, *args):
        Thread.join(self, *args)
        if self._exc:
            raise self._exc
        return self._return


def _get_cli_progress_hook(determinant, logger_name=None):
    try:
        import azure.cli.core.commands.progress as progress
        progress_hook = progress.ProgressHook()
        progress_hook.init_progress(progress.get_progress_view(determinant))
    except Exception as e:
        import logging
        # Must start from 'cli' to be controlled by the azure cli's logging handler
        logger = logging.getLogger(logger_name)
        logger.debug('Failed to load progress indicator:' + str(e))
        progress_hook = None

    return progress_hook


class StatusIndicator(object):
    def __init__(self, progress_hook, auto_flush):
        self._hook = progress_hook
        self._auto_flush = auto_flush

    def update(self, message=None, total_val=None, value=None):
        if total_val and value is not None and total_val > 0 and value >= 0:
            percent = max(0, min(value / total_val, 1))
            # use hook.reporter.add here to not flush immediately
            self._hook.reporter.add(message="{} {:.1%}".format(message, percent), total_val=total_val, value=value)
        else:
            self._hook.reporter.add(message=message)

        if self._auto_flush:
            self._hook.update()


def status_indicator(action_name=None, indicator_var_name=None):
    """A decorator to show status indicator in the CLI,
    used to indicate progress while doing a time-consuming task."""

    progress_hook = _get_cli_progress_hook(determinant=False, logger_name='cli.status_indicator')

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not progress_hook:
                return func(*args, **kwargs)

            if indicator_var_name:
                kwargs.update({indicator_var_name: StatusIndicator(progress_hook, auto_flush=False)})

            thread = ThreadWithReturnValue(target=func, args=args, kwargs=kwargs)
            progress_hook.begin(message=action_name)
            thread.start()

            while thread.is_alive():
                progress_hook.update()
                time.sleep(0.2)

            progress_hook.end()
            # Must use the `update` to get the outstream flushed,
            # otherwise the last status of the status indicator will keep to be shown on the terminal.
            progress_hook.update()
            return thread.join()

        return wrapper

    return decorator


def progress_indicator(action_name=None, indicator_var_name=None):
    """A decorator to show progress bar indicator in the CLI"""

    progress_hook = _get_cli_progress_hook(determinant=True, logger_name='cli.progress_indicator')

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not (progress_hook and indicator_var_name):
                return func(*args, **kwargs)

            kwargs.update({indicator_var_name: StatusIndicator(progress_hook, auto_flush=True)})

            # HACK: progress doesn't report if percent equals 0, we have to make it greater than 0 here.
            progress_hook.begin(message=action_name, total_val=1, value=0.00000001)
            try:
                return func(*args, **kwargs)
            finally:
                progress_hook.end()

        return wrapper

    return decorator
