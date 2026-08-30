# FrontierLoop Plugin 0.8.4

## Install from Git

FrontierLoop is designed to be installed from its canonical Git checkout, not by
linking `~/.agents/skills` directly to the repository or cache.

~~~powershell
git clone https://github.com/vellyalis/FrontierLoop.git "$env:USERPROFILE\plugins\frontier-loop"
cd "$env:USERPROFILE\plugins\frontier-loop"
git checkout v0.8.4
pwsh .\scripts\Verify-FrontierLoop.ps1 -Root .
pwsh .\scripts\Install-FrontierLoop.ps1 `
  -Source . `
  -DestinationRoot "$env:USERPROFILE\.codex\plugins\cache\personal\frontier-loop" `
  -UserSkillRoot "$env:USERPROFILE\.agents\skills"
~~~

For the recommended paired installation with Native UI Governance and the matching
global `AGENTS.md`, use `vellyalis/dpkr-agent-suite`. The suite preserves these
individual repositories as the canonical plugin owners and only orchestrates install/update.

Both Codex and Taddkorro are first-class targets. `.codex-plugin/plugin.json` is the
Codex plugin manifest, `taddkorro.plugin.json` declares the Taddkorro plugin/Skill root,
and the installer materializes the same canonical Skill bodies into `~/.agents/skills`
for the shared runtime catalog. These are registrations of one source, not duplicate
Skill owners.

FrontierLoop contains 23 development skills:

- one self-contained implicit `frontier-core` for routine work and universal guardrails;
- six narrow implicit specialists for architecture, debugging, security, performance, uncertainty, and recovery;
- sixteen explicit-only specialists, including `frontier-migration` for persisted/public contract changes.

Every non-trivial change passes the lightweight Engineering Change Gate, and all 23 canonical Skills are available while only seven are implicit.

Structural changes conditionally load `skills/frontier-core/references/ENGINEERING_JUDGMENT.md`. Its FOUNDATION, REDUCTION, and
REALITY lenses establish the authoritative state and lifetime, remove unnecessary mechanisms, and prove real
runtime cost. New caches, scans, polling loops, workers, queues, retries, fallbacks, and compatibility paths
must satisfy an explicit ownership, activation, stopping, cost, invalidation, failure, observability, and
removal contract. This reference is not another Skill or router, so Routine work stays direct.

Project-specific Fast/Targeted/Subsystem/Full feedback routing remains an on-demand verification lane.
Claimed pure refactors remain an on-demand review-governance equivalence gate. Neither expands the implicit set.

## Approval-gated evolution

`frontier-core` may guide a written improvement proposal, but FrontierLoop never automatically modifies its
source, installed plugin, skill catalog, marketplace entry, or any `AGENTS.md`. Prototype, promotion, and
publication are separate approval boundaries. The detailed process is loaded only while improving
FrontierLoop itself.

Promotion is evidence-gated. `evaluation/improvement-benchmark.json` checks retained and new capabilities,
guardrails, implicit catalog cost, and routing coverage. The fixed live benchmark compares the old and new
active plugin under the same Codex environment for at least three trials before a behavioral promotion claim.
Instruction-bundle claims additionally preserve exact active chains, compare matched final artifacts, keep
holdout and subgroup regressions visible, and judge safety and correctness before cost or compression.

Engineering-judgment changes also use independent read-only activation probes. Each probe runs in a fresh
Codex session, records only successful `SKILL.md` and canonical doctrine reads from execution events, and
retains a small structured decision rather than reasoning or a raw transcript. Routine copy/rename cases
must avoid structural specialists, while canonical-owner, stale-state, continuous-scan, performance, debug,
and migration cases must load the narrow required owners. Critical cases are hard-gated per trial rather
than hidden inside an aggregate score.

## Windows / Taddkorro installation topology

The authoring tree is the canonical source. A verified versioned cache is the installed snapshot, and
`~/.agents/skills/frontier-*` is a materialized discovery copy of the selected cache version. User Skill
directories must not be junctions into the cache: Taddkorro can advertise those paths while refusing to read
the resolved `SKILL.md` outside the instruction-resolution boundary. The installer therefore copies and
byte-verifies each Skill inside `~/.agents/skills`, transactionally migrates recognized legacy FrontierLoop
junctions, and fails closed on foreign directories or arbitrary links.

Runtime activation remains lazy. Catalog metadata is not activation proof: non-trivial work loads
`frontier-core`, a positive structural trigger also loads its Engineering Judgment reference, and only the
nearest triggered specialist is added. Mechanical micro-edits retain the no-body-load fast path.

## Source provenance

FrontierLoop contains adaptations of a user-supplied Vibe Harness devkit snapshot. The active runtime does
not load, install, or ship the upstream Skill copies. The current repository keeps only developer-facing
provenance metadata and the upstream notice under `provenance/vibe-harness-devkit-0.3.2-draft/`, while
`references/SKILL_SOURCE_MAP.json` records the upstream file hashes and their active FrontierLoop mappings.

For an exact copy of the historical upstream Skill snapshot, use Git tag `v0.8.2` and the path
`provenance/vibe-harness-runtime-0.3.2-draft/skills`. Keeping the full snapshot in Git history preserves
auditability without making it part of the normal install cache or release payload.

## Evaluation

Static evaluation and dry-run planning are local and use only Python 3.11+ standard-library code:

~~~text
python scripts/evaluate_frontierloop.py --root . --user-skills-root "%USERPROFILE%\.agents\skills" --json-out evaluation/results/current-static.json --markdown-out evaluation/results/current-static.md
python scripts/evaluate_frontierloop.py --root . --baseline-root "C:\path\to\baseline" --json-out evaluation/results/baseline-candidate-static.json --markdown-out evaluation/results/baseline-candidate-static.md
python scripts/run_live_benchmark.py --root . --dry-run --label candidate --trials 3 --output evaluation/results/candidate-live-plan.json --markdown-out evaluation/results/candidate-live-plan.md
python scripts/run_engineering_judgment_activation.py --root . --cwd evaluation/results/probe-workspace --trials 3 --trace-dir evaluation/results/activation-traces/candidate --output evaluation/results/engineering-activation-candidate.json --label candidate
python scripts/evaluate_engineering_judgment_live.py --baseline-batch evaluation/results/live-baseline.json --candidate-batch evaluation/results/live-candidate.json --baseline-activation evaluation/results/engineering-activation-baseline.json --candidate-activation evaluation/results/engineering-activation-candidate.json --json-out evaluation/results/engineering-judgment-live-gate.json --markdown-out evaluation/results/engineering-judgment-live-gate.md
~~~

Live execution is never automatic. It sends the deterministic prompt to the explicitly configured model command:

~~~text
python scripts/run_live_benchmark.py --root . --label candidate --trials 3 --command "model-cli --json" --output evaluation/results/candidate-live.json --markdown-out evaluation/results/candidate-live.md
~~~

Compare completed live result sets without allowing a blended score to hide capability or guardrail regressions:

~~~text
python scripts/compare_live_benchmarks.py --baseline evaluation/results/baseline-live.json --candidate evaluation/results/candidate-live.json --json-out evaluation/results/live-comparison.json --markdown-out evaluation/results/live-comparison.md
~~~

## Invocation

Most tasks need no skill name. For explicit workflows:

```text
Use $frontier-migration to move this schema through compatible phases.
Use $frontier-deep-engineering for a gated hard problem that requires first-principles reconstruction.
Use $frontier-complexity-review before adding this service.
Use $frontier-independent-review for a fresh defect search on this high-impact change.
Use $frontier-evidence-pack to prepare the final delivery and continuation evidence.
```

See `references/ROUTING_MATRIX.md`, `skills/frontier-core/references/ENGINEERING_JUDGMENT.md`,
`references/RUNTIME_BOUNDARY.md`, and `references/ASSURANCE_LEVELS.md`.

## Verification behavior

Routine changes implement first and use the smallest decisive existing check without a separate verification
plan or receipt. FrontierLoop uses no fixed test/production ratio. Material new infrastructure, expensive
suites, high-impact proof, migrations, or data-integrity boundaries receive only the rationale needed to
change a decision.
