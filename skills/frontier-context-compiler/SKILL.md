---
name: frontier-context-compiler
description: "Explicit-only: preserve decision-bearing context across stages or sessions when sources are stale, conflicting, oversized, or materially incomplete. Not routine repository reconnaissance."
---

# Context Compiler Skill


## Trigger

Explicit user invocation or a material workflow handoff when cross-session decisions depend on missing, stale, conflicting, or oversized context. A new file, nested instruction, or ordinary local edit alone is not a trigger.

## Objective

Transcriptや全Repositoryを無差別に詰め込まず、次の判断に必要なContextを
権威、鮮度、由来、包含理由、競合状態付きで構成する。圧縮やSession再開後も
Goal Invariants、Current Best、失敗知識、Proof状態、次の実験を失わない。

## Inputs

- ユーザーの最新確定指示
- global / project / nested AGENTS
- README、manifest、build設定、ADR、Architecture、API、schema
- Git、diff、branch、worktree、dirty state
- Project State、Handoff、Operation Evidence
- 関連code、tests、logs、measurements、failure examples
- Tool / permission / environment / model capability
- Goal Model、Current Best、Hypothesis Ledger、Verification Surface

## Preconditions

- Repositoryまたは調査対象を一意に特定できる
- 読取可能な範囲と権限を確認できる
- SourceをFact、Instruction、Decision、Hypothesis、Evidenceへ分類できる

## Routine Fast Path and Context Budget

self-containedなRoutine変更では、永続Context Manifestを儀式として作らない。最低限、最新Goal、適用Instruction、対象File／Symbol、既存Pattern、関連Test／Command、Dirty stateだけを確認し、最小差分へ進む。

完全なManifestへ昇格するのは、複数段階・複数Session、矛盾Source、Architecture／Schema／Migration変更、A2／A3、Current Bestまたは失敗仮説の保持、判断を変えるContext不足がある場合だけとする。

各Sourceは、影響するPending DecisionまたはProof Obligationを一つ以上示すこと。何も変えないSource、全Repository inventory、再取得可能な生Log、関連しない過去履歴をContext量のために収集してはならない。

Unknownは`blocking`、`decision-relevant`、`non-blocking`へ分類する。`non-blocking`は可逆なDefaultまたは既存Conventionを採用し、必要な仮定だけ残して進む。検索は最も狭いPath／Symbol／期間から始め、結果が判断不能な場合だけ範囲を広げる。

## Engineering Change Gate integration

安全な継続判断を変える場合だけ、影響DataのSource／Owner／Lifetime／Invalidation、Responsibility、Module／Core配置、API／Contract、Observability、Cleanupの決定または未知点をContextへ保持する。これは`$frontier-core`のGate状態を運ぶもので、Context Compilerが再裁定したり第二のOwnerになったりしない。Routine fast pathでは必要項目だけを現在の作業Contextに保ち、完全なManifestを要求しない。

## Output: Context Manifest

Use the existing project handoff. Only when cross-session decisions require a
full packet, consult [the manifest template](templates/CONTEXT_MANIFEST.md).
Keep goal, current state, ownership, proof, risks, and next action; omit fields
that do not affect safe continuation. This is not a routine prerequisite.

## Default Procedure

1. **Compile the decision**
   - Extract Goal, acceptance, Scope, responsibility, generality, and approval boundaries.
   - Identify the next material decision or experiment. Context without a target decision is
     not yet compiled.
   - Identify the smallest safe and reversible action that could settle it. When that action
     is executable, do not delay it for a complete mental model.

2. **Establish instruction scope**
   - Load global and project instructions.
   - Discover nested instructions, but read only those applicable to files or directories
     entering the current Workstream.
   - Record precedence and any conflict.

3. **Reconcile runtime state**
   - Observe repository identity, branch/worktree, HEAD, dirty paths, configuration,
     dependencies, and fresh verification.
   - Compare State/Handoff against code and evidence.
   - Mark stale or conflicting entries; do not silently overwrite either side.

