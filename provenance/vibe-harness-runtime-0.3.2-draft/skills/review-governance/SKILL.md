---
name: review-governance
description: "Review Findingを閉じた基準で裁定し、Nit、重複、Requirement発明、無限Rework、Review起因の過剰設計を防ぐ。"
---

# Review Governance Skill

- Skill ID: `review-governance`
- Contract version: `1.0.0`
- Authority: Portable Core policy; Reviewer outputより優先

## Trigger

- Independent Reviewerが`ReviewReport`を返した。
- Review FindingのBlocking可否を決める。
- Re-reviewまたはReworkを開始する。
- Reviewerが新Requirement、Architecture変更、大規模Refactorを提案した。
- Completion GateがReview残件を評価する。

## Objective

重大欠陥を見逃さず、Style、Nit、抽象的理想、将来改善、重複指摘による無限Reworkを防ぎ、Reviewを有限回で収束させる。

Reviewを弱くするのではなく、Reviewerの権限を欠陥候補の発見へ限定し、最終Blockingを明示Policyで裁定する。

## Inputs

- Goal Model／Goal Invariants。
- Confirmed Requirements／Acceptance／Risk Policy。
- Assurance Level。
- Frozen Review Scope。
- ReviewReport／Evidence。
- Prior Adjudicated Findings／Fingerprints。
- Current Diff／Proof Results／Complexity Receipts。
- Review Round／Rework Budget。

## Preconditions

- ReviewerとBuilderのRun ID、Principal、Model、Provider、Context lineageを確認済み。
- ReviewerはBuilder SessionをResumeしていない。
- A2／A3では`independence=independent`、A0／A1で`partial`を使う場合はProject PolicyとEvidenceを確認済み。
- Review Scope、Base OID、Head OIDを固定済み。
- Finding Candidate Schemaを検証済み。
- EvidenceのOrigin、Freshness、Content Hashを確認済み。

## Invariants

1. Reviewerは最終Blocking、Completion拒否、Requirement追加を決めない。
2. Self-reviewまたは`independence=invalid`をIndependent Reviewとして扱わない。A2／A3で`partial`を許可しない。
3. Finding 0件は正常なPASSである。
4. 完成条件は指摘ゼロではなく、未解決Adjudicated BLOCK 0件である。
5. S3／InfoはBlocking不可。
6. 同じFingerprintを文言変更だけで再Blockingしない。
7. Reviewer推奨修正は拘束力を持たず、Complexity Gateを迂回しない。
8. Re-reviewごとにRepository全体を掘り直さない。
9. Non-blocking Findingを自動Backlog化せず、Work Unitを再Openしない。

## Procedure

### 1. Normalize

- Requirement／Risk／Proof参照を解決する。
- Location、Failure Mechanism、Evidenceを正規化する。
- Severityを`S0 | S1 | S2 | S3 | Info`へ変換する。
- Fingerprintを再計算する。

### 2. Deduplicate

- Existing Fingerprint一致は`DUPLICATE`。
- 新Evidenceがある場合は既存FindingのRevisionとして関連付ける。
- 同じ欠陥の言い換えを新規Findingとして扱わない。

### 3. Scope／Requirement Guard

- Current Requirementに存在しない理想条件は`NEEDS_PRODUCT_DECISION`。
- Scope外は`OUT_OF_SCOPE`。
- Style、命名、抽象的美しさ、将来改善だけなら`DISMISS`または`DEFER`。

### 4. Blocking Adjudication

`BLOCK`にできるのは次だけ。

- 明示Requirement／Acceptance違反。
- 必須Gate失敗。
- 重大Regression。
- Security／Privacy／Secret／Permission。
- Data Loss／Corruption／Migration破損。
- Crash／Deadlock／実用不能。
- Public API／Contract破壊。
- A2／A3必須Proof欠落。
- 重大なRollback／Recovery不能。

S0／S1はBlocking候補。S2は原則Non-blockingで、Block昇格にはRequirement IDまたはRisk Policy IDが必要。S3／InfoはBlock不可。

### 5. Recommended Action Guard

