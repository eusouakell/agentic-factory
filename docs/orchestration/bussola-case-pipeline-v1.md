# Bússola Public Case — Orchestrated Design Workflow V1

**Status:** proposed pilot  
**Outcome:** produce a publishable public case that demonstrates product/design/content craft without template-like visual language or repeated human micro-direction.

## 1. Why this workflow exists

The current redesign loop produced several increasingly specific visual proofs, but the upstream decisions were not consolidated into one binding PRD/art-direction packet before implementation.

This workflow treats those iterations as evidence, not as the new source of truth.

The pilot tests whether the Agentic Factory can:

- synthesize repository truth and visual references once;
- make specialist decisions in the right order;
- preserve approved upstream artifacts;
- reduce Kell’s role from continuous traffic manager to two meaningful gates;
- measure time, retries, human wait and token usage.

## 2. Canonical context

The workflow must load, at minimum:

### From `eusouakell/bussola`

- `docs/ux/editorial-case-v6-evidence.md`
- `docs/ux/review-v6-content-team.md`
- `docs/ux/case-v7-editorial-ui-brief.md`
- `docs/ux/visual-reference-bank-v1.md`
- current `web/public/case/index.html`
- current visual proofs and responsive renders relevant to the case
- repository history needed to distinguish hackathon work from later refinement

### Negative evidence

Current V7/V8 hero proofs may be used to document failures such as:

- template/SaaS grammar;
- “editorial” reduced to serif + whitespace;
- stacked floating cards mistaken for depth;
- desktop composition resized rather than re-authored for mobile;
- motion introduced before static composition is strong;
- team presented as institutional directory rather than hackathon/documentary evidence.

Negative evidence is not visual authority.

## 3. Workflow graph

```text
INTAKE
  ↓
[Repository Analyst] ─────┐
                          ├─→ CONTEXT PACKET
[Research Synthesist] ────┘
            ↓
[Editorial Storyteller]
            ↓
[Experience Designer]
            ↓
[Editorial Art Director]
      ↘ [Editorial Typography Director] when needed
            ↓
[Creative Director preflight]
      ├─ REVISE → correct upstream owner (max 1 focused loop)
      └─ PASS
            ↓
KELL — DIRECTION / PRD GATE
            ↓
[Flame UI Composer / Graphic Editorial Designer]
            ↓
[Motion Web Director] only if static composition already passes
            ↓
[Frontend Engineer]
            ↓
[Accessibility Auditor] + [Code Reviewer]
            ↓
[Readiness Evaluator]
            ↓
KELL — FINAL / MERGE GATE
```

The control plane owns routing, task state, retries and handoffs. No specialist self-activates another specialist.

## 4. Task contracts

### T1 — Repository truth packet

**Agent:** `repository-analyst`

**Job:** map the current case, evidence, assets, implementation history and design drift.

**Output:** `case-context-packet.md`

Must separate:

- confirmed facts;
- approved copy;
- evidence/provenance constraints;
- existing assets;
- implementation constraints;
- unresolved factual issues;
- failed/rejected visual directions.

Must not propose a redesign.

### T2 — Reference synthesis

**Agent:** `research-synthesist`

**Job:** turn the reference bank into design principles rather than a moodboard.

**Output:** `reference-synthesis.md`

For each retained reference:

- exact design problem it solves;
- compositional principle;
- responsive behavior worth learning from;
- what must not be copied;
- relevance score;
- confidence/limitations.

Only add new references when a material gap remains.

### T3 — Narrative architecture

**Agent:** `editorial-storyteller`

**Inputs:** T1 + T2.

**Job:** identify the strongest case-story progression already supported by evidence.

**Output:** `narrative-architecture.md`

Required:

- central tension;
- section sequence;
- hook;
- turn;
- payoff;
- one-line retell;
- what to omit;
- factual risks.

No layout or final visual composition.

### T4 — Experience/content structure

**Agent:** `experience-designer`

**Inputs:** approved narrative architecture + context packet.

**Job:** define information architecture, responsive reading order and interaction behavior.

**Output:** `experience-structure.md`

Must define:

- section purpose;
- content hierarchy;
- what must be immediately visible;
- what may be progressive disclosure;
- desktop/mobile behavior by section;
- before/after comparison behavior;
- prototype embedding behavior;
- accessibility implications;
- where motion has no job.

This task owns structure, not art direction.

### T5 — Art-direction packet

**Agent:** `editorial-art-director`

**Inputs:** T1–T4 + reference synthesis.

**Job:** create one coherent visual world for the entire case before page implementation.

**Output:** `art-direction-packet.md` plus visual proofs.

Must include:

- one dominant visual idea for the case;
- color/materiality rationale;
- type × image relationship;
- scale and crop rules;
- treatment of product UI;
- treatment of data/evidence;
- treatment of architecture;
- treatment of team/documentary photography;
- desktop/mobile composition logic;
- section rhythm;
- explicit anti-patterns;
- 2–3 representative visual proofs, not a full coded page.

A text-only direction fails this task.

### T5b — Typography review

**Agent:** `editorial-typography-director` only when T5 creates a material typographic system decision.

**Job:** validate hierarchy, families/fallbacks, responsive scale, long-form reading and technical metadata treatment.

