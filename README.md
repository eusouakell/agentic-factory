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

### Human operating model

The human owner should act as an **orchestrator, not an agent babysitter**.

The Factory should absorb routine coordination: route specialists, carry authoritative context, resolve bounded disagreements, run checks/evals and iterate within declared budgets. Human attention is reserved for outcome definition, authority changes, consequential exceptions and final publication/merge decisions.

For mature or explicitly configured workflows, the target interaction model is **human-at-the-gates / human-on-exception**, not human review at every specialist handoff.

See [Creative Convergence V1](docs/orchestration/creative-convergence-v1.md) and [ADR-0002 — A2 independent execution](docs/decisions/ADR-0002-a2-independent-execution.md).

## Architecture

```text
OUTCOME / INTENT
      ↓
DOMAIN AUTHORITIES + ELIGIBLE CONTEXT
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

See [first-class decisions](governance/first-class-decisions.md), the [decision record schema](control-plane/decision-record.schema.json), and the [durable decision records](docs/decisions/README.md).

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

Event-driven routing and execution-surface contracts live in [automations/](automations/). V1 converts supported events into bounded run plans and now includes a provider-neutral A2 execution substrate for isolated specialist runs, independent deliberation and persisted run evidence. Production model-backed A2 still requires a configured provider runner on the execution surface; the Factory does not infer that from the adapter alone.

Codex is modeled as an [execution surface](execution-surfaces/codex.md), not as a privileged agent.

## Observability dashboard

The portfolio-level observability dashboard is published at **[eusouakell.github.io/agentic-factory](https://eusouakell.github.io/agentic-factory/)**.

It consolidates instrumented workflows across projects and repositories to compare planned vs. accepted work, remaining planned work, unplanned work, real spillover, retries, quality gates, isolated agent executions, escaped defects, observable token usage and evidence-backed improvement opportunities. The same event stream also projects an operational task board, normalized timeline, flow/rework/human-gate wait views and agent/project comparisons. Project, repository and workflow type remain analytical filters rather than separate telemetry silos.

Workflow runtime scheduling supports dependency-safe bounded ready-task batches with global and optional per-group concurrency ceilings. Relative sizing is constrained to the declared 1/2/3/5/8 scale (plus 0 for explicitly unsized work) and is never converted automatically to hours.

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

Cross-repository decisions are recorded as ADRs at the authority that owns them: shared governance decisions in the Factory, domain decisions in the owning repository, with implementation PRs linking both. See [decision records](docs/decisions/README.md).

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
