# Use Cameras

Add cameras to runtime config when observations require images.

```yaml
runtime:
  class_path: physicalai.runtime.PolicyRuntime
  init_args:
    fps: 30
    robot:
      class_path: physicalai.robot.so101.SO101
      init_args:
        port: /dev/ttyACM0
    cameras:
      wrist:
        class_path: physicalai.capture.cameras.uvc.UVCCamera
        init_args:
          device_id: /dev/video0
      front:
        class_path: physicalai.capture.cameras.realsense.RealSenseCamera
        init_args:
          serial_number: "123456"
    model:
      class_path: physicalai.inference.InferenceModel
      init_args:
        export_dir: ./exports/act_policy
    execution:
      class_path: physicalai.runtime.SyncExecution
      init_args:
        mode: chunk
```

Runtime observation assembly:

```text
robot.get_observation()
camera["wrist"].read_latest()
camera["front"].read_latest()
merge into observation dict
```

Use `read_latest()` for control loops. Use `read()` when every frame must be preserved.
