# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import argparse
import concurrent.futures
import glob
import importlib
import itertools
import json
import os
import re
import shutil
import sys
import hashlib
from fnmatch import fnmatch
from typing import Union
from pathlib import Path
from abc import ABC, abstractmethod
from tqdm import tqdm

from azure.ml.component._api._api import ComponentAPI
from azure.ml.component._core import ComponentDefinition
from azure.ml.component._util._constants import LOCAL_PREFIX
from azure.ml.component._util._loggerfactory import _LoggerFactory
from azure.ml.component._util._yaml_utils import YAML
from azure.ml.component._util._utils import _relative_path, _sanitize_python_variable_name, TimerContext, \
    _sanitize_folder_name
from azureml.core import Workspace
from azureml.core.authentication import InteractiveLoginAuthentication
from azureml.exceptions import UserErrorException
from azure.ml.component._restclients.designer.models import ModuleDtoFields

from azure.ml.component._core._types import Input, Output, String, _Param, Enum, _Group, Float, Integer, Boolean
from ._module_spec import BaseModuleSpec, Param, OutputPort, InputPort
from ._utils import _change_working_dir, _import_component_with_working_dir, _sanitize_python_class_name, \
    is_notebook_file, NOTEBOOK_EXT, is_py_file, _to_camel_case, get_workspace, WORKSPACE_ERROR_MSG
from .._util._exceptions import DSLComponentDefiningError

DATA_PATH = Path(__file__).resolve().parent / 'data'
NOTEBOOK_ENTRY_TPL_FILE = DATA_PATH / 'from_notebook_sample_code.template'
ARGPARSE_ENTRY_TPL_FILE = DATA_PATH / 'from_argparse_sample_code.template'
ARGPRASE_ENTRY_TPL_FILE_PARALLEL = DATA_PATH / 'from_argparse_parallel_sample_code.template'
GENERATE_PKG_PATH = DATA_PATH / 'generate_package'
DOC_CONF_TPL_FILE = GENERATE_PKG_PATH / 'doc_conf.template'
DOC_INDEX_TPL_FILE = GENERATE_PKG_PATH / 'doc_index.template'
PKG_INIT_TPL_FILE = GENERATE_PKG_PATH / 'pkg_init.template'
PKG_SETUP_TPL_FILE = GENERATE_PKG_PATH / 'pkg_setup.template'
MODULE_INIT_TPL_FILE = GENERATE_PKG_PATH / 'module_init.template'
MOUDLE_ASSETS_TPL_FILE = GENERATE_PKG_PATH / 'assets_file.template'
MODULE_WORKSPACE_TPL_FILE = GENERATE_PKG_PATH / 'workspace_file.template'
SINGLE_COMPONENT_TPL_FILE = GENERATE_PKG_PATH / 'single_component.template'
SINGLE_DATASET_TPL_FILE = GENERATE_PKG_PATH / 'single_dataset.template'
SINGLE_RUNSETTING_CLS_TPL_FILE = GENERATE_PKG_PATH / 'single_runsetting_class.template'
SINGLE_WORKSPACE_TPL_FILE = GENERATE_PKG_PATH / 'single_workspace.template'

REFERENCE = "reference"
SNAPSHOT = "snapshot"
DEFAULT_COMPONENT_CONFIG_PATH = "DEFAULT_COMPONENT_CONFIG_PATH"
COMPONENT_CONFIG_FILE = "components.yaml"
SINGLE_SPACE = ' '
LINE_SEP = '\n'
CLASS_SEP = LINE_SEP * 2


_logger = _LoggerFactory.get_logger()


def new_line(meta='', indent=0):
    return '%s%s%s' % (LINE_SEP, SINGLE_SPACE * indent, meta)


def normalize_working_dir(working_dir):
    if working_dir is None:
        working_dir = '.'
    if not Path(working_dir).is_dir():
        raise ValueError("Working directory '%s' is not a valid directory." % working_dir)
    return working_dir


def normalize_entry_path(working_dir, entry, ext=None, job_type=None):
    is_file = False
    if ext:
        is_file = entry.endswith(ext)
    if is_file:
        if Path(entry).is_absolute():
            raise ValueError("Absolute file path '%s' is not allowed." % entry)
        if not (Path(working_dir) / entry).is_file():
            raise FileNotFoundError("Entry file '%s' not found in working directory '%s'." % (entry, working_dir))
        entry = Path(entry).as_posix()
        # For parallel component, we need to import the entry instead of run it.
        if job_type == 'parallel':
            entry = entry[:-3].replace('/', '.')
    return entry


def normalized_target_file(working_dir, target_file, force):
    if target_file:
        if Path(target_file).is_absolute():
            raise ValueError("Absolute target file path '%s' is not allowed." % target_file)
        if not target_file.endswith('.py'):
            raise ValueError("Target file must has extension '.py', got '%s'." % target_file)
        if not force and (Path(working_dir) / target_file).exists():
            raise FileExistsError("Target file '%s' already exists." % target_file)
    return target_file


def normalized_spec_file(working_dir, spec_file, force):
    if spec_file:
        if Path(spec_file).is_absolute():
            raise ValueError("Absolute module spec file path '%s' is not allowed." % spec_file)
        if not spec_file.endswith('.yaml'):
            raise ValueError("Module spec file must has extension '.yaml', got '%s'." % spec_file)
        if not force and (Path(working_dir) / spec_file).exists():
            raise FileExistsError("Module spec file '%s' already exists." % spec_file)
    return spec_file


class BoolParam(Param):
    def __init__(self, name, description=None, default=None, arg_name=None, arg_string=None):
        super().__init__(
            name=name, type='Boolean', description=description,
            default=default, arg_name=arg_name, arg_string=arg_string,
        )


class StoreTrueParam(BoolParam):

    def __init__(self, name, description=None, default=None, arg_name=None, arg_string=None):
        super().__init__(
            name=name, description=description,
            default=default, arg_name=arg_name, arg_string=arg_string,
        )
        self._optional = True

    @property
    def append_argv_statement(self):
        return "    if %s:\n        sys.argv.append(%r)" % (self.arg_name, self.arg_string)


class StoreFalseParam(BoolParam):

    def __init__(self, name, description=None, default=None, arg_name=None, arg_string=None):
        super().__init__(
            name=name, description=description,
            default=default, arg_name=arg_name, arg_string=arg_string,
        )
        # Store param should be optional.
        self._optional = True

    @property
    def append_argv_statement(self):
        return "    if not %s:\n        sys.argv.append(%r)" % (self.arg_name, self.arg_string)


class BaseParamGenerator:
    def __init__(self, param: Union[_Param, InputPort, OutputPort]):
        self.param = param

    @property
    def type(self):
        return self.param.type

    @property
    def description(self):
        return self.param.description

    @property
    def arg_string(self):
        return self.param.arg_string

    @property
    def default(self):
        value = self.param.default if isinstance(self.param, (_Param, Param)) else None
        if value is None:
            if hasattr(self.param, 'optional') and self.param.optional:
                return 'None'
            return None
        if self.type.lower() == String.TYPE_NAME:
            return "'%s'" % value
        elif self.type.lower() == Enum.TYPE_NAME:
            if value not in self.param.enum:
                value = self.param.enum[0]
            return "%s.%s" % (self.enum_class, self.enum_name(value, self.param.enum.index(value)))
        elif self.type.lower() == _Group.TYPE_NAME:
            return "%s(%s)" % (self.group_class, ', '.join(['%s=%s' % (k, v)for k, v in value.items()]))
        return str(value)

    @property
    def var_name(self):
        return _sanitize_python_variable_name(self.param.name)

    @property
    def arg_value(self):
        if type(self.param.type) == str and self.param.type.lower() == Enum.TYPE_NAME:
            return self.var_name + '.value'
        return 'str(%s)' % self.var_name

    @property
    def arg_def_in_cls(self):
        arg_type = 'Input' if isinstance(self.param, Input) else self.arg_type
        result = "%s: %s" % (self.var_name, arg_type)
        if self.default is not None:
            result += ' = %s' % self.default
        comment = self.param._get_hint(new_line_style=True)
        if comment:
            result += new_line(meta=comment, indent=4)
        return result

    @property
    def arg_def(self):
        result = "%s: %s" % (self.var_name, self.arg_type)
        result += ',' if self.default is None else ' = %s,' % self.default
        return result

    @property
    def enum_class(self):
        return 'Enum%s' % _sanitize_python_class_name(self.var_name)

    @staticmethod
    def enum_name(value, idx):
        name = _sanitize_python_variable_name(str(value))
        if name == '':
            name = 'enum%d' % idx
        return name

    @staticmethod
    def enum_value(value):
        return "'%s'" % value

    @property
    def enum_name_def(self):
        return new_line().join("    %s = %s" % (self.enum_name(option, i), self.enum_value(option))
                               for i, option in enumerate(self.param.enum))

    @property
    def enum_def(self):
        return "class {enum_class}(Enum):\n{enum_value_string}\n".format(
            enum_class=self.enum_class, enum_value_string=self.enum_name_def,
        )

    @property
    def group_class(self):
        return '%sGroup' % _sanitize_python_class_name(self.var_name)

    @property
    def group_cls_fields(self):
        params = [BaseParamGenerator(param) for param in self.param.values.values()]
        ordered_param_def = [''] + [param.arg_def for param in params if param.default is None] + \
            [param.arg_def for param in params if param.default is not None]
        return new_line(indent=4).join(ordered_param_def)

    @property
    def group_def(self):
        return "@dsl.parameter_group\nclass {group_class}:{group_value_string}\n".format(
            group_class=self.group_class, group_value_string=self.group_cls_fields,
        )


class ArgParseParamGenerator(BaseParamGenerator):
    mapping = {str: 'String', int: 'Integer', float: 'Float', bool: 'Boolean'}
    reverse_mapping = {v: k.__name__ for k, v in mapping.items()}

    @property
    def arg_type(self):
        if isinstance(self.param, (InputPort, OutputPort)):
            desc_str = 'description=%r' % self.description if self.description else ''
            key = 'Input' if isinstance(self.param, InputPort) else 'Output'
            return "%s(%s)" % (key, desc_str)
        if not self.description:
            return self.enum_class if self.type.lower() == Enum.TYPE_NAME else self.reverse_mapping[self.type]
        # The placeholders are used to avoid the bug when description contains '{xx}'.
        placeholder_l, placeholder_r = 'L__BRACKET', 'R__BRACKET'
        description = self.description.replace('{', placeholder_l).replace('}', placeholder_r)
        # For arg parser annotation replace Enum as DslEnum as we import python Enum at same time.
        tpl = "DslEnum(enum={enum_class}, description=%r)" % description\
            if self.type.lower() == Enum.TYPE_NAME else "{type}(description=%r)" % description
        result = tpl.format(type=self.type, enum_class=self.enum_class)
        return result.replace(placeholder_l, '{').replace(placeholder_r, '}')

    @property
    def argv(self):
        return ["'%s'" % self.param.arg_string, self.arg_value]

    @property
    def is_optional_argv(self):
        # Rules:
        #   - If param.optional is True and default is None, then it is optional argv in command.
        #   - If param has default, it must be added into sys.argv so it is not optional.
        #   - StoreTrue/StoreFalse param must be optional.
        if isinstance(self.param, (StoreTrueParam, StoreFalseParam)):
            return True
        return not isinstance(self.param, OutputPort) and self.param.optional is True \
            and getattr(self.param, 'default', None) is None

    @property
    def append_argv_statement(self):
        if hasattr(self.param, 'append_argv_statement'):
            return self.param.append_argv_statement
        return """    if %s is not None:\n        sys.argv += [%s]""" % (self.var_name, ', '.join(self.argv))


