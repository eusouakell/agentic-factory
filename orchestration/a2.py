from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import uuid4

from automations.executor import BoundedExecutor, ExecutionAdapter, ExecutionRequest, ExecutionResult
from orchestration.runtime import JsonlEventLog, utc_now


@dataclass(frozen=True)
class SpecialistRun:
    agent_id: str
    execution_id: str
    task_id: str
    result: ExecutionResult


@dataclass(frozen=True)
class CouncilRun:
    reviews: tuple[dict[str, Any], ...]
    execution_run_ids: tuple[str, ...]


@dataclass(frozen=True)
class DeliberationOutcome:
    owner_run: SpecialistRun
    challenger_run: SpecialistRun
    arbiter_run: SpecialistRun
    decision: str
    rationale: str


class A2Orchestrator:
    """Provider-neutral A2 runtime for truly separate specialist executions."""

    def __init__(
        self,
        workflow: dict,
        event_log: JsonlEventLog,
        executor: BoundedExecutor,
        adapter: ExecutionAdapter,
        *,
        execution_surface: str = "a2-control-plane",
        clock=utc_now,
    ):
        self.workflow = workflow
        self.event_log = event_log
        self.executor = executor
        self.adapter = adapter
        self.execution_surface = execution_surface
        self.clock = clock

    @property
    def workflow_id(self) -> str:
        return self.workflow["workflow_id"]

    def _emit(
        self,
        event_type: str,
        *,
        run_id: str,
        task_id: str,
        agent_id: str,
        artifact_refs: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        self.event_log.append(
            {
                "event_id": f"evt_{uuid4().hex[:12]}",
                "workflow_id": self.workflow_id,
                "project_id": self.workflow["project_id"],
                "repository": self.workflow["repository"],
                "workflow_type": self.workflow["workflow_type"],
                "run_id": run_id,
                "task_id": task_id,
                "agent_id": agent_id,
                "event_type": event_type,
                "timestamp": self.clock(),
                "execution_surface": self.execution_surface,
                "artifact_refs": artifact_refs or [],
                "metadata": metadata or {},
            }
        )

    def invoke(
        self,
        *,
        run_id: str,
        task_id: str,
        agent_id: str,
        agent_contract_ref: str,
        output_schema_ref: str,
        context_refs: tuple[str, ...],
        tool_grants: tuple[str, ...] = (),
        retry_budget: int = 0,
        human_gate: str | None = None,
        task_input: dict[str, Any] | None = None,
    ) -> SpecialistRun:
        execution_id = f"exec_{uuid4().hex[:16]}"
        request = ExecutionRequest(
            run_id=run_id,
            repository=self.workflow["repository"],
            task_id=task_id,
            primary_agent=agent_id,
            context_refs=context_refs,
            tool_grants=tool_grants,
            retry_budget=retry_budget,
            human_gate=human_gate,
            agent_contract_ref=agent_contract_ref,
            output_schema_ref=output_schema_ref,
            execution_id=execution_id,
            task_input=task_input or {},
        )

        self._emit(
            "agent_execution_started",
            run_id=run_id,
            task_id=task_id,
            agent_id=agent_id,
            metadata={
                "execution_id": execution_id,
                "agent_contract_ref": agent_contract_ref,
                "output_schema_ref": output_schema_ref,
            },
        )
        result = self.executor.execute(request, self.adapter)
        self._emit(
            "agent_execution_completed" if result.status == "completed" else "agent_execution_failed",
            run_id=run_id,
            task_id=task_id,
            agent_id=agent_id,
            artifact_refs=list(result.artifact_refs),
            metadata={
                "execution_id": result.execution_id,
                "status": result.status,
                "duration_ms": result.duration_ms,
                "usage_quality": result.usage_quality,
                "uncertainty": list(result.uncertainty),
            },
        )
        if result.usage:
            self._emit(
                "usage_recorded",
                run_id=run_id,
                task_id=task_id,
                agent_id=agent_id,
                metadata={
                    **result.usage,
                    "usage_quality": result.usage_quality,
                    "execution_id": result.execution_id,
                },
            )
        return SpecialistRun(
            agent_id=agent_id,
            execution_id=result.execution_id or execution_id,
            task_id=task_id,
            result=result,
        )

    def run_rubric_council(
        self,
        *,
        run_id: str,
        rubric: dict,
        candidate_ref: str,
        evidence_refs: tuple[str, ...],
        context_refs: tuple[str, ...],
        applicability: dict[str, bool] | None = None,
    ) -> CouncilRun:
        applicability = applicability or {}
        reviews: list[dict[str, Any]] = []
        execution_ids: list[str] = []

        for dimension in rubric.get("dimensions", []):
            applies_if = dimension.get("applies_if")
            if applies_if and not applicability.get(applies_if, False):
                continue
            dimension_id = str(dimension["id"])
            for reviewer_id in (
                str(dimension["primary_reviewer"]),
                str(dimension["secondary_reviewer"]),
            ):
                review = self.run_review(
                    run_id=run_id,
                    dimension_id=dimension_id,
                    reviewer_id=reviewer_id,
                    candidate_ref=candidate_ref,
                    evidence_refs=evidence_refs,
                    context_refs=context_refs,
                )
                reviews.append(review)
                execution_ids.append(str(review["review_run_id"]))

        return CouncilRun(
            reviews=tuple(reviews),
            execution_run_ids=tuple(execution_ids),
        )

    def run_review(
        self,
        *,
        run_id: str,
        dimension_id: str,
        reviewer_id: str,
        candidate_ref: str,
        evidence_refs: tuple[str, ...],
        context_refs: tuple[str, ...],
        tool_grants: tuple[str, ...] = ("repository:read",),
    ) -> dict[str, Any]:
        specialist = self.invoke(
            run_id=run_id,
            task_id=f"review:{dimension_id}:{reviewer_id}",
            agent_id=reviewer_id,
            agent_contract_ref=f"agents/contracts/{reviewer_id}.md",
            output_schema_ref="quality/review-output.schema.json",
            context_refs=context_refs,
            tool_grants=tool_grants,
            task_input={
                "kind": "quality_review",
                "dimension_id": dimension_id,
                "reviewer_id": reviewer_id,
                "candidate_ref": candidate_ref,
                "evidence_refs": list(evidence_refs),
            },
        )
        if specialist.result.status != "completed":
            raise RuntimeError(
                f"review execution failed for {dimension_id}:{reviewer_id}: "
                f"{specialist.result.status}"
            )

        output = dict(specialist.result.output)
        if output.get("reviewer_id") not in {None, reviewer_id}:
            raise RuntimeError("reviewer identity mismatch")
        if output.get("dimension_id") not in {None, dimension_id}:
            raise RuntimeError("review dimension mismatch")

        output["reviewer_id"] = reviewer_id
        output["dimension_id"] = dimension_id
        output["review_run_id"] = specialist.execution_id
        return output


class A2DeliberationEngine:
    """Runs owner and challenger independently, then routes both to an arbiter."""

    ALLOWED_DECISIONS = {"KEEP", "REVISE_OWNER", "COMBINE", "ESCALATE"}

    def __init__(self, orchestrator: A2Orchestrator):
        self.orchestrator = orchestrator

    def deliberate(
        self,
        *,
        run_id: str,
        question_id: str,
        question: str,
        owner_agent: str,
        challenger_agent: str,
        arbiter_agent: str,
        candidate_ref: str,
        criterion: str,
        evidence_refs: tuple[str, ...],
        context_refs: tuple[str, ...],
    ) -> DeliberationOutcome:
        if len({owner_agent, challenger_agent, arbiter_agent}) != 3:
            raise ValueError("owner, challenger and arbiter must be distinct agents")

        common = {
            "kind": "deliberation_position",
            "question_id": question_id,
            "question": question,
            "candidate_ref": candidate_ref,
            "criterion": criterion,
            "evidence_refs": list(evidence_refs),
        }
        owner_run = self.orchestrator.invoke(
            run_id=run_id,
            task_id=f"deliberation:{question_id}:owner",
            agent_id=owner_agent,
            agent_contract_ref=f"agents/contracts/{owner_agent}.md",
            output_schema_ref="orchestration/deliberation-position.schema.json",
            context_refs=context_refs,
            tool_grants=("repository:read",),
            task_input={**common, "role": "owner"},
        )
        challenger_run = self.orchestrator.invoke(
            run_id=run_id,
            task_id=f"deliberation:{question_id}:challenger",
            agent_id=challenger_agent,
            agent_contract_ref=f"agents/contracts/{challenger_agent}.md",
            output_schema_ref="orchestration/deliberation-position.schema.json",
            context_refs=context_refs,
            tool_grants=("repository:read",),
            task_input={**common, "role": "challenger"},
        )

        if owner_run.result.status != "completed" or challenger_run.result.status != "completed":
            raise RuntimeError("owner and challenger must both complete before arbitration")
        if owner_run.execution_id == challenger_run.execution_id:
            raise RuntimeError("owner and challenger must be independent executions")

        arbiter_run = self.orchestrator.invoke(
            run_id=run_id,
            task_id=f"deliberation:{question_id}:arbiter",
            agent_id=arbiter_agent,
            agent_contract_ref=f"agents/contracts/{arbiter_agent}.md",
            output_schema_ref="orchestration/deliberation-arbitration.schema.json",
            context_refs=context_refs,
            tool_grants=("repository:read",),
            task_input={
                "kind": "deliberation_arbitration",
                "question_id": question_id,
                "question": question,
                "criterion": criterion,
                "candidate_ref": candidate_ref,
                "evidence_refs": list(evidence_refs),
                "owner_position": owner_run.result.output,
                "challenger_position": challenger_run.result.output,
                "owner_execution_id": owner_run.execution_id,
                "challenger_execution_id": challenger_run.execution_id,
            },
        )
        if arbiter_run.result.status != "completed":
            raise RuntimeError("arbiter execution did not complete")

        decision = str(arbiter_run.result.output.get("decision", "")).strip()
        rationale = str(arbiter_run.result.output.get("rationale", "")).strip()
        if decision not in self.ALLOWED_DECISIONS:
            raise RuntimeError(f"invalid arbiter decision: {decision}")
        if not rationale:
            raise RuntimeError("arbiter rationale is required")

        self.orchestrator._emit(
            "deliberation_round_completed",
            run_id=run_id,
            task_id=f"deliberation:{question_id}",
            agent_id=arbiter_agent,
            artifact_refs=list(arbiter_run.result.artifact_refs),
            metadata={
                "question_id": question_id,
                "decision": decision,
                "rationale": rationale,
                "owner_execution_id": owner_run.execution_id,
                "challenger_execution_id": challenger_run.execution_id,
                "arbiter_execution_id": arbiter_run.execution_id,
            },
        )
        if decision == "ESCALATE":
            self.orchestrator._emit(
                "human_escalation_opened",
                run_id=run_id,
                task_id=f"deliberation:{question_id}",
                agent_id=arbiter_agent,
                metadata={
                    "question_id": question_id,
                    "reason": "arbiter_escalation",
                    "rationale": rationale,
                },
            )

        return DeliberationOutcome(
            owner_run=owner_run,
            challenger_run=challenger_run,
            arbiter_run=arbiter_run,
            decision=decision,
            rationale=rationale,
        )
