# Agency Agents — contract-level deep review

Status: **complete for roster-relevant capabilities**.

## Method

The audit uses two layers:

1. **Complete inventory:** all 282 README-listed agents are present in `catalog.csv/json`.
2. **Contract-level review:** 80 agents were read at contract level because they could plausibly change the local Agentic Factory, expose a capability gap, or reveal a useful control pattern.

The remaining agents are predominantly vertical/domain specialists or variants whose metadata is sufficient to classify them as outside current scope or non-priority. They are still present in the complete inventory.

Upstream license verified: **MIT**. The local Factory does not copy upstream agent files; it records capability provenance and writes its own contracts.

## What the catalog gets right

Across the strongest agents, recurring useful patterns are:

- explicit triggers and scoped roles;
- evidence before approval;
- read-only audit roles separated from executors;
- retry limits and escalation;
- baseline-before-optimization;
- rescan/retest after remediation;
- least privilege;
- concrete artifacts rather than vague "expert" prose;
- measurable acceptance criteria;
- human approval where judgment remains semantic.

These patterns are compatible with the local Guides / Guards / Sensors / Checks / Evals / Human Gates model.

## What should NOT become agents

Several upstream roles are better represented elsewhere in our architecture:

| Upstream role | Local treatment | Why |
|---|---|---|
| Agents Orchestrator | **Control plane** | routing, retry, handoff, state and escalation are infrastructure, not a privileged persona |
| Git Workflow Master | **Guide / repository policy** | branch/commit conventions should constrain all agents |
| Minimal Change Engineer | **Guard for executors** | "smallest necessary diff" is a system-wide implementation rule |
| Prompt Engineer | **Guide + eval practice** | prompt contracts/versioning/regression matter; a standalone persona adds little. Do not depend on hidden chain-of-thought scaffolds |
| Experiment Tracker | **Sensors + experiment protocol** | baselines, hypotheses and measurement belong to the evaluation loop |
| Brand Guardian | **Canonical brand Guide + human gate** | brand authority must remain outside an autonomous persona |
| UI Finish-Gate Reviewer | **Flame eval pattern** | its evidence/product-specificity checks strengthen Flame review rather than require another permanent agent |
| Content Creator / LinkedIn Content Creator | **Editorial Engine + channel Guides** | channel composition should consume the same approved editorial packet, not create competing content authorities |
| Executive Summary Generator | **Reusable writing skill** | deterministic structure is useful, but it does not need autonomous agent authority |
| Meeting Notes Specialist | **Extraction skill** | bounded transformation of source material; no separate autonomous role needed |
| Master Plan Architect | **Planning Guide** | red-team planning is valuable, but "plan before execute" is a mode/contract |
| Studio Producer / Chief of Staff | **Human/project layer** | broad coordination roles would overlap the control plane and create ambiguous authority |

## Existing Registry V1 — decisions

| Local V1 agent | Decision | Deep-review influence |
|---|---|---|
| Frontend Engineer | **Keep; strengthen** | Frontend Developer + Minimal Change + performance/i18n/accessibility patterns |
| Security Auditor | **Keep; strengthen** | AI-Generated Code Auditor + AppSec + Secrets Hygiene; architecture/privacy remain escalations |
| Production Readiness Evaluator | **Keep; strengthen** | Reality Checker + Evidence Collector; remove hard-coded aesthetic heuristics |
| Flame UI Composer | **Keep; strengthen** | UI Designer + UI Finish Gate + Brand Guardian, while Flame remains canonical |
| Motion Web Director | **Keep** | Whimsy Injector's purposeful delight belongs here, not as its own agent |
| Motion Video Director | **Keep** | Short-Video Editing Coach validates narrative/pacing/audio/kinetic type scope |
| Editorial Typography Director | **Keep** | remains a genuine catalog gap: typography is otherwise scattered across UI/brand/document roles |
| Photo Art Director | **Keep** | Visual Storyteller validates photography direction + narrative scope |
| Generative Photography Specialist | **Keep** | Image Prompt Engineer validates technical generation capability, with stricter likeness/rights boundaries locally |
| Inclusive Visual Reviewer | **Evolve** | Inclusive Visuals + Cultural Intelligence show the capability should review workflows/copy as well as imagery |

## Strong gaps found

### 1. Research Synthesist — real gap
The upstream Research Synthesist has one of the cleanest contracts in the catalog: primary-source tracing, evidence grading, disagreement preservation, search-boundary disclosure and explicit confidence.

**Recommendation:** add a local **Research Synthesist** as a core agent.

### 2. Accessibility Auditor — real gap
Our deterministic Flame gates cover machine-checkable failures, but they cannot prove actual accessibility. The upstream agent correctly requires WCAG 2.2 references, keyboard-only and real assistive-technology testing, zoom/reflow and reduced-motion checks.