Reviewerの修正案を欠陥そのものと分離する。BuilderはSimplest Valid Fixを選べる。次を含む案は`complexity-review`へ送る。

- Dependency／Service／Queue／Storage。
- 抽象化層／Plugin／Framework。
- Concurrency／Distributed構成。
- 広域Refactor。
- 新Test／Benchmark／Observability基盤。

### 6. Re-review Scope

初回Review後は次だけを見る。

- 未解決BLOCK。
- その修正Diff。
- 直接Regression Surface。
- 対応Proof。

新規BLOCKは修正起因または新しい具体的Evidenceを持つS0／S1だけ。

### 7. Convergence

- Rework Budget既定2回。
- Budget内でBLOCK解消ならAccept。
- Budget枯渇＋重大BLOCK残存なら一度だけEscalate。
- S2／S3／InfoのみならAccept with residualsまたはDismiss。
- 同じFindingの反復はDuplicateとして却下。

### 8. Non-blocking Retention

Backlog候補にするのは次を満たす場合だけ。

```text
expected_goal_contribution
  > implementation_cost + regression_risk + opportunity_cost
```

満たさないFindingはDismissしてよい。

## Decision Criteria

優先順位:

1. Confirmed Requirement／Acceptance。
2. High-assurance Risk Policy。
3. Direct Runtime Evidence。
4. Regression／Recovery影響。
5. Complexity／Opportunity Cost。
6. Style／Preference。

下位基準だけで上位のCompletionをBlockしない。

## Allowed Discretion

- `FIX_IF_TRIVIAL`と`DEFER`の選択。`FIX_IF_TRIVIAL`は既存Scope内、局所的、可逆、Complexity追加なし、追加Review不要の場合だけ選ぶ。
- Non-blocking FindingをPortfolio Selectionへ送るかDismissするか。
- 欠陥解消方式の選択。

ただしClosed Blocking Basis、Severity floor、Rework Budget、Scope Freezeは裁量で緩和しない。

## Escalation Conditions

- S0／S1 BLOCKがRework Budget後も残る。
- Requirement同士が矛盾する。
- Goal／Scope／責任境界の変更が必要。
- Evidenceが競合し、Source of Truthだけでは解決不能。
- A3の専門判断が必要。

## Outputs

- Adjudicated Findings。
- Work-level Result: `ACCEPT | ACCEPT_WITH_RESIDUAL_RISK | REWORK | ESCALATE | EXTERNAL_BLOCKED`。
- Remaining Rework Budget。
- Next Scoped Review Packet。
- Dismissed／Deferred／Duplicate summary。
- Complexity Gate requests。

## State Events

- `ReviewScopeFrozen`
- `ReviewFindingProposed`
- `ReviewFindingAdjudicated`
- `ReviewFindingDuplicate`
- `ReviewReworkRequested`
- `ReviewConverged`
- `EscalationRaised`

## Proof Obligations

- ReviewerとBuilderの分離。
- FindingのEvidence／Reproduction。
- BLOCKのClosed Basis。
- Fingerprint重複排除。
- Re-review Scope遵守。
- Rework Budget遵守。
- Reviewer推奨ComplexityのGate通過。
- Zero-finding PASS受理。

## Stop Conditions

次をすべて満たしたらReviewを終了する。

- 未解決Adjudicated BLOCKが0。
- 必須ProofがPassまたは許容済みResidual Risk。
- Acceptanceを満たす。
- 新しい重大Regressionがない。
- State Sync済み。

Minor／Nit／Ideaが残ることだけを継続理由にしない。

## Failure Recovery

- Governance途中Crash: Event Ledgerから同一Policy Versionで再Adjudicateする。
- Fingerprint Store不整合: Reviewを進めずRebuildし、重複Blockを防ぐ。
- Reviewer Output malformed: Reviewerへ一度だけSchema修正を要求し、失敗時はReview Capability Gap。
- Scope Hash不一致: Re-reviewを中止して新Scopeを明示的にFreezeする。
- Budget記録不明: 0へ戻さずUnknownとしてEscalateする。
