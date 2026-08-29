# Runtime boundary

FrontierLoop 0.7.0 is an instruction-only Codex plugin.

It deliberately does **not** include or claim:

- `vh.exe`, a daemon, hooks, or a process supervisor;
- SQLite, Mission DB, an event ledger, or a second source of truth;
- atomic state transactions or exactly-once event processing;
- automatic recovery, reviewer identity, independent-model execution, or proof enforcement;
- hidden deployment, remote publication, credential, permission, or billing authority.

Interpret legacy Vibe Harness terms in adapted skills as follows:

| Legacy term | Plugin meaning |
|---|---|
| Harness | the active Codex agent operating under current instructions and tools |
| State | current observable repository state plus an existing handoff when needed |
| State event / ledger | an optional evidence label; never a persisted transaction claim |
| Checkpoint | an observed recovery point such as a verified commit, patch, or backup |
| Independent review | review performed in a genuinely separate context/agent/model and labelled with its actual independence; otherwise self-review |
| Runtime evidence | fresh direct evidence from the real program, environment, repository, service, or target system |
| Assurance A0-A3 | a risk-classification aid defined in `ASSURANCE_LEVELS.md`, not a machine-enforced gate |

Durable authority order:

1. latest explicit user instruction;
2. nearest applicable repository instructions such as `AGENTS.md`;
3. current code, configuration, Git identity, and fresh behavior evidence;
4. accepted ADR/handoff that has been reconciled with current reality;
5. historical notes and prior model claims.

Never invent an unavailable capability. When a procedure requires a separate reviewer, external
state query, persistence guarantee, or authorized tool that is unavailable, report the limitation
and use only the safest valid fallback.
