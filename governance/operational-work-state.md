# Operational work state

Status: **pilot architecture for cross-repository roadmap execution**.

## Why this exists

Chat conversations, model memory and local execution sessions are useful working context, but they are not durable operational state. A conversation can reach its context limit; a new chat may begin with partial history; an agent may run on another execution surface.

> **Conversation is temporary working context. GitHub is durable operational memory.**

The system externalizes enough state that a human or authorized agent can resume work without replaying a previous chat.

## Layer model

```text
CANONICAL DOCS
truth · policy · durable decisions
        ↓
ISSUES
units of work · outcome · acceptance · dependencies
        ↓
GITHUB PROJECT
current state · priority · ownership · flow
        ↓
PR / ARTIFACT / EVIDENCE
implementation and review evidence
        ↓
GATES
authority to advance consequential transitions
```

- **Docs say what is true.**
- **Issues say what needs to happen.**
- **Projects show the state of work.**
- **Gates determine who may authorize the next transition.**

The Project is an operational index, not a new source of domain truth.

## One cross-repository Project

Use one cross-repository Project for the Cereja Flamejante roadmap while the operating scale remains small. Issues stay in the repository that owns the work; the Project provides one operating surface across them.

Do not create one Project per repository unless scale or permissions create a real need.

## Workflow

```text
BACKLOG
   ↓
READY
   ↓
IN PROGRESS
   ↓
GATE / REVIEW
   ↓
DONE
```

### Backlog

Valid work not yet eligible to start because it is lower priority, intentionally deferred, waiting on a dependency, or missing authority/decision.

### Ready

An issue may enter **Ready** only when:
1. its intended outcome is understandable;
2. required canonical sources are identifiable;
3. no declared blocking dependency remains open;
4. the work is authorized to begin;
5. the next execution step is clear.

Ready means **pullable**, not merely important.

### In Progress

Someone or an authorized execution surface is actively working on the issue. Keep WIP low: default guidance is **1–2 active issues per human/agent responsibility**, unless the work genuinely requires parallelism.

### Gate / Review

Execution produced something, but review, QA, merge or a human decision is required before advancement. A gate represents authority still required.

### Done

Acceptance criteria are satisfied and required evidence/decisions are linked. "Worked on" is not Done.

## Native dependencies

Use GitHub issue dependencies (`blocked by` / `blocking`) as the dependency source of truth when available.

Do not duplicate the same condition in a custom `Blocked` status.

> **An issue with an open blocking dependency is not eligible for Ready.**

When a dependency closes, automation may evaluate dependents:

```text
DEPENDENCY CLOSED
      ↓
CHECK REMAINING BLOCKERS
      ↓
none open?
  ├─ no  → stay Backlog
  └─ yes → check authority + required context
                 ↓
              READY
```

Closing a dependency does not authorize execution if another gate or prerequisite remains.

## Minimal Project fields

| Field | Values / purpose |
|---|---|
| Status | Backlog · Ready · In Progress · Gate / Review · Done |
| Priority | P0 · P1 · P2 |
| Area | Media · Lab · Academy · Studio / Products · System |
| Type | Feature · Research · Content · Governance · Maintenance |
| Owner | accountable human or operational responsibility |

Avoid story points, percent-complete, duplicate blocker fields, speculative dates and health scores unless evidence later shows they solve a real problem.

## Issue as a context-recovery packet

A roadmap issue must contain enough information for a new human or agent session to recover the work without depending on old chat history.

Minimum useful packet:

```text
OUTCOME
What changes when this issue is done?

WHY NOW
Why is this worth doing / why is it sequenced here?

CANONICAL SOURCES
Which durable docs or approved artifacts govern the work?

DEPENDENCIES
What must be true or complete before this can start?

CURRENT STATE
What already happened? Which decisions are closed?

NEXT STEP
What is the next executable action?

ACCEPTANCE
What evidence makes this Done?

GATE
Who/what must approve before consequential advancement?
```

The requirement is **recoverability**, not documentation volume.

## Context recovery protocol

When a new chat, agent run or execution surface resumes existing work:

1. read the relevant Project item/status;
2. read the Issue context packet;
3. load only the canonical sources linked by the issue;
4. load the latest approved artifact/handoff needed for the next action;
5. do not reconstruct authority from remembered conversation fragments;
6. if Project, Issue and canonical source conflict, stop and resolve using source-of-truth precedence.

A conversation may add working detail, but it must not be the sole location of a roadmap decision needed later.

This complements [progressive context loading](context-loading.md): persistent state tells the system **where work stands**; progressive disclosure tells it **what context is eligible for the next step**.

## Human + agent use

For humans, the Project is a simple Kanban surface.

For the control plane, it can become structured work-state input. A future bounded route may ask:

> Which issues are Ready, have no open dependency, and fall within this executor's declared authority?

That query proposes eligible work. It does not grant authority by itself.

Agents and automations must not:
- move work through a human gate merely because prerequisites closed;
- mark Done without acceptance evidence;
- infer missing domain truth from Project metadata;
- create work merely to keep WIP occupied.

## Pilot rule

Validate this model on the real Cereja Flamejante roadmap before expanding it.

Success means a human can return after a context break and quickly answer:
- What is happening now?
- What is Ready?
- What is blocked, and by what?
- What needs a human decision?
- What just became eligible?
- Where is the canonical context?
- What is the next action?

If the board becomes another surface that needs constant manual reconciliation, simplify it before adding automation.
