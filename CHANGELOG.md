# Changelog

## 0.8.4 - 2026-08-30

- Removed one-off 0.7.0 -> 0.8.0 acceptance/comparison tooling from current main after its historical
  evidence was preserved by Git. Current evaluation remains owned by the generic static/live benchmark,
  activation, comparison, source-map, and release tools documented in `README.md`.
- Removed the obsolete 0.6.0 migration note and the empty third-party requirements placeholder; historical
  migration facts remain in this changelog and the evaluation stack continues to use Python 3.11+ standard
  library only.
- Removed the redundant release-version copy from `SKILL_SOURCE_MAP.json`; the map now owns only provenance,
  mapping, and hashes while Codex/Taddkorro manifests own release version identity.
- Kept current evaluation cases, deterministic release tooling, Codex activation evidence, transactional
  installation, and all 23 active Skill contracts unchanged.

## 0.8.3 - 2026-08-30

- Reduced Vibe Harness provenance to a developer-only notice and source-map metadata instead of carrying a
  duplicate upstream Skill tree in the current source and runtime install surface.
- Preserved the exact historical upstream Skill snapshot in Git tag `v0.8.2` and recorded its path in
  `references/SKILL_SOURCE_MAP.json` so provenance remains auditable without polluting normal distribution.
- Excluded `provenance/` from versioned install caches and deterministic release archives, with focused tests
  preventing future packaging regressions.

## 0.8.2 - 2026-08-29

- Fixed Codex Personal Marketplace path resolution: local plugin paths are resolved from the configured marketplace root, not from `.agents/plugins/marketplace.json` itself.
- Added a fail-closed marketplace-layout contract so Codex and Taddkorro share the same canonical authoring source without a second plugin owner.

## 0.8.1 - 2026-08-29

- Made Git checkouts first-class installation sources by explicitly excluding `.git/`
  from installed caches, source equivalence, and release payload semantics.
- Added first-class `taddkorro.plugin.json`, public Git distribution metadata,
  portable evaluation paths, root licensing, and a Taddkorro/Codex paired-suite path.
- Preserved all 23 Skill bodies and the 7 implicit / 16 explicit routing split from 0.8.0.

## Unreleased

- Added matched read-only engineering-judgment activation probes that require successful Skill-body and
  canonical-doctrine reads, preserve no reasoning transcript, hard-gate critical cases per trial, and prove
  that routine edits do not activate structural specialists.
- Added a Codex final-message wrapper that records only bounded activation evidence, plus a dedicated live
  gate for canonical ownership, stale-state removal, on-demand versus continuous scanning, measured
  performance, causal debugging, and compatible migration decisions.
- Repaired Taddkorro body activation on Windows by replacing `~/.agents/skills/frontier-*` junctions with
  byte-verified materialized Skill directories. Legacy managed junctions migrate transactionally, arbitrary
  links and foreign directories fail closed, and rollback restores the previous topology.
- Documented and verified the lazy Taddkorro activation boundary: catalog discovery does not prove body load,
  structural work must read the canonical Engineering Judgment body, specialists load only on their concrete
  trigger, and behavior-neutral micro-edits remain lightweight.

## 0.8.0 - 2026-08-29

- Added one conditional shared Engineering Judgment Doctrine with ordered FOUNDATION, REDUCTION, and REALITY
  lenses, current-evidence precedence, explicit decision states, and a mechanism-admission contract.
- Wired the doctrine into `frontier-core`, architecture, debugging, performance, and migration without adding
  a Skill, router, runtime owner, daemon, database, or implicit catalog entry.
- Added deterministic capability coverage and a live always-on-scan case that requires an authoritative,
  on-demand alternative while preserving the 23-Skill / seven-implicit routing surface.
- Extended source verification to require the shared doctrine wiring and exact mapped active-Skill hashes.
- Reconciled pre-existing stale provenance hashes with the unchanged active Skill files so future drift now
  fails closed instead of being silently accepted.
- Made static evaluation fail when live-case capability/decision vocabularies drift from the response schema.

## 0.7.0 - 2026-08-28

- Replaced the global fixed verification-volume proposal with proportional, decision-relevant verification.
- Added artifact-first Instruction Bundle evaluation with exact baselines, matched trials, holdout evidence,
  active-chain headroom, semantic-preservation checks, and explicit rollback and promotion boundaries.
