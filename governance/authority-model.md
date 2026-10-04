# Authority model

## Principle

An agent's capability is not the same thing as its authority.

The registry must declare both.

## Write-authority classes

Current Registry V2 uses:

### `review_only`
Read, inspect and emit findings. No source mutation.

### `research_artifacts`
May create bounded research outputs. Does not change canonical truth.

### `design_artifacts`
May create workflow/architecture/specification artifacts. Does not grant implementation authority.

### `domain_assets`
May create scoped creative/visual assets under a domain brief. Does not publish.

### `proposal_branch`
May change code/assets on an explicit task branch. Cannot merge to `main`.

## Canonical authority

Canonical truth remains in domain repositories.

Examples:

- Flame owns visual-system truth;
- Núcleo owns knowledge/evidence/thesis truth;
- Editorial Engine owns editorial workflow and publication gates;
- Marketing Context System owns context-routing behavior.

An agent may propose a change to canonical authority, but may not silently make itself authoritative.

## Permission invariants

No agent may:

- widen its own tools;
- change its own tier/status;
- bypass a failed Guard/Check;
- grant another agent authority;
- self-approve release/publication;
- merge directly to `main`;
- redefine canonical domain rules without the declared human gate.

## Least privilege

Tool access should be:
- task-scoped;
- time/run-scoped where possible;
- no broader than the declared trigger requires;
- revocable;
- observable.
