# Instantiate Components

A component spec describes one instantiable object.

The most explicit form uses a class path.

```yaml
class_path: physicalai.capture.UVCCamera
init_args:
  device: /dev/video0
  width: 640
  height: 480
```

The shorter form uses a registry name.

```yaml
type: uvc
device: /dev/video0
width: 640
height: 480
```

You can construct and instantiate the same spec from Python.

```python
from physicalai.config import ComponentSpec, instantiate_component

spec = ComponentSpec(
    class_path="physicalai.capture.UVCCamera",
    init_args={"device": "/dev/video0", "width": 640, "height": 480},
)

camera = instantiate_component(spec)
```

Nested component specs are instantiated recursively.

```yaml
class_path: physicalai.runtime.PolicyRuntime
init_args:
  robot:
    class_path: physicalai.robot.so101.SO101
    init_args:
      port: /dev/ttyACM0
  cameras:
    wrist:
      class_path: physicalai.capture.UVCCamera
      init_args:
        device: /dev/video0
```

`ComponentSpec` describes what should be built. Instantiation is the separate step that creates the live object.
