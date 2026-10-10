# PRD — Agentic Factory Orchestration & Observability V1

**Status:** proposal  
**Owner:** Kell  
**Repository:** `eusouakell/agentic-factory`  
**Primary goal:** reduce human orchestration overhead and make agent productivity measurable across the GitHub portfolio before increasing autonomy.

## 1. Problem

The Factory already has:

- registered specialist agents with explicit contracts;
- a control-plane model;
- run-envelope identity;
- deterministic A1 event routing through `automations/route.py`;
- human gates and retry policies.

What it does **not** yet have is an operational A2 layer that:

1. executes a multi-agent route as an inspectable workflow;
2. persists task/run state and handoffs;
3. distinguishes active work from waiting-for-human time;
4. captures model/tool usage when execution surfaces expose it;
5. shows rework and retry loops;
6. exposes the whole flow in a simple visualizer.

As a result, the human owner is still acting as the practical control plane: carrying context between agents, deciding who acts next, requesting another iteration, and manually reconstructing where time was spent.

The current Bússola public-case redesign is the motivating real task. Multiple visual iterations were produced before a sufficiently coherent upstream PRD/art-direction packet existed. This is useful negative evidence: agent specialization without orchestration can distribute rework rather than reduce it.

## 2. Product thesis

The Factory should optimize for **accepted outcome per unit of human attention**, not number of agent calls.

V1 should answer, across the portfolio and for every workflow:

- What is being worked on now?
- Which agent owns the current step?
- What authoritative context did it receive?
- How long did active execution take?
- How long did the flow wait on a human gate?
- How many retries/revisions occurred?
- How many tokens were consumed, when measurable?
- Which artifact was accepted?
- Where did the flow return upstream?
- Did automation reduce or increase human handling?
- Which projects/repositories/workflow types concentrate the most rework, waiting and failed first passes?

## 3. Non-goals

V1 is **not**:

- a general project-management suite;
- a replacement for GitHub issues/PRs;
- a new autonomous “Orchestrator Agent”;
- an LLM deciding its own authority or next tools;
- a real-time billing platform;
- a mandate to expose chain-of-thought;
- an excuse to add every possible metric before learning from real runs.

The control plane remains infrastructure. Specialist authority continues to come from agent contracts and human-approved governance.

## 4. Design principles

### 4.1 Outcome first
A workflow begins from one concrete outcome and acceptance criteria, not from a list of agents.

### 4.2 One source of truth per decision
Approved upstream artifacts are passed forward. Downstream agents do not regenerate the same decision unless an explicit revision edge returns work upstream.

### 4.3 Human-gate compression
Do not ask Kell to approve every specialist handoff. Group low-risk specialist work behind one meaningful gate whenever authority permits.

### 4.4 Bounded retries
Every step has an explicit retry budget. A repeated failure returns to the correct upstream owner instead of adding more effects or more agents.

### 4.5 Static quality before motion
For visual work, the composition must pass without motion. Motion is a downstream enhancement with its own trigger.

### 4.6 Observability is part of the workflow contract
State, timestamps, attempts, handoffs and artifact refs are required run evidence, not optional debugging notes.

### 4.7 Measurement quality is explicit
Exact token usage is captured only when the execution surface exposes it. Estimated or unavailable usage must be labelled as such rather than fabricated.

### 4.8 Quality gates are first-class workflow state
Quality checklists are part of workflow execution, not a final administrative step.

The Factory uses three distinct classes:
- deterministic checks;
- semantic evaluations;
- human decisions.

A blocker check in `fail` or required `unknown` prevents a gate transition unless an authorized human explicitly overrides it with recorded residual risk.

Quality-gate events feed the same portfolio-level observability stream so recurring failures can be analyzed by project, repository, workflow type, agent and stage.

Canonical V1 contract: `docs/orchestration/quality-gates-v1.md`.

### 4.9 Plan vs. actual is first-class
Execution telemetry is not enough to diagnose productivity. The Factory must preserve a planning baseline so actual work can be compared with what was expected before execution started.

