# Copyright (C) 2025 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

# ruff: noqa: DOC201, DOC501

"""Configuration instantiation helpers."""

import dataclasses
import importlib
from pathlib import Path
from typing import TYPE_CHECKING

import yaml
from pydantic import BaseModel

if TYPE_CHECKING:
    from typing import Any


def _import_class(class_path: str) -> type:
    """Import a class from a module path."""
    try:
        module_path, class_name = class_path.rsplit(".", 1)
        module = importlib.import_module(module_path)  # nosemgrep
        return getattr(module, class_name)
    except (ValueError, ImportError, AttributeError) as e:
        msg = f"Cannot import '{class_path}': {e}"
        raise ImportError(msg) from e


def _instantiate_recursive(value: "Any") -> "Any":  # noqa: ANN401
    """Walk a value and instantiate nested ``{class_path, init_args}`` dicts."""
    if isinstance(value, dict):
        if "class_path" in value:
            return instantiate_obj_from_dict(value)
        return {k: _instantiate_recursive(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_instantiate_recursive(item) for item in value]
    if isinstance(value, tuple):
        return tuple(_instantiate_recursive(item) for item in value)
    return value


def instantiate_obj_from_dict(
    config: dict[str, "Any"],
    *,
    key: str | None = None,
    target_cls: type | None = None,
) -> object:
    """Instantiate an object from a configuration dictionary."""
    if key is not None:
        if key not in config:
            msg = f"Configuration must contain '{key}' key. Got keys: {list(config.keys())}"
            raise ValueError(msg)
        config = config[key]

    if "class_path" in config:
        cls = _import_class(config["class_path"])
        init_args = config.get("init_args", {})
    elif target_cls is not None:
        cls = target_cls
        init_args = config
    else:
        msg = (
            "Configuration must contain 'class_path' for instantiation, "
            f"or pass target_cls explicitly. Got keys: {list(config.keys())}"
        )
        raise ValueError(msg)

    if not isinstance(init_args, dict):
        return cls(init_args)

    instantiated_args = {k: _instantiate_recursive(v) for k, v in init_args.items()}

    if "args" in instantiated_args:
        args = instantiated_args.pop("args")
        return cls(*args, **instantiated_args)
    return cls(**instantiated_args)


def instantiate_obj_from_pydantic(
    config: BaseModel,
    *,
    key: str | None = None,
    target_cls: type | None = None,
) -> object:
    """Instantiate an object from a Pydantic model."""
    return instantiate_obj_from_dict(config.model_dump(), key=key, target_cls=target_cls)


def instantiate_obj_from_dataclass(
    config: object,
    *,
    key: str | None = None,
    target_cls: type | None = None,
) -> object:
    """Instantiate an object from a dataclass instance."""
    if not dataclasses.is_dataclass(config) or isinstance(config, type):
        msg = f"Expected dataclass instance, got {type(config)}"
        raise TypeError(msg)

    return instantiate_obj_from_dict(dataclasses.asdict(config), key=key, target_cls=target_cls)


def instantiate_obj_from_file(
    file_path: str | Path,
    *,
    key: str | None = None,
    target_cls: type | None = None,
) -> object:
    """Instantiate an object from a YAML/JSON configuration file."""
    with Path(file_path).open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return instantiate_obj_from_dict(config, key=key, target_cls=target_cls)


def instantiate_obj(
    config: dict[str, "Any"] | BaseModel | object | str | Path,
    *,
    key: str | None = None,
    target_cls: type | None = None,
) -> object:
    """Instantiate an object from dict, Pydantic, dataclass, or file config."""
    if isinstance(config, (str, Path)):
        return instantiate_obj_from_file(config, key=key, target_cls=target_cls)
    if isinstance(config, BaseModel):
        return instantiate_obj_from_pydantic(config, key=key, target_cls=target_cls)
    if dataclasses.is_dataclass(config) and not isinstance(config, type):
        return instantiate_obj_from_dataclass(config, key=key, target_cls=target_cls)
    if isinstance(config, dict):
        return instantiate_obj_from_dict(config, key=key, target_cls=target_cls)

    msg = f"Unsupported configuration type: {type(config)}. Expected dict, file path, Pydantic model, or dataclass."
    raise TypeError(msg)
