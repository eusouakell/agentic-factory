# Change control

The Agentic Factory is a control system. Changes to authority, agent contracts and control-plane behavior therefore require explicit review.

## Sensitive paths

Human attention is required for changes to:

- `agents/registry.json`;
- `agents/contracts/**`;
- `control-plane/**`;
- `controls/**`;
- `governance/**`;
- `.github/**`;
- `ARCHITECTURE.md`.

`.github/CODEOWNERS` records path ownership.

## Pull-request rule

Do not make governance-sensitive changes directly on `main`.

A pull request should state:

1. what capability or control changes;
2. whether authority expands, narrows or stays unchanged;
3. which tests/checks ran;
4. whether any human gate changes;
5. whether provenance or domain ownership changes.

## Current single-maintainer phase

The repository currently operates with a single primary maintainer.

Therefore:

- CODEOWNERS documents ownership and future review routing;
- CI is a deterministic gate;
- semantic/human approval remains an explicit maintainer decision;
- mandatory independent approval should not be enabled until a second authorized reviewer exists.

## Future two-person review

When a second reviewer with write access is available, the `main` ruleset should require:

- at least 1 approval;
- code-owner review for owned paths;
- status check `registry` (emitted by the `Agent Registry Checks` workflow);
- conversation resolution;
- stale-approval dismissal or approval of the latest reviewable push.

## Invariant

No repository governance rule can grant an agent authority that its registry contract does not already declare.
