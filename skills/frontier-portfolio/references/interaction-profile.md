# Interaction profile

An interaction profile changes presentation and steering preferences.
It cannot change product goals, truth, workstream count, responsibility,
evidence requirements, or permission boundaries.

Place persistent cross-project preferences in the global `AGENTS.md`.
Use a local profile only when a narrower preference is worth reusing:

```yaml
version: 1
response:
  language: ja
  tone: inherit
  density: compact
  evidence_order: artifact-first
status:
  cadence: stage-boundary
  include_current_move: true
presentation:
  recommendation_first: true
steering:
  pause_at_next_judgeable_artifact: true
```

Allowed concerns:

- language, tone, density, and formatting when a stronger instruction has not
  fixed them;
- update cadence and evidence order;
- labels and order used to present an existing comparison;
- an earlier pause within the skill's existing stop and permission boundaries.

Forbidden concerns:

- product goals, priorities, acceptance criteria, or workstream count;
- technical validity, code-audit ownership, or the human decision boundary;
- permission for external, irreversible, or out-of-scope actions;
- weaker evidence in exchange for a shorter response;
- a forced solution when current evidence requires another.

Without a profile, follow the active `AGENTS.md` instructions.
If none specify presentation, lead with the observed outcome, name the next
move, and ask only when a human-only choice materially forks the work.
