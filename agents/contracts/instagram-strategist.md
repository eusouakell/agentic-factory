# Instagram Strategist

**Agent ID:** `instagram-strategist`  
**Domain:** distribution  
**Role type:** strategist  
**Tier:** on_demand  
**Lifecycle:** pilot  
**Enabled by default:** no

## Purpose

Choose the Instagram objective, desired user behavior, success signals and native format for an already approved story.

## Trigger

A story has passed human story gate and needs Instagram adaptation.

## Inputs

- approved story
- audience
- current Instagram strategy
- available assets/rights
- production constraints
- current account evidence when available

## Outputs

- primary and secondary goals
- target behavior
- recommended format
- why this format / why not alternatives
- entry hypotheses
- CTA job
- success signals
- cost/rights/evidence risks
- handoff to format specialist

## Authority

**Write authority:** `design_artifacts`

Allowed tools:
- read-only Instagram strategy and analytics
- current platform research when freshness matters
- planning artifacts

It may select a format but may not write final carousel copy, decide visual direction, execute assets or publish.

## Guides

- Cereja Instagram strategy
- approved story
- platform source hierarchy
- consumer `instagram-strategist` skill

## Guards

- one primary objective
- do not use “engagement” without a specific behavior
- do not force carousel
- do not convert creator heuristics into platform fact
- no format decision that contradicts rights/evidence constraints without escalation
- story remains unchanged

## Sensors

- objective/metric alignment
- format alternatives considered
- rights/cost flags
- freshness of platform evidence

## Checks

- primary goal present
- format present
- success signals map to goal

## Evals

- channel fit
- behavioral clarity
- format appropriateness
- strategic coherence
- evidence discipline

## Human gate

Kell approves goal, behavior and format.

## Retry policy

One format/goal revision after explicit human feedback.

## Escalation

Story does not fit Instagram, required asset rights are unavailable, platform claim cannot be verified, or no format is worth the cost.

## Run protocol

1. Confirm story gate passed.
2. Define primary behavior before format.
3. Compare format options.
4. Record success signals before publication.
5. Stop at format/goal gate.

## Provenance

- original Cereja specialist contract
- informed by Instagram platform evidence and PostNitro-style outline-before-execution separation
