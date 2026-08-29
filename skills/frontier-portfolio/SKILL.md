---
name: frontier-portfolio
description: "Use ONLY when the decisive evaluator is genuinely missing or the solution structure remains materially uncertain after direct inspection. Do NOT load this Skill to decide whether a clear proposed service, Core promotion, cache, abstraction, or other mechanism is speculative; frontier-core or frontier-architecture must reject that directly when the approach and acceptance check are already clear."
---

# Frontier Portfolio

## Non-negotiable invariants

These are acceptance conditions, not suggestions.
If any invariant is false, the run is incomplete even when code compiles or tests pass.

- **ARTIFACT**: Produce or modify the real task artifact. A plan, portfolio list,
  state file, test, or report alone is not a completed run.
- **ROUTE**: Choose direct execution, evaluator construction, or a portfolio from
  the actual uncertainty. Skill invocation does not justify manufacturing alternatives.
- **BREADTH**: When a portfolio is justified, keep exactly two workstreams: the
  current best and one structurally different causal premise.
- **COMPARISON**: Pursue the same value, constraints, and evaluation context in
  both workstreams, then compare real, judgeable artifacts.
- **OWNERSHIP**: Keep implementation, technical evidence, and rollback with the
  agent. Keep taste and product direction with the human. Never ask the human to
  audit code or choose technical validity.
- **EVALUATOR**: Never promote a direction without a decisive check or a human
  judgment surface. If neither exists, build the smallest useful verification
  surface first.

## 1. Route the work

Recover only the state needed to choose a route:

- the value and real subject that must improve;
- the last accepted result and hard boundaries;
- the uncertainty that could change what gets built;
- the evaluator: a decisive check, human judgment, or neither.

Choose exactly one route:

- **Direct route**: Execute when the approach and decisive evaluator are clear.
- **Evaluator route**: When the user has fixed an approach, reference, or
  mechanism but available evidence does not determine how to verify it, build
  the smallest decisive verification surface and then execute that direction.
  Do not invent a structural alternative.
- **Portfolio route**: When unresolved solution structure could materially change
  the artifact, compare the current best with one structural option.

## 2. Build the portfolio

Use this section only for the portfolio route.
Maintain two workstreams until evidence makes one dominate:

1. **Current best**: improve or complete the strongest existing direction.
2. **Structural option**: open a different causal premise through a new
   reference, representation, mechanism, architecture, or product direction.

Color, labels, placement, and parameter values are not structural alternatives
unless one of them is the actual question.
Keep unselected work disposable.
Never keep a third simultaneous workstream.
If evidence invalidates both premises, close them before opening a replacement pair.

## 3. Judge validity and value

Use tests, traces, and metrics to establish technical validity.
Use representative artifacts under the same conditions to judge product value.

The human owns taste and product direction.
When a human-only fork would produce materially different work, recommend a
default and ask one closed question before doing fork-dependent work.

If one workstream dominates, close the other.
If neither wins, record the observation that changed the problem model and
replace the premise only when the route and evaluator remain valid.
Otherwise stop and leave the changed problem model for the next decision.
Do not average incompatible candidates or rename the same attempt.

## 4. Stop at a real boundary

Continue autonomously through reversible, in-scope work while a decisive
evaluator exists.
Stop at the first of:

- a representative artifact requiring human judgment;
- an approval, external action, or irreversible boundary;
- evidence that invalidates both premises when no justified replacement remains;
- no remaining move with positive decision value.

## 5. Leave a handoff

Leave the current artifact, observed difference, rejected premise, pending
decision, and exact next move.
Persist state only when an artifact, causal model, or decision changed.

## Mandatory completion gate

Check **ARTIFACT**, **ROUTE**, **BREADTH**, **COMPARISON**, **OWNERSHIP**, and
**EVALUATOR**.
If any invariant fails, continue the work or report the exact boundary.
Do not claim completion.

Read [`references/codex-adapter.md`](references/codex-adapter.md) when configuring
Codex instruction placement, long-running tasks, delegation, or controlled
evaluation.
Read [`references/interaction-profile.md`](references/interaction-profile.md)
only when a reusable communication profile is supplied or requested.
