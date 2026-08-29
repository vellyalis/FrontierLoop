---
name: frontier-core
description: "Use for every non-trivial software change in any repository, including implementation, fixes, refactors, tests, review, documentation, and configuration. Load this Skill even when a narrow specialist is also used: specialists supplement frontier-core and never replace its Work Unit ownership. Apply a lightweight engineering change gate for data ownership and lifetime, responsibility, module and Core placement, API and contracts, verification, observability, and cleanup. When a structural trigger such as source-of-truth/ownership/lifetime, any decision to promote feature behavior into Core, material Module/Core placement or dependency direction, persistence, concurrency, continuous work, measured resource budget, migration, fallback, authorization, or recovery is present, actually read the canonical Engineering Judgment reference before the final engineering decision. A clear speculative Core-promotion proposal is decided directly by Core (and Architecture only when its real boundary is material); do not load frontier-portfolio or frontier-complexity-review merely to reject obvious speculative reuse. For an explicitly behavior-, state-, contract-, owner-, and lifetime-neutral micro-edit, stay on the micro fast path: do not open Engineering Judgment or a specialist merely to confirm non-activation. Also apply direct-first execution, anti-overthinking, anti-overengineering, balanced modularity, finite review, safe Git, and lightweight continuation."
---

# Frontier Core

## Purpose

Move the real deliverable forward with the smallest process that can make a material decision.
This is FrontierLoop's always-available core. It is self-contained: correct routine behavior does
not depend on another skill being loaded through a router.

## Authority and safety

1. Follow the latest explicit user instruction and the nearest applicable repository instructions.
2. Preserve pre-existing user changes. Do not reset, clean, stash, overwrite, or reassign them to
   simplify the task.
3. Safe, in-scope, reversible local reads, edits, and targeted checks may proceed directly.
4. Obtain authorization before external publication, paid actions, credential or permission
   changes, destructive or irreversible operations, or product-direction changes.
5. FrontierLoop is instruction-only. It has no `vh.exe`, daemon, SQLite state, event ledger,
   exactly-once guarantee, or second lifecycle owner.
6. Never modify FrontierLoop source, an installed plugin, a global skill catalog, or any
   `AGENTS.md` automatically. Improvement observation, prototype, promotion, and publication
   are separate authority boundaries.

## Direct-first execution

When outcome, change surface, likely solution, and decisive acceptance check are clear:

1. inspect only the relevant repository state and nearest instructions;
2. confirm the behavior is not already satisfied;
3. implement the smallest coherent change that reaches the requested outcome;
4. run the smallest decisive verification plus any material regression boundary;
5. report the changed artifact, evidence, residual risk, and anything not run.

Do not create a Goal Model, ADR, benchmark harness, new test framework, alternative design,
review round, state database, or handoff unless it can change implementation, adoption, recovery,
or a material risk decision.

## Engineering change gate

Apply this lightweight gate to every non-trivial change while keeping the gate inside the work. Record
only answers that affect implementation, adoption, recovery, or material risk; do not require a separate
plan or document. A typo, private local rename, or similarly obvious mechanical micro-edit that changes no
behavior, data, contract, owner, lifetime, or boundary stays lightweight: preserve current state, make the
edit, run the obvious check when one exists, and stop.

When the request or direct evidence already establishes that behavior, state, ownership, lifetime,
contracts, boundaries, and diagnostics are unchanged, that negative activation decision is complete.
Do not open `references/ENGINEERING_JUDGMENT.md`, glob for that reference, or load a specialist merely to
confirm that the Doctrine does not apply. Open the Doctrine only after a positive material trigger is
identified.

### Structural engineering judgment

The trigger list below is mandatory. Once any listed trigger is positively identified, do not finalize the
engineering decision from this Skill alone: actually read the canonical Doctrine first.

Before selecting an implementation, read
[`references/ENGINEERING_JUDGMENT.md`](references/ENGINEERING_JUDGMENT.md) when the change
materially alters or depends on representation or source of truth, ownership or lifetime, invalidation,
module or Core placement, dependency direction, persistence or an external contract, concurrency or shutdown,
caching/polling/scanning/background work, queues or retries, a measured resource budget, migration, fallback,
authorization, recovery, or irreversible failure semantics.

