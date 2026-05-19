# Copyright (C) 2026 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

# ruff: noqa: DOC201, DOC501

"""Generic component specifications for dynamic instantiation."""

from __future__ import annotations

import inspect
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator

# Alias builtin ``type`` so it remains accessible inside classes that define a
# Pydantic field with the same name (e.g. ``ComponentSpec.type``).
_type = type


class ComponentSpec(BaseModel):
    """Dual-resolution component descriptor for dynamic instantiation.

    Supports two resolution modes:

    1. **type + flat params** (LeRobot-compatible)::

        {"type": "single_pass"}

    2. **class_path + init_args** (full-power PhysicalAI)::

        {"class_path": "physicalai.inference.runners.SinglePass",
         "init_args": {}}

    When ``class_path`` is present it takes precedence. When only ``type`` is
    present, a component registry can resolve it.

    Attributes:
        type: Registered short name (e.g. ``"single_pass"``).
        class_path: Fully-qualified class path for direct import.
        init_args: Keyword arguments forwarded to the constructor
            (used with ``class_path`` mode).
    """

    model_config = ConfigDict(frozen=True, extra="allow")
    type: str = ""
    class_path: str = ""
    init_args: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def _must_have_type_or_class_path(self) -> ComponentSpec:
        if not self.type and not self.class_path:
            msg = "ComponentSpec requires either 'type' or 'class_path'"
            raise ValueError(msg)
        return self

    @property
    def flat_params(self) -> dict[str, Any]:
        """Return extra fields as flat params for type-based resolution."""
        return dict(self.model_extra) if self.model_extra else {}

    @classmethod
    def from_class(cls, target: _type, **overrides: Any) -> ComponentSpec:  # noqa: ANN401
        """Build a spec by introspecting a class constructor.

        Parameters not present in *overrides* use their default values. Required
        parameters without defaults must be provided in *overrides* or a
        TypeError is raised.
        """
        sig = inspect.signature(target)
        init_args: dict[str, Any] = {}
        missing: list[str] = []

        for name, param in sig.parameters.items():
            if name == "self":
                continue
            if name in overrides:
                value = overrides[name]
            elif param.default is not param.empty:
                value = param.default
            else:
                missing.append(name)
                continue

            if isinstance(value, ComponentSpec):
                value = value.model_dump()
            init_args[name] = value

        if missing:
            msg = (
                f"Missing required parameters for {target.__qualname__}: "
                f"{', '.join(missing)}. Pass them as keyword arguments."
            )
            raise TypeError(msg)

        return cls(
            class_path=f"{target.__module__}.{target.__qualname__}",
            init_args=init_args,
        )


__all__ = ["ComponentSpec"]
