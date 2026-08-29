---
name: frontier-deep-engineering
description: "Use explicitly only for a gated hard problem whose material mechanism, architecture, algorithm, or premise remains unresolved after mature solutions, the simplest local approach, reference comparison, and focused experiments cannot decide it. Reconstruct from first principles, prove one real vertical slice, and return to frontier-core or the narrow specialist once the structural decision is resolved. Do not use for Routine work, known solutions, difficulty alone, or speculative framework building."
---

# Deep Engineering Skill

## Codex plugin boundary

This active skill is adapted from the Vibe Harness workflow source. FrontierLoop has no
`vh.exe`, SQLite store, daemon, event ledger, or atomic state service. Treat legacy State/Event/
Ledger terms as logical evidence labels only; durable truth remains current repository files,
Git, nearest instructions, and an existing handoff when one is actually needed. Read
`../../references/RUNTIME_BOUNDARY.md` before claiming persistence, exactly-once behavior,
reviewer independence, or machine enforcement.

## Trigger

- 独自Engine、Framework、Runtime、Compiler、Renderer、Scheduler、Storage、
  Protocol、Interoperability Layer、Audio/Graphics pathを作る
- 成熟した既製実装がRequirementを満たさない
- 低レベル、real-time、concurrency、determinism、cross-platform、FFI、
  binary format、hardware-specificな実装
- 原因・feasibility・architecture・evaluationに大きな未知性がある
- 既存方式がStrategy Audit後もCurrent Bestを更新しない

## Objective

「難しいから長く考える」のではなく、問題を反証可能なMechanismと実験へ変換し、
最小のend-to-end証拠から段階的にCurrent Bestを育てる。必要な独自実装を恐れず、
同時に根拠のないFramework化を防ぐ。

## Activation Gate

このSkillは、難しい、コード量が多い、未知の技術である、独自実装が魅力的である、将来再利用できそうである、という理由だけでは起動しない。次のいずれかを現在Evidenceで示すこと。

- simplerな既存利用、局所変更、Adapt／Wrapが現在Requirementまたは具体的Riskを満たせない
- Semantics、Ownership、Lifecycle、Ordering、RecoveryのUnknownがMechanism選択を変える
- real-time、Concurrency、ABI、Binary Format、Hardware、Migration等のHard Boundaryが専用Oracleまたは実験を要求する
- Routine／Architectureの焦点化した試行が情報またはCurrent Bestを更新できなかった

焦点化した局所変更または一回の可逆実験で判断できる場合は、まず`$frontier-routine-change`または既存`$frontier-architecture`を使用する。起動時に、現在の一つのMaterial Decision、Current Bottleneck、Skillを終了できる観測を明示する。

### First-principles lane gate

First-principles reconstructionは、このSkillを使う全TaskのDefaultではない。次のすべてを現在Evidenceで示せる場合だけ開く。

- ModeがExplorationである
- 未決のMechanism、Architecture、Algorithm、または前提がGoal結果をMaterialに変える
- 成熟した解または最小の局所案がGoal Invariantsを満たさず、参照比較でも一回の焦点化した実験でも次のMaterial Decisionを決められない
- Required Valueが衝突する、Irreducible Constraintが不明、またはStrategy Audit後も焦点化した試行が繰り返し失敗している

難しさ、規模、未知の技術、新規性、独自実装への興味だけでは開かない。Gateが閉じている場合は、通常のcomplexity rung、Architecture、Debugging、Security、Performance、Migrationの該当Ownerへ戻る。Gateが開いても、一つのMaterialな構造判断が解けた時点でこのLaneを終了する。

## Required Inputs

- Goal Model / Acceptance / Goal Invariants
- Responsibility Map / Scope / Generalization Requirement
- Context Manifest
- Current Best or reproducible baseline
- operating envelope and failure impact
- applicable standards, reference implementations, measurements, and constraints
- proof and performance budgets
- rollback/recovery boundary

## Default Procedure

### 0. Select the complexity rung and next decision

次を順に比較する。

1. No Change、設定、既存機能の直接利用
2. 既存Owner内の焦点化した局所実装
3. 既存MechanismのAdapt／Wrap
4. 単一責任の新規Module／Abstraction
5. 再利用Engine／Frameworkまたは新規Lifecycle Owner

