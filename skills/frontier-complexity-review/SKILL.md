---
name: frontier-complexity-review
description: "EXPLICIT-ONLY COMPLEXITY ADMISSION REVIEW. Use ONLY when the user names $frontier-complexity-review or an already-loaded FrontierLoop workflow explicitly hands off a still-material complexity-admission decision. Do not auto-select it merely because a prompt proposes a service, abstraction, cache, or other complexity: frontier-core or frontier-architecture should reject an obviously unnecessary mechanism directly."
---

# Complexity Review Skill

## Codex plugin boundary

This active skill is adapted from the Vibe Harness workflow source. FrontierLoop has no
`vh.exe`, SQLite store, daemon, event ledger, or atomic state service. Treat legacy State/Event/
Ledger terms as logical evidence labels only; durable truth remains current repository files,
Git, nearest instructions, and an existing handoff when one is actually needed. Read
`../../references/RUNTIME_BOUNDARY.md` before claiming persistence, exactly-once behavior,
reviewer independence, or machine enforcement.

## Trigger

- The user explicitly names `$frontier-complexity-review`; or
- an already-loaded workflow hands off a material admission decision that remains unresolved after the
  simplest valid alternative was considered.

The mere presence of a proposed Dependency, Service, Storage layer, abstraction, Plugin, cache, worker,
concurrency owner, configuration surface, large file, or speculative framework is **not** an automatic
trigger. Let `frontier-core` or `frontier-architecture` reject it directly when the simpler answer is clear.

## Objective

現在のGoalへ追跡できない複雑性を防ぎ、必要な複雑性だけを明示的に所有する。

## Inputs

- Proposed change
- Goal / Requirement / Risk
- Existing alternatives

## Preconditions

追加要素とSimplest Valid Alternativeを比較できること。

## Default procedure

1. 現在のRequirementまたはRiskを特定する
2. 既存機能、標準機能、局所実装を調べる
3. Simplest Valid Alternativeを作る
4. 代替が不足する観測証拠を示す
5. Runtime、運用、障害、認知、Test、Security costを列挙する
6. Owner、Monitoring、Failure Mode、Rollback、Removal conditionを定義する
7. Accept / Defer / Reject / Replaceを決める
8. Repositoryが既にArchitecture Health Gateを持つ場合だけBaseline差分を確認し、上限引上げや新規例外を通常解決として採用しない。このReviewのためだけにGateを新設しない
9. `utils/common/helpers/shared`名のModuleは明示Admission、安定Invariant、実在する2消費者なしにRejectする
10. 新規Reusable Abstractionは既存の具体Consumer 2件以上、またはPublic／ABI／Security境界の明示例外なしにRejectする

## Decision criteria

現在の必要性、総複雑性、可逆性、所有可能性、証拠。

## Allowed discretion

Goalを同等に満たす候補からより単純なものを選んでよい。

## Escalation conditions

運用者不在、Rollback不能、費用・権限・外部依存が発生する場合。

## Outputs

templates/complexity-receipt.md。

## Optional evidence labels

DecisionProposed, DecisionAccepted, DecisionRejected, DependencyChanged

## Proof obligations

Requirement traceability、Alternative failure evidence、Removal path。
構造変更ではActual／Limit、Owner、依存方向、下方Ratchetまたは例外拒否のEvidence。
Repositoryが既に`architecture/maintainability-baseline.json`等を所有する場合はGeneric module admissionとReusable abstraction exceptionをそこへ記録する。そうでなければComplexity Receiptへ記録し、新しい台帳を作らない。Machine GateはPath存在とConsumer数など客観事実だけを検査する。
Semantic Debtの新規追加、独立Change Reasonの隠蔽、Raw I/O Baselineの増加を通常解決としてAcceptしてはならない。

## Stop conditions

Decisionと再検討条件が確定した時点。

## Failure recovery

証明が崩れた場合はDeferまたはRemoveし、Current Bestを復元する。
