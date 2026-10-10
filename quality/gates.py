from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


ALLOWED_STATUS = {"pass", "fail", "not_applicable", "unknown"}
BLOCKING_SEVERITY = {"blocker"}


@dataclass(frozen=True)
class GateResult:
    gate_id: str
    passed: bool
    blockers: tuple[str, ...]
    unknown_blockers: tuple[str, ...]
    overridden: bool = False
    override_reason: str | None = None


def evaluate_gate(
    gate_id: str,
    template_items: Iterable[dict],
    results: dict[str, dict],
    *,
    override: bool = False,
    override_reason: str | None = None,
) -> GateResult:
    blockers: list[str] = []
    unknown_blockers: list[str] = []

    for item in template_items:
        check_id = item["check_id"]
        severity = item.get("severity", "advisory")
        record = results.get(check_id, {"status": "unknown"})
        status = record.get("status", "unknown")

        if status not in ALLOWED_STATUS:
            raise ValueError(f"invalid quality status for {check_id}: {status}")

        if severity in BLOCKING_SEVERITY:
            if status == "fail":
                blockers.append(check_id)
            elif status == "unknown":
                unknown_blockers.append(check_id)

    passed = not blockers and not unknown_blockers
    if override:
        if not override_reason:
            raise ValueError("override_reason is required when override=True")
        passed = True

    return GateResult(
        gate_id=gate_id,
        passed=passed,
        blockers=tuple(blockers),
        unknown_blockers=tuple(unknown_blockers),
        overridden=override,
        override_reason=override_reason,
    )
