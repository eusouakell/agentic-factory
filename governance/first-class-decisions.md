# First-class decisions

## Decision

Governed decisions are **first-class system entities** in the Agentic Factory.

The Factory should not organize work primarily as a queue of tasks performed by specialist agents. Tasks remain necessary for execution, but the control plane should be able to identify, govern, attribute and learn from the decisions that shape those tasks.

The operating sequence is:

```text
OUTCOME
  ↓
DECISION
  ↓
CONTROL PLANE
  ↓
CAPABILITIES / AGENTS / TOOLS
  ↓
TASKS / EXECUTION
  ↓
EVIDENCE
  ↓
OUTCOME OBSERVED
  ↓
LEARN-BACK
```

This preserves professional specialization while preventing the agency-inspired org chart from becoming the system architecture.

## What counts as a first-class decision

A decision is first-class when the system needs to reason about it independently of the task that implements it.

Typical examples:

- which customer or audience to prioritize;
- which story route to pursue;
- which channel or format fits an approved story;
- which visual direction should govern production;
- whether a piece is ready to publish;
- whether an agent may proceed autonomously or needs oversight;
- whether a tool/action is permitted under current authority.

A low-level deterministic action does not need to be promoted into a decision object merely because a machine performs it.

## Required identity

Each governed decision has a stable machine-readable record:

- `decision_id`;
- `decision_type`;
- `title`;
- `outcome_ref`;
- `decision_owner`;
- governance profile;
- inputs;
- decision criteria;
- authority required;
- oversight mode;
- state;
- evidence;
- expected outcome;
- observed outcome;
- learn-back.

The canonical machine-readable shape is `control-plane/decision-record.schema.json`.

## Governance profile

The control plane should prioritize oversight using four signals:

- **business value** — impact if the decision is right or wrong;
- **risk** — financial, operational, reputational, legal, brand or user impact;
- **frequency** — how often the decision recurs;
- **reversibility** — how hard it is to undo the consequence.

Value, risk and frequency use a 1–5 scale. Reversibility is categorical.

High-value, high-risk and/or frequently recurring decisions deserve explicit criteria, ownership and evidence before autonomy expands.

## Decision ownership

Every decision has one accountable owner.

The owner may be:

- a human;
- a registered agent operating within bounded authority;
- a system/control-plane rule for deterministic policy decisions.

Ownership is not the same as execution. A human may own a decision while an agent prepares options. An agent may own a bounded operational decision while another executor performs the resulting task.

## Oversight modes

The decision record declares one of these modes:

### `human_only`

Agents may research, synthesize or recommend, but only a human can decide.

Use for irreversible, high-consequence or authority-sensitive decisions.

### `human_gate`

An agent or workflow proposes a decision; a human must approve before execution.

This is the default for new, unvalidated or medium/high-risk decision classes.

### `human_on_exception`

The system may decide and proceed when policy, confidence and evidence are inside declared bounds. It stops for human review only when an exception condition is triggered.

### `sampled_review`

Bounded decisions proceed automatically; humans review a defined sample and all flagged exceptions.

This is useful for mature, frequent and reversible decisions.

### `autonomous_bounded`

The system may decide and act without per-instance human approval only inside explicit authority, context, policy, risk and tool bounds.

All decisions remain observable, attributable and auditable. Crossing a bound escalates rather than improvises.

## Autonomy is earned by decision class

Human involvement should decrease only where evidence supports it.

A decision class may move from:

`human_gate → human_on_exception → sampled_review → autonomous_bounded`

only when there is evidence of:

- stable decision criteria;
- repeated agreement between system proposals and human approvals;
- low revision/error rate;
- bounded and understood failure modes;
- acceptable reversibility/blast radius;
- reliable checks/evals;
- explicit human approval of the new oversight mode.

A senior agent or high model capability does not justify autonomy by itself.

## Decision authority vs action authority

Permission to make a decision does not automatically grant permission to execute its consequence.

Example:

- a channel strategist may be authorized to select an Instagram format;
- that does not grant permission to publish;
- an art director may select a visual direction;
- that does not grant production or merge authority.

Existing tool/write/publication boundaries remain in force.

## Relationship to first-class agents

Agents answer:

> Who or what is acting?

Decisions answer:

> What choice is being made, under whose authority, using which criteria and evidence?

Runs answer:

> What happened during one execution?

Tasks answer:

> What work must be performed because of the decision?

These are related but distinct objects.

A run envelope may reference a first-class decision through `decision_ref`.

## Relationship to the agency-inspired model

The agency-inspired model remains useful as a **capability map**:

- Strategy & Planning;
- Creative;
- Art & Design;
- Experience;
- Production;
- Quality & Risk;
- Engineering;
- Agent Systems.

It should not determine the top-level workflow.

The control plane starts from the outcome and governed decision, then routes only the capabilities required to support or execute that decision.

## Learning loop

The Factory should preserve:

- decision proposed;
- owner;
- inputs and criteria;
- selected option/rationale;
- approval or exception;
- execution evidence;
- observed outcome;
- human revision when applicable;
- learn-back.

This turns Kell's current intensive calibration into reusable evidence.

The goal is not to keep Kell in every gate forever. The goal is to use present gates to learn the decision boundaries, taste, voice, risk tolerance and quality standards well enough that recurring low-risk decisions can later move to exception-based or sampled human oversight.

## Invariants

- no agent may expand its own decision authority;
- no decision object overrides canonical domain truth;
- no decision may silently change its own oversight mode;
- approval of an output does not change authorship provenance;
- autonomy remains bounded by action/tool/write authority;
- high-consequence exceptions escalate;
- producer and critic may remain separate even when a decision class becomes more autonomous;
- learn-back records evidence; it does not silently rewrite canonical rules.
