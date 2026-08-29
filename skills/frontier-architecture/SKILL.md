---
name: frontier-architecture
description: "Use and actually read alongside frontier-core when a software change materially introduces or alters ownership, canonical state or lifetime, data flow, Core or module placement, dependency direction, public API or contract, storage, deployment, failure recovery, or an independent responsibility inside a growing file. Replacing stale cached, scanned, or mirrored state with a direct authoritative read is a material data-flow trigger even when the canonical owner remains unchanged. For any Core-vs-feature placement decision, after loading this Skill always read the shared Engineering Judgment reference before the final decision, including when rejecting the proposed move. This specialist supplements and never replaces frontier-core. Explicitly carry the public-contract lane for a new API, command, schema, or persisted format, except when an explicit frontier-migration already owns coexistence of that same unchanged-owner schema or format and no independent architecture boundary changes. Combine with frontier-security-review when auth, permissions, or a trust boundary is also changed. Do not use for cohesive local edits or line-count-only refactors."
---

# Architecture Skill

## Codex plugin boundary

This active skill is adapted from the Vibe Harness workflow source. FrontierLoop has no
`vh.exe`, SQLite store, daemon, event ledger, or atomic state service. Treat legacy State/Event/
Ledger terms as logical evidence labels only; durable truth remains current repository files,
Git, nearest instructions, and an existing handoff when one is actually needed. Read
`../../references/RUNTIME_BOUNDARY.md` before claiming persistence, exactly-once behavior,
reviewer independence, or machine enforcement.

## Trigger

新規Project、主要境界、Data Flow、公開API、Storage、Deployment方式の変更。
Canonical State／LifetimeのOwner、Core／Module配置、Dependency Direction、Failure Recoveryを実質的に変える場合。
既存Grandfathered Fileへ新しいApplication Service、State Lifecycle、Failure Boundaryを追加する場合、または
絡み合った既存境界を一つのCanonical Ownerへ段階的かつboundedに回復する場合。

## Objective

Goalを満たすSimplest Valid Architectureを選び、技術判断を非エンジニアへ返さない。

## Shared engineering judgment

For a material ownership, state, lifetime, invalidation, boundary, or mechanism decision, read
[`../frontier-core/references/ENGINEERING_JUDGMENT.md`](../frontier-core/references/ENGINEERING_JUDGMENT.md). Architecture applies
FOUNDATION before proposing a new owner, module, state holder, API, or persistence shape, then REDUCTION to
remove duplicate writers, mirrored state, pass-through layers, speculative frameworks, and indefinite old/new
paths. Frontier Core remains the Work Unit owner.

Core-versus-feature placement is always a positive Doctrine-read trigger once this Skill is loaded. Do not
skip the shared Doctrine because the final answer is to reject a speculative Core promotion.

## Inputs

- Goal Model
- Constraints
- Existing architecture
- Repository profile

## Preconditions

A current major use case and responsibility map must be available. If the repository does not already
have them, derive the smallest sufficient map from current source, contracts, runtime behavior, and real
consumers. Do not ask a non-engineer to supply technical ownership, module placement, or dependency
analysis that can be determined from the repository. Do not create a permanent architecture registry
merely to satisfy this precondition.

## Default procedure

1. Responsibility MapとData Flowを作る
2. Simplest Valid Baselineを作る
3. 必要な場合だけ構造的に異なる代替案を作る
4. Goal適合、可逆性、運用負荷、障害点、Security、検証容易性で比較する
5. 新規複雑性へReceiptを作る
6. 推奨案と却下案・再検討条件をADRへ残す
7. Userには価値トレードオフだけを確認する
8. Repositoryが既にArchitecture Health／maintainability baselineを所有する場合だけ変更前後を比較する。このSkillを満たすためだけに新しいRegistryやGateを作らない
9. 新規SourceまたはModuleではOwner、Responsibility、Change Reason、I/O boundary、Public surface、Focused test seamをコード構造または既存設計記録から判断可能にする。別Metadata台帳を必須にしない
10. Dependency directionとOwner hopはGoal、既存Architecture、故障分離に合わせて最小化する。特定のLayer modelや3-4境界を全Repositoryへ強制しない
11. 既存Debtを残す場合は、Repositoryの既存Debt管理があればReasonとExit conditionを記録し、なければDelivery evidenceで増減と残存Riskを明示する

## Core and module placement lane

