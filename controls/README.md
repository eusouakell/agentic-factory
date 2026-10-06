# Factory controls

The Factory separates control responsibilities instead of calling every rule an "agent".

| Layer | Purpose | Decides pass/fail? |
|---|---|---|
| Guide | orient execution | no |
| Guard | constrain before action | yes / block or escalate |
| Sensor | observe what happened | no |
| Check | compare against explicit expectation | yes / score or fail |
| Eval | semantic judgment with rubric | not necessarily binary |
| Human Gate | accountable approval | yes |

## Conceptual axes

The four core control types can also be understood through two orthogonal axes:

- **Feedforward ↔ Feedback** — whether the control acts before generation/execution or inspects what happened after it.
- **Descriptive ↔ Normative** — whether the control explains/observes the system or constrains/judges it against an expectation.

```text
                         DESCRIPTIVE
                              ↑
                Guides        │        Sensors
                              │
FEEDFORWARD ──────────────────┼────────────────── FEEDBACK
                              │
                Guards        │        Checks
                              ↓
                          NORMATIVE
```

This gives the four core classes a clear placement:

| Control | Timing | Nature | Role |
|---|---|---|---|
| **Guide** | feedforward | descriptive | explains context, method, intent and available paths |
| **Guard** | feedforward | normative | constrains or blocks an invalid/consequential action before it proceeds |
| **Sensor** | feedback | descriptive | observes and reports what actually happened |
| **Check** | feedback | normative | compares an observation/result against an explicit expectation |

### Evals and Human Gates

**Evals** extend the feedback side for semantic judgment that should not be reduced to a deterministic boolean. An eval must declare its rubric and whether it is primarily diagnostic/descriptive or normative against a quality threshold.

**Human Gates** are not a fifth quadrant. They are a cross-cutting authority mechanism used when intent, accountability, canonical change or residual risk requires an explicit human decision. A human gate may occur before or after execution depending on the decision being governed.

Conceptual framing adapted from the four-quadrant model shared by Kell from Chris Ford's *Agentic Engineering at Scale* (O'Reilly Media). The Factory extends that model with Evals and Human Gates because semantic quality and accountable authority are not fully represented by the four core quadrants.

## Guides

Guides provide orientation, context contracts, method and sequencing.

A Guide cannot:
- bypass a Guard;
- weaken a Check;
- grant tool permission;
- convert derived material into canonical truth.

## Guards

Guards constrain execution before an invalid or consequential action proceeds.

Examples:
- no direct write to `main`;
- no unapproved publishing;
- no tool-scope self-escalation;
- no confidential evidence in a public artifact.

A text-only prohibition is merely documented until a runtime mechanism can enforce or pause it.

## Sensors

Sensors report observable state.

Examples:
- selected context;
- test result;
- bundle size;
- animation count;
- source freshness;
- unresolved required domain.

A Sensor is not a gate.

## Checks

Checks add a criterion and consequence to an observation.

Prefer deterministic checks when possible.

Examples:
- registry schema valid;
- required contract exists;
- reduced-motion treatment present;
- required test suite passes.

## Evals

Evals handle semantic questions that should not be reduced to superficial booleans.

Examples:
- maintainability;
- evidence sufficiency;
- editorial fit;
- product specificity;
- visual hierarchy.

They should use explicit rubrics and emit uncertainty.

## Human Gates

Human approval remains required when authority, intent or accountability cannot safely be delegated.

Examples:
- merge/release;
- publication;
- canonical strategy or brand changes;
- sensitive representation choices;
- residual high-impact risk acceptance.

## Ordering

```text
Guide
  ↓
Guard
  ↓
Execute
  ↓
Sensor
  ↓
Check
  ↓
Eval
  ↓
Human Gate if required
```