The shared doctrine is a conditional decision reference, not a second router or workflow owner. Keep Routine
local edits direct. Use only the narrow specialist whose boundary changes handling, and do not load the whole
catalog merely because several doctrine fields can be named.

### Data

Identify canonical state, its owner, creation and disposal points, mutation and consumption paths, and
lifetime. Account for persistence, transfer, stale references, cancellation, and cleanup when present.

### Responsibility

Name the behavior and change reason being altered. Keep it with the owner of its state and invariants; do
not add an independent responsibility to a convenient large file or create a second semantic owner.

### Module placement

Place behavior in the module that owns its responsibility, dependencies, I/O boundary, and focused test
seam. Split only for a materially independent change reason, invariant, lifecycle, recovery path, contract,
or trust boundary; reject generic buckets and pass-through wrappers.

### Core placement

Keep feature-specific behavior in its feature module. Put policy or primitives in Core only when they are
stable across at least two real consumers or protect a hard public, ABI, security, or canonical-state
boundary. Reject speculative Core promotion, but move a real shared invariant to its canonical owner when
leaving it local would duplicate authority or reverse dependency direction.

### API and contract

Prefer an internal call when no observable boundary is required. For a real API, command, schema, format,
or configuration surface, define input, output, errors, ordering, idempotency, compatibility, and lifecycle
semantics in proportion to the contract and route material public-contract changes to architecture.

### Verification

Derive proof from changed behavior, data lifetime, contract, failure modes, and regressions. Run the
smallest decisive existing check plus material boundaries; never use a passing shared-premise test as the
only evidence for a claim it cannot falsify.

### Observability

Ensure success, failure, ownership transfer, and cleanup are visible where operations or recovery require
them, preferring existing typed errors, logs, metrics, and status surfaces. Do not add instrumentation to an
obvious micro-edit or create a new telemetry system without a current diagnostic or operational need.

### Cleanup

Remove superseded code, flags, adapters, configuration, tests, and documentation once their real consumers
have crossed the bounded transition. Preserve recoverability and active contracts, but do not leave dual
owners or an unbounded legacy path.

### Smallest coherent change

Choose the responsibility-correct smallest change: the smallest complete vertical slice that satisfies the
full goal with data and lifetime under the right owner, behavior in the right module or Core boundary,
contracts explicit, decisive verification and needed observability present, and superseded paths cleaned up.
Fewest changed lines is not the criterion.

## Anti-overthinking

- Stop researching when the next safe implementation or discriminating experiment is clear.
- Do not generate multiple hypotheses for a clear local fix.
- Do not restate the same plan in new wording, count token use or tool calls as quality, or treat
  analysis volume as progress.
- When two attempts under the same premise and method produce no information or improvement,
  change the representation, evidence source, experiment, mechanism, or boundary instead of tuning.
- Ask only when the answer changes scope, responsibility, irreversible action, product direction,
  or another decision that cannot be inferred safely. Prefer a recommendation with closed options.

## Anti-overengineering

Before adding a dependency, service, framework, storage layer, queue, cache, plugin system,
concurrency owner, reusable abstraction, configuration surface, or new operational component:

1. identify the current requirement or observed risk;
2. compare the simplest valid existing or local alternative;
3. require concrete evidence that the simpler option is insufficient;
4. account for ownership, runtime, failure, security, test, migration, rollback, and removal cost;
5. accept only complexity that is traceable to the current goal and can be owned now.

Future possibility, pattern purity, aesthetic symmetry, or hypothetical reuse is not sufficient.
A reusable abstraction normally needs at least two real consumers, unless it protects a public,
ABI, security, or similarly hard boundary.

## Balanced modularity

Prevent both monolithic growth and ceremonial fragmentation.

Separate a boundary when one or more of these are materially independent:

- change reason or responsibility;
- state or invariant ownership;
- lifecycle, cancellation, or failure recovery;
- I/O or side effects;
- dependency direction or public contract;
- focused verification seam or security boundary.

