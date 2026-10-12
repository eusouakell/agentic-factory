# ADR-0002 — A2 independent execution and visual acceptance

**Status:** proposed — merge implies acceptance  
**Decision owner:** Kell  
**Scope:** Agentic Factory and consumer workflows that opt into A2  
**Date:** 2026-10-11  
**Decision ID:** `a2-independent-execution`

## Context

The first Bússola publish-ready run exposed a governance flaw: one execution surface could simulate several reviewer roles and produce a high readiness score even though the final human gate still found material visual defects.

That is not independent review.

The Factory therefore needs a hard distinction between:

- role-separated reasoning inside one model/run;
- genuinely separate specialist executions with inspectable run identity;
- deterministic checks;
- semantic specialist judgment;
- final human publication authority.

The published Bússola landing remains negative evidence for this escaped-defect class.

## Decision

### 1. A2 specialist execution is a real run boundary

A specialist execution must carry:

- unique `execution_id`;
- registered `agent_id` and contract;
- minimum authoritative context refs;
- task input and output schema;
- explicit tool grants;
- retry budget;
- persisted request/result evidence;
- usage quality and duration when available.

The provider-neutral `JsonSubprocessAdapter` starts one process per specialist invocation. A configured command may wrap Codex, an API worker, or another approved model runtime.

A deterministic fixture used in CI proves isolation/runtime behavior; it is **not** production model evidence.

### 2. Independent review requires independent executions

Primary and secondary reviewers for a quality dimension must have different execution IDs.

When execution provenance is supplied to publish-readiness evaluation, an invented or unknown `review_run_id` is a blocker.

A producer cannot satisfy independent-review requirements merely by relabelling one run as multiple specialist roles.

### 3. Deliberation is owner → challenger → arbiter

Owner and challenger execute independently before either position is passed to the arbiter.

The arbiter receives both persisted positions and chooses:

- `KEEP`
- `REVISE_OWNER`
- `COMBINE`
- `ESCALATE`

Owner, challenger, and arbiter must be distinct specialist identities for this profile.

Publication and merge remain human-owned.

### 4. Visual acceptance includes machine-observable geometry

The browser probe captures the actual candidate with Chrome and records:

- viewport and section;
- screenshot SHA-256;
- DOM anchor and observed heading;
- page overflow;
- section geometry;
- natural vs rendered image dimensions;
- heading/body type scale.

Deterministic blockers include:

- horizontal overflow beyond tolerance;
- distorted image aspect ratio;
- configured image-dominance violations;
- configured severe heading/body hierarchy violations;
- duplicate/missing capture evidence.

These checks do not replace semantic art direction.

### 5. Escaped defects are first-class observability events

When a later stage or final human gate finds a material problem that an upstream gate should have found, record `escaped_defect_recorded` with criterion, expected owner, evidence, severity, and discovery stage.

Portfolio metrics distinguish:

- isolated agent executions;
- failed agent executions;
- unique execution IDs;
- agent execution duration;
- escaped defects;
- human wait vs active execution.

Do not infer active human attention from elapsed gate time.

## Implementation in PR #43

PR #43 implements:

- bounded isolated JSON subprocess execution;
- persisted request/result packets;
- authority denial for merge/publish/authority-modification grants;
- independent specialist and rubric-council orchestration;
- owner/challenger/arbiter runtime;
- review provenance checks;
- real-browser screenshot + geometry probe;
- visual manifest validation;
- escaped-defect telemetry;
- workflow/run-envelope schema extensions;
- end-to-end CI for isolated execution and browser probing.

## Release gates

Before this ADR may be treated as accepted:

- Python unit/integration suite passes;
- real Chrome probe executes in CI and its generated manifest passes the validator;
- specialist tests demonstrate distinct execution IDs and persisted evidence;
- deliberation tests demonstrate independent owner/challenger/arbiter execution;
- human-owned permissions remain blocked at the executor boundary;
- README/decision registry match the implementation.

## Scope boundaries

Canonical shared behavior lives in Agentic Factory.

- Bússola owns its case narrative, visual design and product evidence.
- Cereja owns editorial strategy and storytelling canon.
- WikiLLM integration remains separately tracked in issue #40.

## Pilot rule

Do not call the previous Bússola council an A2 validation.

After this change is accepted, rerun the Bússola case as a new pilot using:

1. real browser evidence from the deployed/candidate page;
2. a configured model-backed specialist runner;
3. at least two genuinely separate specialist executions with inspectable IDs;
4. the visual/hierarchy checks introduced here;
5. the final human gate as escaped-defect calibration.

No automatic merge or republish is authorized.
