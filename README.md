# Agentic Factory

**Canonical control plane and agent registry for the eusouakell agentic system.**

This repository defines:

- first-class governed decisions and their oversight;
- the Agent Registry and specialist contracts;
- control-plane responsibilities;
- Guides / Guards / Sensors / Checks / Evals / Human Gates;
- authority, provenance and lifecycle rules;
- integration boundaries with domain repositories.

It does **not** own domain truth.

Current domain authorities remain:

- `cereja-knowledge-system` — Núcleo + Flame;
- `cereja-editorial-engine` — editorial workflow and publication gates;
- `marketing-context-system` — context routing and context-specific runtime.

## Core principle

> Outcomes drive decisions. Decisions route bounded capabilities. Authority remains explicit, observable and evidence-based.

Agents are capabilities, not the architecture. The agency-inspired structure is a professional capability map, not the primary unit of work.

## Architecture

```text
OUTCOME / INTENT
      ↓
GOVERNED DECISION
owner · criteria · value · risk · frequency · reversibility · oversight
      ↓
CONTROL PLANE
route · authorize · select capabilities · state · retries · escalation
      ↓
AGENT / SKILL / TOOL
      ↓
TASKS / EXECUTION
      ↓
SENSORS → CHECKS → EVALS
      ↓
EVIDENCE → OUTCOME OBSERVED → LEARN-BACK
```

The Orchestrator is **not** an agent persona. Routing and authority are control-plane concerns.

See [ARCHITECTURE.md](ARCHITECTURE.md).

## First-class decisions

Governed decisions are modeled independently from their implementation tasks. Each decision can carry ownership, criteria, business value, risk, frequency, reversibility, oversight mode, evidence and learn-back.

Human gates are a calibration mechanism, not a permanent assumption. Mature recurring decision classes may move toward exception-based, sampled or bounded autonomous oversight only after evidence and explicit approval.

See [first-class decisions](governance/first-class-decisions.md) and the [decision record schema](control-plane/decision-record.schema.json).

## Agent Registry V3

The current Registry V3 contains **31 agents**:

- **7 core** — existing lifecycle states preserved;
- **24 on-demand** — including five new production/design pilots identified by the 2026-10 expertise review.

`active` means validated capability, not autonomous execution. All agents remain disabled by default unless the control plane explicitly routes them.

Registry V3 treats agents as first-class entities with stable identity, department, seniority, bounded authority and attributable runtime state. Seniority does not grant authority.

Start with:

- [Agent Registry](agents/registry.json)
- [Registry documentation](agents/README.md)
- [Agent contracts](agents/contracts/)
- [Agency-inspired operating model](agents/agency-operating-model.md)
- [First-class agent model](governance/first-class-agents.md)
- [Roster expertise review](agents/audit/roster-expertise-review-2026-10.md)
- [Agency Agents audit](agents/audit/agency-agents/)

## Automation Layer

Event-driven routing and execution-surface contracts live in [automations/](automations/). V1 autonomously converts supported events into bounded run plans; model/tool execution remains adapter-specific and preserves human gates.

Codex is modeled as an [execution surface](execution-surfaces/codex.md), not as a privileged agent.

## Controls

The Factory separates:

- **Guides** — orientation;
- **Guards** — pre-execution constraints;
- **Sensors** — observations;
- **Checks** — deterministic or explicit verification;
- **Evals** — semantic judgment;
- **Human Gates** — accountable decisions.

See [controls/README.md](controls/README.md).

## Authority

Agents cannot:

- merge directly to `main`;
- publish autonomously;
- widen their own tool scope;
- bypass the control plane;
- silently modify canonical knowledge, brand or editorial authority.

See [governance/authority-model.md](governance/authority-model.md).

## Context loading

The control plane should pass the **smallest sufficient authoritative context** to each role. Canonical domain rules come before project artifacts; project artifacts come before execution skills. Downstream agents do not reopen approved gates without a documented conflict.

See [progressive context loading](governance/context-loading.md).

## Operational work state

Chat history is working context, not durable roadmap state.

The operating model externalizes state so work can survive context-window exhaustion, a new chat or a different execution surface:

- canonical docs — what is true;
- Issues — what needs to happen;
- one cross-repository GitHub Project — current flow and priority;
- Gates — who may authorize the next transition.

Default flow: `Backlog → Ready → In Progress → Gate / Review → Done`.

See [operational work state](governance/operational-work-state.md).

## Repository boundaries

The Factory is reusable infrastructure. Domain systems remain independent consumers.

Architecture, authority, workflow and context-routing changes follow the [README synchronization invariant](ARCHITECTURE.md#readme-synchronization-invariant): affected README files are reviewed in the same change so navigation stays aligned with the canonical system.

See [integrations/](integrations/).

## Migration provenance

Registry V2 originated from the migration described below; Registry V3 evolves that foundation with first-class identity and professional role separation. The original audit artifacts were migrated from `eusouakell/marketing-context-system` after the extraction boundary was approved.

Migration rule:

`copy → validate → redirect/deprecate → remove`

The source copy is not removed until this repository is validated and consumer repositories point here.

See [governance/provenance.md](governance/provenance.md) and [MIGRATION-MANIFEST.json](MIGRATION-MANIFEST.json).

## Validation evidence

Real-task agent evidence lives in [validation/](validation/). Promotion from `pilot` to `active` requires recorded evidence plus explicit human approval.

## Validation

```bash
python agents/validate_registry.py agents/registry.json
python -m unittest tests.test_agent_registry -v
```

GitHub Actions runs the same registry checks on pull requests and `main`.
