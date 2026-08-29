---
name: frontier-recovery
description: "Use only after an actual interruption, failed command, uncertain external effect, stale or conflicting handoff, regression, worktree confusion, partial installation, or migration failure has occurred. Do not auto-load this Skill merely because a design or migration must be interruption-safe or recoverable; migration/architecture owns design-time rollback and recovery semantics until a real interrupted or uncertain state exists. Reconcile repository identity, Git, artifacts, evidence, and external target state before retrying, rolling back, or resuming. When a non-trivial change resumes, frontier-core remains the Work Unit owner and this specialist supplements it. Do not create a second runtime database."
---

# Frontier Recovery

## Codex plugin boundary

This is an instruction-only adaptation of Vibe Harness `recovery`. It has no Recovery Journal,
SQLite transaction log, event replay, daemon, or exactly-once guarantee. Confirm real repository
and external state before retrying any operation whose outcome is uncertain.

## Trigger

Crash, interruption, stale handoff, failed command, regression, migration failure, ambiguous
worktree/branch, partial external action, or resumed work from another session or computer.

This trigger is about observed recovery state, not a future design requirement. A request to make a
migration interruptible, rollback-safe, or recoverable does not by itself activate this Skill; keep that
design-time responsibility in `$frontier-migration` or `$frontier-architecture` until an actual failure,
interruption, partial effect, stale state, or uncertain outcome exists.

## Objective

Preserve the last verified result, prevent duplicate or destructive side effects, and recover a
safe next action from observable evidence.

## Inputs

- Repository root, branch, worktree, HEAD, status, and diff.
- Existing handoff, patch, checkpoint commit, or backup when available.
- Failed command and its captured output.
- Fresh verification and observable external state.

## Default procedure

1. Identify the exact repository, branch, worktree, HEAD, and upstream before changing anything.
2. Inspect dirty paths and separate task-created changes from pre-existing user work.
3. Reconcile handoff or prior claims against current code, configuration, Git, and fresh evidence.
4. Determine whether the failed operation had no effect, completed, partially completed, or remains unknown.
5. Choose resume, retry, compensating change, rollback, or stop based on observable state—not on the missing session's intent.
6. Before retrying an external or non-idempotent action, query its real target state or obtain authorization when that cannot be established.
7. Return to a known verification baseline and rerun only the checks needed to distinguish recovery success from continued failure.
8. Record the failure mechanism, preserved user work, recovery point, residual uncertainty, and exact next action in the existing handoff when continuation requires it.

## Decision criteria

Data safety, preservation of the verified result, ownership of dirty paths, reversibility,
external-effect certainty, reproduction, and recovery cost.

## Allowed discretion

A local, reversible retry may proceed after its prior effect is proven absent. Do not infer absence
from a timeout or missing response.

## Escalation conditions

Potential data loss, unresolved branch/worktree identity, unknown ownership, secret exposure,
non-reversible external effects, conflicting product goals, or an unavailable rollback.

## Outputs

Recovery report, reconciled repository state, verification result, residual uncertainty, and next action.

## Optional evidence labels

`RecoveryObserved`, `RollbackExecuted`, `StateReconciled`, `ResumePrepared`.
These are descriptive labels only.

## Proof obligations

Repository/Git identity, dirty ownership, preserved user work, known external-effect state,
verification baseline, and no unverified duplicate action.

## Stop conditions

Stop when work is back at a safe, observed state and exactly one next action is justified, or when
a concrete authorization/data-safety boundary is reached.

## Failure recovery

If recovery itself cannot establish safety, stop mutation, preserve evidence and backups, and report
the smallest unresolved conflict. Never reset, clean, force, or discard user work to make the state look simple.
