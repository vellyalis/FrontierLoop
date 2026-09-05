# Public contract lane

Apply this lane when a change affects an API, MCP/ACP/Tauri command, plugin manifest, persisted file,
configuration shape, database schema, event format, or another observable boundary.

- Define typed or otherwise machine-checkable input, output, error, ordering, idempotency, and lifecycle
  behavior before changing the implementation.
- Treat every observable behavior as a potential dependency. Avoid exposing internal paths, provider
  details, timing assumptions, raw exceptions, or mutable implementation state unless they are intended
  contract.
- Validate untrusted input and third-party responses at the boundary. Do not scatter duplicate validation
  through already-typed internal code.
- Prefer additive optional fields and compatible readers/writers. Do not rename, remove, or reinterpret an
  existing field in place merely because the new shape is cleaner.
- Keep error semantics predictable and sanitized across the boundary; separate machine-readable identity
  from human explanation.
- When old and new consumers must coexist, hand the change to the explicit `$frontier-migration` workflow
  instead of hiding migration inside the architecture edit.
- Record the compatibility promise, deprecation trigger, rollback or forward-repair path, and the exact
  observation that proves old and new consumers remain safe.

Do not create API versioning, pagination, an adapter, or a migration framework without a current consumer
or failure that requires it.
