---
name: exploration
description: "原因・要求・設計に未知性がある課題で、構造的に異なる仮説を比較しCurrent Bestを更新する。"
---

# Exploration Skill

## Trigger

原因・解法・評価・Architectureに重要な未知性がある課題。

## Objective

局所調整に沈まず、仮説・反証・比較によってCurrent Bestを更新する。

## Inputs

- Goal Model
- Current Best Registry
- Workstreams
- Evidence / Constraints

## Preconditions

Goal Invariantsと比較条件を定義できること。

## Default procedure

1. Current Bestを復元・再現する
2. Goal GapとGlobal / Local Bottleneckを分ける
3. 成功例、失敗例、制約、評価方法を調査する
4. 構造的に異なる仮説を生成する
5. True / False時の観測、採否基準、副作用を定義する
6. Goalを縮小せず最小実験を作る
7. Current Bestと同条件比較する
8. 採用・棄却・保留を記録する
9. Portfolio Selectionする
10. 2回停滞したStrategyを監査する

## Decision criteria

観測差、再現性、Goal寄与、副作用、機会費用。

## Allowed discretion

Goal Invariants内で仮説、Tool、実験順、評価方法を再設計してよい。

## Escalation conditions

Goal、価値、Scope、責任境界を変える必要がある場合。

## Outputs

- Candidate / experiment
- Comparison evidence
- Updated Current Best / Ledger
- Next Experiment

## State events

HypothesisCreated, CandidateAccepted, CandidateRejected, VerificationRecorded

## Proof obligations

Current Bestとの同条件比較、反証可能性、失敗知識の保存。

## Stop conditions

Workstreamの成功終了条件を満たすか、限界価値が他Workstream以下になった時点。

## Failure recovery

同じ仮説を言い換えて反復せず、Strategy Auditへ移る。
