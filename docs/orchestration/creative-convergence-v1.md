# Creative Convergence V1

**Status:** proposed reusable workflow mode  
**Primary pilot:** Bússola public case  
**Goal:** let specialist agents converge on a publish-ready artifact with minimal human traffic management.

## 1. Problem

A multi-agent system can still be inefficient when the human owner must:

- relay context between specialists;
- reconcile conflicting recommendations;
- decide which specialist speaks next;
- request each revision manually;
- reopen the same question several times;
- inspect half-finished artifacts before the team has converged.

That is not orchestration. It is human-mediated routing.

For high-craft work such as a public case, the team should be able to challenge, refine and reconcile its own work before surfacing a candidate to the human owner.

## 2. Desired behavior

The team receives:

- one approved problem/outcome;
- canonical repository context;
- a quality contract;
- bounded authority;
- a revision budget.

It then works through specialist disagreement internally until one of two states is reached:

### A. Publish-ready candidate

All required gates pass and a complete release packet exists.

Only then should Kell be asked to review.

### B. True human escalation

The system is blocked by something agents are not authorized or able to resolve, such as:

- a factual conflict with no authoritative source;
- a legal/consent/publication decision;
- a material brand/business decision not covered by existing authority;
- exhausted revision budget with unresolved blocker;
- mutually exclusive directions that remain equally defensible after arbitration.

Ordinary craft disagreements are **not** human escalations.

## 3. Core operating principle

> Specialists may disagree. They may not externalize an unresolved disagreement to Kell until the defined internal resolution path has been exhausted.

The objective is not consensus for its own sake. It is a stronger artifact with explicit ownership of decisions.

## 4. Roles in a convergence cell

A convergence cell is assembled from existing specialist contracts.

For a web/editorial case, the default cell is:

### Evidence lane
- Repository Analyst
- Research Synthesist

Owns:
- source truth;
- provenance;
- reference interpretation;
- factual conflicts.

### Story lane
- Editorial Storyteller
- Content/UX-writing authority when applicable

Owns:
- narrative;
- section purpose;
- claims;
- language;
- information burden.

### Experience lane
- Experience Designer

Owns:
- information architecture;
- responsive behavior;
- interaction model;
- accessibility-aware structure.

### Visual lane
- Editorial Art Director
- Graphic Editorial Designer
- Editorial Typography Director when triggered
- Motion Web Director when triggered

Owns:
- visual system;
- composition;
- typography;
- image/product/evidence relationships;
- motion.

### Production lane
- Flame UI Composer / Frontend Engineer

Owns:
- faithful execution;
- implementation quality;
- responsive implementation;
- build/test integrity.

### Independent challenge lane
- Creative Director
- Accessibility Auditor
- Code Reviewer
- Readiness Evaluator

Owns:
- independent critique;
- blocker detection;
- final evidence sufficiency.

## 5. Decision rights

Every question belongs to one owner.

Examples:

| Question | Primary owner |
| --- | --- |
| Is this factual claim supported? | Repository Analyst |
| Is this reference being copied rather than interpreted? | Research Synthesist / Art Director |
| Is this the right story beat? | Editorial Storyteller |
| Is this label understandable? | Content authority / Experience Designer |
| Should this section appear earlier? | Experience Designer |
| Does the composition feel generic? | Editorial Art Director |
| Does typography need another family? | Typography Director |
| Does this motion have a job? | Motion Web Director |
| Does implementation drift from approved direction? | Frontend + Creative Director review |
| Is this accessible enough to release? | Accessibility Auditor |
| Is evidence sufficient for publication? | Readiness Evaluator |

A role may challenge another role, but cannot silently override its decision domain.

## 6. Debate protocol

Debate is artifact-based, not chat-based.

Each review round produces a structured record:

```yaml
question: "Is the team section too institutional?"
raised_by: creative-director
owner: editorial-art-director
severity: blocker
evidence:
  - "current proof uses equal portrait cards"
  - "reference synthesis explicitly rejects leadership-directory grammar"
proposed_resolution: "replace with documentary/contact-sheet composition"
owner_response:
  decision: accept
  rationale: "aligns with approved art-direction principle"
artifact_change: "team proof v2"
status: resolved
```

Allowed statuses:

- `resolved`
- `rejected_with_rationale`
- `needs_arbitration`
- `human_escalation`

The dashboard should count unresolved rounds and repeated issue classes.

## 7. Internal resolution path

For every blocker:

### Step 1 — Owner response
The domain owner must either:
- accept and revise;
- reject with evidence/rationale;
- declare authority conflict.

### Step 2 — Challenger re-review
The challenger verifies whether the concern is resolved.

### Step 3 — Arbitration
If disagreement remains:
- Creative Director arbitrates craft conflicts;
- Repository Analyst arbitrates factual/source conflicts;
- Accessibility Auditor arbitrates accessibility blockers;
- Code Reviewer arbitrates implementation defects;
- Readiness Evaluator arbitrates evidence completeness.

### Step 4 — Human escalation only if necessary
Escalate only when:
- arbitration authority is insufficient;
- revision budget is exhausted;
- the issue is explicitly human-owned.

## 8. Revision budget

To prevent infinite “agent debate”:

- maximum **3 convergence rounds per major stage**;
- maximum **2 attempts on the same blocker class** without escalation;
- a repeated blocker must return to the **earliest owning stage**, not create a new downstream patch;
- after round 3, unresolved blocker → structured escalation.

