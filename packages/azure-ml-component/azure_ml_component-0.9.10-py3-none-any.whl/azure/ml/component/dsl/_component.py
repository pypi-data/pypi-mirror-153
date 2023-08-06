# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""A wrapper to analyze function annotations, generate component specs, and run component in command line."""
import argparse
import contextlib
import copy
import importlib
import json
import multiprocessing
import os
import pathlib
import re
import sys
import tempfile
import inspect
import functools
import types
from dataclasses import is_dataclass, fields as get_dataclass_fields, asdict as dataclass_to_dict
from io import StringIO
from multiprocessing.pool import ThreadPool
from pathlib import Path
from typing import TypeVar, Callable, Any

from azure.ml.component._util._constants import LOCAL_PREFIX
from azure.ml.component._util._utils import _relative_to, dsl_component_execution
from azure.ml.component._util._yaml_utils import YAML
from azure.ml.component._core._component_definition import ComponentType, ComponentDefinition, \
    DistributedComponentDefinition
from azure.ml.component.dsl._component_generator import DSLCommandLineGenerator
from azure.ml.component.dsl._module_spec import SPEC_EXT, ParallelRunModuleSpec
from azure.ml.component.dsl._utils import _resolve_source_directory, \
    is_dsl_component, _import_component_with_working_dir, logger, _resolve_source_file, _dsl_custom_aml_ignore
from azure.ml.component._core._component_definition import CommandComponentDefinition, SweepComponentDefinition
from azure.ml.component._core._types import _InputFileList, Output, _Param, Input, _OutputFile, \
    _get_param_with_standard_annotation, String, _get_annotation_cls_by_type, _is_dsl_type_cls, _is_dsl_types
from azure.ml.component.environment import Environment
from azure.ml.component._util._exceptions import DSLComponentDefiningError, NoDslComponentError, \
    RequiredComponentNameError, TooManyDSLComponentsError, RequiredParamParsingError, UnsupportedError
from azureml.exceptions import UserErrorException

# hint vscode intellisense
_TFunc = TypeVar("_TFunc", bound=Callable[..., Any])
# AML ignore patterns
DSL_COMMAND_COMPONENT_CUSTOM_IGNORE_PATTERNS = ['__pycache__/']


def command_component(
    *, name=None, version='0.0.1', display_name=None, description=None, is_deterministic=None,
    tags=None, environment=None, code=None, distribution=None
):
    """Return a decorator which is used to declare a component with @dsl.command_component.

    A component is a reusable unit in an Azure Machine Learning workspace.
    With the decorator @dsl.command_component, a function could be registered as a component in the workspace.
    Then the component could be used to construct an Azure Machine Learning pipeline.
    The parameters of the decorator are the properties of the component spec,
    see https://aka.ms/azureml-component-specs.

    .. remarks::

        The following example shows how to use @dsl.command_component to declare a simple component.

        .. code-block:: python

            @dsl.command_component()
            def your_component_function(output: Output(), input: Input(), param='str_param'):
                pass

        The following example shows how to declare a component with detailed meta data.

        .. code-block:: python

            @dsl.command_component(name=name, version=version, namespace=namespace, description=description)
            def your_component_function(output: Output(), input: Input(), param='str_param'):
                pass

        The following example shows how to consumption the declared component function with dsl pipeline.

        .. code-block:: python

            # definition dsl pipeline with dsl.command_component function
            @dsl.pipeline()
            def your_pipeline_func(input, param):
                your_component_function(input=input, param=param)

            # create the pipeline
            pipeline = your_pipeline_func(your_input, 'your_str')

            # the dsl component will be registered anonymously
            pipeline.validate(workspace=your_workspace)

        With the Component.create, we could register the component to workspace explicitly.
        The following example shows how to register existing dsl component function.

        .. code-block:: python

            from azure.ml.component import Component

            # register dsl component
            your_registered_component_function = Component.create(
                function=your_component_function, version='0.0.1',
                set_as_default=True, workspace=target_workspace
            )

            # create component
            component = your_registered_component_function()

        With the dsl.command_component function, we could build a component specification yaml file.
        For more details of the component spec, see https://aka.ms/azureml-component-specs


    :param name: The name of the component. If None is set, function name is used.
    :type name: str
    :param description: The description of the component. If None is set, the doc string is used.
    :type description: str
    :param version: Version of the component.
    :type version: str
    :param display_name: Display name of the component.
    :type display_name: str
    :param is_deterministic: Specify whether the component will always generate the same result. The default value is
                             None, the component will be reused by default behavior, the same for True value. If
                             False, this component will never be reused.
    :type is_deterministic: bool
    :param tags: Tags of the component.
    :type tags: dict
    :param environment: Environment config of component, could be a yaml file path, a dict or an Environment object.
                        If None, a default conda with 'azureml-defaults' and 'azure-ml-component' will be used.
    :type environment: Union[str, os.PathLike, dict, azure.ml.component.Environment]
    :param code: The source directory of dsl.command_component, with default value '.'.
                 i.e. The directory of dsl component file.
    :type code: str
    :param distribution: The distribution config of dsl.command_component, e.g. distribution={'type': 'mpi'}.
    :type distribution: dict
    :return: The decorated function which could be used to create component directly.
    """
    if name and not CommandComponentDefinition.is_valid_name(name):
        msg = "Name is not valid, it could only contains a-z, A-Z, 0-9 and '.-_', got '%s'." % name
        raise DSLComponentDefiningError(msg)

    # Get the directory of decorator to resolve absolute code path in environment
    # Note: The decorator defined source directory may be different from dsl component source directory.
    decorator_defined_source_dir = _resolve_source_directory()
    # If is in dsl component execution process, skip resolve file path.
    environment = Environment() if dsl_component_execution() else \
        _refine_environment_to_obj(environment, decorator_defined_source_dir)
    if code:
        # Resolve code source immediately if defined with code.
        code = Path(decorator_defined_source_dir / code).resolve().absolute().as_posix()

    spec_args = {k: v for k, v in locals().items() if v is not None
                 and k in inspect.signature(command_component).parameters}

    from ..component import Component

    def component_func_decorator(func: _TFunc) -> _TFunc:
        if not isinstance(func, Callable):
            raise UserErrorException(f'Dsl component decorator accept only function type, got {type(func)}.')

        nonlocal spec_args
        spec_args = _refine_spec_args(spec_args)

        spec_args['name'] = spec_args.get('name', func.__name__)
        spec_args['display_name'] = spec_args.get('display_name', spec_args['name'])
        spec_args['description'] = spec_args.get('description', func.__doc__)
        func_entry_path = _resolve_source_file()
        if not func_entry_path:
            func_entry_path = Path(inspect.getfile(func)).resolve().absolute()
        # Fall back to func entry directory if not specified.
        spec_args['code'] = code if code else Path(func_entry_path).parent.absolute().as_posix()
        if not os.path.isdir(spec_args['code']):
            raise UserErrorException(
                f"Only folder can be supported as 'code' in dsl.component, got {spec_args['code']!r}")
        # Set entry name as relative path to code
        entry_relative_path = _relative_to(func_entry_path, spec_args['code'])
        if not entry_relative_path:
            raise UserErrorException(
                f"Dsl component {spec_args['name']!r} source directory {func_entry_path!r} "
                f"not under code directory {spec_args['code']!r}")
        entry_relative_path = entry_relative_path.as_posix()
        spec_args['command'] = [
            'python', '-m', 'azure.ml.component.dsl.executor',
            '--file', str(entry_relative_path), '--name', spec_args['name'],
            ComponentExecutor.EXECUTION_PARAMETERS_KEY]
        # Initialize a ComponentExecutor to make sure it works and use it to update the component function.
        # Save the raw func as we will wrap it
        raw_func = _copy_func(func)
        executor = ComponentExecutor(raw_func, spec_args, _entry_file=func_entry_path)
        executor._update_func(raw_func)
        _component_func = None

        @functools.wraps(raw_func)
        def wrapper(*args, **kwargs) -> Component:
            nonlocal _component_func
            if not _component_func:
                _component_func = Component.from_yaml(
                    yaml_file=executor._get_spec_file_path(),
                    additional_amlignore_file=_dsl_custom_aml_ignore(DSL_COMMAND_COMPONENT_CUSTOM_IGNORE_PATTERNS)
                )
            return _component_func(*args, **kwargs)

        wrapper._is_dsl_component = True
        wrapper._executor = executor
        wrapper._definition = executor.spec
        return wrapper

    return component_func_decorator