class NotebookParamGenerator(BaseParamGenerator):

    @property
    def arg_type(self):
        return self.param._to_python_code()


class BaseGenerator(ABC):
    """Base generator class to generate code/file based on given template."""
    @property
    @abstractmethod
    def tpl_file(self):
        """Specify the template file for different generator."""
        pass

    @property
    @abstractmethod
    def entry_template_keys(self):
        """Specify the entry keys in template, they will be formatted by value when generate code/file."""
        pass

    def to_component_entry_code(self):
        with open(self.tpl_file) as f:
            entry_template = f.read()
        return entry_template.format(**{key: getattr(self, key) for key in self.entry_template_keys})

    def to_component_entry_file(self, target='entry.py'):
        target = Path(target).absolute()
        with open(target, 'w', encoding="utf-8") as fout:
            fout.write(self.to_component_entry_code())


class BaseComponentGenerator(BaseGenerator):
    def __init__(self, name=None, entry=None, description=None):
        self._params = []
        self.name = None
        self.display_name = None
        if name is not None:
            self.set_name(name)
        self.entry = None
        self.entry_type = 'path'
        if entry is not None:
            self.set_entry(entry)
        self.description = description
        self._component_meta = {}
        self.parallel_inputs = []

    @property
    @abstractmethod
    def tpl_file(self):
        pass

    @property
    @abstractmethod
    def entry_template_keys(self):
        pass

    def set_name(self, name):
        if name.endswith('.py'):
            name = name[:-3]
        if name.endswith(NOTEBOOK_EXT):
            name = name[:-6]
        # Use the last piece as the component name.
        self.display_name = _to_camel_case(name.split('/')[-1].split('.')[-1])
        self.name = _sanitize_python_variable_name(self.display_name)

    def set_entry(self, entry):
        self.entry = entry
        if type(entry) == str:
            if is_py_file(entry):
                self.entry_type = 'path'  # python path
            elif is_notebook_file(entry):
                self.entry_type = 'notebook_path'
                suffix = NOTEBOOK_EXT
                self.entry_out = self.entry[:-len(suffix)] + '.out' + suffix
            else:
                self.entry_type = 'module'
        else:
            self.entry_type = 'module'

    @property
    def component_name(self):
        if self.entry_type == 'module':
            return self.entry
        elif self.entry_type == 'path':
            return Path(self.entry).as_posix()[:-3].replace('/', '.')
        else:
            raise TypeError("Entry type %s doesn't have component name." % self.entry_type)

    def assert_valid(self):
        if self.name is None:
            raise ValueError("The name of a component could not be None.")
        if self.entry is None:
            raise ValueError("The entry of the component '%s' could not be None." % self.name)

    @property
    def params(self):
        return self._params

    def to_component_entry_code(self):
        self.assert_valid()
        with open(self.tpl_file) as f:
            entry_template = f.read()
        return entry_template.format(**{key: getattr(self, key) for key in self.entry_template_keys})

    @property
    def func_name(self):
        return _sanitize_python_variable_name(self.name)

    @property
    def func_args(self):
        items = [''] + [param.arg_def for param in self.params if param.default is None] + \
                [param.arg_def for param in self.params if param.default is not None]
        return '\n    '.join(items)

    @property
    def dsl_param_dict(self):
        meta = self.component_meta
        if not meta:
            return ''
        items = [''] + ['%s=%r,' % (k, v) for k, v in meta.items()]
        if self.job_type == 'parallel':
            parallel_inputs_str = "Input(name='parallel_input_data')" if not self.parallel_inputs else \
                ', '.join("Input(name=%r)" % name
                          for name in self.parallel_inputs)
            items.append('parallel_inputs=[%s]' % parallel_inputs_str)
        return new_line(indent=4).join(items) + new_line()

    @property
    def component_meta(self):
        meta = {**self._component_meta}
        if self.description and 'description' not in meta:
            meta['description'] = self.description
        if self.name and 'name' not in meta:
            meta['name'] = self.name
        if self.display_name and 'display_name' not in meta:
            meta['display_name'] = self.display_name
        return meta

    @property
    def job_type(self):
        return self.component_meta.get('job_type', 'basic').lower()

    def update_component_meta(self, component_meta):
        for k, v in component_meta.items():
            if v is not None:
                self._component_meta[k] = v


class CommandLineGenerator:
    """This class is used to generate command line arguments for an input/output in a component."""

    def __init__(self, param: Union[Input, Output, _Param], arg_name=None, arg_string=None):
        self._param = param
        self._arg_name = arg_name
        self._arg_string = arg_string

    @property
    def param(self) -> Union[Input, Output, String, Float, Integer, Enum, Boolean]:
        """Return the bind input/output/parameter"""
        return self._param

    @property
    def arg_string(self):
        """Return the argument string of the parameter."""
        return self._arg_string

    @property
    def arg_name(self):
        """Return the argument name of the parameter."""
        return self._arg_name

    @arg_name.setter
    def arg_name(self, value):
        self._arg_name = value

    def to_cli_option_str(self, style=None):
        """Return the cli option str with style, by default return underscore style --a_b."""
        return self.arg_string.replace('_', '-') if style == 'hyphen' else self.arg_string

    def arg_group_str(self):
        """Return the argument group string of the input/output/parameter."""
        s = '%s %s' % (self.arg_string, self._arg_placeholder())
        return '[%s]' % s if isinstance(self.param, (Input, _Param)) and self.param.optional else s

    def _arg_group(self):
        """Return the argument group item. This is used for legacy module yaml."""
        return [self.arg_string, self._arg_dict()]

    def _arg_placeholder(self) -> str:
        raise NotImplementedError()

    def _arg_dict(self) -> dict:
        raise NotImplementedError()


class DSLCommandLineGenerator(CommandLineGenerator):
    """This class is used to generate command line arguments for an input/output in a dsl.component."""

    @property
    def arg_string(self):
        """Compute the cli option str according to its name, used in argparser."""
        return '--' + self.param.name

    def add_to_arg_parser(self, parser: argparse.ArgumentParser, default=None):
        """Add this parameter to ArgumentParser, both command line styles are added."""
        cli_str_underscore = self.to_cli_option_str(style='underscore')
        cli_str_hyphen = self.to_cli_option_str(style='hyphen')
        if default is not None:
            return parser.add_argument(cli_str_underscore, cli_str_hyphen, default=default)
        else:
            return parser.add_argument(cli_str_underscore, cli_str_hyphen,)

    def _update_name(self, name: str):
        """Update the name of the port/param.

        Initially the names of inputs should be None, then we use variable names of python function to update it.
        """
        if self.param._name is not None:
            raise AttributeError("Cannot set name to %s since it is not None, the value is %s." % (name, self._name))
        if not name.isidentifier():
            raise DSLComponentDefiningError("The name must be a valid variable name, got '%s'." % name)
        self.param._name = name

    def _arg_placeholder(self) -> str:
        io_tag = 'outputs' if isinstance(self.param, Output) else 'inputs'
        return "{%s.%s}" % (io_tag, self.param.name)


class ArgParseComponentGenerator(BaseComponentGenerator):

    @property
    def tpl_file(self):
        return ARGPRASE_ENTRY_TPL_FILE_PARALLEL if self.job_type == 'parallel' else ARGPARSE_ENTRY_TPL_FILE

    @property
    def entry_template_keys(self):
        return [
            'enums', 'imports',
            'entry_type', 'entry',
            'component_name',
            'func_name', 'func_args',
            'sys_argv', 'append_stmt',
            'dsl_param_dict',
        ]

    def add_param(self, param: _Param):
        self._params.append(ArgParseParamGenerator(param))

    @property
    def params(self):
        result = self._params
        if self.job_type.lower() == 'parallel' and not self.has_output():
            # Add an output if output is not set, since parallel component require one output,
            # which may not be from argparse.
            return [ArgParseParamGenerator(OutputPort(
                name='Output', type='AnyDirectory', arg_name='output', arg_string='--output',
            ))] + result
        return result

    @property
    def component_entry_file(self):
        if is_py_file(self.entry):
            return self.entry
        return self.entry.replace('.', '/') + '.py'

    @property
    def spec(self):
        """This spec is directly generated by argument parser arguments,
        it is used to create a module spec without a new entry file.
        """
        params = [param.param for param in self.params if isinstance(param.param, Param)]
        inputs = [param.param for param in self.params if isinstance(param.param, InputPort)]
        outputs = [param.param for param in self.params if isinstance(param.param, OutputPort)]
        args = []
        for param in self.params:
            if not isinstance(param.param, OutputPort) and param.param.optional:
                args.append(param.param.arg_group())
            else:
                args += param.param.arg_group()

        return BaseModuleSpec(
            name=self.name, description=self.description,
            inputs=inputs, outputs=outputs, params=params,
            args=args,
            command=['python', self.component_entry_file],
        )

    @property
    def spec_dict(self):
        return self.spec.spec_dict

    def to_spec_yaml(self, folder, spec_file='spec.yaml'):
        self.assert_valid()
        self.spec._save_to_code_folder(folder, spec_file=spec_file)

    def has_type(self, type):
        return any(param.type == type for param in self._params)

    def has_import_type(self, type):
        return any(param.type == type and param.description is not None for param in self._params)

    def has_input(self):
        return any(isinstance(param.param, InputPort) for param in self._params)

    def has_output(self):
        return any(isinstance(param.param, OutputPort) for param in self._params)

    @property
    def enums(self):
        return CLASS_SEP + CLASS_SEP.join(
            param.enum_def for param in self.params
            if type(param.type) == str and param.type.lower() == Enum.TYPE_NAME) if self.has_type('Enum') else ''

    @property
    def imports(self):
        keys = list(ArgParseParamGenerator.reverse_mapping)
        param_imports = [key for key in keys if self.has_import_type(key)]
        # Note that for a parallel component, input/output are required.
        if self.has_input() or self.job_type == 'parallel':
            param_imports.append('Input')
        if self.has_output() or self.job_type == 'parallel':
            param_imports.append('Output')
        imports_str = 'from azure.ml.component.dsl.types import %s' % ', '.join(param_imports) if param_imports else ''
        if self.has_import_type('Enum'):
            # Special case for Enum as we import python Enum.
            if imports_str:
                imports_str = imports_str + '\n'
            imports_str += 'from azure.ml.component.dsl.types import Enum as DslEnum'
        return imports_str

    @property
    def sys_argv(self):
        items = ['', "'%s'," % self.entry] + [
            ', '.join(param.argv) + ',' for param in self.params if not param.is_optional_argv
        ]
        return new_line(indent=8).join(items)

    @property
    def append_stmt(self):
        return new_line().join(param.append_argv_statement for param in self.params if param.is_optional_argv)

    def update_spec_param(self, key, is_output=False):
        target = None
        key = key
        for param in self.params:
            # For add_argument('--input-dir'), we could have var_name='input_dir', arg_string='--input-dir'
            # In this case, both 'input_dir' and 'input-dir' is ok to used for finding the param.
            if param.var_name == key or param.arg_string.lstrip('-') == key:
                target = param
                break
        if not target:
            if not is_output and self.job_type == 'parallel':
                self.parallel_inputs.append(key)
            else:
                valid_params = ', '.join('%r' % param.var_name for param in self.params)
                _logger.warning("%r not found in params, valid params: %s." % (key, valid_params))
            return
        param = target.param
        if is_output:
            target.param = OutputPort(
                name=param.name, type="path", description=param.description,
                arg_string=param.arg_string,
            )
        else:
            target.param = InputPort(
                name=param.name, type="path",
                description=target.description, optional=param.optional,
                arg_string=param.arg_string,
            )

    def update_spec_params(self, keys, is_output=False):
        for key in keys:
            self.update_spec_param(key, is_output)


