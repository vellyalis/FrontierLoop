---
name: complexity-review
description: "Dependency、Service、Storage、抽象化、並列化などの新規複雑性を審査し、根拠のない過剰設計を拒否する。"
---

# Complexity Review Skill

## Trigger

新規Dependency、Service、Storage、抽象化、Plugin、非同期化、設定UI、独自基盤。
既存巨大Fileの成長、新規Budget超過File、Grandfathered例外または上限引上げ。

## Objective

現在のGoalへ追跡できない複雑性を防ぎ、必要な複雑性だけを明示的に所有する。

## Inputs

- Proposed change
- Goal / Requirement / Risk
- Existing alternatives

## Preconditions

追加要素とSimplest Valid Alternativeを比較できること。

## Default procedure

1. 現在のRequirementまたはRiskを特定する
2. 既存機能、標準機能、局所実装を調べる
3. Simplest Valid Alternativeを作る
4. 代替が不足する観測証拠を示す
5. Runtime、運用、障害、認知、Test、Security costを列挙する
6. Owner、Monitoring、Failure Mode、Rollback、Removal conditionを定義する
7. Accept / Defer / Reject / Replaceを決める
8. Architecture Health GateのBaseline差分を確認し、上限引上げや新規例外を通常解決として採用しない
9. `utils/common/helpers/shared`名のModuleは明示Admission、安定Invariant、実在する2消費者なしにRejectする
10. 新規Reusable Abstractionは既存の具体Consumer 2件以上、またはPublic／ABI／Security境界の明示例外なしにRejectする

## Decision criteria

現在の必要性、総複雑性、可逆性、所有可能性、証拠。

## Allowed discretion

Goalを同等に満たす候補からより単純なものを選んでよい。

## Escalation conditions

運用者不在、Rollback不能、費用・権限・外部依存が発生する場合。

## Outputs

templates/complexity-receipt.md。

## State events

DecisionProposed, DecisionAccepted, DecisionRejected, DependencyChanged

## Proof obligations

Requirement traceability、Alternative failure evidence、Removal path。
構造変更ではActual／Limit、Owner、依存方向、下方Ratchetまたは例外拒否のEvidence。
Generic module admissionとReusable abstraction exceptionは`architecture/maintainability-baseline.json`へ記録し、Machine GateはPath存在とConsumer数だけを検査する。安定Invariantの妥当性はReview Obligationとして扱う。
Semantic Debtの新規追加、独立Change Reasonの隠蔽、Raw I/O Baselineの増加を通常解決としてAcceptしてはならない。

## Stop conditions

Decisionと再検討条件が確定した時点。

## Failure recovery

証明が崩れた場合はDeferまたはRemoveし、Current Bestを復元する。
