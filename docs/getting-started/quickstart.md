# Quickstart

Load an exported policy package and compute one action.

```python
from physicalai.inference import InferenceModel

model = InferenceModel.load("./exports/act_policy")
model.reset()

action = model.select_action(observation)
```

`observation` is a dictionary of NumPy arrays using names expected by the exported policy.

Example shape:

```python
observation = {
    "state": joint_positions,
    "image.wrist": wrist_image,
    "image.front": front_image,
}
```

## Chunk Policies

Some policies produce action chunks. `select_action()` still returns one action.

```python
for _ in range(100):
    action = model.select_action(observation)
    observation = env.step(action)
```

For runtime loops, use chunk prediction through `PolicyRuntime` instead of manually managing timing.

```python
chunk = model.predict_action_chunk(observation)
```

## Manifest Path

Exported packages include a manifest:

```text
exports/act_policy/
├── manifest.json
├── model.xml
└── stats.safetensors
```

The manifest describes artifacts, runner, preprocessing, postprocessing, and hardware metadata.
