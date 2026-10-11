from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol
import json


@dataclass(frozen=True)
class ExecutionRequest:
    run_id: str
    repository: str
    task_id: str
    primary_agent: str
    context_refs: tuple[str, ...]
    tool_grants: tuple[str, ...]
    retry_budget: int
    human_gate: str | None


@dataclass(frozen=True)
class ExecutionResult:
    status: str
    execution_surface: str
    artifact_refs: tuple[str, ...] = ()
    uncertainty: tuple[str, ...] = ()
    usage_quality: str = "unavailable"


class ExecutionAdapter(Protocol):
    name: str
    autonomous: bool

    def execute(self, request: ExecutionRequest) -> ExecutionResult:
        ...


class PacketOnlyAdapter:
    """Materializes a bounded task packet without claiming autonomous A2 execution."""

    name = "packet-only"
    autonomous = False

    def __init__(self, output_dir: Path):
        self.output_dir = Path(output_dir)

    def execute(self, request: ExecutionRequest) -> ExecutionResult:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        path = self.output_dir / f"{request.run_id}-{request.task_id}.json"
        path.write_text(
            json.dumps(
                {
                    "run_id": request.run_id,
                    "repository": request.repository,
                    "task_id": request.task_id,
                    "primary_agent": request.primary_agent,
                    "context_refs": list(request.context_refs),
                    "tool_grants": list(request.tool_grants),
                    "retry_budget": request.retry_budget,
                    "human_gate": request.human_gate,
                    "adapter_status": "waiting_external_executor",
                },
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        return ExecutionResult(
            status="waiting_external_executor",
            execution_surface=self.name,
            artifact_refs=(str(path),),
            uncertainty=("No autonomous execution adapter is installed for this request.",),
        )


class BoundedExecutor:
    """Authority/budget guard in front of any future A2 adapter."""

    def __init__(
        self,
        *,
        repository_allowlist: set[str],
        agent_allowlist: set[str],
        max_retry_budget: int = 2,
    ):
        self.repository_allowlist = set(repository_allowlist)
        self.agent_allowlist = set(agent_allowlist)
        self.max_retry_budget = int(max_retry_budget)

    def execute(self, request: ExecutionRequest, adapter: ExecutionAdapter) -> ExecutionResult:
        if request.repository not in self.repository_allowlist:
            raise PermissionError(f"repository not allowlisted: {request.repository}")
        if request.primary_agent not in self.agent_allowlist:
            raise PermissionError(f"agent not allowlisted: {request.primary_agent}")
        if request.retry_budget < 0 or request.retry_budget > self.max_retry_budget:
            raise PermissionError(
                f"retry budget {request.retry_budget} exceeds maximum {self.max_retry_budget}"
            )
        if not request.context_refs:
            raise ValueError("at least one context_ref is required")
        if any(not grant.strip() for grant in request.tool_grants):
            raise ValueError("tool grants must be explicit non-empty strings")

        result = adapter.execute(request)
        if result.status == "completed" and not adapter.autonomous:
            raise RuntimeError(
                "non-autonomous adapter may not report autonomous completion"
            )
        return result
