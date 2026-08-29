---
name: frontier-execution-cycle
description: "Use explicitly when a loaded workflow needs a finite Research-Plan-Do-Check-Act loop for multi-step implementation or exploration. frontier-core remains the work owner; preserve decision-bearing Engineering Change Gate state without turning Routine work into process ceremony."
---

# Execution Cycle Skill

## Codex plugin boundary

This active skill is adapted from the Vibe Harness workflow source. FrontierLoop has no
`vh.exe`, SQLite store, daemon, event ledger, or atomic state service. Treat legacy State/Event/
Ledger terms as logical evidence labels only; durable truth remains current repository files,
Git, nearest instructions, and an existing handoff when one is actually needed. Read
`../../references/RUNTIME_BOUNDARY.md` before claiming persistence, exactly-once behavior,
reviewer independence, or machine enforcement.

## Trigger

RoutineまたはExplorationで、Research、Plan、Do、Check、Actのいずれかを実行する。

## Objective

Goalを縮小せず、原文R-PDCAの判断密度を保ったまま、Routineでは短く、Explorationでは完全に実行する。

## Inputs

- Goal Model、Goal Invariants、Responsibility Map
- Current Best、Goal Gap、Current Bottleneck
- Workstream、Candidate Type、Comparison Class
- Evidence、Constraints、Verification Surface

## Preconditions

Task Modeが判定され、Current BestまたはBaselineを復元できること。

## Frontier Core integration

Execution Cycle is a finite reasoning method, not a second implementation owner. For every
non-trivial change, `frontier-core` owns the work and its Engineering Change Gate. The cycle
preserves decision-bearing Data, Responsibility, Module/Core, API, Verification, Observability,
and Cleanup state without turning each phase into a document.

## Default procedure

このSkillの有限R-PDCAを適用する。Routineでは判断に必要な項目だけを短い内部Passとして実行し、実装へ進む。Explorationでは採否を変えるResearch、仮説、比較Evidenceだけを明示する。Global `AGENTS.md`へのFrontierLoop導入を前提にしない。

- **Research** confirms the affected canonical data, owner, lifetime, current contract, and the smallest decision-relevant unknown.
- **Plan** chooses the responsibility-correct owner and vertical, plus proof, observability, recovery, and cleanup obligations.
- **Do** implements that bounded vertical; it does not add a clean parallel path while leaving divergent semantics behind.
- **Check** decides acceptance and material data-lifetime, contract, failure-visibility, and regression claims.
- **Act** adopts one canonical owner, completes consumer migration and cleanup, or records a real retained owner and exit condition. Then control returns to `frontier-core` or the narrow specialist.

## Reasoning control

- 追加調査は、その結果で変わり得る判断を一つ以上示せる場合だけ行う。
- Routineでは変更Owner、Acceptance、直接検証が判明したら実装へ進む。
- 可逆な反証実験を実行できる場合は、同じ前提の分析を延長せず実験する。
- 前提が反証された場合は、同じ推論を繰り返さず次のCycle境界でModeまたはEffortを再判定する。
- 未知性が解消したWork UnitはRoutineへ戻し、高いEffortを維持すること自体を品質とみなさない。
- Stop conditionsを満たした後は、未採用の局所案が残っていても分析を続けない。

## Decision criteria

Goal寄与、原因仮説の反証可能性、同条件比較、再現性、副作用、Workstreamの機会費用。

## Allowed discretion

Goal Invariants内でResearch深度、実験単位、Tool、評価方法を選択してよい。Routineでは、判断を変えない項目を文書化するためだけにCycleを拡張してはならない。

## Escalation conditions

Goal、責任境界、量化条件、Candidate Type、Global Bottleneckの変更が必要な場合。

## Outputs

- Research output
- Execution plan
- Candidate change
- Comparison evidence
- Act decision and State update

## Optional evidence labels

FactDiscovered, HypothesisCreated, CodeChanged, VerificationRecorded, CandidateAccepted, CandidateRejected, DecisionAccepted

## Proof obligations

検証可能な差分、Current Bestとの同条件比較、Responsibility-correctなOwner、MaterialなData／Contract／Observability／Cleanup、採否根拠、副作用、反証条件。

## Stop conditions

該当Workstreamの成功終了条件を満たすか、Portfolio Selectionで他Workstreamの限界価値が上回った時点。

## Failure recovery

Current Bestを失う可能性がある変更前に復元点を保存し、劣化時はRollbackする。同じ仮説を別表現で反復しない。
