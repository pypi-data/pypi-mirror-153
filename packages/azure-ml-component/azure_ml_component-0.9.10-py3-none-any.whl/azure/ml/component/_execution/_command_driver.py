# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import os
import sys
import runpy
import argparse
import subprocess
import traceback
import shlex
from os import name as os_name
from datetime import datetime
from urllib.parse import unquote

DSL_COMPONENT_EXECUTOR_MODULE = 'azure.ml.component.dsl.executor'


def print_log(msg):
    message = '[{}] Run execute stage: {}'.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), msg)
    print(message)


def check_return_code(return_code, successful_return_code):
    """
    Check whether command execution successful by return_code.
    If return code doesn't meet successful_return_code, it will raise SystemExit.

    :param return_code: Return code of command execution.
    :type return_code: int
    :param successful_return_code: Specify how command return code is interpreted, default value is Zero.
    :type successful_return_code: str
    """
    # print a blank line to distinguish user code log and _command_driver log.
    print()
    print_log("Command finished with return code {}".format(return_code))
    if return_code == 0:
        return
    if return_code >= 0 and successful_return_code == 'ZeroOrGreater':
        return
    sys.exit(return_code)


def _convert_command(command_list):
    """
    Convert command to subprocess executes command.
    If only one item in command_list, it will directly return first item as command. Else, in Windows,
    it will return directly. And in linux, it will convert list command to a shell-escaped string command.

    :param command_list: To be converted command.
    :type command_list: List
    :return command: Converted command.
    :rtype str or list
    """
    command = command_list[0] if len(command_list) == 1 else command_list
    if os_name != 'nt' and isinstance(command, list):
        # In Linux with shell=True, if command is a sequence, the first item specifies the command string,
        # and any additional items will be treated as additional arguments to the shell itself.
        # So need to connect command when shell=True.
        command = ' '.join([shlex.quote(item) for item in command])
    return command


def execute_command(command):
    """
    Execute command in subprocess and get return code.

    :param command: To be executed command.
    :type command: List
    :return return_code: Return code of execution.
                         For windows, it will return 32-bit int. For linux, return code range is 0-255.
    :rtype int
    """
    # Refer to the logic of executing component command in the context_manager_injector.py
    # https://msdata.visualstudio.com/Vienna/_git/vienna?path=%2Fsrc%2Fazureml-api%2Fsrc%2FExecution%2FServices%2FControlContent%2FCommon%2Fcontext_manager_injector.py&version=GBmaster&line=203&lineEnd=217&lineStartColumn=33&lineEndColumn=70&lineStyle=plain&_a=contents
    command = _convert_command(command)
    print_log('Preparing to execute %s command: %s' % ('Windows' if os.name == 'nt' else 'Linux', command))
    # print a blank line to distinguish user code log and _command_driver log.
    print()

    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        cwd=os.getcwd(), bufsize=1, encoding='utf-8', shell=True,
        executable=(None if os_name == 'nt' else '/bin/bash'))

    # Because stdout.readline will hang up to wait for output, needn't to sleep in loop.
    for line in iter(process.stdout.readline, ''):
        print(line)
    # Wait for process to terminate
    return_code = process.wait()

    # Return code is unsigned int in Python, if the result code is negative it will be interpreted as unsigned int.
    import ctypes
    return_code = ctypes.c_int32(return_code).value
    return return_code


def execute_python_script(python_command):
    """
    Execute python script and get return code.

    :param python_command: To be executed command.
    :type python_command: List
    """
    # If is dsl.component command, use executor to run.
    is_dsl_component_command = DSL_COMPONENT_EXECUTOR_MODULE in python_command and python_command[1] == '-m'
    # Refer to the logic of execution python script in the context_manager_injector.py
    # https://msdata.visualstudio.com/Vienna/_git/vienna?path=%2Fsrc%2Fazureml-api%2Fsrc%2FExecution%2FServices%2FControlContent%2FCommon%2Fcontext_manager_injector.py&version=GBmaster&line=224&lineEnd=224&lineStartColumn=29&lineEndColumn=88&lineStyle=plain&_a=contents
    argv_start = 1 if not is_dsl_component_command else python_command.index(DSL_COMPONENT_EXECUTOR_MODULE)
    expand_invocation = []
    for item in python_command[argv_start:]:
        item = os.path.expandvars(item)
        expand_invocation.append(item)
    sys.argv = expand_invocation
    if is_dsl_component_command:
        print_log('Preparing to call script [%s] with arguments: %s' % (sys.argv[0], sys.argv[1:]))
    else:
        print_log('Preparing to run [%s] module with arguments: %s' % (DSL_COMPONENT_EXECUTOR_MODULE, sys.argv))
    # print a blank line to distinguish user code log and _command_driver log.
    print()

    try:
        if is_dsl_component_command:
            runpy.run_module(DSL_COMPONENT_EXECUTOR_MODULE, globals(), run_name="__main__")
        else:
            runpy.run_path(sys.argv[0], globals(), run_name="__main__")
    finally:
        # print a blank line to distinguish user code log and _command_driver log.
        print()


