---
name: frontier-migration
description: "Explicit-only: plan or execute coexistence and cutover for existing readers, writers, persisted data, or public contracts. Not every database or configuration edit."
---

# Frontier Migration

## Boundary

This is an instruction-only migration workflow. It does not add a migration daemon, scheduler, queue,
database, ledger, dual source of truth, or automatic upgrade channel. The existing repository, schema
owner, installer, storage owner, and deployment mechanism remain authoritative.

## Trigger

Use only when the user explicitly asks to plan, implement, verify, or recover a migration involving one
or more of:

- database schema or persisted data;
- file, configuration, manifest, or protocol format;
- public API, command, event, or plugin-registration identity;
- provider, account, session, project, or workspace identity;
- legacy Skill, instruction, install path, or compatibility fallback.

Do not use for a normal additive field that has no old reader/writer, a local rename with no persisted or
public consumer, or speculative future versioning.

## Objective

Move every known consumer from the current contract to the target contract while old and new states remain
truthful at each phase, interrupted work is recoverable, and destructive cleanup occurs only after evidence
shows the old surface is unused.

## Shared engineering judgment

Read [`../frontier-core/references/ENGINEERING_JUDGMENT.md`](../frontier-core/references/ENGINEERING_JUDGMENT.md) for the affected
source of truth, ownership, lifetime, and compatibility mechanism. Apply FOUNDATION to keep one canonical
authority during coexistence, REDUCTION to reject hypothetical consumers and unbounded dual paths, and
REALITY to bound backfill, retry, interruption, resource, and cleanup behavior. This migration workflow still
owns the compatible phase sequence.

## Preconditions

- Identify the current source of truth and its owner.
- Inventory active readers, writers, installers, versions, fallbacks, and external effects.
- Preserve existing dirty work and establish a rollback point or verified backup.
- Identify every destructive, irreversible, credential, permission, external, or production action that
  requires approval before execution.

## Default sequence

### 1. Baseline

Record the current version, schema or format, authoritative owner, active consumers, compatibility promise,
known dirty state, and exact recovery point. Reproduce the current behavior before changing it.

### 2. Expand

Add the new optional shape without removing or reinterpreting the old one. Old readers and writers must
continue to function. Prefer one-version additive evolution over parallel permanent APIs.

### 3. Compatibility

Define the temporary read/write behavior explicitly:

- which version writes old, new, or both;
- which version reads old, new, or either;
- idempotency and duplicate handling;
- ordering, partial failure, retry, and stale-client behavior;
- the owner of canonical identity during coexistence.

Do not create a second durable owner merely to make migration convenient.

### 4. Migrate or backfill

Run the smallest bounded, restartable transformation. Use stable checkpoints owned by the existing
migration mechanism, not an improvised second ledger. Validate counts, identities, invariants, and
privacy-safe evidence before and after each bounded unit.

A down migration is not universally required. Require either:

- a tested reversible rollback that preserves data and compatibility; or
- a verified backup plus a bounded forward-repair path when reversal would itself destroy information.

### 5. Cut over reads

Switch authoritative reads only after old and new representations reconcile under the declared checks.
Keep the compatibility write path until rollback and stale-client windows have closed.

### 6. Contract

Remove old writes, then remove old reads or destructive schema only in a later, separately approved step.
Prove zero known active consumers and preserve the recovery artifact until the removal window closes.

### 7. Close out

Record the final version, removed compatibility paths, verification, residual risk, rollback/repair status,
and exact cleanup still pending. Remove temporary migration code and flags when their exit condition is met.

## Approval gates

Require explicit approval before:

- destructive schema or file removal;
- production or external backfill;
- credential, permission, identity, or registration mutation;
- replacing the active installed plugin or global skill source;
- irreversible cutover, push, publication, tag, or Release.

Approval to design or prototype is not approval to execute these actions.

## Evidence

Use the repository's existing test and migration surfaces. Typical proof includes old/new reader-writer
matrices, idempotent retry, interrupted-unit recovery, exact identity preservation, invariant/count
reconciliation, sanitized error behavior, and one rollback or forward-repair exercise.

Do not add a general migration framework or full environment clone when focused existing checks can decide
the contract.

## Outputs

- migration record using `templates/migration-record.md` when the work spans phases;
- exact compatibility matrix and approval boundaries;
- implemented phase, verification, recovery point, residual risk, and next phase.

## Stop conditions

Stop at the first ungranted approval boundary, unresolved source-of-truth conflict, failed invariant, unsafe
rollback/repair condition, or completed phase whose next destructive action is intentionally separate.
