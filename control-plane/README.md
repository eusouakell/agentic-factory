# Control plane

The control plane is infrastructure, not a privileged "Orchestrator Agent".

## Responsibilities

It owns:

- decision intake and decision-to-capability routing;
- governance-profile interpretation;
- oversight-mode enforcement;
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

## First-class decisions

Before routing work, the control plane should determine whether the request contains a governed decision.

A governed decision has a stable record with owner, value/risk/frequency/reversibility profile, inputs, criteria, required authority, oversight mode, evidence and expected outcome.

See [first-class decisions](../governance/first-class-decisions.md) and [decision record schema](decision-record.schema.json).

## First-class run identity

Before execution, the control plane should bind a registered `agent_id` to a run envelope containing the task, contract ref, authority snapshot, context manifest, tool grants, state, evidence and human gate. When the run supports or executes a first-class decision, it should also include `decision_ref`.

See [run envelope schema](run-envelope.schema.json) and [first-class agents](../governance/first-class-agents.md).

A runner such as Codex does not replace or widen that identity.

## Decision and run state

Decision lifecycle:

```text
PROPOSED → READY → DECIDING → DECIDED → EXECUTING → OBSERVING → CLOSED
                         ↘ ESCALATED / CANCELLED
```

A decision may trigger one or more runs. Run lifecycle:

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

- Start from the outcome and governed decision when one exists; do not route merely because a task label resembles an agent title.
- Use the agency-inspired departments as a capability map, not a mandatory chain.
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


## Oversight and earned autonomy

Human review is not assumed to remain at every gate forever.

A recurring decision class may move from `human_gate` to `human_on_exception`, `sampled_review` and eventually `autonomous_bounded` only when evidence shows stable criteria, low revision/error rates, reliable checks/evals and acceptable reversibility/blast radius.

Changing oversight mode is itself an authority decision and requires explicit approval. Decision autonomy never widens tool, write, merge or publication authority by implication.
