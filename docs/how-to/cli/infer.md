# CLI: Infer

*(Planned API — interface may change.)*

Run inference from a config or exported policy package.

```bash
physicalai infer --config inference.yaml
```

Example config:

```yaml
model:
  class_path: physicalai.inference.InferenceModel
  init_args:
    path: ./exports/act_policy
    backend: openvino
    device: CPU
```

The Python equivalent:

```python
model = InferenceModel.from_config("inference.yaml")
action = model.select_action(observation)
```

Use `physicalai run` for robot control loops. Use `physicalai infer` for offline inference or testing outside a runtime loop.
