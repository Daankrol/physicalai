# CLI

The CLI is a thin wrapper over the same config APIs used by Python.

```bash
physicalai run --config runtime.yaml --duration-s 60
```

Equivalent:

```python
PolicyRuntime.from_config("runtime.yaml").run(duration_s=60)
```

## Runtime Commands

| Command | Purpose |
| --- | --- |
| `physicalai infer` | run offline inference |
| `physicalai run` | run a policy on robot hardware |
| `physicalai serve` | serve policy inference remotely |
| `physicalai inspect-manifest` | inspect exported package metadata |

## Training Commands

Training commands should come from training packages or entry-point plugins.

```toml
[project.entry-points."physicalai.cli.subcommands"]
fit = "physicalai.train.cli:register_fit"
export = "physicalai.train.cli:register_export"
```

Importing `physicalai` should not import training dependencies.
