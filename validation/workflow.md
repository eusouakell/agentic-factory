# Agent validation workflow

Status: **operational contract**.

This workflow defines how a registered agent moves from unproven capability to validated lifecycle state without allowing the agent to self-promote.

## Scope

Applies to all agents in `agents/registry.json`.

It governs:

- real-task validation;
- evidence capture;
- promotion recommendations;
- human lifecycle decisions;
- revalidation after material contract changes;
- demotion when evidence no longer supports the active status.

It does **not** grant tool authority or replace domain-specific human gates.

## State model

```text
REGISTERED / PILOT
      ↓
TASK SELECTED
      ↓
TRIGGER + SCOPE CONFIRMED
      ↓
AUTHORIZED RUN
      ↓
EVIDENCE CAPTURED
      ↓
OUTCOME CLASSIFIED
      ├── validated_once ───────→ PROMOTION CANDIDATE
      │                               ↓
      │                           HUMAN GATE
      │                          ↙          ↘
      │                     APPROVE       DECLINE
      │                        ↓              ↓
      │                      ACTIVE         PILOT
      │
      ├── needs_more_evidence ─────────────→ PILOT
      │
      ├── boundary_problem ─→ CONTRACT REVISION ─→ NEW VALIDATION
      │
      └── failed ─────────────→ PILOT / RETIRE DECISION
```

Lifecycle state in the registry remains:

`pilot → active → retired`

Validation workflow states are evidence/process states, not new registry lifecycle values.

## 1. Task selection

A valid test must be a **real task**, not a synthetic prompt demo.

The task should have at least one consequence such as:

- a repository decision;
- a pull request;
- an audit finding;
- a production-readiness recommendation;
- a design or architecture artifact;
- a test/tooling change;
- a research-backed strategy decision.

### Guard

Do not select a task only because it is easy for the agent to pass.

## 2. Trigger and scope confirmation

Before execution, record:

- why this agent's trigger applies;
- which inputs are authoritative;
- allowed tools;
- write authority;
- required checks/evals;
- human gate;
- known exclusions.

If two agents claim the same decision authority, stop and classify as a potential `boundary_problem`.

## 3. Authorization

The control plane authorizes the run.

The agent cannot:

- widen its own tools;
- activate another agent outside routing;
- change its own lifecycle;
- bypass a Guard or required human gate.

## 4. Execute

Run the task inside the declared authority.

Executor agents may write only to the authority class in their contract.

Auditors/evaluators with `review_only` authority emit findings, reviews or issues rather than silently applying their own remediation.

## 5. Evidence capture

A validation record belongs in:

`validation/runs/YYYY-MM-DD-<agent>-<task>.md`

Minimum fields:

- date;
- agent ID;
- outcome;
- task;
- trigger;
- inputs/scope;
- work performed;
- evidence;
- useful contribution;
- corrections or failed assumptions;
- authority-boundary result;
- limitations;
- promotion recommendation.

Machine-readable indexing belongs in:

`validation/index.json`

## 6. Outcome classification

### `validated_once`

Use when:

- the task was real;
- the role contributed distinct value;
- authority boundaries held;
- evidence is inspectable;
- no unresolved role collision remains.

This makes the agent **eligible for a promotion recommendation**, not automatically active.

### `needs_more_evidence`

Use when:

- the run was useful but did not exercise enough of the contract;
- critical behavior could not be tested;
- the result depends on untested rendered/runtime behavior.

The agent remains pilot.

### `boundary_problem`

Use when:

- two roles claim the same decision;
- the agent attempts authority that belongs to control plane/domain authority/human gate;
- trigger or write-authority boundaries are ambiguous.

Fix the contract first. Then use a **new validation run**.

### `failed`

Use when the agent:

- produces materially unreliable output;
- misses a consequential known constraint;
- creates unsafe/unbounded behavior;
- cannot recover within its retry policy.

A failed run does not automatically retire the agent. Human review decides whether to revise, keep pilot or retire.

## 7. Retry policy

Validation is not a retry-until-pass loop.

Allowed:

- correct factual/implementation errors found during an otherwise valid task;
- re-run deterministic checks after remediation;
- one evidence-record correction when the record itself is incomplete.

Not allowed:

- repeatedly reframe the same failed test until it becomes a pass;
- remove a failed observation from the record;
- weaken the contract after failure solely to make the run conform.

A substantive contract change requires a new validation run.

## 8. Promotion gate

Promotion requires all of:

1. at least one `validated_once` real-task record;
2. evidence that the role reduced ambiguity, risk or rework;
3. no unresolved `boundary_problem`;
4. registry + contract synchronization;
5. applicable CI green;
6. explicit human approval.

Promotion is implemented through a dedicated PR changing lifecycle fields.

The validation record may say:

`candidate_active_pending_human_approval`

It may not change its own lifecycle.

## 9. Activation semantics

`active` means:

> this capability has passed the lifecycle evidence gate.

It does **not** mean:

- always-on;
- autonomous;
- enabled by default;
- permitted to skip routing;
- permitted to self-call.

`enabled_by_default` remains a separate control-plane decision.

## 10. Revalidation

Revalidate an active agent when a material change affects:

- purpose;
- trigger;
- role type;
- tool scope;
- write authority;
- human gate;
- retry/escalation;
- major domain responsibility.

Minor wording or provenance changes do not require automatic revalidation.

## 11. Regression / demotion

If an active agent later shows a consequential boundary or reliability failure:

```text
ACTIVE
  ↓
REGRESSION EVIDENCE
  ↓
HUMAN REVIEW
  ├── minor / remediated → ACTIVE + record
  ├── contract change ───→ PILOT + revalidation
  └── capability no longer useful/safe → RETIRED
```

Demotion is a lifecycle PR with explicit rationale.

## 12. Human decision record

When a promotion/demotion PR is merged:

- record the PR in `validation/index.json`;
- do not rewrite historical run conclusions;
- add a separate `decision` field such as:
  - `promoted_active_via_pr_8`;
  - `remained_pilot_via_pr_X`;
  - `retired_via_pr_Y`.

Historical evidence stays immutable except for factual corrections.

## Operational invariants

- Evidence precedes promotion.
- A reviewer cannot approve its own authority expansion.
- A successful CI run is not semantic validation.
- A real task may involve several agents, but each role's contribution must remain distinguishable.
- Human approval is an explicit state transition, not an assumption.
- Failure remains visible.
