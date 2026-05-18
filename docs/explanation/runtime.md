# Runtime

`PolicyRuntime` runs a policy on robot hardware.

```python
runtime = PolicyRuntime.from_config("runtime.yaml")
runtime.run(duration_s=60)
```

## Responsibilities

| Component | Owns | Does not own |
| --- | --- | --- |
| `InferenceModel` | model load, preprocess, inference, postprocess | robot loop timing |
| `Execution` | where inference runs | robot IO |
| `ActionQueue` | action chunks and buffering | model inference |
| `PolicyRuntime` | observe, request inference, send action, callbacks, timing | policy math |
| `Robot` | hardware connection, observations, actions | policy inference |

## Loop

```python
while running:
    obs = robot.get_observation()
    obs.update(read_cameras(cameras))

    execution.maybe_request(obs)
    action = action_queue.pop_or_none()

    if action is None:
        action = hold_position()

    robot.send_action(action)
    sleep_until_next_tick()
```

## Execution Modes

| Mode | Where inference runs | Use |
| --- | --- | --- |
| `SyncExecution(mode="single_action")` | runtime thread | simple policies |
| `SyncExecution(mode="chunk")` | runtime thread | chunk policies without background worker |
| `AsyncExecution(transport="thread")` | worker thread | avoid blocking control loop |
| `AsyncExecution(transport="process")` | worker process | isolate model execution |
| `RemoteExecution` | remote server | robot host without policy weights |

## Product Workflows

HIL, recording, highlight, and DAgger compose through callbacks until they need reusable runtime primitives.

```python
class HILCallback:
    def before_send_action(self, action, step):
        if teleop.enabled:
            return teleop.read_action()
        return action
```
