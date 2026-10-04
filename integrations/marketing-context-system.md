# Marketing Context System integration

Repository: `eusouakell/marketing-context-system`

## Responsibility

Marketing Context System remains the executable reference implementation for:

- context cataloging;
- authority/relevance selection;
- required-domain routing;
- context budgets;
- manifests;
- context-specific sensors/checks;
- context ablation experiments.

It is a **consumer/implementation** of the generic Agentic Factory control model.

## Mapping

```text
Factory concept         Marketing Context System
Guide                   task spec / context bundle / domain description
Guard                   source eligibility / authority / scope / budget
Sensor                  routing manifest / include-exclude reasons / size
Check                   required-domain / budget / router assertions
Eval                    context/brand semantic evaluation
Human Gate              consequential strategic/publication approval
```

## Boundary

The Factory owns the canonical agent registry and generic authority model.

Marketing Context System owns context-routing code and context-specific mechanisms.

Do not duplicate active agent contracts in this repository after migration is complete.
