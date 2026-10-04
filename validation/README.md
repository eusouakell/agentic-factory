# Agent validation

This directory records **real-task evidence** used to decide whether a registered agent should remain `pilot`, become `active`, or be changed/retired.

## Principle

A passing prompt demo is not validation.

A useful validation run must have:

- a real task with a consequence;
- an explicit trigger and scope;
- observable evidence;
- the declared authority boundary;
- a result that can be inspected later;
- limitations and unresolved uncertainty;
- a promotion recommendation separate from the human promotion decision.

See [workflow.md](workflow.md) for the full lifecycle/state-machine contract.

## Promotion gate

Registry policy remains:

`pilot → active → retired`

Promotion to `active` requires:

1. at least one real task;
2. evidence that the role boundary reduced ambiguity or rework;
3. no unresolved authority collision;
4. explicit human approval.

A validation record may recommend promotion. It cannot promote itself.

## Run outcomes

- **validated_once** — completed a real task with useful evidence;
- **needs_more_evidence** — task was real, but did not exercise enough of the role;
- **boundary_problem** — role collided with another agent/control layer;
- **failed** — output was materially unreliable or unsafe.

## Evidence model

Each run should record:

- agent;
- task;
- trigger;
- inputs;
- actions/output;
- evidence;
- useful contribution;
- errors/corrections;
- authority-boundary result;
- limitations;
- recommendation.
