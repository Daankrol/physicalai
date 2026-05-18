# CLI: Inspect Manifest

Use this command to inspect an exported policy manifest.

```bash
physicalai inspect-manifest ./exports/act_policy/manifest.json
```

The output should include at least the following information.

- manifest format and version
- policy name
- runner type
- artifacts
- preprocessors and postprocessors
- robot and camera specs

Run this command before deployment to verify that the package contains the expected artifacts and metadata.
