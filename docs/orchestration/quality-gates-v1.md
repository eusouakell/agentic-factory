# Quality Gates & Checklists V1

**Status:** proposed shared contract  
**Scope:** all Agentic Factory workflows and instrumented GitHub projects  
**Purpose:** make quality expectations explicit, testable where possible and observable across projects without replacing specialist judgment.

## 1. Principle

A checklist is a **gate contract**, not a decorative sign-off form.

It exists to answer:

- what must be true before work moves forward;
- who owns each criterion;
- what evidence proves it;
- whether the criterion is deterministic, semantic or human-owned;
- which failures block progression;
- which quality problems recur across projects.

A checklist must not be used to convert subjective craft into fake binary certainty.

## 2. Three classes of checks

### A. Deterministic checks

Machine-verifiable criteria.

Examples:

- required artifact exists;
- required viewport render exists;
- no broken internal links;
- CI passes;
- reduced-motion path exists;
- source/provenance field is present;
- workflow emitted required telemetry fields.

These may be executed automatically.

### B. Semantic evaluations

Require specialist judgment.

Examples:

- visual direction is distinctive rather than template-like;
- narrative has a clear tension and payoff;
- mobile composition is authored rather than a desktop stack;
- evidence is represented honestly;
- content hierarchy reduces explanation burden.

These are owned by the relevant agent/evaluator and must include a short rationale/evidence reference.

### C. Human decisions

Consequential or authorial acceptance that remains with Kell or another declared human owner.

Examples:

- approve art direction;
- accept a material brand-system change;
- approve publication/merge;
- accept a known residual risk.

The system records the decision; it does not impersonate it.

## 3. Checklist item model

Each item should have a stable ID and the following shape:

```json
{
  "check_id": "visual.mobile.authored_composition",
  "title": "Mobile composition is intentionally authored",
  "class": "semantic",
  "owner": "creative-director",
  "severity": "blocker",
  "applies_if": ["surface:web"],
  "evidence_required": true,
  "status": "pass",
  "evidence_refs": ["artifact://hero-mobile-v2"],
  "note": "UI and protagonist remain one visual scene at 390px."
}
```

Allowed statuses:

- `pass`
- `fail`
- `not_applicable`
- `unknown`

A required blocker in `fail` or `unknown` prevents the gate from passing.

## 4. Gate model

A workflow may declare several gates, but V1 should prefer a small number of meaningful gates.

Recommended structure:

```text
UPSTREAM QUALITY GATE
→ human direction/PRD gate when required
→ production
→ RELEASE QUALITY GATE
→ human merge/publication gate
```

Each gate declares:

- `gate_id`
- required checklist template(s)
- required evidence
- owners
- blocking rule
- human decision when applicable

## 5. Shared checklist families

These are reusable families. Workflows select only what applies.

### 5.1 Context / intake

- authoritative sources identified;
- source precedence is explicit;
- unresolved factual gaps are named;
- project/repository/workflow metadata are present;
- acceptance criteria exist;
- retry/escalation owner exists.

### 5.2 Evidence / provenance

- factual claims have traceable evidence;
- synthetic/reconstructed/generated artifacts are labelled;
- rights/consent status is recorded when relevant;
- observed fact is separated from interpretation;
- unsupported metrics/claims are excluded.

### 5.3 Narrative / content design

- one central story/job is identifiable;
- each section/component has a distinct purpose;
- terminology is audience-appropriate;
- claims do not overstate product maturity or outcomes;
- labels/microcopy reduce ambiguity;
- content order matches decision/read sequence.

### 5.4 Experience / responsive behavior

- task/reading order is explicit;
- mobile behavior is designed, not merely stacked;
- progressive disclosure is intentional;
- critical information does not depend on hover;
- error/empty/loading behavior is defined where applicable;
- interaction does not rely on motion for meaning.

### 5.5 Visual direction

- one dominant compositional idea is present;
- references are translated into principles rather than copied templates;
- type, image and product evidence form one coherent hierarchy;
- repeated card/container patterns are justified rather than default;
- visual distinctiveness does not reduce comprehension;
- representative mobile and desktop proofs exist before implementation.

### 5.6 Motion

Only applies when motion has a declared job.

- motion intent is documented;
- static composition already passes;
- no essential information exists only in animation;
- reduced-motion behavior is defined;
- duration/density are within declared budget;
- motion does not mask a weak layout.

### 5.7 Accessibility

