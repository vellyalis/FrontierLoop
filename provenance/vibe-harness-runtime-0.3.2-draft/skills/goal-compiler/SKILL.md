---
name: goal-compiler
description: "曖昧な依頼をGoal、Acceptance、制約、責任境界、反証条件へ変換し、実装可能なWork Unitを作る。"
---

# Goal Compiler Skill

## Trigger

- 曖昧な依頼
- 新規機能・製品方向
- Acceptanceが不明
- GoalまたはScopeが変化した

## Objective

ユーザーの言葉を、実装・比較・完成判定が可能なGoal Modelへ変換する。

## Inputs

- Intake summary
- ユーザーの最新確定指示
- Project constraints
- 既存Goal Model

## Preconditions

事実、仮説、不確実性を区別できること。

## Default procedure

1. Subject、User、Context、Desired Valueを抽出する
2. Success / Failure Conditionsを作る
3. Scope / Non-Scope / Constraintsを定義する
4. 暗黙要件を仮説として分離する
5. Responsibility Mapを作る
6. Acceptance Criteriaを観測可能にする
7. Generalization Requirementを明示する
8. 価値判断だけをClosed Questionにする
9. Stateへ保存する

## Decision criteria

設計案の採否、Proof Obligation、完成判定をGoal Modelから導けるか。

## Allowed discretion

技術手段、内部構造、検証方法はGoal Invariants内で選択してよい。

## Escalation conditions

同価値の相互排他的方向、費用・Privacy・UX、Goal Invariant変更。

## Outputs

templates/goal-model.mdに適合するGoal Model。

## State events

GoalInterpreted, GoalChanged, DecisionProposed

## Proof obligations

Acceptanceが観測可能であり、User責任とHarness責任が分離されていること。

## Stop conditions

設計・実装・完成判定に必要な情報が揃った時点。文章の精緻化自体を続けない。

## Failure recovery

不明点を勝手にFactへ昇格せず、AssumptionとFalsification Conditionを残す。
