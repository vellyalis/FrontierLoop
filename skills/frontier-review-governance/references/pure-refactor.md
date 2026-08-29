# Pure Refactor Gate

Use this reference only when a change is presented as a pure or behavior-preserving refactor, or when the user explicitly asks whether a refactor is safe. It is FrontierLoop's independent equivalence-review contract and follows the same evidence, bounded-review, and fail-closed rules as the rest of the plugin.

## Contract

`pure_refactor: true` means the externally and internally relied-upon behavior of the reviewed range is equivalent before and after the change, except for explicitly allowed non-behavioral differences such as symbol location or name.

One material change to semantics, side effects, ordering, errors, public contracts, persistence, concurrency, performance guarantees, configuration, migration, or operational behavior makes the pure-refactor claim false. The change may still be correct and acceptable; classify it honestly and review it under the ordinary contract.

Do not infer equivalence from passing tests, similar-looking code, author intent, or a `refactor/` branch name alone.

## 1. Establish the comparison

Record:

- repository, branch/worktree, HEAD, and dirty state;
- explicit base supplied by the user or PR;
- otherwise, the unambiguous upstream/default-branch merge base;
- exact reviewed range and changed paths;
- the stated refactor purpose;
- required tests, traces, contracts, or other available oracles.

Do not fetch, unshallow, rewrite, or contact a remote merely to complete review unless the current task permits that external effect. If no trustworthy base can be derived locally, report `not_proven` and ask one closed base-selection question only when the answer is necessary.

## 2. Classify every changed path

Classify each changed path and relevant transformation as one or more of:

- move;
- rename;
- function or method extraction;
- inline;
- file/package/module reorganization;
- type alias or wrapper change;
- field/accessor or API access-path change;
- dependency/import rewiring;
- test relocation or test-ownership change;
- documentation/comment/format-only change;
- intentional behavior, configuration, migration, workflow, dependency, or build change.

The last class makes `pure_refactor: false`. Do not hide it inside a mostly structural diff.

## 3. Inspect semantic risk surfaces

For each affected surface, compare before, after, and callers/consumers. Resolve each credible risk to equivalent, changed, or not proven.

### Control and values

- conditions, branching, early returns, loop bounds, and short-circuit behavior;
- default values, constants, zero values, sentinel values, and environment-derived values;
- `null`/`nil`/missing versus empty collection, string, object, or optional value;
- type conversion, narrowing, precision, overflow, signedness, encoding, and normalization;
- return values, mutability, identity/aliasing, ownership, and copy versus reference behavior.

### Effects and ordering

- evaluation and side-effect order;
- initialization, registration, shutdown, cleanup, cancellation, and destructor/drop order;
- validation, filtering, authorization, caching, and transformation timing;
- retry count, timeout, fallback, deduplication, idempotency, and exactly-once assumptions;
- logs, metrics, events, notifications, and externally observed messages when they are contractual or operationally relied upon.

### Errors and contracts

- error type, wrapping chain, code, message, stack/cause preservation, and retry classification;
- panic/exception/crash behavior and recovery boundary;
- public API, ABI, schema, serialization, wire format, CLI, environment, config, and compatibility surface;
- visibility and package/module boundary changes that alter accessible behavior.

When wrapper depth changes, inspect the wrapper implementation before declaring behavior changed. An idempotent wrapper may preserve behavior; a non-idempotent wrapper may not.

### Concurrency and lifecycle

- lock acquisition order and scope;
- atomicity and memory visibility;
- channel/queue capacity, blocking, wakeup, and close behavior;
- task/thread/goroutine creation, join, cancellation, and ownership;
- event ordering, races, deadlocks, starvation, and lifecycle-owner changes.

### Persistence and external systems

- reader versus writer endpoint, transaction owner, isolation, commit/rollback timing;
- SQL/query shape, count, ordering, predicates, joins, locking, and result mapping;
- filesystem path, mode, atomic replacement, permissions, encoding, and cleanup;
- network destination, request method/body/headers, retry, timeout, and response interpretation;
- clock, randomness, locale, platform, device, process, and environment dependencies.

## 4. Trace affected call sites

Search all current references to moved, renamed, extracted, inlined, wrapped, or access-path-changed symbols.

For each distinct caller context, confirm:

- arguments and evaluation order are equivalent;
- receiver/state/lifecycle ownership is unchanged;
- return and error handling is equivalent;
- side effects occur the same number of times and at the same meaningful point;
- no caller was missed by dynamic registration, generated code, reflection, serialization, config, scripts, or external consumers.

Do not use `other occurrences` or `same as above` to conceal unverified locations. Mechanically identical occurrences may be grouped only when an exhaustive search proves the set; list every location in the group and show the common proof once.

## 5. Review tests without treating them as the contract

Existing tests should normally continue to pass unchanged for a pure refactor, so modified assertions, fixtures, snapshots, expected errors, timing, or ordering are strong evidence of a contract change.

Allowed test-only structural changes can include:

- file/package relocation;
- import/path/name updates caused by the refactor;
- helper ownership changes that preserve assertions;
- added characterization or regression tests that do not redefine expected behavior.

For every modified existing test, state whether its observable expectation changed. Passing tests prove only covered behavior; inspect uncovered risk surfaces directly.

## 6. Decide and report

Return:

```text
pure_refactor: true | false | not_proven
base: <ref or commit>
range: <base>...<head or exact diff>
```

Then include:

1. changed-path classification;
2. risky transformations and before/after/call-site evidence;
3. test-contract assessment;
4. mixed or intentional behavior changes;
5. unresolved equivalence risks;
6. ordinary `$frontier-review-governance` findings and adjudication.

Use `true` only when every material changed path is non-behavioral and principal equivalence risks are supported by direct evidence. Use `false` when any behavior or operational contract changed. Use `not_proven` when the base, callers, generated/external consumers, or required evidence cannot be established.
