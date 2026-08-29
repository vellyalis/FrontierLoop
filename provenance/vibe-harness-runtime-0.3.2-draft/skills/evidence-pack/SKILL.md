---
name: evidence-pack
description: "完成時に変更、証拠、未実施、残存Risk、再開・Rollback情報を非エンジニアにも分かる形でまとめる。"
---

# Evidence Pack Skill

## Trigger

作業完了、レビュー依頼、Session停止、User acceptance。

## Objective

コードを読めないユーザーへ、価値、動作、証拠、Risk、復元方法を明確に渡す。

## Inputs

- Goal Model
- Changes
- Verification
- Complexity Receipts
- Residual risks
- State

## Preconditions

未解決のAdjudicated BLOCK、必須Proof、未処理Eventが確認されていること。Finding総数はCompletion条件にしない。

## Default procedure

1. Goalと重要条件を示す
2. 実際に変わった挙動と変えていない範囲を示す
3. Requirement → Design → Implementation → Evidenceを接続する
4. Verification結果をPass / Partial / NotRunで示す
5. 追加複雑性と理由を示す
6. Residual riskと未確認条件を示す
7. Rollback / Recoveryを示す
8. Userが使用感として確認する点だけを示す
9. Current StateとNext Actionを示す

## Decision criteria

専門知識なしで完成・Risk・次の判断を理解できるか。

## Allowed discretion

技術詳細は折りたたみ可能な補足へ送ってよい。

## Escalation conditions

重大未検証Risk、秘密情報混入、Goal未達。

## Outputs

templates/evidence-pack.mdに適合するDelivery Evidence。

## State events

EvidenceGenerated, SessionStopping

## Proof obligations

TraceabilityとSecret redaction。

## Stop conditions

Userが価値判断と使用感を確認でき、技術判断を要求されない時点。

## Failure recovery

証拠不足を文章で埋めず、IncompleteとしてVerificationへ戻す。