def _sweep_component(*, algorithm, search_space, objective, limits, early_termination=None,
                     name=None, version='0.0.1', display_name=None, description=None,
                     tags=None, is_deterministic=False):
    """(This feature is work-in-progress and related API interface may change at any time)
      Decorator which is used to declare a sweep component.

    A sweep component is a kind of component to enable user to automate efficient hyperparameter tuning.
    With the function dsl.sweep_component, a function could be registered as a sweep component in the workspace.
    The parameters of the decorator are the properties fo the component spec,
    refer to https://componentsdk.azurewebsites.net/components/sweep_component.html#reference if needed.

    The following example shows how to use dsl.sweep_component to declare a sweep component.

    .. code-block:: python

        from azure.ml.component import dsl
        from azureml.train.hyperdrive import choice
        from azureml.train.hyperdrive.policy import BanditPolicy

        # define a command component via dsl.command_component first, this component is referred to as trial component
        @dsl.command_component()
        def command_component_from_dsl(input_param1: int, input_param2: int)
            pass
        # declare sweep component
        sweep_component = dsl.sweep_component(
            algorithm='random',
            search_space={
                'input_param1': choice([0.01, 0.1]),
                'input_param2': choice([1, 2])
            },
            objective={
                'primary_metric': 'accuracy',
                'goal': 'maximize'
            },
            early_termination=BanditPolicy(
                evaluation_interval=1,
                slack_factor=0.1,
                delay_evaluation=5
            ),
            limits={
                'max_concurrent_trials': 2,
                'max_total_trials': 4
            }
        )(command_component_from_dsl)

    .. note ::

        The parameters defined in field `search_space` need to be already defined in trial component's inputs,
        otherwise a `DSLComponentDefiningError` will be thrown. In this example, parameter `input_param1` and
        `input_param2` are defined in function `command_component_from_dsl`, therefore this is a valid definition.

    The following code shows how to generate hyperparameter expression via methods in `azureml.train.hyperdrive`.
    For more information about hyperparameter expression, refer to
    https://componentsdk.azurewebsites.net/components/sweep_component.html#hyperparameter-expression

    .. code-block:: python

        from azureml.train.hyperdrive import choice, randint, uniform, quniform, normal, qnormal

        search_space = {
            'choice_parameter': choice(0.05, 0.1),
            'randint_parameter': randint(upper=5),
            'uniform_parameter': uniform(min_value=0.05, max_value=0.1),  # same for loguniform
            'quniform_parameter': quniform(min_value=0.2, max_value=0.8, q=3),  # same for qloguniform
            'normal_parameter': normal(mu=0.2, sigma=0.8),  # same for lognormal
            'qnormal_parameter': qnormal(mu=0.2, sigma=0.8, q=3)  # same for qlognormal
        }

    The following piece of code shows a sample of parameter `objective`, refer to
    https://componentsdk.azurewebsites.net/components/sweep_component.html#objective for more information.

    .. code-block:: python

        from azureml.train.hyperdrive import PrimaryMetricGoal

        # An objective sample, should consist of 'primary_metric' and 'goal'
        #   and metric should have been logged using run log
        objective = {
            'primary_metric': 'accuracy',
            'goal': PrimaryMetricGoal.MAXIMIZE  # or PrimaryMetricGoal.MINIMIZE
        }

    .. note ::

        Sweep component is inheritance of AzureML Component, its parameters follow AzureML component definition,
        refer to https://aka.ms/azureml-component-specs for detailed information.

    :param algorithm: Specify the parameter sampling methods to use over the hyperparameter search space.
                      Possible values are: 'random', 'grid', 'bayesian'.
    :type algorithm: str
    :param search_space: The range of values to search for each hyperparameter. Keys need be already defined
                         in trial component, and values should be hyperparamter expression. You can generate
                         hyperparameter expression using methods in `azureml.train.hyperdrive`.
    :type search_space: dict
    :param objective: Define primary metrics and goal. Should consist of fields 'primary_metric' and 'goal',
                      and the metric should be logged using run log. Value for 'goal' should be PrimaryMetricGoal.
    :type objective: dict
    :param limits: Control your resource budget by specifying resource limit like the maximum number of training runs.
                   Mandatory field is 'max_total_trials', 'max_concurrent_trials' and 'timeout_minutes' are optional.
    :type limits: dict
    :param early_termination: Automatically end poorly performing runs with an early termination policy.
    :type early_termination: azureml.train.hyperdrive.policy.EarlyTerminationPolicy
    :param name: Name of the component. If None is set, function name with prefix 'sweep' will be used.
    :type name: str
    :param version: Version of the component, default value is '0.0.1'.
    :type version: str
    :param display_name: Display name of the component.
    :type display_name: str
    :param description: Detailed description of the component.
    :type description: str
    :param tags: A list of key-value pairs to describe the different perspectives of the component.
    :type tags: dict
    :param is_deterministic: Specify whether the component will always generate the same result when
                             given the same input data, default value is False.
    :type is_deterministic: bool
    :return: The decorated function which works as a sweep component.
    """
    if algorithm not in {'random', 'grid', 'bayesian'}:
        msg = f"Algorithm is invalid, it could only be one of 'random', 'grid' or 'bayesian', got '{algorithm}'."
        raise DSLComponentDefiningError(msg)
    if name and not ComponentDefinition.is_valid_name(name):
        msg = f"Name is not valid, it could only contains a-z, A-Z, 0-9 and '.-_', got '{name}'."
        raise DSLComponentDefiningError(msg)

    # convert Enum to str
    if not isinstance(objective['goal'], str):
        objective['goal'] = objective['goal'].value.lower()

    spec_args = {k: v for k, v in locals().items()
                 if v is not None and k in inspect.signature(_sweep_component).parameters}
    spec_args['type'] = ComponentType.SweepComponent.value

    from ..component import Component

    def sweep_component_func_decorator(func: _TFunc) -> _TFunc:
        if not isinstance(func, Callable):
            raise UserErrorException(f'Dsl component decorator accept only function type, got {type(func)}.')
        if not hasattr(func, '_definition'):
            raise UserErrorException("Trial component function is invalid, decorate your local function "
                                     "with 'dsl.command_component' or use function returned by "
                                     "'Component.load' or 'Component.from_yaml'.")

        nonlocal spec_args
        spec_args = _refine_spec_args(spec_args)
        spec_args['trial_definition'] = getattr(func, '_definition')
        spec_args['name'] = spec_args.get('name', f"sweep_{spec_args['trial_definition'].name}")
        spec_args['display_name'] = spec_args.get('display_name', spec_args['name'])
        spec_args['description'] = spec_args.get('description', func.__doc__)

        # trial component comes from existing yaml or registered component
        spec_args['_is_dsl_component'] = getattr(func, '_is_dsl_component', False)
        if not spec_args['_is_dsl_component']:
            trial_definition = spec_args['trial_definition']
            if trial_definition.workspace:
                # ComponentDefinition owns workspace, snapshot exists on backend and download it to temp directory
                trial_definition.get_snapshot()
                spec_args['trial_spec_file'] = trial_definition.get_snapshot_spec_file_path()
            else:
                # ComponentDefinitely has no workspace, the trial component comes from local,
                #   manually create a snapshot using ComponentSource.
                from azure.ml.component._api._component_source import ComponentSource
                trial_component_yaml_file = os.path.join(trial_definition._snapshot_local_cache,
                                                         trial_definition._spec_file_path)
                component_source = ComponentSource.from_source(trial_component_yaml_file,
                                                               package_zip=None, logger=logger)
                # record trial spec file with path in snapshot folder
                snapshot_folder = component_source.snapshot._get_snapshot_folder()
                spec_args['trial_spec_file'] = Path(os.path.join(snapshot_folder,
                                                                 Path(trial_definition._spec_file_path).name))

        # validate all search_space are defined in trial component inputs
        trial_component_inputs = spec_args['trial_definition']._to_dict()['inputs'].keys()
        undefined_search_space_params = [search_space_param for search_space_param in spec_args['search_space']
                                         if search_space_param not in trial_component_inputs]
        if len(undefined_search_space_params) > 0:
            undefined_search_space_params_str = ','.join(undefined_search_space_params)
            raise DSLComponentDefiningError(f'Search space parameter {undefined_search_space_params_str} '
                                            f'not defined in trial components.')

        raw_func = _copy_func(func)
        executor = ComponentExecutor(raw_func, spec_args)
        executor._update_func(raw_func)
        _component_func = None

        @functools.wraps(raw_func)
        def wrapper(*args, **kwargs) -> Component:
            nonlocal _component_func
            if not _component_func:
                _component_func = Component.from_yaml(yaml_file=executor._get_spec_file_path().as_posix())
            return _component_func(*args, **kwargs)

        wrapper._is_dsl_component = True
        wrapper._executor = executor
        wrapper._definition = executor.spec
        return wrapper

    return sweep_component_func_decorator


