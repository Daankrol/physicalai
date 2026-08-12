# Copyright (C) 2026 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import threading
from typing import Any, cast

from loguru import logger

from physicalai.capture.discovery import DeviceInfo

__all__ = ["discover_realsense"]

# pyrealsense2 tears down its USB enumeration state once the last rs.context()
# instance is garbage collected, so a fresh context pays a ~2s cold-enumeration
# cost on the next query_devices() call. Caching one context for the process
# lifetime keeps discovery fast after the first call.
_context_lock = threading.Lock()
_cached_context: Any | None = None


def _get_context(rs_any: Any) -> Any:  # noqa: ANN401
    """Return a process-wide pyrealsense2 context, creating it on first use."""
    global _cached_context  # noqa: PLW0603
    with _context_lock:
        if _cached_context is None:
            _cached_context = rs_any.context()
        return _cached_context


def discover_realsense() -> list[DeviceInfo]:
    try:
        import pyrealsense2 as rs  # noqa: PLC0415
    except ImportError:
        return []

    rs_any = cast("Any", rs)  # cast to Any to avoid false positive "missing-attribute"
    ctx = _get_context(rs_any)

    try:
        devices = ctx.query_devices()
    except RuntimeError:
        # Recover from a stale/broken context by recreating it once.
        logger.exception("RealSense context query failed; recreating context")
        global _cached_context  # noqa: PLW0603
        with _context_lock:
            _cached_context = None
        ctx = _get_context(rs_any)
        devices = ctx.query_devices()

    results: list[DeviceInfo] = []

    for i, dev in enumerate(devices):
        try:
            serial = dev.get_info(rs_any.camera_info.serial_number)
            name = dev.get_info(rs_any.camera_info.name)
        except RuntimeError:
            continue

        results.append(
            DeviceInfo(
                device_id=serial,
                index=i,
                name=name,
                driver="realsense",
                hardware_id=serial,
                id_stable=True,
                manufacturer="RealSense",
                model=name,
            )
        )

    return results
