---
name: frontier-routine-change
description: "Explicit-only handoff helper for a clear local change. Core remains owner; ordinary routine or micro-edit requests do not activate this helper."
---

# Routine Change Skill


## Trigger

- The user explicitly names `$frontier-routine-change`; or
- an already-loaded FrontierLoop workflow explicitly hands off a clear local change to it.

A clear, Routine, local, or micro-edit user request by itself is **not** a trigger. In that case keep
`frontier-core` as the sole owner and do not load this Skill.

## Objective

Goalを満たす最小のResponsibility-correctなVerticalを実装し、既存StructureはOwner、Invariant、
Lifecycle、Dependency Directionが正しい場合だけ保持する。
## Inputs

- Goal / Acceptance
- Relevant code
- Existing tests / conventions

## Preconditions

Routine判定とAssurance判定が済んでいること。

## Frontier Core integration

`$frontier-core` remains the end-to-end owner for every non-trivial Routine change. Routine classification
never waives Data, Responsibility, Module, Core, API, Verification, Observability, or Cleanup judgment;
keep answers brief and inline when obvious. Preserve existing structure only when its owner and dependency
direction are responsibility-correct. A nearest-file or fewest-line patch in the wrong owner is not minimal.
Escalate only a material independent responsibility, canonical owner, state lifecycle／invalidation, Core
placement, dependency direction, public contract, storage, or failure／recovery boundary decision to
`$frontier-architecture`; implementation ownership stays with `$frontier-core`.
## Default procedure

1. 要求または不具合を確認・再現する
2. 現在すでに満たしていないか確認する
3. No Change、設定、既存機能を検討する
4. 変更Surfaceを限定する
5. Affected Data、Canonical Owner、Lifetime、Invalidationと変更Responsibilityを短く確認する
6. 既存Core／Platform能力を再利用するか、Feature内へ置くかを判断し、投機的Core化を避ける
7. Existing StructureとConventionがResponsibility-correctなら従う。間違ったOwnerへの局所Patchで温存しない
8. Independent Responsibility、Canonical Owner、State Lifecycle／Invalidation、Core Placement、Dependency Direction、Public Contract、Storage、Failure／Recovery BoundaryがMaterialに変わるなら、そのBoundaryだけ`$frontier-architecture`へ渡し、`$frontier-core`をend-to-end ownerに保つ
9. 行数は注意信号にすぎない。分割はResponsibility、Change Reason、I/O、Public Surface、Test Seamで判断する
10. Repositoryに既存のArchitecture Healthまたはsemantic metadata policyがある場合だけ従う。Routine変更のために新しいRegistryやBaselineを作らない
11. 最小のResponsibility-correctなVerticalを実装する
12. 変更挙動、Data／ContractのMaterial Boundary、Failure Visibilityを検証する
13. 置換した旧経路、Fallback、Flag、重複Helper、Obsolete Testを削除し、残す場合はOwnerとExit Conditionを示す
14. 明白に不要な複雑性はCore内で却下する。最小案の比較後も重要な採否判断が未解決の場合だけ`$frontier-complexity-review`へ明示的に渡す
15. Evidenceを更新し、再開に必要な場合だけ既存Handoffを更新する


## Decision criteria

Goalを満たす最小のResponsibility-correctなVerticalか。DataとInvariantが正しいOwnerにあり、無関係な変更や不必要な旧経路がないか。

## Allowed discretion

局所的で可逆な実装詳細は自律選択してよい。

## Escalation conditions

既存ArchitectureがGoal達成を阻害する、新規複雑性が必須、A2/A3のRisk。

## Outputs

実装、Verification Evidence、MaterialなPlacement／Cleanup Decision、必要時だけContinuation。
## Optional evidence labels

CodeChanged, CommandExecuted, VerificationRecorded, CandidateAccepted

## Proof obligations

Acceptance、Affected Data／Invariant、変更Responsibility、主要Failure Visibility、Cleanup、Materialな回帰境界。

## Stop conditions

必須Proofが閉じ、Scope外変更がなく、必要なEvidenceとHandoffが整合した時点。

## Failure recovery

明白な回帰はRollbackし、最小の失敗原因を記録する。
