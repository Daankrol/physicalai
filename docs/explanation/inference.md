# Inference

`InferenceModel` is the runtime API for exported policies.

```python
model = InferenceModel.load("./exports/act_policy")
action = model.select_action(observation)
```

## Pipeline

```text
observation
  -> preprocessors
  -> runner
  -> postprocessors
  -> action
```

## APIs

| Method | Use |
| --- | --- |
| `select_action(observation)` | return one action now |
| `predict_action_chunk(observation)` | return a chunk for runtime queueing |
| `reset()` | clear state for a new episode |
| `close()` | release backend resources |

## Chunked Policies

Chunk-producing policies still support `select_action()`.

```python
if cursor.empty():
    cursor.push_chunk(model.predict_action_chunk(obs))

return cursor.pop()
```

The cursor is a model convenience. It is not the runtime action queue.

## Runtime Boundary

Use `select_action()` for scripts, tests, demos, and evaluation loops.

Use `predict_action_chunk()` through `PolicyRuntime` for robot execution.

```text
PolicyRuntime
  -> Execution.maybe_request(obs)
  -> InferenceModel.predict_action_chunk(obs)
  -> ActionQueue.push_chunk(chunk)
  -> ActionQueue.pop_or_none()
  -> robot.send_action(action)
```
