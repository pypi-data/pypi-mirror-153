# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import os
import io
import subprocess
import tarfile
import docker
import json
import time
from pathlib import Path, PurePosixPath, PureWindowsPath

from azureml.exceptions._azureml_exception import UserErrorException
from azureml._model_management._util import get_docker_client
from ._constants import TEST_COMMAND_EXECUTE_IN_WSL_OR_CONTAINER
from .._util._loggerfactory import track
from .._util._utils import _convert_to_shell_execution_command


def _is_in_container():
    path = '/proc/self/cgroup'
    return (
        os.path.exists('/.dockerenv') or
        os.path.isfile(path) and any('docker' in line for line in open(path))
    )


def _is_in_wsl1():
    process = subprocess.run(["systemd-detect-virt", "-c"], shell=True, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, bufsize=1, universal_newlines=True)
    return 'wsl' in process.stdout


def is_linux_container():
    """
    Check docker server whether support linux container.
    Using "docker info" to get the container os type which docker server support.

    :return is_linux_container: If support linux container, return True, else return False.
    :rtype bool
    """
    process = subprocess.Popen(
        'docker info --format "{{json .}}"',
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, encoding='utf-8')
    returncode = process.wait()
    process_stdout = process.stdout.read()
    error_msg = 'Cannot get os type from docker info. ' \
                'Please make sure docker installed and docker daemon is running. Detail message: %s.' % process_stdout
    try:
        docker_info = json.loads(process_stdout)
        if returncode == 0 and 'OSType' in docker_info:
            return docker_info['OSType'].lower() == 'linux'
        else:
            raise UserErrorException(error_msg)
    except:
        raise UserErrorException(error_msg)


class CommandExecution:
    """
    CommandExecution is used to execute command in local or container. When init CommandExecution, need to set command
    and execution environment. CommandExecution exposes interfaces, local_run, docker_run and docker_exec to
    execute command.
    """
    _is_in_wsl1_or_container = _is_in_container() or _is_in_wsl1()
    try:
        """Check current docker support linux container. If not found docker command, set _docker_available as false"""
        _is_linux_container = is_linux_container()
        _docker_available = True
    except Exception:
        _docker_available = False

    def __init__(
            self, command, command_environment, logger, cwd=None,
            environment_variables={}, volumes={}):
        """
        :param command: command to execute
        :type command: list or str
        :param command_environment: execution environment info
        :type command_environment: azure.ml.component._execution._component_environment.CommandEnvironment
        :param logger: log command execution output
        :type logger: azure.ml.component._execution._component_run_logger.Logger
        :param cwd: current directory when execute command
        :type cwd: str
        :param environment_variables: the environment variables for execute command
        :type environment_variables: dict
        :param volumes: volumes need to mount in container
        :type volumes: dict
        """
        self.command = command
        self.environment_variables = {} if environment_variables is None else environment_variables
        self.cwd = cwd
        self.logger = logger
        self.volumes = volumes
        self.command_environment = command_environment

    @track(is_long_running=True)
    def local_run(self):
        """
        Execute command in subprocess and streaming log output in logger.

        :return command_result: is command execute success
        :rtype bool
        """
        if not self._check_os_type('windows' if os.name == 'nt' else 'linux'):
            warning_msg = '[Warning] Component os type is %s, which is different from the host os type.' \
                % self.command_environment.os_type
            print(warning_msg)
        environment = {**os.environ, **self.environment_variables}
        command = _convert_to_shell_execution_command(self.command, self.command_environment.conda_environment_name)
        # Since different /bin/sh are used in different Linux systems,
        # specify executable to /bin/bash when run in linux.
        process = subprocess.Popen(
            command, env=environment, cwd=self.cwd, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, bufsize=1, universal_newlines=True, encoding='utf-8',
            shell=True, executable=(None if os.name == 'nt' else '/bin/bash')
        )
        # Because stdout.readline will hang up to wait for output, needn't to sleep in loop.
        for line in iter(process.stdout.readline, ''):
            self.logger.write_message(line)
        # Wait for process to terminate
        returncode = process.wait()
        return returncode == 0

    @track(is_long_running=True)
    def docker_run(self):
        """
        Execute command with the image and streaming log container output to logger.
        It's like command "docker run <image name> <command>".

        :return command_result: is command execute success
        :rtype bool
        """
        CommandExecution._assert_docker_available()
        self._assert_docker_support_os_type('linux' if self._is_linux_container else 'windows')
        # Set PYTHONUNBUFFERED=1 to force the stdout and stderr streams to be unbuffered.
        environment = {'PYTHONUNBUFFERED': 1, **self.environment_variables}
        try:
            docker_client = get_docker_client()
            if self._is_in_wsl1_or_container or (TEST_COMMAND_EXECUTE_IN_WSL_OR_CONTAINER in os.environ):
                container = docker_client.containers.create(
                    self.command_environment.image_name, working_dir=self.cwd, environment=environment,
                    stdin_open=True, tty=True)
                container.start()
                command_result = CommandExecution._docker_exec_in_wsl1_or_container(
                    container, self.command, self.volumes, self.logger)
            else:
                container = docker_client.containers.create(
                    self.command_environment.image_name, working_dir=self.cwd, environment=environment,
                    volumes=self.volumes, stdin_open=True, tty=True)
                container.start()
                command_result = CommandExecution.docker_exec(container, self.command, self.logger)
            container.stop()
            container.remove()
        except Exception as e:
            raise UserErrorException(str(e))
        return command_result == 0

    @staticmethod
    def _assert_docker_available():
        if not CommandExecution._docker_available:
            raise UserErrorException(
                "Cannot execute docker command in current environment, "
                "please make sure docker installed and docker daemon is running.")

    def _check_os_type(self, os_type):
        """Check host os type is equal component os type."""
        # default value of command_environment_os_type is linux.
        command_environment_os_type = 'linux' if not self.command_environment.os_type or \
            self.command_environment.os_type.lower() != 'windows' else 'windows'
        return command_environment_os_type == os_type

    def _assert_docker_support_os_type(self, os_type):
        """
        Check current environment docker is available, if not, will raise error.
        """
        CommandExecution._assert_docker_available()
        if not self._check_os_type(os_type):
            raise UserErrorException(
                'Current execution os type is %s, does not match command required os type, %s.'
                'Please check configuration of command execution os type.' % (
                    os_type, self.command_environment.os_type))

    @staticmethod
    def docker_exec(container, command, logger):
        """
        Execute command in an existing container, streaming log execution output.
        It's like command "docker exec <container name> <command>".

        :param container: container
        :type container: docker.container
        :param command: execute command in container
        :type command: list or str
        :param logger: log container output
        :type logger: azure.ml.component._execution._component_run_logger.Logger
        :return command_result: command run result, if not 0, may some error when execute
        :rtype int
        """
        CommandExecution._assert_docker_available()
        if isinstance(command, str):
            # Adding the prefix, 'bash -c' or 'CMD /C', is used to carries out the command specified by the string.
            # It will read and execute commands from string after processing the options.
            if CommandExecution._is_linux_container:
                command = ['bash', '-c', command]
            else:
                command = ['CMD', '/c', command]
        container_exec = docker.APIClient().exec_create(container.id, command)
        exec_output = docker.APIClient().exec_start(container_exec['Id'], stream=True)

        for line in exec_output:
            line = line.decode('utf-8')
            logger.write_message(line)
        # Get command exit code in container
        container_inspect = docker.APIClient().exec_inspect(container_exec['Id'])
        command_result = container_inspect['ExitCode']
        return command_result

    @staticmethod
    def _docker_exec_in_wsl1_or_container(container, command, volumes, logger):
        """
        In WSL1 and container, will execute docker command in host machine, so folder in WSL1/container
        cannot mount in docker container. Using "docker cp" to replace mounting, then using "docker exec"
        to execute command in extension container.

        :param container: container
        :type container: docker.container
        :param command: execute command in container
        :type command: list or str
        :param volumes: volumes need to mount in container
        :type volumes: dict
        :param logger: log container output
        :type logger: azure.ml.component._execution._component_run_logger.Logger
        :return command_result: command run result, if not 0, may some error when execute
        :rtype int
        """
        print('Warning: Running in WSL1 or container')
        # When copy file into running windows container, it will raise "filesystem operations against a running Hyper-V
        # container are not supported". Need to be stopped before file can be copied.
        if not CommandExecution._is_linux_container:
            container.stop()
        # copy code and data to container
        for key, item in volumes.items():
            _copy_to_container(container, key, item['bind'])
        if not CommandExecution._is_linux_container:
            container.start()

        # execute command
        command_result = CommandExecution.docker_exec(container, command, logger=logger)

        # copy reuslt to local
        if not CommandExecution._is_linux_container:
            container.stop()
        for key, item in volumes.items():
            if 'w' in item['mode']:
                _copy_from_container(container, item['bind'], key)
        return command_result


