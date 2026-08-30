# Vibe Harness Runtime Notices

Vibe Harness Runtime source is offered under the repository's `MIT OR Apache-2.0` license declaration.

The compiled Runtime is resolved by the checked-in `Cargo.lock`. The local release-candidate Gate
used `cargo-audit 0.22.2` against RustSec advisory database commit
`0bfde9d6a469ae503f8a6147c2dd552856cd5999` (updated 2026-07-27T13:27:01-04:00):
87 resolved dependencies, 0 known vulnerabilities, and 0 informational warnings.

Cargo metadata reported 81 registry packages and no missing license expression. The resolved
expressions are permissive combinations of MIT, Apache-2.0, Apache-2.0 WITH LLVM-exception,
BSD-2-Clause, BSL-1.0, Unicode-3.0, and Unlicense. A distribution operator must rerun both
advisory and license checks against the exact lockfile and current databases at release time.

Development-only requirements, detailed designs, evaluation scenarios, Aelyris integration material, and implementation prompts are not part of the end-user Runtime payload.
