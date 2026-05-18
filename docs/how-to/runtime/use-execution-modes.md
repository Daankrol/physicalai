# Use Execution Modes

`Execution` decides where inference runs.

## Synchronous

Runs inference in the runtime thread.

```yaml
execution:
  class_path: physicalai.runtime.SyncExecution
  init_args:
    mode: chunk
```

Use for simple deployments and debugging.

## Thread Worker

Runs inference in a background thread.

```yaml
execution:
  class_path: physicalai.runtime.AsyncExecution
  init_args:
    transport: thread
```

Use when model latency should not block robot timing.

## Process Worker

Runs inference in a worker process.

```yaml
execution:
  class_path: physicalai.runtime.AsyncExecution
  init_args:
    transport: process
```

Use when model execution should be isolated from the robot process.

## Remote

Sends inference requests to a policy server.

```yaml
execution:
  class_path: physicalai.runtime.RemoteExecution
  init_args:
    endpoint: http://robot-server:8080
```

Use when the robot host should not hold policy weights or accelerator dependencies.
