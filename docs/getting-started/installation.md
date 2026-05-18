# Installation

Install the runtime package:

```bash
pip install physicalai
```

Install hardware extras only when needed:

```bash
pip install "physicalai[realsense]"
pip install "physicalai[so101]"
pip install "physicalai[robots]"
```

Development install:

```bash
uv sync
uv run pytest
```

## Package Boundary

`physicalai` is the runtime package. It should stay usable on deployment hosts without training dependencies such as Torch or Lightning.

Training commands may be provided by a separate training distribution or plugin entry points.

## Check Install

```python
import physicalai
from physicalai.inference import InferenceModel
```

If hardware extras are not installed, importing the base runtime should still work.
