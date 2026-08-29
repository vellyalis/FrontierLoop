# FrontierLoop improvement evaluation

## What self-improvement means here

FrontierLoop can improve its own reviewed source, but it cannot grant itself authority. A useful failure or
successful tactic may become evidence, a proposal, an isolated prototype, a measured comparison, and—only
after explicit approval—a promoted installation. It never silently rewrites or reinstalls itself.

The improvement loop is:

```text
field observation
  -> proposal
  -> prototype approval
  -> preserved baseline + isolated candidate
  -> deterministic comparison
  -> repeated live Codex comparison when behavior is model-dependent
  -> promotion decision
  -> post-promotion field observation
  -> retain, revise, or roll back
```

Git remains the source of truth. Evaluation files are evidence, not a second state owner.

## Promotion claims

Every improvement proposal must declare one primary claim and its comparison class. Examples:

- a routing change reduces unnecessary specialist activation;
- a verification change reaches decisive evidence with fewer irrelevant checks;
- a safety boundary prevents an unapproved action;
- a migration workflow preserves old and new consumers;
- a packaging change makes release output reproducible.

Do not use one blended score to hide a regression. Track at least:

1. **Capability retention** — every baseline capability in scope still passes;
2. **Capability gain** — at least one declared capability or outcome newly passes;
3. **Hard guardrails** — permissions, data safety, rollback, one source of truth, and no automatic mutation;
4. **Automatic surface cost** — implicit Skill count and catalog bytes exposed to ordinary work;
5. **Behavior evidence** — routing and decisions under the same cases, model, CLI, instructions, and repetitions;
6. **Field evidence** — actual project outcomes after promotion when synthetic cases cannot prove usefulness.

For routing evidence, distinguish three questions instead of trusting one total score: were all required
capabilities selected, were unnecessary capabilities avoided, and was the exact minimal set selected? The
benchmark's expected set is the smallest non-redundant owner set, not every logically related method.

## Instruction-bundle claims

Treat `AGENTS.md`, Skill bodies and metadata, routing references, tool exposure, and relevant configuration
as one versioned Instruction Bundle. A shorter file, lower token count, cleaner prose, or passing schema check
is not by itself a behavioral improvement.

For any claimed instruction improvement:

1. preserve exact baseline and candidate bundles, their hashes or Git refs, and the complete diff;
2. measure the complete active instruction chain against the configured discovery limit and retain practical
   headroom for repository and nested instructions;
3. hold repository state, model and reasoning settings, tools, permissions, environment, prompts, and graders
   constant across matched representative tasks;
4. separate development cases from a locked holdout and later field or canary evidence; retain failed trials
   and subgroup or worst-case regressions;
5. gate safety and correctness first, then compare final Artifact quality, hard-task resolution, first-pass
   acceptance, stability, routing precision/recall, and only then cost;
6. evaluate compression or relocation as semantic preservation: every required capability must remain usable,
   not merely mentioned elsewhere;
7. for a first-principles claim, include both a genuinely hard positive case and a Routine negative case, and
   use ablation when premise reconstruction and another workflow change are bundled.

Judge the produced Artifact and observable decisions. Do not collect chain of thought, hidden reasoning, or
raw session transcripts. Promotion still requires the authority boundaries and rollback defined below.

## Evidence lanes

### Lane A — deterministic source comparison

Run from the FrontierLoop source repository:

```powershell
python -m pip install --requirement requirements-release.txt
python scripts/evaluate_frontierloop.py `
  --baseline-ref <preserved-baseline> `
  --candidate-ref <candidate> `
  --json-out evaluation/results/static-comparison.json `
  --markdown-out evaluation/results/static-comparison.md
```

This lane measures capability probes, retained-capability regressions, Skill inventory, implicit catalog
surface, routing-contract coverage, forbidden runtime files, and automatic-mutation boundaries.

### Lane B — repeated live Codex behavior

Run the same benchmark while each version is the sole active FrontierLoop source:

```powershell
python scripts/run_live_benchmark.py `
  --label baseline `
  --trials 3 `
  --output evaluation/results/live-baseline.json `
  --markdown-out evaluation/results/live-baseline.md

python scripts/run_live_benchmark.py `
  --label candidate `
  --trials 3 `
  --output evaluation/results/live-candidate.json `
  --markdown-out evaluation/results/live-candidate.md

python scripts/compare_live_benchmarks.py `
  --baseline evaluation/results/live-baseline.json `
  --candidate evaluation/results/live-candidate.json `
  --json-out evaluation/results/live-comparison.json `
  --markdown-out evaluation/results/live-comparison.md
```

The live runner is read-only, ephemeral, and uses one batch of fixed cases per trial. It stores only routing,
decision, and guardrail outputs—not chain of thought or raw session logs. Because model behavior is stochastic,
one trial is diagnostic only; promotion evidence requires at least three comparable trials.

### Lane C — post-promotion field evidence

Synthetic cases cannot prove that real project work became better. After promotion, collect only outcomes
already produced by real work:

- first meaningful implementation or discriminating experiment;
- unnecessary user questions before safe local work;
- irrelevant broad test runs;
- material defects caught or missed;
- rollback or recovery success;
- user-visible completion and residual risk.

Do not add telemetry, a watcher, database, hidden log, or background agent. Record field evidence in the
proposal or existing project handoff only when it changes the retain/revise/rollback decision.

## Adoption rule

A candidate is eligible for promotion only when all applicable conditions hold:

- every retained baseline capability passes in both baseline and candidate;
- all candidate hard guardrails pass;
- the declared candidate capability gain passes;
- live behavior has no critical safety violation;
- no live metric regresses beyond the declared tolerance;
- at least one decision-relevant live metric improves, unless the proposal is a pure safety fix whose
  reproduced failure is eliminated without behavioral regression;
- automatic surface growth is visible and justified rather than hidden;
- rollback is concrete and the active installation remains unchanged until approval.

Passing the benchmark does not force promotion. Failing it blocks promotion or narrows the claim.

## Metric-gaming guard

- Do not add marker text only to satisfy a capability probe; the matching behavior or contract must exist.
- Do not tune directly against the fixed live cases without adding held-out or field evidence for a material change.
- Do not reduce useful capability merely to lower context bytes or tool calls.
- Do not add rules, tests, or Skills solely to increase a count.
- If metrics and direct project outcomes disagree, direct outcomes win and the benchmark must be revised.

## Rollback and removal

Keep the preserved baseline ref and previous active installation until candidate verification completes.
Roll back when a critical guardrail fails, a retained capability regresses, or field evidence shows practical
degradation. Remove an evaluation case or metric when it no longer represents a real decision, duplicates a
stronger case, or encourages gaming without catching material failures.
