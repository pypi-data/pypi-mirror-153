# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

from abc import ABC, abstractmethod
from ._util._loggerfactory import _LoggerFactory, _PUBLIC_API, track
from ._util._telemetry import WorkspaceTelemetryMixin
from ._util._utils import _is_prod_workspace, _can_visualize, _is_in_notebook
from ._aml_core_dependencies import experimental


_logger = None


def _get_logger():
    global _logger
    if _logger is not None:
        return _logger
    _logger = _LoggerFactory.get_logger()
    return _logger


def _is_visible(object):
    return isinstance(object, Visible)


class Visible(ABC):
    @property
    @abstractmethod
    def workspace(self):
        """
        The subclass of Visible must have workspace
        """

    @track(_get_logger, activity_type=_PUBLIC_API, activity_name="Visible_build_visualization_dict")
    @abstractmethod
    def _build_visualization_dict(self, name=None):
        """
        Build visualization dict that could be rendered in notebook.
        """

    @experimental
    @track(_get_logger, activity_type=_PUBLIC_API)
    def diff(self, to_compare: 'Visible'):
        """
        Visualize the difference of two pipelines. The result shows two graphs either inline or side-by-side.

        :param to_compare: The pipeline to compare
        :type to_compare: Visible
        """
        if _is_visible(to_compare):
            workspace = self.workspace
            if self._can_visualize():
                is_prod = _is_prod_workspace(workspace)
                envinfo = WorkspaceTelemetryMixin._get_telemetry_value_from_workspace(workspace)

                left_yaml = to_compare._build_visualization_dict()
                right_yaml = self._build_visualization_dict()
                from ._widgets._visualize import _visualize_diff
                _visualize_diff(graphyaml=left_yaml, graphyaml_to_compare=right_yaml, envinfo=envinfo, is_prod=is_prod)
            else:
                from ._widgets import VISUALIZATION_NOT_SUPPORTED_MESSAGE
                print(VISUALIZATION_NOT_SUPPORTED_MESSAGE)
        else:
            raise Exception('Could not compare. The object to compare must be a subclass of Visible.')

    def _can_visualize(self):
        return _can_visualize()

    def _visualize_not_support_warning(self, only_show_in_notebook=True):
        """
        Show the visualization not supported warning message.

        :param only_show_in_notebook: only show the warning message in notebook environment.
        :type only_show_in_notebook: bool
        """
        from ._widgets import VISUALIZATION_NOT_SUPPORTED_MESSAGE
        if not only_show_in_notebook or _is_in_notebook():
            print(VISUALIZATION_NOT_SUPPORTED_MESSAGE)
