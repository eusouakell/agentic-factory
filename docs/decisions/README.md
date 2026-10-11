# Decision records

Architecture Decision Records (ADRs) preserve consequential decisions that must survive a chat, execution surface or repository boundary.

## Placement rule

- shared governance / orchestration / authority / observability → this directory in `agentic-factory`;
- domain-specific decision → `docs/decisions/` in the repository that owns that truth.

Do not copy a shared ADR into each consumer repository. Link it and record only the local consequence.

## Status

`proposed → accepted → superseded|deprecated`

Merge is the default acceptance gate unless an ADR names a different authority.

## Current records

- [ADR-0001 — Cross-repository decision governance](ADR-0001-cross-repository-decision-governance.md)
