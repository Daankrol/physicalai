# Documentation Plan

This document records the documentation approach for the `physicalai` repository.

## Goals

- document the runtime package as a user-facing product
- separate stable user docs from detailed design history
- keep tone engineering-neutral and concise
- prefer examples, pseudo-code, and exact contracts over long prose
- keep docs portable across Markdown renderers

## Documentation Model

The docs follow the Diataxis structure.

```text
docs/
├── getting-started/  # tutorials
├── how-to/           # task guides
├── explanation/      # concepts and boundaries
├── reference/        # exact commands, schemas, APIs
└── design/           # detailed design notes and tradeoffs
```

## Section Rules

### Getting Started

Use for first successful workflows.

Examples:

- install the package
- load an exported policy
- run a policy on a robot

### How-To

Use for a concrete task with a clear end state.

Examples:

- write a runtime config
- use cameras in a control loop
- run the CLI

### Explanation

Use for stable mental models and boundaries.

Keep these short.

Do:

- explain ownership boundaries
- explain invariants
- explain terminology

Do not:

- copy design documents
- include implementation history
- include option analysis unless still required for understanding

### Reference

Use for exact lookup material.

Examples:

- CLI arguments
- config shapes
- manifest fields
- public API signatures

### Design

Keep detailed plans, tradeoffs, reviews, and alternatives here.

These documents are inputs to user docs, not user docs themselves.

## Writing Style

- plain Markdown only
- short paragraphs
- short headings
- engineering-neutral tone
- no marketing language
- no speculative language unless explicitly labeled
- prefer tables for boundaries and fields
- prefer small examples over long narrative text

## Examples

Prefer:

- minimal Python examples
- minimal YAML examples
- short CLI commands
- short pseudo-code for control flow

Avoid:

- long generated code blocks
- repeated examples with only small changes
- framework-specific Markdown features

## Assumptions and Planned APIs

Some docs describe APIs that are planned but not fully implemented yet.

Current planned areas:

- `physicalai.runtime.PolicyRuntime`
- runtime `Execution` and `ActionQueue`
- runtime CLI commands such as `run`, `infer`, `serve`, and `inspect-manifest`
- config entry points around `ComponentSpec`, workflow config, and `from_config`

When documentation describes planned APIs, it should reflect the accepted design direction and intended contracts.

## Reference Strategy

Use a mixed model.

### Manual Reference

Keep these hand-written:

- CLI reference while commands are still evolving
- config schema reference
- manifest schema reference with semantics and examples

### Generated Reference

Generate these later from docstrings when implementation stabilizes:

- public Python API pages

Recommended future tool:

- `mkdocstrings` for Python API pages

Rule:

- generated API pages should be wrapped by short hand-written introductions and examples

## Build Strategy

Use MkDocs with plain Markdown.

Reasons:

- simple repository-local build
- portable Markdown source
- easy future integration with `mkdocstrings`
- does not require MDX

The repository includes a build-ready `mkdocs.yml`.

## Maintenance Rules

- design docs can be detailed
- explanation docs must stay trimmed
- if code and docs disagree, update both in the same change when possible
- do not let design docs become the only source of public behavior
- keep examples runnable or close to runnable

## Future Work

1. Add a docs CI build.
2. Add `mkdocstrings` once runtime/config APIs stabilize.
3. Replace manual API signature pages with generated API pages.
4. Generate CLI reference from parser help once CLI implementation lands.
5. Generate JSON Schema for manifest and config models where useful.
