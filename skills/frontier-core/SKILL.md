---
name: frontier-core
description: "Own non-trivial software changes and reviews. Keep work proportional; add specialists only for material unresolved boundaries. Mechanical micro-edits need no workflow."
---

# Frontier Core

Own the requested engineering deliverable end to end; specialists supplement the
work rather than restarting it. Keep clear local work direct and proportionate.

## Authority and deliverable

- Preserve user changes and respect current host, user, and repository authority.
  Inspection or review is not implementation approval. Explicit authorization to
  fix this bundle covers the named local source and installation, not publication.
- Complete the requested kind of work: an audit can finish with findings and a
  failing product verdict; implementation requires the integrated behavior and
  its material checks. A verified no-change result can also satisfy the request.
- Continue safe authorized implementation, runtime inspection, repair, and
  affected tests without asking at every step. Stop only at a real boundary,
  not after an initial patch or a transition to another Skill.
- Do not silently modify FrontierLoop, installed plugins, global skills, or
  `AGENTS.md` during unrelated work. Publication and irreversible effects remain
  separate authority boundaries; already granted scope does not need reapproval.
- FrontierLoop is instruction-only. Git and existing project artifacts own
  durable state; no daemon, SQLite ledger, independent reviewer, or exactly-once
  guarantee is supplied by this Skill.

## Working judgment

Inspect the affected owner and applicable instructions, confirm the gap, implement
the smallest responsibility-correct change, and decide acceptance with the
smallest sufficient existing check plus material regression/runtime boundaries.
For review-only tasks, inspect and report instead of implementing.

Keep data ownership/lifetime, responsibility, Module/Core placement, contracts,
verification, failure visibility, and cleanup in the decision. Record only what
changes the implementation or risk treatment; no mandatory nine-field report.
Do not require ADRs, receipts, a full test suite, a repository map, or a new
verification framework for a clear local change.

Use one canonical state and invariant owner. Keep cohesive behavior together;
split independent responsibilities, not files by line count. Reuse needs real
consumers or a hard public/security/ABI boundary. Reject speculative mechanisms
directly when the simpler answer is already clear.

## Conditional references

- Read [Engineering Judgment](references/ENGINEERING_JUDGMENT.md) before a material
  state/ownership/lifetime, module/Core, dependency, persistence/public-contract,
  concurrency, measured-resource, migration, fallback, authorization, or recovery
  decision. Mechanical micro-edits do not load it; high-assurance Routine work
  still does when one of these boundaries is affected.
- Read [Assurance levels](references/ASSURANCE_LEVELS.md) when risk classification
  changes proof or approval; [runtime boundary](references/RUNTIME_BOUNDARY.md)
  only when a workflow claims enforcement, persistence, or reviewer independence.
- For a requested change to this bundle itself, use
  [improvement governance](references/IMPROVEMENT_GOVERNANCE.md); for a claim that
  model behavior improved, use [evaluation](references/IMPROVEMENT_EVALUATION.md).
  Source integrity or fewer bytes alone does not prove better model behavior.

## Specialist selection

Read the exact applicable body before applying its procedure. A readable body may
be loaded in this same task; do not require another user turn. Use matching
specialists only for distinct material boundaries, with Core remaining owner.

- `frontier-debug-investigation`: unknown, intermittent, layered, recurring, or
  failed-fix causes; not an already proven local cause and fix.
- `frontier-architecture`: material ownership, lifetime, Module/Core placement,
  dependency direction, public contract, deployment, or failure-boundary decisions.
  A data-flow mechanism change with those boundaries proven unchanged is not
  independently an Architecture trigger. Performance may own it. Migration may
  own schema coexistence without another Architecture workflow.
- `frontier-security-review`: changed trust, authorization, secrets, privacy,
  untrusted input, external effects, or supply-chain risk. Merely mentioning a
  database, persisted file, or dependency does not activate it.
- `frontier-performance-engineering`: a concrete resource goal or regression,
  including polling/scanning costs; measurement may be the first task.
- `frontier-portfolio`: an evaluator or solution structure still materially
  unresolved after direct inspection, not an obvious speculative proposal.
- `frontier-recovery`: actual interrupted, partial, conflicting, or uncertain
  effects. Not design-time recoverability or a harmless, understood command error.

Other Skills are explicit-only helpers. A user request or a loaded workflow may
request the relevant procedure in this same task when its unresolved decision
requires it. Routine classification alone does not activate `frontier-routine-change`;
a proposed abstraction alone does not activate `frontier-complexity-review`.

## Verification and stopping

Derive proof from the requested behavior and real failure boundaries. Do not
manufacture alternatives, infrastructure, or extra review rounds when the next
safe action is clear. Change an uninformative repeated experiment rather than
repeating it. Do not label self-review independent or missing evidence successful.

For implementation, fix caused failures, check relevant runtime behavior, and
finish required cleanup. Stop checking when further evidence cannot change
acceptance or material risk. Report outcome, decisive evidence, remaining risk,
and material NotRun work; preserve a compact handoff only when continuation needs it.
