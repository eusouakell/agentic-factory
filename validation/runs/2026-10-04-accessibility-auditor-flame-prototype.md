# Validation run — Accessibility Auditor / Flame prototype

**Date:** 2026-10-04  
**Agent:** `accessibility-auditor`  
**Outcome:** `needs_more_evidence`  
**Task:** Audit the source-controlled Flame prototype against Flame's WCAG 2.2 AA baseline and broader accessibility contract.

## Trigger

A real web/design-system surface is under active development and is intended to become a reference for Cereja experiences.

## Inputs

Reviewed in `eusouakell/cereja-knowledge-system`:

- `brand/flame/prototype/site.html`;
- `brand/flame/prototype/index.html`;
- `brand/flame/prototype/tokens.css`;
- `brand/flame/accessibility.md`;
- `brand/flame/motion.md`;
- Flame visual-delivery sensor/check implementation.

## Output

Issue #16:

**Accessibility audit: Flame prototype focus order, control boundary and QA gaps**

## Findings

### 1. Responsive visual order vs DOM/focus order

At `max-width: 900px`, CSS moves the navigation using flex `order: 3`, while DOM order remains navigation before the subscribe CTA.

This can make keyboard focus appear to jump against the visual sequence.

Recommendation: align DOM and visual order; do not patch with positive `tabindex`.

### 2. Secondary-control boundary contrast

The secondary control boundary uses `#D8D6D1` against white/soft surfaces.

Measured contrast:
- ~1.45:1 against white;
- ~1.33:1 against `#F6F5F2`.

This is below Flame's 3:1 component-boundary target when the border is needed to identify the control.

### 3. Deterministic audit-tooling gap

The current HTML sensor reads inline `<style>` CSS but the real prototype uses a linked `tokens.css`.

Therefore the gate cannot reliably observe the real focus/reduced-motion CSS when run directly against those prototype files.

## Positive evidence

The source has a strong baseline:

- `lang="pt-BR"`;
- skip link;
- one main landmark;
- coherent heading hierarchy;
- explicit focus style;
- meaningful/empty alt usage is generally deliberate;
- reduced-motion CSS exists;
- primary action contrast is strong.

Spot checks:
- `#BE1035` / white ≈ 6.33:1;
- `#616161` / `#F6F5F2` ≈ 5.68:1;
- `#3A3A3A` / `#D7E25B` ≈ 8.08:1.

## Boundary result

**PASS**

The Accessibility Auditor emitted findings only. It did not mutate the implementation it audited and did not treat automated/static inspection as proof of conformance.

## Why more evidence is required

This run was source-level.

It did **not** exercise:

- actual keyboard traversal;
- screen-reader behavior;
- 200%/400% zoom and reflow;
- rendered target sizes;
- real reduced-motion behavior;
- cognitive/sensory comfort with production motion.

The agent explicitly preserved these as untested rather than claiming WCAG conformance.

## Promotion recommendation

**Keep `pilot`.**

Run a second validation on a rendered surface with keyboard + zoom/reflow and, where available, screen-reader testing before considering `active`.
