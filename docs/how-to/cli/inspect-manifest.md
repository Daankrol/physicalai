# CLI: Inspect Manifest

Inspect an exported policy manifest:

```bash
physicalai inspect-manifest ./exports/act_policy/manifest.json
```

Expected output should include:

- manifest format and version
- policy name
- runner type
- artifacts
- preprocessors and postprocessors
- robot and camera specs

Use this before deployment to check that the package contains the expected artifacts and metadata.
