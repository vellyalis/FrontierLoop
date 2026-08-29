---
name: routine-change
description: "原因と解法が明確な小変更を、既存構造を保つ最小の有効差分と必要十分な検証で完了する。"
---

# Routine Change Skill

## Trigger

Goal、解法、変更Surface、評価方法が概ね明確な変更。

## Objective

既存構造を壊さず、最小の有効差分で素早く完成させる。

## Inputs

- Goal / Acceptance
- Relevant code
- Existing tests / conventions

## Preconditions

Routine判定とAssurance判定が済んでいること。

## Default procedure

1. 要求または不具合を確認・再現する
2. 現在すでに満たしていないか確認する
3. No Change、設定、既存機能を検討する
4. 変更Surfaceを限定する
5. 既存ArchitectureとConventionに従う
6. Grandfathered Fileを変更する場合は、局所責任内で非増加かを確認し、新責任または成長が必要ならArchitectureへ昇格する
7. 800行超過はArchitecture注意閾値として確認し、Line数だけで分割しない
8. 新規Sourceを作る場合はOwned semantic metadataを同時に追加し、Legacy inventoryへ逃がさない
9. 最小差分を実装する
10. 変更挙動と高影響境界を検証する
11. Complexity GateとArchitecture Healthを通す
12. StateとEvidenceを更新する

## Decision criteria

Goalを満たす最小差分か。無関係な変更がないか。

## Allowed discretion

局所的で可逆な実装詳細は自律選択してよい。

## Escalation conditions

既存ArchitectureがGoal達成を阻害する、新規複雑性が必須、A2/A3のRisk。

## Outputs

- Minimal diff
- Verification result
- Lightweight Evidence
- Updated State

## State events

CodeChanged, CommandExecuted, VerificationRecorded, CandidateAccepted

## Proof obligations

Acceptance、変更挙動、高影響境界。

## Stop conditions

必須Proofが閉じ、Scope外変更がなく、State Syncが完了した時点。

## Failure recovery

明白な回帰はRollbackし、最小の失敗原因を記録する。
