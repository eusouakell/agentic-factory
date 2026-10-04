# Agentic Factory

**Canonical control and agent registry for the eusouakell agentic system.**

This repository defines:

- the Agent Registry and specialist contracts;
- the control-plane boundary;
- Guides / Guards / Sensors / Checks / Evals / Human Gates;
- authority, provenance and lifecycle rules;
- integrations with domain repositories.

It does **not** own domain truth.

Current domain authorities remain:

- `cereja-knowledge-system` — Núcleo + Flame;
- `cereja-editorial-engine` — editorial workflow and publication gates;
- `marketing-context-system` — context routing and context-specific runtime.

## Core principle

> Agents are bounded capabilities. Authority lives in the control plane and canonical domain systems.

## Migration status

This repository is being seeded from the approved extraction plan in:

`eusouakell/marketing-context-system/docs/agentic-factory-extraction.md`

Migration follows:

`copy → validate → redirect/deprecate → remove`

Do not delete the source registry from Marketing Context System until this repository is validated and all consumers point here.
