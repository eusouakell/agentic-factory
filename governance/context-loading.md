# Progressive context loading

## Purpose

Reduce role drift and hallucination by giving an agent the **smallest authoritative context that is sufficient for the current task**.

More context is not automatically better. Unrelated canonical material creates competing instructions, encourages agents to reopen settled decisions and makes it harder to distinguish authority from reference.

## Authority chain

The Factory does not own domain truth. It resolves and passes the applicable domain layers.

```text
TASK / APPROVED HANDOFF
        ↓
APPLICABLE DOMAIN CANON
        ↓
BRAND / PRODUCT / CHANNEL INSTANTIATION
        ↓
SURFACE / PROJECT CONTRACT
        ↓
AGENT CONTRACT
        ↓
EXECUTION SKILL / TOOL
```

A narrower layer may specialize a broader one. It may not silently contradict it.

If two applicable authorities conflict, stop and escalate instead of averaging them.

## Context packet

A run plan should pass only what the role needs to make its declared decision.

Prefer:

- the approved upstream artifact;
- the exact canonical file that governs the concern;
- the specific project/channel/component contract;
- unresolved uncertainties and human decisions;
- the agent's own contract;
- execution references only when needed.

Avoid:

- whole repositories as prompt context;
- every brand document for every visual task;
- every strategy file for an execution task;
- historical alternatives after a gate has selected one;
- external skills as substitutes for canonical domain rules.

## Progressive disclosure

Load context in layers.

### Layer 0 — task

Always include:
- current goal;
- approved inputs;
- declared output;
- stop condition / next gate.

### Layer 1 — domain authority

Load only the canonical rule set relevant to the task.

Examples:
- experience work → applicable Núcleo/Flame experience contract;
- editorial claim → evidence/source contract;
- Instagram execution → approved story/strategy/format artifact plus applicable Flame/channel rules.

### Layer 2 — project/surface

Load the artifact that narrows the decision:
- user flow;
- component contract;
- channel brief;
- design direction;
- acceptance criteria;
- project constraints.

### Layer 3 — execution aid

Load a skill, external reference or tool guide only after authority is resolved.

Execution aids can suggest implementation. They do not become policy.

## Gate preservation

After a human or declared system gate approves a decision, downstream roles receive the approved artifact as an input.

They should not regenerate alternatives for that decision unless:

- the artifact is internally contradictory;
- a required state/constraint is missing;
- implementation exposes a real feasibility conflict;
- a higher authority has changed;
- the human explicitly reopens the gate.

A downstream role that reopens strategy without one of these conditions is a boundary failure.

## Context conflict protocol

When context conflicts:

1. identify the exact conflicting statements;
2. identify each source and its authority level;
3. apply the documented precedence if one exists;
4. if precedence does not resolve the conflict, stop;
5. route to the declared human/domain owner.

Do not reconcile ambiguity by inventing a compromise.

## Context provenance

A run artifact should make it possible to reconstruct:

- which canonical sources were loaded;
- which approved upstream artifact was used;
- which execution skill/reference was consulted;
- which assumptions remained unresolved.

This does not require logging every token or prompt. Record only the sources that materially governed the decision.

## Role of the control plane

The control plane should decide **what context is eligible**, not ask the active agent to browse the whole system and choose its own authorities.

The run plan may provide:
- required sources;
- optional sources unlocked by a condition;
- forbidden/out-of-scope sources;
- the gate after which the role must stop.

This is context routing, not semantic decision-making.

## Example — social editorial pipeline

```text
approved story route
  + Instagram strategy contract
        ↓
Instagram Strategist
        ↓ FORMAT/GOAL GATE

approved story
  + approved format/goal brief
  + carousel planner contract
        ↓
Carousel Planner
        ↓ OUTLINE GATE

approved outline
  + Flame visual rules
  + Visual Storyteller contract
        ↓
Visual Storyteller
```

The Carousel Planner should not receive enough latitude to replace the approved story. The Visual Storyteller should not receive unresolved format strategy.

## Example — future app flow

```text
product task + acceptance criteria
  + Núcleo experience principles
  + Flame experience contract
  + platform contract
  + relevant component/state contracts
        ↓
bounded product/UX role
        ↓
flow/spec artifact
        ↓
independent checks/evals
```

Do not load social/editorial channel rules into an app task unless the product explicitly reuses that surface.

## Verification

A context-routing design is healthy when:

- the role can state which authority owns each material decision;
- downstream roles preserve approved upstream choices;
- external skills do not override domain policy;
- context packets remain small enough to inspect;
- conflicts cause escalation rather than synthesis-by-guessing;
- the final artifact records the material source chain.
