# First-class agents

## Decision

Specialist agents are **first-class system entities** in the Agentic Factory.

That does not mean autonomous or privileged. It means the system can identify, route, authorize, observe, constrain, validate and retire an agent independently of the prompt or execution surface that happens to run it.

Codex, a browser session or another runner is an execution surface. The registered agent remains the accountable capability identity.

## Required identity

Every registered agent has a stable machine-readable identity in `agents/registry.json`:

- `id`;
- `name`;
- `department`;
- `seniority`;
- `domain`;
- `role_type`;
- `tier`;
- `status`;
- contract path.

These concepts are deliberately separate:

- **department** — professional discipline / organizational home;
- **seniority** — expected depth of judgment and craft;
- **role_type** — operational function such as director, specialist, executor or evaluator;
- **tier** — routing frequency (`core` vs `on_demand`);
- **status** — lifecycle evidence (`pilot → active → retired`).

Seniority never grants tool or write authority.

## Authority and least privilege

A first-class agent also declares:

- explicit trigger;
- inputs and outputs;
- allowed tools;
- write-authority class;
- Guides, Guards, Sensors, Checks and Evals;
- human gate;
- retry policy;
- escalation policy.

Capability is not authority. Department and seniority do not widen permissions.

## Runtime identity

Every execution should be attributable to a registered agent through a run envelope.

Minimum runtime identity:

```text
run_id
agent_id
agent_contract_ref
task_ref
trigger
authority_snapshot
context_manifest
tool_grants
state
evidence
human_gate
```

The canonical machine-readable shape is `control-plane/run-envelope.schema.json`.

## Runtime states

Recommended run states:

`queued → authorized → running → waiting_gate → completed`

Alternative terminal/interruption states:

- `blocked`;
- `failed`;
- `escalated`;
- `cancelled`.

State belongs to the run, not to the agent registry. The registry describes durable capability and lifecycle.

## Observability and accountability

A first-class run should make it possible to answer:

1. Which registered agent acted?
2. Which contract version/ref governed it?
3. Which task and trigger activated it?
4. What context was authoritative, approved handoff, reference or execution aid?
5. Which tools were granted for this run?
6. Which writes or artifacts were produced?
7. Which Checks/Evals ran and what failed?
8. Which human gate remains or approved the transition?
9. What evidence is preserved for audit or lifecycle validation?

## Organizational model

For creative, social, web, motion and video work, the Factory uses an agency-inspired operating model. This supplies professional role boundaries and seniority without reproducing agency bureaucracy.

See `agents/agency-operating-model.md`.

## Invariants

- an agent cannot self-promote lifecycle, seniority or authority;
- a runner cannot impersonate a different registered agent without a new route/authorization;
- downstream context does not transfer upstream authority;
- producer and critic remain separable;
- a human gate cannot be crossed by relabeling the same agent;
- promotion from pilot still requires real-task evidence and explicit human approval.
