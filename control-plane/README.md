# Control plane

The control plane is infrastructure, not a privileged "Orchestrator Agent".

## Responsibilities

It owns:

- route selection;
- context eligibility and progressive disclosure;
- explicit task state;
- tool authorization;
- agent activation;
- retries and retry limits;
- handoffs;
- escalation;
- run evidence;
- terminal-state ownership.

## First-class run identity

Before execution, the control plane should bind a registered `agent_id` to a run envelope containing the task, contract ref, authority snapshot, context manifest, tool grants, state, evidence and human gate.

See [run envelope schema](run-envelope.schema.json) and [first-class agents](../governance/first-class-agents.md).

A runner such as Codex does not replace or widen that identity.

## Run state

Recommended generic lifecycle:

```text
INTAKE
  ↓
ROUTE
  ↓
AUTHORIZE
  ↓
EXECUTE
  ↓
OBSERVE
  ↓
CHECK
  ↓
EVALUATE
  ↓
HUMAN_GATE? ── no ─→ DONE
  │
 yes
  ↓
APPROVE / REVISE / ESCALATE
```

## Context-loading rules

- pass the smallest sufficient authoritative context for the role;
- prefer approved upstream artifacts over regenerating prior decisions;
- load domain canon before execution skills;
- external references never gain authority merely because they are in context;
- surface a conflict instead of asking an agent to improvise precedence.

See [progressive context loading](../governance/context-loading.md).

## Routing rules

- Core agents may be considered when their declared trigger is satisfied.
- On-demand agents require an explicit specialist trigger.
- No agent may call arbitrary agents or tools solely because it "believes" they are useful.
- The control plane may reject an otherwise capable agent when tool authority, confidentiality or blast radius is incompatible with the task.

## Retry rules

Every retry policy needs:

- a maximum count or termination condition;
- new evidence or a changed state;
- an escalation owner when retry fails.

"Try again until it works" is not an acceptable policy.

## Handoffs

A handoff should declare:

- source role;
- destination role;
- artifact/evidence passed;
- unresolved uncertainty;
- authority not transferred.

## Escalation

Escalation is expected behavior, not failure of the system.

Escalate when:

- a required authority is missing;
- constraints conflict;
- a Guard blocks;
- a Check repeatedly fails;
- high-impact uncertainty remains;
- a human decision is explicitly required.


## Automation boundary

The control plane may receive routes from [Automation Layer V1](../automations/README.md). Automation can select an eligible run plan from explicit event contracts, but cannot grant broader tool/write authority than the selected agent contract already permits.

Execution surfaces such as Codex are adapters/runners. They do not become the authority source merely because they can browse, edit or execute code.
