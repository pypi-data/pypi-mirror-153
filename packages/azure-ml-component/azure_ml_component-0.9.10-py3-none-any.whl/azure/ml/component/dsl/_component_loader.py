# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import re
import importlib
import importlib.util
from pathlib import Path
from omegaconf import OmegaConf
from functools import wraps

from azureml.core.workspace import Workspace
from azureml.exceptions import UserErrorException

from ._utils import ComponentLoaderConfig as StructuredComponentLoaderConfig
from .._util._loggerfactory import _LoggerFactory


VALID_WORKSPACE_COMPONENT_ID = 'azureml://subscriptions/{subscription_id}/resourcegroups/{resource_group}' \
                               '/workspaces/{workspace_name}/components/{name}:{version}'
GLOBAL_CONFIG_NAME = 'global_config.yaml'


class Config:
    CONFIG_KEY = ''
    STRUCTURED_CONFIG = None

    def __init__(self, default_config_path=None, config_key=None):
        structured_config = OmegaConf.structured(self.STRUCTURED_CONFIG) \
            if self.STRUCTURED_CONFIG else OmegaConf.create({})
        if default_config_path:
            default_config = OmegaConf.load(default_config_path)
            if config_key:
                default_config = default_config.get(config_key, {})
            self.default_config = OmegaConf.merge(OmegaConf.to_container(structured_config, resolve=True),
                                                  default_config)
        else:
            self.default_config = structured_config

    @classmethod
    def convert_to_absolute_path(cls, config, conf_keys, config_path):
        """
        Convert relative path to absolute path in the config.

        :param config: The config which need to be updated.
        :type config: DictConfig
        :param conf_keys: The config keys which need to be convert to absolute path in the config.
        :type conf_keys: List[str]
        :param config_path: Config file path.
        :type config_path: str or Path
        """
        config_parent_path = Path(config_path).parent
        for key in conf_keys:
            if OmegaConf.select(config, key):
                OmegaConf.update(config, key, (config_parent_path / config[key]).absolute().as_posix())


class ComponentsConfig(Config):
    CONFIG_KEY = "components"
    YAML_KEY = 'yaml'

    def __init__(self, default_config_path=None, config_key=None):
        super(ComponentsConfig, self).__init__(default_config_path, config_key)
        if default_config_path:
            # Convert yaml path to absolute path.
            for _, component_config in self.default_config.items():
                self.convert_to_absolute_path(component_config, [self.YAML_KEY], default_config_path)


class ComponentLoaderConfig(Config):
    CONFIG_KEY = "component_loader"
    POST_LOAD_KEY = "post_load"
    STRUCTURED_CONFIG = StructuredComponentLoaderConfig

    def __init__(self, default_config_path, config_key):
        super(ComponentLoaderConfig, self).__init__(default_config_path, config_key)
        self._validate_use_local(self.default_config)

    @staticmethod
    def _validate_use_local(config):
        error_format = False
        if "use_local" not in config:
            use_local = "*"
        elif not config.use_local:
            use_local = None
        elif config.use_local == "*":
            use_local = "*"
        else:
            use_local = config.use_local
            if isinstance(use_local, str):
                use_local = [x.strip() for x in config.use_local.split(",")]
            if not use_local or not isinstance(use_local, list) or not all(use_local):
                error_format = True
            else:
                # Check use_local syntax valid, all items are prefixed by ! or not.
                is_other_local = use_local[0].startswith("!")
                error_format = not all([not (item.startswith("!") ^ is_other_local) for item in use_local])

        if error_format:
            raise UserErrorException(
                f'Invalid value for `use_local`. Please follow one of the four patterns: \n'
                f'1) use_local="", all modules are remote\n'
                f'2) use_local="*", all modules are local\n'
                f'3) use_local="MODULE_KEY_1, MODULE_KEY_2", only MODULE_KEY_1, MODULE_KEY_2 are local, '
                f'everything else is remote\n'
                f'4) use_local="!MODULE_KEY_1, !MODULE_KEY_2", all except for MODULE_KEY_1, MODULE_KEY_2 are local'
            )
        return use_local


