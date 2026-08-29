---
name: execution-cycle
description: "実装と探索をResearch、Plan、Do、Check、Actの有限ループで進め、停滞時に前提や戦略を監査する。"
---

# Execution Cycle Skill

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

## Default procedure

常時Global AGENTSのR-PDCAを省略せず適用する。Routineでは必要な項目を短い内部Passとして実行し、Explorationでは各出力をStateへ明示する。

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

Goal Invariants内でResearch深度、実験単位、Tool、評価方法を選択してよい。ただし常時Global AGENTSの判定項目を要約によって消してはならない。

## Escalation conditions

Goal、責任境界、量化条件、Candidate Type、Global Bottleneckの変更が必要な場合。

## Outputs

- Research output
- Execution plan
- Candidate change
- Comparison evidence
- Act decision and State update

## State events

FactDiscovered, HypothesisCreated, CodeChanged, VerificationRecorded, CandidateAccepted, CandidateRejected, DecisionAccepted

## Proof obligations

検証可能な差分、Current Bestとの同条件比較、採否根拠、副作用、反証条件。

## Stop conditions

該当Workstreamの成功終了条件を満たすか、Portfolio Selectionで他Workstreamの限界価値が上回った時点。

## Failure recovery

Current Bestを失う可能性がある変更前に復元点を保存し、劣化時はRollbackする。同じ仮説を別表現で反復しない。
