# ADR proposal — A2 execution and independent quality evidence

Status: proposed. Owner: Kell. Date: 2026-10-11.

## Decision

Do not call a single model's role-based review an independent multi-agent council. Implement actual bounded specialist invocations and persist their independent outputs, challenge/response, arbiter decision, and provenance. Keep human publication authority.

## Incremental delivery

1. A2 executor adapter: invoke distinct specialist runs with explicit contract, minimum authoritative context, task inputs, output schema, tool permissions and run ID. Persist outputs and failures. No agent can grant itself publication/merge authority.
2. Deliberation engine: challenger, domain owner, one revision budget, independent arbiter and escalation. Enforce transitions in runtime rather than only describing them in markdown.
3. Quality evidence: deterministic gates separated from semantic judgments and human decisions. A score must include reviewer provenance, calibration and unresolved dissent. No ungrounded 10/10 certification.
4. Visual acceptance: real browser capture at desktop/390/320, image geometry, typography hierarchy, layout overflow, loaded assets, accessible navigation and rendered prototype. Evidence must be from the actual deployment candidate, not mislabeled isolated-section screenshots.
5. Observability: record active time, retries, gate returns, unplanned work and human decisions. Distinguish elapsed waiting from human attention; never fabricate token/time telemetry.
6. Pilot: rerun Bússola only after A2 checks pass; retain the published landing as negative evidence and do not automatically republish.

## Release gates

- Unit and integration tests prove that specialist runs are distinct and outputs are persisted.
- Deliberation tests prove bounded retries, ownership and escalation.
- Visual QA fails on broken images, disproportionate image containers, horizontal overflow or severe hierarchy regressions; semantic art direction remains separately reviewed.
- Publish candidate includes PRD, ADR, screenshots, source provenance, disagreement log, test results and explicit residual risk.
- No automatic merge or publish.

## Scope boundaries

Canonical shared behavior lives in Agentic Factory. Bússola owns its case narrative, design and product evidence. Cereja owns editorial strategy. WikiLLM integration is separately tracked in issue #40.

## Acceptance

A real pilot must demonstrate at least two independently executed specialists with inspectable run IDs and evidence; the current single-surface council does not qualify.
