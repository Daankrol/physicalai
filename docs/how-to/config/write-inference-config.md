# Write Inference Config

Use inference config when you need to author an inference pipeline outside an exported manifest.

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

If a manifest already contains the required runner, artifacts, processors, and hardware metadata, prefer loading from the manifest:

```python
model = InferenceModel.load("./exports/act_policy")
```

Use workflow config for user-authored intent. Use manifest for exported package metadata.
