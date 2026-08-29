---
name: subagent-orchestration
description: "複数AgentのWork Unit、所有権、Write Scope、依存、合流を設計し、同一箇所の競合を防ぐ。"
---

# Subagent Orchestration Skill

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

Workstreamが独立し、書込Ownershipを分離できること。

## Default procedure

1. 独立Workstreamだけを分離する
2. 読取、探索、テスト、反証、比較を優先して並列化する
3. 同じファイルへの同時書込を禁止しOwnerを一意にする
4. Goal Invariants、責任境界、候補型、期待出力、Proofを渡す
5. 生ログではなく判断に必要なEvidenceと要約を返させる
6. Parentが共通Goal ModelとVerification Surfaceで統合する
7. Creativityでは前提、構造、価値仮説を分岐させる

## Decision criteria

独立性、競合可能性、Context completeness、統合可能性、反証価値。

## Allowed discretion

独立したRead-only調査は広く並列化してよい。書込はFile OwnershipとTransaction境界を満たす場合だけ許す。

## Escalation conditions

同一ファイル競合、責任境界衝突、Subagent間でGoal Modelが不一致、A2/A3の重大判断。

## Outputs

Workstream assignment、Evidence summary、Conflict report、Integrated decision。

## State events

WorkstreamStarted, FactDiscovered, VerificationRecorded, RiskDiscovered, WorkstreamCompleted

## Proof obligations

同時書込なし、必要Context伝達、Parentによる独立統合、自己評価の非採用。

## Stop conditions

各WorkstreamのEvidenceが統合可能な形で返り、Conflictが解消または明示された時点。

## Failure recovery

競合時は書込を停止し、Ownerを再割当てする。分岐が同一案の言い換えなら仮説生成からやり直す。
