# CLI: Run

Run a policy runtime from YAML:

```bash
physicalai run --config runtime.yaml
```

Limit duration:

```bash
physicalai run --config runtime.yaml --duration-s 60
```

Expected Python equivalent:

```python
from physicalai.runtime import PolicyRuntime

PolicyRuntime.from_config("runtime.yaml").run(duration_s=60)
```

The CLI must use the same config schema as Python APIs.

Runtime commands live in the `physicalai` package. Training commands should be provided by training packages or plugin entry points.
