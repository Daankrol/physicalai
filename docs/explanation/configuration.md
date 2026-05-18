# Configuration

The config system makes Python, YAML, CLI, and Studio payloads use the same workflow shape.

```python
runtime = PolicyRuntime.from_config("runtime.yaml")
runtime.run()
```

```bash
physicalai run --config runtime.yaml
```

## Layers

```text
Config
  typed constructor args for one class

ComponentSpec
  target + args for one instantiable component

Workflow config
  user-authored workflow before execution

Manifest
  exported package metadata after build/export

Orchestrator
  live object that executes the workflow
```

## ComponentSpec

Direct class mode:

```yaml
class_path: physicalai.inference.runners.ActionChunking
init_args:
  chunk_size: 50
  n_action_steps: 50
```

Registry mode:

```yaml
type: action_chunking
chunk_size: 50
n_action_steps: 50
```

`class_path` takes precedence when both are present.

## Typed Config

Use typed configs for constructor validation.

```python
@dataclass
class Pi05Config(Config):
    chunk_size: int = 50
    n_action_steps: int = 50

    def __post_init__(self) -> None:
        if self.n_action_steps > self.chunk_size:
            raise ValueError("n_action_steps must be <= chunk_size")
```

Typed configs do not decide which class to instantiate.

```python
cfg = Pi05Config(chunk_size=50)
policy = instantiate_obj(cfg, target_cls=Pi05)
```

## Rule

Config is data. Orchestrators execute.

```python
config = RuntimeConfig.load("runtime.yaml")
runtime = PolicyRuntime.from_config(config)
runtime.run()
```
