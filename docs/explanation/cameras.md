# Cameras

Cameras expose a small capture interface.

```python
camera.connect()
frame = camera.read_latest()
camera.disconnect()
```

## Read Modes

| Method | Behavior | Use |
| --- | --- | --- |
| `read()` | next frame, blocking | recording or complete frame streams |
| `read_latest()` | newest frame, non-blocking | real-time control |
| `async_read()` | async wrapper around `read()` | async applications |

## Runtime Use

Control loops usually need freshness over completeness.

```python
observation["image.wrist"] = wrist_camera.read_latest()
```

Camera instances are not thread-safe. Use one thread per camera instance or external synchronization.
