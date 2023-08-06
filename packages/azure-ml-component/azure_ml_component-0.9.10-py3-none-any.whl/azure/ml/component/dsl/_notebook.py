# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Contains function to execute notebook
"""
import os
import json
import tempfile
from azureml.core.run import Run


def execute_notebook(entry_notebook: str, output_notebook: str, parameters: dict):
    """
    Execute notebook with parameters.
    The notebook must contain a cell call dsl.component().
    Other variables in the cell will be overwrite by parameters.

    :param entry_notebook: The notebook to be executed
    :type entry_notebook: str
    :param output_notebook: The notebook output
    :type output_notebook: str
    :param parameters: parameters that will be overwrite in the notebook
    :type parameters: dict
    """
    # Only executable with azure-ml-component[notebooks]
    import papermill as pm
    with open(entry_notebook) as nbfile:
        notebook_data = json.load(nbfile)

    from azure.ml.component.dsl._component_from_notebook import convert_notebook
    convert_notebook(notebook_data)
    # Create a new temp notebook file
    input_notebook = tempfile.mkstemp(suffix='.ipynb')[1]
    with open(input_notebook, 'w') as f:
        json.dump(notebook_data, f, indent=4)

    papermill_args = dict(
        progress_bar=False,
        log_output=True,
        engine_name="azureml_engine",
        input_path=input_notebook,
        output_path=output_notebook,
        history=True,  # For using scrapbook to log metrics
        parameters=parameters
    )
    try:
        pm.execute_notebook(**papermill_args)
    finally:
        if os.path.exists(output_notebook):
            context = Run.get_context()
            context.upload_file('output_notebook.ipynb', output_notebook)