class ComponentLoader:
    """
    Load component in different ways through the config.
    ComponentLoader exposes two public methods set_override_config and load_component.
    set_override_config is a class method, it's used to set the override config when loading the component.
    load_component is used to load the component is specified by name.

    The component loader provides the following features:
        - Determine the component to be loaded remotely or locally through the component config loader
        - Modify the runsettings of a specific type of component after the component loaded
        - Execute user-defined function after the component loaded.

    Example of loading component by ComponentLoader:
    .. code-block:: python
        # Init component loader
        component_loader = ComponentLoader(default_component_config_path)
        # Load the component by name
        component_func = component_loader(name=<component name>)
        # Create component
        component = component_func()

        # The post function is executed after component loaded.
        def post_load_func(component: azure.ml.component.Component):
            # Update component runsettings after loading.
            component.runsettings.resource_layout.node_count = 1

    Example of component config and component loader config:
    .. code-block:: yaml
        components:
          component1:
            name: Component1
            version: version1
            id: azureml://subscriptions/<subscription_id>/resourcegroups/<resourcegroups>/workspaces
                    /<workspaces>/components/Component1:version1
            yaml: ..\components\component1\version1\module1.spec.yaml
        component_loader:
          use_local: '*'
          post_load: <module_name>:<function_name>
    """

    _default_workspace = None
    _override_components_config = None
    _override_component_loader_config = None

    def __init__(self, default_component_config_path):
        """
        Init component loader.

        :param default_component_config_path: Default component config path
        :type default_component_config_path: str or Path
        """
        self._components_config = ComponentsConfig(default_config_path=default_component_config_path,
                                                   config_key=ComponentsConfig.CONFIG_KEY).default_config
        self._component_loader_config = ComponentLoaderConfig(
            default_config_path=default_component_config_path,
            config_key=ComponentLoaderConfig.CONFIG_KEY
        ).default_config
        self._cache_component_func = {}

    @staticmethod
    def _get_post_component_load_func(component_loader_config):
        """
        Get the user defined post_component_load function from component loader config.

        :param component_loader_config: Component loader config
        :type component_loader_config: DictConfig
        :return: post_component_load function
        :rtype: func
        """
        post_load_func_name = component_loader_config.get(ComponentLoaderConfig.POST_LOAD_KEY, None)
        if post_load_func_name:
            if ':' not in post_load_func_name:
                raise UserErrorException("Wrong format of post_load in the component loader config, "
                                         "please use <module_name>:<post_load_func_name>")
            module_name, func_name = post_load_func_name.rsplit(':', 1)
            try:
                module = importlib.import_module(module_name)
                return getattr(module, func_name)
            except Exception as e:
                raise UserErrorException(f'Cannot import the post component load function "{func_name}"'
                                         f' from the module "{module_name}"')
        else:
            return None

    @staticmethod
    def _is_load_component_from_local(component_name, component_loader_config):
        """
        Check whether the component is loaded from local.

        use_local="", all modules are remote'
        use_local="*", all modules are local
        use_local="component1, component2", only component1, component2 are local, everything else is remote
        use_local="!component1, !component2", all except for component1, component2 are local
        Throw exceptions in other situations

        :param component_name: Component name
        :param component_loader_config: Component loader config.
        :return: Whether component load from local.
        :rtype: bool
        """
        use_local = ComponentLoaderConfig._validate_use_local(component_loader_config)
        if not use_local:
            # If use_local='', all components will be loaded from remote.
            return False
        elif isinstance(use_local, str) and use_local == '*':
            # If use_local='*', all components will be loaded from local.
            return True
        elif use_local[0].startswith("!"):
            # If !component_name in use_local, the component will be loaded from remote.
            return f"!{component_name}" not in use_local
        else:
            # If component name in use_local, the component will be loaded from local.
            return component_name in use_local

    @classmethod
    def _load_component_by_config(cls, component_name, component_config, component_loader):
        """
        Load component by component loader config.

        If the component_name is specified from local, it will use component yaml to load component.
        If the component_name is specified from remote, it will first use workspace/registry id to load if id exists.
        Then, if name and version exists, it will use default workspace to load component.
        If only name exists, it will load default version from default workspace.

        :param component_name: Component name
        :type component_name: str
        :param component_config: Component config
        :type component_config: DictConfig
        :param component_loader: Config of component loader
        :type component_loader: DictConfig
        :return: Component function
        :rtype: func
        """
        from azure.ml.component.component import Component

        def get_component_name_version(component_id):
            component_version_pattern = r".*/components/([\S\s]*)$"
            result = re.match(component_version_pattern, component_id)
            name_version = result.groups()[0]
            if not name_version:
                raise UserErrorException(f'Not specify component name and version in {component_id}, '
                                         'valid format: /components/{name}:{version}')
            if ':' in name_version:
                return tuple(name_version.rsplit(":", 1))
            else:
                return name_version, None

        uuid_pattern = r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
        if cls._is_load_component_from_local(component_name, component_loader) and 'yaml' in component_config:
            # Load component by yaml file.
            return Component.from_yaml(yaml_file=component_config.yaml)
        elif 'id' in component_config:
            from azure.ml.component.dsl._component_generator import ModuleUtil
            if component_config.id.startswith(ModuleUtil.WS_PREFIX):
                # Load component by workspace id.
                try:
                    subscription_id, resource_group, workspace_name = ModuleUtil.match_workspace_tuple(
                        component_config.id)
                except Exception:
                    # Error format of component workspace id.
                    raise UserErrorException(f'Unknown type of component id {component_config.id}, '
                                             f'valid format: {VALID_WORKSPACE_COMPONENT_ID}')
                name, version = get_component_name_version(component_config.id)
                version = component_loader.get('force_version') or version
                workspace = Workspace.get(name=workspace_name,
                                          subscription_id=subscription_id,
                                          resource_group=resource_group)
                return Component.load(workspace=workspace, name=name,
                                      version=version)
            elif component_config.id.startswith(ModuleUtil.REGISTRY_PREFIX):
                # Load component by registry.
                from azure.ml.component.dsl import _assets
                registry_name = ModuleUtil.match_registry_name(component_config.id)
                name, version = get_component_name_version(component_config.id)
                return _assets.load_component(workspace=None, name=name, version=version, registry_name=registry_name)
            elif re.match(uuid_pattern, component_config.id.lower()):
                if not cls._default_workspace:
                    cls._default_workspace = Workspace.from_config()
                return Component.load(workspace=cls._default_workspace, id=component_config.id)
            else:
                raise UserErrorException(f'Unknown type of component id {component_config.id}.')
        elif 'name' in component_config:
            # Load component by component name and version.
            default_version = \
                component_loader.get('force_version') or component_config.get('version') or \
                component_loader.get('default_version')
            if not cls._default_workspace:
                cls._default_workspace = Workspace.from_config()
            return Component.load(workspace=cls._default_workspace,
                                  name=component_config.name,
                                  version=default_version)
        else:
            raise UserErrorException("Cannot load component through the component config.")

    @classmethod
    def set_override_config(cls, components_config=None, component_loader_config=None):
        """
        Set the override config when loading component.

        It will set component config and component loader config to the override config of ComponentLoader.
        Override config of ComponentLoader has higher priority than the object config.
        When loading the component, it will first use override config.

        :param components_config: Override component config
        :type components_config: DictConfig
        :param component_loader_config: Override config of component loader
        :type component_loader_config: DictConfig
        """
        cls._override_component_loader_config = component_loader_config
        cls._override_components_config = components_config

    def load_component(self, name):
        """
        Load the component by name.

        It will use the name to get the config of the component and component loader.
        Then it will use these configs to load the components. Override config of ComponentLoader has higher priority
        than the default config. If not found override config, it will use the default config to load the component.
        After loading the component function, if user defines the post component load function,
        it will execute user defined function after the component initialize.

        :param name: The name of the component to be loaded
        :type name: str
        :return: Component function
        :rtype: func
        """
        if name in self._cache_component_func:
            return self._cache_component_func[name]

        if self._override_components_config:
            component_config = self._override_components_config.get(name) or self._components_config.get(name)
        else:
            component_config = self._components_config.get(name)
        if not component_config:
            raise UserErrorException(f"Cannot find {name} in the components config.")

        # Get the component function by config
        component_loader_config = self._override_component_loader_config or self._component_loader_config
        component_func = self._load_component_by_config(name, component_config, component_loader_config)
        post_component_load_func = self._get_post_component_load_func(component_loader_config)

        @wraps(component_func)
        def wrapper(*args, **kwargs):
            component = component_func(*args, **kwargs)
            if component._module_dto and component._module_dto.default_version and \
                    component._module_dto.default_version != component.version:
                _LoggerFactory.get_logger().warning(
                    f"The loaded component version {component.version} is not default version, "
                    f"default version is {component._module_dto.default_version}")
            if post_component_load_func:
                try:
                    # Execute user defined function after component load.
                    post_component_load_func(component)
                except Exception as e:
                    raise UserErrorException(f"Post component load func failed. {e}")
            return component

        self._cache_component_func[name] = wrapper
        return wrapper
