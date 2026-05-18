# Instantiate Components

A component spec describes one instantiable object.

The most explicit form uses a class path.

```yaml
class_path: physicalai.inference.runners.ActionChunking
init_args:
  chunk_size: 50
  n_action_steps: 50
```

The shorter form uses a registry name.

```yaml
type: action_chunking
chunk_size: 50
n_action_steps: 50
```

You can construct and instantiate the same spec from Python.

```python
from physicalai.config import ComponentSpec, instantiate_component

spec = ComponentSpec(
    class_path="physicalai.inference.runners.ActionChunking",
    init_args={"chunk_size": 50, "n_action_steps": 50},
)

runner = instantiate_component(spec)
```

Nested component specs are instantiated recursively.

```yaml
class_path: physicalai.runtime.PolicyRuntime
init_args:
  robot:
    class_path: physicalai.robot.so101.SO101
    init_args:
      port: /dev/ttyACM0
```

`ComponentSpec` describes what should be built. Instantiation is the separate step that creates the live object.
