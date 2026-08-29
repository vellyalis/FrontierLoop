---
name: security-review
description: "Prompt Injection、Secret、権限、外部作用、Supply Chain、Data境界をRiskに応じて検査する。"
---

# Security Review Skill

## Trigger

Secret、Auth、Permission、External input、Dependency、Network、A2/A3。

## Objective

非エンジニアが判断できないSecurity境界をHarnessが検査し、秘密と権限を保護する。

## Inputs

- Threat surface
- Diff / dependencies
- Tool plan
- Data flow

## Preconditions

Trust boundaryとData classificationを定義できること。

## Default procedure

1. SecretとPersonal dataの流れを確認する
2. 未信頼入力とPrompt injectionを分離する
3. AuthN / AuthZ / Permissionを確認する
4. External communicationとD3 actionを検出する
5. Dependency source / license / integrity / vulnerabilityを確認する
6. Log / State / Evidence redactionを確認する
7. Failure / Abuse casesを検証する

## Decision criteria

最小権限、Data exposure、外部影響、Supply-chain、Recovery。

## Allowed discretion

安全側の局所設定は自律適用できるが、権限変更や外部送信は承認を得る。

## Escalation conditions

Secret exposure、未認可Access、重大脆弱性、外部送信、権限変更。

## Outputs

Security findings、Required mitigations、Residual risk。

## State events

RiskDiscovered, VerificationRecorded, DecisionProposed

## Proof obligations

SECURITY.mdのA2/A3 completion conditions。

## Stop conditions

重大Security claimがEvidenceで閉じ、Residual riskが明示された時点。

## Failure recovery

Secretが露出した場合は保存を停止し、Redact、Rotation推奨、影響範囲記録を行う。
