#!/usr/bin/env python3
# Copyright (C) 2026 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

"""Align an SO101 leader to a held follower without Studio or a policy."""

from __future__ import annotations

import argparse
import inspect
import os
import sys
import time
from pathlib import Path

import numpy as np
from physicalai.robot import SO101, SharedRobot

RATE_HZ = 30.0
SPEED = 1.0  # Normalized units per second.
TOLERANCE = 0.25
MAX_START_GAP = 5.0
TIMEOUT_S = 15.0
STATE_TIMEOUT_S = 2.0


def fresh_pose(robot: SO101 | SharedRobot, after: float = float("-inf")) -> tuple[np.ndarray, float]:
    """Read a finite, fresh six-joint pose or fail within two seconds."""
    deadline = time.monotonic() + STATE_TIMEOUT_S
    while time.monotonic() < deadline:
        observation = robot.get_observation()
        pose = np.asarray(observation.joint_positions, dtype=np.float32)
        timestamp = float(observation.timestamp)
        if pose.shape != (SO101.NUM_JOINTS,) or not np.all(np.isfinite(pose)) or not np.isfinite(timestamp):
            raise ValueError("Robot returned an invalid joint pose or timestamp")
        if timestamp > after:
            return pose.copy(), timestamp
        time.sleep(0.01)
    raise TimeoutError("Robot observations stopped advancing")


def check_gap(start: np.ndarray, target: np.ndarray) -> float:
    """Reject a large movement before enabling torque or sending a target."""
    gap = float(np.max(np.abs(target - start)))
    if gap > MAX_START_GAP:
        raise ValueError(
            f"Starting gap {gap:.2f} exceeds {MAX_START_GAP:.2f} normalized units. "
            "Align the arms more closely by hand and rerun."
        )
    return gap


def align_leader(leader: SO101 | SharedRobot, start: np.ndarray, target: np.ndarray, timestamp: float) -> None:
    """Ramp bounded targets and require the measured leader pose to arrive."""
    commanded = start.copy()
    deadline = time.monotonic() + TIMEOUT_S
    next_report = 0.0
    while time.monotonic() < deadline:
        actual, timestamp = fresh_pose(leader, timestamp)
        error = float(np.max(np.abs(target - actual)))
        if time.monotonic() >= next_report:
            print(f"Command: {commanded.round(3).tolist()}", flush=True)
            print(f"Leader:  {actual.round(3).tolist()}  max error: {error:.3f}", flush=True)
            next_report = time.monotonic() + 1.0
        if error <= TOLERANCE:
            print("PASS: measured leader pose reached the follower target")
            return
        # Advance the command, not the encoder reading: sub-tick steps must accumulate.
        commanded = commanded + np.clip(target - commanded, -SPEED / RATE_HZ, SPEED / RATE_HZ)
        leader.send_action(commanded, goal_time=1.0 / RATE_HZ)
        time.sleep(1.0 / RATE_HZ)
    raise TimeoutError("Leader did not reach the follower target; see the measured errors above")


def main() -> None:
    """Run an operator-confirmed hardware check using each arm's own calibration."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--leader-port", required=True)
    parser.add_argument("--leader-calibration", required=True, type=Path)
    parser.add_argument("--follower-port", required=True)
    parser.add_argument("--follower-calibration", required=True, type=Path)
    parser.add_argument(
        "--shared",
        action="store_true",
        help="Use SharedRobot instead of direct serial control",
    )
    args = parser.parse_args()
    if Path(args.leader_port).resolve() == Path(args.follower_port).resolve():
        parser.error("Leader and follower must use different serial ports")
    for calibration in (args.leader_calibration, args.follower_calibration):
        if not calibration.expanduser().is_file():
            parser.error(f"Calibration file not found: {calibration}")

    leader: SO101 | SharedRobot = SO101(
        port=args.leader_port,
        calibration=args.leader_calibration.expanduser(),
        role="leader",
        unit="normalized",
    )
    follower: SO101 | SharedRobot = SO101(
        port=args.follower_port,
        calibration=args.follower_calibration.expanduser(),
        role="follower",
        unit="normalized",
    )
    if args.shared:
        leader = SharedRobot.from_config(leader, name=f"align-leader-{os.getpid()}", idle_timeout=2.0)
        follower = SharedRobot.from_config(follower, name=f"align-follower-{os.getpid()}", idle_timeout=2.0)
    print("Driver:", inspect.getfile(SO101))
    print("Transport:", "SharedRobot" if args.shared else "direct serial")
    print("Stop Studio and other controllers. Clear the workspace and keep the emergency stop reachable.")
    print("Connecting enables follower torque and disables leader torque. Support both arms safely.")
    print("Leader torque-off will be attempted on completion or failure. The follower remains held.")
    if input("Type CONNECT to continue: ") != "CONNECT":
        raise SystemExit("Cancelled before connecting")

    torque_requested = False
    cleanup_errors: list[str] = []
    try:
        follower.connect()
        target, _ = fresh_pose(follower)
        follower.send_action(target)
        leader.connect()
        if leader.joint_names != follower.joint_names:
            raise ValueError("Leader and follower joint names differ")
        start, timestamp = fresh_pose(leader)
        print("Joints:", leader.joint_names)
        print("Follower target:", target.round(3).tolist())
        print("Leader start:   ", start.round(3).tolist())
        gap = check_gap(start, target)
        if gap <= TOLERANCE:
            print("Already aligned; no leader torque requested. Start slightly offset to test movement.")
            return
        print(f"Maximum gap: {gap:.3f}; speed: {SPEED:.1f} units/s; deadline: {TIMEOUT_S:.0f}s")
        if input("Check the path is clear and the leader is supported for torque-off. Type ALIGN to move: ") != "ALIGN":
            raise SystemExit("Cancelled before enabling leader torque")

        # The reply can be lost even when the hardware enabled torque.
        torque_requested = True
        leader.set_torque(enabled=True)
        print("Leader torque ON acknowledged", flush=True)
        start, timestamp = fresh_pose(leader, timestamp)
        check_gap(start, target)
        align_leader(leader, start, target, timestamp)
    finally:
        if torque_requested:
            try:
                leader.set_torque(enabled=False)
                print("Leader torque OFF acknowledged", flush=True)
            except Exception as exc:
                cleanup_errors.append(f"Leader torque state is uncertain: {exc}")
        for robot in (leader, follower):
            if robot.is_connected():
                try:
                    robot.disconnect()
                except Exception as exc:
                    cleanup_errors.append(f"Robot disconnect failed: {exc}")
        if cleanup_errors:
            for error in cleanup_errors:
                print(f"STOP: {error}", file=sys.stderr, flush=True)
            raise RuntimeError("Inspect the arms and owners before continuing")


if __name__ == "__main__":
    main()
