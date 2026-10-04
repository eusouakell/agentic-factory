# Agent Registry V2

This directory is the canonical registry for specialist agents in the eusouakell Agentic Factory.

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

### On demand — 14

Activated only when a task clearly matches the specialist trigger:

- Motion Web Director
- Motion Video Director
- Editorial Typography Director
- Photo Art Director
- Generative Photography Specialist
- Inclusive Experience Reviewer
- Experience Researcher
- Test Automation Engineer
- Workflow Architect
- Repository Analyst
- Agent Tooling Engineer
- Knowledge Systems Architect
- Discoverability Architect
- Data Visualization Engineer

## Registry contract

The machine-readable source is [registry.json](registry.json).

Every registered agent declares:

- tier and lifecycle;
- purpose and trigger;
- inputs and outputs;
- allowed tools;
- write authority;
- Guides, Guards, Sensors, Checks and Evals;
- human gate;
- retry policy;
- escalation policy;
- provenance;
- matching Markdown contract.

## Lifecycle

`pilot → active → retired`

Current lifecycle target in Registry V2:

- **Active core:** Research Synthesist, Frontend Engineer, Code Reviewer, Security Auditor, Production Readiness Evaluator, Flame UI Composer.
- **Pilot core:** Accessibility Auditor — source-level validation completed; rendered/manual validation still required.
- **Active on-demand:** Agent Tooling Engineer, Test Automation Engineer, Repository Analyst, Workflow Architect.
- **Pilot on-demand:** Motion Web Director, Motion Video Director, Editorial Typography Director, Photo Art Director, Generative Photography Specialist, Inclusive Experience Reviewer, Experience Researcher, Knowledge Systems Architect, Discoverability Architect, Data Visualization Engineer.

`active` means the capability has passed its lifecycle evidence gate. It does **not** mean autonomous execution. `enabled_by_default` remains false, so routing still requires an explicit trigger/control-plane decision.

Promotion requires real-task evidence and explicit human approval. See [validation/](../validation/).

## Authority

The registry defines **who can do what**.

It does not define domain truth.

See:
- [Factory authority model](../governance/authority-model.md)
- [Control plane](../control-plane/README.md)
- [Factory controls](../controls/README.md)

## Audit basis

Roster V2 was designed after a complete inventory of the Agency Agents catalog:

- 282 agents inventoried;
- 80 roster-relevant contracts deep-reviewed;
- no upstream agent installed automatically;
- broad roles were often converted into Guards, Guides, control-plane rules or skills instead of additional agents.

See [audit/agency-agents/](audit/agency-agents/).