class NotebookComponentGenerator(BaseComponentGenerator):

    @property
    def tpl_file(self):
        return NOTEBOOK_ENTRY_TPL_FILE

    @property
    def entry_template_keys(self):
        return [
            'func_name',
            'func_args', 'parameters_dict',
            'entry', 'entry_out',
            'dsl_param_dict',
        ]

    def add_param(self, param: Union[_Param, Input, Output]):
        self._params.append(NotebookParamGenerator(param))

    @property
    def parameters_dict(self):
        items = [''] + ['%s=%s,' % (param.param.name, param.param.name) for param in self.params]
        return new_line(indent=12).join(items)

    @property
    def dsl_param_dict(self):
        param_dict_str = super().dsl_param_dict
        # Add environment as we still dump yaml for component from notebook
        param_dict_str += SINGLE_SPACE * 4 + 'environment=env' + new_line()
        return param_dict_str


class ModuleParamGenerator(BaseParamGenerator):
    def __init__(self, param, var_name, _component_cls_name):
        super().__init__(param)
        self._component_cls_name = _component_cls_name
        self._var_name = var_name

    @property
    def arg_type(self):
        if isinstance(self.param, _Param):
            _typ = self.type.lower()
            if _typ == Enum.TYPE_NAME:
                return self.enum_class
            if _typ == _Group.TYPE_NAME:
                return self.group_class
            # type not in mapping: group
            return _Param._PARAM_TYPE_STRING_MAPPING[_typ].__name__ \
                if _typ in _Param._PARAM_TYPE_STRING_MAPPING else 'str'
        # set Input annotation as pathlib.Path if on function
        return 'Data' if isinstance(self.param, Input) else 'Output'

    @property
    def default(self):
        default_value = super().default
        # Directly assign if is valid default, else assign str
        if default_value and default_value != str(None) and \
                self.type.lower() not in [Enum.TYPE_NAME, _Group.TYPE_NAME]:
            try:
                exec('var=%s' % default_value)
            except Exception:
                # Change to str if is not valid numeric string
                default_value = f'{default_value!r}'
        # Note: Add 'None' if no default to align with our component func loaded from backend
        return default_value if default_value else str(None)

    @property
    def docstring(self):
        param_desc = self.param._get_hint()
        return f'{SINGLE_SPACE * 4}{self.var_name} ({self.arg_type}): {param_desc}'

    @property
    def enum_class(self):
        return '_%s%sEnum' % (self._component_cls_name, _sanitize_python_class_name(self.var_name))

    @property
    def group_class(self):
        return '_%s%sGroup' % (self._component_cls_name, _sanitize_python_class_name(self.var_name))

    @property
    def group_cls_fields(self):
        params = [ModuleParamGenerator(param, name, self._component_cls_name)
                  for name, param in self.param.values.items()]
        ordered_param_def = [''] + [param.arg_def_in_cls for param in params if param.default is None] + \
            [param.arg_def_in_cls for param in params if param.default is not None]
        return new_line(indent=4).join(ordered_param_def)

    @property
    def var_name(self):
        return self._var_name


class ModuleRunsettingParamGenerator(ModuleParamGenerator):
    def __init__(self, param, _component_cls_name):
        self._var_name = param.display_argument_name
        param = param.definition.definition

        super().__init__(param, self._var_name, _component_cls_name)
        self._component_cls_name = _component_cls_name
        self._schema_type_converter = {'array': 'list', 'object': 'dict'}
        self._is_union_type = 'Union' in self.arg_type

    @property
    def arg_def_in_cls(self):
        # Note: No default value if runsetting parameter arg
        result = "%s: %s" % (self.var_name, self.arg_type)
        # Note: No optional field in hint str
        comment_str = self.param.description.replace('"', '\\"') if self.param.description else self.param.type
        hint_str = ', '.join(['%s: %s' % (key, val) for key, val in zip(
            ['min', 'max', 'enum'], [self.param._min, self.param._max, self.param.enum]) if val])
        comment_str += ' (%s)' % hint_str if hint_str else ''
        result += new_line(meta='"""%s"""' % comment_str, indent=4) if comment_str else ''
        return result

    @property
    def arg_type(self):
        if self.param.json_schema:
            _type = self.param.json_schema.get('type')
            _type = self._schema_type_converter.get(_type, str.__name__)
            return f'Union[str, {_type}]' if _type != str.__name__ else str.__name__
        return self.param.parameter_type_in_py.__name__

    @property
    def var_name(self):
        return self._var_name


class ModuleRunsettingClsGenerator(BaseGenerator):

    def __init__(self, runsettings_param_section, component_type, section_name=None):
        super().__init__()
        section_name = '' if section_name is None else section_name
        self._component_type = component_type
        self._section_name = section_name
        # Replace the top level description
        self._description = runsettings_param_section.description if section_name \
            else f'Run setting configuration for {component_type}'
        self._section_cls_name = _sanitize_python_class_name(section_name)
        self._sections = [ModuleRunsettingClsGenerator(
            section, component_type, section_name=section.display_name)
            for section in runsettings_param_section.sub_sections]
        self._full_cls_name = '_%sRunsetting%s' % (component_type, self._section_cls_name)
        if not self._description:
            self._description = self._full_cls_name
        from azure.ml.component._restclients.designer.models import ModuleRunSettingTypes
        self._params = [ModuleRunsettingParamGenerator(param, self._full_cls_name)
                        for param in runsettings_param_section.parameters
                        if param.definition.definition.module_run_setting_type != ModuleRunSettingTypes.LEGACY]
        self._has_union_runsetting = any(param._is_union_type for param in self._params)

    @property
    def tpl_file(self):
        return SINGLE_RUNSETTING_CLS_TPL_FILE

    @property
    def entry_template_keys(self):
        return ['sections', 'component_type', 'section_cls_name', 'cls_fields']

    @property
    def component_type(self):
        return self._component_type

    @property
    def cls_fields(self):
        # params
        items = [''] + ['"""%s"""' % self._description] + [param.arg_def_in_cls for param in self._params]
        # sections
        for section in self._sections:
            items.append('%s: %s' % (section._section_name, section._full_cls_name))
            items.append('"""%s"""' % (section._description))
        cls_field_string = new_line(indent=4).join(items)
        return cls_field_string if cls_field_string.strip() else new_line(meta='pass', indent=4)

    @property
    def section_cls_name(self):
        return self._section_cls_name

    @property
    def sections(self):
        if not self._sections:
            return ''
        return new_line().join(section.to_component_entry_code() for section in self._sections) + new_line()


class ModuleComponentGenerator(BaseComponentGenerator):
    COMPONENT_LOADER_CODE = "_%s = component_loader.load_component(name='%s')"

    def __init__(self, definition, pattern, mode=REFERENCE, component_id_2_func_name=None):
        if component_id_2_func_name:
            name = component_id_2_func_name[definition.identifier]
        else:
            name = _sanitize_python_variable_name(definition.name)
        super().__init__(name=name, entry=definition)
        self._component_cls_name = _sanitize_python_class_name(_sanitize_python_variable_name(self.name))
        self._params = self.get_component_params()
        self._outputs = self.get_component_outputs()
        self._pattern = pattern
        self._source_type = AssetSource.get_asset_source_type(pattern)
        self._mode = mode
        self._component_id = definition.identifier
        self._is_anonymous = definition.registration_context.is_anonymous

    def generate_components_config(self, relative_path=None):
        """
        Generate component config dict.
        """
        component_config = {'name': self.component_name, 'version': self.component_version}
        if self._source_type == AssetSource.REGISTRY:
            registry_name = ModuleUtil.match_registry_name(self._pattern)
            version = self.component_version
            registry_id = f'{ModuleUtil.REGISTRY_PREFIX}/{registry_name}/components/{self.component_name}' \
                f'{f":{version}" if version else ""}'
            component_config['id'] = registry_id
        elif self.entry.workspace:
            if self.entry.registration_context.is_anonymous:
                component_config['id'] = self.entry.identifier
            else:
                workspace_id = ModuleUtil.WS_FORMATTER % (self.entry.workspace.subscription_id,
                                                          self.entry.workspace.resource_group,
                                                          self.entry.workspace.name)
                arm_id = f"{workspace_id}/components/{self.component_name}" \
                         f"{f':{self.component_version}' if self.component_version else ''}"
                component_config['id'] = arm_id
        if (self._mode == SNAPSHOT or self._source_type == AssetSource.LOCAL) and \
                hasattr(self.entry, '_source_file_path'):
            yaml_path = getattr(self.entry, '_source_file_path')
            if relative_path:
                try:
                    yaml_path = Path(os.path.relpath(yaml_path, relative_path)).as_posix()
                except ValueError:
                    # Cannot convert path on different drivers, it will use absolute path as yaml path.
                    pass
            component_config['yaml'] = Path(yaml_path).as_posix()
        return component_config

    @property
    def tpl_file(self):
        return SINGLE_COMPONENT_TPL_FILE

    @property
    def entry_template_keys(self):
        return [
            'enums', 'groups', 'component_cls_name',
            'runsettings_field', 'component_description',
            'input_cls_fields', 'output_cls_fields',
            'func_name', 'func_args', 'func_docstring',
            'get_component_code', 'func_init_args']

    def get_component_params(self):
        all_component_params = {**self.entry.inputs, **self.entry.parameters}
        generators = []
        for var_name, param in all_component_params.items():
            if var_name:
                generators.append(ModuleParamGenerator(param, var_name, self._component_cls_name))
            else:
                raise Exception("The parameter name of component is None.")
        return generators

    def get_component_outputs(self):
        component_outputs = []
        for var_name, param in self.entry.outputs.items():
            if var_name:
                component_outputs.append(ModuleParamGenerator(param, var_name, self._component_cls_name))
            else:
                raise Exception("The output name of component is None.")
        return component_outputs

    @property
    def component_name(self):
        return self.entry.name

    @property
    def component_cls_name(self):
        return self._component_cls_name

    @property
    def runsettings_field(self):
        if not self.entry.runsettings or not self.entry.runsettings.params:
            return '# No runsettings in this component.'
        component_type = self.entry.type.value
        return 'runsettings: _%sRunsetting' % component_type

    @property
    def component_description(self):
        return self.entry.description.replace('"', '\\"') if self.entry.description else self.component_name

    @property
    def component_version(self):
        return self.entry.version

    @property
    def enums(self):
        enum_str = CLASS_SEP.join(
            param.enum_def for param in self.params
            if type(param.type) == str and param.type.lower() == Enum.TYPE_NAME) + new_line()
        return new_line() + enum_str if enum_str.strip() else ''

    @property
    def get_component_code(self):
        """Generate component load code."""
        return self.COMPONENT_LOADER_CODE % (self.func_name, self.name)

    @property
    def groups(self):
        group_str = new_line() + CLASS_SEP.join(
            param.group_def for param in self.params
            if type(param.type) == str and param.type.lower() == _Group.TYPE_NAME) + new_line()
        return group_str if group_str.strip() else ''

    @property
    def input_cls_fields(self):
        items = [''] + [param.arg_def_in_cls for param in self.params if param.default is None] + \
                [param.arg_def_in_cls for param in self.params if param.default is not None]
        cls_field_string = new_line(indent=4).join(items)
        return cls_field_string if cls_field_string.strip() else new_line(meta='pass', indent=4)

    @property
    def output_cls_fields(self):
        items = [''] + [param.arg_def_in_cls for param in self._outputs]
        cls_field_string = new_line(indent=4).join(items)
        return cls_field_string if cls_field_string.strip() else new_line(meta='pass', indent=4)

    @property
    def func_docstring(self):
        params = [param.docstring for param in self.params if param.default is None] + \
                 [param.docstring for param in self.params if param.default is not None]
        args = ["", "Args:"] + params

        returns = ["", "Returns:",
                   f"{SINGLE_SPACE * 4}_{self.component_cls_name}Component: A component object. "
                   f"This component contains the following output ports:", ""]
        # Add \n at the end of output param descirption to avoid merging all output on the same line when generate doc
        outputs = [f'{SINGLE_SPACE * 4}{param.docstring}\\n' for param in self._outputs]
        return new_line(indent=4).join(args + returns + outputs)

    @property
    def func_init_args(self):
        items = [''] + ['%s=%s,' % (param.var_name, param.var_name) for param in self.params]
        return new_line(indent=12).join(items)


