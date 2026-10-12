from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from time import perf_counter
from typing import Any, Mapping, Protocol, Sequence
from uuid import uuid4
import json
import os
import subprocess


FORBIDDEN_AGENT_TOOL_GRANTS = {
    "repository:merge",
    "publication:publish",
    "authority:modify",
}


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
    agent_contract_ref: str | None = None
    output_schema_ref: str | None = None
    execution_id: str | None = None
    task_input: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ExecutionResult:
    status: str
    execution_surface: str
    artifact_refs: tuple[str, ...] = ()
    uncertainty: tuple[str, ...] = ()
    usage_quality: str = "unavailable"
    execution_id: str | None = None
    output: dict[str, Any] = field(default_factory=dict)
    usage: dict[str, int] = field(default_factory=dict)
    duration_ms: int | None = None


class ExecutionAdapter(Protocol):
    name: str
    autonomous: bool

    def execute(self, request: ExecutionRequest) -> ExecutionResult:
        ...


def _request_payload(request: ExecutionRequest, execution_id: str) -> dict[str, Any]:
    return {
        "execution_id": execution_id,
        "run_id": request.run_id,
        "repository": request.repository,
        "task_id": request.task_id,
        "primary_agent": request.primary_agent,
        "agent_contract_ref": request.agent_contract_ref,
        "output_schema_ref": request.output_schema_ref,
        "context_refs": list(request.context_refs),
        "tool_grants": list(request.tool_grants),
        "retry_budget": request.retry_budget,
        "human_gate": request.human_gate,
        "task_input": request.task_input,
    }


