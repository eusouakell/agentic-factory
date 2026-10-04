# Agentic Factory architecture

## Scope

The Factory governs **execution capability and authority**.

It answers:

> Who or what may act, with which context, tools, controls, evidence and approval?

It does not decide domain truth.

## System relationship

```text
DOMAIN AUTHORITIES
Núcleo · Flame · Editorial Engine · Context System
             ↓
        CONTROL PLANE
             ↓
    AGENT REGISTRY + TOOLS
             ↓
GUIDES / GUARDS / SENSORS / CHECKS
             ↓
            EVALS
             ↓
       HUMAN DECISIONS
```

## Responsibilities

### Control plane owns

- routing;
- task/run state;
- tool authorization;
- retries;
- handoffs;
- escalation;
- failure ownership;
- execution evidence requirements.

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
- provenance.

### Domain repositories own

- truth;
- policy;
- brand;
- knowledge;
- editorial intent;
- product-specific constraints.

## Non-goals

The Factory is not:

- an autonomous publisher;
- a universal source of truth;
- a reason to turn every capability into an agent;
- permission for one agent to design, execute and approve its own work;
- proof that more agents produce better outcomes.

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
