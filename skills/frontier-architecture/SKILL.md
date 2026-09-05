---
name: frontier-architecture
description: "Resolve material ownership, lifetime, module, dependency, public-contract, or deployment decisions. Not unchanged-boundary performance work or schema coexistence already owned by migration."
---

# Architecture Skill


## Trigger

新規Project、主要境界、Data Flow、公開API、Storage、Deployment方式の変更。
Canonical State／LifetimeのOwner、Core／Module配置、Dependency Direction、Failure Recoveryを実質的に変える、またはそれらの重要な未知点を判断する場合。
これらが不変と確認済みのData Flow／性能Mechanism変更はPerformanceが所有できる。既存OwnerのSchema共存はMigrationが所有でき、語彙の重複だけでArchitectureを追加しない。
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
5. 新規複雑性が必要なら、最小案の不足とOwnerを示す
6. 継続判断に必要な重要Decisionだけ既存記録へ残す。局所変更のためにReceiptやADRを必須化しない
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

Recovering an existing tangled ownership boundary: read [the focused lane](references/boundary-recovery.md).

## Public contract lane

Changing an observable API, command, schema, or external contract: read [the focused lane](references/public-contract.md).

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
