# Use a Manifest

An exported policy package contains `manifest.json`.

```text
exports/act_policy/
├── manifest.json
├── model.xml
└── stats.safetensors
```

Load through `InferenceModel`:

```python
model = InferenceModel.load("./exports/act_policy")
```

Inspect the manifest directly:

```python
from physicalai.inference.manifest import Manifest

manifest = Manifest.load("./exports/act_policy/manifest.json")
print(manifest.model.runner)
print(manifest.model.artifacts)
```

CLI:

```bash
physicalai inspect-manifest ./exports/act_policy/manifest.json
```

Use manifests for exported artifacts. Use workflow config for authoring training, inference, or runtime workflows.