下位段階を棄却する観測Evidenceと、上位段階で新たに所有するFailure Modeを記録する。各Work Unitでは一つのMaterial Decisionまたは一つのVertical Slice Gapだけを進める。安全で可逆な識別実験が設計可能になったら、追加仮説の列挙より先に実行する。

### 1. Define the problem model

Specify:

- inputs, outputs, state, time, ordering, ownership, lifecycle;
- invariants and forbidden states;
- operating envelope and boundary conditions;
- latency, throughput, memory, determinism, compatibility, portability, and
  recovery budgets as applicable;
- observable success and failure mechanisms.

Do not choose an architecture until the model can explain what must remain true.

### 1A. Reconstruct from first principles when gated

この節はFirst-principles lane gateが開いている場合だけ使う。

1. Materialな前提を`Fundamental`、`Derived`、`User Requirement`、`External Contract`、`Environmental`、`Convention`、`Preference`、`Hypothesis`、`Unknown`へ分類し、source、owner、confidence、dependent decision、refutation conditionを残す。
2. Goal、state、lifecycle、information/control flow、resource bound、ownership、failure modeの因果・制約Graphを作る。Leafは一つの因果役割または責任、明示的なinput/outputまたはinvariant、owner、独立した検証またはboundを持つものに限る。
3. すべての有効解が守るIrreducible Constraint、Global Bottleneck、Required Valueの衝突、Current Best固有の制限、Goalを動かせる最小介入を導く。
4. ConstraintからMechanism、state owner、responsibility allocation、information/control flow、system/user/environment boundaryの異なる候補を再構成する。名前、配置、Parameter値だけの違いを構造候補に数えない。

User Requirement、Public Contract、避けられない環境制約は壊さず、ConventionとHypothesisだけを根拠付きで疑う。追加分解がimplementation、ownership、comparison、verificationのいずれも変えない時点で止める。巨大なDossierを必須にせず、既存のADRまたはExperiment Recordへ次のdecision traceだけを残す。

`Goal -> premise -> irreducible constraint -> candidate structure -> Artifact -> evidence -> decision`

### 2. Establish Current Best and references

- Reproduce the current implementation or simplest valid baseline.
- Inspect standards, prior art, reference implementations, known failures, and
  measured platform constraints where available.
- Extract principles and failure conditions rather than copying surface structure.
- Record assumptions and licensing/provenance boundaries.

### 3. Make the reuse/adapt/build decision

Compare:

- existing library/product as-is;
- adapting or wrapping an existing mechanism;
- a focused local implementation;
- a reusable custom engine/framework.

A custom mechanism is justified when simpler alternatives fail a current
Requirement or concrete Risk by evidence. Record the smallest alternative and
the observation that disqualifies it.

### 4. Define an executable oracle

Prefer one or more of:

- simple reference model;
- standards-derived expected vectors;
- differential comparison with a trusted implementation;
- trace replay;
- property/invariant checker;
- minimal prototype;
- hardware or runtime direct observation.

The oracle must be independent enough to catch shared assumptions.

### 5. Partition Workstreams

Typical independent Workstreams:

- semantic/reference model;
- core mechanism;
- platform adapter;
- performance path;
- compatibility and migration;
- verification and failure injection;
- observability and recovery.

Give each Workstream contribution, owner, dependencies, Current Best, and
termination condition. Do not split by arbitrary files.

### 6. Prove a vertical slice

Implement the smallest end-to-end path that exercises the real ownership,
data flow, and failure boundary. A vertical slice must produce a value-bearing
observable result, not only scaffolding.

Freeze broad API/framework expansion until the slice demonstrates:

- semantic correctness;
- required ownership and lifecycle;
- viable performance envelope;
- diagnosable failure behavior;
- realistic integration path.

### 7. Run discriminating experiments

For each experiment record（Skill directory内の`templates/EXPERIMENT_RECORD.md`を使用可能）:

- hypothesis and candidate type;
- change from Current Best;
- true/false observations;
- controlled conditions;
- metric/direct observation;
- side effects and regression surfaces;
- result and adoption decision;
- refutation and retry conditions.

