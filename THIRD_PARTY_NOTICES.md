# Third-party and source notices

The active FrontierLoop skills include adaptations of files from the user-supplied
`vibe-harness-runtime-main(2).zip`, specifically
`vibe-harness-devkit-0.3.2-draft/skills/*`.

The supplied Vibe Harness notice states that its source is offered under the repository's
`MIT OR Apache-2.0` license declaration. FrontierLoop is distributed under the MIT
license in `LICENSE`; the original declaration and provenance are preserved at
`provenance/vibe-harness-runtime-0.3.2-draft/NOTICE.md`, and the original skill files and hashes are
included for traceability.

This package does not include Vibe Harness compiled runtime dependencies or binaries.

## Engineering workflow references added in 0.6.0

FrontierLoop 0.6.0 independently adapts workflow concepts from:

- `addyosmani/agent-skills` (MIT), including version-sensitive primary-source verification, public
  contract design, safe migration sequencing, and browser/retrieved-data trust boundaries.
  Copyright (c) 2025 Addy Osmani.
- `PrimeIntellect-ai/prime-agent` (MIT), specifically the concept of small evidence-backed continual
  harness refinement with local/global scope separation and rollback. Copyright (c) 2025 Mario Zechner;
  Copyright (c) 2026 Prime Intellect.
- A public refactoring-review Gist was consulted historically while exploring skeptical
  behavior-equivalence review. The current `pure-refactor` contract is independently written,
  does not reproduce that Gist, and the Gist is not a distribution dependency.

No executable code, runtime, daemon, Python-backed Skill package, credential handling, or session state from
those reference projects is bundled. FrontierLoop's active implementation remains instruction-only.
If future versions copy protectable upstream text or code, retain the applicable upstream license,
attribution, and NOTICE requirements.
