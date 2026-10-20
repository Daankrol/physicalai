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


@pytest.mark.parametrize("start", [1.0, 40.0])
@pytest.mark.parametrize("observation_delay", [0.0, 0.1])
def test_alignment_sends_one_timed_target_and_waits_for_measurements(example, monkeypatch, start, observation_delay):
    clock = SimpleNamespace(now=0.0)

    def sleep(seconds):
        clock.now += seconds

    monkeypatch.setitem(example, "time", SimpleNamespace(monotonic=lambda: clock.now, sleep=sleep))
    robot = MagicMock()
    pose = np.full(6, start, dtype=np.float32)
    target = np.zeros(6, dtype=np.float32)
    timestamp = 0.0

    def observe():
        nonlocal timestamp
        timestamp += 1.0
        sleep(observation_delay)
        pose[:] = np.round(start * (1.0 - min(clock.now / 3.0, 1.0)), 1)
        return SimpleNamespace(joint_positions=pose.copy(), timestamp=timestamp)

    robot.get_observation.side_effect = observe

    example["align_leader"](robot, target, 0.0, goal_time=3.0)

    robot.send_action.assert_called_once()
    np.testing.assert_array_equal(robot.send_action.call_args.args[0], target)
    assert robot.send_action.call_args.kwargs == {"goal_time": 3.0}
    assert np.max(np.abs(pose)) <= example["TOLERANCE"]
    assert robot.get_observation.call_count > 1


def test_motion_timeout_does_not_resend_the_target(example, monkeypatch):
    clock = SimpleNamespace(now=0.0)

    def sleep(seconds):
        clock.now += seconds

    monkeypatch.setitem(example, "time", SimpleNamespace(monotonic=lambda: clock.now, sleep=sleep))
    robot = MagicMock()
    robot.get_observation.side_effect = lambda: SimpleNamespace(joint_positions=np.ones(6), timestamp=clock.now + 1.0)

    with pytest.raises(TimeoutError, match="did not reach"):
        example["align_leader"](robot, np.zeros(6, dtype=np.float32), 0.0, goal_time=3.0)

    robot.send_action.assert_called_once()


@pytest.mark.parametrize("goal_time", ["0", "-1", "nan", "inf"])
def test_invalid_duration_is_rejected_before_connecting(example, monkeypatch, goal_time):
    driver = MagicMock()
    monkeypatch.setitem(example, "SO101", driver)
    monkeypatch.setattr(
        "sys.argv",
        [
            "align_so101_leader.py",
            "--leader-port",
            "unused-leader",
            "--leader-calibration",
            "unused-leader.json",
            "--follower-port",
            "unused-follower",
            "--follower-calibration",
            "unused-follower.json",
            "--goal-time",
            goal_time,
        ],
    )

    with pytest.raises(SystemExit) as exc_info:
        example["main"]()

    assert exc_info.value.code == 2
    driver.assert_not_called()


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
