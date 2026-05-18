# Run a Policy on a Robot

Start by writing a runtime configuration file.

```yaml
# runtime.yaml
runtime:
  class_path: physicalai.runtime.PolicyRuntime
  init_args:
    fps: 30
    robot:
      class_path: physicalai.robot.so101.SO101
      init_args:
        port: /dev/ttyACM0
    model:
      class_path: physicalai.inference.InferenceModel
      init_args:
        export_dir: ./exports/act_policy
    execution:
      class_path: physicalai.runtime.SyncExecution
      init_args:
        mode: chunk
```

Then run the runtime from the CLI.

```bash
physicalai run --config runtime.yaml --duration-s 60
```

The equivalent Python entry point is shown below.

```python
from physicalai.runtime import PolicyRuntime

runtime = PolicyRuntime.from_config("runtime.yaml")
runtime.run(duration_s=60)
```

The runtime is easier to reason about when each object has a clear ownership boundary.

| Object | Owns |
| --- | --- |
| `InferenceModel` | policy inference |
| `PolicyRuntime` | robot loop and timing |
| `Execution` | where inference runs |
| `ActionQueue` | action buffering |
| `Robot` | hardware IO |
