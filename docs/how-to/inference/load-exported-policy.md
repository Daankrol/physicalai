# Load an Exported Policy

Load with auto-detection:

```python
from physicalai.inference import InferenceModel

model = InferenceModel.load("./exports/act_policy")
```

Run one action:

```python
model.reset()
action = model.select_action(observation)
```

Select backend explicitly:

```python
model = InferenceModel.load(
    "./exports/act_policy",
    backend="openvino",
    device="CPU",
)
```

Use chunk prediction when a runtime owns queueing:

```python
chunk = model.predict_action_chunk(observation)
```

Do not implement robot-loop timing around `select_action()`. Use `PolicyRuntime` for that.
