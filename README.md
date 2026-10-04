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

The current registry contains **21 pilot agents**:

- **7 core** — broadly reusable when their trigger is met;
- **14 on-demand** — specialist capabilities activated only for matching tasks.

All pilots remain disabled by default.

Start with:

- [Agent Registry](agents/registry.json)
- [Registry documentation](agents/README.md)
- [Agent contracts](agents/contracts/)
- [Agency Agents audit](agents/audit/agency-agents/)

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
