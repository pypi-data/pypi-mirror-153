# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import copy
import uuid

from azureml.core import Workspace
from azureml.data.abstract_dataset import AbstractDataset

from ._utils import fetch_user_id_from_aad_token


class TelemetryMixin(object):

    def __init__(self):
        # Need to call init for potential parent, otherwise it won't be initialized.
        super().__init__()

    def _get_telemetry_values(self, *args, **kwargs):
        return {}


class RequestTelemetryMixin(TelemetryMixin):

    def __init__(self):
        super().__init__()
        self._request_id = None
        self._from_cli = False

    def _get_telemetry_values(self, *args, **kwargs):
        return {'request_id': self._request_id, 'from_cli': self._from_cli}

    def _set_from_cli_for_telemetry(self):
        self._from_cli = True

    def _refresh_request_id_for_telemetry(self):
        self._request_id = str(uuid.uuid4())


class WorkspaceTelemetryMixin(TelemetryMixin):
    _workspace_telemetry = {}

    def __init__(self, workspace: Workspace):
        super(WorkspaceTelemetryMixin, self).__init__()
        self._workspace_for_telemetry = workspace

    def _get_telemetry_values(self, *args, **kwargs):
        return self._get_telemetry_value_from_workspace(self._workspace_for_telemetry)

    def _set_workspace_for_telemetry(self, workspace: Workspace):
        self._workspace_for_telemetry = workspace

    @staticmethod
    def _get_telemetry_value_from_workspace(workspace: Workspace):
        """
        Get telemetry value out of a Workspace.

        The telemetry values include the following entries:

        * workspace_id
        * workspace_name
        * subscription_id
        * resource_group
        * location
        * tenant_id

        :param workspace: The workspace.
        :type workspace: azureml.core.Workspace

        :return: telemetry values.
        :rtype: dict
        """
        if workspace is None:
            # log mock workspace for CI tests.
            import os
            # TODO: we may need a place for all these constants
            if '_TEST_ENV' in os.environ:
                return {'subscription_id': 'mock_subscription_id'}
            return {}
        telemetry_values = {
            'workspace_id': workspace._workspace_id,
            'workspace_name': workspace._workspace_name,
            'subscription_id': workspace._subscription_id,
            'resource_group': workspace.resource_group,
            'location': workspace.location,
            'tenant_id': "",
            'user_oid': "",
            'is_service_principle': "",
            'telemetry_error': "",
        }

        workspace_id = workspace._workspace_id
        try:
            # Use cached tenant id because deep call stack depth may pop a window
            # request for auth and block the CI pipeline run.
            if workspace_id in WorkspaceTelemetryMixin._workspace_telemetry.keys():
                telemetry_values = WorkspaceTelemetryMixin._workspace_telemetry[workspace_id]
            else:
                from azureml._base_sdk_common.common import fetch_tenantid_from_aad_token
                arm_token = workspace._auth_object._get_arm_token()
                tenant_id = fetch_tenantid_from_aad_token(arm_token)
                # We track user object id as core UI does here: https://msdata.visualstudio.com/Vienna/_git/
                # workspace-portal?path=%2Fcommon%2Fexperimentation-worker%2Fsrc%2Fworkers%2Frequest%2F
                # getTelemetryProperties.ts&version=GBmaster
                user_oid, is_service_principle = fetch_user_id_from_aad_token(arm_token)
                telemetry_values.update({
                    'tenant_id': tenant_id,
                    'user_oid': user_oid,
                    'is_service_principle': is_service_principle
                })
                WorkspaceTelemetryMixin._workspace_telemetry[workspace_id] = telemetry_values
        except Exception as e:
            telemetry_values['telemetry_error'] = "Error retrieving workspace telemetry: {}".format(e)

        # Here we return a copy of workspace telemetry to prevent cached workspace telemetry dict got modified outside
        # of this function
        return copy.deepcopy(telemetry_values)


def _get_telemetry_value_from_pipeline_parameter(pipeline_parameters):
    telemetry_values = {}
    pipeline_parameters_count = 0
    data_pipeline_parameters_count = 0
    literal_pipeline_parameters_count = 0
    parameter_group_count = 0

    if pipeline_parameters is not None:
        pipeline_parameters_count = len(pipeline_parameters)
        data_pipeline_parameters_count = len([x for x in pipeline_parameters.values() if
                                              isinstance(x, AbstractDataset)])
        literal_pipeline_parameters_count = pipeline_parameters_count - data_pipeline_parameters_count
        from azure.ml.component._core._types import _GroupAttrDict
        parameter_group_count = len([param for param in pipeline_parameters.values()
                                     if isinstance(param, _GroupAttrDict)])

    telemetry_values['pipeline_parameters_count'] = pipeline_parameters_count
    telemetry_values['data_pipeline_parameters_count'] = data_pipeline_parameters_count
    telemetry_values['literal_pipeline_parameters_count'] = literal_pipeline_parameters_count
    telemetry_values['parameter_group_count'] = parameter_group_count
    return telemetry_values
