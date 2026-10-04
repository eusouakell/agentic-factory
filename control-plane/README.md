# Control plane

The control plane is infrastructure, not a privileged "Orchestrator Agent".

## Responsibilities

It owns:

- route selection;
- explicit task state;
- tool authorization;
- agent activation;
- retries and retry limits;
- handoffs;
- escalation;
- run evidence;
- terminal-state ownership.

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
