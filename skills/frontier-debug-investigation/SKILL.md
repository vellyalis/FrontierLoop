---
name: frontier-debug-investigation
description: "Use alongside frontier-core when a defect cause is unknown, intermittent, multi-layer, recurring, environment-sensitive, or prior fixes failed. This specialist supplements and never replaces frontier-core. For a race, timing, shutdown, cancellation, ordering, or lifetime defect whose owner or causal ordering is not yet proven, actually read the shared Engineering Judgment reference before the final investigation decision. Build a reproduction boundary, competing causal hypotheses, discriminating experiments, and a minimal mechanism-level fix. Do not use when the cause and local fix are already clear."
---

# Debug Investigation Skill

## Codex plugin boundary

This active skill is adapted from the Vibe Harness workflow source. FrontierLoop has no
`vh.exe`, SQLite store, daemon, event ledger, or atomic state service. Treat legacy State/Event/
Ledger terms as logical evidence labels only; durable truth remains current repository files,
Git, nearest instructions, and an existing handoff when one is actually needed. Read
`../../references/RUNTIME_BOUNDARY.md` before claiming persistence, exactly-once behavior,
reviewer independence, or machine enforcement.

## Trigger

- 原因が不明または複数layerにまたがる
- intermittent、race、timing、environment-dependent、data-dependent
- 一度以上の修正が失敗した
- symptomを抑えるfallback/retryしか案がない
- crash、deadlock、corruption、performance regression、protocol mismatch
- logと実際の挙動が矛盾する

## Objective

症状へ場当たり的な変更を重ねず、故障Mechanismを識別できる最小実験を繰り返し、
Current Bestを壊さない最小の原因修正へ収束する。

## Shared engineering judgment

Read [`../frontier-core/references/ENGINEERING_JUDGMENT.md`](../frontier-core/references/ENGINEERING_JUDGMENT.md) when a suspected
fix would add or change a state owner, cache, scan, polling loop, retry, delay, background task, fallback,
invalidation rule, or lifetime boundary. Use INVESTIGATE until a discriminating observation identifies the
authoritative state and causal mechanism; do not admit a compensating mechanism merely because it suppresses
the visible symptom.

Also read the shared Doctrine before the investigation decision itself when the defect is a race, timing,
shutdown, cancellation, ordering, or lifetime problem and the responsible owner/order is still unknown.
That uncertainty is already a positive concurrency/lifetime trigger; do not wait until a proposed fix adds
a new mechanism before applying the Doctrine.

## Inputs

- user-visible symptom and impact
- expected vs actual behavior
- environment, revision, data, timing, frequency
- relevant code/config/log/trace/dump
- recent changes and known good baseline
- verification and recovery boundary
- Context Manifest when multi-stage or high-impact

## Failure Model

Separate:

- **Symptom**: observed wrong behavior
- **Trigger**: event/input that exposes it
- **Precondition**: hidden state required for it
- **Mechanism**: causal chain producing it
- **Impact**: user/system consequence
- **Detection**: how it becomes observable
- **Containment**: temporary limit on harm, not a claimed fix

## Default Procedure

1. **Bound the incident**
   - Identify affected versions, environments, data, frequency, and impact.
   - Protect data and preserve evidence before invasive experiments.

2. **Reproduce or constrain**
   - Build the smallest reliable reproduction when feasible.
   - If not reproducible, bound the failure statistically or through trace/correlation.
   - Record a known-good comparison.

3. **Verify observation quality**
   - Confirm clocks, log levels, sampling, truncation, buffering, symbol/source revision,
     and instrumentation side effects.
   - Do not reason from stale or mismatched artifacts.

4. **Build a ranked hypothesis ledger**
   Each hypothesis includes:
   - proposed mechanism;
   - supporting and contradicting evidence;
   - true/false observation;
   - cheapest high-information experiment;
   - affected layer and owner.

5. **Run discriminating experiments**
   Prefer:
   - binary search/bisection;
   - differential comparison;
   - controlled input/environment changes;
   - trace/counter/invariant instrumentation;
   - failure injection;
   - deterministic scheduler/replay where available;
   - minimal reproduction or reference model.

   Change one causal variable at a time unless the fix is inherently atomic.

6. **Localize ownership**
   Determine whether the defect belongs to input, system, platform, dependency,
   integration contract, state migration, or observation layer. Do not move a
   structural defect to user configuration.

7. **Implement the smallest causal fix**
   - Repair the violated invariant or ownership boundary.
   - Avoid suppressing the symptom, swallowing errors, broad retries, arbitrary delays,
     cache flushes, or fallback proliferation unless they are the verified mechanism.
   - Preserve compatibility and recovery.

8. **Verify**
   - Original reproduction fails before and passes after.
   - Known-good behavior remains.
   - Boundary and high-impact recurrence conditions are covered.
   - Instrumentation confirms the mechanism where feasible.
   - Performance/resource/security side effects are checked as relevant.

9. **Capture failure knowledge**
   Record cause, trigger, precondition, reproduction, fix, rejected hypotheses,
   regression evidence, and conditions that would refute the conclusion.

## Investigation Economy

- 最も安い境界観測でOwnerを分離し、全Layerへ一度にInstrumentationを追加しない。
- Active hypothesisは次の識別実験を変えるものだけ残し、同じ観測を予測する案はまとめるか保留する。
- 高情報量で安全な実験が実行可能になったら、追加Log読取、一般調査、仮説列挙より先に実行する。
- 恒久的Telemetry、Retry基盤、Fallback、Watchdog、Cache invalidation、Debug UIは、局所Instrumentationで現在の原因を判定できないEvidenceがある場合だけ検討する。
- 診断中に広いRefactor、Cleanup、API再設計を行わない。Mechanismが局所化したら`$frontier-routine-change`または`$frontier-architecture`へ移し、調査Skillを終了する。
- 「完全なRoot Cause説明」ではなく、採用判断と再発防止に必要な因果水準まで到達したら停止する。

## Intermittent Failure Rules

- Record frequency and confidence; do not call one passing run a fix.
- Prefer event correlation, deterministic replay, stress amplification, and
  invariant monitoring over arbitrary repetition.
- Separate absence of observation from evidence of absence.
- Stop a stress loop when it can no longer change the decision.

## Proof Obligations

- symptom and expected behavior are precise;
- revision/environment identity is known;
- evidence is fresh and matched to the running artifact;
- causal hypothesis was discriminated, not merely narrated;
- fix addresses the mechanism;
- original failure boundary and material regressions are verified;
- residual uncertainty and recurrence conditions are explicit.

## Stop Conditions

Stop when the causal mechanism is sufficiently supported, the minimal fix passes
the original and material regression boundaries, no material Global defect remains,
and additional investigation would not change adoption.

## Failure Recovery

- If an experiment damages Current Best, roll back immediately and preserve evidence.
- If two attempts repeat the same strategy without information gain, audit the
  representation, instrumentation, data path, and oracle.
- If evidence conflicts, freeze conclusions and design a discriminating experiment.
- If the environment cannot reproduce, provide a bounded diagnostic build or
  observation plan without claiming resolution.
