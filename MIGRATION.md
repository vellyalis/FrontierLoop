# Migration to FrontierLoop 0.6.0

## From 0.5.1

- The implicit skill set remains seven; ordinary task routing is unchanged.
- `frontier-migration` is a new explicit-only workflow. It does not auto-activate for ordinary edits.
- `frontier-core` now forbids automatic self-modification and separates proposal, prototype, promotion, and publication authority.
- Version-sensitive framework/protocol work can use a primary-source lane through explicit context compilation.
- Public contracts, retrieved/browser data, and runtime experience proof have tighter boundaries.
- Local 0.4 project-feedback routing is retained inside explicit `frontier-verification`; existing
  `frontier-flow` managed blocks can be updated in place rather than duplicated.
- Local 0.4 pure-refactor review is retained inside explicit `frontier-review-governance` with
  `true | false | not_proven` verdicts against an explicit base.
- Total skills increase from 22 to 23; explicit-only specialists increase from 15 to 16.

Reinstall or update the plugin, verify the exact installed source, and open a new Codex session. Existing
GlobalSkills fallback remains exclusive with Plugin activation.

## From 0.5.0 and earlier

0.5.1 removed fixed production/test ratios, added a routine no-paperwork fast path, and hardened transactional
Personal Plugin migration. 0.5.0 replaced router-only activation with a self-contained core and six narrow
implicit specialists.

FrontierLoop still includes no `vh.exe`, Rust runtime, SQLite, Mission/Session/Operation database, daemon,
hooks, event ledger, exactly-once claim, global `AGENTS.md` replacement, or second lifecycle owner.
