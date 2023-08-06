# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from azure.ml.component.run import Run as ComponentRun
from azure.ml.component._util._utils import deprecated


class Run(ComponentRun):
    def __init__(self, experiment=None, run_id=None, run: ComponentRun = None):
        if run is not None:
            super().__init__(run._experiment, run.id)
        else:
            super().__init__(experiment, run_id)

    @property
    @deprecated
    def output_ports(self):
        """DEPRECATED, use :meth:`outputs`."""
        return self._outputs

    @deprecated
    def get_port(self, name):
        """DEPRECATED, use :meth:`get_output`."""
        return self._get_output(name)

    @deprecated
    def find_step_run(self, name):
        """DEPRECATED, use :meth:`find_child_run`."""
        return self._find_child_run(name)

    @deprecated
    def get_step_run(self, _id):
        """
        Get a child run by id.

        :param _id: The id of the child run.
        :type _id: str

        :return: The Run object with the provided id.
        :rtype: azure.ml.component.Run
        """
        return self._get_child_run(_id)
