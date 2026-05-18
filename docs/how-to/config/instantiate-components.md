# Instantiate Components

A component spec describes one instantiable object.

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

Python:

```python
from physicalai.config import ComponentSpec, instantiate_component

spec = ComponentSpec(
    class_path="physicalai.inference.runners.ActionChunking",
    init_args={"chunk_size": 50, "n_action_steps": 50},
)

runner = instantiate_component(spec)
```

Nested components are instantiated recursively:

```yaml
class_path: physicalai.runtime.PolicyRuntime
init_args:
  robot:
    class_path: physicalai.robot.so101.SO101
    init_args:
      port: /dev/ttyACM0
```

Rule: `ComponentSpec` describes what to build. Instantiation builds it.
