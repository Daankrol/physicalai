<p align="center">
  <img src="docs/assets/physicalai.png" alt="Physical AI" width="100%">
</p>

<div align="center">

**Runtime package for Physical AI inference, cameras, and robot interfaces**

[Overview](#overview) •
[Package Scope](#package-scope) •
[Quick Start](#quick-start) •
[Documentation](#documentation) •
[Contributing](#contributing)

<!-- TODO: Add badges here -->
<!-- [![python](https://img.shields.io/badge/python-3.12%2B-green)]() -->
<!-- [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE) -->

</div>

---

## Overview

`physicalai` is the runtime package for deploying exported robot policies and interacting with hardware. The repository currently provides:

- exported policy inference through `physicalai.inference`
- manifest-based model loading and component instantiation
- camera discovery and capture through `physicalai.capture`
- robot interfaces and verification utilities through `physicalai.robot`
- optional hardware-specific integrations through extras such as `so101`, `trossen`, `realsense`, and `basler`

This repository is intended to stay focused on runtime and deployment concerns. Training-specific code should live in a separate training package or be added through plugin-style extension points.

## Package Scope

The codebase is organized around a few runtime-facing areas.

| Area | What it provides |
| --- | --- |
| `physicalai.inference` | `InferenceModel`, manifests, adapters, runners, preprocessors, and postprocessors |
| `physicalai.capture` | camera interfaces, discovery, multi-camera reads, and transport helpers |
| `physicalai.robot` | robot protocol, connection helpers, verification utilities, and concrete robot integrations |
| `examples/` | small scripts for camera reads and hardware verification |
| `docs/` | user-facing documentation and detailed design notes |

## Key Features

- **Unified inference API**: Load exported policies with `InferenceModel` and run them with one runtime-facing interface.
- **Manifest-based packaging**: Use `manifest.json` to describe artifacts, runners, processors, and hardware metadata.
- **Camera interfaces**: Discover and read UVC, RealSense, and other supported camera backends.
- **Robot interfaces**: Connect to supported robots through a shared protocol and hardware-specific extras.
- **Deployment-oriented boundaries**: Keep runtime concerns in this package and avoid pulling in training dependencies by default.

## Quick Start

### Install

```bash
pip install physicalai
```

Install hardware extras only when you need them.

```bash
pip install "physicalai[so101]"
pip install "physicalai[realsense]"
```

### Inference

```python
from physicalai.inference import InferenceModel

model = InferenceModel.load("./exports/act_policy")
model.reset()
action = model.select_action(observation)
```

### Camera Read Example

```python
from physicalai.capture import UVCCamera

with UVCCamera(device="0") as camera:
    frame = camera.read_latest()
    print(frame.data.shape)
```

### Robot Verification Example

```python
from physicalai.robot import SO101, verify_robot

robot = SO101(port="/dev/ttyUSB0")
verify_robot(robot)
```

## Examples

The repository includes small scripts for common hardware checks.

| Example | Purpose |
| --- | --- |
| `examples/so101/read_joints.py` | Read live joint positions from an SO-101 arm |
| `examples/so101/move_joints.py` | Verify joint motion and calibration on an SO-101 arm |
| `examples/capture/read_uvc_camera.py` | Discover a UVC camera and print live frame summaries |

## Documentation

| Resource | Description |
| --- | --- |
| [Documentation](./docs/index.md) | Tutorials, how-to guides, explanations, and reference pages |
| [Documentation Plan](./docs/documentation-plan.md) | Documentation structure, writing rules, and maintenance strategy |
| [Design Docs](./docs/design/README.md) | Detailed architecture notes, design proposals, and tradeoffs |
| [Contributing](./CONTRIBUTING.md) | Development setup and contribution guidelines |
| [Support](./SUPPORT.md) | Help and reporting guidance |
| [Security](./SECURITY.md) | Vulnerability disclosure policy |
| [Code of Conduct](./CODE_OF_CONDUCT.md) | Community participation standards |

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](./CONTRIBUTING.md) for development setup, repository workflow, and contribution guidelines.
