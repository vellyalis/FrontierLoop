---
name: intake
description: "新しい開発依頼の開始時にRepositoryを調査し、安全に推論できる事実を集め、不要な質問をせず次のSkillへルーティングする。"
---

# Intake Skill

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

## Default procedure

1. Repository root、言語、Framework、Package managerを検出する
2. Build、Test、Lint、Run方法を既存設定から推定する
3. 既存Goal、Architecture、Stateを探す
4. ユーザーのGoalと重要条件を抽出する
5. 不足情報を事実・仮説・価値判断に分ける
6. Goal Compilerへ渡す
7. 技術質問ではなく価値判断だけをClosed Question候補にする

## Decision criteria

- 安全に推論可能か
- 回答でGoalまたは責任境界が変わるか
- Repository調査で解消可能か

## Allowed discretion

可逆なDefault、既存Convention、標準Toolの選択はHarnessが決めてよい。

## Escalation conditions

外部送信、費用、Privacy、Goal変更、不可逆操作が必要な場合。

## Outputs

- Intake summary
- Repository profile
- Facts / hypotheses / uncertainties
- Goal Compiler input

## State events

IntakeReceived, FactDiscovered, RiskDiscovered

## Proof obligations

Repository profileが実ファイルと整合し、ユーザーへ技術選択を丸投げしていないこと。

## Stop conditions

Goal Compilerが開始でき、残る質問が価値判断に限定された時点。

## Failure recovery

検出不能なCommandは未確定として記録し、一般的Commandを勝手に実行せず既存設定を追加調査する。