class PacketOnlyAdapter:
    """Materializes a bounded task packet without claiming autonomous A2 execution."""

    name = "packet-only"
    autonomous = False

    def __init__(self, output_dir: Path):
        self.output_dir = Path(output_dir)

    def execute(self, request: ExecutionRequest) -> ExecutionResult:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        execution_id = request.execution_id or f"exec_{uuid4().hex[:16]}"
        path = self.output_dir / f"{request.run_id}-{request.task_id}-{execution_id}.json"
        packet = _request_payload(request, execution_id)
        packet["adapter_status"] = "waiting_external_executor"
        path.write_text(
            json.dumps(packet, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        return ExecutionResult(
            status="waiting_external_executor",
            execution_surface=self.name,
            artifact_refs=(str(path),),
            uncertainty=("No autonomous execution adapter is installed for this request.",),
            execution_id=execution_id,
        )


class JsonSubprocessAdapter:
    """Runs one bounded specialist as an isolated JSON stdin/stdout process.

    The adapter is provider-neutral: the configured command may wrap Codex, an
    OpenAI API worker, another model runtime, or a deterministic test runner.
    Every invocation is a distinct process and receives only its declared
    packet. It must return one JSON object on stdout.
    """

    name = "json-subprocess"
    autonomous = True

    def __init__(
        self,
        command: Sequence[str],
        artifact_dir: Path,
        *,
        timeout_seconds: int = 180,
        cwd: Path | None = None,
        extra_env: Mapping[str, str] | None = None,
    ):
        if not command:
            raise ValueError("command is required")
        if timeout_seconds < 1:
            raise ValueError("timeout_seconds must be >= 1")
        self.command = tuple(str(part) for part in command)
        self.artifact_dir = Path(artifact_dir)
        self.timeout_seconds = int(timeout_seconds)
        self.cwd = Path(cwd) if cwd else None
        self.extra_env = dict(extra_env or {})

    def execute(self, request: ExecutionRequest) -> ExecutionResult:
        execution_id = request.execution_id or f"exec_{uuid4().hex[:16]}"
        run_dir = self.artifact_dir / request.run_id
        run_dir.mkdir(parents=True, exist_ok=True)

        request_path = run_dir / f"{execution_id}.request.json"
        result_path = run_dir / f"{execution_id}.result.json"
        packet = _request_payload(request, execution_id)
        request_path.write_text(
            json.dumps(packet, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

        env = os.environ.copy()
        env.update(self.extra_env)
        started = perf_counter()
        try:
            completed = subprocess.run(
                self.command,
                input=json.dumps(packet, ensure_ascii=False),
                text=True,
                capture_output=True,
                cwd=str(self.cwd) if self.cwd else None,
                env=env,
                timeout=self.timeout_seconds,
                check=False,
            )
            duration_ms = max(0, round((perf_counter() - started) * 1000))
        except subprocess.TimeoutExpired as exc:
            duration_ms = max(0, round((perf_counter() - started) * 1000))
            record = {
                "execution_id": execution_id,
                "status": "failed",
                "error": "timeout",
                "duration_ms": duration_ms,
                "stderr": str(exc.stderr or "")[-4000:],
            }
            result_path.write_text(
                json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            return ExecutionResult(
                status="failed",
                execution_surface=self.name,
                artifact_refs=(str(request_path), str(result_path)),
                uncertainty=("Specialist process exceeded its timeout.",),
                execution_id=execution_id,
                duration_ms=duration_ms,
            )

        if completed.returncode != 0:
            record = {
                "execution_id": execution_id,
                "status": "failed",
                "error": "nonzero_exit",
                "returncode": completed.returncode,
                "duration_ms": duration_ms,
                "stderr": completed.stderr[-4000:],
            }
            result_path.write_text(
                json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            return ExecutionResult(
                status="failed",
                execution_surface=self.name,
                artifact_refs=(str(request_path), str(result_path)),
                uncertainty=(f"Specialist process exited with {completed.returncode}.",),
                execution_id=execution_id,
                duration_ms=duration_ms,
            )

        try:
            payload = json.loads(completed.stdout)
        except json.JSONDecodeError:
            record = {
                "execution_id": execution_id,
                "status": "failed",
                "error": "invalid_json",
                "duration_ms": duration_ms,
                "stdout": completed.stdout[-4000:],
                "stderr": completed.stderr[-4000:],
            }
            result_path.write_text(
                json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            return ExecutionResult(
                status="failed",
                execution_surface=self.name,
                artifact_refs=(str(request_path), str(result_path)),
                uncertainty=("Specialist process did not return valid JSON.",),
                execution_id=execution_id,
                duration_ms=duration_ms,
            )

        status = str(payload.get("status", "")).strip()
        if status not in {"completed", "failed", "blocked"}:
            status = "failed"
            payload.setdefault("uncertainty", []).append("Invalid or missing result status.")

        output = payload.get("output")
        if not isinstance(output, dict):
            output = {}

        usage_raw = payload.get("usage")
        usage: dict[str, int] = {}
        if isinstance(usage_raw, dict):
            for key in ("input_tokens", "output_tokens", "cached_tokens", "total_tokens"):
                value = usage_raw.get(key)
                if isinstance(value, int) and value >= 0:
                    usage[key] = value

        usage_quality = str(payload.get("usage_quality", "unavailable"))
        if usage_quality not in {"exact", "estimated", "unavailable"}:
            usage_quality = "unavailable"

        uncertainty_raw = payload.get("uncertainty") or []
        uncertainty = tuple(str(item) for item in uncertainty_raw if str(item).strip())
        external_refs = tuple(
            str(item) for item in (payload.get("artifact_refs") or []) if str(item).strip()
        )

        record = {
            "execution_id": execution_id,
            "status": status,
            "duration_ms": duration_ms,
            "output": output,
            "usage": usage,
            "usage_quality": usage_quality,
            "uncertainty": list(uncertainty),
            "artifact_refs": list(external_refs),
            "stderr": completed.stderr[-4000:] if completed.stderr else "",
        }
        result_path.write_text(
            json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

        return ExecutionResult(
            status=status,
            execution_surface=self.name,
            artifact_refs=(str(request_path), str(result_path), *external_refs),
            uncertainty=uncertainty,
            usage_quality=usage_quality,
            execution_id=execution_id,
            output=output,
            usage=usage,
            duration_ms=duration_ms,
        )


class BoundedExecutor:
    """Authority/budget guard in front of A2 execution adapters."""

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

        forbidden = FORBIDDEN_AGENT_TOOL_GRANTS.intersection(request.tool_grants)
        if forbidden:
            raise PermissionError(
                "agent execution cannot receive human-owned authority: "
                + ", ".join(sorted(forbidden))
            )

        if adapter.autonomous:
            if not request.agent_contract_ref:
                raise ValueError("autonomous execution requires agent_contract_ref")
            if not request.output_schema_ref:
                raise ValueError("autonomous execution requires output_schema_ref")

        result = adapter.execute(request)
        if result.status == "completed" and not adapter.autonomous:
            raise RuntimeError("non-autonomous adapter may not report autonomous completion")
        if adapter.autonomous and not result.execution_id:
            raise RuntimeError("autonomous adapter must return execution_id")
        return result