Tasks may carry a **relative sizing value in points**, following agile/IT sizing logic. Points represent relative complexity/effort/risk; they are not hours and must not be automatically converted into time.

For every planning period or committed workflow slice, preserve:

- baseline task set;
- baseline points;
- planned/unplanned origin;
- date added to the plan;
- scope/size changes after baseline;
- current state and accepted outcome.

This enables the system to distinguish:
- execution that followed the plan;
- work added after the plan;
- work that spilled over;
- tasks that grew materially after discovery;
- rework caused by failed quality gates or revision loops.

### 4.10 Portfolio-first observability
Observability is a Factory capability, not a feature scoped to Bússola or to one repository.

The default analytical scope is **all instrumented workflows**. Project, repository, workflow type, agent, execution surface, state and time window are filters over the same event model.

A project is not assumed to equal a repository:

- one project may span several repositories;
- one repository may contain several projects/workstreams;
- internal Factory work is observable under the same model.

This separation is required so the system can reveal whether a recurring problem belongs to a specific project, repository, workflow type, agent boundary or operating pattern.

## 5. V1 workflow model

A workflow is a directed acyclic graph of **tasks**.

Every workflow also binds portfolio dimensions:

- `project_id` — stable analytical project/workstream identifier;
- `repository` — GitHub `owner/name` where the primary work is happening;
- `workflow_type` — reusable class such as `web_design`, `editorial`, `agent_governance`, `frontend_change`;
- optional `related_repositories` — other repositories materially involved in the same workflow.

`project_id` is an analytical dimension, not a storage boundary. Runs from all projects feed the same observability layer.

A task binds:

- `sizing_points` — relative sizing value such as 1, 2, 3, 5, 8;
- `planning_origin` — `planned | unplanned`;
- `baseline_points` — original committed size when present;
- `planned_at` — timestamp or planning-period reference;
- optional `due_or_target_period`;
- optional `scope_change_reason`;

- `task_id`;
- `run_id`;
- `agent_id`;
- `agent_contract_ref`;
- trigger;
- required inputs;
- authoritative context refs;
- allowed tools/write authority;
- expected output artifact;
- acceptance criteria;
- retry budget;
- next edge(s);
- human gate, when required.

Minimum task states:

`queued → ready → running → review → completed`

Interruption/terminal alternatives:

- `waiting_human`;
- `blocked`;
- `failed`;
- `escalated`;
- `cancelled`.

A workflow has one explicit `outcome_status`:

- `accepted`;
- `needs_work`;
- `blocked`;
- `cancelled`.

## 6. Telemetry event model

Use an append-only event log as the V1 system of record.

Recommended path:

`runs/events/YYYY-MM-DD.jsonl`

Each event should contain:

```json
{
  "event_id": "evt_...",
  "workflow_id": "wf_...",
  "project_id": "bussola-public-case",
  "repository": "eusouakell/bussola",
  "workflow_type": "web_design",
  "run_id": "run_...",
  "task_id": "task_...",
  "agent_id": "editorial-art-director",
  "event_type": "task_started",
  "timestamp": "ISO-8601",
  "execution_surface": "codex",
  "artifact_refs": [],
  "metadata": {}
}
```

Portfolio dimensions (`project_id`, `repository`, `workflow_type`) should be copied onto every event or resolved deterministically from immutable workflow metadata so aggregations do not need repository-specific joins.

Maintain a small registry such as `observability/projects.json` for human-readable project names, optional repository membership and lifecycle metadata. The registry organizes filters; it does not own workflow state.

Required event types:

- `planning_baseline_created`
- `task_planned`
- `task_added_unplanned`
- `task_resized`
- `task_scope_changed`
- `workflow_created`
- `task_queued`
- `task_started`
- `task_completed`
- `task_failed`
- `task_retried`
- `handoff_created`
- `human_gate_opened`
- `human_gate_resolved`
- `artifact_created`
- `artifact_accepted`
- `quality_gate_opened`
- `quality_check_recorded`
- `quality_gate_passed`
- `quality_gate_failed`
- `quality_gate_overridden`
- `workflow_completed`

