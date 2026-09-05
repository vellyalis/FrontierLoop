# Engineering Judgment Doctrine

## Status and scope

This is a shared conditional reference, not a Skill, router, runtime component, or second workflow owner.
`frontier-core` continues to own the Work Unit. A narrow specialist adds only its material boundary.

Read this reference before selecting an implementation when a non-trivial code or configuration change
materially changes or depends on one or more of:

- data representation, canonical source, write authority, ownership, lifetime, or invalidation;
- persistence, serialization, module, process, API, or external-system boundaries;
- concurrency, ordering, cancellation, startup, or shutdown;
- caching, indexing, polling, scanning, background work, queues, retries, or fallbacks;
- a measured hot path or material CPU, memory, I/O, allocation, lock, or logging budget;
- migration, compatibility, authorization, recovery, irreversible effects, or failure semantics.

Do not load this reference for a mechanical micro-edit whose owner, behavior, state, contract, and decisive
check are already clear. FOUNDATION, REDUCTION, and REALITY are ordered engineering lenses, not simulated
personalities, fixed weights, or votes.

## Goal

Choose the smallest responsibility-correct causal change that satisfies the real acceptance criteria while
preserving correctness, one authoritative source of truth, explicit ownership and lifetime, bounded resource
cost, observable failure, and maintainability under representative use.

Do not optimize for the fewest changed lines, fewest files, most layers, least layers, or most elegant
abstraction in isolation. The target is the smallest complete causal surface that can be freshly verified.

## Evidence precedence

Use evidence in this order:

1. current runtime behavior, current files and Git, and real data;
2. reproducible tests, traces, profiles, counters, and direct observations;
3. current external contracts and repository documentation;
4. handoffs, plans, comments, intended designs, and previous completion reports.

Lower-ranked evidence must not override higher-ranked evidence. A stale handoff, passing mock, intended
architecture, or previous completion claim is not proof of current behavior.

## Decision states

Use one state when the distinction changes execution:

- **DIRECT** — the current ownership and structure are sound; a local implementation and proportional proof
  are sufficient.
- **INVESTIGATE** — the causal mechanism or authoritative state is not yet proven; run the smallest bounded
  experiment that can distinguish the material hypotheses.
- **RESTRUCTURE** — the requested behavior cannot be correct without repairing source of truth, ownership,
  lifetime, invalidation, dependency direction, or failure contract.
- **BLOCKED** — an unavailable external prerequisite, ungranted authority, unsafe irreversible action, or
  unobtainable decisive evidence prevents safe continuation.

Ordinary uncertainty is not BLOCKED when local evidence can resolve it. Investigate instead of asking the
user to choose a technical owner, module, cache, scan strategy, or API placement.

## Observable outcome

Before choosing a mechanism, identify:

- the observable behavior that must change;
- the behavior that must remain unchanged;
- the invariant or contract that must hold;
- the smallest fresh observation that can prove or falsify success.

Do not begin from a preferred cache, worker, polling loop, rewrite, abstraction, compatibility layer, or
framework and then reshape the Goal to justify it.

## Ground-truth map

Map only the fields that can change the decision, but do not omit a material unknown:

- concrete data structure and representation;
- origin and authoritative source;
- writer or write authority;
- readers and real consumers;
- creation and destruction points;
- lifetime and validity period;
- refresh, invalidation, or staleness rule;
- persistence and external contract;
- concurrency, ordering, cancellation, and transfer boundary;
- current failure and recovery behavior;
- execution frequency, maximum scope, and current resource cost.

Unknown fields are investigation targets. They are not permission to invent guessed defaults, duplicate
state, retries, scans, delays, or silent fallbacks.

## FOUNDATION

First verify that the underlying representation and authority are correct.

Require:

- one authoritative source for each fact;
- explicit write ownership;
- a lifetime matching the real entity or operation;
- an explicit invalidation rule for derived or cached state;
- an explicit transfer rule across module, process, thread, or device boundaries;
- persistence that preserves the meaning required by real consumers;
- APIs that expose domain semantics rather than accidental storage details.

Reject:

- two writable copies of the same fact;
- cached or mirrored state with unknown invalidation;
- ownership inferred only from call order;
- pointers, handles, IDs, snapshots, or references used beyond their proven lifetime;
- lossy conversion that removes information required by a later consumer;
- a new state owner introduced only to avoid understanding or repairing the existing owner.

## REDUCTION

Remove mechanisms not required by the acceptance criteria or a proven risk.

Challenge:

