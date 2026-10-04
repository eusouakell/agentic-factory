# Codex execution surface

Status: **approved interactive execution surface**.

## Why

Codex is useful when work benefits from:

- browser/IDE interaction;
- seeing a rendered surface while editing;
- iterative debugging with Kell;
- repository-local implementation;
- visual/product feedback during execution.

The Agentic Factory should not duplicate those strengths.

## Relationship to agents

Codex is **not** a privileged agent role.

The control plane gives Codex a task packet that names the agent contract(s) it is executing.

Example:

```text
execution_surface: codex
primary_agent: frontend-engineer
review_agents:
  - accessibility-auditor
  - code-reviewer
domain_authority:
  - Flame
human_gate:
  - Kell
```

Codex may collaborate with Kell during the task, but the declared agent authority still applies.

## Task packet

A Codex handoff should include:

1. **Goal** — concrete outcome.
2. **Repository / branch**.
3. **Primary agent contract**.
4. **Canonical domain sources**.
5. **Acceptance criteria**.
6. **Hard Guards**.
7. **Checks to run**.
8. **Semantic evals/reviewers after execution**.
9. **Human gate**.
10. **Known open questions**.

## Return packet

Codex should return:

- branch/PR;
- files changed;
- tests/checks run;
- screenshots/rendered observations when relevant;
- deviations from the task packet;
- unresolved uncertainty;
- what Kell decided interactively;
- what still requires independent review.

## Important separation

Kell collaborating with Codex during implementation is a valid human-in-the-loop execution mode.

It does **not** replace independent semantic review when the primary executor is also capable of self-critiquing.

For consequential work, prefer:

```text
Codex executes
→ separate agent/eval reviews
→ Kell approves
```

rather than:

```text
Codex executes
→ Codex says its own work is excellent
→ merge
```
