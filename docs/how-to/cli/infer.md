# CLI: Infer

Run inference from a config or exported package.

```bash
physicalai infer --config inference.yaml --input observation.npz --output action.npz
```

Example config:

```yaml
model:
  class_path: physicalai.inference.InferenceModel
  init_args:
    export_dir: ./exports/act_policy
    backend: openvino
    device: CPU
```

Expected Python equivalent:

```python
model = InferenceModel.from_config("inference.yaml")
action = model.select_action(observation)
```

Use `physicalai run` for robot control loops. Use `physicalai infer` for offline or single-step inference.