# Refer to strip_stack_of_azureml_layers in the context_manager_injector.py
# https://msdata.visualstudio.com/Vienna/_git/vienna?path=%2Fsrc%2Fazureml-api%2Fsrc%2FExecution%2FServices%2FControlContent%2FCommon%2Fcontext_manager_injector.py&version=GBmaster&line=376&lineEnd=419&lineStartColumn=7&lineEndColumn=34&lineStyle=plain&_a=contents
def print_strip_stack_of_traceback():
    """
    The actual traceback that gets printed when the exception is in the user code is:

        Traceback (most recent call last):
            File "/mnt/_execution/_command_driver.py", line 91, in <module>
                execute_python_script(command)
            File "/mnt/_execution/_command_driver.py", line 73, in execute_python_script
                runpy.run_path(sys.argv[0], globals(), run_name="__main__")
            File "<PYTHON_PATH>/runpy.py", line 265, in run_path
                return _run_module_code(code, init_globals, run_name,
            File "<PYTHON_PATH>/runpy.py", line 97, in _run_module_code
                _run_code(code, mod_globals, init_globals,
            File "<PYTHON_PATH>/runpy.py", line 87, in _run_code
                exec(code, run_globals)
            File "test.py", line 8, in <module>
                raise Exception('exception_msg')
        Exception: exception_msg

    however we strip the first 5 layers to give the user a traceback that only contains the user code as part of it
    """
    exc_type, exc_val, exc_traceback = sys.exc_info()
    traceback_as_list = traceback.format_exception(exc_type, exc_val, exc_traceback)
    reversed_traceback_list = reversed(traceback_as_list)
    reversed_trimmed_stack = []
    # currently the innermost runpy stack occurs inside runpy.py in _run_code and inside the exec(code, run_globals)
    # function if that changes then the regular stack will be printed
    keywords_in_innermost_runpy_stack_frame = ["runpy.py", "_run_code", "exec(code, run_globals)"]
    error_is_in_user_code = False
    for stack_frame in reversed_traceback_list:
        if all([keyword in stack_frame for keyword in keywords_in_innermost_runpy_stack_frame]):
            error_is_in_user_code = True
            break
        reversed_trimmed_stack.append(stack_frame)
    if error_is_in_user_code:
        # Find the first index of "Traceback (most recent call last):" in reversed list and append the cause exceptions
        # This will handle users using 'from with raise' when raising exception
        reversed_traceback_as_list = traceback_as_list[::-1]
        traceback_indexes = [idx for idx, stack_frame in enumerate(reversed_traceback_as_list)
                             if "Traceback (most recent call last):" in stack_frame]
        if len(traceback_indexes) > 0:
            reversed_trimmed_stack.extend(reversed_traceback_as_list[traceback_indexes[0]:])

    trimmed_stack = list(reversed(reversed_trimmed_stack))
    print("".join(trimmed_stack))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--command')
    parser.add_argument('--successful_return_code', default='Zero')
    parser.add_argument('--is_command')
    args, extra_args = parser.parse_known_args()
    command = [unquote(item) for item in args.command.split(' ')]
    is_command = False if args.is_command is not None and args.is_command.lower() == 'false' else True

    # add user script directory to the top of sys.path for user module imports
    sys.path.insert(0, os.getcwd())

    try:
        if not is_command:
            execute_python_script(command)
        else:
            return_code = execute_command(command)
            check_return_code(return_code, args.successful_return_code)
    except SystemExit as ex:
        if ex.code is not None and ex.code != 0:
            print_log('Command run failed with SystemExit exception, exit code: %s' % ex.code)
            print_strip_stack_of_traceback()
            raise
    except BaseException:
        print_log('Command run failed with Exception.')
        print_strip_stack_of_traceback()
        sys.exit(1)
