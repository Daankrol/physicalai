# Getting Started

Tutorials for the first successful PhysicalAI workflows.

## Order

1. [Installation](installation.md)
2. [Quickstart](quickstart.md)
3. [Run a Policy](run-a-policy.md)

## Minimal Path

```bash
pip install physicalai
physicalai inspect-manifest ./exports/act_policy/manifest.json
physicalai run --config runtime.yaml --duration-s 60
```

Use Python when you need control over objects. Use YAML and CLI when you need reproducible runs.