class ModuleAssetsFileGenerator(BaseGenerator):

    def __init__(self, definitions, datasets, source_directory_relpath, specify_datasets=False,
                 specify_models=False, mode=REFERENCE, component_id_2_func_name=None, snapshot_component_ids=None):
        super().__init__()
        self._components = []
        self._datasets = []
        self._models = []
        self._runsettings = {}  # with component type as key and runsettings generator as value
        self._source_directory_relpath = source_directory_relpath
        self._errors = []
        # Add component generator
        for pattern, definition_list in definitions.items():
            for definition in definition_list:
                generator_mode = mode
                if snapshot_component_ids and definition.identifier in snapshot_component_ids:
                    generator_mode = SNAPSHOT
                try:
                    self._components.append(ModuleComponentGenerator(
                        definition, pattern, generator_mode, component_id_2_func_name))
                except Exception as ex:
                    self._errors.append(
                        Exception(f'Skip {definition.name!r} for generate component failed with {ex!r}.'))
        # Add dataset generator
        for pattern, dataset_list in datasets.items():
            self._datasets.extend([ModuleDatasetGenerator(
                dataset, pattern) for dataset in dataset_list])
        # Note: If pattern specified assets type like azureml://xxx/datasets or azureml://xxx/models,
        # we will leave the class here even if its empty, else if pattern is general filter(azureml://xxx/*)
        # we will hide the whole class if no item in it.
        self._has_datasets_cls = specify_datasets or self._datasets
        self._has_models_cls = specify_models or self._models
        # Add runsetting cls generator
        for generator in self._components:
            definition = generator.entry
            component_type = definition.type.value
            if component_type in self._runsettings \
                    or not definition.runsettings or not definition.runsettings.params:
                continue
            runsettings_definition = definition.runsettings
            runsetting_section_list, _ = runsettings_definition._get_display_sections(
                component_type, component_name=component_type)
            self._runsettings[component_type] = \
                ModuleRunsettingClsGenerator(runsetting_section_list, component_type)

    @property
    def tpl_file(self):
        return MOUDLE_ASSETS_TPL_FILE

    @property
    def entry_template_keys(self):
        return [
            'component_loader', 'component_names', 'all_imports',
            'all_type_runsetting_cls', 'all_components_cls', 'all_datasets_cls']

    @property
    def all_type_runsetting_cls(self):
        if not self._runsettings:
            return new_line(meta='# No runsetting class is generated.') + new_line()
        return new_line().join(generator.to_component_entry_code()
                               for generator in self._runsettings.values())

    @property
    def all_components_cls(self):
        if not self._components:
            return new_line(meta='# No component class is generated.') + new_line()
        return new_line().join(generator.to_component_entry_code() for generator in self._components)

    @property
    def all_datasets_cls(self):
        def _get_cls_item_code(generators):
            if not generators:
                return new_line(meta='pass', indent=4) + new_line()
            return new_line() + ''.join(generator.to_component_entry_code() for generator in generators)

        cls_separator = """
# +===================================================+
#                    %s
# +===================================================+
"""
        cls_code_list = []
        if self._has_datasets_cls:
            cls_code_list.append('%s\n\nclass Datasets:%s\n\ndatasets = Datasets()\n' % (
                cls_separator % 'datasets', _get_cls_item_code(self._datasets)))
        if self._has_models_cls:
            cls_code_list.append('%s\n\nclass Models:%s\n\nmodels = Models()\n' % (
                cls_separator % 'models', _get_cls_item_code(self._models)))
        cls_codes = new_line().join(cls_code_list)
        return cls_codes if cls_codes else new_line(meta='# No datasets class is generated.') + new_line()

    @property
    def component_names(self):
        items = ['#  - %s::%s' % (generator.component_name, generator.component_version)
                 for generator in self._components]
        return new_line().join(items) if items else '# No component is generated in this file.'

    @property
    def all_imports(self):
        component_pkg = 'azure.ml.component'
        dsl_pkg = 'azure.ml.component.dsl'
        component_file = 'azure.ml.component.component'
        _imports = {}
        _pkg_imports = {component_pkg: [], component_file: [], dsl_pkg: []}
        _local_imports = {}
        _has_enum, _has_inputs, _has_outputs, _has_dsl, _has_registry = False, False, False, False, False
        _has_registry_component = False
        _has_workspace_dataset, _has_workspace_asset = False, False

        for component_generator in self._components:
            _has_dsl = _has_dsl or component_generator.groups
            _has_enum = _has_enum or component_generator.enums
            _has_inputs = _has_inputs or component_generator.entry.inputs
            _has_outputs = _has_outputs or component_generator.entry.outputs
            _has_registry_component |= component_generator._source_type == AssetSource.REGISTRY

        for dataset in self._datasets:
            _has_workspace_dataset |= dataset._source_type == AssetSource.WORKSPACE
        # Note: currently registry need workspace so we treat it as workspace asset
        _has_workspace_asset |= _has_workspace_dataset
        _has_registry |= _has_registry_component

        if self._components:
            _pkg_imports[component_pkg] += ['Component']
            _pkg_imports[f'{dsl_pkg}._component_loader'] = ['ComponentLoader']
            _imports['pathlib'] = ['Path']
        if _has_workspace_asset:
            _local_imports = {'.': ['_workspace']}
        if _has_dsl:
            _pkg_imports[component_pkg] += ['dsl']
        if _has_enum:
            _imports['enum'] = ['Enum']
        if self._datasets or self._models:
            _imports['functools'] = ['lru_cache']
        if _has_inputs or self._components:
            _imports['typing'] = ['Any as Data']
            _pkg_imports[component_file] += ['Input']
        if _has_outputs:
            _pkg_imports[component_file] += ['Output']
        if _has_registry:
            _pkg_imports[dsl_pkg] += ['_assets']
        if any(runsetting_cls._has_union_runsetting for runsetting_cls in self._runsettings.values()):
            _imports['typing'] = _imports.get('typing', []) + ['Union']
        if _has_workspace_dataset:
            _pkg_imports['azureml.core'] = ['Dataset']

        def _imports_to_str(import_list):
            return new_line().join(['from %s import %s' % (name, ', '.join(values))
                                    for name, values in import_list.items() if values])
        all_imports_str = [_imports_to_str(_imports), _imports_to_str(_pkg_imports), _imports_to_str(_local_imports)]
        all_imports_str = CLASS_SEP.join([
            import_str for import_str in all_imports_str if import_str.strip()]) + new_line()
        return all_imports_str if all_imports_str.strip() else ''

    @property
    def component_loader(self):
        if self._components:
            return \
                new_line() + \
                f"component_loader = ComponentLoader(Path(__file__).parent / \"{COMPONENT_CONFIG_FILE}\")" + \
                new_line()
        else:
            return ''

    def to_component_entry_file(self, target='entry.py'):
        super().to_component_entry_file(target)

    def generate_config(self, base_folder, module_folder):
        # Generate component config file for component assets.
        components_config = {
            component_generator.name: component_generator.generate_components_config(
                relative_path=base_folder) for component_generator in self._components}
        YAML._dump_yaml_file({'components': components_config}, os.path.join(module_folder, COMPONENT_CONFIG_FILE))


class ModuleWorkspaceGenerator(BaseGenerator):
    def __init__(self, sub_id, rg, ws_name):
        self.subscription_id = sub_id
        self.resource_group = rg
        self.workspace_name = ws_name
        self.workspace_var_name = _sanitize_python_variable_name(ws_name)

    @property
    def tpl_file(self):
        return SINGLE_WORKSPACE_TPL_FILE

    @property
    def entry_template_keys(self):
        return ['workspace_var_name', 'subscription_id',
                'resource_group', 'workspace_name']


class ModuleWorkspaceFileGenerator(BaseGenerator):
    WORKSPACE_IMPORT = "from azureml.core import Workspace"
    WORKSPACE_FROM_CONFIG = f"""
_default_workspace_from_config = None


def from_config():
    global _default_workspace_from_config
    if _default_workspace_from_config is None:
        try:
            _default_workspace_from_config = Workspace.from_config()
        except Exception:
            raise Exception('''{WORKSPACE_ERROR_MSG}
            ''')
    return _default_workspace_from_config
"""

    def __init__(self, pattern_list):
        self._generators = []
        self._has_ws_from_config = False
        for pattern in set(pattern_list):
            if pattern.startswith(ModuleUtil.LOCAL_PREFIX) or pattern.startswith(ModuleUtil.REGISTRY_PREFIX):
                self._has_ws_from_config = True
            elif pattern.startswith(ModuleUtil.WS_PREFIX):
                self._generators.append(
                    ModuleWorkspaceGenerator(*ModuleUtil.match_workspace_tuple(pattern))
                )

    @property
    def tpl_file(self):
        return MODULE_WORKSPACE_TPL_FILE

    @property
    def entry_template_keys(self):
        return ['all_imports', 'all_workspace']

    @property
    def all_workspace(self):
        if not self._generators and not self._has_ws_from_config:
            return new_line(meta='# No Workspace is generated.') + new_line()
        entry_codes = [generator.to_component_entry_code() for generator in self._generators]
        if self._has_ws_from_config:
            entry_codes = [self.WORKSPACE_FROM_CONFIG] + entry_codes
        return new_line() + new_line().join(entry_codes)

    @property
    def all_imports(self):
        return self.WORKSPACE_IMPORT if self._generators or self._has_ws_from_config else ''


class ModuleDatasetGenerator(BaseGenerator):
    WS_DATASET_CODE = """Dataset.get_by_name(
            _workspace.%s(),
            name='%s', version=%s)"""

    def __init__(self, dataset_dto, pattern):
        self.dataset_name = dataset_dto.name
        self.dataset_var_name = _sanitize_python_variable_name(self.dataset_name)
        self.dataset_description = dataset_dto.description.replace('"', '\\"') if dataset_dto.description \
            else 'No description for this dataset.'
        self._is_model = hasattr(dataset_dto, ModuleUtil.MODEL_ATTR_NAME)
        self._pattern = pattern
        self._dataset_dto = dataset_dto
        self._source_type = AssetSource.get_asset_source_type(pattern)

    @property
    def tpl_file(self):
        return SINGLE_DATASET_TPL_FILE

    @property
    def entry_template_keys(self):
        return ['dataset_var_name', 'dataset_description', 'get_dataset_code']

    @property
    def get_dataset_code(self):
        if self._pattern.startswith(ModuleUtil.WS_PREFIX):
            _, _, workspace_name = ModuleUtil.match_workspace_tuple(self._pattern)
            ws_var_name = _sanitize_python_variable_name(workspace_name)
            dataset_version = self._dataset_dto.latest.version_id
            dataset_version = "'%s'" % dataset_version if dataset_version else dataset_version
            return self.WS_DATASET_CODE % (ws_var_name, self.dataset_name, dataset_version)
        raise UserErrorException(f'Unknown type of pattern {self._pattern}.')


