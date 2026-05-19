# Copyright (C) 2025 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

# ruff: noqa: DOC201, DOC501

"""Configuration mixins for adding from_config functionality."""

import dataclasses
from pathlib import Path
from typing import Any, Self, cast

import yaml
from pydantic import BaseModel

from physicalai.config.instantiate import instantiate_obj_from_dict
from physicalai.config.serializable import dataclass_to_dict


class FromConfig:
    """Mixin that adds configuration-based construction helpers."""

    @classmethod
    def from_yaml(cls, file_path: str | Path, *, key: str | None = None) -> Self:
        """Load configuration from a YAML file and instantiate the class."""
        with Path(file_path).open("r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        return cls.from_dict(config, key=key)

    @classmethod
    def from_dict(cls, config: dict[str, Any], *, key: str | None = None) -> Self:
        """Instantiate the class from a configuration dictionary."""
        return cast("Self", instantiate_obj_from_dict(config, key=key, target_cls=cls))

    @classmethod
    def from_pydantic(
        cls,
        config: BaseModel,
        *,
        key: str | None = None,
        recursive: bool = False,
    ) -> Self:
        """Instantiate the class from a Pydantic model."""
        if recursive:
            config_dict = config.model_dump()
        else:
            config_dict = {name: getattr(config, name) for name in config.__class__.model_fields}
        return cls.from_dict(config_dict, key=key)

    @classmethod
    def from_dataclass(
        cls,
        config: object,
        *,
        key: str | None = None,
        recursive: bool = False,
    ) -> Self:
        """Instantiate the class from a dataclass instance."""
        if not dataclasses.is_dataclass(config) or isinstance(config, type):
            msg = f"Expected dataclass instance, got {type(config)}"
            raise TypeError(msg)

        config_dict = cast("dict[str, Any]", dataclass_to_dict(config, recursive=recursive))
        return cls.from_dict(config_dict, key=key)

    @classmethod
    def from_config(
        cls,
        config: dict[str, Any] | BaseModel | object | str | Path,
        *,
        key: str | None = None,
        recursive: bool = False,
    ) -> Self:
        """Generic entry point that dispatches on the type of ``config``."""
        if isinstance(config, (str, Path)):
            return cls.from_yaml(config, key=key)
        if isinstance(config, BaseModel):
            return cls.from_pydantic(config, key=key, recursive=recursive)
        if dataclasses.is_dataclass(config) and not isinstance(config, type):
            return cls.from_dataclass(config, key=key, recursive=recursive)
        if isinstance(config, dict):
            return cls.from_dict(config, key=key)

        msg = f"Unsupported configuration type: {type(config)}. Expected dict, file path, Pydantic model, or dataclass."
        raise TypeError(msg)


def from_config[T: type](cls: T) -> T:
    """Decorate a class with the same config constructors as ``FromConfig``."""
    for name in ("from_yaml", "from_dict", "from_pydantic", "from_dataclass", "from_config"):
        setattr(cls, name, FromConfig.__dict__[name])
    return cls
