<p align="center">
  <img src="docs/assets/physicalai.png" alt="Physical AI" width="100%">
</p>

<div align="center">

**Runtime package for exported robot policies, cameras, and robots**

[Quick Start](#quick-start) •
[Examples](#examples) •
[Docs](#docs)

</div>

---

## What This Repo Is

```text
exported policy package
    -> physicalai.inference
    -> physicalai.capture
    -> physicalai.robot
```

This repository contains the runtime-side pieces for deploying policies and talking to hardware.

## What You Can Do

```text
load a policy         physicalai.inference.InferenceModel
read cameras          physicalai.capture.*
connect robots        physicalai.robot.*
verify hardware       examples/ and robot utilities
```

## Quick Start

Install:

```bash
pip install physicalai
```

Inference:

```python
from physicalai.inference import InferenceModel

model = InferenceModel.load("./exports/act_policy")
model.reset()
action = model.select_action(observation)
```

Camera read:

```python
from physicalai.capture import UVCCamera

with UVCCamera(device="0") as camera:
    frame = camera.read_latest()
    print(frame.data.shape)
```

Robot verify:

```python
from physicalai.robot import SO101, verify_robot

robot = SO101(port="/dev/ttyUSB0")
verify_robot(robot)
```

## Examples

SO-101 joint read:

```bash
python examples/so101/read_joints.py --port /dev/ttyUSB0
```

SO-101 motion check:

```bash
python examples/so101/move_joints.py --port /dev/ttyUSB0 --calibration calibration.json
```

UVC camera read:

```bash
python examples/capture/read_uvc_camera.py
```

## Docs

- [Documentation Home](./docs/index.md)
- [Getting Started](./docs/getting-started/README.md)
- [How-To Guides](./docs/how-to/README.md)
- [Explanation](./docs/explanation/README.md)
- [Reference](./docs/reference/README.md)
- [Design Docs](./docs/design/README.md)

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md).
