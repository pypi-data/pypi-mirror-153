# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import json
import ast
import logging
import os
from pathlib import Path
from papermill.engines import papermill_engines
from azure.ml.component.dsl._component_generator import\
    normalize_working_dir,\
    normalize_entry_path,\
    normalized_target_file,\
    NotebookComponentGenerator
from azure.ml.component._core._types import Input, Output, String, \
    _get_annotation_cls_by_type_name, _Param, _get_annotation_by_value
from azure.ml.component.dsl._utils import logger, NOTEBOOK_EXT
from azure.ml.component.dsl._module_spec import _Dependencies
from azure.ml.component._util._yaml_utils import YAML
from azureml.exceptions._azureml_exception import UserErrorException
from azure.ml.component._notebook.azureml_engine import AzureMLEngine
papermill_engines.register('azureml_engine', AzureMLEngine)
CONDA_FILE = 'conda.yaml'
DEFAULT_PIP_PACKAGES_FOR_NOTEBOOKS_COMPONENT = ['azureml-defaults', 'azure-ml-component[notebooks]']
DEFAULT_PIP_PACKAGES_FOR_NOTEBOOKS_WRAPPER = ['azureml-defaults', 'azureml-pipeline-wrapper[notebooks]']

INPUT_DIRECTORY_CLASS_NAME = 'Input'
OUTPUT_DIRECTORY_CLASS_NAME = 'Output'


class Assignment:
    def __init__(self, name, value, annotation):
        self.name = name
        self.value = value
        self.annotation = annotation

    def __repr__(self):
        return '(%s, %s ,%s)' % (self.name, self.value, self.annotation)


def is_dsl_component_expr(ast_obj):
    """
    Checking this is an expression ast obj like 'dsl.component(...)'.

    :param ast_obj: The ast object.
    :type ast_obj: any

    :return: Whether the ast object is an expression of 'dsl.component(...)'.
    :rtype: boolean
    """
    return isinstance(ast_obj, ast.Expr) and\
        isinstance(ast_obj.value, ast.Call) and\
        isinstance(ast_obj.value.func, ast.Attribute) and\
        isinstance(ast_obj.value.func.value, ast.Name) and\
        ast_obj.value.func.value.id == 'dsl' and\
        (ast_obj.value.func.attr == 'component' or ast_obj.value.func.attr == '_component' or
         ast_obj.value.func.attr == 'module' or ast_obj.value.func.attr == 'command_component')


def parse_ast_body(code_cell):
    """
    Parse the code ast body from cell source code.

    :param code_cell: the code cell to be parsed.
    :type: dict

    :return: The ast body.
    :rtype: list[AST]
    """
    try:
        source = ''.join([line for line in code_cell['source']])
        ast_body = ast.parse(source).body
    except Exception as ex:
        logger.error("Error occurs while trying to ast parse code in notebook")
        logger.error(ex)
        raise
    return ast_body


def extract_assignments(ast_body):
    """
    Get all assignment ast obj from the ast body.

    :param ast_body: the ast body.
    :type: list[AST]

    :return: The assigment in ast body.
    :type: list[Assigment]
    """
    assignments = []
    for ast_obj in ast_body:
        if isinstance(ast_obj, ast.Assign):
            if len(ast_obj.targets) > 0 and isinstance(ast_obj.targets[0], ast.Name):
                assignments.append(Assignment(ast_obj.targets[0].id, ast_obj.value, None))
        elif isinstance(ast_obj, ast.AnnAssign):
            assignments.append(Assignment(ast_obj.target.id, ast_obj.value, ast_obj.annotation))
    return assignments


def find_dsl_component_expr(ast_body):
    """
    Find the expression call dsl.component function in ast body

    :param ast_body: the ast body.
    :type: list[AST]

    :return: The expression ast obj of 'dsl.component(...)'
    :type: ast.Expr
    """
    dsl_component_expr = list(filter(is_dsl_component_expr, ast_body))
    if len(dsl_component_expr) > 0:
        return dsl_component_expr[0]
    return None


def find_dsl_component_ast(notebook_data):
    """
    Find the cell contains expression call dsl.component function in the notebook

    :param notebook_data: the notebook data dictionary
    :type: dict

    :return: The ast body of cell contains "dsl.component(...)"
    :type: list[AST]
    """
    for code_cell in notebook_data['cells']:
        if code_cell['cell_type'] == 'code':
            ast_body = parse_ast_body(code_cell)
            expr = find_dsl_component_expr(ast_body)
            if expr is not None:
                return ast_body
    return None