- semantic structure is coherent;
- keyboard path is usable where applicable;
- focus is visible;
- contrast/reflow checks are performed;
- reduced motion is respected;
- untested assistive-technology areas are explicitly named;
- automated scans are not presented as full conformance.

### 5.8 Implementation quality

- implementation matches approved design/content artifacts;
- no silent design-system invention;
- no unapproved dependency for visual effect;
- tests/build pass;
- known deviations are documented;
- repository conventions and scope are respected.

### 5.9 Observability completeness

- project ID is present;
- repository/workflow type are present;
- task start/end events exist;
- human-gate open/resolve events exist when applicable;
- retry/revision events are captured;
- accepted artifact is linked;
- usage quality is explicit (`exact | estimated | unavailable`);
- no synthetic token precision is reported.

### 5.10 Release / readiness

- blocker findings are closed or explicitly accepted by the human owner;
- required screenshots/renders exist;
- accessibility/code reviews are present;
- readiness evaluator has sufficient evidence;
- publication/merge risks are named;
- final human gate is recorded.

## 6. Checklist templates vs project-specific criteria

The Factory owns reusable checklist templates.

Projects may add criteria, but must not fork the underlying semantics.

Example:

`quality/templates/web-editorial-case.json`

can be used by Bússola, Cereja or another repository. A project may extend it with a criterion such as:

`bussola.synthetic_data.disclosure_visible`

but should not create a separate quality engine.

Project is a filter and source of additional constraints, not an observability silo.

## 7. Telemetry

Checklist execution should emit events into the same portfolio-level event stream.

Recommended events:

- `quality_gate_opened`
- `quality_check_recorded`
- `quality_gate_passed`
- `quality_gate_failed`
- `quality_gate_overridden`

For `quality_gate_overridden`, record:

- human owner;
- failed/unknown criteria;
- rationale;
- residual risk.

## 8. Derived quality metrics

Across portfolio and filterable by project/repository/workflow/agent:

- gate pass rate;
- first-pass gate pass rate;
- most frequently failed checks;
- blocker recurrence;
- average number of failed checks per workflow;
- quality-rework correlation;
- quality failure → upstream owner distribution;
- override count and residual-risk categories;
- escaped defect count when a later stage discovers a criterion that should have failed earlier.

The purpose is to identify process weaknesses such as:

- poor requirements;
- weak art direction;
- repeated responsive failures;
- missing provenance;
- implementation drift;
- insufficient review.

Do not use a single composite “quality score” in V1.

## 9. Anti-patterns

Do not:

- create a 100-item checklist nobody reads;
- mark semantic craft as automatically passed;
- let the executor approve its own independent-review criteria;
- treat `not_applicable` as a way to bypass inconvenient checks;
- use checklist completion as proof of excellence;
- optimize for pass rate by weakening criteria;
- create separate checklist engines per project.

## 10. Bússola pilot gates

### Gate A — Direction readiness

Before Kell sees the direction packet:

**Context**
- source-of-truth packet complete;
- approved copy/evidence boundaries preserved;
- rejected visual directions explicitly separated from authority.

**Narrative/content**
- central tension and section purpose explicit;
- PoC vs later refinement distinction preserved;
- public wording uses “agentes de IA” where clearer than agentic jargon.

**Experience**
- desktop and mobile reading order defined;
- before/after comparison behavior defined;
- team/prototype/data sections each have a distinct job.

**Art direction**
- one dominant visual idea;
- 2–3 representative proofs;
- mobile proof is independently composed;
- no generic SaaS/card-grid grammar;
- no motion required to make static direction work.

**Creative preflight**
- Creative Director = PASS;
- unresolved conflicts surfaced.

A blocker failure returns to the owning upstream task. It does not go to Kell as a vague “what do you think?”

### Gate B — Release readiness

Before final Kell merge gate:

- implementation matches approved packet;
- desktop + 390 + 320 evidence exists;
- reduced-motion path works;
- keyboard/focus/reflow checks complete where applicable;
- code review has no unresolved blocker;
- accessibility review names tested and untested areas;
- readiness evaluator has complete evidence;
- publication risks/provenance are explicit;
- telemetry is complete enough to compute pilot metrics.

## 11. Implementation slice

V1 implementation should add:

1. checklist template schema;
2. gate result schema;
3. deterministic evaluator for required/blocker state;
4. event emission into observability JSONL;
5. dashboard view for gate status and failure hotspots;
6. Bússola Gate A and Gate B templates;
7. tests for blocker, unknown, override and not-applicable semantics.

