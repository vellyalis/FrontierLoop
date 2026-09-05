# Assurance levels

These labels are a lightweight risk aid retained from the Vibe Harness source. They do not create
a runtime gate or permission.

| Level | Typical impact | Expected treatment |
|---|---|---|
| A0 | reversible prototype, no real data or external effect | direct local proof; easy rollback |
| A1 | ordinary feature or bounded regression risk | targeted positive/boundary verification |
| A2 | auth, payment, PII, persistence, migration, public API, important concurrency | negative cases, integrity/recovery proof, stronger review when available |
| A3 | irreversible external effect, serious data loss, release/permission/history boundary | explicit authorization, recoverability, and genuinely independent review or a clear blocked status |

Classify risk independently from task difficulty. A difficult algorithm can be A0/A1; a one-line
permission or migration change can be A2/A3. Repository policy and explicit user instructions take precedence.