Keep code together when behavior, state, invariants, lifecycle, and change reason are cohesive.
Line count is a warning signal, not a verdict. A pass-through wrapper, one-function file,
`utils/common/helpers/shared` bucket, or interface with one speculative consumer is not modularity.
Do not keep adding an independent responsibility to a large file merely to avoid creating a real
boundary.

## Proportional verification and review

### Routine verification fast path

- For a clear, reversible change, implement first and run the smallest decisive existing check plus
  any material regression boundary. Do not require a test plan, receipt, separate document, new
  framework, or full suite before editing unless repository policy requires it.
- Start with existing tests, focused commands, direct observation, or boundary reproduction. Expand
  only when the first check fails, a material acceptance claim remains undecided, a new risk boundary
  appears, or the repository explicitly requires broader coverage.
- An obvious regression or boundary test needs no separate rationale when its name, setup, and
  assertions already identify the failure it protects.

### Expanded verification gate

- Use a brief decision-relevant rationale only for material verification work: a new runner or
  framework, large fixture or corpus, benchmark/evaluation harness, expensive integration or E2E,
  broad generated cases, high-impact security/migration/data-integrity proof, or coverage that may
  duplicate an existing surface.
- Keep that rationale in the current work report or existing project record unless repository policy
  requires a dedicated artifact. State the claim or failure, missed-failure impact, existing coverage
  gap, decision the result can change, and why existing infrastructure is insufficient.
- Do not use a fixed production-to-test ratio as a gate or target. Never delete necessary regression
  proof, inflate production code, or collapse independent failures into an opaque test to satisfy a metric.
- Verification-only work must not displace the deliverable. High-impact proof may be larger than the
  code change, but every material artifact must remain traceable to a concrete decision or risk.
- Record `Pass`, `Fail`, `Partial`, or `NotRun`; never upgrade missing evidence into confidence.
- Stop verification when required claims are decided and another check cannot change implementation,
  adoption, rollback, or residual-risk treatment.
- Stop review when no unresolved, evidence-backed blocker remains. Do not let review invent new
  requirements, duplicate findings, or create an infinite rework loop.

## Approval-gated FrontierLoop evolution

FrontierLoop may learn from repeated evidence, but it never silently rewrites itself or the active
instruction surface.

- A one-off failure remains task-local unless the user explicitly asks for a FrontierLoop proposal.
- A repeated cross-task pattern, a concrete high-impact defect, or an explicit user request may justify
  an improvement proposal. Drafting the proposal does not authorize implementation.
- **Prototype approval** authorizes only isolated local edits in a preserved branch or worktree. It does
  not authorize replacing the installed plugin, changing global skills, or editing global `AGENTS.md`.
- After focused routing, safety, packaging, and regression evidence is shown, **promotion approval** is
  required before merging or installing the candidate as the active FrontierLoop source.
- Push, PR, tag, marketplace update, or public Release requires separate **publication approval**.
- Keep Git and repository files authoritative. Do not add a watcher, daemon, scheduler, database, hidden
  feedback channel, or automatic self-update mechanism for this workflow.

When improving FrontierLoop itself, read
[`references/IMPROVEMENT_GOVERNANCE.md`](references/IMPROVEMENT_GOVERNANCE.md) and use
[`templates/improvement-proposal.md`](templates/improvement-proposal.md). Do not load that process for
ordinary project work.

Before claiming that a candidate is better, also read
[`references/IMPROVEMENT_EVALUATION.md`](references/IMPROVEMENT_EVALUATION.md) and use
[`templates/improvement-scorecard.md`](templates/improvement-scorecard.md). Preserve the prior version,
measure retained capability and hard guardrails, and use repeated live evidence for model-dependent behavior.

## Git and continuation

- Inspect branch, worktree, status, and relevant diff before Git-affecting work.
- Do not include unrelated paths, alter protected history, push, publish, merge, tag, or release
  without the applicable instruction or authorization.
- Use Git, current files, nearest instructions, and an existing repository handoff as durable truth.
- Create or update a handoff only for work that actually spans sessions or machines, and keep it to
  verified state, owned dirty paths, accepted/rejected decisions, residual risk, and the exact next
  action. Do not create a parallel Mission database.

