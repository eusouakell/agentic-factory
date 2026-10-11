# Deliberative Quality Loop V1

**Status:** proposed Creative Convergence profile  
**Scope:** high-craft editorial/web/product case work  
**Extends:** `docs/orchestration/creative-convergence-v1.md`  
**Primary use case:** Bússola public case  
**Goal:** allow specialist agents to challenge, revise and arbitrate work internally until the artifact is publish-ready, while keeping publication/merge authority human-owned.

## 1. Why this exists

Sequential handoffs can still leave the human owner acting as the de facto creative director and traffic manager:

- one specialist produces;
- Kell identifies a weakness;
- context is manually carried to another specialist;
- the next specialist fixes a local symptom;
- an upstream decision quietly reopens;
- implementation begins before the full direction is coherent.

This profile specializes Creative Convergence for high-craft work with a **bounded deliberation loop**. It does not replace the generic convergence contract.

The system should only interrupt Kell before publication when a question cannot legitimately be answered inside existing evidence or delegated authority.

## 2. Core principle

> Specialists may disagree, challenge and return work. They may not self-expand authority, invent missing evidence or self-approve publication.

The target is not consensus for its own sake.

The target is:

- one coherent artifact;
- explicit resolution of material disagreements;
- no unresolved blocker;
- no open factual/provenance question;
- publish-ready implementation evidence;
- one final human publication/merge decision.

## 3. Oversight model

For an explicitly delegated workflow:

- intermediate story, experience, visual and production decisions use **human_on_exception** oversight;
- publication, merge and acceptance of material residual risk remain **human_only / human_gate**;
- producer and critic remain separate;
- a workflow-scoped decision record must document the delegation.

This does not globally change any specialist contract.

The contract's usual human gate is compressed only for the declared workflow and only because the accountable human owner explicitly delegated those reversible intermediate decisions.

## 4. What causes an exception to Kell

Do **not** escalate preference questions.

Escalate only when one of these is true:

1. factual evidence is missing and cannot be recovered from authoritative sources;
2. publication rights, consent or confidentiality is unclear;
3. two canonical sources conflict and precedence cannot be determined;
4. a requested change would alter a canonical brand/product rule outside workflow authority;
5. accepting a blocker creates material legal, reputational, accessibility or security risk;
6. the workflow has exhausted its bounded deliberation/retry budget without resolving a material conflict;
7. the final artifact is publish-ready and needs merge/publication approval.

Everything else is routed to the relevant expertise.

## 5. Deliberation object

A material question is a first-class object.

Minimum fields:

```json
{
  "question_id": "q_...",
  "decision_ref": "decision_...",
  "raised_by": "agent_id",
  "topic": "visual | content | narrative | experience | evidence | accessibility | engineering | motion | provenance | process",
  "question": "What specifically is unresolved?",
  "evidence_refs": [],
  "owner_agent": "agent_id",
  "challenger_agent": "agent_id",
  "arbiter_agent": "agent_id",
  "severity": "advisory | material | blocker",
  "state": "open | debating | resolved | escalated",
  "resolution": null
}
```

Questions must be specific enough to change a decision.

"Does this feel premium?" is invalid.

"Does the hero still read as three independent columns at 390 px?" is valid.

## 6. Expertise routing

Default routing for editorial-web work:

| Topic | Primary owner | Challenger / second lens | Arbiter |
| --- | --- | --- | --- |
| facts / repository truth | repository-analyst | research-synthesist | readiness-evaluator |
| narrative | editorial-storyteller | experience-designer | creative-director |
| content hierarchy / UX writing | experience-designer | editorial-storyteller | creative-director |
| information architecture / interaction | experience-designer | accessibility-auditor or inclusive-experience-reviewer | creative-director |
| art direction | editorial-art-director | visual-storyteller / experience-designer | creative-director |
| typography | editorial-typography-director | editorial-art-director | creative-director |
| photography / crop / image treatment | photo-art-director | editorial-art-director | creative-director |
| data/evidence visualization | data-visualization-engineer | repository-analyst | creative-director |
| motion | motion-web-director | accessibility-auditor | creative-director |
| implementation | frontend-engineer | code-reviewer | readiness-evaluator |
| accessibility / inclusion | accessibility-auditor | inclusive-experience-reviewer | readiness-evaluator |
| release evidence | readiness-evaluator | code-reviewer | human final gate |
| workflow / authority | workflow-architect | readiness-evaluator | human exception when required |

Specialists are activated only when their trigger is materially present.

Do not call typography, photo, motion or data visualization merely to simulate a large team.

## 7. Debate protocol

Each material disagreement runs at most **three structured rounds**.

### Round 1 — Position

Owner and challenger independently state:

- decision;
- evidence;
- criterion affected;
- risk of being wrong;
- recommended action;
- confidence.

No one sees the other's position before writing their own when independent judgment matters.

### Round 2 — Challenge