_component = command_component


def _copy_func(f):
    """Copy func without deep copy as some method may contains fields can not be copied."""
    g = types.FunctionType(f.__code__, f.__globals__, name=f.__name__,
                           argdefs=f.__defaults__,
                           closure=f.__closure__)
    g = functools.update_wrapper(g, f)
    g.__kwdefaults__ = f.__kwdefaults__
    return g


def _refine_environment_to_obj(environment, dsl_component_source_dir) -> Environment:
    if isinstance(environment, dict):
        # Write into a temp file.
        path = tempfile.mktemp()
        environment = _refine_path_in_environment_dict(environment, dsl_component_source_dir)
        with open(path, 'w') as f:
            YAML().dump(environment, f)
        environment = path
    if isinstance(environment, (str, pathlib.Path)):
        environment = Path(dsl_component_source_dir) / environment
        environment = Environment(file=environment)
    if environment and not isinstance(environment, Environment):
        raise UserErrorException(
            f'Unexpected environment type {type(environment).__name__!r}, '
            f'expected str, path, dict or azure.ml.core.Environment object.')
    return environment


def _refine_path_in_environment_dict(env_dict: dict, source_dir: str) -> dict:
    """Refine relative path in env dict to abs path."""
    if 'conda' in env_dict:
        conda_dict = env_dict['conda']
        if 'pip_requirements_file' in conda_dict:
            conda_dict['pip_requirements_file'] = \
                (Path(source_dir) / conda_dict['pip_requirements_file']).resolve().absolute().as_posix()
        if 'conda_dependencies_file' in conda_dict:
            conda_dict['conda_dependencies_file'] = \
                (Path(source_dir) / conda_dict['conda_dependencies_file']).resolve().absolute().as_posix()
    if "docker" in env_dict and "build" in env_dict["docker"] and \
            "dockerfile" in env_dict["docker"]["build"]:
        dockerfile = env_dict["docker"]["build"]["dockerfile"]
        if dockerfile.startswith(LOCAL_PREFIX):
            env_dict["docker"]["build"]["dockerfile"] = \
                (Path(source_dir) / dockerfile[len(LOCAL_PREFIX):]).resolve().absolute().as_posix()
    return env_dict