- Added a hard-only first-principles lane inside the existing explicit `frontier-deep-engineering` owner;
  no new Skill or implicit routing surface was added.

- Added Engineering Change Gate continuity across the full Skill catalog and evidence handoffs.
- Exposed all 23 canonical Skills for user-level discovery while retaining exactly seven implicit Skills.
- Added bounded Core/module placement judgment and existing-architecture recovery without repository-wide rewrites.
- Added static evaluation, live dry-run, benchmark comparison tooling, and a fixed 22-case response schema.
- Added deterministic release building, source verification, and a transactional installer with source/prior-version link upgrades and rollback.
- Added global Skill fallback guidance and corrected FrontierLoop Skill IDs without automatic global replacement.

## 0.6.0 - 2026-08-11

- Added approval-gated FrontierLoop evolution: proposal, isolated prototype, promotion, and publication
  are separate authority boundaries; no automatic self-modification or `AGENTS.md` mutation exists.
- Added source-only improvement proposals plus an on-demand governance reference and proposal template.
- Added explicit-only `frontier-migration` for compatible schema, persisted-format, configuration,
  registration, identity, and public-contract migrations.
- Added a version-sensitive primary-source lane to context compilation without forcing research on routine
  or version-independent work.
- Added a public-contract lane for boundary validation, additive evolution, predictable errors, and migration handoff.
- Hardened browser, retrieved-content, runtime-experience, focus, credential, and untrusted-data boundaries.
- Preserved the local 0.4 feedback-flow and pure-refactor work as on-demand lanes inside existing
  verification and review-governance skills, without increasing the skill count or implicit surface.
- Added deterministic baseline/candidate capability and guardrail comparison, a fixed 16-case repeated live
  Codex benchmark, a comparison gate, and a post-promotion field-evidence contract for measurable improvement.
- Split live routing evidence into required-capability recall and unnecessary-capability precision, and used
  the first failed comparison to tighten multi-boundary architecture/security routing before promotion.
- Kept the implicit skill set at seven and added no daemon, watcher, scheduler, database, runtime, MCP server,
  automatic installer, or second state owner.


## 0.5.1 - 2026-08-05

- Removed fixed and advisory production-to-test ratios from active workflow decisions.
- Added a no-paperwork routine verification fast path so clear changes implement first and use the
  smallest decisive existing check.
- Restricted verification rationale to material new infrastructure, expensive suites, high-impact
  proof, or genuinely undecidable coverage gaps.
- Added anti-gaming rules against deleting required tests, inflating production code, or collapsing
  independent failures to satisfy a metric.
- Added release validation that prevents ratio rules from reappearing in active skills.
- Fixed migration from legacy marketplace IDs by removing every installed `frontier-loop@*` registration
  transactionally and restoring the prior IDs and files on failure.
- Made verification fail on duplicate Codex registrations, wrong Personal Plugin source paths, and
  installed-file SHA-256 drift.
- Added an exact Windows installation smoke for migration, rollback, uninstall, and GlobalSkills fallback.

## 0.5.0 - 2026-08-05

- Replaced the router-only activation model with a self-contained implicit `frontier-core`.
- Enabled six narrow specialists for direct implicit selection: architecture, debugging, security,
  performance, frontier portfolio, and recovery.
- Kept the remaining 15 specialist workflows explicit-only to avoid context and process inflation.
- Added deterministic release building, structural validation, checksums, a release manifest, and
  Windows setup/update/verify/uninstall wrappers.
- Added GitHub Actions validation and tag-based draft Release packaging.
- Added a documented Plugin-first path and exclusive direct-skill compatibility fallback.
- Kept all 20 Vibe Harness-derived workflows and provenance while retaining the no-runtime boundary.
- Continued to avoid any global `AGENTS.md` mutation.

## 0.4.0 - 2026-08-04

- Restored all 20 Vibe Harness workflow skills from the uploaded 0.3.2 draft.
- Namespaced active skills as `frontier-*` to avoid collisions in the global user skill catalog.
- Added one implicit `frontier-router`; made all 21 specialist skills explicit-only.
- Kept `frontier-portfolio` as the decisive-evaluator / two-workstream specialist.
- Replaced runtime-only State Manager and Recovery semantics with Git/repository/handoff procedures.
- Removed global `AGENTS.md` mutation, `vh.exe`, SQLite, hooks, Mission DB, and duplicate lifecycle ownership.
