# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import os
from configparser import ConfigParser
from azureml.exceptions import UserErrorException

_DEFAULT_NAMESPACE_CONFIG_KEY = 'module_namespace'


def _get_default_namespace():
    config = ConfigParser()
    config.read(os.path.expanduser(os.path.join('~', '.azure', 'config')))
    if config.has_section('defaults') and config.has_option('defaults', _DEFAULT_NAMESPACE_CONFIG_KEY):
        return config.get('defaults', _DEFAULT_NAMESPACE_CONFIG_KEY)
    else:
        raise UserErrorException(
            'Error, default namespace not set and --namespace parameter not provided.\n'
            'Please run "az configure --defaults {0}=<namespace>" to set default namespace, '
            'or provide a value for the --namespace parameter.'.format(_DEFAULT_NAMESPACE_CONFIG_KEY))


class ModuleCliError(Exception):
    """All the errors from module related commands will be wrapped as ModuleCliError."""

    def __init__(self, ex):
        message = ModuleCliError._readable_error_message(ex)
        super(ModuleCliError, self).__init__(message)

    @staticmethod
    def _readable_error_message(ex):
        """
        This function extracts human readable error message (that to be displayed on the CLI)
        from an Exception object.

        * For the exceptions have only one str argument, respect the argument as the readable message.
          which is most of the use case, such as:

            >>> ex = FileNotFoundError("File /path/to/the/file not found.")
            >>> _readable_error_message(ex)
            'File /path/to/the/file not found.'

            >>> from azureml.exceptions import UserErrorException
            >>> ex = UserErrorException("Workspace bad_workspace does not exist.")
            >>> _readable_error_message(ex)
            'Workspace bad_workspace does not exist.'

        * For other cases, respect the __repr__ of the ex.

            >>> ex = ZeroDivisionError()
            >>> _readable_error_message(ex)
            'ZeroDivisionError()'

            >>> import os, errno
            >>> ex = OSError(errno.EPERM, os.strerror(errno.EPERM))
            >>> _readable_error_message(ex)
            "PermissionError(1, 'Operation not permitted')"

            >>> ex = OSError(errno.EIO, os.strerror(errno.EIO))
            >>> _readable_error_message(ex)
            "OSError(5, 'Input/output error')"
        """
        if len(ex.args) == 1 and isinstance(ex.args[0], str):
            message = ex.args[0]
        else:
            message = ex.__repr__()
        return message


def _has_azure_ml_not_found_message(message):
    # Returns true if message contains azureml not found in it.
    # AzureMLException has special format, no module named xxx won't appear at the last line.
    return "No module named 'azure.ml" in message


def _has_user_error_message(message):
    # Returns true if message contains user error message in it.
    # Use code part to distinguish so subclass of UserErrorException can be included.
    return '"code": "UserError"' in message