## Specialist escalation

Frontier Core owns every non-trivial change end to end. Add only the narrow specialist whose material
uncertainty or boundary requires its full procedure:

Each matching bullet below is a positive activation contract, not an optional suggestion. Before making the
final engineering decision, actually open and read every matching specialist `SKILL.md`. Naming a specialist,
using only Frontier Core, or reading only `ENGINEERING_JUDGMENT.md` does not satisfy specialist activation.
When independent triggers coexist, load each matching specialist while keeping Frontier Core as the one Work
Unit owner. Do not add a specialist whose trigger is absent.

- `$frontier-debug-investigation` for unknown, intermittent, layered, recurring, or failed-fix bugs;
- `$frontier-architecture` for ownership, lifecycle, data-flow, material Module/Core placement,
  dependency-direction, public-contract, storage, deployment, or failure-boundary changes, including
  moving behavior into or out of Core and replacing stale cached, scanned, or mirrored state with a direct
  authoritative read even when the canonical owner itself remains unchanged;
- `$frontier-security-review` for secrets, auth, permissions, untrusted input, external effects,
  persistence/migration, privacy, or supply-chain risk;
- `$frontier-performance-engineering` for every measured performance goal or regression, including a
  measured frame-time cost caused by polling, scanning, or continuous background work;
- `$frontier-portfolio` when the decisive evaluator or solution structure is materially uncertain;
- `$frontier-recovery` after interruption, uncertain effects, stale state, failed migration, or
  worktree confusion.

Do not multiply specialists from vocabulary overlap. When explicit `$frontier-migration` already owns a
persisted-schema or format coexistence plan and the canonical owner plus independent public boundary stay
unchanged, do not add `$frontier-architecture` merely because persistence or storage is involved. Likewise,
future interruption-safety, rollback, or recoverability is a migration design obligation; do not add
`$frontier-recovery` unless an actual interruption, failed migration, partial effect, stale state, or
uncertain outcome already exists.

A narrow performance mechanism replacement is not automatically an Architecture Workstream. If the
canonical owner, lifetime, public contract, module ownership, and dependency boundary are already proven
unchanged, and `$frontier-performance-engineering` plus the shared Doctrine fully owns replacing continuous
polling/scanning with an authoritative on-demand read, Architecture is optional rather than mandatory. Add
it only when the data-flow change also changes or leaves material uncertainty about one of those boundaries.

Do not auto-load the explicit-only `$frontier-complexity-review` merely because a request proposes a new
service, abstraction, cache, layer, or Core promotion. When Frontier Core or the already-triggered
Architecture specialist can directly reject obvious speculative complexity from current evidence, make that
decision there. Use `$frontier-complexity-review` only when the user names it or an already-loaded workflow
explicitly hands off a still-material admission decision that cannot be closed directly.

Use the explicit-only `$frontier-migration` when the user asks to design or execute a compatible
database, persisted-format, configuration, plugin-registration, provider-identity, or public-contract
migration. It does not activate merely because an ordinary change touches a file named migration.

All other FrontierLoop skills remain available for explicit use. Escalate only the uncertainty or
risk that is actually present; do not run the whole catalog.

## Completion

A task is complete when the requested artifact is materially updated, required claims are decided,
material regressions or blockers are absent, residual uncertainty is explicit, and the next action
is not being withheld merely to continue analysis, testing, review, or documentation.

For every non-trivial change, report compactly:

- **Data**: canonical state, owner, lifetime, and invalidation;
- **Responsibility**: the owner changed or reused;
- **Module/Core**: placement decision and reason;
- **API**: public/private contract impact;
- **Tests**: `Pass`, `Fail`, `Partial`, and material `NotRun`;
- **Observability**: existing or added failure visibility;
- **Cleanup**: removed or deliberately retained old paths;
- **Evidence**: commands, runtime observations, or direct artifacts;
- **Residual risk**: remaining material uncertainty.

An item may be `No change`; state the reason when material. Do not require this expanded report for
typo-only, format-only, or presentation-only micro-edits that cannot affect behavior, state,
contracts, dependencies, or diagnostics.