def convert_basic_type_argument(value, func_name, arg_name=None):
    """
    Convert ast obj of basic type to its value for arguments in function

    :param value: the ast obj of the argument value
    :type value: AST
    :param func_name: the name of the function contains argument
    :type func_name: str
    :param arg_name: the name of the keyword argument
    :type arg_name: str

    :return: the actual value of the argument
    :rtype: str|int|float|boolean|list
    """
    if isinstance(value, ast.Str):
        return value.s
    elif isinstance(value, ast.Num):
        return value.n
    elif isinstance(value, ast.NameConstant):
        return value.value
    elif isinstance(value, ast.List) or isinstance(value, ast.Tuple):
        return [convert_basic_type_argument(val, func_name, arg_name) for val in value.elts]
    else:
        if arg_name:
            errorMessage = "Argument %s of %s in dsl.component cell is assigned to value which is not support." % (
                arg_name,
                func_name)
        else:
            errorMessage = "Argument of %s in dsl.component cell is assigned to value which is not " \
                           "support." % func_name
        errorMessage += "\nSupport value types: number, string, boolean, list, tuple"
        raise UserErrorException(errorMessage)


def extract_args_from_call(func_name, call_ast):
    """
    Get all argument from call ast obj
    :param func_name: the function name of the call obj
    :type func_name: str
    :param call_ast: the ast call obj
    :type call_ast: ast.Call

    :return: the arguments and keyword arguments value in ast call obj
    :type: [], {}
    """
    args = [convert_basic_type_argument(arg, func_name) for arg in call_ast.args]
    keywords = call_ast.keywords
    kwargs = dict((keyword.arg, convert_basic_type_argument(
        keyword.value,
        func_name,
        keyword.arg)) for keyword in keywords)
    return args, kwargs


def replace_kernel_to_notebook(notebook_data):
    """
    Set kernel to notebook to default kernelspec in default conda environment

    :param notebook_data: the notebook data to set kernel
    :type notebook_data: dict
    """
    notebook_data['metadata']['kernelspec'] = dict(
        display_name="python3",
        language="python",
        name="python3"
    )


def tag_parameters_to_notebook(notebook_data):
    """
    Add parameter tag to the cell defines dsl_component and remove for others
    https://papermill.readthedocs.io/en/latest/usage-parameterize.html
    Papermill will add a new cell to overwrite parameters after a cell tags parameters
    So tag 'parameters' to a cell with dsl.component definition and remove others

    :param notebook_data: the notebook data to be add and remove tag
    :type notebook_data: dict
    """
    for cell in notebook_data.get('cells', []):
        if cell.get('cell_type') != 'code':
            continue
        ast_body = parse_ast_body(cell)
        if find_dsl_component_expr(ast_body):
            cell['metadata'].setdefault('tags', []).append('parameters')
        elif 'parameters' in cell['metadata'].setdefault('tags', []):
            cell['metadata']['tags'].remove('parameters')


def convert_notebook(notebook_data):
    """
    Convert a notebook to be executable.
    Need to set kernel & add the cell defines dsl.component with parameters tag
    Please check the papermill doc:
    https://papermill.readthedocs.io/en/latest/troubleshooting.html?highlight=kernel#nosuchkernel-errors-using-conda
    https://papermill.readthedocs.io/en/latest/usage-parameterize.html

    :param notebook_data: the notebook data
    :type notebook_data: dict
    """

    replace_kernel_to_notebook(notebook_data)
    tag_parameters_to_notebook(notebook_data)


def get_assign_value(assign):
    """
    Get real assign value.

    :param assign: The Assignment need to be converted.
    :type assign: Assignment
    :return:
    """
    value = None
    if isinstance(assign.value, ast.Str):
        value = assign.value.s
    elif isinstance(assign.value, ast.Num):
        value = assign.value.n
    elif isinstance(assign.value, ast.NameConstant):
        # NameConstant e.g. None, True, False
        value = assign.value.value
    return value


def extract_metadata_from_dsl_component_ast(dsl_component_ast):
    """
    Get needed metadata from the ast body.

    :param dsl_component_ast: the ast body.
    :type dsl_component_ast: list[AST]
    :return tuple(inputs, outputs, params)
    """
    assignments = extract_assignments(dsl_component_ast)
    annotation_call_assignments = list(filter(lambda assign: isinstance(assign.annotation, ast.Call), assignments))
    inputs = [assign for assign in annotation_call_assignments
              if assign.annotation.func.id == INPUT_DIRECTORY_CLASS_NAME]
    outputs = [assign for assign in annotation_call_assignments
               if assign.annotation.func.id == OUTPUT_DIRECTORY_CLASS_NAME]
    ports = [port.name for port in inputs + outputs]
    params = [assign for assign in assignments if assign.name not in ports]

    return inputs, outputs, params


