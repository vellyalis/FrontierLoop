# Approval-gated FrontierLoop improvement governance

## Explicit scope already granted

One explicit user request may authorize both the named source fixes and their local installation.
Honor that concrete scope without asking the same approval again at each internal phase. Preserve
the baseline and validate before installation; do not infer publication, destructive actions, or
broader self-modification. The separate approval stages below apply when those stages were not
already granted. An audit or proposal alone still grants no implementation or installation authority.


## Contract

FrontierLoop never modifies its own source, an installed plugin, global skill directories, marketplace
registration, or any `AGENTS.md` automatically. Observation is not authorization. A proposal is not an
implementation. A validated candidate is not an active installation.

Git and the current repository remain the only durable source of truth. This workflow adds no daemon,
watcher, scheduler, hidden telemetry, database, background agent, or second state owner.

## Eligible evidence

Create a proposal only when at least one condition is true:

1. the same mechanism-level failure or useful tactic appears in two independent tasks;
2. one reproducible security, data-loss, permission, migration, or public-contract defect has material
   impact;
3. the user explicitly asks to improve FrontierLoop for a concrete observed gap.

A preference, one noisy run, model disagreement, speculative future benefit, or an isolated typo is not
cross-project evidence. Keep it task-local unless the user explicitly requests a proposal.

## Proposal states

- `observed`: evidence exists; no proposal file or source edit is authorized.
- `proposed`: the user asked for a written proposal; only the proposal artifact may be created.
- `approved_for_prototype`: isolated local implementation is authorized; the active installation stays unchanged.
- `validated_for_promotion`: the prototype passed its declared checks; promotion is still unauthorized.
- `approved_for_promotion`: merge and local installation are authorized within the stated scope.
- `rejected`: do not implement; preserve the reason when it prevents repeated reconsideration.
- `superseded`: a newer proposal owns the same issue.

Publication is deliberately not a proposal state. Push, PR, tag, marketplace publication, and Release
remain a separate external-action approval after local promotion.

## Gates

### 1. Observe and propose

Record only evidence that can change routing, correctness, safety, speed, recovery, or maintenance.
When the user asks for a proposal, create a `proposals/improvements/FIP-YYYYMMDD-short-name.md` file from
the template. The proposal must identify the existing rule gap, narrow change, expected outcome,
false-positive risk, rollback, removal condition, provenance, and evaluation cases.

Do not edit active skills while drafting the proposal.

### 2. Prototype approval

Require an explicit instruction that identifies the proposal or the exact change. Then:

1. inspect branch, worktree, status, dirty ownership, and active installation;
2. preserve existing work; use an isolated branch or worktree when the checkout is not safely owned;
3. change only the approved proposal scope;
4. leave the installed plugin and global instruction surfaces unchanged;
5. record the candidate diff and exact verification.

Approval to investigate or write a proposal is not prototype approval.

### 3. Validation

Use the smallest decisive checks plus material regression boundaries. For FrontierLoop changes this
normally includes:

- plugin schema and skill-set validation;
- implicit/explicit routing contracts and false-positive cases;
- no automatic source, install, marketplace, global-skill, or `AGENTS.md` mutation;
- no runtime, database, daemon, hook, MCP server, or second state owner;
- deterministic package build and archive safety when packaging changed;
- Windows installation lifecycle when installer behavior changed.

Read [`IMPROVEMENT_EVALUATION.md`](IMPROVEMENT_EVALUATION.md) and use
[`../templates/improvement-scorecard.md`](../templates/improvement-scorecard.md) for a promotion claim.
Preserve a concrete baseline and compare the candidate under the same conditions. Static markers alone are
insufficient for model-dependent routing or decision behavior; use repeated live Codex cases when those
behaviors are part of the claim.

Promotion evidence must show retained-capability regressions, capability gains, hard guardrails, automatic
surface cost, and any live or field evidence that can change adoption. Passing one blended score cannot hide
a safety, compatibility, or baseline-capability regression.

Move to `validated_for_promotion` only when the proposal's expected outcome is evidenced and residual
risk is explicit.

### 4. Promotion approval

Show the proposal, candidate diff, verification, installed-version delta, rollback point, and remaining
risk. Require explicit approval before merging the candidate or updating the active Personal Plugin.
Re-run verification against the exact promoted files and confirm there is one installed source.

Approval to prototype does not imply promotion.

### 5. Publication approval

Push, PR, merge, tag, marketplace update, or public Release requires a separate explicit approval.
Local promotion does not imply publication.

## Scope placement

- Cross-project stable rule: FrontierLoop Skill or shared reference, only after promotion approval.
- FrontierLoop repository maintenance rule: repository-local instruction or documentation.
- One project: that project's nearest `AGENTS.md`, Skill, or documentation—not FrontierLoop global behavior.
- One task: current request or handoff only.

Do not place a detailed workflow in global `AGENTS.md`. At most, a repository-local instruction may point
to this reference and restate the no-auto-modification and approval boundaries.

## Stop conditions

Stop when one of these is true:

- evidence is insufficient for a proposal;
- the user has not granted the next required approval;
- the candidate fails its decisive evaluation and no approved revision remains;
- promotion is complete and exact installed verification passes;
- the proposal is rejected or superseded.
