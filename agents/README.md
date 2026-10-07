# Agent Registry V3

This directory is the canonical machine-readable registry for specialist agents in the eusouakell Agentic Factory.

## First-class identity

Every agent declares:

- stable ID and contract;
- department;
- seniority;
- domain and role type;
- tier and lifecycle;
- purpose and trigger;
- inputs and outputs;
- allowed tools and write authority;
- Guides, Guards, Sensors, Checks and Evals;
- human gate;
- retry and escalation policy;
- provenance.

See [first-class agents](../governance/first-class-agents.md).

**Seniority is not authority.**

A Director may still be `review_only`; a Senior executor may write only scoped domain assets. Tool/write authority remains explicit and run-scoped.

## Organization

Creative/social/web/video roles follow the [agency-inspired operating model](agency-operating-model.md):

- Strategy & Planning
- Creative
- Art & Design
- Experience
- Production
- Quality & Risk
- Engineering
- Agent Systems

The control plane performs traffic/routing/state work; there is no Traffic Manager Agent.

## Tiers

### Core — 7

Broadly reusable capabilities considered when their explicit trigger is met:

- Research Synthesist
- Frontend Engineer
- Code Reviewer
- Security Auditor
- Accessibility Auditor
- Production Readiness Evaluator
- Flame UI Composer

### On demand — 24

Activated only when a task clearly matches the specialist trigger. This includes established specialist roles plus the five new pilot gaps registered in 2026-10:

- Editorial Art Director
- Graphic / Editorial Designer
- Experience Designer
- Motion Designer
- Video Editor / Post-production Specialist

Use `registry.json` as the complete current roster rather than maintaining a second full list here.

## Lifecycle

`pilot → active → retired`

`active` means the capability passed its lifecycle evidence gate. It does **not** mean autonomous execution. `enabled_by_default` remains false unless an explicit control-plane policy says otherwise.

Promotion requires real-task evidence and explicit human approval. See [validation/](../validation/).

## Expertise audit

The 2026-10 review evaluated every existing agent against professional analogue, craft depth, seniority, overlap and gaps.

Key changes:

- Visual Storyteller is a mid-level bounded specialist, not the Editorial Art Director;
- Instagram Carousel Planner is a format specialist, not a director;
- Editorial/Instagram strategy roles are labeled as strategists;
- art direction is separated from graphic production;
- experience design is separated from research, UI composition and frontend;
- motion/video direction is separated from motion/editing execution.

See [roster expertise review](audit/roster-expertise-review-2026-10.md).

## Authority

The registry defines **who can do what**. It does not define domain truth.

See:
- [Factory authority model](../governance/authority-model.md)
- [Control plane](../control-plane/README.md)
- [Factory controls](../controls/README.md)

## Audit basis

Registry V2 was originally designed after a complete inventory of the Agency Agents catalog:

- 282 agents inventoried;
- 80 roster-relevant contracts deep-reviewed;
- no upstream agent installed automatically;
- broad roles were often converted into Guards, Guides, control-plane rules or skills instead of extra agents.

Registry V3 preserves that anti-proliferation principle: new roles were added only where a real workflow gap was found.

See [agency-agents audit](audit/agency-agents/).
