---
name: frontier-evidence-pack
description: "Explicit-only: prepare a compact delivery or acceptance packet when the user or a real handoff needs it. Not a mandatory report format for every change."
---

# Evidence Pack Skill


## Trigger

Explicit user invocation or a material workflow handoff for a requested delivery/acceptance packet or real session boundary. Ordinary completion does not require a separate report workflow.

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
