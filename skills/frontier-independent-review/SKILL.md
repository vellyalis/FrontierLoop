---
name: frontier-independent-review
description: "Explicit-only: search for defects in genuinely separate agent, model, or session context. Report evidence, not final blocking decisions; never label self-review independent."
---

# Independent Review Skill


## Trigger

Explicit user invocation or a material workflow handoff requesting a genuinely separate defect search. A2 work benefits from independent review when available; mandatory A3/project guarantees must not be invented or replaced with self-review.

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
- ReviewerのContextをBuilderと分離する。別Agent／別Model／別Sessionが利用不能ならSelf-reviewとして明示し、Independent Reviewと呼ばない。
- Review Scopeと基準Versionを固定する。

## Invariants

- Reviewerは最終`BLOCK`、Work Unit再Open、Completion拒否、Requirement追加、Scope拡張を決定しない。
- Reviewerは修正方式を強制しない。
- Finding数のノルマを持たない。問題がなければ0件で終了する。
- Style、命名、抽象的美しさ、将来改善、別Architectureの好みだけを重大欠陥として提出しない。

## Engineering Change Gate integration

materialな変更では、Canonical DataのSource／Owner／LifetimeとDuplicate Owner、Responsibility leakage、Module／Core misplacement、Public Contract leakage、Failure Observability、superseded／dual pathを確認する。構造Findingは具体的なFailure MechanismとGoal Impactを必須とし、Architectureの好みだけでは提出しない。ReviewerはGateの実装Ownerにも最終裁定者にもならない。

## Default procedure

1. Requirement / Acceptance Review
2. Canonical Data／Owner／Lifetime／Invalidation and duplicate ownership Review
3. Responsibility leakage／Module-Core placement／Dependency／Public Contract Review
4. Implementation／Failure／Observability／superseded or dual-path Review
5. Simplicity／unnecessary complexity and Verification／proof coverage Review
6. Security／Privacy／Permission／Data Integrity Review
7. Finding候補へ具体的Evidence、ReproductionまたはReasoned Proof、Affected Location、Failure Mechanism、Goal Impactを付ける
8. Severityを`S0 | S1 | S2 | S3 | Info`として**提案**する
9. Recommended Actionは参考案として示し、Simplest Valid Fixを妨げない
10. `ReviewReport`を`$frontier-review-governance`へ渡す

## Decision criteria

Goal Impact、実害、再現性、回帰、Security、Data Integrity、運用不能性、明示Requirementとの対応。

## Allowed discretion

同一Agentの分離ContextはA0/A1の`partial` Reviewとして扱えるが、Independentとは呼ばない。A2/A3は別Agentまたは別Modelを優先し、利用不能ならその保証不足を明示する。複数修正案がある場合は最小の有効修正を参考案としてよい。

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

## Optional evidence labels

ReviewStarted, ReviewReportRecorded, RiskCandidateDiscovered

## Proof obligations

各Finding候補がEvidence、Location、Failure Mechanism、Goal Impactを持つこと。0件PASSではReview Scopeを実際に確認したCoverage Evidenceを持つこと。

## Stop conditions

Frozen Scopeを一巡し、追加確認の情報価値が採否判断を変えなくなった時点。指摘を捻り出すために継続しない。

## Failure recovery

False Positiveが多い場合はReview Rubric、Context、Requirement mappingを監査する。Reviewer出力が最終Blockingを含む場合はSchema violationとして拒否し、裁定へ渡さない。