class ModuleInitGenerator(BaseGenerator):
    LOCAL_HASH_PREFIX = "LOCAL_ASSETS_HASH: "

    def __init__(self, pattern_list, source_dir):
        self._patterns = [pattern for pattern in ModuleUtil.convert_abs_patterns_to_relative(
            pattern_list, source_dir)]
        self._import_names = []

        local_files = [glob.glob(item[len(LOCAL_PREFIX):], recursive=True)
                       for item in pattern_list if item.startswith(LOCAL_PREFIX)]
        local_files = list(itertools.chain.from_iterable(local_files))
        components_yaml_path = Path(source_dir) / COMPONENT_CONFIG_FILE
        if components_yaml_path.exists():
            # Remove components.yaml generated by dsl.generate_package in pattern list
            local_files = [file for file in local_files if not os.path.samefile(file, components_yaml_path)]

        if local_files:
            hasher = hashlib.sha1()
            local_files.sort()
            for item in local_files:
                with open(item, "rb") as f:
                    hasher.update(f.read())
            self._local_asset_hash = hasher.hexdigest()
        else:
            self._local_asset_hash = None

    @property
    def tpl_file(self):
        return MODULE_INIT_TPL_FILE

    @property
    def entry_template_keys(self):
        return ['asset_docstring', 'local_asset_hash', 'asset_func_names', 'asset_pattern', 'asset_exports']

    @property
    def asset_func_names(self):
        return new_line(indent=4).join([''] + [f'{import_name},' for import_name in self._import_names])

    @property
    def asset_exports(self):
        return new_line(indent=4).join([''] + [f'\'{import_name}\',' for import_name in self._import_names])

    @property
    def asset_pattern(self):
        return new_line(indent=4).join([''] + [f'{pattern!r},' for pattern in self._patterns])

    @property
    def asset_docstring(self):
        return new_line(indent=4, meta='- ').join([''] + self._patterns)

    @property
    def local_asset_hash(self):
        if self._local_asset_hash:
            return f"\n\n{self.LOCAL_HASH_PREFIX}{self._local_asset_hash}"
        else:
            return ""

    def set_import_names(self, components, has_datasets_cls, has_models_cls):
        self._import_names = [_sanitize_python_variable_name(component.name) for component in components]
        if has_datasets_cls:
            self._import_names += ['datasets', 'Datasets']
        if has_models_cls:
            self._import_names += ['models', 'Models']


class PackageInitGenerator(BaseGenerator):

    def __init__(self, mode):
        self._mode = mode

    @property
    def mode(self):
        return self._mode

    @property
    def tpl_file(self):
        return PKG_INIT_TPL_FILE

    @property
    def entry_template_keys(self):
        return ["mode", ]


class PackageSetUpGenerator(BaseGenerator):
    def __init__(self, pkg_name):
        self.package_name_param = pkg_name
        self.package_path_param = pkg_name.replace('-', '/')

    @property
    def tpl_file(self):
        return PKG_SETUP_TPL_FILE

    @property
    def entry_template_keys(self):
        return ['package_name_param', 'package_path_param']


class DocConfGenerator(BaseGenerator):
    def __init__(self, pkg_name):
        self.package_name_param = pkg_name

    @property
    def tpl_file(self):
        return DOC_CONF_TPL_FILE

    @property
    def entry_template_keys(self):
        return ['package_name_param']


class DocIndexGenerator(BaseGenerator):
    def __init__(self, pkg_name):
        self.package_name_param = pkg_name

    @property
    def tpl_file(self):
        return DOC_INDEX_TPL_FILE

    @property
    def entry_template_keys(self):
        return ['package_name_param']


class AssetSource(Enum):
    WORKSPACE = 'WORKSPACE'
    REGISTRY = 'REGISTRY'
    LOCAL = 'LOCAL'

    @classmethod
    def get_asset_source_type(cls, pattern):
        if pattern.startswith(ModuleUtil.REGISTRY_PREFIX):
            return AssetSource.REGISTRY
        if pattern.startswith(ModuleUtil.WS_PREFIX):
            return AssetSource.WORKSPACE
        if pattern.startswith(ModuleUtil.LOCAL_PREFIX):
            return AssetSource.LOCAL
        raise UserErrorException(ModuleUtil.INVALID_FORMAT_MSG % pattern)


class ModuleUtil:
    REGISTRY_MATCHER = '^azureml:\\/\\/registries\\/([^\\/]+)/?$'
    WS_MATCHER = '^azureml:\\/\\/subscriptions\\/([0-9a-z-]{36})\\/' \
                 'resourcegroups\\/([^\\/]+)\\/workspaces\\/([^\\/]+)\\/?$'
    GENERAL_ASSET_MATCHER_PART = '\\*\\/?(.*)$'
    COMPONENT_MATCHER_PART = 'components\\/?(.*)$'
    DATASET_MATCHER_PART = 'datasets\\/?(.*)$'
    MODEL_MATCHER_PART = 'models\\/?(.*)$'
    SINGLE_REGISTRY_COMPONENT_MATCHER = \
        '^azureml:\\/\\/registries\\/([^\\/]+)\\/components\\/([^\\/]+)\\/versions\\/([^\\/]+)?$'
    # TODO: link an aka.ms to dsl package doc here.
    VALID_FORMATS = \
        "'azureml://subscriptions/{subscription_id}/resourcegroups/{resource_group}/workspaces/{workspace_name}', " \
        "'azureml://registries/{registry_name}' and 'file:{path}'"
    INVALID_FORMAT_MSG =  \
        f"Invalid assets pattern: %r, valid formats are {VALID_FORMATS}, refer to 'dsl.generate_package'" \
        " function docstring for more details."
    WS_FORMATTER = 'azureml://subscriptions/%s/resourcegroups/%s/workspaces/%s'
    REGISTRY_FORMATTER = 'azureml://registries/%s'
    COMPONENT_FLAG = '/components'
    DATASET_FLAG = '/datasets'
    MODEL_FLAG = '/models'
    MODEL_ATTR_NAME = '_is_model'
    COMPONENT_FORMATTER_PART = COMPONENT_FLAG + '/%s'
    DATASET_FORMATTER_PART = DATASET_FLAG + '/%s'
    MODEL_FORMATTER_PART = MODEL_FLAG + '/%s'
    GENERAL_ASSET_FORMATTER_PART = '/*/%s'
    LOCAL_PREFIX = LOCAL_PREFIX
    WS_PREFIX = 'azureml://subscriptions'
    REGISTRY_PREFIX = 'azureml://registries'

    @staticmethod
    def convert_abs_patterns_to_relative(pattern_list, source_directory):
        """Convert all abs path to relative path before writing into __init__.py."""
        updated_pattern_list = []
        for pattern in pattern_list:
            if pattern.startswith(ModuleUtil.LOCAL_PREFIX):
                # Note: here we call os.path.relpath instead of Path.relative_to because
                # module pattern may not start with source dir
                pattern = ModuleUtil.LOCAL_PREFIX + _relative_path(
                    pattern[len(ModuleUtil.LOCAL_PREFIX):], source_directory).as_posix()
            updated_pattern_list.append(pattern)
        return updated_pattern_list

    @staticmethod
    def convert_relative_pattern_module_to_abs(modules, source_directory):
        """Convert all local path to abs path for follow-up calculation."""
        updated_modules = {}
        with _change_working_dir(source_directory, mkdir=False):
            for module_name, patterns in modules.items():
                if not isinstance(patterns, (list, str)):
                    raise UserErrorException(
                        f'Invalid components value type {type(patterns)}, expected list or str. (value: {patterns!r})')
                updated_modules[module_name] = []
                patterns = [patterns] if isinstance(patterns, str) else patterns
                for pattern in patterns:
                    if pattern.startswith(ModuleUtil.LOCAL_PREFIX):
                        # For local path pattern like ./*, convert to abs path pattern
                        pattern = ModuleUtil.LOCAL_PREFIX + os.path.abspath(pattern[len(ModuleUtil.LOCAL_PREFIX):])
                    updated_modules[module_name].append(pattern)
        return updated_modules

    @staticmethod
    def match_workspace_tuple(_string):
        sub_id, rg, ws_name, _ = ModuleUtil.match_and_refine(
            _string, ModuleUtil.WS_MATCHER, ModuleUtil.WS_FORMATTER, refine_pattern=False)
        return sub_id, rg, ws_name

    @staticmethod
    def match_registry_name(_string):
        registry_name, _ = ModuleUtil.match_and_refine(
            _string, ModuleUtil.REGISTRY_MATCHER, ModuleUtil.REGISTRY_FORMATTER, refine_pattern=False)
        return registry_name

    @staticmethod
    def match_single_registry_component(_string):
        result = re.match(ModuleUtil.SINGLE_REGISTRY_COMPONENT_MATCHER, _string)
        registry_name, component_name, version = tuple(result.groups())
        return registry_name, component_name, version

    @staticmethod
    def match_and_refine(_string, base_matcher, base_formater, refine_pattern=True):
        """
        Match workspace message from string

        :param _string: e.g.
            azureml://subscriptions/sub_id/resourcegroups/rg/workspaces/ws_name/?
            azureml://subscriptions/sub_id/resourcegroups/rg/workspaces/ws_name/components[/(glob)?]?
            azureml://subscriptions/sub_id/resourcegroups/rg/workspaces/ws_name/datasets[/(glob)?]?
        :type _string: str
        :param refine_pattern: refine input string as standard format or not. e.g.
            azureml://subscriptions/sub_id/resourcegroups/rg/workspaces/ws_name/?
            -> subscriptions/sub_id/resourcegroups/rg/workspaces/ws_name/*
        :type refine_pattern: bool
        :return: subscription id, resource group, workspace name and refined string
        :rtype: tuple
        """
        if ModuleUtil.COMPONENT_FLAG in _string:
            # Full component matcher
            matcher = base_matcher[:-2] + ModuleUtil.COMPONENT_MATCHER_PART
            formatter = base_formater + ModuleUtil.COMPONENT_FORMATTER_PART
        elif ModuleUtil.DATASET_FLAG in _string:
            # Full dataset matcher
            matcher = base_matcher[:-2] + ModuleUtil.DATASET_MATCHER_PART
            formatter = base_formater + ModuleUtil.DATASET_FORMATTER_PART
        elif ModuleUtil.MODEL_FLAG in _string and base_matcher == ModuleUtil.REGISTRY_MATCHER:
            # Full model matcher
            matcher = base_matcher[:-2] + ModuleUtil.MODEL_MATCHER_PART
            formatter = base_formater + ModuleUtil.MODEL_FORMATTER_PART
        else:
            # Full general asset matcher
            matcher = base_matcher[:-2] + ModuleUtil.GENERAL_ASSET_MATCHER_PART
            formatter = base_formater + ModuleUtil.GENERAL_ASSET_FORMATTER_PART
        result = re.match(matcher, _string)
        if result is None:
            # Fall back to base matcher
            result = re.match(base_matcher, _string)
            formatter = base_formater + '/*'
        if result is None:
            raise UserErrorException(ModuleUtil.INVALID_FORMAT_MSG % _string)
        if refine_pattern:
            parts = tuple(part if part else '*' for part in result.groups())
            _string = formatter % parts
        if base_matcher == ModuleUtil.WS_MATCHER:
            sub_id, rg, ws_name = tuple(result.groups()[:3])
            return sub_id, rg, ws_name, _string
        else:
            registry_name = result.groups()[0]
            return registry_name, _string


