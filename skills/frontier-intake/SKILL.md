---
name: frontier-intake
description: "Use explicitly when repository, Goal, acceptance, affected owner, or safe-next-action context is materially unknown. Inspect only facts and data/ownership unknowns that can change routing or implementation, then hand clear work to $frontier-core or material Goal ambiguity to $frontier-goal-compiler. Do not use as an automatic prerequisite or ceremony for every task."
---

# Intake Skill

## Codex plugin boundary

This active skill is adapted from the Vibe Harness workflow source. FrontierLoop has no
`vh.exe`, SQLite store, daemon, event ledger, or atomic state service. Treat legacy State/Event/
Ledger terms as logical evidence labels only; durable truth remains current repository files,
Git, nearest instructions, and an existing handoff when one is actually needed. Read
`../../references/RUNTIME_BOUNDARY.md` before claiming persistence, exactly-once behavior,
reviewer independence, or machine enforcement.

## Trigger

- 新しい依頼を受けた
- Repositoryの状態が不明
- ユーザーが目的だけを伝えた

## Objective

依頼を止めずに開始可能な情報を自動収集し、技術知識をユーザーへ要求しない。

## Inputs

- ユーザーの自然言語
- Repository metadata
- 既存README、AGENTS、設定、Package manifest

## Preconditions

RepositoryへのRead access。存在しないProjectでは空Projectとして扱う。

## Frontier Core handoff

Intakeは実装を所有せず、明確になったFactsを`$frontier-core`へ渡してEngineering Change Gateを免除しない。
Routingまたは実装判断を変えるMaterialなOwnership、Lifecycle、Core／Module、Public API／Contractの
uncertaintyだけを`$frontier-architecture`へ追加Routingする。Routine workのために別Plan文書を作らない。

## Default procedure

1. Repository root、言語、Framework、Package managerを検出する
2. Build、Test、Lint、Run方法を既存設定から推定する
3. 既存Goal、Architecture、Current State、Applicable Instructionsを探す
4. ユーザーのGoal、重要条件、観測可能なAcceptanceを抽出する
5. Routingまたは実装判断を変え得る場合だけ、Materialな対象Data／StateのSource、Canonical Owner、Lifetime、Invalidationと変更Responsibilityの未知を特定する
6. 不足情報をFact、Hypothesis、Technical Unknown、Value Decisionへ分離する
7. GoalまたはAcceptanceがMaterialに曖昧な場合だけ`$frontier-goal-compiler`へ渡す。明確ならFactsとUnknownsを`$frontier-core`へ渡す
8. Ownership、Lifecycle、Core／Module、Public Contract等のMaterial Boundaryが未解決なら、`$frontier-core`を主Ownerとしたまま`$frontier-architecture`へ追加Routingする
9. Repositoryから解ける技術質問をUserへ返さず、残る価値判断だけをClosed Question候補にする


## Decision criteria

- 安全に推論可能か
- 回答でGoalまたは責任境界が変わるか
- Repository調査で解消可能か

## Allowed discretion

可逆なDefault、既存Convention、標準Toolの選択はCodex agentが決めてよい。

## Escalation conditions

外部送信、費用、Privacy、Goal変更、不可逆操作が必要な場合。

## Outputs

- Intake summary and repository profile
- Facts / hypotheses / technical unknowns / value decisions
- Routingまたは実装判断に影響するData／Ownership unknowns
- Selected next owner: `$frontier-core`, or `$frontier-goal-compiler` while material Goal ambiguity remains
- Material boundary uncertaintyへの追加`$frontier-architecture` routing（必要時のみ）

Routine workのために独立したPlan文書を作らない。
## Optional evidence labels

IntakeReceived, FactDiscovered, RiskDiscovered

## Proof obligations

Repository profileが実ファイルと整合し、ユーザーへ技術選択を丸投げしていないこと。

## Stop conditions

`frontier-core`または必要時のGoal Compilerが開始でき、残る質問が価値判断に限定された時点。Intake自体は実装Ownerにならない。

## Failure recovery

検出不能なCommandは未確定として記録し、一般的Commandを勝手に実行せず既存設定を追加調査する。
