# Copyright (C) 2025 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

# ruff: noqa: DOC201, DOC501

"""Base configuration class for typed constructor configs."""

import dataclasses
from collections.abc import Mapping
from pathlib import Path
from typing import Any, Literal, Self

from physicalai.config.serializable import dataclass_to_dict, dict_to_dataclass

__all__ = ["Config"]


class Config:
    """Base class for dataclass-backed configuration objects."""

    def to_dict(self) -> dict[str, Any]:
        """Convert this config to a plain dict for serialization."""
        if not dataclasses.is_dataclass(self):
            msg = f"{self.__class__.__name__} must be a dataclass to use Config"
            raise TypeError(msg)

        result = dataclass_to_dict(self)
        if not isinstance(result, dict):
            msg = f"Expected dict from dataclass_to_dict, got {type(result)}"
            raise TypeError(msg)
        return result

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Self:
        """Reconstruct this config from a dict."""
        if not dataclasses.is_dataclass(cls):
            msg = f"{cls.__name__} must be a dataclass to use Config"
            raise TypeError(msg)
        return dict_to_dataclass(cls, data)

    def to_jsonargparse(self) -> dict[str, Any]:
        """Convert config to ``class_path``/``init_args`` format."""
        return {
            "class_path": f"{self.__class__.__module__}.{self.__class__.__qualname__}",
            "init_args": self.to_dict(),
        }

    def save(
        self,
        path: str | Path,
        *,
        format: Literal["jsonargparse", "dict"] = "jsonargparse",  # noqa: A002
    ) -> None:
        """Save config to a YAML file."""
        path = Path(path)
        data = self.to_dict() if format == "dict" else self.to_jsonargparse()

        if path.suffix not in {".yaml", ".yml"}:
            msg = f"Unsupported file extension: {path.suffix}. Use .yaml or .yml"
            raise ValueError(msg)

        import yaml  # noqa: PLC0415

        with path.open("w") as f:
            yaml.safe_dump(data, f, default_flow_style=False, sort_keys=False)

    @classmethod
    def load(cls, path: str | Path) -> Self:
        """Load config from a YAML file."""
        path = Path(path)

        if path.suffix not in {".yaml", ".yml"}:
            msg = f"Unsupported file extension: {path.suffix}. Use .yaml or .yml"
            raise ValueError(msg)

        import yaml  # noqa: PLC0415

        with path.open() as f:
            data = yaml.safe_load(f)

        if "init_args" in data:
            data = data["init_args"]

        return cls.from_dict(data)
