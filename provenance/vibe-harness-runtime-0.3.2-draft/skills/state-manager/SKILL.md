---
name: state-manager
description: "複数段階・複数Sessionの開発状態、判断、証拠、次の行動を一つの正本へ同期し、再開可能性を維持する。"
---

# State Manager Skill

## Trigger

- 複数段階・複数Session
- Exploration
- A2以上
- 重要判断、変更、検証、失敗
- Session開始・停止・再開

## Objective

Current Best、失敗知識、残存Risk、再開地点を自動維持し、ユーザーへ記録作業を要求しない。

## Inputs

- State Event
- Existing State / Ledgers
- Git / Repository / Verification

## Preconditions

Event envelopeとState schemaが検証可能であること。

## Default procedure

1. Eventを検証しSecretをRedactする
2. Processed Eventを確認する
3. Current State versionを確認する
4. 該当Stateだけを更新する
5. Schema validationする
6. Atomic commitする
7. Ledgerへappendする
8. Resume時はGitと照合する
9. 判断を変えない古い情報を圧縮する

## Decision criteria

次の判断、反証、復元、再開に必要か。コードやGitから再取得可能か。

## Allowed discretion

Routineの小変更は軽量Stateにできる。

## Escalation conditions

Source of Truth衝突、Branch混入、State改ざん、Migration失敗。

## Outputs

- Current State
- Ledgers
- Reconciliation report
- Resume summary

## State events

StateReconciled, SessionStopping, SessionStopped

## Proof obligations

State schema、Git整合、Event idempotency、Secret非保存。

## Stop conditions

EventがExactly-once相当で反映され、StateとLedgerが整合した時点。

## Failure recovery

Recovery Journalから再実行し、同じEventを二重適用しない。
