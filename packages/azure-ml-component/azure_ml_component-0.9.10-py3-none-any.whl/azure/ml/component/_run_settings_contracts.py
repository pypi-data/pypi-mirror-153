# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Support more contracts in runsettings. Currently, we support [BanditPolicy, MedianStoppingPolicy,
TruncationSelectionPolicy, NoTerminationPolicy] from azureml.train.hyperdrive for sweep.early_termination,
[Environment, Docker, Conda] for environment override."""

from ._util._yaml_utils import YAML
from .environment import Environment, Docker, Conda

yaml = YAML(with_additional_representer=True)


# region: parameter converters
def _docker_converter(obj: Docker):
    if obj._docker:
        return yaml.dump(obj._docker._to_dict_in_vnext_format())
    return None


def _conda_converter(obj: Conda):
    if obj._conda:
        return yaml.dump(obj._conda._to_dict())
    return None
# endregion


# region: section converters
def _bandit_policy_converter(obj):
    result = {
        'policy_type': 'bandit',
        'evaluation_interval': obj._evaluation_interval,
        'delay_evaluation': obj._delay_evaluation
    }
    if obj._slack_factor:
        result['slack_factor'] = obj._slack_factor
    else:
        result['slack_amount'] = obj._properties.get('slack_amount')
    return result


def _median_stopping_policy_converter(obj):
    return {
        'policy_type': 'median_stopping',
        'evaluation_interval': obj._evaluation_interval,
        'delay_evaluation': obj._delay_evaluation
    }


def _truncation_selection_policy_converter(obj):
    return {
        'policy_type': 'truncation_selection',
        'truncation_percentage': obj._truncation_percentage,
        'evaluation_interval': obj._evaluation_interval,
        'delay_evaluation': obj._delay_evaluation
    }


def _no_termination_policy_converter(obj):
    return {
        'policy_type': 'default'
    }


def _environment_converter(obj: Environment):
    return {
        "docker": obj._get_docker(),
        "conda": obj._get_conda(),
        "os": obj._get_os()
    }
# endregion


# For new classes support, we just add more converters here
def _get_converters_by_section_name(section_name):
    if section_name == 'early_termination':
        # This part is used for supporting sweep_component.runsettings.sweep.early_termination = Policy
        try:
            from azureml.train.hyperdrive import BanditPolicy, MedianStoppingPolicy, TruncationSelectionPolicy, \
                NoTerminationPolicy
            return {
                BanditPolicy: _bandit_policy_converter,
                MedianStoppingPolicy: _median_stopping_policy_converter,
                TruncationSelectionPolicy: _truncation_selection_policy_converter,
                NoTerminationPolicy: _no_termination_policy_converter,
            }
        except Exception:
            return {}
    elif section_name == "environment":
        return {
            Environment: _environment_converter
        }
    return {}


def try_convert_obj_to_dict(section_name, obj):
    """Return dict if obj is dict or there is a dict-converter for obj, otherwise return None."""
    obj_type = type(obj)
    if obj_type == dict:
        return obj
    converters = _get_converters_by_section_name(section_name)
    if obj_type in converters:
        converter = converters[obj_type]
        # In case the converter throws exception
        try:
            return converter(obj)
        except Exception as e:
            raise Exception("Failed to set '{}' from type '{}'.".format(section_name, obj_type)) from e
    return None


_parameter_converters = {
    'environment.docker': {
        Docker: _docker_converter
    },
    'environment.conda': {
        Conda: _conda_converter
    }
}


def try_convert_obj_to_value(parameter_id, obj, expected_type):
    obj_type = type(obj)
    if obj_type == expected_type:
        return obj
    # Look up for a converter
    if parameter_id in _parameter_converters:
        if obj_type in _parameter_converters[parameter_id]:
            converter = _parameter_converters[parameter_id][obj_type]
            try:
                return converter(obj)
            except Exception as e:
                raise Exception("Failed to set '{}' from type '{}'.".format(parameter_id, obj_type)) from e
    # Otherwise, return obj directly
    return obj