Optional usage event:

- `usage_recorded`

Usage payload:

```json
{
  "input_tokens": 0,
  "output_tokens": 0,
  "cached_tokens": 0,
  "total_tokens": 0,
  "usage_quality": "exact | estimated | unavailable",
  "source": "execution_surface_report"
}
```

No field should be populated with a synthetic estimate unless `usage_quality=estimated` and the estimation method is recorded.

## 7. Derived metrics

V1 visualizes metrics that can change operating behavior.

Every metric must be aggregatable at portfolio level and sliceable by:

- project;
- repository;
- workflow type;
- agent;
- execution surface;
- outcome status;
- time window.

### Planning / predictability

- **committed points:** sum of baseline points at planning lock;
- **accepted planned points:** committed points completed and accepted in the target period;
- **baseline attainment:** accepted planned points / committed points;
- **unplanned points:** points introduced after planning lock;
- **unplanned-work ratio:** unplanned points / total points entering execution in the period;
- **spillover points:** committed points not accepted by the end of the target period;
- **scope-growth delta:** current points minus baseline points for resized work;
- **throughput:** accepted points per period;
- **WIP by points:** relative load currently running/review/waiting;
- **cycle time by point bucket:** actual duration grouped by relative size, without converting points into hours.

Keep both the original baseline and current scope. Do not rewrite history when a task is resized or descoped.

### Flow efficiency

- **cycle time:** workflow created → accepted/cancelled;
- **active execution time:** sum of task running intervals;
- **human wait time:** sum of open human-gate intervals;
- **flow efficiency:** active execution / cycle time;
- **handoff count:** number of agent-to-agent transitions.

### Rework

- **revision loops:** number of edges returning to an upstream task;
- **retry rate:** retried tasks / started tasks;
- **first-pass acceptance:** artifacts accepted without revision / artifacts submitted for gate;
- **rework ratio:** repeated task execution time / total active execution time.

### Model/tool consumption

When available:

- input/output/total tokens by task;
- tokens by accepted artifact;
- tokens discarded in rejected/reworked artifacts;
- tool-call count and failure count;
- model/execution-surface breakdown.

### Quality

- first-pass quality-gate pass rate;
- most frequently failed checks;
- blocker recurrence;
- quality failure → upstream owner distribution;
- gate override count;
- escaped defects found in a later stage;
- quality-failure correlation with rework;
- quality-failure correlation with scope growth/spillover.

Do not collapse these into one opaque quality score in V1.

### Human attention

- number of human gates;
- time waiting for Kell;
- number of decisions requested from Kell;
- revision requests initiated by Kell;
- accepted-outcome / human-gate ratio.

V1 must not equate “fewer tokens” with “better work”. The primary operating metric is **accepted outcome with less rework and less human handling**.

## 8. Visualizer V1

Build a repo-native, dependency-light visualizer generated from JSONL events.

### Required views

#### A. Portfolio overview
Default view: all instrumented projects.

Show:

- committed points for the selected period;
- accepted planned points;
- baseline attainment;
- unplanned points / unplanned-work ratio;
- spillover points;
- active workflows;
- accepted outcomes;
- median cycle time;
- median active time;
- median human-wait time;
- first-pass acceptance;
- rework ratio;
- observable token consumption;
- top rework hotspots;
- top plan-deviation hotspots.

Global filters:

- project;
- repository;
- workflow type;
- agent;
- execution surface;
- status/outcome;
- date range.

Project is therefore a **filter**, not a separate dashboard or data silo.

#### B. Plan vs. actual / task ledger

Use a compact operational table inspired by engineering delivery views.

Minimum columns:

- objective/outcome;
- project;
- repository or area;
- task;
- owner/agent;
- sizing points;
- planning origin (`planned | unplanned`);
- target period;
- actual state;
- active time;
- human wait;
- attempts/revisions;
- quality-gate status;
- accepted artifact.

Visually call out:

- work added after planning lock;
- resized work;
- spillover;
- blocked/waiting tasks;
- tasks whose cycle time is anomalous for their point bucket.

This is not a timesheet and does not infer hours from points.

#### C. Current workflow board
Columns:

- Ready
- Running
- Waiting for human
- Review
- Blocked
- Done

Each task card shows:

- agent;
- elapsed active time;
- attempt number;
- current artifact;
- next gate.

#### D. Timeline
A horizontal timeline/Gantt-like view showing:

- active agent spans;
- human-wait spans;
- retries;
- handoffs.

This should make “we spent 8 minutes executing and 3 hours waiting/reworking” immediately visible.

#### E. Efficiency summary
For selected workflow:

- cycle time;
- active time;
- human wait;
- rework time/ratio;
- task count;
- revision loops;
- token usage and quality label;
- accepted artifact.

#### F. Agent comparison
Across completed workflows:

- tasks completed;
- median active time;
- first-pass acceptance;
- retry rate;
- median token use when measurable;
- human revisions triggered.

Do not rank agents by token count alone.

#### G. Quality gates
For the selected workflow or portfolio slice, show:

- current gate;
- pass/fail/unknown status by criterion;
- deterministic vs semantic vs human-owned checks;
- blocker failures;
- evidence refs;
- overrides and residual risk;
- most recurrent failed criteria in the selected period.

#### H. Project / repository comparison
Across the same normalized event stream, compare:

- cycle time;
- first-pass acceptance;
- rework ratio;
- human-wait ratio;
- average gates per accepted outcome;
- observable tokens per accepted outcome;
- dominant failure/revision reason.

The purpose is diagnosis, not a simplistic league table. A high-rework project may indicate poor upstream requirements rather than a weak agent.

#### I. Improvement opportunities

Generate evidence-backed opportunities from recurring telemetry patterns. Each opportunity must include:

- observed signal;
- affected project/repository/workflow/agent/stage;
- sample size/time window;
- likely process cause stated as a hypothesis, not fact;
- recommended intervention;
- expected metric to improve;
- confidence.

Examples:
- repeated mobile-quality failures → strengthen the responsive art-direction gate;
- high human-wait ratio → consolidate or relocate gates;
- high unplanned-work ratio → improve intake/planning completeness;
- repeated scope-growth in 1–2 point tasks → sizing rubric may be underestimating uncertainty;
- high retries after frontend implementation → upstream design/acceptance criteria may be underspecified.

#### J. Work that left the plan

A dedicated exception list should show work that deviated from baseline:

- unplanned tasks;
- spillover tasks;
- resized tasks above a configurable delta;
- reopened/retried tasks;
- tasks blocked beyond a threshold;
- tasks that failed a blocker quality gate;
- tasks cancelled or descoped after commitment.

This is intended for inspection and improvement, not blame.

## 9. Implementation constraints

V1 should be intentionally small:

- append-only JSONL or JSON event storage in-repo/local workspace;
- Python stdlib preferred for aggregation;
- static HTML/CSS/JS dashboard output;
- GitHub Pages as the default portfolio visualization surface;
- no database required;
- no external observability SaaS required;
- no new model dependency;
- exact token capture remains adapter-specific and optional;
- GitHub remains the canonical source for issues, branches, PRs and accepted code/artifacts;
- adapters from multiple GitHub repositories emit into the same normalized event model;
- planning baselines and point sizing use a shared schema across projects;
- no per-project telemetry implementation or dashboard fork.

The visualizer must be runnable locally **and** publishable to GitHub Pages from the `agentic-factory` repository.

Pages is the read surface, not the system of record:

```text
instrumented repositories / execution surfaces
        ↓
normalized portfolio events
        ↓
aggregator + derived metrics
        ↓
static dashboard build
        ↓
GitHub Pages
```

The dashboard must not read private repository data directly in the browser. Any data intended for Pages must already be normalized and safe for publication. Sensitive/raw evidence remains referenced by opaque IDs or repository links according to access policy.

The Pages build should support:

- local preview from the same generated files;
- deployment from `main` only;
- PR build/test without publishing;
- cache-busting/version metadata showing the data/build timestamp;
- no project-specific fork of the site.

## 10. Control-plane changes

### 10.1 Keep current run envelope
Do not break existing `run-envelope.schema.json`.

Add optional runtime telemetry through either:

- an additive `telemetry_ref` field in a future schema revision; or
- event-log correlation by `run_id` in V1.

Prefer the second option first to avoid coupling operational telemetry to identity schema prematurely.

### 10.2 Add workflow specification
Create a machine-readable workflow definition that supports:

- ordered/dependent tasks;
- parallel task groups;
- acceptance gates;
- revision edges;
- retry budgets;
- terminal ownership.

The deterministic router can continue selecting a workflow. A runner then materializes task runs from that workflow.

## 11. Acceptance criteria

V1 is successful when real workflows from multiple GitHub projects can feed the same observability layer and the dashboard can answer:

1. which task is current;
2. which agent owns it;
3. what artifact it produced;
4. active execution duration;
5. human-wait duration;
6. retries/revisions;
7. token usage with an explicit exact/estimated/unavailable label;
8. final accepted artifact;
9. total cycle time;
10. whether a revision returned to the right upstream role;
11. how the same metrics compare across projects/repositories;
12. whether project filtering changes the diagnosis of the productivity bottleneck;
13. what was planned vs unplanned;
14. how many committed points were accepted;
15. which tasks spilled over, grew in scope or required rework;
16. which evidence-backed improvement opportunities should be investigated.

Use the Bússola public-case redesign as the first pilot, but do not call V1 operational until at least one additional GitHub project/repository emits a compatible workflow and appears in the same dashboard without custom code.

## 12. Pilot success thresholds

These are learning thresholds, not permanent SLAs.

For the Bússola pilot:

- no more than **2 human gates** across the full pilot workflow:
  1. direction/PRD gate before implementation;
  2. final release/merge gate after implementation;
- no more than **1 focused revision** per director-level task before escalation;
- no implementation begins before PRD + art-direction packet is accepted;
- no motion task starts before static composition passes;
- every downstream task consumes the approved upstream artifact instead of regenerating it;
- dashboard captures all task transitions and timestamps;
- token usage is shown only where observable.

## 13. Risks

### Telemetry becomes bureaucracy
Mitigation: instrument automatically at runner boundaries; do not ask specialists to write manual timesheets.

### Token metrics distort behavior
Mitigation: keep accepted outcome, rework and human attention as primary metrics.

### Too many agents recreate the same problem
Mitigation: route only capabilities with a distinct decision/output contract.

### Dashboard encourages local optimization
Mitigation: evaluate whole-workflow cycle time and accepted artifact, not agent speed alone.

### Human gate compression hides important decisions
Mitigation: only compress gates where authority contracts permit; consequential brand, publication and merge decisions remain human-owned.

## 14. Next implementation slice

The first implementation slice should contain only:

1. workflow definition schema;
2. append-only run event schema/logger;
3. local runner capable of sequential + parallel dependencies and bounded revision edges;
4. quality checklist/gate schema and deterministic blocker evaluation;
5. static dashboard generator including gate status/failure hotspots;
6. GitHub Pages build/deploy workflow with local-preview parity;
7. project/workflow metadata registry and repository-agnostic ingestion contract;
8. Bússola case workflow definition + quality-gate templates;
9. one second-project validation workflow from another GitHub repository;
10. planning-baseline + point-sizing model;
11. plan-vs-actual and improvement-opportunity dashboard views;
12. tests for state transitions, retry limit, checklist semantics, sizing/baseline history, cross-project filtering and telemetry derivation.

Do **not** add external databases, queues or distributed tracing in V1.

## 15. Human decision

Kell approves:

- the V1 scope;
- telemetry fields;
- dashboard metrics;
- Bússola as the first pilot, with a second GitHub project required for cross-project validation;
- whether the implementation may proceed to a proposal branch.

