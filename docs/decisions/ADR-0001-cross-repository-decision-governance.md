# ADR-0001 — Cross-repository decision governance

**Status:** accepted  
**Decision owner:** Kell  
**Scope:** Agentic Factory and all consumer repositories  
**Date:** 2026-10-11  
**Decision ID:** `cross-repo-decision-governance`

## Context

Work now spans multiple repositories and execution surfaces, including concurrent ChatGPT/Codex conversations. Chat history is useful working context, but it is not durable authority. Without an explicit cross-repository decision protocol, the same architectural or operating question can be solved independently in multiple repos, producing silos, contradictory rules, duplicated agents or divergent workflow assumptions.

The Agentic Factory already defines the canonical control plane while domain repositories retain domain truth. This ADR makes the decision-record layer explicit.

## Decision

### 1. Put decisions where their authority lives

- **Cross-repository governance, orchestration, authority, observability and reusable workflow decisions** live in `agentic-factory/docs/decisions/`.
- **Domain decisions** live in `<domain-repo>/docs/decisions/`.
- A local ADR may consume a cross-repository ADR, but must not silently redefine it.
- Domain truth remains owned by the domain repository. The Factory does not become a content, brand or product source of truth.

### 2. PRs are the implementation/review envelope

Every consequential decision should be implemented through a PR that links the relevant ADR(s).

A PR should state:
- decision(s) implemented;
- affected repositories;
- dependencies or stacked PRs;
- canonical sources;
- residual conflicts or open decisions;
- whether README synchronization is required.

For concurrent work, prefer **stacked PRs or explicit dependency links** instead of copying pending decisions into another branch.

### 3. Chats are not durable authority

A conversation may propose or clarify a decision, but a decision required by future work must be externalized before it is treated as durable.

Recovery order:

```text
PROJECT / ISSUE STATE
→ ACCEPTED ADRS
→ CANONICAL DOMAIN DOCS
→ APPROVED ARTIFACT / PR
→ CURRENT EXECUTION CONTEXT
```

If these sources conflict, stop and resolve the conflict at the owning authority. Do not infer the answer from remembered chat history.

### 4. Cross-repository contradictions must be explicit

When a local project needs behavior that appears to conflict with a shared Factory decision:

1. record the conflict;
2. identify whether the disagreement is governance or domain truth;
3. route governance conflicts to the Factory;
4. route domain conflicts to the owning repository;
5. supersede one decision explicitly if the conflict is real.

Do not keep two active rules for the same decision class without a documented scope boundary.

### 5. ADR lifecycle

Allowed statuses:

- `proposed`
- `accepted`
- `superseded`
- `deprecated`

An ADR should include:
- context;
- decision;
- authority/scope;
- consequences;
- affected repositories;
- rollout or migration notes;
- related ADRs/PRs;
- unresolved questions.

## Consequences

### Positive

- concurrent chats can resume from durable state;
- Bússola, Cereja and future projects can reuse the same orchestration rules without copying them;
- domain repos remain autonomous for domain truth;
- contradictions become reviewable artifacts rather than invisible drift;
- PR history provides implementation evidence for each accepted decision.

### Cost

- consequential cross-repository changes require one additional decision record;
- stacked work may temporarily depend on an unmerged parent PR;
- maintainers must resolve scope before duplicating a rule locally.

The intended cost is small. ADRs should record decisions, not become project diaries.

## Immediate application

- Creative Convergence remains defined in Agentic Factory and validated through the Bússola pilot.
- Cereja Flamejante consumes the shared convergence/governance model but records its editorial and marketing decisions locally.
- Work happening in a separate Bússola conversation is not edited by the Cereja planning branch; cross-project changes must be linked through Factory decisions instead.

## Related

- `governance/operational-work-state.md`
- `governance/first-class-decisions.md`
- `docs/orchestration/creative-convergence-v1.md`
- PR #36 — Creative Convergence V1
- PR #37 — accepted this ADR
