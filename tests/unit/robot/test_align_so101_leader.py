# Copyright (C) 2026 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

"""Exercise the standalone alignment check without opening serial ports."""

import runpy
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, call

import numpy as np
import pytest


@pytest.fixture
def example():
    script = Path(__file__).resolve().parents[3] / "examples/runtime/align_so101_leader.py"
    return runpy.run_path(str(script))["main"].__globals__


def test_alignment_accumulates_steps_smaller_than_an_encoder_tick(example, monkeypatch):
    clock = SimpleNamespace(now=0.0)

    def sleep(seconds):
        clock.now += seconds

    monkeypatch.setitem(example, "time", SimpleNamespace(monotonic=lambda: clock.now, sleep=sleep))
    robot = MagicMock()
    pose = np.ones(6, dtype=np.float32)
    commands = []
    timestamp = 0.0

    def observe():
        nonlocal timestamp
        timestamp += 1.0
        return SimpleNamespace(joint_positions=pose.copy(), timestamp=timestamp)

    def send(action, **kwargs):
        commands.append(action.copy())
        pose[:] = np.round(action, 1)

    robot.get_observation.side_effect = observe
    robot.send_action.side_effect = send

    example["align_leader"](robot, pose.copy(), np.zeros(6, dtype=np.float32), 0.0)

    assert np.max(np.abs(pose)) <= example["TOLERANCE"]
    assert np.max(np.abs(np.diff(np.stack(commands), axis=0))) <= example["SPEED"] / example["RATE_HZ"] + 1e-6


@pytest.mark.parametrize("shared", [False, True])
@pytest.mark.parametrize("failure", [TimeoutError, KeyboardInterrupt])
def test_failure_or_interrupt_attempts_torque_off(example, monkeypatch, tmp_path, shared, failure):
    leader = MagicMock()
    follower = MagicMock()
    leader.joint_names = follower.joint_names = [f"joint_{i}" for i in range(6)]
    monkeypatch.setitem(example, "SO101", MagicMock(side_effect=[leader, follower]))
    monkeypatch.setitem(example, "inspect", SimpleNamespace(getfile=lambda driver: "fake-driver"))
    transport = MagicMock()
    transport.from_config.side_effect = lambda driver, **kwargs: driver
    monkeypatch.setitem(example, "SharedRobot", transport)
    monkeypatch.setitem(
        example,
        "fresh_pose",
        MagicMock(
            side_effect=[
                (np.zeros(6, dtype=np.float32), 1.0),
                (np.ones(6, dtype=np.float32), 1.0),
                (np.ones(6, dtype=np.float32), 2.0),
            ]
        ),
    )
    monkeypatch.setitem(example, "align_leader", MagicMock(side_effect=failure))
    answers = iter(["CONNECT", "ALIGN"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(answers))
    calibration = tmp_path / "calibration.json"
    calibration.write_text("{}")
    monkeypatch.setattr(
        "sys.argv",
        [
            "align_so101_leader.py",
            "--leader-port",
            "unused-leader",
            "--leader-calibration",
            str(calibration),
            "--follower-port",
            "unused-follower",
            "--follower-calibration",
            str(calibration),
            *(["--shared"] if shared else []),
        ],
    )

    with pytest.raises(failure):
        example["main"]()

    assert leader.set_torque.call_args_list == [call(enabled=True), call(enabled=False)]
    follower.set_torque.assert_not_called()
    leader.disconnect.assert_called_once()
    follower.disconnect.assert_called_once()
    assert transport.from_config.call_count == (2 if shared else 0)


def test_large_starting_gap_is_rejected(example):
    with pytest.raises(ValueError, match="Align the arms more closely"):
        example["check_gap"](np.zeros(6), np.full(6, 10.0))
