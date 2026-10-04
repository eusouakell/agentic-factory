# Automation Layer V1

Status: **operational routing layer; model execution adapters are intentionally bounded**.

The Automation Layer turns the Agentic Factory from a library of specialist contracts into an event-driven system.

It does not make agents sovereign.

## What automation owns

- listen for supported events;
- match event + repository + changed surface to an automation contract;
- select eligible agents/evals;
- produce a run plan;
- preserve retry limits;
- preserve human gates;
- record which execution surface should perform the work.

## What automation does not own

- domain truth;
- publication authority;
- canonical brand decisions;
- arbitrary tool escalation;
- permission to call every agent;
- unlimited retry;
- silent lifecycle promotion.

## Architecture

```text
EVENT
  ↓
AUTOMATION REGISTRY
  ↓
DETERMINISTIC ROUTER
  ↓
RUN PLAN
  ├── agents
  ├── semantic evals
  ├── execution surface
  ├── retry budget
  └── human gate
        ↓
EXECUTION SURFACE
  ├── GitHub deterministic/review
  ├── Codex interactive
  └── ChatGPT / Work where connected
        ↓
EVIDENCE
        ↓
CHECKS + EVALS
        ↓
HUMAN GATE
```

## Why execution surfaces are separate

An agent is a capability/authority contract.

Codex, ChatGPT, GitHub Actions or another runner is an **execution surface**.

The same `frontend-engineer` contract can be executed interactively in Codex or through another approved runner without pretending Codex itself is the agent.

This preserves:

- one source of truth for authority;
- executor-specific strengths;
- human collaboration when the work benefits from a browser/IDE loop.

## V1 registry

Machine-readable automation contracts live in:

`automations/registry.json`

V1 contracts include:

- Factory governance PR review — **adapter installed**;
- agent-validation lifecycle changes — **adapter installed through the Factory PR surface**;
- editorial-draft quality review — **central contract, consumer adapter pending**;
- Flame product/design changes — **central contract, consumer adapter pending**.

A route is not called operational merely because its contract exists. `adapter_status` records whether the repository event is actually connected.

## Routing

`automations/route.py` accepts a small event payload and emits a run plan.

Example:

```bash
python automations/route.py \
  --repository eusouakell/agentic-factory \
  --event pull_request \
  --path governance/change-control.md \
  --path automations/registry.json
```

The output is deterministic. It does not call a model.

## Autonomy levels

### A0 — manual
Human selects agent + executor.

### A1 — autonomous routing
System detects an event and produces the required agent/eval plan.

**Automation Layer V1 reaches A1.**

### A2 — bounded execution
Approved adapters invoke the selected agent on an execution surface using task-scoped credentials/context.

### A3 — bounded remediation
Low-risk changes may be proposed automatically on a branch, followed by independent review/checks.

### A4 — autonomous consequential action
Not a current target for publication, canonical brand/knowledge, security-sensitive changes or agent lifecycle.

## Codex

Codex is treated as an execution surface optimized for interactive browser/IDE work.

See [execution-surfaces/codex.md](../execution-surfaces/codex.md).

## Safety invariant

Automation may route authority.

It may not invent authority.
