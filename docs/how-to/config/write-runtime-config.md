# Write Runtime Config

Runtime config describes a robot control workflow before execution.

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

Run from Python:

```python
from physicalai.runtime import PolicyRuntime

runtime = PolicyRuntime.from_config("runtime.yaml")
runtime.run(duration_s=60)
```

Run from CLI:

```bash
physicalai run --config runtime.yaml --duration-s 60
```

Nested components use the same shape:

```yaml
class_path: module.ClassName
init_args:
  key: value
```

Config is passive data. `PolicyRuntime.run()` executes the workflow.
