# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import argparse
import sys
import runpy
import importlib
from pathlib import Path

from azure.ml.component._util._exceptions import CustomerCodeError
from azure.ml.component.dsl._component_generator import ArgParseComponentGenerator, ArgParseParamGenerator, \
    normalize_working_dir, normalize_entry_path, normalized_target_file, normalized_spec_file, \
    StoreFalseParam, StoreTrueParam
from azure.ml.component.dsl._module_spec import Param
from azure.ml.component.dsl._utils import logger, inject_sys_path, is_py_file
from azure.ml.component._util._utils import _sanitize_python_variable_name


def gen_component_by_argparse(
    entry: str, target_file=None, spec_file=None,
    working_dir=None, force=False,
    inputs=None, outputs=None,
    component_meta=None,
):
    working_dir = normalize_working_dir(working_dir)
    job_type = component_meta.get('job_type') if isinstance(component_meta, dict) else None
    entry = normalize_entry_path(working_dir, entry, '.py', job_type)
    target_file = normalized_target_file(working_dir, target_file, force)
    spec_file = normalized_spec_file(working_dir, spec_file, force)

    with inject_sys_path(working_dir):
        with ArgumentParserWrapper(entry=entry) as wrapper:
            try:
                _invoke_module(entry, working_dir, job_type)
            except ImportError as e:
                # For ImportError, it could be environment problems, just raise it.
                raise CustomerCodeError('Failed to invoke {} from argparse'.format(entry), inner_exception=e) from e
            except BaseException as e:
                # If the entry is correctly returned, wrapper.succeeded will be True
                # Otherwise it is not run correctly, just raise an exception.
                if not wrapper.succeeded:
                    exception_msg_line = str(e).replace('\n', ' ')  # Replace \n to make sure the msg is one line.
                    msg = "Run entry '%s' failed, please make sure it uses argparse correctly, exception: %s" % (
                        entry, exception_msg_line)
                    raise CustomerCodeError(msg, inner_exception=e) from e
            if not wrapper.succeeded:
                raise CustomerCodeError("Entry '%s' doesn't call parser.parse_known_args()." % entry)

            if wrapper.generator.name is None:
                wrapper.generator.set_name(entry)

            wrapper.generator.set_entry(entry)

            if component_meta:
                wrapper.generator.update_component_meta(component_meta)

            if inputs:
                wrapper.generator.update_spec_params(inputs, is_output=False)
            if outputs:
                wrapper.generator.update_spec_params(outputs, is_output=True)

            if target_file:
                wrapper.generator.to_component_entry_file(Path(working_dir) / target_file)
                logger.info("Module entry file '%s' is dumped." % target_file)

            if spec_file:
                wrapper.generator.to_spec_yaml(working_dir, spec_file)
                logger.info("Module spec file '%s' is dumped." % spec_file)


def _invoke_module(entry, working_dir, job_type=None):
    if job_type == 'parallel':
        score_module = importlib.import_module(entry)
        if hasattr(score_module, 'init'):
            score_module.init()
        score_module.run([])
    else:
        if is_py_file(entry):
            logger.info("Run py file '%s' to get the args in argparser." % entry)
            runpy.run_path(str(Path(working_dir) / entry), run_name='__main__')
        else:
            logger.info("Run py module '%s' to get the args in argparser." % entry)
            runpy.run_module(entry, run_name='__main__')


ORIGINAL_ARGUMENT_PARSER = argparse.ArgumentParser


class _ArgumentParser(argparse.ArgumentParser):
    """This is a class used for generate dsl.component with an existing main code with argparser.

    Usage:
    Replace argparse.ArgumentParser with this _ArgumentParser,
    then when the entry file is called by "python entry.py",
    your code will not be run, a ModuleGenerator will be prepared for generating dsl.component.
    """
    def __init__(self, prog=None, *args, **kwargs):
        """Init the ArgumentParser with spec args."""
        argparse.ArgumentParser = ORIGINAL_ARGUMENT_PARSER
        super().__init__(prog, *args, **kwargs)
        self.injected_generator = ArgParseComponentGenerator(description=self.description or self.usage)
        if prog:
            self.injected_generator.set_name(name=prog)
        self.parsed = False

    @classmethod
    def _get_best_arg_string(cls, arg_strings):
        """Get the best arg string to construct parameter.

        Here we prefer to use the arg string with '--' instead of '-' which could be used to match input/output.
        ['-i', '--input'] => '--input'  Choose the one use --
        If only the arg string with '-' like '-i' is provided, we use the first arg string.
        ['-ii', '-i'] => '-ii'  Choose the first one
        """
        arg_string_with_two_dashes = next((arg for arg in arg_strings if arg.startswith('--')), None)
        return arg_strings[0] if arg_string_with_two_dashes is None else arg_string_with_two_dashes

    def add_argument(self, *args, **kwargs):
        """Call add_argument of ArgumentParser and add the argument to spec."""
        # Get the argument.
        result = super().add_argument(*args, **kwargs)

        action = kwargs.get('action')
        # The action help is used for help message, which is useless.
        if action == 'help':
            return result
        # Currently we only support default action 'store', AzureML cannot support others.
        if action and action not in {'store', 'store_true', 'store_false'}:
            logger.warning("Argument action type '%s' of '%s' is not supported now, ignored." % (action, result.dest))
            return result

        # Ignore the case add_argument('some_arg')
        if not result.option_strings:
            msg = "Argument %r without option_string(--xx) is not supported now, " % result.dest + \
                "ignored in the generated code, " \
                "you may update the generated code to make sure the component is correct."
            logger.warning(msg)
            return result

        # Get meta information of the argument.
        options = result.choices if result.type in {None, str} else []  # Only str type enum is valid.
        param_type = 'Enum' if options else ArgParseParamGenerator.mapping.get(result.type, 'String')
        default = result.default if result.default != argparse.SUPPRESS and result.default != [] else None
        optional = not result.required or default is not None
        # Make sure this is valid
        name = _sanitize_python_variable_name(result.dest)

        param = Param(
            name=name, type=param_type,
            enum=options, description=result.help,
            default=default, optional=optional,
            arg_name=name,
            arg_string=self._get_best_arg_string(result.option_strings),
        )
        if action == 'store_true':
            param = StoreTrueParam(
                name=name, description=result.help, default=default,
                arg_name=result.dest, arg_string=self._get_best_arg_string(result.option_strings),
            )
        elif action == 'store_false':
            param = StoreFalseParam(
                name=name, description=result.help, default=default,
                arg_name=result.dest, arg_string=self._get_best_arg_string(result.option_strings),
            )

        # Add param to the generator.
        self.injected_generator.add_param(param)
        # Return the result to make sure the result is ok.
        return result

    def parse_known_args(self, args=None, namespace=None):
        # Set parsed=True then exit the program.
        # Note that parser.parse_args will also call parse_known_args, so both call are supported.
        self.parsed = True
        sys.exit(0)


class ArgumentParserWrapper:

    def __init__(self, entry):
        self._generator = None
        self._parser = None
        self._entry = entry

    def __enter__(self):
        that = self
        # Once using with(), store original ArgumentParser for recovering,
        # then set argparse.ArgumentParser = WrapperdArgumentParser

        class WrapperdArgumentParser(_ArgumentParser):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                that._parser = self
        argparse.ArgumentParser = WrapperdArgumentParser
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        argparse.ArgumentParser = ORIGINAL_ARGUMENT_PARSER

    @property
    def parser(self):
        return self._parser

    @property
    def generator(self):
        return self._parser.injected_generator

    @property
    def succeeded(self):
        return self._parser and self._parser.parsed