def _refine_spec_args(spec_args: dict) -> dict:
    # Deep copy because inner dict may be changed (environment or distribution).
    spec_args = copy.deepcopy(spec_args)
    tags = spec_args.get('tags', {})

    # Convert the type to support old style list tags.
    if isinstance(tags, list):
        tags = {tag: None for tag in tags}

    if not isinstance(tags, dict):
        raise DSLComponentDefiningError("Keyword 'tags' must be a dict.")

    # Indicate the component is generated by dsl.component
    if ComponentDefinition.CODE_GEN_BY_KEY not in tags:
        tags[ComponentDefinition.CODE_GEN_BY_KEY] = ComponentDefinition.DSL_COMPONENT
    spec_args['tags'] = tags

    if 'type' in spec_args and spec_args['type'] == ComponentType.SweepComponent.value:
        return spec_args

    environment = spec_args.pop('environment') if 'environment' in spec_args else Environment()
    core_env = environment._env
    spec_args['environment'] = core_env

    distribution = spec_args.pop('distribution') if 'distribution' in spec_args else None
    if distribution:
        if not isinstance(distribution, dict):
            raise DSLComponentDefiningError("Keyword 'distribution' must be a dict.")
        # Add component type
        spec_args['type'] = ComponentType.DistributedComponent.value
        # Convert distribution key to launcher
        spec_args['launcher'] = distribution
    return spec_args


def _deepcopy_spec_args(spec_args: dict) -> dict:
    # deepcopy ComponentDefinition will result in RecursionError and TypeError (can't pickle _thread.lock objects),
    #   therefore populate definition (if exists), deepcopy and place definition back.
    definition = spec_args.pop('trial_definition', None)
    copy_spec_args = copy.deepcopy(spec_args)
    if definition:
        spec_args['trial_definition'] = copy_spec_args['trial_definition'] = definition
    return copy_spec_args


