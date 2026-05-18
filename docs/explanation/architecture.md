# Architecture

PhysicalAI runtime has four main layers.

```text
exported package
    -> InferenceModel
    -> PolicyRuntime
    -> Robot and cameras
```

## Components

| Component | Responsibility |
| --- | --- |
| `Manifest` | describes exported artifacts and inference pipeline |
| `InferenceModel` | loads artifacts and computes actions |
| `Robot` | reads state and sends commands |
| `Camera` | reads image frames |
| `Execution` | decides where inference runs |
| `ActionQueue` | buffers and merges action chunks |
| `PolicyRuntime` | runs the robot control loop |

## Package Boundary

`physicalai` is the runtime package. It should not require training dependencies to import or run deployment workflows.

Training packages can add commands through CLI entry points.

```text
physicalai
  infer
  run
  serve
  inspect-manifest

physicalai-train package
  fit
  validate
  test
  predict
  export
```

## Design Rules

- Config objects are passive data.
- Orchestrators execute workflows.
- `InferenceModel` does not own robot timing.
- `PolicyRuntime` does not own policy math.
- Manifests describe exported packages.
- Workflow configs describe desired execution before it starts.