def _copy_to_container(container, path_in_host, path_in_container):
    """
    Copy file/folder from host to container.

    :param container: execute command in container
    :type container: docker.container
    :param path_in_host: path in host.
    :type path_in_host: str
    :param path_in_container: path in container
    :type path_in_container: str
    """
    # Consistent with docker cli operation, when mount path not exists will create as dir.
    if not Path(path_in_host).exists():
        Path(path_in_host).mkdir(parents=True, exist_ok=True)
    try:
        path_in_container = PurePosixPath(path_in_container) \
            if CommandExecution._is_linux_container else PureWindowsPath(path_in_container)
        relative_path = str(path_in_container.relative_to(path_in_container.anchor))
        archive_bytes = io.BytesIO()
        if Path(path_in_host).is_dir():
            with tarfile.open(fileobj=archive_bytes, mode='w') as archive_tar:
                archive_tar.add(path_in_host, arcname=relative_path)
        else:
            with tarfile.open(fileobj=archive_bytes, mode='w') as archive_tar:
                with open(path_in_host, 'rb') as f:
                    data = f.read()
                    data_tarinfo = tarfile.TarInfo(name=relative_path)
                    data_tarinfo.mtime = time.time()
                    data_tarinfo.size = len(data)
                    archive_tar.addfile(data_tarinfo, io.BytesIO(data))

        archive_bytes.seek(0)

        container.put_archive(path_in_container.anchor, archive_bytes)
    except docker.errors.APIError as e:
        raise UserErrorException('Copy {} to container has failed. Detail message: {}'.format(path_in_host, e))


def _copy_from_container(container, path_in_container, path_in_host):
    """
    Copy file/folder from container to host.

    :param container: execute command in container
    :type container: docker.container
    :param path_in_container: file/folder path in container.
    :type path_in_container: str
    :param path_in_host: file/folder path in host
    :type path_in_host: str
    """
    try:
        data_stream, _ = container.get_archive(path_in_container)
        tar_file = path_in_host + '.tar'
        with open(tar_file, 'wb') as f:
            for chunk in data_stream:
                f.write(chunk)
        with tarfile.open(tar_file, mode='r') as tar:
            for file_name in tar.getnames():
                tar.extract(file_name, os.path.dirname(path_in_host))
        os.remove(tar_file)
    except docker.errors.APIError as e:
        raise UserErrorException('Copy {} from container has failed. Detail message: {}'.format(path_in_container, e))
