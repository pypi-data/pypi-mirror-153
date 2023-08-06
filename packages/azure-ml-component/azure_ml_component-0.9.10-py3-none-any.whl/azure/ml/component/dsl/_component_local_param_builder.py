# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import os
from pathlib import Path
from typing import Union, List

from azure.ml.component import Component
from azure.ml.component._core._component_definition import ComponentDefinition
from azure.ml.component.dsl._constants import DATA_FOLDER, INPUTS_FOLDER, OUTPUTS_FOLDER
from azure.ml.component.dsl._utils import _sanitize_python_variable_name
from azure.ml.component.dsl._component_generator import DSLCommandLineGenerator
from azure.ml.component.dsl._module_spec import OutputPort, InputPort, _get_io_spec_from_component


class _ComponentLocalParamBuilder:
    """Generate default input/output, param and command for component."""

    def __init__(self, input_ports, output_ports, params, source_directory: Path, component_file_name: str):
        self.input_ports = input_ports
        self.output_ports = output_ports
        self.params = params
        # Source directory should be a valid path.
        if not source_directory.exists():
            raise KeyError(f'Source directory {source_directory} does not exist.')
        self.source_folder = source_directory

        self.data_folder = self.source_folder / DATA_FOLDER
        self.input_dir = self.data_folder / component_file_name / INPUTS_FOLDER
        self.output_dir = self.data_folder / component_file_name / OUTPUTS_FOLDER

        self.inputs = {}
        self.outputs = {}
        self.parameters = {}
        # for vscode launch.json
        self.arguments = []

        self.component_file_name = component_file_name

    def build(self, dry_run=False):
        """Build default input/output, param and command.

        :param dry_run: If specified, won't create input/output.
        """
        # clear existing val
        self.inputs = {}
        self.outputs = {}
        self.parameters = {}
        self.arguments = []

        # build input
        self._build_port_argument(self.input_ports, self.input_dir, self.inputs, dry_run)

        # build output
        self._build_port_argument(self.output_ports, self.output_dir, self.outputs, dry_run)

        # build parameters
        for param in self.params:
            key = _sanitize_python_variable_name(param.name)
            if param.default is not None:
                val = param.default
            else:
                val = f'input parameter for {key}'
            self.parameters[key] = val
            self.arguments += [self._to_cli_option_str(param), str(val)]

    def _build_port_argument(self, ports: List[Union[InputPort, OutputPort]],
                             port_dir: Path, port_dict: dict, dry_run=False):
        """Build input/output data

        :param ports: Input/output port.
        :param port_dir: Input/Output directory.
        :param port_dict: Input/Output dictionary.
        :param dry_run: If specified, won't create input/output.
        """
        for port in ports:
            key = _sanitize_python_variable_name(port.name)
            port_path = port_dir / key
            # port value relative to data folder
            value = str(port_path.relative_to(self.data_folder).as_posix())
            port_dict[key] = value
            # arguments relative to source directory
            self.arguments += [self._to_cli_option_str(port),
                               str(port_path.relative_to(self.source_folder).as_posix())]

            if not dry_run:
                if port.type in {'AnyDirectory', 'path'}:
                    os.makedirs(port_path, exist_ok=True)
                elif port.type == 'AnyFile':
                    os.makedirs(str(port_dir), exist_ok=True)
                    open(port_path, 'a').close()
                else:
                    from azure.ml.component.dsl._utils import logger
                    logger.warning('Did not generate file/folder for port {}.'.format(port.name))

    def _to_cli_option_str(self, param):
        return DSLCommandLineGenerator(param).arg_string


class _ComponentLocalParamBuilderFromSpec(_ComponentLocalParamBuilder):
    def __init__(self, spec: ComponentDefinition, source_directory: Path, component_file_name: str):
        super(_ComponentLocalParamBuilderFromSpec, self).__init__(
            spec.inputs.values(), spec.outputs.values(), spec.parameters.values(),
            source_directory, component_file_name,
        )


class _ComponentLocalParamBuilderFromDefinition(_ComponentLocalParamBuilder):
    def __init__(self, component: Component, source_directory: Path):
        self.component = component
        inputs, outputs, params = _get_io_spec_from_component(component)
        self.component_entry = component._module_dto.entry
        if not self.component_entry.endswith('.py'):
            raise RuntimeError(f'Component entry: {self.component_entry} for component {component.name}'
                               ' did not ends with .py.')
        component_file_name = self.component_entry[:-3]

        super().__init__(inputs, outputs, params, source_directory, component_file_name)

    def build(self, dry_run=False):
        """Build default input/output, param and command.

        :param dry_run: If specified, won't create input/output.
        """
        super().build(dry_run)
        if not dry_run:
            self.component.set_inputs(**self.inputs, **self.parameters)
