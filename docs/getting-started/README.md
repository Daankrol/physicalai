# Getting Started

This section contains short tutorials for the first successful PhysicalAI workflows.

## Recommended Order

1. [Installation](installation.md)
2. [Quickstart](quickstart.md)
3. [Run a Policy](run-a-policy.md)

## Minimal Path

```bash
pip install physicalai
physicalai inspect-manifest ./exports/act_policy/manifest.json
physicalai run --config runtime.yaml --duration-s 60
```

Use Python when you need direct control over objects. Use YAML and the CLI when you need a reproducible run that can be shared or repeated.
