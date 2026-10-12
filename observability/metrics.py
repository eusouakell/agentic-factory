from __future__ import annotations

import json
import statistics
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Iterable


def parse_ts(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def load_events(paths: Iterable[Path]) -> list[dict]:
    events: list[dict] = []
    for path in paths:
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                events.append(json.loads(line))
    return sorted(events, key=lambda e: e["timestamp"])


def _seconds(start: str, end: str) -> float:
    return max(0.0, (parse_ts(end) - parse_ts(start)).total_seconds())


def summarize_run(events: list[dict]) -> dict:
    if not events:
        return {}

    events = sorted(events, key=lambda e: e["timestamp"])
    first = events[0]
    run_id = first["run_id"]

    workflow_created = next((e for e in events if e["event_type"] == "workflow_created"), first)
    workflow_completed = next(
        (e for e in reversed(events) if e["event_type"] == "workflow_completed"),
        None,
    )
    cycle_seconds = (
        _seconds(workflow_created["timestamp"], workflow_completed["timestamp"])
        if workflow_completed
        else _seconds(workflow_created["timestamp"], events[-1]["timestamp"])
    )

    task_starts: dict[tuple[str, int], dict] = {}
    active_seconds = 0.0
    rework_seconds = 0.0
    attempts_by_task: Counter[str] = Counter()

    for event in events:
        if event["event_type"] == "task_started":
            attempt = int(event.get("metadata", {}).get("attempt", 1))
            key = (event.get("task_id"), attempt)
            task_starts[key] = event
            attempts_by_task[event.get("task_id")] = max(attempts_by_task[event.get("task_id")], attempt)
        elif event["event_type"] in {"task_completed", "task_failed"}:
            attempt = int(event.get("metadata", {}).get("attempt", 1))
            key = (event.get("task_id"), attempt)
            start = task_starts.get(key)
            if start:
                elapsed = _seconds(start["timestamp"], event["timestamp"])
                active_seconds += elapsed
                if attempt > 1:
                    rework_seconds += elapsed

    open_gates: dict[str, str] = {}
    human_wait_seconds = 0.0
    for event in events:
        metadata = event.get("metadata", {})
        if event["event_type"] == "human_gate_opened":
            open_gates[metadata.get("gate_id", "unknown")] = event["timestamp"]
        elif event["event_type"] == "human_gate_resolved":
            gate_id = metadata.get("gate_id", "unknown")
            if gate_id in open_gates:
                human_wait_seconds += _seconds(open_gates.pop(gate_id), event["timestamp"])

    planned: dict[str, dict] = {}
    current_points: dict[str, int] = {}
    unplanned_points = 0
    for event in events:
        metadata = event.get("metadata", {})
        task_id = event.get("task_id")
        if event["event_type"] == "task_planned":
            planned[task_id] = {
                "baseline_points": int(metadata.get("baseline_points", metadata.get("sizing_points", 0))),
                "planning_origin": "planned",
            }
            current_points[task_id] = int(metadata.get("sizing_points", 0))
        elif event["event_type"] == "task_added_unplanned":
            points = int(metadata.get("sizing_points", 0))
            planned[task_id] = {"baseline_points": 0, "planning_origin": "unplanned"}
            current_points[task_id] = points
            unplanned_points += points
        elif event["event_type"] == "task_resized" and task_id:
            current_points[task_id] = int(metadata.get("to_points", current_points.get(task_id, 0)))

    committed_points = sum(
        item["baseline_points"]
        for item in planned.values()
        if item["planning_origin"] == "planned"
    )
    accepted_tasks = {
        e.get("task_id") for e in events if e["event_type"] == "artifact_accepted"
    }
    accepted_planned_points = sum(
        item["baseline_points"]
        for task_id, item in planned.items()
        if item["planning_origin"] == "planned" and task_id in accepted_tasks
    )
    remaining_planned_points = max(0, committed_points - accepted_planned_points)
    spillover_points = remaining_planned_points if workflow_completed else 0
    scope_growth_delta = sum(
        max(0, current_points.get(task_id, item["baseline_points"]) - item["baseline_points"])
        for task_id, item in planned.items()
        if item["planning_origin"] == "planned"
    )

    usage = {"input_tokens": 0, "output_tokens": 0, "cached_tokens": 0, "total_tokens": 0}
    usage_qualities: set[str] = set()
    for event in events:
        if event["event_type"] != "usage_recorded":
            continue
        metadata = event.get("metadata", {})
        usage_qualities.add(metadata.get("usage_quality", "unavailable"))
        for key in usage:
            value = metadata.get(key)
            if isinstance(value, int):
                usage[key] += value

    if not usage_qualities or usage_qualities == {"unavailable"}:
        usage_quality = "unavailable"
    elif usage_qualities == {"exact"}:
        usage_quality = "exact"
    else:
        usage_quality = "mixed_or_estimated"

    retries = sum(1 for e in events if e["event_type"] == "task_retried")
    quality_failures = [
        e for e in events if e["event_type"] == "quality_gate_failed"
    ]
    failed_checks = Counter(
        e.get("metadata", {}).get("check_id")
        for e in events
        if e["event_type"] == "quality_check_recorded"
        and e.get("metadata", {}).get("status") in {"fail", "unknown"}
    )

    material_issues_created = sum(
        1
        for e in events
        if e["event_type"] == "convergence_issue_created"
        and e.get("metadata", {}).get("severity") in {"major", "blocker"}
    )
    material_issues_resolved = sum(
        1
        for e in events
        if e["event_type"] == "convergence_issue_resolved"
        and e.get("metadata", {}).get("severity") in {"major", "blocker"}
    )
    human_escalations = sum(1 for e in events if e["event_type"] == "human_escalation_opened")
    human_gates = sum(1 for e in events if e["event_type"] == "human_gate_opened")
    human_interventions = human_escalations + human_gates

    agent_execution_started = [
        e for e in events if e["event_type"] == "agent_execution_started"
    ]
    agent_execution_completed = [
        e for e in events if e["event_type"] == "agent_execution_completed"
    ]
    agent_execution_failed = [
        e for e in events if e["event_type"] == "agent_execution_failed"
    ]
    execution_ids = {
        str(e.get("metadata", {}).get("execution_id"))
        for e in agent_execution_started + agent_execution_completed + agent_execution_failed
        if e.get("metadata", {}).get("execution_id")
    }
    agent_execution_ms = sum(
        int(e.get("metadata", {}).get("duration_ms", 0) or 0)
        for e in agent_execution_completed + agent_execution_failed
    )
    escaped_defects = sum(
        1 for e in events if e["event_type"] == "escaped_defect_recorded"
    )

    internal_resolution_rate = (
        material_issues_resolved / material_issues_created
        if material_issues_created
        else 1.0
    )

    deviations = []
    for event in events:
        metadata = event.get("metadata", {})
        et = event["event_type"]
        if et == "task_added_unplanned":
            deviations.append({
                "type": "unplanned",
                "task_id": event.get("task_id"),
                "points": metadata.get("sizing_points", 0),
                "detail": "Added after planning baseline",
            })
        elif et == "task_resized" and metadata.get("delta_points", 0) > 0:
            deviations.append({
                "type": "resized",
                "task_id": event.get("task_id"),
                "points": metadata.get("delta_points", 0),
                "detail": metadata.get("reason", "Scope grew"),
            })
        elif et == "task_retried":
            deviations.append({
                "type": "retry",
                "task_id": event.get("task_id"),
                "points": current_points.get(event.get("task_id"), 0),
                "detail": metadata.get("reason", "Task retried"),
            })
        elif et == "quality_gate_failed":
            deviations.append({
                "type": "quality",
                "task_id": event.get("task_id"),
                "points": 0,
                "detail": f"Quality gate failed: {metadata.get('gate_id', 'unknown')}",
            })

    if workflow_completed:
        for task_id, item in planned.items():
            if item["planning_origin"] == "planned" and task_id not in accepted_tasks:
                deviations.append({
                    "type": "spillover",
                    "task_id": task_id,
                    "points": item["baseline_points"],
                    "detail": "Committed work not accepted by workflow close",
                })

    outcome_status = (
        workflow_completed.get("metadata", {}).get("outcome_status")
        if workflow_completed
        else "in_progress"
    )

    return {
        "run_id": run_id,
        "workflow_id": first["workflow_id"],
        "project_id": first["project_id"],
        "repository": first["repository"],
        "workflow_type": first["workflow_type"],
        "outcome_status": outcome_status,
        "cycle_seconds": round(cycle_seconds, 3),
        "active_seconds": round(active_seconds, 3),
        "human_wait_seconds": round(human_wait_seconds, 3),
        "flow_efficiency": round(active_seconds / cycle_seconds, 4) if cycle_seconds else 0.0,
        "rework_seconds": round(rework_seconds, 3),
        "rework_ratio": round(rework_seconds / active_seconds, 4) if active_seconds else 0.0,
        "retries": retries,
        "committed_points": committed_points,
        "accepted_planned_points": accepted_planned_points,
        "baseline_attainment": round(accepted_planned_points / committed_points, 4) if committed_points else 0.0,
        "unplanned_points": unplanned_points,
        "remaining_planned_points": remaining_planned_points,
        "spillover_points": spillover_points,
        "scope_growth_delta": scope_growth_delta,
        "usage": usage,
        "usage_quality": usage_quality,
        "quality_gate_failures": len(quality_failures),
        "failed_checks": dict(failed_checks),
        "convergence_issues": material_issues_created,
        "convergence_resolved": material_issues_resolved,
        "internal_resolution_rate": round(internal_resolution_rate, 4),
        "human_escalations": human_escalations,
        "human_gates": human_gates,
        "human_interventions": human_interventions,
        "agent_executions_started": len(agent_execution_started),
        "agent_executions_completed": len(agent_execution_completed),
        "agent_executions_failed": len(agent_execution_failed),
        "independent_execution_ids": len(execution_ids),
        "agent_execution_seconds": round(agent_execution_ms / 1000.0, 3),
        "escaped_defects": escaped_defects,
        "deviations": deviations,
    }


def summarize_portfolio(events: list[dict]) -> dict:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for event in events:
        grouped[event["run_id"]].append(event)

    runs = [summarize_run(run_events) for run_events in grouped.values()]
    runs = [run for run in runs if run]

    def med(field: str) -> float:
        values = [float(run[field]) for run in runs if run.get(field) is not None]
        return round(statistics.median(values), 3) if values else 0.0

    total_committed = sum(run["committed_points"] for run in runs)
    total_accepted = sum(run["accepted_planned_points"] for run in runs)
    total_unplanned = sum(run["unplanned_points"] for run in runs)
    total_remaining = sum(run["remaining_planned_points"] for run in runs)
    total_spillover = sum(run["spillover_points"] for run in runs)

    failure_counter: Counter[str] = Counter()
    for run in runs:
        failure_counter.update(run["failed_checks"])

    opportunities = derive_opportunities(runs, failure_counter)

    return {
        "runs": runs,
        "summary": {
            "workflow_count": len(runs),
            "accepted_outcomes": sum(run["outcome_status"] == "accepted" for run in runs),
            "committed_points": total_committed,
            "accepted_planned_points": total_accepted,
            "baseline_attainment": round(total_accepted / total_committed, 4) if total_committed else 0.0,
            "unplanned_points": total_unplanned,
            "remaining_planned_points": total_remaining,
            "spillover_points": total_spillover,
            "median_cycle_seconds": med("cycle_seconds"),
            "median_active_seconds": med("active_seconds"),
            "median_human_wait_seconds": med("human_wait_seconds"),
            "median_rework_ratio": med("rework_ratio"),
            "total_tokens_observed": sum(run["usage"]["total_tokens"] for run in runs),
            "convergence_issues": sum(run["convergence_issues"] for run in runs),
            "convergence_resolved": sum(run["convergence_resolved"] for run in runs),
            "human_escalations": sum(run["human_escalations"] for run in runs),
            "human_interventions": sum(run["human_interventions"] for run in runs),
            "agent_executions_started": sum(run["agent_executions_started"] for run in runs),
            "agent_executions_completed": sum(run["agent_executions_completed"] for run in runs),
            "agent_executions_failed": sum(run["agent_executions_failed"] for run in runs),
            "independent_execution_ids": sum(run["independent_execution_ids"] for run in runs),
            "agent_execution_seconds": round(
                sum(run["agent_execution_seconds"] for run in runs), 3
            ),
            "escaped_defects": sum(run["escaped_defects"] for run in runs),
            "internal_resolution_rate": round(
                (
                    sum(run["convergence_resolved"] for run in runs)
                    / sum(run["convergence_issues"] for run in runs)
                )
                if sum(run["convergence_issues"] for run in runs)
                else 1.0,
                4,
            ),
        },
        "failed_checks": dict(failure_counter),
        "opportunities": opportunities,
        "deviations": [
            {**item, "project_id": run["project_id"], "repository": run["repository"], "run_id": run["run_id"]}
            for run in runs
            for item in run["deviations"]
        ],
    }


def derive_opportunities(runs: list[dict], failed_checks: Counter[str]) -> list[dict]:
    if not runs:
        return []

    opportunities: list[dict] = []
    total_points = sum(run["committed_points"] + run["unplanned_points"] for run in runs)
    unplanned = sum(run["unplanned_points"] for run in runs)
    spillover = sum(run["spillover_points"] for run in runs)
    cycle = sum(run["cycle_seconds"] for run in runs)
    wait = sum(run["human_wait_seconds"] for run in runs)
    retries = sum(run["retries"] for run in runs)
    convergence_issues = sum(run["convergence_issues"] for run in runs)
    convergence_resolved = sum(run["convergence_resolved"] for run in runs)
    human_escalations = sum(run["human_escalations"] for run in runs)
    escaped_defects = sum(run.get("escaped_defects", 0) for run in runs)

    if total_points and unplanned / total_points >= 0.25:
        opportunities.append({
            "signal": "High unplanned-work ratio",
            "hypothesis": "Intake or planning may be incomplete before execution begins.",
            "recommended_intervention": "Tighten intake/PRD completeness and record scope additions explicitly.",
            "metric": "unplanned-work ratio",
            "confidence": "medium",
        })
    if sum(run["committed_points"] for run in runs) and spillover > 0:
        opportunities.append({
            "signal": "Committed points spilled beyond target",
            "hypothesis": "Capacity, dependencies or sizing may be miscalibrated.",
            "recommended_intervention": "Inspect spillover tasks by point bucket and blocker/retry history.",
            "metric": "spillover points",
            "confidence": "medium",
        })
    if cycle and wait / cycle >= 0.4:
        opportunities.append({
            "signal": "Human-wait share is high",
            "hypothesis": "Human gates may be too frequent or positioned too early.",
            "recommended_intervention": "Consolidate low-risk reviews behind meaningful decision gates.",
            "metric": "human-wait ratio",
            "confidence": "medium",
        })
    if retries:
        opportunities.append({
            "signal": "Retry/revision loops detected",
            "hypothesis": "Upstream acceptance criteria or handoffs may be underspecified.",
            "recommended_intervention": "Trace retries to the earliest failed quality criterion and owning role.",
            "metric": "retry rate / rework ratio",
            "confidence": "medium",
        })
    if convergence_issues and convergence_resolved / convergence_issues < 0.8:
        opportunities.append({
            "signal": "Internal resolution rate is below 80%",
            "hypothesis": "The workflow may be escalating or abandoning specialist disagreements too early.",
            "recommended_intervention": "Inspect unresolved issue classes, owner routing and arbitration budgets before adding human gates.",
            "metric": "internal-resolution rate",
            "confidence": "medium",
        })
    if human_escalations:
        opportunities.append({
            "signal": f"Human escalations detected ({human_escalations})",
            "hypothesis": "Some questions exceeded declared internal authority, evidence or revision budgets.",
            "recommended_intervention": "Classify escalation reasons and decide whether authority/context should move upstream.",
            "metric": "human escalation rate",
            "confidence": "medium",
        })
    if escaped_defects:
        opportunities.append({
            "signal": f"Escaped defects detected ({escaped_defects})",
            "hypothesis": "A final human gate or later stage found a material defect that upstream quality evidence missed.",
            "recommended_intervention": "Trace each escaped defect to the owning upstream criterion and strengthen that gate before rerunning the pilot.",
            "metric": "escaped defect count",
            "confidence": "high",
        })
    if failed_checks:
        check_id, count = failed_checks.most_common(1)[0]
        opportunities.append({
            "signal": f"Recurring quality failure: {check_id} ({count}x)",
            "hypothesis": "A repeatable quality weakness may exist upstream of the gate.",
            "recommended_intervention": "Move the criterion earlier or strengthen the owning specialist handoff.",
            "metric": "first-pass quality-gate pass rate",
            "confidence": "high" if count >= 3 else "medium",
        })

    return opportunities