class ModulePackageGenerator:
    def __init__(self, assets, source_directory, func_call_directory,
                 package_name=None, force_regenerate=False, mode=REFERENCE, auth=None, _is_nested_call=False,
                 component_id_2_func_name=None, component_id_2_module_name=None):
        base_dir = func_call_directory
        if isinstance(assets, str):
            with open(os.path.join(source_directory, assets), 'r') as f:
                assets = YAML.safe_load(f).get('assets', {})
            base_dir = source_directory
        if not assets:
            assets = self._assets_from_default(source_directory)
        if isinstance(assets, list):
            assets = self._assets_list_to_dict(assets, source_directory)
        # Note: if assets is read from file, we need calculate abs path with source dir as base
        #       if assets is passed by parameter, we need calculate abs path with func call directory as base
        self._assets = ModuleUtil.convert_relative_pattern_module_to_abs(assets, base_dir)
        self._auth = auth if auth else InteractiveLoginAuthentication()
        self._source_directory = source_directory
        self._pkg_name = package_name
        self._gen_pkg = self._pkg_name and self._pkg_name != '.'
        self._force_regenerate = force_regenerate
        self._mode = mode
        # Lazy load the ws assets
        self._assets_dict = {}
        # Map of module name and the snapshot needs to download.
        self._download_snapshots = {}
        self._downloaded_snapshot_path = set()
        self._is_nested_call = _is_nested_call
        # Mapping from module version id to it's function name and module name
        # the func name and module name are guaranteed to be unique in current pipeline
        self._component_id_2_func_name = component_id_2_func_name
        self._component_id_2_module_name = component_id_2_module_name
        self._warnings = []
        self._errors = []

    @staticmethod
    def _import_or_reload_module(module_name, working_dir):
        # Note: Force reload can not be trigger in _import_component_with_working_dir when module file changes
        # So we manually trigger reload if module already in sys.modules
        if module_name not in sys.modules:
            _import_component_with_working_dir(module_name, working_dir, force_reload=True)
        else:
            importlib.reload(sys.modules[module_name])

    @staticmethod
    def _list_ws_dataset(workspace):
        # Note: For performance issue we will not use Dataset.get_all here.
        from azureml.data._dataset_rest_helper import _restclient, _custom_headers
        result = _restclient(workspace).dataset.list(
            subscription_id=workspace.subscription_id, resource_group_name=workspace.resource_group,
            workspace_name=workspace.name, page_size=500, include_latest_definition=True,
            include_invisible=False, continuation_token=None, custom_headers=_custom_headers)
        all_datasets = result.value
        while result.continuation_token:
            result = _restclient(workspace).dataset.list(
                subscription_id=workspace.subscription_id, resource_group_name=workspace.resource_group,
                workspace_name=workspace.name, page_size=500, include_latest_definition=True,
                include_invisible=False, continuation_token=result.continuation_token, custom_headers=_custom_headers)
            all_datasets += result.value
        return all_datasets

    @staticmethod
    def _list_ws_assets(subscription_id, resource_group, name):
        ws = Workspace.get(subscription_id=subscription_id,
                           resource_group=resource_group,
                           name=name)
        api_caller = ComponentAPI(ws, _logger)
        thread_pool = concurrent.futures.ThreadPoolExecutor()
        tasks = [thread_pool.submit(api_caller.list, basic_info_only=False, module_dto_fields=ModuleDtoFields.ALL),
                 thread_pool.submit(ModulePackageGenerator._list_ws_dataset, ws)]
        concurrent.futures.wait(tasks)
        return tuple([task.result() for task in tasks])

    @staticmethod
    def _list_registry_assets(registry_name, workspace):
        from azure.ml.component._restclients.designer.models import ModuleScope
        registry_names = [registry_name]
        api_caller = ComponentAPI(None, _logger, registry=registry_name)
        components = api_caller.list(module_scope=ModuleScope.REGISTRY,
                                     basic_info_only=False,
                                     module_dto_fields=ModuleDtoFields.ALL)
        registry_assets = {ModuleUtil.REGISTRY_FORMATTER % name: [] for name in registry_names}
        for component in components:
            pattern = ModuleUtil.REGISTRY_FORMATTER % component._registry_name
            if pattern not in registry_assets:
                continue
            registry_assets[pattern].append(component)
        return registry_assets

    def _load_local_definition(self, file_path, source_directory):
        definition = None
        relpath = Path(os.path.relpath(file_path, source_directory)).as_posix()
        # Load definition from yaml
        try:
            # Pre-check schema key
            with open(file_path) as f:
                data = YAML.safe_load(f)
                schema = data.get('$schema')
                if schema is None:
                    self._errors.append(f'FAILED {relpath} - UserError: Missing key \'$schema\' in yaml.')
                    return definition
            definition = ComponentDefinition.load(file_path, _construct_local_runsettings=True)
            _logger.debug(f'Loaded component from file: {relpath!r}')
            setattr(definition, '_source_file_path', file_path)
        except UserErrorException as ex:
            self._errors.append(f'FAILED {relpath} - {str(ex.__class__.__name__)}: {ex.message!r}.')
        except Exception as ex:
            self._errors.append(f'FAILED {relpath} - {str(ex.__class__.__name__)}: {ex!r}.')
        return definition

    @staticmethod
    def _assets_from_default(source_directory):
        workspace = get_workspace(path=source_directory)
        assets = ModuleUtil.WS_FORMATTER % (
            workspace.subscription_id, workspace.resource_group, workspace.name)
        _logger.info(f'Assets for default workspace: {assets!r}')
        return {_sanitize_python_variable_name(workspace.name): [assets]}

    @staticmethod
    def _assets_list_to_dict(assets, source_directory):
        assets_dict = {}

        def add_asset(module_name, asset):
            module_name = '.'.join(_sanitize_python_variable_name(item) for item in module_name.split("."))
            if module_name not in assets_dict:
                assets_dict[module_name] = []
            assets_dict[module_name].append(asset)

        with _change_working_dir(source_directory, mkdir=False):
            for asset in assets:
                # Resolve module name as workspace name/registry name/local
                if asset.startswith(ModuleUtil.WS_PREFIX):
                    _, _, module_name = ModuleUtil.match_workspace_tuple(asset)
                    add_asset(module_name, asset)
                elif asset.startswith(ModuleUtil.REGISTRY_PREFIX):
                    module_name = ModuleUtil.match_registry_name(asset)
                    add_asset(module_name, asset)
                elif asset.startswith(ModuleUtil.LOCAL_PREFIX):
                    for file_path in glob.glob(asset[len(ModuleUtil.LOCAL_PREFIX):], recursive=True):
                        file_path = Path(file_path)
                        if file_path.is_absolute():
                            file_path = file_path.relative_to(source_directory)
                        module_name = str(file_path.parent.parent.as_posix()).replace("/", ".")
                        add_asset(module_name, f"{ModuleUtil.LOCAL_PREFIX}{file_path.absolute().as_posix()}")
                else:
                    raise UserErrorException(ModuleUtil.INVALID_FORMAT_MSG % asset)
        _logger.info(f'Generating assets: {assets}')
        _logger.info(f'Grouped as subpackages: {json.dumps(assets_dict)}.')
        return assets_dict

    @staticmethod
    def _remove_dup_datasets(datasets):
        dataset_names = set()
        model_names = set()
        updated_datasets = []
        for dataset in datasets:
            name = _sanitize_python_variable_name(dataset.name)
            if hasattr(dataset, ModuleUtil.MODEL_ATTR_NAME):
                if name in model_names:
                    _logger.warn(f'Skip {name!r} for duplicate model name found.')
                    continue
                model_names.add(name)
            else:
                if name in dataset_names:
                    _logger.warn(f'Skip {name!r} for duplicate dataset name found.')
                    continue
                dataset_names.add(name)
            updated_datasets.append(dataset)
        return updated_datasets

    def _remove_dup_definition(self, definitions, component_names, is_local=False, key_pattern=None):
        updated_definitions = []
        for definition in definitions:
            name = _sanitize_python_variable_name(definition.name)
            if name in component_names:
                source = getattr(definition, '_source_file_path') if is_local else \
                    key_pattern + '/'.join([ModuleUtil.COMPONENT_FLAG, definition.name])
                self._warnings.append(f'WARNING {source!r}: Skipped for duplicate component name {name!r}.')
                continue
            component_names.add(name)
            updated_definitions.append(definition)
        return updated_definitions

    @staticmethod
    def is_regenerate_module(source_module_dir, init_generator):
        """
        Check if the module needs to be regenerated

        It will check whether the __init__.py of module exists.
        If it exists, it will check if the asset pattern is in the content.
        If there are local yaml files in pattern, it will check whether the hash of the files is the same.

        :param source_module_dir: Path of the module
        :type source_module_dir: str
        :param init_generator: Init generator
        :type init_generator: ModuleInitGenerator
        :return: Whether regenerate the module
        :rtype: bool
        """
        module_init_path = os.path.join(source_module_dir, '__init__.py')

        # Execute to get assets spec if exists init file.
        if os.path.exists(module_init_path):
            with open(module_init_path, 'r') as f:
                assets_spec_code = f.read()
        else:
            # When __init__.py not exist, regenerate the module.
            return True

        # Check assets in __init__.py
        if init_generator.asset_pattern not in assets_spec_code:
            # TODO check workspace/registry assets in the docstring
            return True

        # Local file assets
        local_hash_regex = f"{ModuleInitGenerator.LOCAL_HASH_PREFIX}(.*)"
        regex_result = re.search(local_hash_regex, assets_spec_code, re.MULTILINE)
        origin_local_asset_hash = regex_result.groups()[0] if regex_result else None
        if origin_local_asset_hash == init_generator._local_asset_hash:
            return False
        else:
            return True

    def _download_component_snapshot(self, component_definitions, source_dir, module_name, index=None):
        warning_list = []

        def download_snapshot(source_directory, definition):
            component_module_name = getattr(
                definition, "_module_name", _sanitize_python_variable_name(definition.name))
            module_version = _sanitize_folder_name(definition.version)
            target = os.path.join(source_directory, "components", component_module_name, module_version)
            if target in self._downloaded_snapshot_path:
                warning_list.append(f'WARINING {target!r}: Skipped for duplicate component name '
                                    f'{definition.name!r} found in {module_name}.')
            else:
                self._downloaded_snapshot_path.add(target)
                definition.get_snapshot(target=target, overwrite=True)

        # Download snapshot when mode is Snapshot
        thread_pool = concurrent.futures.ThreadPoolExecutor()
        download_snapshot_tasks = [
            thread_pool.submit(download_snapshot,
                               definition=component_definition,
                               source_directory=source_dir)
            for component_definition in component_definitions]
        # Print out the progress as tasks complete
        list(tqdm(concurrent.futures.as_completed(download_snapshot_tasks), total=len(component_definitions),
                  position=index, desc=module_name, leave=True, unit=' asset'))
        exceptions = [task.exception() for task in download_snapshot_tasks if task.exception()]
        if exceptions:
            # TODO: double check if we can throw all
            raise exceptions[0]
        return warning_list

    def _prepare_assets(self, source_module_dir, asset_value):
        """List all components and datasets from workspace/registry in the asset."""
        from azure.ml.component._restclients.service_caller_factory import _DesignerServiceCallerFactory
        thread_pool, ws_futures, local_futures, registry_futures, assets_dict = \
            concurrent.futures.ThreadPoolExecutor(), {}, {}, {}, {}
        # Prepare workspace assets
        for pattern in asset_value:
            if not pattern.startswith(ModuleUtil.WS_PREFIX):
                continue
            sub_id, rg, ws_name = ModuleUtil.match_workspace_tuple(pattern)
            key = ModuleUtil.WS_FORMATTER % (sub_id, rg, ws_name)
            if key in ws_futures:
                continue
            if key in self._assets_dict:
                assets_dict[key] = self._assets_dict[key]
                continue
            ws_futures[key] = thread_pool.submit(
                ModulePackageGenerator._list_ws_assets, sub_id, rg, ws_name)
        # Prepare local components
        pattern_path = {}
        for pattern in asset_value:
            if not pattern.startswith(ModuleUtil.LOCAL_PREFIX) or pattern in pattern_path:
                continue
            if pattern in self._assets_dict:
                assets_dict[pattern] = self._assets_dict[pattern]
                continue
            file_pattern = pattern[len(ModuleUtil.LOCAL_PREFIX):]
            pattern_path[pattern] = glob.glob(file_pattern, recursive=True)
            components_yaml_path = Path(source_module_dir) / COMPONENT_CONFIG_FILE
            if components_yaml_path.exists():
                # Remove components.yaml generated by dsl.generate_package
                pattern_path[pattern] = [file_path for file_path in pattern_path[pattern]
                                         if not os.path.samefile(components_yaml_path, file_path)]
            # Create caller instance to avoid some components are skipped due to failure of getting auth.
            # Get runsettings directly to avoid sending multiple calls in threadpool.
            _DesignerServiceCallerFactory.get_instance(None).get_component_run_setting_parameters_mapping()
            for file_path in pattern_path[pattern]:
                if file_path in local_futures:
                    continue
                local_futures[file_path] = thread_pool.submit(
                    self._load_local_definition, file_path, self._source_directory)
        # Prepare registry
        for pattern in asset_value:
            if not pattern.startswith(ModuleUtil.REGISTRY_PREFIX):
                continue
            registry_name = ModuleUtil.match_registry_name(pattern)
            if registry_name in registry_futures:
                continue
            workspace = get_workspace(path=self._source_directory)
            registry_futures[registry_name] = thread_pool.submit(
                ModulePackageGenerator._list_registry_assets, registry_name, workspace)

        concurrent.futures.wait([*ws_futures.values(), *local_futures.values(), *registry_futures.values()],
                                return_when=concurrent.futures.ALL_COMPLETED)
        for key, task in ws_futures.items():
            components, datasets = task.result()
            assets_dict[key] = [*components, *datasets]
        for key, path_list in pattern_path.items():
            results = [local_futures[path].result() for path in path_list]
            assets_dict[key] = [result for result in results if result]
        for registry_task in registry_futures.values():
            assets_dict.update(registry_task.result())
        self._assets_dict.update(assets_dict)
        return assets_dict

    def _resolve_assets_in_file(self, assets_dict, module):
        """Filter matched components and datasets for file."""
        module = [module] if isinstance(module, str) else module
        matched_definitions = {}
        matched_datasets = {}
        # Skip and print warning if definition has duplicate component name with another
        # Reserve 'datasets' as we name it to Dataset class instance
        component_names = {'datasets', 'models'}
        # Indicate user specified type or not.
        specify_datasets, specify_models = False, False
        total, generated = 0, 0
        for pattern in module:
            _logger.debug(f'Listing assets from {pattern!r}')
            if ModuleUtil.DATASET_FLAG in pattern:
                specify_datasets = True
            if ModuleUtil.MODEL_FLAG in pattern:
                specify_models = True
            if pattern.startswith(ModuleUtil.LOCAL_PREFIX):
                # Local components
                definitions = assets_dict.get(pattern, None)
                if definitions is None:
                    definitions = [ComponentDefinition.load(file_path) for file_path in glob.glob(pattern)]
                _logger.debug(f'Listed assets from {pattern!r}: {len(definitions)} component(s).')
                total += len(definitions)
                matched_definitions[pattern] = self._remove_dup_definition(
                    definitions=definitions, component_names=component_names, is_local=True)
                generated += len(matched_definitions[pattern])
                continue
            if pattern.startswith(ModuleUtil.WS_PREFIX):
                # Workspace assets
                sub_id, rg, ws_name, pattern = ModuleUtil.match_and_refine(
                    pattern, ModuleUtil.WS_MATCHER, ModuleUtil.WS_FORMATTER)
                # Get ws components from prepared ws components
                key_pattern = ModuleUtil.WS_FORMATTER % (sub_id, rg, ws_name)
                cached_assets = assets_dict.get(key_pattern, None)
                if cached_assets is None:
                    components, datasets = self._list_ws_assets(sub_id, rg, ws_name)
                    cached_assets = [*components, *datasets]
            else:
                # Registry assets
                registry_name, pattern = ModuleUtil.match_and_refine(
                    pattern, ModuleUtil.REGISTRY_MATCHER, ModuleUtil.REGISTRY_FORMATTER)
                key_pattern = ModuleUtil.REGISTRY_FORMATTER % registry_name
                cached_assets = assets_dict.get(key_pattern, None)
                if cached_assets is None:
                    workspace = get_workspace(path=self._source_directory)
                    cached_assets = self._list_registry_assets(registry_name, workspace)[key_pattern]
            if key_pattern not in matched_definitions:
                matched_definitions[key_pattern] = []
                matched_datasets[key_pattern] = []
            definitions = []
            datasets = []
            models = []
            # Get components from prepared assets
            for asset in cached_assets:
                if isinstance(asset, ComponentDefinition):
                    if fnmatch(key_pattern + '/'.join([ModuleUtil.COMPONENT_FLAG, asset.name]), pattern):
                        definitions.append(asset)
                elif hasattr(asset, ModuleUtil.MODEL_ATTR_NAME):
                    if fnmatch(key_pattern + '/'.join([ModuleUtil.MODEL_FLAG, asset.name]), pattern):
                        models.append(asset)
                elif fnmatch(key_pattern + '/'.join([ModuleUtil.DATASET_FLAG, asset.name]), pattern):
                    datasets.append(asset)
            definitions_cnt, datasets_cnt, models_cnt = len(definitions), len(datasets), len(models)
            _logger.info(f'Listed assets from {pattern!r}: {definitions_cnt} component(s), '
                         f'{datasets_cnt} dataset(s), {models_cnt} model(s).')
            total += definitions_cnt + datasets_cnt + models_cnt
            matched_definitions[key_pattern].extend(
                self._remove_dup_definition(definitions, component_names, key_pattern=key_pattern))
            matched_datasets[key_pattern].extend(self._remove_dup_datasets([*datasets, *models]))
            generated += len(matched_datasets[key_pattern]) + len(matched_definitions[key_pattern])
        return matched_definitions, matched_datasets, specify_datasets, specify_models, total, generated

    def generate_pkg_assets_yaml(self, target, source_directory):
        with open(target, 'w', encoding="utf-8") as fout:
            # Convert abs to relative path before write into yaml
            modules_in_file = {
                module_name: ModuleUtil.convert_abs_patterns_to_relative(patterns, source_directory)
                for module_name, patterns in self._assets.items()
            }
            YAML().dump({'assets': modules_in_file}, fout)

    def generate_pkg_tree(self, source_dir):
        # Create top pkg folder
        pkg_tree = self._pkg_name.replace('-', os.sep)
        from ._generate_package import _generate_package
        if os.path.exists(source_dir) and not os.path.isdir(source_dir):
            raise UserErrorException(
                'There is already a file with the same name as the package name you specified. '
                f'Path: {source_dir}')
        os.makedirs(source_dir, exist_ok=True)
        # Generate setup.py for package
        target = os.path.join(source_dir, 'setup.py')
        if not os.path.exists(target) or self._force_regenerate:
            PackageSetUpGenerator(self._pkg_name).to_component_entry_file(target=target)
        # Generate doc conf for package
        doc_dir = os.path.join(source_dir, 'doc')
        os.makedirs(doc_dir, exist_ok=True)
        target = os.path.join(doc_dir, 'conf.py')
        if not os.path.exists(target) or self._force_regenerate:
            DocConfGenerator(self._pkg_name).to_component_entry_file(target=target)
        target = os.path.join(doc_dir, 'index.rst')
        if not os.path.exists(target) or self._force_regenerate:
            DocIndexGenerator(self._pkg_name).to_component_entry_file(target=target)
        os.makedirs(os.path.join(source_dir, pkg_tree), exist_ok=True)
        # Step into inner folder
        for folder_name in pkg_tree.split(os.sep):
            source_dir = os.path.join(source_dir, folder_name)
            # Attach __init__.py
            Path(os.path.join(source_dir, '__init__.py')).touch(exist_ok=True)
        # Generate assets.yaml
        target = os.path.join(source_dir, 'assets.yaml')
        assets_in_file = {}
        if os.path.exists(target):
            # Compare and refresh assets.yaml if exists
            with open(target, 'r') as f:
                assets_in_file = YAML.safe_load(f).get('assets', {})
            # resolve as abs path
            assets_in_file = ModuleUtil.convert_relative_pattern_module_to_abs(assets_in_file, source_dir)
        if not os.path.exists(target) or self._force_regenerate or assets_in_file != self._assets:
            self.generate_pkg_assets_yaml(target, source_dir)
        # Generate __init__.py
        target = os.path.join(source_dir, '__init__.py')
        # File not exists or empty or the mode is modified.
        if os.path.exists(target):
            # Compare and refresh assets.yaml if exists
            with open(target, 'r') as f:
                is_mode_modified = f"mode='{self._mode}'" not in f.read()
        else:
            is_mode_modified = True
        if not os.path.exists(target) or os.stat(target).st_size == 0 or self._force_regenerate or is_mode_modified:
            PackageInitGenerator(mode=self._mode).to_component_entry_file(target=target)
        if self._force_regenerate:
            # Clear module folder if force_regenerate is true
            for module_name in self._assets:
                module_path = os.path.join(source_dir, module_name)
                if not os.path.exists(module_path):
                    continue
                shutil.rmtree(module_path)
        # Run generate package to execute existing __init__.py to complete generate module steps
        _generate_package(
            assets='assets.yaml', source_directory=source_dir, package_name='.',
            mode=self._mode, force_regenerate=self._force_regenerate, auth=self._auth, _is_nested_call=True)

    def generate_module_tree(self, module_name, pattern_list, source_dir):
        # Generate folder for each module
        with TimerContext() as timer:
            source_module_dir = source_dir
            for dir_name in module_name.split("."):
                source_module_dir = os.path.join(source_module_dir, dir_name)
                Path(source_module_dir).mkdir(exist_ok=True, parents=True)
                (Path(source_module_dir) / "__init__.py").touch(exist_ok=True)
            module_init_path = os.path.join(source_module_dir, '__init__.py')
            init_generator = ModuleInitGenerator(pattern_list, source_module_dir)
            assets_spec_code = ''
            # Execute to get assets spec if exists init file.
            if os.path.exists(module_init_path):
                with open(module_init_path, 'r') as f:
                    assets_spec_code = f.read()
            # Reuse module files if pattern same with cached and not force regenerate
            if not self._force_regenerate and not self.is_regenerate_module(source_module_dir, init_generator):
                if self._is_nested_call:
                    # Print message only when calling by generate pkg tree.
                    _logger.info(f'Reusing subpackage {module_name!r} in {timer.get_duration_seconds()} seconds.')
                else:
                    _logger.info(
                        f"Reusing component module {module_name!r} in {timer.get_duration_seconds()} seconds.")
                return
            # Prepare and resolve assets
            assets_dict = self._prepare_assets(source_module_dir, pattern_list)
            components, datasets, specify_datasets, specify_models, total, generated = \
                self._resolve_assets_in_file(assets_dict, pattern_list)
            if total == 0 and not specify_models and not specify_datasets:
                # No assets or class is generated
                self._warnings.append(f'WARNING {module_name!r}: Skip generate subpackage for no asset was listed.')
                return
            _logger.debug(f'Generating subpackage: {module_name!r}')
            # Generate snapshot tasks
            self._generate_snapshot_download_tasks(components, module_name, source_dir)
            # Generate module workspace
            workspace_file_location = os.path.join(source_module_dir, '_workspace.py')
            self._generate_workspace(workspace_file_location, datasets)

            # Generate module assets
            source_directory_relpath = Path(os.path.relpath(source_dir, source_module_dir)).as_posix()
            assets_generator = self._get_assets_generator(
                components, datasets, source_directory_relpath, specify_datasets, specify_models)
            assets_generator.to_component_entry_file(target=os.path.join(source_module_dir, '_assets.py'))
            assets_generator.generate_config(base_folder=source_module_dir, module_folder=source_module_dir)
            # Generate an __init__ for module
            init_generator.set_import_names(
                assets_generator._components, assets_generator._has_datasets_cls, assets_generator._has_models_cls)
            init_generator.to_component_entry_file(target=os.path.join(source_module_dir, '__init__.py'))
            operation = 'Generated' if not assets_spec_code else 'Regenerated'
            _logger.info(f'{operation} subpackage {module_name!r} in {timer.get_duration_seconds()} secondes, '
                         f'total {total} assets, generated {generated}.')

    def generate(self):
        source_dir = Path(self._source_directory)
        if self._gen_pkg:
            _logger.warn(
                "Method generate_package: This is an experimental method, and may change at any time.")
            _logger.info(f'========== Generating package: {self._pkg_name!r}'
                         f'in source directory: {self._source_directory} ========== ')
            source_dir = os.path.join(source_dir, self._pkg_name)
            self.generate_pkg_tree(source_dir)
            pkg_path = self._pkg_name.replace('-', '.')
            module_name = next((name for name in self._assets), '{module_name}')
            _logger.info(f'========== Successfully generated package {self._pkg_name!r}. ========== ')
            _logger.info(f'Please run "pip install -e \'{source_dir}\'" to install the generated python package.')
            _logger.info(f'Then consume with python import statement: \'from {pkg_path}.{module_name} import *\'.')
            return

        def _parallel_execute_tasks(func, params_list):
            with concurrent.futures.ThreadPoolExecutor() as pool:
                tasks = [pool.submit(func, *params) for params in params_list]
                concurrent.futures.wait(tasks, return_when=concurrent.futures.ALL_COMPLETED)
                task_results = [task.result() for task in tasks]
                return task_results

        # Generate module files
        for module_name, pattern_list in self._assets.items():
            if isinstance(pattern_list, str):
                pattern_list = [pattern_list]
            self.generate_module_tree(module_name, pattern_list, source_dir)

        # Download snapshots
        if len(list(itertools.chain(*self._download_snapshots.values()))):
            _logger.info("Creating snapshots...")
            with TimerContext() as timer_context:
                if self._force_regenerate:
                    self._downloaded_snapshot_path.clear()
                warning_lists = _parallel_execute_tasks(
                    func=self._download_component_snapshot,
                    params_list=[
                        (definitions, source_dir, module_name, index) for index, (module_name, definitions) in
                        enumerate(self._download_snapshots.items())]
                )
            _logger.info(f"Finished create snapshots in {timer_context.get_duration_seconds()} seconds.")
            # Print the warnings after snapshot downloaded to avoid affect process bar.
            self._warnings.extend(list(itertools.chain(*warning_lists)))

        self._summary_generate_package_info()

        if self._errors:
            sys.exit(1)

    def _summary_generate_package_info(self):
        print(f"========== Short generate package summary info ==========")
        if self._warnings:
            print('\n'.join(self._warnings))

        if self._errors:
            print('\n'.join(self._errors))
        print(f"========== {len(self._errors)} error, {len(self._warnings)} warning ==========")

    @staticmethod
    def _get_definition_yaml_link(definition):
        if definition._spec_file_path is None and definition._module_dto is None:
            _logger.warning(f'Skip snapshot task for component {definition.name!r} as no yaml path found.')
            return None
        return definition._spec_file_path or definition._module_dto.yaml_link

    def _generate_snapshot_download_tasks(self, components, module_name, source_dir):
        # Generate snapshot tasks for components which need to generate snapshot
        if self._mode == SNAPSHOT:
            # Record the component definitions which needs to download.
            download_snapshot_definitions = set()
            for definition in set(itertools.chain(*components.values())):
                module_name = _sanitize_python_variable_name(definition.name)
                yaml_link = self._get_definition_yaml_link(definition)
                if not yaml_link:
                    continue
                if (definition.snapshot_id or definition._snapshot_local_cache) and yaml_link:
                    # Set relative path of snapshot to source directory to component definition.
                    yaml_path = os.path.join(
                        source_dir, "components", _sanitize_python_variable_name(definition.name),
                        _sanitize_folder_name(definition.version), yaml_link)
                    setattr(definition, '_source_file_path', Path(yaml_path).as_posix())
                    download_snapshot_definitions.add(definition)
            self._download_snapshots[module_name] = download_snapshot_definitions

    def _generate_workspace(self, workspace_file_location, datasets):
        ModuleWorkspaceFileGenerator(datasets.keys()).to_component_entry_file(target=workspace_file_location)

    def _get_assets_generator(self, components, datasets, source_directory_relpath, specify_datasets, specify_models):
        return ModuleAssetsFileGenerator(definitions=components, datasets=datasets,
                                         source_directory_relpath=source_directory_relpath,
                                         specify_datasets=specify_datasets,
                                         specify_models=specify_models, mode=self._mode,
                                         component_id_2_func_name=self._component_id_2_func_name)