A new round must cite what changed since the previous round.

No “try another variation” without a stated hypothesis.

## 9. Stage model

### Stage 0 — Intake / PRD

Output:
- problem;
- target audience;
- evidence;
- success criteria;
- constraints;
- explicit non-goals;
- publication risks;
- quality checklist.

Internal debate:
- Evidence + Story + Experience challenge completeness.

Exit:
- PRD passes intake gate.

### Stage 1 — Narrative / Experience

Parallel work:
- Story lane;
- Experience lane.

Then cross-review:
- Story challenges IA;
- Experience challenges narrative sequence.

Exit:
- one narrative/experience contract.

### Stage 2 — Art Direction

Art Director creates:
- visual system;
- section rhythm;
- representative proofs;
- responsive rules.

Cross-review:
- Story: does visual hierarchy tell the same story?
- Experience: does responsive behavior preserve meaning?
- Research: are references interpreted rather than copied?
- Creative Director: is it authored/distinctive?

Exit:
- art-direction gate passes.

### Stage 3 — Production

Production executes the approved system.

Cross-review:
- Creative Director checks fidelity;
- Experience checks responsive behavior;
- Content checks copy integrity;
- Accessibility checks semantic/access behavior.

Exit:
- complete candidate.

### Stage 4 — Release challenge

Run:
- Accessibility Auditor;
- Code Reviewer;
- Creative Director final review;
- Readiness Evaluator.

All blockers must resolve internally.

Exit:
- `publish_ready=true`.

### Stage 5 — Human publication gate

Kell receives only:
- live/staged URL;
- desktop + mobile evidence;
- concise change summary;
- checklist results;
- residual risks;
- PR ready to merge/publish.

No unresolved internal craft debate should appear here.

## 10. Definition of publish-ready

A page is not publish-ready because all tasks are done.

It is publish-ready only if:

### Narrative/content
- one-line retell works;
- every section has a distinct job;
- no unsupported claims;
- factual/provenance notes are correct;
- language is consistent and audience-appropriate.

### Experience
- desktop/mobile reading order is intentional;
- no essential interaction depends on hover/motion;
- product evidence is inspectable;
- responsive layout is authored.

### Visual
- one coherent visual system across the page;
- no generic template grammar;
- typography hierarchy is deliberate;
- images/UI/data/architecture belong to the same world;
- static page is complete without motion.

### Production
- implementation matches approved direction;
- no unexplained deviation;
- build/tests pass;
- no visual regressions at target viewports.

### Accessibility
- keyboard/focus/reflow/reduced motion pass;
- semantic structure is coherent;
- known assistive-tech gaps are named;
- no blocker remains.

### Evidence/readiness
- provenance complete;
- PoC vs production distinction clear;
- public links work;
- release notes complete;
- PR is mergeable.

## 11. Scoring

Do not use a single opaque 10/10 score as the control mechanism.

Use a rubric with independent dimensions, each 1–5:

- narrative coherence;
- content design;
- experience architecture;
- visual authorship;
- responsive quality;
- product/evidence legibility;
- accessibility;
- implementation fidelity;
- provenance/readiness.

Publish-ready threshold:

- **no dimension below 4/5**;
- average **≥ 4.5/5**;
- zero blockers;
- zero unresolved authority conflicts.

The purpose of the rubric is to expose weakness, not create false precision.

## 12. Autonomous question handling

When a question appears, the system must first classify it:

1. factual/source;
2. narrative/content;
3. experience;
4. visual;
5. motion;
6. implementation;
7. accessibility;
8. publication/readiness.

Then:
- route to domain owner;
- require evidence;
- record answer;
- update artifact;
- re-run only affected checks.

Do not route ordinary domain questions to Kell.

## 13. Observability additions

Record:

- debate issue created/resolved;
- issue class;
- owner;
- challenger;
- rounds to resolution;
- reopened issue;
- arbitration;
- human escalation;
- quality score by dimension per round;
- artifact accepted/rejected;
- tokens/time by round when observable.

Derived metrics:

- average convergence rounds;
- blockers per stage;
- most common disagreement class;
- percentage resolved without human input;
- human escalations per workflow;
- rework created downstream by upstream misses;
- quality-score change per round;
- accepted outcome / human interaction.

## 14. Bússola operating mode

For the Bússola public case:

- Kell does **not** review the current intermediate Direction/PRD packet.
- The team continues from PRD through production and release challenge.
- The current art-direction packet may be treated as V1 input, not immutable truth.
- Agents may reopen earlier choices when a downstream specialist produces evidence of a real conflict.
- The team must converge on one complete staged landing page.

Kell is called only when:
- the page is staged and publish-ready; or
- a true human escalation occurs.

## 15. Final human packet

The final packet should fit on one screen:

### Candidate
- staging/live preview URL

### What changed
- 3–5 consequential changes

### Quality
- dimension rubric;
- blockers: 0;
- unresolved issues: 0;
- accessibility/code/readiness status.

### Evidence
- desktop screenshot;
- 390px screenshot;
- 320px screenshot.

### Risk
- only residual risks that remain after internal resolution.

### Action
- `APPROVE PUBLISH`
- `REJECT WITH ONE MATERIAL REASON`

The human should not need to perform design QA from scratch.

## 16. Success criterion

The workflow succeeds if Kell receives a materially stronger page with fewer intermediate interventions than the previous manual loop.

The target is:

> **one final review, not continuous supervision.**