Each side may challenge:

- unsupported assumption;
- conflict with canonical evidence;
- downstream consequence;
- accessibility/content/implementation trade-off.

A challenge must identify the exact criterion at risk.

### Round 3 — Arbitration

The arbiter chooses:

- `KEEP`
- `REVISE <owner>`
- `COMBINE`
- `ESCALATE`

The rationale and evidence are recorded.

The arbiter may not produce the replacement artifact unless separately routed as an executor.

## 8. Revision routing

A failure returns to the **earliest owning decision**, not necessarily the latest executor.

Examples:

- mobile becomes a vertical pile → return to Experience Designer / Art Director, not Frontend alone;
- visual proof is beautiful but narrative is unclear → return to Storyteller;
- UI text is unreadable at 390 → return to Experience/Content before adding CSS tricks;
- implementation departs from approved art direction → return to Frontend;
- art direction depends on motion to feel complete → return to Art Director, not Motion Director;
- team section feels corporate because information structure is wrong → return to Experience/Story, not only visual production.

This is a primary anti-rework rule.

## 9. Bounded iteration

For one publishable page:

- maximum 3 material deliberation rounds per decision;
- maximum 2 production revision cycles for the same root cause;
- repeated recurrence of the same failure triggers root-cause review;
- a new visual route requires evidence that the existing route cannot meet the rubric;
- "try another version" without a diagnosed failure is prohibited.

The goal is not infinite polish.

## 10. "10/10" operating definition

"10/10" is a **quality target**, not an objective score.

The scorecard is used for disagreement detection and calibration. It cannot override a blocker.

A page reaches the final human gate only when:

1. all deterministic blocker checks pass;
2. no required semantic check is `fail` or `unknown`;
3. no material question remains open;
4. no unresolved specialist dissent remains;
5. the readiness evaluator returns `READY`;
6. every quality dimension has independent evidence;
7. the weighted publish-readiness score is at least **9.2/10**;
8. no dimension is below **9.0/10**;
9. subjective reviewer spread above **1.5 points** has been debated and resolved;
10. desktop + 390 + 320 renders have been inspected through a visual-evidence manifest with section anchors, content hashes and independent review IDs;
11. static composition passes with motion disabled;
12. accessibility/code/implementation reviews have no unresolved blocker;
13. provenance and public claims are publish-safe.

The numeric threshold is deliberately demanding, but the **blocker model remains authoritative**.

## 11. Publish-readiness council

Before final human review, the council receives the same frozen candidate.

Required independent reviews:

- Editorial Storyteller — narrative;
- Experience Designer — content hierarchy / responsive/task logic;
- Editorial Art Director — composition/craft;
- Creative Director — overall authorship/coherence;
- Accessibility Auditor — accessibility evidence;
- Code Reviewer — implementation quality;
- Readiness Evaluator — evidence sufficiency.

Conditional:

- Typography Director;
- Photo Art Director;
- Motion Web Director;
- Data Visualization Engineer;
- Inclusive Experience Reviewer.

The implementation producer does not score its own production-craft criterion as the deciding reviewer.

Primary and secondary reviews must come from **different execution runs** (`review_run_id`). Merely relabelling one execution as two specialist roles is not independent review.

Visual evidence must also be machine-checkable enough to catch QA failures such as a single screenshot being saved under multiple section names. Required captures therefore include section ID, DOM anchor, observed heading, artifact reference and SHA-256 content hash. Duplicate image content across different required sections in the same viewport is a blocker until explained and re-reviewed.

## 12. Final output to Kell

Kell should receive **one compact publication packet**, not the debate transcript.

Required:

- live/preview URL;
- desktop + 390 + 320 final renders;
- one paragraph explaining the final story and visual idea;
- final quality scorecard;
- accessibility/code/readiness status;
- publication/provenance risks;
- exact diff/PR;
- unresolved items: ideally none;
- recommendation: `PUBLISH` or `DO NOT PUBLISH`.

The full debate remains available as audit evidence, but does not burden the final gate.

## 13. Observability

Record:

- questions opened/resolved;
- owner/challenger/arbiter;
- root-cause category;
- deliberation rounds;
- revisions generated by each failure;
- first-pass score by dimension;
- final score by dimension;
- human exceptions;
- active time / wait / tokens when available.

Useful derived metrics:

- questions resolved without human intervention;
- average deliberation rounds;
- repeated root causes;
- score improvement per revision;
- tokens spent on rejected routes;
- number of human interventions before publication;
- final human revision after council says READY.

The most important learning signal is whether the final human gate still discovers material defects.

## 14. Invariants

- publication and merge remain human-owned;
- agents do not change their own authority;
- no fabricated evidence;
- no hidden disagreement;
- no producer self-certification;
- no quality score laundering a failed blocker;
- no endless debate;
- no escalation to Kell for ordinary specialist judgment;
- no implementation before the working PRD is internally coherent enough to support it.