class ComponentExecutor:
    """An executor to analyze the spec args of a function and convert it to a runnable component in AzureML."""

    INJECTED_FIELD = '_spec_args'  # The injected field is used to get the component spec args of the function.
    EXECUTION_PARAMETERS_KEY = '--params'

    def __init__(self, func: types.FunctionType, spec_args=None, _entry_file=None):
        """Initialize a ComponentExecutor with a function to enable calling the function with command line args.

        :param func: A function wrapped by dsl.component.
        :type func: types.FunctionType
        """
        if not isinstance(func, types.FunctionType):
            raise TypeError("Only function type is allowed to initialize ComponentExecutor.")
        if spec_args is None:
            spec_args = getattr(func, self.INJECTED_FIELD, None)
            if spec_args is None:
                raise TypeError("You must wrap the function with dsl component decorators before using it.")
        self._raw_spec_args = _deepcopy_spec_args(spec_args)
        self._name = spec_args['name']
        self._type = spec_args.get('type', ComponentType.CommandComponent.value)
        executor_cls = self._get_executor_by_type(self.type)
        # TODO: Not sure why additional executor with similar fields here.
        self._executor = executor_cls(func, spec_args=spec_args, _entry_file=_entry_file)
        self._spec_file_path = None
        if is_dsl_component(func):
            # If is dsl component func, set the func and entry file as original value
            self._func = func._executor._func
            self._entry_file = func._executor._entry_file
        else:
            # Else, set func directly, if _entry_file is None, resolve it from func.
            # Note: The entry file here might not equal with inspect.getfile(component._func),
            # as we can define raw func in file A and wrap it with dsl component in file B.
            # For the example below, we set entry file as B here (the dsl component defined in).
            self._func = func
            self._entry_file = _entry_file if _entry_file else Path(inspect.getfile(self._func)).absolute()

    @property
    def name(self):
        """Return the name of the component."""
        return self._name

    @property
    def type(self):
        """Return the job type of the component."""
        return self._type

    @property
    def spec(self):
        """Return the module spec instance of the component.

        Initialized by the function annotations and the meta data.
        """
        return self._executor.spec

    @property
    def spec_dict(self):
        """Return the component spec data as a python dict."""
        return self._executor.spec._to_dict()

    def to_spec_yaml(self, folder=None, spec_file=None):
        """
        Generate spec dict object, and dump it as a yaml spec file.

        :param folder: Folder of spec file, will be function file folder if not specified.
        :type folder: Path
        :param spec_file: The spec file name, will be generated based on function file.
        :type spec_file: str
        :return: The path of spec file.
        :rtype: Path
        """
        pyfile = Path(inspect.getfile(self._func))
        if folder is None:
            # If the folder is not provided, we generate the spec file in the same folder of the function file.
            folder = pyfile.parent
        if spec_file is None:
            # If the spec file name is not provided, get the name from the file name.
            spec_file = pyfile.with_suffix(SPEC_EXT).name
        self.spec._save_to_code_folder(Path(folder), spec_file)
        return Path(folder) / spec_file

    def get_interface(self):
        """Return the interface of this component.

        :return: A dictionary including the definition of inputs/outputs/params.
        """
        return self._executor.get_interface()

    def execute(self, argv):
        """Execute the component with command line arguments."""
        return self._executor.execute(argv)

    def __call__(self, *args, **kwargs):
        """Directly calling a component executor equals to calling the underlying function directly."""
        return self._func(*args, **kwargs)

    @classmethod
    def collect_component_from_file(
            cls, py_file, working_dir=None, force_reload=False, component_name=None, from_executor=False):
        """Collect single dsl component in a file and return the executors of the components."""
        py_file = Path(py_file).absolute()
        if py_file.suffix != '.py':
            raise ValueError("%s is not a valid py file." % py_file)
        if working_dir is None:
            working_dir = py_file.parent
        working_dir = Path(working_dir).absolute()

        component_path = py_file.relative_to(working_dir).as_posix().split('.')[0].replace('/', '.')

        component = cls.collect_component_from_py_module(
            component_path, working_dir=working_dir, force_reload=force_reload,
            component_name=component_name, from_executor=from_executor)
        if not component and from_executor:
            raise NoDslComponentError(py_file, component_name)
        return component

    @classmethod
    def collect_component_from_py_module(
            cls, py_module, working_dir, force_reload=False, component_name=None, from_executor=False):
        """Collect single dsl component in a py module and return the executors of the components."""
        components = [component for component in cls.collect_components_from_py_module(py_module,
                                                                                       working_dir,
                                                                                       force_reload)]

        def defined_in_current_file(component):
            # The entry file here might not equal with inspect.getfile(component._func),
            # as we can define raw func in file A and wrap it with dsl component in file B.
            # For the example below, we got entry file as B here (the dsl component defined in).
            entry_file = component._entry_file
            component_path = py_module.replace('.', '/') + '.py'
            return Path(entry_file).resolve().absolute() == (Path(working_dir) / component_path).resolve().absolute()

        components = [component for component in components if defined_in_current_file(component)
                      and (not component_name or component.name == component_name)]
        if len(components) == 0:
            return None
        component = components[0]
        entry_file = Path(inspect.getfile(component._func))
        if len(components) > 1:
            if from_executor:
                if not component_name:
                    raise RequiredComponentNameError(entry_file)
                else:
                    raise TooManyDSLComponentsError(len(components), entry_file, component_name)
            else:
                # Calls from pipeline project with no component name.
                raise TooManyDSLComponentsError(len(components), entry_file)
        return component

    @classmethod
    def collect_components_from_py_module(cls, py_module, working_dir=None, force_reload=False):
        """Collect all components in a python module and return the executors of the components."""
        if isinstance(py_module, str):
            try:
                py_module = _import_component_with_working_dir(py_module, working_dir, force_reload)
            except Exception as e:
                raise ImportError("""Error occurs when import component '%s': %s.\n
                Please make sure all requirements inside conda.yaml has been installed.""" % (py_module, e)) from e
        for _, obj in inspect.getmembers(py_module):
            if cls.look_like_component(obj):
                component = cls(obj)
                component.check_py_module_valid(py_module)
                yield component

    @classmethod
    def look_like_component(cls, f):
        """Return True if f looks like a component."""
        if not isinstance(f, types.FunctionType):
            return False
        if not hasattr(f, cls.INJECTED_FIELD):
            return False
        return True

    @classmethod
    def _get_executor_by_type(cls, type):
        """Get the real executor class according to the type, currently we only support CommandComponent."""
        if type == ComponentType.CommandComponent.value:
            return _CommandComponentExecutor
        elif type == ComponentType.DistributedComponent.value:
            return _DistributedComponentExecutor
        elif type == ComponentType.SweepComponent.value:
            return _SweepComponentExecutor
        raise DSLComponentDefiningError("Unsupported component type '%s'." % type)

    def check_py_module_valid(self, py_module):
        """Check whether the entry py module is valid to make sure it could be run in AzureML."""
        return self._executor.check_py_module_valid(py_module)

    def _generate_additional_includes(self):
        """ Generate additional includes.

            1. Get additional includes from file {component_name}.additional_includes.
            2. Refine relative path to abs path.
            3. Dump as {component_name}.spec.additional_includes under spec path folder.
        """
        source_dir = Path(self._entry_file).parent
        additional_includes_path = (source_dir / self.name).with_suffix('.additional_includes').resolve()
        if not additional_includes_path.is_file():
            return
        with open(additional_includes_path, 'r') as f:
            path_list = f.readlines()
        if not path_list:
            return
        additional_includes = [(Path(source_dir) / path).resolve().as_posix() for path in path_list]
        # Dump additional includes to file
        spec_additional_includes = self._spec_file_path.with_suffix('.additional_includes')
        with open(spec_additional_includes, 'w', encoding='utf-8') as out_file:
            out_file.writelines(additional_includes)

    def _get_spec_file_path(self, force_regenerate=False):
        """Return the generated spec file path."""
        if not self._spec_file_path or not os.path.exists(self._spec_file_path) or force_regenerate:
            if force_regenerate:
                self._reload_func()
            temp_spec_folder = tempfile.mkdtemp()
            file_name = self.name + SPEC_EXT
            temp_spec_file = (Path(temp_spec_folder) / file_name).absolute()
            # Note: conda will be added to spec if necessary and not valid conda detected.
            self._spec_file_path = self.to_spec_yaml(
                folder=temp_spec_file.parent, spec_file=temp_spec_file.name)
            # If not in dsl component execution process, try to resolve additional includes
            # Get additional includes file ({name}.additional_includes) under source and refine all path to abs path.
            if not dsl_component_execution():
                self._generate_additional_includes()
        return self._spec_file_path

    def _update_func(self, func: types.FunctionType):
        # Set the injected field so the function could be used to initializing with `ComponentExecutor(func)`
        setattr(func, self.INJECTED_FIELD, self._raw_spec_args)
        if hasattr(self._executor, '_update_func'):
            self._executor._update_func(func)

    def _reload_func(self):
        """Reload the function to make sure the latest code is used to generate yaml."""
        f = self._func
        module = importlib.import_module(f.__module__)
        # if f.__name__ == '__main__', reload will throw an exception
        if f.__module__ != '__main__':
            from azure.ml.component.dsl._utils import _force_reload_module
            _force_reload_module(module)
        func = getattr(module, f.__name__)
        self._func = func._executor._func if is_dsl_component(func) else func
        executor_cls = self._get_executor_by_type(self.type)
        self._executor = executor_cls(self._func, spec_args=self._raw_spec_args, _entry_file=self._entry_file)


