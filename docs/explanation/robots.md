# Robots

Robots implement a structural interface. Inheritance is not required.

```python
class MyRobot:
    joint_names = ["shoulder", "elbow", "wrist"]

    def connect(self) -> None: ...
    def disconnect(self) -> None: ...
    def get_observation(self) -> MyObservation: ...
    def send_action(self, action, *, goal_time: float = 0.1) -> None: ...
    def is_connected(self) -> bool: ...
```

## Observation

An observation exposes at least:

```python
joint_positions: np.ndarray
timestamp: float
sensor_data: dict[str, np.ndarray] | None
images: dict[str, Frame] | None
```

## Action Contract

`send_action()` receives one action ordered to match `joint_names`.

```python
action.shape == (len(robot.joint_names),)
```

Robot implementations own hardware safety on disconnect.