Use ablation when a candidate contains independent changes.

### 8. Stabilize semantics before generalization

Extract a framework only after:

- at least two real call paths share a stable invariant;
- responsibility and lifecycle are clear;
- local duplication creates a concrete divergence or security/maintenance risk;
- the abstraction preserves debugging and performance visibility;
- removal/rollback remains practical.

一つのCall Path、将来の可能性、見た目の重複だけではFramework化しない。現在のGeneralization Requirementを超えるPlatform、Plugin、設定、Fallback、Extension Pointを先回りして作らない。

### 9. Engineer the hard boundaries

As applicable, explicitly design and verify:

- state transitions and cancellation;
- ownership, lifetime, resource cleanup, and backpressure;
- concurrency, ordering, races, deadlocks, and reentrancy;
- determinism, floating-point/numerical stability, and reproducibility;
- binary/API/ABI compatibility;
- error taxonomy and partial failure;
- persistence, crash consistency, migration, and recovery;
- clock, scheduling, device, OS, and platform assumptions;
- observability without changing timing or semantics materially.

### 10. Converge

- Accept only observed improvements to the same Comparison Class.
- Audit after two failures under the same strategy or immediately when the cause is clear.
- Restore Current Best and redesign after three non-improving attempts including the audit.
- Close a Workstream when its termination condition is met even if local ideas remain.
- Do not declare completion while a material executable Global Gap remains.

## Architecture Decision Record

For every material architecture choice preserve:

- problem and decision context;
- alternatives and Comparison Class;
- selected mechanism;
- evidence and constraints;
- rejected alternatives and reconsideration triggers;
- owner and lifecycle;
- failure/recovery;
- performance and compatibility impact;
- migration/rollback.

## Verification Surface

Choose by claim:

- semantic vectors and reference-model comparison;
- differential, property, metamorphic, fuzz, and boundary tests;
- stress, soak, race/deadlock, failure injection, and crash recovery;
- benchmark and profiler evidence;
- compatibility matrix and trace replay;
- end-to-end demo on representative environments.

Do not require every method. Require the smallest set that can refute the
principal claims.

## Anti-Overengineering Rules

- 現在Acceptanceへ不要なService、Store、Queue、Worker、Cache、Daemon、Plugin System、Policy Language、Concurrency Ownerを追加しない。
- Prototype、Benchmark Codex agent、Debug InstrumentationをProduction Ownerへ昇格させない。
- 既存Ownerを拡張できるのに第二Ownerまたは並行Source of Truthを作らない。
- Architecture変更と無関係なCleanup、Rename、Dependency更新、Format変更を混ぜない。
- 「あとで必要かもしれない」をPublic API、Config、Persistence、Migrationの根拠にしない。
- 一般化は要求された量化条件までに限定し、全Platform／全Use Caseを自動的なGoalにしない。
- Documentation、Diagram、ADRの完全性を実装Evidenceより優先しない。

## Proof Obligations

- problem model and invariants are explicit;
- reuse/adapt/build decision is evidence-backed;
- Current Best is reproducible;
- an end-to-end vertical slice exists;
- required budgets have evidence;
- failures are diagnosable and recovery is defined;
- experiment history prevents repetition;
- public contracts and migration are proportional to actual use;
- no unjustified framework or second owner was introduced.
- when the first-principles lane was used, its gate evidence and decision trace are reproducible.

## Stop Conditions

Stop when the whole relevant Goal is satisfied, required budgets and proof pass,
material structural defects are absent, residual variation is classified, and
the next Workstream has higher expected value.

また、追加Research、Architecture案、抽象化がPending Decisionを変えず、次の安全な実験または実装が明確になった時点で思考を停止して実行へ移る。
First-principles laneは構造判断が解けた時点で閉じ、残作業をRoutineまたは該当する専門Ownerへ戻す。

## Failure Recovery

- Preserve Current Best before structural experiments.
- Roll back clear degradation immediately.
- When the reference/oracle is wrong, version it and re-evaluate affected decisions.
- When platform assumptions fail, separate Mechanism defects from adapter/context settings.
- When instrumentation changes behavior, use lower-impact observation or external measurement.
