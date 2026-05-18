# Run a Policy

Use `PolicyRuntime` when the policy controls a robot loop.

```python
from physicalai.inference import InferenceModel
from physicalai.runtime import PolicyRuntime, SyncExecution
from physicalai.robot.so101 import SO101

model = InferenceModel.load("./exports/act_policy")
robot = SO101(port="/dev/ttyACM0")

runtime = PolicyRuntime(
    robot=robot,
    model=model,
    execution=SyncExecution(mode="chunk"),
    fps=30,
)

runtime.run(duration_s=60)
```

Equivalent CLI:

```bash
physicalai run --config runtime.yaml --duration-s 60
```

Minimal runtime config:

```yaml
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

Runtime loop shape:

```text
read robot observation
read camera frames
request inference
pop one action
send action
sleep until next tick
```
