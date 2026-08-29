---
name: architecture
description: "責任境界、Data Flow、契約、所有者、Failure Modeを設計し、第二Ownerや不要な基盤を作らない。"
---

# Architecture Skill

## Trigger

新規Project、主要境界、Data Flow、公開API、Storage、Deployment方式の変更。
既存Grandfathered Fileへ新しいApplication Service、State Lifecycle、Failure Boundaryを追加する場合。

## Objective

Goalを満たすSimplest Valid Architectureを選び、技術判断を非エンジニアへ返さない。

## Inputs

- Goal Model
- Constraints
- Existing architecture
- Repository profile

## Preconditions

Responsibility Mapと主要Use Caseがあること。

## Default procedure

1. Responsibility MapとData Flowを作る
2. Simplest Valid Baselineを作る
3. 必要な場合だけ構造的に異なる代替案を作る
4. Goal適合、可逆性、運用負荷、障害点、Security、検証容易性で比較する
5. 新規複雑性へReceiptを作る
6. 推奨案と却下案・再検討条件をADRへ残す
7. Userには価値トレードオフだけを確認する
8. `architecture/maintainability-baseline.json`があるRepositoryでは、変更前後のArchitecture Healthを比較し、Grandfathered成長を許可しない
9. 新規SourceとOwned ModuleはOwner、単一Responsibility、単一Change Reason、Layer、I/O Policy、Public Surface、Focused Test Seam、最大Owner Hopを同Baselineへ記録する
10. ApplicationはCoordinator、Domain/CoreはDB／HTTP／UI／Filesystem／Process／Platform Adapter非依存、代表Flowは3-4 Owner境界内で設計する
11. 既存のRaw I/Oまたは複数Change Reasonを残す場合はSemantic DebtへReason、独立Change Reason、Exit Condition、Review Owner、Raw I/O Baselineを記録し、増加させない

## Decision criteria

Goal適合、責任分離、Failure recovery、総複雑性、現在の制約。

## Allowed discretion

内部技術選定は既存ConventionとEvidenceに基づき自律選択してよい。

## Escalation conditions

費用、Privacy、Vendor lock-in、不可逆Migration、製品価値が変わる場合。

## Outputs

Architecture Decision、Data Flow、Complexity Receipts、Failure / Recovery。

## State events

DecisionProposed, DecisionAccepted, ArchitectureChanged, RiskDiscovered

## Proof obligations

Simplest Valid Alternativeとの比較、Failure Mode、Rollback。
Source責任を変更する場合はOwner、File／Module Boundary、依存方向、Architecture Health結果。
800行超過は注意閾値であり、分割する場合はLine数ではなくResponsibility、Change Reason、I/O境界、Public Surface、Test Seam、Owner Hopで正当化する。
Machine Gateは客観事実だけを検査するため、単一責任・認知負荷・Traceabilityの意味判断はReview ObligationとしてEvidenceへ残す。

## Stop conditions

選択理由と再検討条件がEvidence付きで確定した時点。

## Failure recovery

前提が崩れた場合はADRを上書きせず、新Decisionとして記録する。
