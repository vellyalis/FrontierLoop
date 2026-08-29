# Project Flow Profile

Use this reference only when a recurring project needs a persistent development-flow profile. The profile
records project-specific commands and escalation boundaries;
`frontier-verification/SKILL.md` remains the reusable policy owner.

## Placement

Prefer, in order:

1. an existing development/testing section in the nearest project `AGENTS.md`;
2. an existing contributor, testing, or engineering guide;
3. one managed block in the nearest project `AGENTS.md` when no canonical location exists.

When using a managed block, use exactly one pair of markers:

```markdown
<!-- frontier-flow:start -->
## Frontier development flow

...
<!-- frontier-flow:end -->
```

The legacy `frontier-flow` marker name is retained so existing project profiles can be updated in place
instead of duplicated during migration to FrontierLoop 0.6.0.

Update the existing block in place. Never modify content outside it as a side effect of flow optimization.

## Minimal profile

```markdown
<!-- frontier-flow:start -->
## Frontier development flow

### Command ladder

| Tier | Command | Scope | Run when |
|---|---|---|---|
| Fast | `<command>` | `<syntax/static/local scope>` | Every relevant edit loop |
| Targeted | `<command>` | `<changed behavior>` | Before claiming the local fix works |
| Subsystem | `<command>` | `<package/integration boundary>` | When `<closed trigger>` is touched |
| Full | `<command>` | `<repository/release scope>` | At `<release or risk boundary>` |

### Escalation triggers

- `<public/schema/persistence/security/concurrency/platform/release condition>`

### Test admission

- Add or change a test only for a changed acceptance condition, reproduced defect,
  material boundary, high-impact regression, or refactor contract.
- Do not add duplicate or speculative coverage.

### Evidence basis

- Last reconciled: `<YYYY-MM-DD>`
- Observed: `<only the evidence that changed this routing>`
<!-- frontier-flow:end -->
```

## Profile rules

- Commands must be executable from a stated project-relative working directory or use the project's canonical task runner.
- Do not copy every CI job into the local ladder. Reference a canonical aggregate command when one exists.
- Do not turn one machine's duration into a universal threshold. Record an observed duration or range only when it changed routing.
- Do not list a Full command as optional when project policy makes it required.
- Do not claim a Targeted command covers generated, dynamic, external, or cross-platform consumers without evidence.
- Keep the profile compact. Replace stale evidence instead of accumulating a permanent command log.
- When local and CI behavior diverge, state the difference explicitly and keep CI as the authority for protected remote gates.
