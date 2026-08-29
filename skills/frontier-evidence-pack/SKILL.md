---
name: frontier-evidence-pack
description: "Use explicitly when final delivery, review, user acceptance, or a real session boundary requires a compact non-engineer-readable evidence packet. Preserve Engineering Change Gate decisions, proof, NotRun work, residual risk, and recovery without creating a document for every Routine change."
---

# Evidence Pack Skill

## Codex plugin boundary

This active skill is adapted from the Vibe Harness workflow source. FrontierLoop has no
`vh.exe`, SQLite store, daemon, event ledger, or atomic state service. Treat legacy State/Event/
Ledger terms as logical evidence labels only; durable truth remains current repository files,
Git, nearest instructions, and an existing handoff when one is actually needed. Read
`../../references/RUNTIME_BOUNDARY.md` before claiming persistence, exactly-once behavior,
reviewer independence, or machine enforcement.

## Trigger

作業完了、レビュー依頼、Session停止、User acceptance。

## Objective

コードを読めないユーザーへ、価値、動作、証拠、Risk、復元方法を明確に渡す。

## Inputs

- Goal Model
- Changes
- Decision-bearing Engineering Change Gate summary
- Verification
- Complexity Receipts
- Residual risks
- Current repository state or existing handoff when needed

## Preconditions

未解決のAdjudicated BLOCK、必須Proof、未処理Eventが確認されていること。Finding総数はCompletion条件にしない。

## Default procedure

1. Goalと重要条件を示す
2. 実際に変わった挙動と変えていない範囲を示す
3. Requirement → Design → Implementation → Evidenceを接続する
4. 非自明な変更ではData、Responsibility、Module／Core、API／Contract、Tests、Observability、Cleanup、Evidence、Residual Riskを要約する
5. Verification結果をPass / Partial / NotRunで示す
6. 追加複雑性と理由を示す
7. Residual riskと未確認条件を示す
8. Rollback / Recoveryを示す
9. Userが使用感として確認する点だけを示す
10. Current repository stateとNext Actionを示す

## Engineering Change Gate integration

非自明な変更では、Delivery EvidenceへData、Responsibility、Module／Core、API／Contract、Tests、Observability、Cleanup、Evidence、Residual Riskのcompact summaryを一つ含める。各項目は実装判断と直接証拠へ結び、Missing proofを説明文で成功へ変換しない。Behavior、Data、Contract、Owner、Lifetime、Boundaryを変えないmicro-editはexpanded summaryを要求しない。

## Decision criteria

専門知識なしで完成・Risk・次の判断を理解できるか。

## Allowed discretion

技術詳細は折りたたみ可能な補足へ送ってよい。

## Escalation conditions

重大未検証Risk、秘密情報混入、Goal未達。

## Outputs

templates/evidence-pack.mdに適合するDelivery Evidence。

## Optional evidence labels

EvidenceGenerated, SessionStopping

## Proof obligations

MaterialなEngineering Change Summaryが直接Evidenceまたは明示的NotRunへTraceし、Missing proofを文章で成功扱いせず、Secret redactionが保たれること。

## Stop conditions

Userが価値判断と使用感を確認でき、技術判断を要求されない時点。

## Failure recovery

証拠不足を文章で埋めず、IncompleteとしてVerificationへ戻す。
