# OpenVINO Validation — Foundation

**Status:** Draft · **Owner:** physicalai team · **Date:** 2026-06-26

The starting point for validating that physicalai keeps working across OpenVINO
releases. This defines the contract, who owns what, and the basic test that
covers it. More test scenarios build on this.

## Why

An OpenVINO upgrade broke physicalai inference — hence the current
`openvino==2026.1` pin in [`pyproject.toml`](../../pyproject.toml). We need an
automated signal that an OpenVINO change still works with physicalai _before_ we
adopt it.

## The Contract

"OpenVINO works with physicalai" means a real exported policy loads and runs
through the physicalai OpenVINO code paths. Three stages must pass:

| Stage         | Code path                 | What it proves                                                   |
| ------------- | ------------------------- | ---------------------------------------------------------------- |
| **load**      | `OpenVINOAdapter.load`    | `read_model` + `compile_model` succeed                           |
| **tokenizer** | `OVTokenizer`             | `openvino_tokenizers` extension loads + matches core OpenVINO    |
| **predict**   | `OpenVINOAdapter.predict` | inference runs, outputs have expected shape/dtype and are finite |

The tokenizer stage matters because `openvino` and `openvino_tokenizers` are
versioned **independently** and must stay a matched pair — a mismatch is what
broke us, and it only affects models that carry a tokenizer.

## Who Owns What

| Concern                                           | Owner             |
| ------------------------------------------------- | ----------------- |
| Test definition (source of truth)                 | **physicalai**    |
| Pass/fail criteria                                | **physicalai**    |
| PR merge gate                                     | **physicalai** CI |
| Early-warning runs against new/pre-release wheels | **physicalai** CI |
| Running the same test in pre-release matrix       | **OpenVINO**      |
| Pre-release wheels + breakage notification        | **OpenVINO**      |

The test lives in the physicalai repo because it encodes _our_ use of OpenVINO.
OpenVINO points their pre-release matrix at it. Same test, multiple runners: we
catch _our_ changes on every PR; we run an independent early-warning against new
OpenVINO wheels; OpenVINO catches _their_ changes before release.

## Basic Test

[`tests/integration/test_ov_model_compat.py`](../../tests/integration/test_ov_model_compat.py),
marker `ov_smoke`. It runs the three contract stages against discovered model
exports and records the `openvino` / `openvino_tokenizers` versions in each
result.

Coverage needs **two models** to cover the contract:

| Model                                     | Covers                     |
| ----------------------------------------- | -------------------------- |
| **ACT** (no tokenizer)                    | load + predict             |
| **a tokenizer-bearing model** (e.g. pi05) | load + tokenizer + predict |

Verified 2026-06-26: under a core/tokenizer mismatch, ACT passes and the
tokenizer model fails at the tokenizer stage — so this pair detects the exact
break that caused the pin.

## Early Warning

Two runners on physicalai CI, both **alert-only** (open an issue, never block
merges), with a named owner to triage:

- **Renovate-triggered (primary):** when a Renovate PR bumps `openvino*`, run
  `ov_smoke` against the PR's resolved versions. Event-driven — fires exactly
  when a new version appears.
- **Weekly (catch-all):** scheduled run installing the latest / `--pre` wheels,
  for releases Renovate won't propose and quiet weeks with no PRs.

This is our **independent** safety net for "did a new OpenVINO break us" — it
does not depend on OpenVINO running anything.

## Next (after this foundation)

- Lock `openvino` + `openvino_tokenizers` as a matched pair in
  [`pyproject.toml`](../../pyproject.toml).
- Add a small tokenizer-bearing model the gate can run (pi05 is too large for
  hosted CI).
- Wire `ov_smoke` into [`library.yml`](../../.github/workflows/library.yml) as a
  PR gate, plus the two early-warning runners above.
- Add more scenarios: full pipeline + golden action, GPU/NPU (untested locally —
  no Intel GPU on the dev machine).
