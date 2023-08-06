# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import os

from azure.ml.component._api._utils import is_absolute
from azure.ml.component._util._loggerfactory import _PUBLIC_API, track, _LoggerFactory
from azure.ml.component.dsl._utils import _change_working_dir, _resolve_source_directory
from azureml.exceptions import UserErrorException
from azure.ml.component._util._utils import TimerContext

from ._component_generator import ModulePackageGenerator, REFERENCE, SNAPSHOT


_logger = None


def _get_logger():
    global _logger
    if _logger is not None:
        return _logger
    _logger = _LoggerFactory.get_logger()
    return _logger


@track(_get_logger, activity_type=_PUBLIC_API, activity_name="dsl_generate_package", is_long_running=True)
def _generate_package(*, assets=None, package_name='assets', source_directory=None,
                      force_regenerate=False, mode="reference", auth=None, **kwargs):
    """
    This is an experimental method, and may change at any time.

    For a set of components, generate python package which contains component consumption functions and import it
    for use.

    :param assets: None, list[assets_pattern], dict[sub_package_name, assets_pattern] or str.

        * None: generate package for assets in default workspace. i.e. Workspace.from_config()

        * list[assets]: assets pattern list, generate packages with name:
          {workspace_name} or {feed_name}, or 'local' for local yaml files.

            .. code-block:: python

                # assets will be grouped into three sub packages: 'local', 'workspace_name', 'my_feed'
                assets = [
                    'file:*.yaml',
                    'azureml://subscriptions/{subscription_id}/resourcegroups/{resource_group}'\
                        '/workspaces/{workspace_name}'
                    'azureml://registries/my_registry',
                ]

        * dict[sub_package_name, assets_identifier]: sub package name as key and assets_identifier as value

            .. code-block:: python

                # sub_package_name with an assets identifier
                assets = {"sub_package_name": "azureml://subscriptions/{subscription_id}/"
                                         "resourcegroups/{resource_group}/workspaces/{workspace_name}"}
                # sub_package_name with a list of assets identifier
                assets = {"sub_package_name": ["azureml://subscriptions/{subscription_id}/"
                                          "resourcegroups/{resource_group}/workspaces/{workspace_name}",
                                          "file:components/**/module_spec.yaml"]}

        * str: specify as ``assets.yaml`` config file which contains the assets dict

        .. remarks::

            sub_package_name: a string which is the name of the generated python sub package.
            components: single or list of glob string which specify a set of components. Example values:
                * assets from workspace
                    1. all assets
                        ``azureml://subscriptions/{subscription_id}/resource_group/{resource_group}/
                        workspaces/{workspace_name}``
                    2. components with name filter
                        ``azureml://subscriptions/{subscription_id}/resource_group/{resource_group}
                        /workspaces/{workspace_name}/components/microsoft_samples_*``
                    3. datasets
                        ``azureml://subscriptions/{subscription_id}/resource_group/{resource_group}
                        /workspaces/{workspace_name}/datasets``
                * components from local yaml
                    ``file:components/**/module_spec.yaml``
                * components from registry. For registry concept, please see: https://aka.ms/azuremlsharing.
                    1. All assets in registry
                        ``azureml://registries/azureml``
                    2. components which name contains 'Convert'
                        ``azureml://registries/azureml/components/*Convert*``

    :type assets: Union[None, list, dict, str]
    :param source_directory: parent folder to generate source code.

        * If not specified, we generate the file relative to the folder of python file that triggers the
          dsl.generate_package call.

        * If specified, we also generate all non-exist intermediate path.

    :type source_directory: str
    :param package_name: name of the generated python pip package. Example: cool-component-package .

        * If specified, we create a package directory under ``{source_directory}``.
            * If the cool-component-package folder does not exists,
              we will create a new skeleton package under ``{source_directory}/cool-component-package``
              and print info in command line and ask user to do:
              ``pip install -e {source_directory}/cool-component-package``.
              The next user can do: ``from cool.component.package import sub_package_name``
            * If the folder exists, we trigger the __init__.py in the folder.
        * If specified '.', we skip generate the root package directory and just generate the subpackages.

    :type package_name: str
    :param force_regenerate: whether to force regenerate the python module file.

        * If True, will always generate and re-import the newly generated file.
        * If False, will reuse previous generated file. If the existing file not valid, raise import error.

    :type force_regenerate: bool
    :param mode: whether to retain a snapshot of assets in package.

        * reference: will not build/download snapshot of asset, and load by name for remote assets.
        * snapshot: will build/download snapshot of asset, and load from local yaml.

    :type mode: str
    :param auth: The authentication object. For more details, see https://aka.ms/aml-notebook-auth.
        If None and need auth, the default Azure CLI credentials will be used or the API will prompt for credentials.
    :type auth: azureml.core.authentication.ServicePrincipalAuthentication or
        azureml.core.authentication.InteractiveLoginAuthentication
    """
    with TimerContext() as timer:
        # Resolve the customer function call directory for calculate relative path
        func_call_directory = _resolve_source_directory()
        if not source_directory:
            source_directory = func_call_directory
        elif not is_absolute(source_directory):
            # Resolve absolute path if source_directory is relative path
            # Note: source directory may be different with customer function call directory
            with _change_working_dir(func_call_directory, mkdir=False):
                source_directory = os.path.abspath(source_directory)
        if assets and not isinstance(assets, (str, dict, list)):
            raise UserErrorException(f'Unexpected assets value {assets}, expected type list, dict or file name str.')
        support_mode = [REFERENCE, SNAPSHOT]
        if mode not in support_mode:
            raise UserErrorException(f'Unexpected mode value {mode}, expected {support_mode}.')
        # _nested_call is True if is calling from generate package tree.
        _is_nested_call = kwargs.get('_is_nested_call', False)
        ModulePackageGenerator(
            assets, source_directory, func_call_directory, package_name,
            force_regenerate, mode, auth, _is_nested_call).generate()
        if not _is_nested_call:
            _get_logger().info(f"Finished generating packages in {timer.get_duration_seconds()} seconds")
