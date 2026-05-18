# Manifests

A manifest describes an exported policy package.

```text
export/
├── manifest.json
├── model.xml
└── stats.safetensors
```

## Example

```yaml
format: policy_package
version: "1.0"

policy:
  name: pi05
  source:
    class_path: physicalai.policies.pi05.Pi05

model:
  artifacts:
    openvino: model.xml
  runner:
    type: action_chunking
    chunk_size: 50
  preprocessors:
    - type: normalize
      artifact: stats.safetensors

hardware:
  robots:
    - name: main
      type: SO101
```

## Manifest vs Workflow Config

| Data | Meaning |
| --- | --- |
| Workflow config | desired workflow before running or exporting |
| Manifest | concrete exported package after build/export |

Load package:

```python
model = InferenceModel.load("./export")
```

Inspect metadata:

```python
manifest = Manifest.load("./export/manifest.json")
```

The schemas can share `ComponentSpec`, but their purpose stays different.
