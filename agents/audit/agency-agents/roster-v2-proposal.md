# Roster V2 — proposal after full catalog audit

Status: **proposal only — no registry mutation in this branch**.

## Design principle

Roster size is not a capability metric.

The Factory should keep always-useful reviewers/executors small, expose specialist agents on demand, and keep orchestration/policy in the control plane.

## Proposed tiers

### Core agents

These are broadly useful across most GitHub/product/content work.

| Agent | Action |
|---|---|
| **Research Synthesist** | **ADD** — evidence search, source grading, synthesis, contradictions, confidence |
| **Frontend Engineer** | KEEP + strengthen with minimal-diff, performance, i18n/accessibility escalation rules |
| **Code Reviewer** | **ADD** — correctness, maintainability, performance and non-security review |
| **Security Auditor** | KEEP + strengthen with AppSec and secrets lifecycle patterns |
| **Accessibility Auditor** | **ADD** — independent WCAG 2.2 + assistive-tech review |
| **Production Readiness Evaluator** | KEEP — consumes evidence; never overrides blocker checks |
| **Flame UI Composer** | KEEP — visual executor under Flame authority |

### Specialists on demand

| Agent | Action |
|---|---|
| Motion Web Director | KEEP |
| Motion Video Director | KEEP |
| Editorial Typography Director | KEEP — genuine gap not supplied cleanly by upstream catalog |
| Photo Art Director | KEEP |
| Generative Photography Specialist | KEEP |
| **Inclusive Experience Reviewer** | EVOLVE from Inclusive Visual Reviewer; extend from imagery to UI/copy/workflow exclusion |
| **Experience Researcher** | ADD — real UX research + feedback synthesis; persona walkthrough only as hypothesis |
| **Test Automation Engineer** | ADD |
| **Workflow Architect** | ADD |
| **Repository Analyst** | ADD — merge onboarding + drift-audit capabilities |
| **Agent Tooling Engineer** | ADD — merge MCP Builder + developer tooling |
| **Knowledge Systems Architect** | ADD — merge RAG + knowledge graph + search relevance |
| **Discoverability Architect** | ADD — SEO + AEO/GEO + agent-readiness modes |
| **Data Visualization Engineer** | ADD |

### Conditional / future

Do not add until a concrete project justifies them:

- Security Architect
- Identity & Access Engineer
- Privacy Engineer / DPO
- DevOps / SRE / Platform Engineer
- Technical Writer
- PDF / document compiler specialists
- Proposal Strategist
- Tracking & Measurement Specialist
- Ad Creative Strategist
- Video Optimization Specialist
- Agentic Identity & Trust Architect
- Model QA Specialist
- Business Strategist

### Explicitly not agents

These capabilities should live elsewhere:

| Capability | Local home |
|---|---|
| Orchestration / agent spawning | control plane |
| Git workflow discipline | Guide / repository policy |
| Minimal-change discipline | Guard for executors |
| Prompt versioning / prompt tests | Guide + eval infrastructure |
| Experiment tracking | Sensors / experiment protocol |
| Brand guardianship | canonical brand system + human gate |
| Channel-specific post writing | Editorial Engine + format Guides |
| Executive summaries | writing skill |
| Meeting notes | extraction skill |
| Master implementation planning | planning Guide / mode |
| Studio/Chief-of-Staff coordination | human/project layer |

## Net effect

Registry V1 currently has **10** agents.

If this proposal is approved:
- **3 new core agents**;
- **8 new on-demand specialists**;
- **1 existing role broadened**;
- existing visual specialists retained;
- no external agent files installed.

The roster grows because the audit found distinct capabilities, not because the upstream catalog is large.

## Proposed implementation sequence

1. Add Research Synthesist, Code Reviewer and Accessibility Auditor.
2. Evolve Inclusive Visual Reviewer → Inclusive Experience Reviewer.
3. Add Experience Researcher + Test Automation Engineer.
4. Add Repository Analyst + Workflow Architect.
5. Add Agent Tooling Engineer + Knowledge Systems Architect.
6. Add Discoverability Architect + Data Visualization Engineer.
7. Run one real task per new/changed role before promoting any from `pilot` to `active`.
8. Revisit conditional roles only when a project creates a concrete trigger.

## Acceptance criteria for any new agent

Before merge:
- unique capability boundary;
- explicit trigger;
- no collision with control plane;
- least-privilege tools;
- write authority bounded;
- human gate declared;
- deterministic checks separated from semantic evals;
- provenance recorded;
- at least one real validation scenario defined.

## What this proposal does not do

- It does not install Agency Agents.
- It does not copy upstream role files.
- It does not activate any new agent.
- It does not treat external metrics as local targets.
- It does not mutate `agents/registry.json` until Kell approves the roster direction.
