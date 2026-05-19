# Copyright (C) 2025-2026 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

"""Configuration primitives shared by runtime and training packages."""

from physicalai.config.base import Config
from physicalai.config.component import ComponentSpec
from physicalai.config.instantiate import instantiate_obj
from physicalai.config.mixin import FromConfig, from_config

__all__ = ["ComponentSpec", "Config", "FromConfig", "from_config", "instantiate_obj"]
