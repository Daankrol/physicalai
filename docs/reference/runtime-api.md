# Runtime API Reference

## `PolicyRuntime`

```python
PolicyRuntime(
    robot: Robot,
    model: InferenceModel,
    execution: Execution,
    fps: float,
    cameras: Mapping[str, Camera] | None = None,
    action_queue: ActionQueue | None = None,
    callbacks: Sequence[Callback] = (),
    return_to_home: bool = False,
)
```

Methods:

```python
runtime.run(duration_s: float | None = None) -> None
runtime.stop() -> None
runtime.close() -> None
```

Construct from config:

```python
runtime = PolicyRuntime.from_config("runtime.yaml")
```

## `Execution`

```python
class Execution:
    def start(self, action_queue: ActionQueue, model: InferenceModel) -> None: ...
    def maybe_request(self, observation: Mapping[str, Any]) -> None: ...
    def warmup(self, sample_observation: Mapping[str, Any], n: int = 2) -> None: ...
    def stop(self) -> None: ...
```

Implementations:

| Class | Purpose |
| --- | --- |
| `SyncExecution` | run inference in runtime thread |
| `AsyncExecution` | run inference in thread or process worker |
| `RemoteExecution` | request inference from remote server |

## `ActionQueue`

```python
queue.push_chunk(chunk)
action = queue.pop_or_none()
queue.clear()
```

Action queue owns runtime buffering, merging, smoothing, and late-result policy.
