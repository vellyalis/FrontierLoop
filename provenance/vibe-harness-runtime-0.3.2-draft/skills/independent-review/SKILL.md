---
name: independent-review
description: "Builderと分離したContextで重大な欠陥候補と証拠を発見する。最終BlockingやRequirement追加は行わない。"
---

# Independent Review Skill

## Trigger

A2以上、Architecture変更、Explorationの重要採用、完了前の反証。

## Objective

Builderの説明から独立して、Goal未達、欠陥、過剰設計、検証不足の**候補**を証拠付きで発見する。Reviewerは最終裁定者ではない。

## Inputs

- Goal / Acceptance / confirmed Requirement IDs
- ADR / responsibility map
- Frozen review scope
- Diff / artifact
- Runtime evidence / proof results
- Complexity Receipts
- Current Best

## Preconditions

- 最初のPassではBuilderの長い意図説明を除外する。
- Reviewer IDまたはSessionをBuilderと分離する。
- Review Scopeと基準Versionを固定する。

## Invariants

- Reviewerは最終`BLOCK`、Work Unit再Open、Completion拒否、Requirement追加、Scope拡張を決定しない。
- Reviewerは修正方式を強制しない。
- Finding数のノルマを持たない。問題がなければ0件で終了する。
- Style、命名、抽象的美しさ、将来改善、別Architectureの好みだけを重大欠陥として提出しない。

## Default procedure

1. Requirement / Acceptance Review
2. Architecture / Responsibility Review
3. Implementation / Failure Review
4. Simplicity / unnecessary complexity Review
5. Verification / proof coverage Review
6. Security / Data / Permission Review
7. Finding候補へ具体的Evidence、ReproductionまたはReasoned Proof、Affected Location、Failure Mechanism、Goal Impactを付ける
8. Severityを`S0 | S1 | S2 | S3 | Info`として**提案**する
9. Recommended Actionは参考案として示し、Simplest Valid Fixを妨げない
10. `ReviewReport`を`review-governance`へ渡す

## Decision criteria

Goal Impact、実害、再現性、回帰、Security、Data Integrity、運用不能性、明示Requirementとの対応。

## Allowed discretion

同一Agentでも分離Contextを使用できる。A2/A3は別Agentまたは別Modelを優先する。複数修正案がある場合は最小の有効修正を参考案としてよい。

## Escalation conditions

重大な未知Risk、Evidence取得不能、Reviewer間でFailure Mechanismが競合する場合。Escalationは製品判断候補であり、ReviewerによるScope拡張ではない。

## Outputs

`ReviewReport`:

- review_id / round_id / reviewer_identity
- frozen_scope_digest
- findings[]
  - finding_id
  - proposed_severity
  - requirement_or_policy_id（不明ならnull）
  - affected_location
  - failure_mechanism
  - evidence_refs
  - reproduction_or_reasoned_proof
  - goal_impact
  - recommended_action（非拘束）
- review_coverage
- unavailable_evidence

`blocking`または最終Dispositionを出力してはならない。

## State events

ReviewStarted, ReviewReportRecorded, RiskCandidateDiscovered

## Proof obligations

各Finding候補がEvidence、Location、Failure Mechanism、Goal Impactを持つこと。0件PASSではReview Scopeを実際に確認したCoverage Evidenceを持つこと。

## Stop conditions

Frozen Scopeを一巡し、追加確認の情報価値が採否判断を変えなくなった時点。指摘を捻り出すために継続しない。

## Failure recovery

False Positiveが多い場合はReview Rubric、Context、Requirement mappingを監査する。Reviewer出力が最終Blockingを含む場合はSchema violationとして拒否し、裁定へ渡さない。
