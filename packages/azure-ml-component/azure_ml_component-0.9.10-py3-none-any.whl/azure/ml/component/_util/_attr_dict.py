# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

from typing import TypeVar, Generic

from .._util._exceptions import UnexpectedKeywordError, UnexpectedAttributeError

K = TypeVar('K')
V = TypeVar('V')


class _AttrDict(Generic[K, V], dict):
    """This class is used for accessing values with instance.some_key."""

    def __getattr__(self, name: K) -> V:
        if name not in self:
            raise UnexpectedAttributeError(
                keyword=name, keywords=[key for key in self]
            )
        return super().__getitem__(name)

    def __setattr__(self, key, value):
        return super().__setitem__(key, value)

    def __getitem__(self, item: K) -> V:
        # We raise this exception instead of KeyError
        if item not in self:
            raise UnexpectedKeywordError(
                func_name='__getitem__', keyword=item, keywords=[key for key in self]
            )
        return super().__getitem__(item)

    # For Jupyter Notebook auto-completion
    def __dir__(self):
        return list(super().__dir__()) + list(self.keys())