class _CommandComponentExecutor:
    CONTROL_OUTPUTS_KEY = 'azureml.pipeline.control'
    SPEC_CLASS = CommandComponentDefinition  # This class is used to initialize a definition instance.
    SPECIAL_FUNC_CHECKERS = {
        'Coroutine': inspect.iscoroutinefunction,
        'Generator': inspect.isgeneratorfunction,
    }
    # This is only available on Py3.6+
    if sys.version_info.major == 3 and sys.version_info.minor > 5:
        SPECIAL_FUNC_CHECKERS['Async generator'] = inspect.isasyncgenfunction

    VALID_SPECIAL_FUNCS = set()

    def __init__(self, func: types.FunctionType, spec_args=None, _entry_file=None):
        """Initialize a ComponentExecutor with a function."""
        if spec_args is None:
            spec_args = getattr(func, ComponentExecutor.INJECTED_FIELD)
        self._spec_args = _deepcopy_spec_args(spec_args)
        self._assert_valid_func(func)
        if is_dsl_component(func):
            # If is dsl component func, set the func and entry file as original value
            self._func = func._executor._func
            self._entry_file = func._executor._entry_file
        else:
            # Else, set func directly, if _entry_file is None, resolve it from func.
            # Note: The entry file here might not equal with inspect.getfile(component._func),
            # as we can define raw func in file A and wrap it with dsl component in file B.
            # For the example below, we set entry file as B here (the dsl component defined in).
            self._func = func
            self._entry_file = _entry_file if _entry_file else Path(inspect.getfile(self._func)).absolute()
        # Note we will add outputs in return mapping into arg_mapping.
        self._arg_mapping, self._return_mapping = self._analyze_annotations(func)
        self._parallel_inputs = None
        if 'parallel_inputs' in spec_args:
            self._parallel_inputs = _InputFileList(self._spec_args.pop('parallel_inputs'))

    @property
    def type(self):
        return self._spec_args.get('type', ComponentType.CommandComponent.value)

    @property
    def spec(self):
        """
        Return the module spec instance of the component.

        Initialized by the function annotations and the meta data.
        """
        io_properties = self._generate_spec_io_properties(self._arg_mapping, self._parallel_inputs)
        command, args = self._spec_args['command'], io_properties.pop('args')
        spec_args = copy.copy(self._spec_args)
        spec_args['command'] = self.get_command_str_by_command_args(command, args)
        return self.SPEC_CLASS._from_dict({**spec_args, **io_properties})

    @classmethod
    def get_command_str_by_command_args(cls, command, args):
        return ' '.join(command + args)

    def get_interface(self):
        """Return the interface of this component.

        :return: A dictionary including the definition of inputs/outputs/params.
        """
        properties = self._generate_spec_io_properties(self._arg_mapping, self._parallel_inputs)
        properties.pop('args')
        return properties

    def finalize(self, run_result, return_args):
        """Write file for outputs specified by return annotation, write RH for control outputs."""
        # Convert run_result to mapping
        if is_dataclass(run_result):
            # run result is dataclass type object
            run_result_mapping = dataclass_to_dict(run_result)
        elif len(self._return_mapping) == 1:
            key = list(self._return_mapping.keys())[0]
            run_result_mapping = {key: run_result}
        else:
            raise UnsupportedError(
                f'Unsupported return type {type(run_result)!r} of function '
                f'{self._func.__name__!r}, expected dataclass object for multiple outputs.')
        # Write outputs for outputs specified by return annotation
        control_output_keys = [key for key, output in self._return_mapping.items() if output.is_control]
        for key, path in return_args.items():
            if key not in run_result_mapping:
                raise UserErrorException(
                    f'Output with name {key!r} not found in run result {run_result_mapping}.')
            path = Path(path)
            if path.exists() and path.is_dir():
                path = path / 'output'  # refer to a file path if receive directory
            Path(path).write_text(str(run_result_mapping[key]))
        # Write control outputs into run properties
        from azureml.core import Run
        run = Run.get_context()
        run.add_properties({self.CONTROL_OUTPUTS_KEY: json.dumps({
            k: v for k, v in run_result_mapping.items() if k in control_output_keys})})
        return run

    def execute(self, argv):
        """Execute the component with command line arguments."""
        args = self._parse(argv)
        param_args, return_args = {}, {}
        # Split outputs specified by param and by return annotation
        for k, v in args.items():
            if k in self._return_mapping:
                return_args[k] = v
            else:
                param_args[k] = v
        run = self._func(**param_args)
        if self._parallel_inputs is not None:
            run(self._parallel_inputs.load_from_argv(argv))
        if return_args:
            self.finalize(run, return_args)

    def __call__(self, *args, **kwargs):
        """Directly calling a component executor equals to calling the underlying function directly."""
        return self._func(*args, **kwargs)

    @classmethod
    def is_valid_type(cls, type):
        return type in {None, ComponentType.CommandComponent.value}

    def _assert_valid_func(self, func):
        """Check whether the function is valid, if it is not valid, raise."""
        for k, checker in self.SPECIAL_FUNC_CHECKERS.items():
            if k not in self.VALID_SPECIAL_FUNCS:
                if checker(func):
                    raise NotImplementedError("%s function is not supported for %s now." % (k, self.type))

    def check_py_module_valid(self, py_module):
        pass

    @classmethod
    def _parse_with_mapping(cls, argv, arg_mapping):
        """Use the parameters info in arg_mapping to parse commandline params.

        :param argv: Command line arguments like ['--param-name', 'param-value']
        :param arg_mapping: A dict contains the mapping from param key 'param_name' to _ComponentBaseParam
        :return: params: The parsed params used for calling the user function.
        """
        parser = argparse.ArgumentParser()
        for param in arg_mapping.values():
            DSLCommandLineGenerator(param).add_to_arg_parser(parser)
        args, _ = parser.parse_known_args(argv)

        # Convert the string values to real params of the function.
        params = {}
        for name, param in arg_mapping.items():
            val = getattr(args, param.name)
            generator = DSLCommandLineGenerator(param)
            if val is None:
                # Note: here param value only contains user input except default value on function
                if isinstance(param, Output) or (not param.optional and param._default is None):
                    raise RequiredParamParsingError(name=param.name, arg_string=generator.arg_string)
                continue
            # If it is a parameter, we help the user to parse the parameter,
            # if it is an input port, we use load to get the param value of the port,
            # otherwise we just pass the raw value as the param value.
            param_value = val
            if isinstance(param, _Param):
                param_value = param._parse_and_validate(val)
            elif isinstance(param, Input):
                param_value = val
            params[name] = param_value
            # For OutputPath, we will create a folder for it.
            if isinstance(param, Output) and not isinstance(param, _OutputFile) and not Path(val).exists():
                Path(val).mkdir(parents=True, exist_ok=True)
        return params

    def _parse(self, argv):
        return self._parse_with_mapping(argv, self._arg_mapping)

    @classmethod
    def _generate_spec_outputs(cls, arg_mapping) -> dict:
        """Generate output ports of a component, from the return annotation and the arg annotations.

        The outputs including the return values and the special PathOutputPort in args.
        """
        return {val.name: val for val in arg_mapping.values() if isinstance(val, Output)}

    @classmethod
    def _generate_spec_inputs(cls, arg_mapping, parallel_inputs: _InputFileList = None) -> dict:
        """Generate input ports of the component according to the analyzed argument mapping."""
        input_ports = {val.name: val for val in arg_mapping.values() if isinstance(val, Input)}
        parallel_input_ports = {val.name: val for val in parallel_inputs.inputs} if parallel_inputs else {}
        return {**input_ports, **parallel_input_ports}

    @classmethod
    def _generate_spec_params(cls, arg_mapping) -> dict:
        """Generate parameters of the component according to the analyzed argument mapping."""
        return {val.name: val for val in arg_mapping.values() if isinstance(val, _Param)}

    @classmethod
    def _generate_spec_io_properties(cls, arg_mapping, parallel_inputs=None):
        """Generate the required properties for a component spec according to the annotation of a function."""
        inputs = cls._generate_spec_inputs(arg_mapping, parallel_inputs)
        outputs = cls._generate_spec_outputs(arg_mapping)
        params = cls._generate_spec_params(arg_mapping)
        args = []
        for val in list(inputs.values()) + list(outputs.values()) + list(params.values()):
            args.append(DSLCommandLineGenerator(val).arg_group_str())
        return {'inputs': inputs, 'outputs': outputs, 'parameters': params, 'args': args}

    @classmethod
    def _analyze_annotations(cls, func):
        """Analyze the annotation of the function to get the parameter mapping dict and the output port list.
        :param func:
        :return: (param_mapping, output_list)
            param_mapping: The mapping from function param names to input ports/component parameters;
            output_list: The output port list analyzed from return annotations.
        """
        mapping = _get_param_with_standard_annotation(func, is_func=True)
        # Outputs defined by return annotation will be added into mapping
        return_mapping = cls._get_outputs_from_return_annotation(func)
        for key, definition in mapping.items():
            # Not annotated param fall back to String type.
            if isinstance(definition, _Param) and not definition.type:
                definition._type = String.TYPE_NAME
        for key, definition in return_mapping.items():
            if key in mapping:
                raise DSLComponentDefiningError(
                    f'Duplicate output {key!r} found in both parameters '
                    f'and return annotations of function {func.__name__!r}.')
            mapping[key] = definition
        return mapping, return_mapping

    @classmethod
    def _get_outputs_from_return_annotation(cls, func):
        """Convert return annotation to Outputs.

        Supported type:
            1. dsl parameter types. func()->Boolean(is_control=True)
                will be converted to Output(type='boolean')
            2. dsl output type. func()->Output(type='boolean', is_control=True) will be keep as they are.
            3. dataclass type. func()->OutputClass will add output1 and output2 to component defined, with OutputClass:
                @dataclass
                class OutputClass:
                    output1: bool
                    output2: Boolean(is_control=True)

        Note:
            - Single output without dataclass will be named as 'output'.
              If there are duplicate outputs, exception will be raised. i.e.
                func(output: Output)->Output  # Exception raised.
            - Nested dataclass object is not support.
        """
        exception_tail = f'in return annotation of function {func.__name__!r}'

        def get_standard_output_annotation(anno, name=None):
            if anno is _Param.EMPTY:
                return {}
            name = 'output' if name is None else name
            if is_dataclass(anno):
                fields = get_dataclass_fields(anno)
                fields_mapping = {}
                for field in fields:
                    field_type = field.type
                    if is_dataclass(field_type):
                        raise UnsupportedError(f'Nested dataclass is not supported {exception_tail}.')
                    # Convert python type or class to dsl type object inside dataclass
                    if not _is_dsl_types(field_type):
                        field_type = _get_annotation_cls_by_type(field_type, raise_error=True) \
                            if not _is_dsl_type_cls(field_type) else field_type
                        field_type = field_type()
                        field_type._auto_gen = True
                    fields_mapping.update(get_standard_output_annotation(field_type, name=field.name))
                return fields_mapping
            if not _is_dsl_types(anno) or type(anno) == Input:
                raise UnsupportedError(
                    f'Unsupported type {anno!r} {exception_tail}, '
                    f'expected are primitive type dsl.types objects. e.g. func()->Boolean()')

            if isinstance(anno, Output) and anno.type not in _Param._PARAM_TYPE_STRING_MAPPING:
                raise UnsupportedError(
                    f'Unsupported output type {anno.type!r} {exception_tail}, '
                    f'expected are primitive types {list(_Param._PARAM_TYPE_STRING_MAPPING.keys())}.'
                    f'e.g. func()->Boolean() or func()->Output(type=Boolean.TYPE_NAME)')
            if isinstance(anno, _Param):
                if anno._optional is True:
                    # NOTE: use ._optional instead of .optional as there are some calculation in .optional.
                    # Print warning and ignore optional field.
                    logger.warning(f"'optional=True' is not supported and will be ignored in Output.")
                # Change to Output(type='xx', name='output')
                anno = Output(type=anno.type, is_control=anno.is_control)
            anno._name = name
            return {anno._name: anno}

        return get_standard_output_annotation(inspect.signature(func).return_annotation)

    def _update_func(self, func):
        pass


