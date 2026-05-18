# Write Inference Config

Use an inference config when you need to author an inference pipeline outside an exported manifest.

```yaml
model:
  class_path: physicalai.inference.InferenceModel
  init_args:
    export_dir: ./exports/act_policy
    backend: openvino
    device: CPU
```

Python:

```python
from physicalai.config import instantiate_component

model = instantiate_component(config.model)
action = model.select_action(observation)
```

If the manifest already contains the required runner, artifacts, processors, and hardware metadata, prefer loading from the manifest instead.

```python
model = InferenceModel.load("./exports/act_policy")
```

Use workflow config to express user-authored intent. Use a manifest to describe exported package metadata.