def gen_component_by_notebook(
    entry: str, target_file=None,
    working_dir=None, force=False
):
    """Generate component from jupyter notebook.

    :param entry: The source file of jupyter notebook.
    :param target_file: The target file for the generated component entry python source file.
    :param working_dir: The source directory of the component.
    :param force: Overwrite existing files.
    :return: The generator object.
    :rtype: azure.ml.component.dsl._component_generator.NotebookComponentGenerator
    """
    working_dir = normalize_working_dir(working_dir)
    notebook_file = normalize_entry_path(working_dir, entry, NOTEBOOK_EXT)
    target_file = normalized_target_file(working_dir, target_file, force)

    generator = NotebookComponentGenerator(notebook_file, notebook_file)

    # Find the cell defined dsl_component
    try:
        with open(os.path.join(working_dir, notebook_file)) as f:
            notebook_data = json.load(f)
    except Exception as ex:
        raise UserErrorException("The notebook '%s' content is invalid. Error: %s" % (
            notebook_file,
            str(ex)))
    logger.info("Extracting dsl component info from the notebook")
    dsl_component_ast = find_dsl_component_ast(notebook_data)
    if dsl_component_ast is None:
        raise UserErrorException("The notebook '%s' does not have a cell which defines dsl.component." % notebook_file)
    # Extract dsl.component arguments
    dsl_component_expr = find_dsl_component_expr(dsl_component_ast)
    annotation = dsl_component_expr.value.func.attr
    is_using_component = annotation in ['component', '_component', 'command_component', 'sweep_component']
    if is_using_component:
        args, kwargs = extract_args_from_call(f'dsl.{annotation}', dsl_component_expr.value)
    else:
        args, kwargs = extract_args_from_call('dsl.module', dsl_component_expr.value)

    # Only support keyword arguments in dsl.component
    generator.update_component_meta(kwargs)

    if generator.job_type != 'basic':
        raise UserErrorException("Only basic component is supported now.")

    inputs, outputs, params = extract_metadata_from_dsl_component_ast(dsl_component_ast)

    for assign in inputs:
        args, kwargs = extract_args_from_call(INPUT_DIRECTORY_CLASS_NAME, assign.annotation)
        port = Input(*args, **kwargs)
        port._name = assign.name
        generator.add_param(port)

    for assign in outputs:
        args, kwargs = extract_args_from_call(OUTPUT_DIRECTORY_CLASS_NAME, assign.annotation)
        port = Output(*args, **kwargs)
        port._name = assign.name
        generator.add_param(port)

    for assign in params:
        # TODO: can we distinguish customer None with real None here?
        # To distinguish default cls from user annotation,
        # fall back to _Param cls with type name 'string' instead of use String cls directly.
        param = _Param()
        assign_value = None
        if assign.annotation:
            # Get parameter type by annotation
            if not hasattr(assign.annotation, 'func'):
                # Plain annotation, could be anything. Ignore it.
                logging.warning(
                    "Parameter {} has unrecognized type annotation and will be ignored.".format(assign.name))
                continue
            annotation_id = assign.annotation.func.id
            args, kwargs = extract_args_from_call(annotation_id, assign.annotation)
            param_cls = _get_annotation_cls_by_type_name(annotation_id)
            if param_cls is None:
                # If the type is not unrecognized, ignore it.
                logging.warning(
                    "Parameter {} has unrecognized type annotation {} and will be ignored.".format(
                        assign.name, annotation_id
                    ))
                continue
            param = param_cls(*args, **kwargs)
        if assign.value is not None:
            if not isinstance(assign.value, (ast.Str, ast.Num, ast.NameConstant)):
                # If the type is not unrecognized, ignore it.
                logging.warning(
                    "Parameter {} has unrecognized assign value {} and will be ignored.".format(
                        assign.name, assign.value
                    ))
                continue
            # Update direct assignment to param default
            # If param is _Param type, infer param type from assign value
            assign_value = get_assign_value(assign)
            if type(param) == _Param:
                param = _get_annotation_by_value(assign_value)()
        # Not annotated and can't infer type, fall back to String.
        if type(param) == _Param:
            param = String()
        param._update_name(assign.name)
        if assign.value is not None:
            param._update_default(assign_value)
        generator.add_param(param)

    if target_file:
        generator.to_component_entry_file(Path(working_dir) / target_file)
        logger.info("Component entry file '%s' is dumped." % target_file)
        target_path = Path(working_dir) / target_file
    else:
        target_path = Path(working_dir) / notebook_file

    # Dump default conda with target file
    target_folder = target_path.parent
    if not (target_folder / CONDA_FILE).exists():
        logger.info("Conda file %s doesn't exist in the folder %s, a default one is dumped." % (
            CONDA_FILE,
            target_folder))
        dep = DEFAULT_PIP_PACKAGES_FOR_NOTEBOOKS_COMPONENT if is_using_component \
            else DEFAULT_PIP_PACKAGES_FOR_NOTEBOOKS_WRAPPER
        YAML._dump_yaml_file(
            _Dependencies.create_default(
                default_pip_packages=dep).conda_dependency_dict,
            target_folder / CONDA_FILE
        )

    return generator
