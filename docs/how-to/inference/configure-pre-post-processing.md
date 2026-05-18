# Configure Preprocessing and Postprocessing

Preprocessors run before model execution. Postprocessors run after model execution.

Manifest example:

```yaml
model:
  runner:
    type: action_chunking
    chunk_size: 50
  artifacts:
    openvino: model.xml
  preprocessors:
    - type: normalize
      artifact: stats.safetensors
  postprocessors:
    - type: denormalize
      artifact: stats.safetensors
```

Direct class mode:

```yaml
preprocessors:
  - class_path: physicalai.inference.preprocessors.StatsNormalizer
    init_args:
      artifact: stats.safetensors
```

Pipeline shape:

```text
observation
  -> preprocessors
  -> runner
  -> postprocessors
  -> action output
```

Use `type` for registered built-ins. Use `class_path` for explicit imports.