4. **Build a source inventory**
   - Classify each source as Instruction, Value, Architecture Decision, Implementation,
     Runtime Evidence, State, Reference, or Untrusted Input.
   - Record provenance and revision/hash when supported.

5. **Select by information value**
   - P0: required for correctness, safety, Scope, or the next decision.
   - P1: likely to change candidate ranking, diagnosis, or verification.
   - P2: useful on demand.
   - Exclude duplication, recoverable logs, unrelated history, and speculative context.
   - Record why a material-looking source was excluded.
   - Stop source collection when all P0 and enough P1 context exist to execute the decision.

6. **Compile engineering state**
   - Preserve Current Best/baseline, active hypotheses, rejected hypotheses and evidence,
     current bottleneck, proof status, risks, and next discriminating experiment.

7. **Check completeness**
   The manifest must answer:
   - What are we trying to improve?
   - What cannot change?
   - What is currently true?
   - What remains unknown?
   - What is the Current Best?
   - What observation selects the next action?
   - What can fail and how will we recover?
   - Which source authorizes each material decision?

8. **Emit a compact execution packet**
   - Provide only P0/P1 sources or precise ranges/symbols to the active worker.
   - Use references to P2 rather than embedding them.
   - Never pass secrets or unrelated private content.

9. **Refresh and compact**
   - Recompile when a refresh trigger fires.
   - Under token pressure, preserve compaction anchors before explanatory prose.

## Version-sensitive sources

When correctness depends on an exact external version, read
[the version-sensitive source lane](references/version-sensitive-sources.md).
Do not load it for version-independent local logic or mechanical edits.

## Context Conflict Rules

- User value conflicts are resolved only by the latest confirmed user instruction.
- Project constraints use the nearest applicable AGENTS.
- Architecture intent uses accepted ADRs unless superseded.
- Implementation truth uses current code/config/Git.
- Behavior truth uses fresh runtime evidence.
- A stale State entry is retained as history but cannot override newer implementation.
- Evidence conflict remains explicit until a discriminating observation resolves it.

## Capability Rules

The manifest records capabilities as `available`, `degraded`, `unavailable`, or
`unverified`.

Do not infer enforcement from a Skill description. In particular, verify before
claiming:

- atomic state update or exactly-once semantics;
- persistent event replay;
- independent reviewer identity;
- frozen review scope or content hashes;
- finding fingerprint deduplication;
- shell/process availability;
- parallel tool execution;
- external network or service access.

## Compaction Anchors

Never discard before lower-value context:

1. Goal Invariants and Acceptance
2. Responsibility / decision-bearing Engineering Change Gate / approval boundaries
3. Applicable instruction chain
4. Current Best and reproduction
5. Active and rejected hypotheses with evidence
6. Dirty state and ownership
7. Proof status and residual risk
8. Next executable experiment and stop condition

## Proof Obligations

- Every P0 source has provenance, authority, freshness, and inclusion reason.
- State/Handoff is reconciled against repository and fresh evidence.
- Conflicts are explicit.
- Context can justify the next implementation or adoption decision.
- No secret or unrelated private content is included.
- Compaction preserves all anchors.

## Stop Conditions

Stop compiling when:

- the next material decision is executable;
- all P0 context is present or an explicit capability/context gap is recorded;
- adding another source is unlikely to change that decision;
- refresh triggers are defined.

For Routine fast-path work, stop after the minimum instruction, target, dirty-state,
and verification context is known. Do not promote to a full Manifest merely because
more repository information is available.

Do not improve the Context Manifest as a documentation exercise after it can drive
the decision.

## Failure Recovery

- Missing P0 source: use the safest valid fallback, mark the decision blocked or
  degraded only to the extent necessary, and continue independent investigation.
- Stale State: preserve it, reconcile with Git/code/evidence, and update the existing repository handoff only when resumption needs it.
- Context overflow: apply priority and compaction anchors; do not truncate arbitrarily.
- Conflicting evidence: design the smallest discriminating experiment.
- Unavailable persistence: emit a repository-local manifest or explicit handoff and
  label the guarantee level honestly.
