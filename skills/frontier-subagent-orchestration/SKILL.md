---
name: frontier-subagent-orchestration
description: "Use explicitly when independent read, exploration, falsification, testing, comparison, or disjoint write Workstreams can be delegated with unique ownership and integration boundaries. Pass relevant Engineering Change Gate decisions and unknowns; never parallelize conflicting mutable ownership or treat subagent self-assessment as acceptance."
---

# Subagent Orchestration Skill

## Codex plugin boundary

This active skill is adapted from the Vibe Harness workflow source. FrontierLoop has no
`vh.exe`, SQLite store, daemon, event ledger, or atomic state service. Treat legacy State/Event/
Ledger terms as logical evidence labels only; durable truth remains current repository files,
Git, nearest instructions, and an existing handoff when one is actually needed. Read
`../../references/RUNTIME_BOUNDARY.md` before claiming persistence, exactly-once behavior,
reviewer independence, or machine enforcement.

## Trigger

独立して分割可能なWorkstream、探索、読取、テスト、ログ解析、反証、比較を並列化する。

## Objective

並列性を品質と速度へ変換し、同一ファイル競合、文脈欠落、自己評価の無批判採用を防ぐ。

## Inputs

- Goal Invariants、Responsibility Map
- Candidate Type、Comparison Class
- Workstream Portfolio
- Expected output、Proof Obligations

## Preconditions

Subagentまたは独立Task capabilityが実際に利用可能で、Workstreamが独立し、書込Ownershipを分離できること。利用不能なら並列化を演じない。

## Default procedure

1. 独立Workstreamだけを分離する
2. 読取、探索、テスト、反証、比較を優先して並列化する
3. 同じファイルへの同時書込を禁止しOwnerを一意にする
4. 各WorkstreamへGoal、Constraints、Owner、Write Scope、依存、Proofに加え、MaterialなData／Owner／Lifetime、Module／Core、API／Contract、Observability、CleanupのDecision／Unknownを渡す
5. 生ログではなく判断に必要なEvidenceと要約を返させる
6. Parentは統合前にData、Responsibility、Module／Core、API／Contract、Tests、Observability、CleanupをRepository Truthと照合する
7. Creativityでは前提、構造、価値仮説を分岐させる

## Engineering Change Gate integration

各delegated packetには、そのWorkstreamにmaterialなData／Owner／Lifetime、Responsibility、Module／Core、API／Contract、Tests、Observability、Cleanupの決定と未知点を含める。SubagentはCanonical Data、Contract、State、実装の第二Ownerを発明せず、競合するOwner判断をEvidence付きでParentへ返す。Parentは統合前にこれら全Dimensionを共通GoalとRepository truthへ照合する。

## Decision criteria

独立性、競合可能性、Context completeness、統合可能性、反証価値。

## Allowed discretion

独立したRead-only調査は広く並列化してよい。書込はFile OwnershipとTransaction境界を満たす場合だけ許す。

## Escalation conditions

同一ファイル競合、責任境界衝突、Subagent間でGoal Modelが不一致、A2/A3の重大判断。

## Outputs

Workstream assignment、Evidence summary、Conflict report、Integrated decision。

## Optional evidence labels

WorkstreamStarted, FactDiscovered, VerificationRecorded, RiskDiscovered, WorkstreamCompleted

## Proof obligations

- No concurrent writes to the same mutable scope.
- Every Workstream has one unique owner and integration boundary.
- Relevant Engineering Change Gate decisions and unknowns are passed to the worker.
- Parent reconciliation covers Data, Responsibility, Module／Core, API／Contract, Tests, Observability, and Cleanup against repository truth.
- Subagent self-assessment never becomes acceptance or self-approval.

## Stop conditions

各WorkstreamのEvidenceが統合可能な形で返り、Conflictが解消または明示された時点。

## Failure recovery

競合時は書込を停止し、Ownerを再割当てする。分岐が同一案の言い換えなら仮説生成からやり直す。
