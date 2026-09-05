# Routing matrix

FrontierLoop does not depend on a meta-router loading another skill.

## Implicit set

| Trigger | Skill |
|---|---|
| Every non-trivial software change, with a lightweight gate for data, responsibility, placement, contracts, proof, observability, and cleanup; micro-edits stay lightweight | `frontier-core` |
| Material ownership, lifetime, Core/module, dependency, public-contract, deployment, or failure-boundary decision; not an unchanged-boundary performance mechanism or schema coexistence already owned by migration | `frontier-architecture` |
| Unknown, intermittent, multi-layer, recurring, environment-sensitive, or failed-fix defect | `frontier-debug-investigation` |
| Material changes to trust, secrets, auth, permissions, untrusted input, privacy, external effects, or supply-chain risk; not persistence alone | `frontier-security-review` |
| Measured latency, throughput, startup, jitter, memory, CPU/GPU/I/O, scale, contention, or backpressure goal/regression | `frontier-performance-engineering` |
| Missing decisive evaluator or materially open solution structure | `frontier-portfolio` |
| Actual interrupted, partial, conflicting, or uncertain effects; not a harmless understood command error or design-time rollback plan | `frontier-recovery` |

These seven skills use `policy.allow_implicit_invocation: true`. `frontier-core` owns every non-trivial
change and contains the routine engineering gate itself. Escalate only a material ownership, lifetime,
Core/module placement, dependency, public-contract, deployment, or failure-boundary decision to
`frontier-architecture`; the architecture skill supplements rather than replaces the core owner.
The same ownership rule applies to every implicit specialist: load `frontier-core` for non-trivial work,
then add only the narrow specialist that changes handling. An explicit-only helper such as
`frontier-routine-change` is never selected directly from an ordinary user task or as a peer substitute.

## Shared structural judgment

`skills/frontier-core/references/ENGINEERING_JUDGMENT.md` is a conditional reference, not an eighth implicit Skill or a second
router. `frontier-core` loads it only for material representation, ownership/lifetime, mechanism, resource,
compatibility, or failure decisions. Architecture, debugging, performance, and migration then apply only the
FOUNDATION, REDUCTION, or REALITY focus relevant to their existing responsibility. Mechanical micro-edits do
not load it.

## Explicit-only set

`frontier-intake`, `frontier-goal-compiler`, `frontier-routine-change`,
`frontier-execution-cycle`, `frontier-exploration`, `frontier-complexity-review`,
`frontier-context-compiler`, `frontier-deep-engineering`, `frontier-evidence-pack`,
`frontier-independent-review`, `frontier-review-governance`, `frontier-state-manager`,
`frontier-subagent-orchestration`, `frontier-verification`, and `frontier-version-control`.

Use these when the user names them or when a loaded workflow explicitly needs their full procedure.
The universal safety and stop rules needed for ordinary work already exist in `frontier-core`.

### Hard-problem first-principles lane

`frontier-deep-engineering` remains explicit-only. Its first-principles lane opens only for an Exploration
task with a material unresolved mechanism, architecture, algorithm, or premise after mature solutions,
the simplest local approach, reference comparison, and focused experiments cannot decide the next material
choice. Difficulty, size, unfamiliarity, or novelty alone are not triggers.

`frontier-exploration` owns general hypothesis comparison, `frontier-portfolio` owns a missing evaluator or
two-artifact structural comparison, and `frontier-deep-engineering` owns constraint-based reconstruction for
the gated hard custom-mechanism decision. Close the lane as soon as that structural decision is resolved.

## Direct by default

Clear goal + clear solution + clear evaluator -> implement -> targeted proof -> stop.

Do not run all skills. Documentation, state, tests, reviews, alternatives, and abstractions are
created only when they change implementation, adoption, recovery, or a material risk decision.


## 0.8.0 explicit and integration notes

- Use `$frontier-migration` explicitly for database, persisted-format, configuration, registration,
  identity, or public-contract migration phases. It is not implicit.
- Use `$frontier-verification` explicitly to create or revise a recurring project's
  Fast/Targeted/Subsystem/Full feedback profile. Ordinary targeted checks stay in `frontier-core`.
- Use `$frontier-review-governance` explicitly when a branch, PR, commit, or user claims a pure or
  behavior-preserving refactor and equivalence must be judged against an explicit base.
- FrontierLoop improvement observation stays inside `frontier-core`; detailed governance is loaded only
  when the user asks to propose or implement a FrontierLoop change. No observation triggers a write.

## Routing boundaries

A readable required Skill body may be loaded in the same task; no next-turn handoff is required.
A harmless command error with known absent effects is not Recovery. Persistence alone is not Security.
Review/audit completion means delivered findings and evidence, not an automatically repaired or passing product.
Mechanical micro-edits do not need Core or specialists. Other work keeps Core as the one owner.
