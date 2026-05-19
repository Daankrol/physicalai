# Copyright (C) 2025 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

# ruff: noqa: DOC201, DOC501

"""Serialization utilities for dataclasses."""

from __future__ import annotations

import dataclasses
import operator
import types
from enum import Enum
from functools import reduce
from itertools import starmap
from typing import TYPE_CHECKING, Union, get_args, get_origin, get_type_hints

if TYPE_CHECKING:
    from collections.abc import Mapping

_MIN_DICT_TYPE_ARGS = 2
_VAR_TUPLE_ARG_COUNT = 2

__all__ = ["dataclass_to_dict", "dict_to_dataclass"]


def dataclass_to_dict(obj: object, *, recursive: bool = True) -> object:  # noqa: PLR0911
    """Convert a dataclass or nested structure to plain Python data."""
    if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
        if not recursive:
            return {field.name: getattr(obj, field.name) for field in dataclasses.fields(obj)}
        return {field.name: dataclass_to_dict(getattr(obj, field.name)) for field in dataclasses.fields(obj)}

    if not recursive:
        return obj

    if isinstance(obj, dict):
        return {(k.value if isinstance(k, Enum) else k): dataclass_to_dict(v) for k, v in obj.items()}

    if isinstance(obj, (list, tuple)):
        return [dataclass_to_dict(item) for item in obj]

    if isinstance(obj, Enum):
        return obj.value

    if hasattr(obj, "tolist") and hasattr(obj, "ndim"):
        return obj.tolist()  # type: ignore[union-attr]

    return obj


def dict_to_dataclass[T](cls: type[T], data: Mapping[str, object]) -> T:
    """Reconstruct a dataclass from a dict using type hints."""
    if not dataclasses.is_dataclass(cls):
        msg = f"Expected dataclass, got {cls}"
        raise TypeError(msg)

    try:
        hints = get_type_hints(cls)
    except Exception:  # noqa: BLE001
        hints = {}

    kwargs = {}
    for field in dataclasses.fields(cls):
        if field.name not in data:
            continue
        value = data[field.name]
        field_type = hints.get(field.name, field.type)
        kwargs[field.name] = _reconstruct_value(value, field_type)

    return cls(**kwargs)  # type: ignore[return-value]


def _reconstruct_value(value: object, field_type: object) -> object:  # noqa: PLR0911
    """Reconstruct a value based on its expected type."""
    if value is None:
        return None

    origin = get_origin(field_type)
    args = get_args(field_type)

    if origin is type(None):
        return None

    if _is_optional_type(field_type):
        return _reconstruct_value(value, _get_optional_inner_type(field_type))

    if origin is dict and isinstance(value, dict):
        if len(args) >= _MIN_DICT_TYPE_ARGS:
            return {k: _reconstruct_value(v, args[1]) for k, v in value.items()}
        return value

    if origin is list and isinstance(value, list):
        if args:
            return [_reconstruct_value(item, args[0]) for item in value]
        return value

    if origin is tuple and isinstance(value, list):
        if args:
            if len(args) == _VAR_TUPLE_ARG_COUNT and args[1] is ...:
                return tuple(_reconstruct_value(item, args[0]) for item in value)
            return tuple(starmap(_reconstruct_value, zip(value, args, strict=False)))
        return tuple(value)

    actual_type = origin or field_type
    if isinstance(actual_type, type) and dataclasses.is_dataclass(actual_type) and isinstance(value, dict):
        return dict_to_dataclass(actual_type, value)

    if isinstance(actual_type, type) and issubclass(actual_type, Enum) and not isinstance(value, Enum):
        return actual_type(value)

    return value


def _is_optional_type(field_type: object) -> bool:
    """Check if a type is Optional[X]."""
    origin = get_origin(field_type)
    if origin is None:
        return False
    if origin is types.UnionType:
        return type(None) in get_args(field_type)
    if origin is Union:
        return type(None) in get_args(field_type)
    return False


def _get_optional_inner_type(field_type: object) -> object:
    """Get the non-None inner type from Optional[X]."""
    non_none_args = [arg for arg in get_args(field_type) if arg is not type(None)]
    if len(non_none_args) == 1:
        return non_none_args[0]
    return reduce(operator.or_, non_none_args)