### T6 — Independent creative preflight

**Agent:** `creative-director`

**Authority:** review only.

**Decision:** `PASS | REVISE`

Evaluate:

- coherence across story + UX + art direction;
- memorability;
- authorship;
- restraint;
- whether the case still looks like a generic template;
- whether product/evidence remains legible;
- whether mobile is genuinely composed, not merely resized.

One focused revision only. If the same failure repeats, escalate to Kell instead of generating more routes.

## 5. Quality Gate A — Direction readiness

Before Kell receives the packet, run the Bússola Direction Readiness checklist defined in `docs/orchestration/quality-gates-v1.md`.

Blockers include:

- source-of-truth/evidence boundaries incomplete;
- narrative or section purpose unresolved;
- mobile reading order undefined;
- no representative mobile proof;
- generic SaaS/card-grid grammar remains;
- motion is required to make the static composition work;
- Creative Director = REVISE.

A blocker failure routes back to its owning upstream task. It does **not** become another vague manual review request to Kell.

Checklist execution emits portfolio-level quality events.

## 6. First human gate

### KELL — DIRECTION / PRD GATE

Kell receives one packet containing:

- context truth;
- narrative architecture;
- experience structure;
- art direction;
- representative proofs;
- Creative Director verdict;
- unresolved decisions only.

Kell should not need to reconstruct previous specialist conversations.

Possible outcomes:

- `APPROVE`
- `REVISE <specific owner>`
- `STOP / REFRAME`

No production implementation before approval.

## 7. Production after approval

### T7 — Visual/interface execution

Use the minimum production role set needed by the accepted direction:

- `flame-ui-composer` for web/interface composition;
- `graphic-editorial-designer` when static graphic/editorial assets or specific visual spreads require specialist production.

They execute the accepted direction. They do not reopen strategy.

### T8 — Motion

**Agent:** `motion-web-director`

Trigger only when motion has a defined job such as:

- orientation;
- narrative transition;
- revealing relation between evidence layers.

No motion exists only to make an otherwise weak composition feel premium.

Required:

- reduced-motion equivalent;
- performance budget;
- trigger/state map.

### T9 — Frontend implementation

**Agent:** `frontend-engineer`

Implements approved artifacts on a proposal branch.

Guards:

- no new visual direction;
- no silent token/font/component invention;
- no rewriting approved copy;
- responsive implementation follows T4/T5;
- implementation diff remains scoped.

### T10 — Independent QA

Run after implementation:

- `accessibility-auditor`;
- `code-reviewer`;
- `readiness-evaluator`.

Accessibility and code review may run in parallel. Readiness consumes both.

## 8. Quality Gate B — Release readiness

Before the final human decision, run the Bússola Release Readiness checklist defined in `docs/orchestration/quality-gates-v1.md`.

Blockers include:

- implementation drift from approved direction;
- missing desktop/390/320 evidence;
- unresolved accessibility/code blocker;
- incomplete provenance/publication risk;
- reduced-motion behavior missing when motion exists;
- readiness evidence incomplete;
- telemetry insufficient to compute pilot metrics.

## 9. Final human gate

### KELL — FINAL / MERGE GATE

Packet:

- preview/screenshots desktop + 390 + 320;
- final diff/PR;
- accessibility findings;
- code-review findings;
- readiness result;
- deviations from approved direction;
- unresolved publication risks.

Kell decides merge/publication.

## 10. Content-design standard

The case must demonstrate content-design judgment, not only visual polish.

Required qualities:

- narrative order reduces explanation burden;
- each section has one job;
- labels and annotations explain evidence without turning the page into documentation;
- no unsupported product promises;
- hackathon PoC vs later refinement is explicit;
- synthetic data limitations remain understandable without legalistic repetition;
- UI copy remains simple and natural;
- no “AI agentic/agentiva” jargon where “agentes de IA” is clearer;
- visual hierarchy and text hierarchy tell the same story.

## 11. Visual quality bar

The page should be rejected before production if it can be accurately described as any of:

- generic fintech landing page;
- generic Tailwind/SaaS;
- “editorial” because it uses serif and whitespace;
- portfolio template with pasted screenshots;
- corporate leadership/team directory;
- collection of cards in different z-indexes;
- desktop layout stacked vertically for mobile;
- motion masking weak static design.

The desired synthesis remains:

**human protagonist + financial evidence + product craft + technical depth**

but this phrase is a design criterion, not a layout prescription.

## 12. Pilot observability

Every task emits telemetry events defined by the Orchestration & Observability V1 PRD.

For this pilot, record:

- task start/end;
- agent;
- execution surface;
- artifact produced;
- revision edge;
- human gate open/close;
- retries;
- token usage quality;
- final acceptance;
- quality-gate open/pass/fail/override events;
- checklist criterion evidence and owner.

At completion, compare:

- cycle time;
- active execution time;
- human wait;
- rework ratio;
- human gate count;
- first-pass acceptance;
- token consumption where available.

## 13. Pilot hypothesis

The workflow succeeds if it produces a stronger design with fewer human-directed micro-iterations than the current manual loop.

The hypothesis is **not** that more agents increase quality.

The hypothesis is:

> correct sequencing + shared authoritative context + bounded specialist ownership + observable handoffs reduces rework.

