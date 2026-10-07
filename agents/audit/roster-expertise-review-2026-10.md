# Roster expertise review — 2026-10

## Scope

Re-evaluation of every registered Agent Registry V2 capability against:

- human professional analogue;
- actual contract depth;
- declared title / role type;
- seniority needed by the work;
- overlap and missing handoffs;
- real-task evidence, especially the #031 visual failure.

This is a capability review, not a lifecycle promotion. Existing `pilot/active` states remain unchanged unless a separate validation gate approves promotion.

## Main finding

The roster was stronger at **capability coverage** than at **professional organization**.

The largest failure mode was title inflation around creative work: planning roles could be routed as if they were senior direction. #031 showed that Visual Storyteller could define visual jobs but could not reliably replace an Editorial Art Director. More rules and references did not close that craft gap.

Registry V3 therefore separates:

- department;
- seniority;
- operational role type;
- routing tier;
- lifecycle evidence.

## Existing roster review

| Agent | Department | Seniority | Expertise assessment | Decision |
|---|---|---:|---|---|
| Frontend Engineer | Engineering | senior | Strong implementation boundary; not a web designer | keep |
| Research Synthesist | Strategy & Planning | senior | Strong evidence/research specialist | keep |
| Code Reviewer | Quality & Risk | senior | Strong independent technical critic | keep |
| Security Auditor | Quality & Risk | senior | Strong bounded security audit role | keep |
| Accessibility Auditor | Quality & Risk | senior | Correct expertise; still needs rendered/manual evidence | keep pilot |
| Production Readiness Evaluator | Quality & Risk | senior | Strong evidence-synthesis role; must not release | keep |
| Flame UI Composer | Experience | senior | Useful UI composition role; not senior editorial art direction or UX research | keep |
| Motion Web Director | Experience | director | Correct motion-system direction; frontend remains executor | keep pilot |
| Motion Video Director | Art & Design | director | Correct video/motion direction; lacks production executor downstream | keep pilot + add executor |
| Editorial Typography Director | Art & Design | director | Genuine specialist direction across media | keep pilot |
| Photo Art Director | Art & Design | director | Genuine photographic direction; not video capture/editing | keep pilot |
| Generative Photography Specialist | Production | mid | Correct bounded synthetic-image executor | keep pilot |
| Inclusive Experience Reviewer | Quality & Risk | senior | Correct independent inclusion review | keep pilot |
| Experience Researcher | Experience | senior | Correct research role; does not fill UX/interaction design gap | keep pilot + add Experience Designer |
| Test Automation Engineer | Quality & Risk | senior | Strong deterministic QA executor | keep |
| Workflow Architect | Agent Systems | lead | Strong state/handoff architecture role | keep |
| Repository Analyst | Engineering | senior | Strong evidence-based repo analysis; no write authority | keep |
| Agent Tooling Engineer | Agent Systems | senior | Strong typed-tool implementation role | keep |
| Knowledge Systems Architect | Agent Systems | lead | Strong architecture scope; keep separate from generic retrieval prompting | keep pilot |
| Discoverability Architect | Strategy & Planning | senior | Strong search/AI-discovery strategy scope | keep pilot |
| Data Visualization Engineer | Experience | senior | Strong specialist implementation/encoding role | keep pilot |
| Editorial Storyteller | Creative | senior | Strong narrative strategy, not final copywriting or art direction | reclassify role type to strategist |
| Instagram Strategist | Strategy & Planning | senior | Strong channel/objective/format strategy | reclassify role type to strategist |
| Instagram Carousel Planner | Creative | mid | Narrow format specialist; “director” overstated authority | reclassify to specialist |
| Visual Storyteller | Creative | mid | Useful visual-job planner; “director” and domain-asset authority overstated expertise | reclassify to specialist + design_artifacts |
| Creative Director | Creative | director | Correct senior semantic critic/preflight role; should remain review-only | keep |

## Confirmed gaps registered as pilots

### Editorial Art Director
**Gap:** senior composition and art-direction judgment between visual-story planning and execution.  
**Evidence:** #031 repeatedly satisfied textual visual rules while failing composition/taste.  
**Action:** registered as `editorial-art-director`, director, Art & Design.

### Graphic / Editorial Designer
**Gap:** final static craft executor downstream of approved art direction.  
**Action:** registered as `graphic-editorial-designer`, senior, Production.

### Experience Designer
**Gap:** UX/interaction structure between Experience Researcher and Flame UI Composer / Frontend Engineer.  
**Action:** registered as `experience-designer`, senior, Experience.

### Motion Designer
**Gap:** motion-craft execution downstream of motion direction.  
**Action:** registered as `motion-designer`, senior, Production.

### Video Editor / Post-production Specialist
**Gap:** real edit/post-production executor downstream of story/video direction.  
**Action:** registered as `video-editor-postproduction`, senior, Production.

## Gaps considered but intentionally not registered

| Capability | Decision | Trigger to reconsider |
|---|---|---|
| Video Producer / Cinematographer | conditional | recurring real-world capture/shoot production |
| Creative Copywriter | conditional | explicit need for final advertising/social copy not adequately covered by human-authorial workflow |
| Media Planner / Buyer | conditional | paid-media budget and buying operations become real scope |
| Community Manager | conditional | recurring moderation/community operations |
| Traffic Manager | do not create | control plane already owns routing/state/handoffs |
| Generic Social Media Manager | do not create | splits into strategy, creative, production and analytics instead of a mega-role |

## Social-media coverage after review

For a simple single post:

`Story → Instagram Strategist when needed → Visual Storyteller when needed → Editorial Art Director → Creative Director → Kell Gate → Graphic / Editorial Designer → QA → Publish Gate`

For carousel:

Insert Instagram Carousel Planner before visual planning.

This is intentionally different from #031: the next visual validation should be a **single post**, not another multi-frame potato rescue exercise.

## Web-design coverage after review

`Research/requirements → Experience Designer → Flame UI Composer → Motion Web Director when justified → Kell Design Gate → Frontend Engineer → Accessibility/Code/Readiness`

The prior gap was not another UI executor. It was experience/interaction design ownership.

## Motion/video coverage after review

`Story/channel → Photo/visual direction as applicable → Motion Video Director → Kell Video Direction Gate → Video Editor/Post-production → Motion Designer when needed → QA → Publish Gate`

Real filming still needs a conditional production/cinematography role when that work actually exists.

## Promotion requirement for new roles

All five new roles begin as `pilot` and disabled by default.

A title such as Director does not prove expertise. Promotion requires:

1. a real task;
2. inspectable output;
3. evidence that the role reduced ambiguity/rework;
4. no authority collision;
5. explicit Kell approval.

The planned first validation for Editorial Art Director should use one static post with one composition, not a carousel.
