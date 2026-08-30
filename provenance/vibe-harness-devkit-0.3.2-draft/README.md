# Vibe Harness devkit provenance

This directory is **developer-only provenance**, not a FrontierLoop runtime, Skill root, install source, or
release payload.

FrontierLoop adapted a subset of Skills from the user-supplied
`vibe-harness-runtime-main(2).zip`, specifically
`vibe-harness-devkit-0.3.2-draft/skills/*`. The active FrontierLoop Skill implementations live only under
`skills/frontier-*`.

The current tree intentionally keeps only:

- the upstream notice in `NOTICE.md`;
- the canonical source hashes and active mappings in `references/SKILL_SOURCE_MAP.json`.

The complete historical upstream Skill snapshot is preserved by Git rather than duplicated in current
main. Retrieve it from Git tag `v0.8.2` at:

`provenance/vibe-harness-runtime-0.3.2-draft/skills`

Install caches and deterministic release archives exclude the entire `provenance/` directory. This keeps
runtime ownership and distribution minimal while preserving auditability and license traceability.
