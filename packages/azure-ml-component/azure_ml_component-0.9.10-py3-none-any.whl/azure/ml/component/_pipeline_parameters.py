# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

from enum import Enum
from pathlib import Path
from azureml.core import Dataset
from azureml.data.data_reference import DataReference
from azureml.data.datapath import DataPath
from azureml.data.abstract_dataset import AbstractDataset
from azureml.data.dataset_consumption_config import DatasetConsumptionConfig
from azureml.exceptions import UserErrorException

from ._dataset import _GlobalDataset, _FeedDataset
from azure.ml.component._pipeline_expression import OperableMixin


class LinkedParametersMixedIn(object):
    """Defines mapping between a pipeline parameter/input and it's assigned parameters.

    The linking is not defined in PipelineParameter class because some pipeline parameters are instance of Input.
    """
    def __init__(self):
        # TODO: move this to PipelineParameter when all pipeline parameters are instance of PipelineParameters
        super().__init__()
        # mapping from component_name to parameter this pipeline parameter assigned to
        # The key is module_name:parameter_name, value is type of StructuredInterfaceInput/StructuredInterfaceParameter
        # eg: {'component1:input1': StructuredInterfaceInput} or {'component1:param1': StructuredInterfaceParameter}
        self.linked_params = {}
        # mapping from component_name to parameter this pipeline parameter assigned to via parameter assign
        # eg: component_param = "{}".format(pipeline_param)
        self.linked_param_assignments = {}
        # The key is module_name:parameter_name, value is type of parameter owner's type
        # eg: {'component1:input1': PipelineComponent}
        self.linked_param_owner_type = {}
        # used to mark if a pipeline parameter is used in pipeline definition, eg:
        # sweep_component_func(
        #     subsample={
        #         "type": type,
        #         "min_value": min_value,
        #         "max_value": max_value
        #     })
        self.used_in_definition = False
        # used to mark if a pipeline parameter is used actually
        self.is_used_param = True
        # validation errors for this pipeline parameter
        self.errors = []

    @classmethod
    def repr_linked_params(cls, linked_params: dict) -> str:
        from azure.ml.component._util._utils import repr_parameter
        return str(["{}{}".format(k, repr_parameter(v)) for k, v in linked_params.items()])


class PipelineParameter(LinkedParametersMixedIn, OperableMixin):
    """Defines a parameter in a pipeline execution.

    Use PipelineParameters to construct versatile Pipelines which can be resubmitted later with varying
    parameter values. Note that we do not expose this as part of our public API yet. This is only intended for
    internal usage.

    :param name: The name of the pipeline parameter.
    :type name: str
    :param default_value: The default value of the pipeline parameter.
    :type default_value: literal values
    :param _auto_wrap_for_build: Indicate whether the pipeline parameter is wrapped for build definition.
    :type _auto_wrap_for_build: bool
    :param _groups: The group names of pipeline parameter.
        e.g. group list of group.sub_group1.sub_group2.param is [group, sub_group1, sub_group2]
    :type _groups: list[str]
    """
    ALLOWED_DATA_TYPES = (
        int, str, bool, float, Path,
        DataPath, Dataset, DatasetConsumptionConfig, AbstractDataset, _GlobalDataset, DataReference, _FeedDataset)

    def __init__(self, name, default_value, _auto_wrap_for_build=False, _groups=None):
        super(PipelineParameter, self).__init__()
        default_value = default_value.value if isinstance(default_value, Enum) else default_value

        self.name = name
        self.default_value = default_value
        self._auto_wrap_for_build = _auto_wrap_for_build
        self._groups = _groups if _groups else []

        from .component import Output
        if not isinstance(default_value, self.ALLOWED_DATA_TYPES) \
                and type(default_value) not in [list, dict] \
                and not isinstance(default_value, Output) \
                and default_value is not None:
            doc_site = 'https://aka.ms/azure-ml-component-pipeline-parameter'
            supported_types = "'int', 'str', 'bool', 'float', 'path' and 'Dataset'"
            raise UserErrorException(
                f'Default value is of unsupported type: %r, supported types are {supported_types},'
                f' refer to %s for more details.' % (
                    type(default_value).__name__, doc_site))

        # if a pipeline parameter is annotated, store it's annotation for validation
        self._annotation = None
        # user specified type annotation for this pipeline parameter
        self._user_annotation = None

    def __repr__(self):
        """
        __repr__ override.

        :return: The representation of the PipelineParameter.
        :rtype: str
        """
        return f'PipelineParameter(name={repr(self._full_name)}, default_value={repr(self.default_value)})'

    def __str__(self):
        """
        __str__ override.

        :return: The placeholder of the PipelineParameter.
        :rtype: str
        """
        return "@@{}@@".format(self._full_name)

    def _serialize_to_dict(self):
        if isinstance(self.default_value, DataPath):
            return {"type": "datapath",
                    "default": self.default_value._serialize_to_dict()}
        else:
            return {"type": self._type,
                    "default": self.default_value}

    @property
    def _full_name(self):
        return '_'.join([*self._groups, self.name])

    @property
    def _type(self):
        if isinstance(self.default_value, bool):
            return 'bool'
        if isinstance(self.default_value, int):
            return 'int'
        if isinstance(self.default_value, float):
            return 'float'
        return 'string'
