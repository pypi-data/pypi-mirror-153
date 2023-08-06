# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import os
import sys
import types
import traceback
from queue import Queue
from time import sleep
from threading import Lock, currentThread, Thread, Event
from pathlib import Path
from datetime import datetime
from ._constants import SLEEP_INTERVAL


LOG_FILE = 'log_file'
SHOW_TERMINAL = 'show_terminal'
TRACKER = 'tracker'
STOP_EVENT = 'stop_event'
MESSAGE = 'message'
UPLOAD_THREAD = 'upload_thread'


class Logger(object):
    """
    Logging message to local and remote log file by redirecting sys.stdout.
    """
    _instance_lock = Lock()
    tid_to_loginfo = {}
    _instance = None

    def __new__(cls, *args, **kwargs):
        # Singleton creation Logger
        with cls._instance_lock:
            if cls._instance is None:
                cls._sys_stdout = sys.stdout
                cls._sys_stderr = sys.stderr

                # When test case of Logger failed, it doesn't show test info. Since unittest also redirects sys.stdout,
                # some methods not exists in Logger. To handle this problem, will add attribute and method of
                # sys.stdout to Logger when initialize.
                # Set build-in method of sys.stdout to Logger
                for attr_name in dir(sys.stdout):
                    attr = getattr(sys.stdout, attr_name)
                    if attr_name not in dir(cls) and isinstance(attr, types.BuiltinMethodType):
                        add_method_to_class(cls, attr_name, attr)

                cls._instance = super(Logger, cls).__new__(Logger)
                # Set attribute of sys.stdout to Logger instance
                for attr_name in dir(sys.stdout):
                    if attr_name not in dir(cls._instance):
                        attr = getattr(sys.stdout, attr_name)
                        if not isinstance(attr, types.BuiltinMethodType):
                            setattr(cls._instance, attr_name, attr)
        return cls._instance

    def __init__(self, log_path, show_terminal=False, tracker=None):
        """
        Init logger of current thread. If tracker not None, it will start thread to streaming upload log.

        :param log_path: Log file path
        :type log_path: str
        :param show_terminal: If show_terminal=True, will print log in terminal.
        :type show_terminal: bool
        :param tracker: Used to upload logs to run history
        :type tracker: azure.ml.component._execution.RunHistoryTracker
        """
        Path(log_path).parent.mkdir(parents=True, exist_ok=True)
        tid = currentThread().ident
        loginfo = {
            # define logger file encoding using 'utf-8', else default encoding will be 'cp1252'
            LOG_FILE: open(log_path, "a", encoding='utf-8'),
            SHOW_TERMINAL: show_terminal,
            TRACKER: tracker,
            STOP_EVENT: Event(),
            MESSAGE: None
        }
        self.tid_to_loginfo[tid] = loginfo
        if tracker and tracker.track_run_history:
            loginfo[MESSAGE] = Queue()
            loginfo[UPLOAD_THREAD] = Thread(target=self._upload_logger_message, args=(tid,))
            loginfo[UPLOAD_THREAD].start()
        if sys.stdout != self:
            sys.stdout = self
        if sys.stderr != self:
            sys.stderr = self

    def set_show_terminal(self, show_terminal):
        tid = currentThread().ident
        self.tid_to_loginfo[tid][SHOW_TERMINAL] = show_terminal

    def get_log_path(self):
        tid = currentThread().ident
        return self.tid_to_loginfo[tid][LOG_FILE].name

    def write(self, message):
        """
        Overwrite sys.stdout.write, it will add timestamp in each line and write message to log file of current thread.
        If show_ternimal=True, will print message in terminal.
        """
        if message and message != '\n':
            message = '[{}] {}'.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message)
        elif not message:
            return
        self.write_message(message)

    def write_message(self, message='\n'):
        """
        Writing message to log file and ternimal.
        """
        tid = currentThread().ident
        if tid not in self.tid_to_loginfo:
            if hasattr(currentThread(), 'parent') and currentThread().parent.ident in self.tid_to_loginfo:
                tid = currentThread().parent.ident
            else:
                return
        if self.tid_to_loginfo[tid][SHOW_TERMINAL]:
            self._sys_stdout.write(message)
            self._sys_stdout.flush()
        self.tid_to_loginfo[tid][LOG_FILE].write(message)
        self.tid_to_loginfo[tid][LOG_FILE].flush()
        if self.tid_to_loginfo[tid][MESSAGE]:
            self.tid_to_loginfo[tid][MESSAGE].put(message)

    def flush(self):
        tid = currentThread().ident
        if tid in self.tid_to_loginfo:
            if self.tid_to_loginfo[tid][SHOW_TERMINAL]:
                self._sys_stdout.flush()
            self.tid_to_loginfo[tid][LOG_FILE].flush()

    def remove_current_thread(self):
        """Remove current thread in Logger and wait for uploading log completed."""
        log_info = self.tid_to_loginfo.pop(currentThread().ident, None)
        if log_info:
            log_info[LOG_FILE].close()
            if log_info[MESSAGE]:
                log_info[MESSAGE].join()
            log_info[STOP_EVENT].set()

        if len(self.tid_to_loginfo) == 0:
            sys.stdout = self._sys_stdout
            sys.stderr = self._sys_stderr

    def fileno(self):
        tid = currentThread().ident
        if tid in self.tid_to_loginfo.keys():
            return self.tid_to_loginfo[tid][LOG_FILE].fileno()
        else:
            raise ValueError('Cannot find thread_id: {} in Logger.'.format(tid))

    def print_to_terminal(self, message):
        """Only print message on terminal."""
        self._sys_stdout.write(message)
        self._sys_stdout.flush()

    def print_logfile(self):
        """Print logfile on terminal."""
        tid = currentThread().ident
        log_path = self.tid_to_loginfo[tid]['log_file'].name
        if os.path.exists(log_path):
            # Convert log path to long path
            long_name = Path(log_path).resolve().absolute().as_posix()
            print_str = "\n{}\n{}\n".format(long_name, '=' * len(long_name))
            with open(log_path, encoding='utf-8') as f:
                for line in f.readlines():
                    print_str += line
            self.print_to_terminal(print_str)

    def _upload_logger_message(self, tid):
        """
        Streamming upload logger message to run history.
        When stop event is set, it will stop uploading.
        """
        queue = self.tid_to_loginfo[tid][MESSAGE]
        tracker = self.tid_to_loginfo[tid][TRACKER]
        stop_event = self.tid_to_loginfo[tid][STOP_EVENT]
        while True and not stop_event.isSet():
            try:
                upload_message = ''
                while not queue.empty():
                    upload_message = upload_message + queue.get(block=False)
                    if not queue.empty():
                        queue.task_done()
                    else:
                        tracker.append_run_history_log(upload_message)
                        queue.task_done()
                        sleep(SLEEP_INTERVAL)
                        break
            except Exception as e:
                raise ValueError('Failed to upload execution info to run history log: {}'.format(e))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            traceback.print_exc()
        self.remove_current_thread()


def add_method_to_class(cls, method_name, method):
    """
    Add mehtod to Class dynamically.

    :param cls: the class which add method
    :type cls: class
    :param method_name: method name in cls
    :type method_name: str
    :param method: the method needed to add to cls
    :type method: typing.Callable
    """
    def delegated(self, *args, **kwargs):
        return method(*args, **kwargs)

    setattr(cls, method_name, delegated)
