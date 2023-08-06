# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from collections import OrderedDict
from collections.abc import Hashable
from pathlib import Path

from ruamel.yaml import YAML as _YAML, Loader, MappingNode, SequenceNode, ScalarNode
from ruamel.yaml import Dumper
from ruamel.yaml.compat import StringIO
from ruamel.yaml.constructor import ConstructorError


class YamlFlowDict(dict):
    """This class is used to dump dict data with flow_style."""

    @classmethod
    def representer(cls, dumper: Dumper, data):
        return dumper.represent_mapping('tag:yaml.org,2002:map', data, flow_style=True)


class YamlFlowList(list):
    """This class is used to dump list data with flow_style."""

    @classmethod
    def representer(cls, dumper: Dumper, data):
        return dumper.represent_sequence('tag:yaml.org,2002:seq', data, flow_style=True)


class YamlMultiLineStr(str):
    """
    This class is used to dump multi-line str with > style.

    For more information about the style, refer to https://yaml-multiline.info/.
    """
    @classmethod
    def representer(cls, dumper: Dumper, data):
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='>')


def _str_representer(dumper: Dumper, data):
    """Dump a string with normal style or '|' style according to whether it has multiple lines."""
    style = ''
    if '\n' in data:
        style = '|'
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style=style)


def _enum_reserved_mapping_constructor(loader: Loader, node):
    """Load mapping with each enum value raw string."""
    # See reference code to ruamel.yaml.constructor.BaseConstructor.construct_mapping
    deep = True
    if not isinstance(node, MappingNode):
        raise ConstructorError(
            None,
            None,
            f'expected a mapping node, but found {node.id!s}',
            node.start_mark,
        )
    total_mapping = loader.yaml_base_dict_type()
    if getattr(node, 'merge', None) is not None:
        todo = [(node.merge, False), (node.value, False)]
    else:
        todo = [(node.value, True)]
    for values, check in todo:
        mapping = loader.yaml_base_dict_type()  # type: Dict[Any, Any]
        for key_node, value_node in values:
            # keys can be list -> deep
            key = loader.construct_object(key_node, deep=True)
            # lists are not hashable, but tuples are
            if not isinstance(key, Hashable):
                if isinstance(key, list):
                    key = tuple(key)
            if not isinstance(key, Hashable):
                raise ConstructorError(
                    'while constructing a mapping',
                    node.start_mark,
                    'found unhashable key',
                    key_node.start_mark,
                )
            # For enum and str type, load each enum value and default as raw string.
            if key in ['enum', 'default'] and mapping.get('type', None) in ['enum', 'string', 'Enum', 'String']:
                if isinstance(value_node, SequenceNode):
                    value = [loader.construct_scalar(child) for child in value_node.value]
                elif isinstance(value_node, ScalarNode):
                    value = value_node.value
                else:
                    # Fall back to construct_object
                    value = loader.construct_object(value_node, deep=deep)
            else:
                value = loader.construct_object(value_node, deep=deep)
            if check:
                if loader.check_mapping_key(node, key_node, mapping, key, value):
                    mapping[key] = value
            else:
                mapping[key] = value
        total_mapping.update(mapping)
    return total_mapping


class YAML(_YAML):
    """
    Note:
        - Use the static method safe_load if dict type result is what you want.
        - Set typ as 'unsafe' could improve performance if use customer representer.
        - A 'StringIO()' has been added to dump() if stream is None.
    """
    YAML_HELP_COMMENTS = """#  This is an auto generated component spec yaml file.
#  For more details, please refer to https://aka.ms/azure-ml-component-specs
"""

    def __init__(self, typ='rt', with_additional_representer=False):
        """
        Set up and get a yaml instance.

        :param typ: 'rt'/None -> RoundTripLoader/RoundTripDumper,  (default)
                    'safe'    -> SafeLoader/SafeDumper,
                    'unsafe'  -> normal/unsafe Loader/Dumper
                    'base'    -> baseloader
                    For more information, please refer to ruamel.yaml.YAML document at
                     https://yaml.readthedocs.io/en/latest/overview.html.
        :param with_additional_representer: Add additional representer or not.
        """
        super().__init__(typ=typ, pure=True)
        self.default_flow_style = False
        self.allow_unicode = True
        self.encoding = 'utf-8'
        if with_additional_representer:
            self.representer.add_representer(YamlFlowDict, YamlFlowDict.representer)
            self.representer.add_representer(YamlFlowList, YamlFlowList.representer)
            self.representer.add_representer(YamlMultiLineStr, YamlMultiLineStr.representer)
            self.representer.add_representer(str, _str_representer)
            self.representer.add_representer(
                type(None), lambda dumper, value: dumper.represent_scalar(u'tag:yaml.org,2002:null', ''))

            # Setup to preserve order in yaml.dump, see https://stackoverflow.com/a/8661021
            def _represent_dict_order(self, data):
                return self.represent_mapping("tag:yaml.org,2002:map", data.items())

            self.representer.add_representer(OrderedDict, _represent_dict_order)

    def dump(self, data, stream=None, **kw):
        # Rewrite dump function and add default StringIO when dump without stream.
        inefficient = False
        if stream is None:
            inefficient = True
            stream = StringIO()
        _YAML.dump(self, data, stream, **kw)
        if inefficient:
            return stream.getvalue()

    @staticmethod
    def _dump_yaml_file(data, file, *, unsafe=False, header=None, **kwargs):
        """Dump data as a yaml file.

        :param data: The data which will be dumped.
        :param file: The target yaml file to be dumped.
        :param unsafe: If unsafe yaml, yaml.dump is called, which allow customized object,
                       otherwise only the object with basic types could be dumped.
                       May set unsafe=True if use YamlFlowDict, YamlFlowList str for better readability.
        :param header: The content at the top of the yaml file, could be some comments about this yaml.
        :param kwargs: Other args, see https://yaml.readthedocs.io/en/latest/overview.html
        :return:
        """
        file = Path(file)
        file.parent.mkdir(parents=True, exist_ok=True)
        yaml = YAML(typ='unsafe' if unsafe else 'rt', with_additional_representer=True)
        with open(file, 'w', encoding='utf-8') as fout:
            if header:
                fout.write(header)
            yaml.dump(data, fout, **kwargs)

    @staticmethod
    def safe_load(stream):
        yaml = YAML(typ='safe')
        return yaml.load(stream)

    @staticmethod
    def safe_load_with_raw_enum_values(stream):
        yaml = YAML(typ='safe')
        # Add customer mapping constructor,
        # construct scalar when meet 'enum' key's value list.
        yaml.constructor.add_constructor('tag:yaml.org,2002:map', _enum_reserved_mapping_constructor)
        return yaml.load(stream)
