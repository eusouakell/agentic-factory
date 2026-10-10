from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable
from uuid import uuid4


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class JsonlEventLog:
    def __init__(self, path: Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, event: dict) -> None:
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")


@dataclass
class TaskState:
    task_id: str
    agent_id: str
    sizing_points: int
    planning_origin: str
    retry_budget: int
    depends_on: tuple[str, ...]
    attempts: int = 0
    state: str = "queued"


class WorkflowRuntime:
    def __init__(
        self,
        workflow: dict,
        event_log: JsonlEventLog,
        *,
        execution_surface: str = "codex",
        clock: Callable[[], str] = utc_now,
    ):
        self.workflow = workflow
        self.event_log = event_log
        self.execution_surface = execution_surface
        self.clock = clock
        self.run_id = f"run_{uuid4().hex[:12]}"
        self.states = {
            raw["task_id"]: TaskState(
                task_id=raw["task_id"],
                agent_id=raw["agent_id"],
                sizing_points=int(raw.get("sizing_points", 0)),
                planning_origin=raw.get("planning_origin", "planned"),
                retry_budget=int(raw.get("retry_budget", 0)),
                depends_on=tuple(raw.get("depends_on", [])),
            )
            for raw in workflow.get("tasks", [])
        }

    @property
    def workflow_id(self) -> str:
        return self.workflow["workflow_id"]

    def _emit(
        self,
        event_type: str,
        *,
        task_id: str | None = None,
        agent_id: str | None = None,
        metadata: dict | None = None,
        artifact_refs: list[str] | None = None,
    ) -> dict:
        event = {
            "event_id": f"evt_{uuid4().hex[:12]}",
            "workflow_id": self.workflow_id,
            "project_id": self.workflow["project_id"],
            "repository": self.workflow["repository"],
            "workflow_type": self.workflow["workflow_type"],
            "run_id": self.run_id,
            "task_id": task_id,
            "agent_id": agent_id,
            "event_type": event_type,
            "timestamp": self.clock(),
            "execution_surface": self.execution_surface,
            "artifact_refs": artifact_refs or [],
            "metadata": metadata or {},
        }
        self.event_log.append(event)
        return event

    def create(self) -> None:
        committed = sum(
            state.sizing_points
            for state in self.states.values()
            if state.planning_origin == "planned"
        )
        self._emit("workflow_created", metadata={"target_period": self.workflow.get("target_period")})
        self._emit("planning_baseline_created", metadata={"committed_points": committed})
        for state in self.states.values():
            event_type = "task_planned" if state.planning_origin == "planned" else "task_added_unplanned"
            self._emit(
                event_type,
                task_id=state.task_id,
                agent_id=state.agent_id,
                metadata={
                    "sizing_points": state.sizing_points,
                    "baseline_points": state.sizing_points if state.planning_origin == "planned" else 0,
                    "planning_origin": state.planning_origin,
                    "depends_on": list(state.depends_on),
                },
            )

    def ready_tasks(self) -> list[str]:
        completed = {task_id for task_id, state in self.states.items() if state.state == "completed"}
        ready = []
        for task_id, state in self.states.items():
            if state.state not in {"queued", "ready"}:
                continue
            if all(dep in completed for dep in state.depends_on):
                state.state = "ready"
                ready.append(task_id)
        return ready

    def start_task(self, task_id: str) -> None:
        state = self.states[task_id]
        if task_id not in self.ready_tasks() and state.state != "ready":
            raise ValueError(f"task {task_id} is not ready")
        state.attempts += 1
        if state.attempts > state.retry_budget + 1:
            raise RuntimeError(f"retry budget exceeded for {task_id}")
        state.state = "running"
        self._emit(
            "task_started",
            task_id=task_id,
            agent_id=state.agent_id,
            metadata={
                "attempt": state.attempts,
                "sizing_points": state.sizing_points,
                "planning_origin": state.planning_origin,
            },
        )

    def complete_task(self, task_id: str, artifact_refs: list[str] | None = None) -> None:
        state = self.states[task_id]
        if state.state != "running":
            raise ValueError(f"task {task_id} is not running")
        state.state = "completed"
        self._emit(
            "task_completed",
            task_id=task_id,
            agent_id=state.agent_id,
            artifact_refs=artifact_refs,
            metadata={
                "attempt": state.attempts,
                "sizing_points": state.sizing_points,
                "planning_origin": state.planning_origin,
            },
        )

    def retry_task(self, task_id: str, reason: str) -> None:
        state = self.states[task_id]
        if state.attempts >= state.retry_budget + 1:
            raise RuntimeError(f"retry budget exceeded for {task_id}")
        state.state = "ready"
        self._emit(
            "task_retried",
            task_id=task_id,
            agent_id=state.agent_id,
            metadata={"attempt": state.attempts, "reason": reason},
        )

    def resize_task(self, task_id: str, new_points: int, reason: str) -> None:
        state = self.states[task_id]
        old_points = state.sizing_points
        state.sizing_points = int(new_points)
        self._emit(
            "task_resized",
            task_id=task_id,
            agent_id=state.agent_id,
            metadata={
                "from_points": old_points,
                "to_points": state.sizing_points,
                "delta_points": state.sizing_points - old_points,
                "reason": reason,
            },
        )

    def open_human_gate(self, gate_id: str) -> None:
        self._emit("human_gate_opened", metadata={"gate_id": gate_id})

    def resolve_human_gate(self, gate_id: str, decision: str) -> None:
        self._emit("human_gate_resolved", metadata={"gate_id": gate_id, "decision": decision})

    def record_usage(
        self,
        task_id: str,
        *,
        input_tokens: int | None = None,
        output_tokens: int | None = None,
        cached_tokens: int | None = None,
        total_tokens: int | None = None,
        usage_quality: str = "unavailable",
        source: str = "execution_surface_report",
    ) -> None:
        if usage_quality not in {"exact", "estimated", "unavailable"}:
            raise ValueError("usage_quality must be exact, estimated or unavailable")
        state = self.states[task_id]
        self._emit(
            "usage_recorded",
            task_id=task_id,
            agent_id=state.agent_id,
            metadata={
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "cached_tokens": cached_tokens,
                "total_tokens": total_tokens,
                "usage_quality": usage_quality,
                "source": source,
            },
        )

    def record_quality_gate(
        self,
        gate_id: str,
        *,
        passed: bool,
        results: dict[str, dict],
        overridden: bool = False,
        override_reason: str | None = None,
    ) -> None:
        self._emit("quality_gate_opened", metadata={"gate_id": gate_id})
        for check_id, record in results.items():
            self._emit(
                "quality_check_recorded",
                metadata={"gate_id": gate_id, "check_id": check_id, **record},
            )
        event_type = "quality_gate_overridden" if overridden else (
            "quality_gate_passed" if passed else "quality_gate_failed"
        )
        self._emit(
            event_type,
            metadata={
                "gate_id": gate_id,
                "override_reason": override_reason,
            },
        )

    def accept_artifact(self, task_id: str, artifact_ref: str) -> None:
        state = self.states[task_id]
        self._emit(
            "artifact_accepted",
            task_id=task_id,
            agent_id=state.agent_id,
            artifact_refs=[artifact_ref],
            metadata={
                "sizing_points": state.sizing_points,
                "planning_origin": state.planning_origin,
                "attempt": state.attempts,
            },
        )

    def complete_workflow(self, outcome_status: str = "accepted") -> None:
        self._emit("workflow_completed", metadata={"outcome_status": outcome_status})
