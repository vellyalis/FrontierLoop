---
name: frontier-version-control
description: "Use explicitly when Git observation, checkpointing, worktree isolation, commit, push, PR, merge, tag, release, or recovery-point management is required. Preserve pre-existing dirty work and checkpoint only a responsibility-correct coherent vertical; remote publication and history changes remain separate approval boundaries."
---

# Version Control Skill

## Codex plugin boundary

This active skill is adapted from the Vibe Harness workflow source. FrontierLoop has no
`vh.exe`, SQLite store, daemon, event ledger, or atomic state service. Treat legacy State/Event/
Ledger terms as logical evidence labels only; durable truth remains current repository files,
Git, nearest instructions, and an existing handoff when one is actually needed. Read
`../../references/RUNTIME_BOUNDARY.md` before claiming persistence, exactly-once behavior,
reviewer independence, or machine enforcement.

## Trigger

- Git repository内でコード、設定、文書、Schemaを変更した
- 検証済みCurrent Bestを保存する
- 構造的実験、広いRefactor、削除、Migration、自動生成へ移る
- 採用ArchitectureまたはCurrent Bestを置き換える
- Sessionを停止、再開、またはHandoffする
- Commit、Push、Issue、Pull Request、Tag、Release、Mergeを検討する

## Objective

検証済み成果を復元可能なCheckpointとして保存しつつ、ユーザーの既存差分、Scope外変更、秘密情報、Local設定、再配布不能AssetをVersion Controlへ混入させない。IssueやPull Requestを進捗儀式にせず、必要な協調境界だけを作る。

## Inputs

- Goal Model、Task Scope、Acceptance Criteria
- Git status、diff、branch、worktree、HEAD、remote、upstream
- Project-local commit / branch / protected-branch policy
- Verification result、Current Best、Recovery requirement
- Secret scan、file ownership / provenance classification

## Preconditions

- Repository root、現在のBranch、Worktreeを一意に特定できる
- 今回のTask Scopeと、開始前から存在するDirty stateを区別できる
- Commit対象の変更がユーザーの既存差分か今回のTaskで作成した差分かを判定できる
- 外部Remote操作では承認またはProject Policyによる事前許可を確認できる

## Default procedure

1. `status`, `diff`, `branch`, `worktree`, `HEAD`, `remote`, `upstream`を観測し`GitStatusObserved`を記録する
2. Dirty pathを`task_scope`, `preexisting_user_change`, `secret`, `local_config`, `generated_evidence`, `unredistributable_asset`, `unknown`へ分類する
3. Checkpointが必要かを、復元価値、次の変更の破壊性、Session境界、Current Best更新から判定する
4. Commit前に対象成果の必要なVerificationが完了していることを確認する
5. Stage対象を明示的Allowlistで選び、Scope外差分と危険分類を除外する
6. Checkpoint one reviewable responsibility-correct coherent vertical, including required consumer migration and Cleanup, or explicit migration coexistence with its owner and removal condition.
7. Commit後にhash、committed diff、remaining dirty state、HEAD整合を再確認する
8. `CheckpointCreated`を発行し、既存HandoffのCheckpoint／Verification／Recovery Pointを、再開に必要な場合だけ更新する
9. Push等のRemote反映はProject Policyと承認境界を評価し、target remote / branch / commitが一意な場合だけ実行する
10. Issue / Pull Requestは追跡、外部調整、Review、Merge境界に実価値がある場合だけ作成する

## Engineering Change Gate integration

Reviewable Checkpointは一つのresponsibility-correct coherent verticalであり、必要なConsumer migration、Verification、Observability、Cleanupを同じ成果へ含める。新しいCanonical Pathだけを保存し、divergentな旧Pathを残した状態を完成Checkpointとしない。実在するContractが共存を要求する場合だけ、明示Migration Owner、Compatibility boundary、Removal conditionを持つCheckpointとして扱う。

## Decision criteria

- CheckpointがCurrent Best、検証済み成果、Migration前状態、Handoffの復元価値を持つか
- Commit対象が今回のTask Scopeへ追跡できるか
- 変更が必要なVerificationを通過しているか
- 一つのCommitが一つの成果または責任変更としてReview可能か
- Remote操作の対象、影響、権限、承認が一意か
- Issue / Pull Requestが実際の追跡または協調コストを下げるか

## Allowed discretion

- Project Policyが`auto_local_checkpoint=true`なら、Scope内の検証済みD1 Local Commitを自律実行してよい
- Repository規約がない場合はConventional Commitsの適切なtypeとscopeを選択してよい
- Session停止時に検証済みCheckpointへできない作業は、Commitせず既存Handoff、Patch、明示承認されたStash、またはBackupの最も安全な方法で保存してよい
- Pull Request本文、Commit body、Issue本文はEvidence PackとStateから必要情報を自動生成してよい

## Escalation conditions

- Dirty pathの所有者またはScopeを一意に判定できない
- Secret、Token、秘密鍵、個人情報、Local-only設定の混入候補がある
- protected branchへの直接反映、force push、履歴改変、公開済みCommitの書換えが必要
- remote、branch、upstream、publish対象Commitが曖昧
- ユーザーの未完成差分を移動、破棄、上書きする可能性がある
- Repository policyとGoalまたは安全境界が衝突する

## Outputs

- Git observation / path classification report
- Local Checkpoint commit hashまたはCheckpoint rejection reason
- Commit messageとVerification summary
- Remaining dirty state
- Remote publish decision / result
- 必要な場合だけIssueまたはPull Request成果物

## Optional evidence labels

GitStatusObserved, CheckpointRequested, CheckpointCreated, CheckpointRejected, RemotePublishRequested, RemotePublishCompleted, RemotePublishRejected

## Proof obligations

- Stageされた全pathがTask Scopeへ追跡できる
- Secret、Local-only設定、ユーザー既存差分、再配布不能AssetがCommitへ含まれない
- Checkpointの成果と必要なVerificationが対応する
- Commit後のhash、diff、remaining dirty stateが観測済み
- Remote publishは明示承認または事前許可Policy、非protected target、non-force条件を満たす
- Issue / Pull Request作成には追跡または協調上の価値がある
- A checkpoint does not claim replacement complete while a divergent superseded runtime path remains without an explicit migration owner and removal condition.


## Stop conditions

- 必要な検証済み成果が復元可能なCheckpointになった、またはCommitしない合理的理由とRecovery Pointが既存HandoffまたはDelivery evidenceへ残った
- Scope外差分と危険情報がVersion Control成果物から除外された
- Remote反映が不要ならLocal Checkpoint後に終了する
- Remote反映を行った場合はtracking stateと対象Commit hashを確認した
- Issue / Pull Requestに実価値がなければ作成せず終了する

## Failure recovery

- Commit前失敗ではIndexを安全に復元し、ユーザー既存差分を変更しない
- Commit後の検証不一致ではCommitを公開せず、follow-up修正または安全なLocal rollbackを選ぶ
- Remote publishの部分失敗ではRemote stateを再取得し、同一Commitの重複送信を防ぐ
- 公開済みCommitの修正は明示許可がない限り履歴改変ではなくFollow-up Commitで行う
- Secret混入を検出した場合はPublishを停止し、履歴状態を隔離し、Rotationと影響確認をSecurity ReviewへEscalateする