Use this lane when a material decision concerns canonical state, Core versus feature-module placement, or
dependency direction.

- Map the canonical state, invariants, owner, lifetime, mutators, consumers, I/O, and failure recovery
  before moving code. A physical helper location must not become a second semantic owner.
- Keep feature behavior with the module that owns its change reason, state, lifecycle, and test seam.
- Place policy or primitives in Core only for at least two real consumers or a hard public, ABI, security,
  canonical-state, or dependency boundary. Reject speculative reuse and aesthetic symmetry.
- An obvious speculative Core promotion can be rejected directly by Frontier Core; Architecture is needed
  when the placement decision materially changes an actual module/owner/dependency boundary. Do not load the
  explicit-only `frontier-complexity-review` merely to confirm an obvious speculative rejection.
- Direct dependencies toward the canonical policy and state owner. Keep adapters and side effects at their
  owned boundary without forcing a universal layer count or repository-wide rewrite.
- Leave a large but cohesive module intact. Extract only an independently ownable responsibility and move
  its real callers, tests, observability, and cleanup obligations with it.

## Existing-system boundary recovery lane

Use bounded recovery when ownership, state writes, side effects, and dependency direction are already
tangled. This is not authority for an omnibus cleanup.

1. Inventory the real entry points, callers, state readers and writers, side effects, contracts, tests,
   observability, and recovery behavior for one bounded responsibility.
2. Choose one canonical owner and the smallest slice whose callers, contract, verification, and rollback
   can move together.
3. Introduce a seam only when it removes owner ambiguity or reverses a harmful dependency. Route real
   consumers through it and prove success and failure behavior before cutover.
4. Cut over to the canonical owner and remove the superseded runtime path in the same bounded transition,
   or use an explicit migration with a removal condition when active contracts prevent that.
5. Stop when that boundary is responsibility-correct. Report neighboring debt without rewriting it, and
   never retain indefinite dual ownership as a compatibility fallback.

## Public contract lane

Apply this lane when a change affects an API, MCP/ACP/Tauri command, plugin manifest, persisted file,
configuration shape, database schema, event format, or another observable boundary.

- Define typed or otherwise machine-checkable input, output, error, ordering, idempotency, and lifecycle
  behavior before changing the implementation.
- Treat every observable behavior as a potential dependency. Avoid exposing internal paths, provider
  details, timing assumptions, raw exceptions, or mutable implementation state unless they are intended
  contract.
- Validate untrusted input and third-party responses at the boundary. Do not scatter duplicate validation
  through already-typed internal code.
- Prefer additive optional fields and compatible readers/writers. Do not rename, remove, or reinterpret an
  existing field in place merely because the new shape is cleaner.
- Keep error semantics predictable and sanitized across the boundary; separate machine-readable identity
  from human explanation.
- When old and new consumers must coexist, hand the change to the explicit `$frontier-migration` workflow
  instead of hiding migration inside the architecture edit.
- Record the compatibility promise, deprecation trigger, rollback or forward-repair path, and the exact
  observation that proves old and new consumers remain safe.

Do not create API versioning, pagination, an adapter, or a migration framework without a current consumer
or failure that requires it.

## Decision criteria

Goal適合、責任分離、Failure recovery、総複雑性、現在の制約。

## Allowed discretion

内部技術選定は既存ConventionとEvidenceに基づき自律選択してよい。

## Escalation conditions

費用、Privacy、Vendor lock-in、不可逆Migration、製品価値が変わる場合。

## Outputs

Architecture Decision、Data Flow、Complexity Receipts、Failure / Recovery。

## Optional evidence labels

DecisionProposed, DecisionAccepted, ArchitectureChanged, RiskDiscovered

## Proof obligations

Simplest Valid Alternativeとの比較、Failure Mode、Rollback。
Source責任を変更する場合はOwner、File／Module Boundary、依存方向、およびRepositoryが既に持つ場合だけArchitecture Health結果。
Line数は注意信号であり、分割はResponsibility、Change Reason、I/O境界、Public Surface、Test Seam、Owner Hopで正当化する。
Machine Gateがある場合も客観事実だけに限定し、単一責任・認知負荷・Traceabilityの意味判断はEvidenceへ残す。

## Stop conditions

選択理由と再検討条件がEvidence付きで確定した時点。

## Failure recovery

前提が崩れた場合はADRを上書きせず、新Decisionとして記録する。