- duplicated state or writers;
- wrappers and layers with no semantic responsibility;
- speculative generic frameworks;
- continuous polling or scanning when an authoritative event or direct read exists;
- background work when the result is needed only at an action boundary;
- caches without a stable invalidation event;
- queues without bounds, backpressure, cancellation, and ownership;
- aliases, feature flags, compatibility branches, retries, and silent fallbacks;
- parallel old and new paths that remain dual sources of truth.

An abstraction is justified by a stable semantic boundary, owned policy, hard safety boundary, dependency
direction, or proven repeated operation. File length, aesthetic symmetry, hypothetical reuse, or one
speculative consumer is insufficient.

Prefer a direct authoritative read over a copied shadow state, a reliable event over polling, and on-demand
work over continuous work when the Goal only needs the result at a specific action boundary.

## REALITY

Evaluate the proposed behavior under representative real conditions.

Determine as applicable:

- activation condition and execution frequency;
- maximum traversal, scan, batch, queue, or retry scope;
- CPU, memory, I/O, allocation, lock, GPU, network, and logging cost;
- cancellation, shutdown, restart, and cleanup behavior;
- timeout, retry, backoff, and failure-amplification behavior;
- queue bounds, backpressure, contention, starvation, and ordering risks;
- behavior with stale, missing, malformed, partial, or concurrently changed data;
- maintenance, review, and operational burden introduced by the design.

Do not claim a performance improvement without a relevant baseline and fresh post-change measurement under
equivalent conditions. Do not use a toy benchmark or mock that removes the expensive runtime, storage,
device, process, synchronization, or network boundary responsible for the real symptom.

## Mechanism admission rule

For every new cache, index, polling loop, scan, background task, thread, queue, retry system, abstraction
layer, compatibility path, feature flag, or fallback, establish:

1. the concrete current problem that cannot be solved without it;
2. its single owner;
3. when it starts or activates;
4. when and how it stops, cancels, or is disposed;
5. its maximum resource cost and work scope;
6. its invalidation, refresh, ordering, or consistency rule;
7. its failure and recovery behavior;
8. how activation, failure, and cleanup are observed;
9. its removal or consolidation condition.

Reject the mechanism when these obligations cannot be satisfied, unless the mechanism itself is a bounded,
reversible experiment whose only purpose is to obtain the missing evidence and whose cleanup is explicit.

## Smallest causal change

Change the smallest complete set of responsibilities that removes the proven cause and satisfies the full
acceptance criteria.

The smallest causal change is not necessarily:

- the smallest textual diff;
- the fewest modified files;
- a patch at the visible symptom;
- preservation of an incorrect owner or dependency boundary.

Do not include unrelated cleanup. Do not leave a half-migrated design where old and new paths remain
authoritative. When a real compatibility obligation prevents immediate removal, use a bounded migration with
one canonical owner and a verified exit condition.

## Failure and compatibility contract

Fail closed when uncertainty affects correctness, authorization, persistence, ownership, external contracts,
irreversible operations, or data integrity.

Graceful degradation is allowed only for optional behavior when core semantics remain correct, activation is
observable, the fallback has one owner, focused tests exist, and an exit or supported-mode condition is
explicit. Never turn an unknown, partial success, stale value, unsupported state, or silent fallback into
apparent success.

Preserve compatibility only for an identified real consumer, persisted-data obligation, or published
external contract. Record the consumer, compatibility period, owner, migration path, verification method,
and removal condition. After cutover is verified, remove the superseded implementation, aliases, flags,
legacy documentation, and obsolete tests.

## Verification

Use fresh evidence proportional to the causal surface. As applicable, verify:

- the original user-visible scenario or acceptance case;
- the affected invariant and authoritative state;
- the relevant failure path;
- a material regression boundary;
- representative resource cost when performance or continuous work changed;
- startup, cancellation, shutdown, restart, migration, or cleanup behavior.

Start with targeted proof and broaden only when the dependency or risk surface requires it. A mock that
replaces the boundary responsible for the defect is not proof that the real defect is fixed. Stop when all
required claims are decided and another check cannot change implementation, adoption, rollback, or residual
risk treatment.

## Reporting

Do not emit this doctrine as a checklist for Routine work. For structural, investigative, or blocked work,
report only decision-bearing results:

- **DECISION** — DIRECT, INVESTIGATE, RESTRUCTURE, or BLOCKED;
- **OBSERVED GROUND TRUTH** — authoritative state, owner, lifetime, and relevant execution path;
- **PROVEN CAUSE or MATERIAL UNKNOWN**;
- **CHOSEN CAUSAL CHANGE**;
- **MECHANISMS ADDED or REMOVED**;
- **FRESH VERIFICATION**;
- **REMAINING RISK**.

Do not report an intended action, created plan, passing mock, or previous completion statement as completed
work.