class _DistributedComponentExecutor(_CommandComponentExecutor):
    SPEC_CLASS = DistributedComponentDefinition  # This class is used to initialize a definition instance.

    def __init__(self, func: callable, spec_args=None, _entry_file=None):
        super(_DistributedComponentExecutor, self).__init__(func, spec_args, _entry_file)

    @property
    def spec(self):
        """
        Return the module spec instance of the component.

        Initialized by the function annotations and the meta data.
        """
        io_properties = self._generate_spec_io_properties(self._arg_mapping, self._parallel_inputs)
        command, args = self._spec_args['command'], io_properties.pop('args')
        spec_args = copy.deepcopy(self._spec_args)
        spec_args.pop('command')
        spec_args['launcher']['additional_arguments'] = self.get_command_str_by_command_args(command, args)
        return self.SPEC_CLASS._from_dict({**spec_args, **io_properties})


class _ParallelComponentExecutor(_CommandComponentExecutor):
    """This executor handle parallel component specific operations to enable parallel component."""

    SPEC_CLASS = ParallelRunModuleSpec
    JOB_TYPE = 'parallel'
    FIELDS = {'init', 'run', 'shutdown'}
    CONFLICT_ERROR_TPL = "It is not allowed to declare {}() once a parallel component is defined."
    VALID_SPECIAL_FUNCS = {'Generator'}

    def __init__(self, func: callable, spec_args=None):
        """Initialize a ParallelComponentExecutor with a provided function."""
        super().__init__(func, spec_args)
        if not self._parallel_inputs:
            raise ValueError(
                "Parallel component should have at lease one parallel input, got 0.",
            )
        self._output_keys = [key for key, val in self._arg_mapping.items() if isinstance(val, Output)]
        if len(self._output_keys) == 0:
            raise ValueError(
                "Parallel component should have at least one OutputPath, got %d." % len(self._output_keys)
            )
        self._args = {}
        self._spec_args.update({
            'input_data': [port.name for port in self._parallel_inputs.inputs],
            # We use the first output as the parallel output data.
            # This is only a workaround according to current parallel run design, picking any output port is OK.
            'output_data': self._arg_mapping[self._output_keys[0]].name,
        })
        command = self._spec_args.pop('command')
        self._spec_args['entry'] = command[-1]
        self._spec_args.pop('job_type')
        self._run_func = None
        self._generator = None

    def execute(self, argv, batch_size=4):
        """Execute the component using parallel run style. This is used for local debugging."""
        self.init_argv(argv)

        files = self._parallel_inputs.load_from_argv(argv)
        # Use multiprocessing to run batches.
        count = len(files)
        batches = (count + batch_size - 1) // batch_size
        nprocess = min(max(batches, 1), multiprocessing.cpu_count())
        logger.info("Run %d batches to process %d files." % (batches, count))
        batch_files = [files[i * batch_size: (i + 1) * batch_size] for i in range(batches)]
        with ThreadPool(nprocess) as pool:
            batch_results = pool.map(self.run, batch_files)
        results = []
        for result in batch_results:
            results += result
        shutdown_result = self.shutdown()
        return shutdown_result if shutdown_result is not None else results

    @staticmethod
    def _remove_ambiguous_option_in_argv(argv: list, parse_method):
        """Remove ambiguous options in argv for an argparser method.

        This is a workaround to solve the issue that parallel run will add some other command options
        which will cause the problem 'ambiguous option'.
        """
        pattern = re.compile(r"error: ambiguous option: (\S+) could match")
        while True:
            stderr = StringIO()
            with contextlib.redirect_stderr(stderr):
                try:
                    parse_method(argv)
                except SystemExit:
                    stderr_value = stderr.getvalue()
                    match = pattern.search(stderr_value)
                    if not match:
                        # If we cannot found such pattern, which means other problems is raised, we directly raise.
                        sys.stdout.write(stderr_value)
                        raise
                    # Remove the option_str and the value of it.
                    option_str = match.group(1)
                    logger.debug("Ambiguous option '%s' is found in argv, remove it." % option_str)
                    idx = argv.index(option_str)
                    argv = argv[:idx] + argv[idx + 2:]
                else:
                    # If no exception is raised, return the ready args.
                    return argv

    def init(self):
        """Init params except for the InputFiles with the sys args when initializing parallel component.

        This method will only be called once in one process.
        """
        return self.init_argv(sys.argv)

    def init_argv(self, argv=None):
        """Init params except for the InputFiles with argv."""
        if argv is None:
            argv = sys.argv
        logger.info("Initializing parallel component, argv = %s" % argv)
        mapping = copy.copy(self._arg_mapping)
        argv = self._remove_ambiguous_option_in_argv(
            argv, functools.partial(self._parse_with_mapping, arg_mapping=mapping),
        )
        args = self._parse_with_mapping(argv, mapping)
        logger.info("Parallel component initialized, args = %s" % args)
        ret = self._func(**args)
        # If the init function is a generator, the first yielded result is the run function.
        if isinstance(ret, types.GeneratorType):
            self._generator = ret
            ret = next(ret)

        # Make sure the return result is a callable.
        if callable(ret):
            self._run_func = ret
        else:
            raise TypeError("Return/Yield result of the function must be a callable, got '%s'." % (type(ret)))

        sig = inspect.signature(self._run_func)
        if len(sig.parameters) != 1:
            raise ValueError(
                "The method {}() returned by {}() has incorrect signature {}."
                " It should have exact one parameter.".format(ret.__name__, self._func.__name__, sig)
            )
        return self._run_func

    def run(self, files):
        results = self._run_func(files)
        if results is not None:
            return files
        return results

    def shutdown(self):
        if self._generator:
            # If the function is using yield, call next to run the codes after yield.
            while True:
                try:
                    next(self._generator)
                except StopIteration as e:
                    return e.value

    def check_py_module_valid(self, py_module):
        # For parallel component, the init/run/shutdown in py_module should be
        # _ParallelComponentExecutor.init/run/shutdown
        for attr in self.FIELDS:
            func = getattr(py_module, attr)
            if not self.is_valid_init_run_shutdown(func, attr):
                raise AttributeError(self.CONFLICT_ERROR_TPL.format(attr))

    def _update_func(self, func: types.FunctionType):
        # For a parallel component, we should update init/run/shutdown for the script.
        # See "Write your inference script" in the following link.
        # https://docs.microsoft.com/en-us/azure/machine-learning/how-to-use-parallel-run-step
        py_module = importlib.import_module(func.__module__)
        for attr in self.FIELDS:
            func = getattr(py_module, attr, None)
            # We don't allow other init/run/shutdown in the script.
            if func is not None and not self.is_valid_init_run_shutdown(func, attr):
                raise AttributeError(self.CONFLICT_ERROR_TPL.format(attr))
            setattr(py_module, attr, getattr(self, attr))

    @classmethod
    def is_valid_init_run_shutdown(cls, func, attr):
        return isinstance(func, types.MethodType) and func.__func__ == getattr(_ParallelComponentExecutor, attr)

    @classmethod
    def _generate_spec_io_properties(cls, arg_mapping, parallel_inputs=None):
        """Generate the required properties for a component spec according to the annotation of a function.

        For parallel component, we need to remove InputFiles and --output in args.
        """
        properties = super()._generate_spec_io_properties(arg_mapping, parallel_inputs)
        args_to_remove = []
        for k, v in arg_mapping.items():
            # InputFiles and the output named --output need to be removed in the arguments.
            # For InputFiles: the control script will handle it and pass the files to run();
            # For the output, the control script will add an arg item --output so we should not define it again.
            if v.to_cli_option_str() == '--output':
                args_to_remove.append(v)
        if parallel_inputs:
            args_to_remove += [port for port in parallel_inputs.inputs]
        args = properties['args']
        for arg in args_to_remove:
            args.remove(arg.arg_group_str())
        return properties

    @property
    def spec(self):
        """
        Return the module spec instance of the component.

        Initialized by the function annotations and the meta data.
        """
        io_properties = self._generate_spec_io_properties(self._arg_mapping, self._parallel_inputs)
        return self.SPEC_CLASS._from_dict({**self._spec_args, **io_properties})

    @classmethod
    def is_valid_type(cls, job_type):
        return job_type == cls.JOB_TYPE


class _SweepComponentExecutor:
    SPEC_CLASS = SweepComponentDefinition

    def __init__(self, func: types.FunctionType, spec_args=None, _entry_file=None):
        self._spec_args = _deepcopy_spec_args(spec_args)

    @property
    def spec(self):
        return self.SPEC_CLASS._from_dict(self._spec_args)
