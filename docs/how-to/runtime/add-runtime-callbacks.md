# Add Runtime Callbacks

Use callbacks for product behavior around the runtime loop.

Example: record observations and actions.

```python
class RecordingCallback:
    def on_observation(self, observation, step):
        recorder.write_observation(step.t, observation)

    def before_send_action(self, action, step):
        recorder.write_policy_action(step.t, action)
        return action

    def on_action_sent(self, action, step):
        recorder.write_sent_action(step.t, action)

    def on_stop(self):
        recorder.close()
```

Attach it:

```python
runtime = PolicyRuntime(
    robot=robot,
    model=model,
    execution=execution,
    fps=30,
    callbacks=[RecordingCallback()],
)
```

Design rule: keep workflow-specific logic in callbacks unless it becomes a reusable runtime primitive.
