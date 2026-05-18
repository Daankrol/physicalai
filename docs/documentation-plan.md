# Documentation Plan

This document records the documentation approach for the `physicalai` repository.

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

Use this section for first successful workflows.

Examples include:

- installing the package
- loading an exported policy
- running a policy on a robot

### How-To

Use this section for a concrete task with a clear end state.

Examples include:

- writing a runtime config
- using cameras in a control loop
- running the CLI

### Explanation

This section should explain the stable mental model of the system.

It should cover:

- ownership boundaries
- invariants
- terminology

### Reference

Use this section for exact lookup material.

Examples include:

- CLI arguments
- config shapes
- manifest fields
- public API signatures

### Design

This section keeps detailed plans, tradeoffs, reviews, and alternatives.

These documents are inputs to implementation and stable user docs. They are not the user docs themselves.

## Writing Style

- Use plain Markdown only.
- Keep paragraphs short.
- Keep headings short.
- Use an engineering-neutral tone.
- Avoid marketing language.
- Avoid speculative language unless it is explicitly labeled.
- Prefer tables for boundaries and fields.
- Prefer small examples over long narrative text.

## Examples

Examples should use:

- minimal Python examples
- minimal YAML examples
- short CLI commands
- short pseudo-code for control flow

Examples should avoid:

- long generated code blocks
- repeated examples with only small changes
- framework-specific Markdown features

## Assumptions and Planned APIs

Some docs describe APIs that are planned but not fully implemented yet.

Current planned areas include:

- `physicalai.runtime.PolicyRuntime`
- runtime `Execution` and `ActionQueue`
- runtime CLI commands such as `run`, `infer`, `serve`, and `inspect-manifest`
- config entry points around `ComponentSpec`, workflow config, and `from_config`

When documentation describes planned APIs, it should reflect the accepted design direction and intended contracts.

## Reference Strategy

Use a mixed model, with both manual and auto-generated references.

### Manual Reference

Keep the following pages hand-written:

- CLI reference while commands are still evolving
- config schema reference
- manifest schema reference with semantics and examples

### Generated Reference

Generate the following pages later from docstrings when the implementation stabilizes:

- public Python API pages

The recommended future tool is `mkdocstrings`.

The general rule is simple: generated API pages should be wrapped by short hand-written introductions and examples.

## Build Strategy

Use MkDocs with plain Markdown.

This choice keeps the documentation simple to maintain.

Reasons:

- the build stays repository-local
- the Markdown source remains portable
- future integration with `mkdocstrings` stays straightforward
- the docs do not require MDX

The repository includes a build-ready `mkdocs.yml`.

## Maintenance Rules

- Design docs can be detailed.
- Explanation docs should stay trimmed.
- If code and docs disagree, update both in the same change when possible.
- Do not let design docs become the only source of public behavior.
- Keep examples runnable or close to runnable.

## Future Work

1. Add a docs CI build.
2. Add `mkdocstrings` once runtime and config APIs stabilize.
3. Replace manual API signature pages with generated API pages.
4. Generate CLI reference from parser help once the CLI implementation lands.
5. Generate JSON Schema for manifest and config models where useful.
