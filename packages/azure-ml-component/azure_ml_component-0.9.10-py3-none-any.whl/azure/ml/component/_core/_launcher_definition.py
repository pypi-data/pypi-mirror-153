# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from enum import Enum


class LauncherType(Enum):
    """Represents all types of components."""

    UNKNOWN = 'unknown'
    MPI = 'mpi'
    TORCH_DISTRIBUTED = 'torch.distributed'
    TORCH_DISTRIBUTED_V2 = 'Pytorch'

    @classmethod
    def get_launcher_type_by_str(cls, type_str):
        if type_str is None:
            return cls.UNKNOWN

        for t in cls:
            if type_str.lower() == t.value.lower():
                return t

        return cls.MPI

    def get_definition_class(self):
        mapping = {
            self.MPI: MPILauncherDefinition,
            self.TORCH_DISTRIBUTED: TorchDistributedLauncherDefinition,
            self.TORCH_DISTRIBUTED_V2: TorchDistributedLauncherDefinition,
        }
        # For unknown types, we treat it as MPI launcher
        return mapping.get(self, LauncherDefinition)


class LauncherDefinition:
    """Represents a definition of launcher for DistributedComponent."""
    TYPE = LauncherType.UNKNOWN

    def __init__(self, additional_arguments):
        self._type = self.TYPE
        self._args = additional_arguments

    @property
    def type(self):
        return self.TYPE

    @property
    def additional_arguments(self):
        return self._args

    def _to_dict(self) -> dict:
        return {
            'type': self.type.value,
            'additional_arguments': self.additional_arguments,
        }

    @staticmethod
    def _from_dict(dct):
        launcher_type = dct.get('type', None)
        cls = LauncherType.get_launcher_type_by_str(launcher_type).get_definition_class()
        return cls(**{k: v for k, v in dct.items() if k != 'type'})


class MPILauncherDefinition(LauncherDefinition):
    """Represents a definition of MPI launcher."""

    TYPE = LauncherType.MPI


class TorchDistributedLauncherDefinition(LauncherDefinition):
    """Represents a definition of torch.distributed launcher"""

    TYPE = LauncherType.TORCH_DISTRIBUTED
