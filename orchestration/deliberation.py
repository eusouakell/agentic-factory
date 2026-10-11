from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable
from uuid import uuid4

from orchestration.runtime import JsonlEventLog, utc_now


ALLOWED_CLASSES = {
    "factual_source",
    "narrative_content",
    "experience",
    "visual",
    "motion",
    "implementation",
    "accessibility",
    "publication_readiness",
    "authority",
}
ALLOWED_SEVERITIES = {"advisory", "major", "blocker"}
ALLOWED_OWNER_DECISIONS = {"accept", "reject_with_rationale", "authority_conflict"}
ALLOWED_ARBITRATION = {"resolve_owner", "resolve_challenger", "human_escalation"}


@dataclass
class ConvergenceIssue:
    issue_id: str
    stage_id: str
    question: str
    issue_class: str
    raised_by: str
    owner: str
    severity: str
    arbiter: str | None
    root_cause: str
    round_number: int
    same_blocker_attempt: int
    evidence_refs: list[str] = field(default_factory=list)
    proposed_resolution: str | None = None
    owner_decision: str | None = None
    owner_rationale: str | None = None
    artifact_refs: list[str] = field(default_factory=list)
    status: str = "open"


class DeliberationRuntime:
    """Bounded owner → challenger → arbiter convergence state machine.

    This runtime is execution-surface agnostic. It records deliberation state and
    budgets; it does not pretend to isolate model agents by itself.
    """

    def __init__(
        self,
        workflow: dict,
        event_log: JsonlEventLog,
        *,
        run_id: str,
        execution_surface: str = "control-plane",
        clock: Callable[[], str] = utc_now,
    ):
        self.workflow = workflow
        self.event_log = event_log
        self.run_id = run_id
        self.execution_surface = execution_surface
        self.clock = clock
        self.issues: dict[str, ConvergenceIssue] = {}
        self.root_cause_attempts: dict[tuple[str, str], int] = {}

    @property
    def max_stage_rounds(self) -> int:
        explicit = self.workflow.get("max_stage_rounds")
        if explicit is not None:
            return int(explicit)
        rounds = [
            int(phase.get("max_material_rounds", 0))
            for phase in self.workflow.get("phases", [])
            if phase.get("max_material_rounds")
        ]
        return max(rounds, default=3)

    @property
    def max_same_blocker_attempts(self) -> int:
        explicit = self.workflow.get("max_same_blocker_attempts")
        if explicit is not None:
            return int(explicit)
        attempts = [
            int(phase.get("max_revision_cycles_per_root_cause", 0))
            for phase in self.workflow.get("phases", [])
            if phase.get("max_revision_cycles_per_root_cause")
        ]
        return max(attempts, default=2)

    def _emit(self, event_type: str, *, issue: ConvergenceIssue, metadata: dict | None = None) -> dict:
        payload = {
            "event_id": f"evt_{uuid4().hex[:12]}",
            "workflow_id": self.workflow["workflow_id"],
            "project_id": self.workflow["project_id"],
            "repository": self.workflow["repository"],
            "workflow_type": self.workflow["workflow_type"],
            "run_id": self.run_id,
            "task_id": None,
            "agent_id": None,
            "event_type": event_type,
            "timestamp": self.clock(),
            "execution_surface": self.execution_surface,
            "artifact_refs": list(issue.artifact_refs),
            "metadata": {
                "issue_id": issue.issue_id,
                "stage_id": issue.stage_id,
                "issue_class": issue.issue_class,
                "raised_by": issue.raised_by,
                "owner": issue.owner,
                "arbiter": issue.arbiter,
                "severity": issue.severity,
                "root_cause": issue.root_cause,
                "round": issue.round_number,
                "same_blocker_attempt": issue.same_blocker_attempt,
                "status": issue.status,
                **(metadata or {}),
            },
        }
        self.event_log.append(payload)
        return payload

    def create_issue(
        self,
        *,
        issue_id: str,
        stage_id: str,
        question: str,
        issue_class: str,
        raised_by: str,
        owner: str,
        severity: str,
        root_cause: str,
        round_number: int,
        evidence_refs: list[str] | None = None,
        proposed_resolution: str | None = None,
        arbiter: str | None = None,
    ) -> ConvergenceIssue:
        if issue_id in self.issues:
            raise ValueError(f"issue already exists: {issue_id}")
        if issue_class not in ALLOWED_CLASSES:
            raise ValueError(f"invalid issue_class: {issue_class}")
        if severity not in ALLOWED_SEVERITIES:
            raise ValueError(f"invalid severity: {severity}")
        if round_number < 1:
            raise ValueError("round_number must be >= 1")

        key = (stage_id, root_cause)
        attempt = self.root_cause_attempts.get(key, 0) + 1
        self.root_cause_attempts[key] = attempt

        issue = ConvergenceIssue(
            issue_id=issue_id,
            stage_id=stage_id,
            question=question,
            issue_class=issue_class,
            raised_by=raised_by,
            owner=owner,
            severity=severity,
            arbiter=arbiter,
            root_cause=root_cause,
            round_number=round_number,
            same_blocker_attempt=attempt,
            evidence_refs=evidence_refs or [],
            proposed_resolution=proposed_resolution,
        )
        self.issues[issue_id] = issue

        if round_number > self.max_stage_rounds or attempt > self.max_same_blocker_attempts:
            issue.status = "human_escalation"
            self._emit(
                "human_escalation_opened",
                issue=issue,
                metadata={
                    "reason": "revision_budget_exhausted",
                    "question": question,
                    "evidence_refs": issue.evidence_refs,
                },
            )
            return issue

        self._emit(
            "convergence_issue_created",
            issue=issue,
            metadata={
                "question": question,
                "evidence_refs": issue.evidence_refs,
                "proposed_resolution": proposed_resolution,
            },
        )
        return issue

    def owner_respond(
        self,
        issue_id: str,
        *,
        decision: str,
        rationale: str,
        artifact_refs: list[str] | None = None,
    ) -> ConvergenceIssue:
        issue = self.issues[issue_id]
        if issue.status != "open":
            raise ValueError(f"issue {issue_id} is not open")
        if decision not in ALLOWED_OWNER_DECISIONS:
            raise ValueError(f"invalid owner decision: {decision}")
        if not rationale.strip():
            raise ValueError("owner rationale is required")

        issue.owner_decision = decision
        issue.owner_rationale = rationale
        issue.artifact_refs = list(artifact_refs or [])
        if decision == "authority_conflict":
            issue.status = "human_escalation"
            self._emit(
                "human_escalation_opened",
                issue=issue,
                metadata={"reason": "authority_conflict", "rationale": rationale},
            )
            return issue

        issue.status = "re_review"
        self._emit(
            "convergence_issue_owner_responded",
            issue=issue,
            metadata={"decision": decision, "rationale": rationale},
        )
        return issue

    def challenger_rereview(
        self,
        issue_id: str,
        *,
        resolved: bool,
        rationale: str,
    ) -> ConvergenceIssue:
        issue = self.issues[issue_id]
        if issue.status != "re_review":
            raise ValueError(f"issue {issue_id} is not awaiting re-review")
        if not rationale.strip():
            raise ValueError("challenger rationale is required")

        if resolved:
            issue.status = "resolved"
            self._emit(
                "convergence_issue_resolved",
                issue=issue,
                metadata={"resolution": "challenger_accepts", "rationale": rationale},
            )
            return issue

        issue.status = "needs_arbitration"
        self._emit(
            "convergence_issue_arbitration_requested",
            issue=issue,
            metadata={"rationale": rationale},
        )
        return issue

    def arbitrate(
        self,
        issue_id: str,
        *,
        decision: str,
        rationale: str,
        artifact_refs: list[str] | None = None,
    ) -> ConvergenceIssue:
        issue = self.issues[issue_id]
        if issue.status != "needs_arbitration":
            raise ValueError(f"issue {issue_id} is not awaiting arbitration")
        if decision not in ALLOWED_ARBITRATION:
            raise ValueError(f"invalid arbitration decision: {decision}")
        if not issue.arbiter:
            raise ValueError("arbiter is required before arbitration")
        if not rationale.strip():
            raise ValueError("arbitration rationale is required")

        issue.artifact_refs = list(artifact_refs or issue.artifact_refs)
        if decision == "human_escalation":
            issue.status = "human_escalation"
            self._emit(
                "human_escalation_opened",
                issue=issue,
                metadata={"reason": "unresolved_after_arbitration", "rationale": rationale},
            )
            return issue

        issue.status = "resolved"
        self._emit(
            "convergence_issue_arbitrated",
            issue=issue,
            metadata={"decision": decision, "rationale": rationale},
        )
        self._emit(
            "convergence_issue_resolved",
            issue=issue,
            metadata={"resolution": decision, "rationale": rationale},
        )
        return issue

    def open_material_issues(self) -> list[ConvergenceIssue]:
        return [
            issue
            for issue in self.issues.values()
            if issue.severity in {"major", "blocker"}
            and issue.status not in {"resolved", "rejected_with_rationale"}
        ]

    def internal_resolution_rate(self) -> float:
        material = [
            issue
            for issue in self.issues.values()
            if issue.severity in {"major", "blocker"}
        ]
        if not material:
            return 1.0
        internally_resolved = sum(issue.status == "resolved" for issue in material)
        return internally_resolved / len(material)
