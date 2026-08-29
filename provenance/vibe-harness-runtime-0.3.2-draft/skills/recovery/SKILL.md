---
name: recovery
description: "Crash、中断、State不整合、Git不確定状態を検出し、重複副作用なしでResume、Rollback、Reconcileする。"
---

# Recovery Skill

## Trigger

Crash、中断、State drift、失敗Command、回帰、Migration失敗、再開。

## Objective

Current Bestを失わず、安全に復旧し、重複作業を避ける。

## Inputs

- Recovery Journal
- State snapshot
- Git / Worktree
- Failed command / verification

## Preconditions

破壊的操作前のRecovery Pointがあること。

## Default procedure

1. Project / Branch / Worktree identityを確認する
2. 未完了TransactionとEventを特定する
3. Stateと実体をReconcileする
4. ResumeかRollbackかをEvidenceで選ぶ
5. 同じEventの二重適用を防ぐ
6. Verification baselineへ戻す
7. Failure causeと再発条件を記録する
8. Next Actionを再計算する

## Decision criteria

Data safety、Current Best保持、可逆性、復旧コスト、再現性。

## Allowed discretion

局所的で安全なRetryは自動実行できる。

## Escalation conditions

Data loss、Branch conflict、価値・Scope衝突、Rollback不能。

## Outputs

Recovery report、Reconciled State、Next Action。

## State events

RollbackExecuted, StateReconciled, SessionStarted

## Proof obligations

State / Git整合、Verification baseline、二重適用なし。

## Stop conditions

安全なVerified stateへ戻り、次のActionが確定した時点。

## Failure recovery

Recovery自体が失敗した場合は変更を停止し、SnapshotとEvidenceを保持して承認境界へ上げる。
