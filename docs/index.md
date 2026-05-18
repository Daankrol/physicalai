# PhysicalAI Documentation

PhysicalAI provides runtime components for working with exported robot policies. The documentation is organized around the main deployment tasks and the runtime concepts behind them.

## Quick Links

| I want to | Go to |
| --- | --- |
| Understand the documentation structure | [Documentation Plan](documentation-plan.md) |
| Install the package | [Installation](getting-started/installation.md) |
| Run first inference | [Quickstart](getting-started/quickstart.md) |
| Run a policy on a robot | [Run a Policy](getting-started/run-a-policy.md) |
| Write runtime YAML | [Runtime Config](how-to/config/write-runtime-config.md) |
| Use the runtime CLI | [CLI Run](how-to/cli/run.md) |
| Understand architecture | [Architecture](explanation/architecture.md) |
| Look up schemas | [Config Schema](reference/config-schema.md) |

## Documentation Structure

```text
docs/
├── getting-started/  # tutorials
├── how-to/           # task guides
├── explanation/      # concepts and boundaries
├── reference/        # exact commands, schemas, APIs
└── design/           # detailed design notes
```

## Workflow

Most deployment workflows follow the same path from an exported package to a running robot loop.

```text
exported policy package
    -> InferenceModel
    -> PolicyRuntime
    -> Robot
```

Python example:

```python
from physicalai.inference import InferenceModel
from physicalai.runtime import PolicyRuntime, SyncExecution
from physicalai.robot.so101 import SO101

model = InferenceModel.load("./exports/act_policy")
robot = SO101(port="/dev/ttyACM0")

runtime = PolicyRuntime(
    robot=robot,
    model=model,
    execution=SyncExecution(mode="chunk"),
    fps=30,
)

runtime.run(duration_s=60)
```

CLI example:

```bash
physicalai run --config runtime.yaml --duration-s 60
```

## Notes

- The documentation structure and maintenance rules are recorded in [Documentation Plan](documentation-plan.md).
- Detailed tradeoffs and phased design work remain in [Design Docs](design/README.md).
