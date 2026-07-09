# Runtime System Design

This directory describes how PhysicalAI runs a robot control loop — policy
rollout, teleop, or any other action source — on a robot.

The short version:

```text
InferenceModel   computes actions
Execution        decides when/where inference runs
ActionQueue      buffers chunks and emits one action per tick
ActionSource     decides the action for this tick (PolicySource, TeleopSource, ...)
RobotRuntime     runs the robot loop
```

## Recommended Reading Order

1. [runtime_design.md](./runtime_design.md) — the design: API shape, ownership rules, and rationale
2. [policy_server_design.md](./policy_server_design.md), only for remote inference

## Main Example

```python
from physicalai.inference import InferenceModel
from physicalai.runtime import RobotRuntime, PolicySource, SyncExecution
from physicalai.robot.so101 import SO101

model = InferenceModel.load("./exports/act_policy")
robot = SO101(port="/dev/ttyACM0")

runtime = RobotRuntime(
    robot=robot,
    action_source=PolicySource(model=model, execution=SyncExecution(mode="chunk")),
    fps=30,
)

runtime.run(duration_s=60)
```

Same shape from the CLI:

```bash
physicalai run --config so101_act.yaml --duration-s 60
```

## Documents

| File                                                 | Use it for                                                 |
| ---------------------------------------------------- | ---------------------------------------------------------- |
| [runtime_design.md](./runtime_design.md)             | API shape, code examples, ownership rules                  |
| [policy_server_design.md](./policy_server_design.md) | Remote inference with `PolicyServer` and `RemoteExecution` |

## Key Decisions

1. Keep `InferenceModel` as the object that loads and runs the policy (see `docs/design/components/inferencekit.md` for `select_action()`/`predict_action_chunk()`/`ActionChunkCursor`).
2. `RobotRuntime` owns the robot control loop; the action source is a required constructor argument, not an optional subclass path.
3. `ActionSource` is a 3-method protocol (`connect`, `update`, `disconnect`) — `PolicySource` and `TeleopSource` are its two concrete implementations.
4. Keep runtime action buffering in `ActionQueue`, not inside `RobotRuntime`, `ActionSource`, or `InferenceModel`.
5. Keep benchmarking as an evaluation harness over tasks/gyms, not a second runtime.
6. Put `physicalai run` and `physicalai serve` in the runtime distribution, without Torch or Lightning.

## Related Docs

- Broader stack vision: [Robot Stack vision](`../../architecture/robot_stack_vision.md`)
- Top-level design index: [README](`../../README.md`)
