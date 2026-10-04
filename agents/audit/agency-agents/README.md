# Agency Agents catalog audit

Status: **complete — ready for roster decision**.

This directory audits the public `msitarzewski/agency-agents` catalog against the local eusouakell Agentic Factory.

## Scope

- 282 README-listed agents inventoried.
- Every agent receives a first-pass role class, capability family and Factory-fit status.
- 80 agents received contract-level deep review because they could overlap with, strengthen or expose gaps in the current Registry V1.
- Domain-specific agents outside current goals remain accounted for but are not deep-read unless they expose a transferable capability.

## Files

- `catalog.csv` — complete inventory.
- `catalog.json` — complete machine-readable inventory + audit metadata.
- `capability-map.md` — generated first-pass summary.
- `deep-review.md` — completed contract-level findings.
- `roster-v2-proposal.md` — proposed Core / on-demand / future / control-plane split; registry unchanged pending approval.

## Decision rule

No external agent is installed automatically.

The external catalog is a benchmark for discovering capabilities, authority patterns and anti-patterns. The local Registry remains authoritative.
