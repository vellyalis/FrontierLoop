---
name: frontier-state-manager
description: "Explicit-only: reconcile a compact handoff when work actually spans sessions, machines, or agents. Use existing repository state; do not create another ledger."
---

# Frontier Repository State

## Codex plugin boundary

This is the instruction-only replacement for Vibe Harness `state-manager`. There is no
`vh.exe`, SQLite state store, event ledger, transaction service, daemon, or exactly-once
processing. Git and current repository contents remain authoritative. Use an existing handoff
file when available; create a new repository-local handoff only when continuation truly needs it
and repository policy permits it.

## Trigger

- Work spans multiple stages, sessions, machines, or agents.
- Exploration or a high-impact change leaves accepted/rejected hypotheses that matter later.
- A session is stopping before the work is complete.
- Existing handoff claims may be stale relative to Git, code, or fresh verification.

Do not trigger for a self-contained Routine change that can finish in the current session.

## Objective

Preserve the smallest durable continuation packet that lets the next worker act safely without
re-reading the whole conversation or creating a second source of truth.

## Inputs

- Repository, branch, worktree, HEAD, and dirty state.
- Nearest applicable `AGENTS.md` and project policy.
- Existing handoff or state document, if any.
- Current Goal, accepted result, rejected hypotheses, verification, risks, and next action.

## Default procedure

1. Identify repository, branch, worktree, HEAD, and relevant dirty paths.
2. Classify dirty paths as task-created, pre-existing user work, generated evidence, secret/local-only, or unknown.
3. Reconcile any existing handoff against current code, Git, configuration, and fresh verification. Preserve stale claims as history only when useful; do not let them override current evidence.
4. Record only decision-bearing state:
   - Goal and non-negotiable constraints;
   - material Data／Owner／Lifetime, Responsibility, Module／Core, API／Contract, Observability, and Cleanup decisions or unknowns that change safe resumption;
   - current accepted implementation or Current Best;
   - accepted and rejected hypotheses with decisive evidence;
   - dirty-path ownership and prohibited operations;
   - verification status and residual risks;
   - recovery point and exact next executable action.
5. Prefer the repository's existing handoff convention. If none exists, use a concise `HANDOFF.md` or a path explicitly allowed by project policy; do not create a state directory, schema, ledger, or database.
6. Update only the owned section or coherent document. Never overwrite unrelated user notes.
7. Re-read the resulting file and compare it with Git/status before declaring it usable.
8. When the work is complete and the handoff has no continuing value, remove only the agent-owned temporary handoff if project policy allows; otherwise leave it clearly marked complete.

## Engineering Change Gate integration

Data／Owner／Lifetime、Responsibility、Module／Core、API／Contract、Tests、Observability、Cleanupの決定または未知点は、安全な再開、Recovery、Adoption、次Actionを変える場合だけ既存Handoffへ保持する。Repository、current files、Git、fresh evidenceをCanonical sourceとし、State ManagerはGateを再所有せず、第二のState Owner、Registry、Ledgerを作らない。

## Decision criteria

Keep an item only when it changes safe resumption, reproduction, adoption, rollback, ownership,
or the next action. Omit data that can be cheaply recovered from the repository.

## Outputs

- Reconciled repository-local handoff or an explicit reason no handoff was needed.
- Current identity, ownership, proof status, recovery point, and next action.

## Optional evidence labels

`StateObserved`, `HandoffUpdated`, `StateReconciled`, `SessionBoundaryRecorded`.
These are descriptive labels only; they are not machine-enforced events.

## Proof obligations

- Handoff agrees with repository identity, Git, and fresh evidence.
- Pre-existing user changes are identified and preserved.
- No secret or unrelated private data is stored.
- No claim of atomicity, exactly-once processing, or durable enforcement is made without a real mechanism.
- Material Engineering Change Gate state needed for continuation is reconciled with current repository truth rather than copied from stale prose.


## Stop conditions

Stop when the next worker can identify the correct repository state, protect existing work,
reproduce the current result, understand residual risk, and execute one exact next action.

## Failure recovery

If repository identity, dirty ownership, or source-of-truth conflicts cannot be resolved safely,
do not rewrite or normalize the worktree. Preserve observed evidence and escalate the specific conflict.
