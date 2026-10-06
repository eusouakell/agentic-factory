# Agentic Factory

**Canonical control plane and agent registry for the eusouakell agentic system.**

This repository defines:

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

> Agents are bounded capabilities. Authority lives in the control plane and canonical domain systems.

## Architecture

```text
INTENT / TASK
     ↓
CONTROL PLANE
route · authorize · state · retries · handoffs · escalation
     ↓
GUIDES + GUARDS
     ↓
AGENT / SKILL / TOOL
     ↓
SENSORS
     ↓
CHECKS
     ↓
EVALS
     ↓
HUMAN GATE when required
     ↓
DONE / REVISE / ESCALATE
```

The Orchestrator is **not** an agent persona. Routing and authority are control-plane concerns.

See [ARCHITECTURE.md](ARCHITECTURE.md).

## Agent Registry V2

The current Registry V2 contains **21 agents**:

- **7 core** — 6 active, 1 pilot;
- **14 on-demand** — 4 active, 10 pilot.

`active` means validated capability, not autonomous execution. All agents remain disabled by default unless the control plane explicitly routes them.

Start with:

- [Agent Registry](agents/registry.json)
- [Registry documentation](agents/README.md)
- [Agent contracts](agents/contracts/)
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

## Repository boundaries

The Factory is reusable infrastructure. Domain systems remain independent consumers.

See [integrations/](integrations/).

## Migration provenance

Registry V2 and its audit artifacts were migrated from `eusouakell/marketing-context-system` after the extraction boundary was approved.

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
