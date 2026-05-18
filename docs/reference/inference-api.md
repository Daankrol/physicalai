# Inference API Reference

## `InferenceModel`

```python
InferenceModel(
    export_dir: str | Path,
    policy_name: str | None = None,
    backend: str = "auto",
    device: str = "auto",
    runner: InferenceRunner | None = None,
    preprocessors: list[Preprocessor] | None = None,
    postprocessors: list[Postprocessor] | None = None,
    callbacks: list[Callback] | None = None,
    **adapter_kwargs,
)
```

## Constructors

```python
model = InferenceModel.load("./exports/act_policy")
model = InferenceModel.from_config("inference.yaml")
```

## Methods

### `select_action`

```python
action = model.select_action(observation)
```

Returns one action.

### `predict_action_chunk`

```python
chunk = model.predict_action_chunk(observation)
```

Returns a chunk of actions for runtime queueing.

### `reset`

```python
model.reset()
```

Clears runner state and action cursor.

### `close`

```python
model.close()
```

Releases backend resources.

## Observation

Observations are dictionaries of NumPy arrays.

```python
observation = {
    "state": joint_positions,
    "image.wrist": wrist_image,
}
```

Expected keys and shapes come from the exported package and policy preprocessing pipeline.