class GraphComponentAssetFileGenerator(ModuleAssetsFileGenerator):
    def generate_config(self, base_folder, module_folder):
        # base folder will be parent of components folder
        base_folder = Path(base_folder).absolute().parent
        super(GraphComponentAssetFileGenerator, self).generate_config(base_folder, module_folder)


class GraphComponentSnapshotGenerator(ModulePackageGenerator):
    def __init__(
            self,
            workspace,
            target_directory,
            module_name,
            component_id_2_func_name,
            component_id_2_module_name,
            snapshot_component_ids
    ):
        """Generator used to generate component package in graph to code scenario.

        :param workspace: The workspace for current pipeline.
        :param target_directory: Target directory to generate package.
        :param module_name: Module package's name, normally it'll be "components".
        :param component_id_2_func_name: Mapping from component id to unique function name.
        :param component_id_2_module_name: Mapping from component id to unique module name.
        :param snapshot_component_ids: Module ids which need to generate snapshot.
        """
        self._workspace = workspace
        if component_id_2_func_name is None or component_id_2_module_name is None:
            raise RuntimeError("Parameter component_id_2_func_name or component_id_2_module_name is required.")
        # Use this as pattern for this workspace
        self._workspace_pattern = ModuleUtil.WS_FORMATTER % (
            workspace.subscription_id, workspace.resource_group, workspace.name)
        components_pattern = self._workspace_pattern + ModuleUtil.COMPONENT_FLAG
        self._snapshot_component_ids = snapshot_component_ids
        super(GraphComponentSnapshotGenerator, self).__init__(
            {module_name: components_pattern}, source_directory=target_directory,
            func_call_directory=target_directory,
            package_name=None, force_regenerate=False, mode=REFERENCE, auth=None, _is_nested_call=False,
            component_id_2_func_name=component_id_2_func_name, component_id_2_module_name=component_id_2_module_name
        )

    def _prepare_assets(self, source_module_dir, asset_value):
        """No need to list all assets from workspace."""

    def _get_registry_components(self, registry_ids):
        thread_pool, futures = concurrent.futures.ThreadPoolExecutor(), {}
        component_api = ComponentAPI(workspace=self._workspace, logger=_logger)
        for pattern in registry_ids:
            registry_name, component_name, version = ModuleUtil.match_single_registry_component(pattern)
            if registry_name not in futures:
                futures[registry_name] = []
            futures[registry_name].append(thread_pool.submit(
                component_api.get, registry_name=registry_name, name=component_name, version=version))
        all_task = list(itertools.chain.from_iterable(futures.values()))
        concurrent.futures.wait(
            all_task, return_when=concurrent.futures.ALL_COMPLETED
        )
        registry_mapping = {
            ModuleUtil.REGISTRY_FORMATTER % registry_name: [task.result() for task in tasks]
            for registry_name, tasks in futures.items()
        }
        return registry_mapping, len(all_task)

    def _resolve_assets_in_file(self, assets_dict, module):
        registry_ids = set({
            id for id in self._component_id_2_module_name.keys() if ModuleUtil.REGISTRY_PREFIX in id
        })
        module_version_ids = set(self._component_id_2_module_name.keys()) - registry_ids
        registry_components, registry_number = self._get_registry_components(registry_ids)
        components = ComponentAPI(workspace=self._workspace, logger=_logger).batch_get(
            module_version_ids=list(module_version_ids), name_identifiers=None)
        datasets = {}
        components.sort(key=lambda component: component.name)
        specify_datasets, specify_models = False, False

        total = len(components) + registry_number
        generated = len(components) + registry_number
        components = {
            self._workspace_pattern: components,
            **registry_components
        }
        return components, datasets, specify_datasets, specify_models, total, generated

    def _generate_snapshot_download_tasks(self, components, module_name, source_dir):
        # Generate snapshot tasks for components which need to generate snapshot
        # Record the component definitions which needs to download.
        download_snapshot_definitions = set()
        for definition in set(itertools.chain(*components.values())):
            # Only generate snapshot for specified components
            if definition.identifier not in self._snapshot_component_ids:
                continue
            module_name = self._component_id_2_module_name[definition.identifier]
            yaml_link = self._get_definition_yaml_link(definition)
            if not yaml_link:
                continue
            if (definition.snapshot_id or definition._snapshot_local_cache) and yaml_link:
                # Set relative path of snapshot to source directory to component definition.
                module_version = _sanitize_folder_name(definition.version)
                relpath = os.path.join("components", module_name, module_version, yaml_link)
                # Save (unique) module name for future download
                setattr(definition, '_module_name', module_name)
                setattr(definition, '_source_file_path', Path(relpath).as_posix())
                download_snapshot_definitions.add(definition)
        self._download_snapshots[module_name] = download_snapshot_definitions

    def _generate_workspace(self, workspace_file_location, datasets):
        # For graph scenario, won't generate workspace.py
        pass

    def _get_assets_generator(self, components, datasets, source_directory_relpath, specify_datasets, specify_models):
        return GraphComponentAssetFileGenerator(definitions=components, datasets=datasets,
                                                source_directory_relpath=source_directory_relpath,
                                                specify_datasets=specify_datasets,
                                                specify_models=specify_models, mode=self._mode,
                                                component_id_2_func_name=self._component_id_2_func_name,
                                                snapshot_component_ids=self._snapshot_component_ids)
