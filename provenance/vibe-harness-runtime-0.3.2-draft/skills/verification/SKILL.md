---
name: verification
description: "Goalと品質主張から必要なProofだけを選び、追加検証が判断を変えなくなった時点で停止する。"
---

# Verification Skill

## Trigger

主要品質をユーザーが直接判定できない、変更を完成判定する、仮説を比較する。

## Objective

品質Claimを専門知識なしで確認可能なEvidenceへ変換し、過不足なく停止する。

## Inputs

- Goal / Acceptance
- Change / Candidate
- Failure impact
- Existing verification surface

## Preconditions

Claimと失敗影響を列挙できること。

## Default procedure

1. Proof Obligationを抽出する
2. Claimを直接判定する最小Evidence methodを選ぶ
3. Acceptance、変更挙動、中核、高影響失敗、境界を優先する
4. Test / Demo / Measurement / Failure injectionを実行する
5. Pass / Fail / Partial / NotRunを記録する
6. Residual Riskを明示する
7. テスト、検証専用実装、安全設計の総量が成果物本体の新規実装量の1/3以下であることを確認する
8. 追加検証が判断を変えるか評価する
9. Stop ruleで終了する

## Decision criteria

Claim判定能力、Failure impact、独立性、再現性、追加情報価値。

## Allowed discretion

Test種別、Tool、比較方法はClaimに最適なものを選べる。Risk-based Proof Obligationは、常時Global AGENTSの固定1/3上限内で情報価値の高い検証を選ぶためにだけ使用する。

## Escalation conditions

A2/A3で異常系、Rollback、権限、Data lossが未検証、または必須Proofを固定1/3上限内で成立させられない。

## Outputs

Proof Obligations、Evidence、Residual Risks。

## State events

CommandExecuted, VerificationRecorded, RiskDiscovered

## Proof obligations

- 必須Proof自身
- テスト、検証専用実装、安全設計の総量が成果物本体の新規実装量の1/3以下
- 名称ではなく主目的で検証量を分類した根拠

## Stop conditions

必須Proofが閉じ、重大未検証Riskがなく、固定1/3上限を満たし、追加検証が判断を変えない時点。

## Failure recovery

Testと実装が同じ前提を共有する疑いがあれば、独立Oracleまたは別Methodで再検証する。必須Proofを固定上限内で成立させられない場合は、上限を黙って超過したり検証済みとClaimしたりせず、実装またはVerification Surfaceを再設計して未解決Conflictとして扱う。
