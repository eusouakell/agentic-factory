# Agency-inspired operating model

## Why this exists

The Factory uses the useful part of a traditional agency model: **clear professional disciplines, seniority, handoffs and separation of strategy, direction, craft, production and review**.

This is a **capability map, not the Factory's top-level architecture**. Work starts from an outcome and, when a real choice exists, a governed first-class decision. The control plane selects only the capabilities required to support or execute that decision.

It does not reproduce account-management bureaucracy or create an agent for every historical agency job.

The control plane performs decision routing, traffic/state and authority responsibilities. It is infrastructure, not a Traffic Manager persona.

## Departments

### Strategy & Planning
Owns problem framing, audience/channel choices, evidence and success criteria.

Typical roles:
- Research Synthesist
- Instagram Strategist
- Discoverability Architect

### Creative
Owns narrative concept, editorial route and cross-discipline creative coherence.

Typical roles:
- Editorial Storyteller
- Instagram Carousel Planner
- Visual Storyteller
- Creative Director

The Creative Director remains an independent evaluator/preflight role. It is not the default producer.

### Art & Design
Owns art direction and specialist visual systems.

Typical roles:
- Editorial Art Director
- Editorial Typography Director
- Photo Art Director
- Motion Video Director

### Experience
Owns user flows, interaction design, interface composition and experience-specific craft.

Typical roles:
- Experience Researcher
- Experience Designer
- Flame UI Composer
- Motion Web Director
- Data Visualization Engineer

### Production
Executes approved creative/design direction into deliverable assets.

Typical roles:
- Graphic / Editorial Designer
- Generative Photography Specialist
- Motion Designer
- Video Editor / Post-production Specialist

### Quality & Risk
Independently tests, audits and synthesizes readiness.

Typical roles:
- Accessibility Auditor
- Inclusive Experience Reviewer
- Code Reviewer
- Security Auditor
- Test Automation Engineer
- Production Readiness Evaluator

### Engineering
Implements and analyzes software systems.

Typical roles:
- Frontend Engineer
- Repository Analyst

### Agent Systems
Designs and implements agentic infrastructure itself.

Typical roles:
- Workflow Architect
- Agent Tooling Engineer
- Knowledge Systems Architect

## Seniority

Registry seniority is a professional-depth signal, not an authority grant:

- `junior` — bounded execution with close specification;
- `mid` — independent bounded specialist work;
- `senior` — strong domain judgment and ambiguity handling;
- `lead` — system/discipline-level decisions across multiple artifacts;
- `director` — directional judgment spanning specialists and craft disciplines.

## Reference capability flows

These flows are reusable defaults, not mandatory org-chart pipelines. A decision record may skip capabilities that add no value.

### Static social / editorial post

```text
approved source/story
→ channel strategy when needed
→ Visual Storyteller (what must be shown; optional for simple single post)
→ Editorial Art Director (how the composition works)
→ Creative Director preflight
→ KELL — ART DIRECTION GATE
→ Graphic / Editorial Designer
→ QA / accessibility / provenance as applicable
→ KELL — PUBLISH GATE
```

For a carousel, insert the Carousel Planner after channel strategy. Do not force a carousel when a single post can prove the concept.

### Web experience

```text
research / requirements
→ Experience Designer
→ Flame UI Composer
→ Motion Web Director when motion has a job
→ KELL — DESIGN GATE
→ Frontend Engineer
→ Accessibility + Code Review + Readiness
→ human release/merge
```

Experience Designer owns flow/interaction logic. Flame UI Composer owns visual interface composition under Flame. Frontend Engineer owns implementation.

### Video / Reel

```text
approved story + channel objective
→ visual / shot direction
→ Motion Video Director when designed motion is needed
→ KELL — VIDEO DIRECTION GATE
→ Video Editor / Post-production Specialist
→ Motion Designer for non-trivial motion graphics
→ technical QA + creative review
→ KELL — PUBLISH GATE
```

A real shoot may additionally require a Video Producer / Cinematographer. That remains conditional until a concrete production task exists.

## Explicit non-agents for now

Do not register these merely to mirror a traditional agency org chart:

- Traffic Manager — control-plane responsibility;
- Account Manager — no current client-service workflow requires it;
- Media Buyer / Planner — register only when paid media becomes real scope;
- Community Manager — register only when community operations become recurring work;
- Creative Copywriter — current provenance model and authorial workflow require a concrete final-copy use case before creating a separate agent;
- Video Producer / Cinematographer — conditional on real capture/production.

## Producer / critic boundary

- Art Director directs; Graphic Designer executes.
- Motion Director directs; Motion Designer / Video Editor executes.
- Experience Designer designs interaction; Frontend Engineer implements.
- Creative Director evaluates; it does not self-certify work it produced.
- Production Readiness summarizes evidence; it does not publish.

This separation is a structural control, not stylistic preference.
