"""Helper utilities for deprecating other code."""

from __future__ import annotations

from functools import wraps
from typing import Any, Callable
from warnings import warn


def deprecated(func: Callable, wmsg: str) -> Callable:
    """
    Used to deprecate @func after renaming it or moving it to a
    different module/package.
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        warn(wmsg, category=MetamanDeprecationWarning, stacklevel=2)
        return func(*args, **kwargs)

    return wrapper


class MetamanDeprecationWarning(Warning):
    """DepreciationWarning that doesn't get ignored by default."""
