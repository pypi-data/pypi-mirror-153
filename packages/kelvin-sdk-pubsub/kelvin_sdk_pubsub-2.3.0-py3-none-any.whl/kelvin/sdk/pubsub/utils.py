"""Utility functions."""

from __future__ import annotations

import sys
from functools import reduce
from typing import Any, Mapping, TypeVar, Union, overload

if sys.version_info >= (3, 8):
    from typing import Literal
else:  # pragma: no cover
    from typing_extensions import Literal  # type: ignore

T = TypeVar("T")
S = TypeVar("S")


def deep_get(data: Mapping[str, Any], key: str, default: Any = None) -> Any:
    """Get deep key."""

    return reduce(lambda x, y: x.get(y, default), key.split("."), data)


@overload
def coalesce(x: Literal[None], y: S) -> S:
    ...


@overload
def coalesce(x: T, y: S) -> T:
    ...


def coalesce(x: T, y: S) -> Union[S, T]:
    """Coalesce values."""

    return x if x is not None else y
