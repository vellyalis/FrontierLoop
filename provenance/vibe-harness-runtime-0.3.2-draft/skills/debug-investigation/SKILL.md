---
name: debug-investigation
description: "原因不明・断続的・多層・再発する不具合を、再現境界、仮説Ledger、識別実験、計測、最小修正、回帰証拠で因果的に解く。"
---

# Debug Investigation Skill

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
- 診断中に広いRefactor、Cleanup、API再設計を行わない。Mechanismが局所化したら`routine-change`または`architecture`へ移し、調査Skillを終了する。
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
