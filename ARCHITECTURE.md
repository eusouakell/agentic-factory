# Agentic Factory architecture

## Scope

The Factory governs **execution capability and authority**.

It answers:

> Who or what may act, with which context, tools, controls, evidence and approval?

It does not decide domain truth.

## System relationship

The Factory is **decision-oriented, capability-routed and evidence-driven**.

```text
OUTCOME / INTENT
      ↓
GOVERNED DECISION
      ↓
DOMAIN AUTHORITIES
Núcleo · Flame · Editorial Engine · Context System
      ↓
CONTROL PLANE
route · authorize · select capabilities · set oversight
      ↓
AGENTS / SKILLS / TOOLS
      ↓
TASKS / EXECUTION
      ↓
GUIDES / GUARDS / SENSORS / CHECKS / EVALS
      ↓
EVIDENCE
      ↓
OUTCOME OBSERVED
      ↓
LEARN-BACK
```

Tasks remain execution units. They are not the primary abstraction for choices that affect outcomes, risk, authority or downstream work. See [first-class decisions](governance/first-class-decisions.md).

## Responsibilities

### Control plane owns

- decision intake and decision-to-capability routing;
- oversight-mode enforcement;
- routing;
- context eligibility and progressive disclosure;
- task/run state;
- operational work-state interpretation;
- tool authorization;
- retries;
- handoffs;
- escalation;
- failure ownership;
- execution evidence requirements.

Operational roadmap state is externalized rather than reconstructed from chat history. Canonical docs remain truth; Issues define work; GitHub Projects expose current flow; Gates preserve authority. See [operational work state](governance/operational-work-state.md).

### Automation layer owns

- supported event contracts;
- deterministic routing from event to run plan;
- execution-surface selection;
- retry budgets;
- preservation of declared human gates;
- run-plan evidence.

Automation routes authority; it does not invent authority.

### Registry owns

- named capabilities;
- triggers;
- inputs/outputs;
- allowed tools;
- write authority;
- controls;
- retry and escalation policy;
- lifecycle and tier;
- department and seniority;
- stable first-class identity;
- provenance.

### Domain repositories own

- truth;
- policy;
- brand;
- knowledge;
- editorial intent;
- product-specific constraints.

### Context resolution

The control plane resolves both **where work stands** and which domain artifacts are eligible for a run. Durable work state should come from the Project/Issue/approved-artifact chain rather than depending on a previous conversation still fitting in context.

The control plane should not dump entire domain repositories into the active agent.

Use [progressive context loading](governance/context-loading.md):

```text
task / approved handoff
→ applicable domain canon
→ surface/project contract
→ agent contract
→ execution aid
```

A downstream role inherits approved decisions. Reopening them requires a documented conflict, missing authority or explicit human instruction.

## Non-goals

The Factory is not:

- an autonomous publisher;
- a universal source of truth;
- a reason to turn every capability into an agent;
- permission for one agent to design, execute and approve its own work;
- proof that more agents produce better outcomes.

## First-class decisions and agents

Governed decisions are first-class entities with stable identity, ownership, criteria, governance profile, oversight mode, evidence and learn-back.

Registered specialist agents are also first-class entities with stable identity, professional placement, bounded authority and attributable runtime state. The execution surface does not become the agent identity.

The agency-inspired model is a **capability map**, not the top-level architecture. The control plane starts from the outcome and decision, then routes only the professional capabilities needed to support or execute it.

See [first-class decisions](governance/first-class-decisions.md), [first-class agents](governance/first-class-agents.md) and [agency operating model](agents/agency-operating-model.md).

## Agent tiers

### Core

Broadly reusable capabilities considered when their explicit trigger is met.

### On demand

Specialists activated only when a task clearly matches their trigger.

### Conditional/future

Capabilities discovered by audit but intentionally absent from the registry until a concrete project justifies them.

## Lifecycle

`pilot → active → retired`

A pilot may be promoted only after real-task evidence shows that:

1. the capability boundary is useful;
2. authority is not colliding with another role;
3. controls and escalation work;
4. a human explicitly approves promotion.


## README synchronization invariant

README files are navigation and system-state surfaces, not secondary decoration.

Any change that materially alters one or more of the following must review the affected README(s) in the same change:

- architecture or system relationships;
- canonical authority or source-of-truth location;
- workflow, gates or handoff sequence;
- context-loading/routing behavior;
- agent or control-plane responsibilities;
- repository navigation or primary entry points.

If the README does not require a change, the PR should make that an explicit decision rather than silently assuming it.

Detailed rules should remain in their canonical documents. README updates should summarize the changed model and point to the authoritative source, preserving progressive disclosure rather than duplicating full specifications.
