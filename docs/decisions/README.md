# Decision records

Architecture Decision Records (ADRs) preserve consequential decisions that must survive a chat, execution surface or repository boundary.

## Placement rule

- shared governance / orchestration / authority / observability → this directory in `agentic-factory`;
- domain-specific decision → `docs/decisions/` in the repository that owns that truth.

Do not copy a shared ADR into each consumer repository. Link it and record only the local consequence.

## PR traceability

A PR that implements or changes a durable decision should cite:

- the canonical decision ID;
- the canonical ADR or canonical reference;
- affected repositories;
- whether it conforms, extends or conflicts;
- any stacked or dependent PRs.

A conflicting proposal does not become canonical until the repository that owns the authority accepts it.

Machine-readable decision status lives in [registry.json](registry.json).

## Status

`proposed → accepted → superseded|deprecated`

Merge is the default acceptance gate unless an ADR names a different authority.

## Current records

- [ADR-0001 — Cross-repository decision governance](ADR-0001-cross-repository-decision-governance.md)