**Recommendation:** add **Accessibility Auditor** as an independent core reviewer. It must never equate a clean automated scan with conformance.

### 3. Code Reviewer — real gap
Security review and readiness review do not replace maintainability/correctness review. The upstream Code Reviewer has a useful read-only, prioritized, teaching-oriented boundary.

**Recommendation:** add **Code Reviewer** as a core review agent.

### 4. Experience research — real gap, but simulated personas are not evidence
UX Researcher is strong on method, consent, sampling and triangulation. Persona Walkthrough is useful for hypothesis generation but explicitly admits it is qualitative simulation.

**Recommendation:** create one on-demand **Experience Researcher**. Persona simulation may be a method inside it, labeled as hypothesis generation — never as user evidence. Feedback Synthesizer can feed this role.

### 5. Test automation — real operational gap
The Test Automation Engineer cleanly separates E2E from unit/API tests, owns deterministic data, artifacts and flake control.

**Recommendation:** add **Test Automation Engineer** on demand.

### 6. Workflow specification — real gap
Workflow Architect's branch/failure/recovery/observable-state discipline is useful before implementation. Its tendency to require specific other agents should not be copied.

**Recommendation:** add an on-demand **Workflow Architect** with local routing contracts.

### 7. Repository understanding & drift — merge two roles
Codebase Onboarding Engineer is excellent for read-only factual repo explanation. Codebase Archaeologist is strong on multi-session drift and cross-file intent mismatch.

**Recommendation:** combine them into one on-demand **Repository Analyst** with two modes: `onboard` and `drift-audit`.

### 8. Agent tooling — merge MCP + developer tooling
MCP Builder and Developer Tooling Engineer cover tool contracts, typed interfaces, actionable errors, stable outputs and agent testing.

**Recommendation:** create **Agent Tooling Engineer** on demand. It builds tools; the control plane decides who may use them.

### 9. Knowledge retrieval — merge RAG + graph + relevance
RAG Pipeline Engineer, Knowledge Graph Engineer and Search Relevance Engineer all share the same core discipline: explicit retrieval objective, gold/judgment sets, provenance, evaluation and no vibe-based tuning.

**Recommendation:** create **Knowledge Systems Architect** on demand with three modes: retrieval, graph, relevance. Do not create three permanent agents.

### 10. Discoverability — merge SEO + AEO/GEO + agentic readiness
SEO Specialist, AI Citation Strategist, AEO Foundations Architect and Agentic Search Optimizer represent related but fast-changing layers.

**Recommendation:** create **Discoverability Architect** on demand with separate SEO / AI-citation / agent-readiness modes. Any claims about crawler behavior, standards or browser support require fresh verification at execution time.

### 11. Data visualization — distinct specialist
Data Visualization Engineer adds perceptual honesty, accessible charting and large-data rendering that Flame/UI roles do not cover.

**Recommendation:** add **Data Visualization Engineer** on demand.

## Capabilities that should stay conditional, not permanent

| Capability | Reason |
|---|---|
| Security Architect / IAM / Privacy Engineer | high value when a project has material auth/data risk; unnecessary as always-on agents |
| DevOps / SRE / Platform Engineer | activate when infrastructure becomes a real delivery surface |
| Technical Writer | useful for public SDK/API/docs projects; otherwise a skill is sufficient |
| PDF Engine / Universal Document Compiler | highly specialized; activate only for document-product work |
| Proposal Strategist | valuable for commercial/RFP work, but separate from the core Factory today |
| Tracking & Measurement / Ad Creative / Video Optimization | activate when paid media or channel operations become an explicit workflow |
| Business Strategist | useful outside software delivery; avoid mixing corporate strategy authority into the code/content control plane |
| Agentic Identity & Trust Architect | important when agents gain high-impact delegated actions; premature for current tool scopes |
| Model QA Specialist | activate when the Factory ships/owns ML models rather than simply consuming foundation models |

## Anti-patterns found

- broad agents that both design, execute and approve their own work;
- role descriptions with fixed tool paths or framework-specific assumptions masquerading as universal methodology;
- hard-coded numeric "success metrics" with no local baseline;
- channel agents that optimize algorithms at the expense of canonical content authority;
- orchestration personas with permission to spawn arbitrary agents;
- agents that rely on aesthetic adjectives or trend defaults rather than product evidence;
- autonomous promotion/routing without a human-approved risk envelope.

## Bottom line

The catalog is valuable as a **capability benchmark**, not as a package to install.

Its strongest contribution to our Factory is not 282 personas. It is a smaller set of reusable role boundaries and operational patterns that can be expressed as local agents, Guides, Guards, Sensors, Checks and Evals.
