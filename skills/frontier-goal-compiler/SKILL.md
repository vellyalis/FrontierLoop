---
name: frontier-goal-compiler
description: "Explicit-only: turn materially ambiguous goals, acceptance, scope, or product trade-offs into observable success. Do not ask users to choose technical placement."
---

# Goal Compiler Skill


## Trigger

Explicit user invocation or a material workflow handoff for unresolved goals, acceptance, scope, or product trade-offs. Not a clear feature request merely because it is new.

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
2. Success / Failure ConditionsとForbidden Stateを作る
3. Scope / Non-Scope / Constraints / Approval Boundariesを定義する
4. GoalがData／StateをMaterialに変更または制約する場合だけ、Affected Data／StateのSource、Canonical Owner、Lifetime、Invalidation、Required Invariant、Forbidden Stateを整理する
5. 暗黙要件をHypothesisとして分離する
6. User、System、Environment、External ContractのResponsibility Mapを作る
7. Acceptance CriteriaをUser-visibleかつ観測可能にする
8. Generalization Requirementを明示する
9. 技術的なModule／Core／API配置はRepositoryとEvidenceからAgentが判断し、Userへ丸投げしない
10. 価値判断だけをClosed Questionにする
11. 複数段階・複数Sessionで再開に必要な場合だけ、既存のRepository HandoffまたはTask記録へ保存する
12. Goalが実装可能になったら、非自明な変更を`$frontier-core`へ渡し、Material Boundary変更だけを`$frontier-architecture`へ追加Routingする


## Frontier Core handoff

Goal Compilerは実現すべき状態を所有し、実装構造を所有しない。TechnicalなModule、Core、API配置は
Repository EvidenceからAgentが導き、UserへはValue／Product decisionだけを確認する。GoalとAcceptanceが
実行可能になったら、非自明な実装を`$frontier-core`へ戻す。MaterialなOwnership、Lifecycle、Core／Module、
Dependency Direction、Public Contract、Storage、Failure／Recovery boundary decisionだけを
`$frontier-architecture`へ追加Routingする。
## Decision criteria

設計案の採否、Proof Obligation、完成判定をGoal Modelから導けるか。

## Allowed discretion

技術手段、内部構造、検証方法はGoal Invariants内で選択してよい。

## Escalation conditions

同価値の相互排他的方向、費用・Privacy・UX、Goal Invariant変更。

## Outputs

templates/goal-model.mdに適合するGoal Model。

## Optional evidence labels

GoalInterpreted, GoalChanged, DecisionProposed

## Proof obligations

Acceptanceが観測可能であり、Affected DataとInvariant、Forbidden State、User責任とAgent責任が分離され、技術配置をUserへ丸投げしていないこと。

## Stop conditions

設計・実装・完成判定に必要な情報が揃った時点。文章の精緻化自体を続けない。

## Failure recovery

不明点を勝手にFactへ昇格せず、AssumptionとFalsification Conditionを残す。
