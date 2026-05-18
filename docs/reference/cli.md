# CLI Reference

The runtime CLI commands use the same schemas as the Python APIs.

## `physicalai run`

```bash
physicalai run --config runtime.yaml [--duration-s 60]
```

Arguments:

| Argument | Required | Description |
| --- | --- | --- |
| `--config` | yes | Runtime config YAML |
| `--duration-s` | no | Stop after the given duration in seconds |

The equivalent Python call is shown below.

```python
PolicyRuntime.from_config("runtime.yaml").run(duration_s=60)
```

## `physicalai infer`

```bash
physicalai infer --config inference.yaml --input observation.npz --output action.npz
```

Arguments:

| Argument | Required | Description |
| --- | --- | --- |
| `--config` | yes | Inference config YAML |
| `--input` | yes | Input observation file |
| `--output` | no | Output action file |

## `physicalai serve`

```bash
physicalai serve --config server.yaml --host 0.0.0.0 --port 8080
```

Use this command when inference should run remotely instead of on the robot host.

## `physicalai inspect-manifest`

```bash
physicalai inspect-manifest ./exports/act_policy/manifest.json
```

This command prints the exported package metadata.

## Plugin Commands

Training packages can add commands through entry points.

```toml
[project.entry-points."physicalai.cli.subcommands"]
fit = "physicalai.train.cli:register_fit"
validate = "physicalai.train.cli:register_validate"
test = "physicalai.train.cli:register_test"
predict = "physicalai.train.cli:register_predict"
export = "physicalai.train.cli:register_export"
```
