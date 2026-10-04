from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = {
    "id",
    "repository",
    "event",
    "triggers",
    "route",
    "execution_surface",
    "human_gate",
    "max_retries",
    "adapter_status",
}


def validate(data: dict) -> list[str]:
    errors: list[str] = []
    if data.get("schema_version") != "1.0":
        errors.append("schema_version must be 1.0")

    ids: set[str] = set()
    for i, automation in enumerate(data.get("automations", [])):
        missing = REQUIRED - set(automation)
        if missing:
            errors.append(f"automations[{i}] missing: {', '.join(sorted(missing))}")
            continue
        if automation["id"] in ids:
            errors.append(f"duplicate automation id: {automation['id']}")
        ids.add(automation["id"])
        if not isinstance(automation["max_retries"], int) or automation["max_retries"] < 0:
            errors.append(f"{automation['id']}: max_retries must be >= 0")
        if not automation["human_gate"]:
            errors.append(f"{automation['id']}: human_gate required")
        if not automation["route"]:
            errors.append(f"{automation['id']}: route must not be empty")
        if automation["adapter_status"] not in {"installed", "spec_only"}:
            errors.append(f"{automation['id']}: invalid adapter_status")
    return errors


def main() -> int:
    path = ROOT / "automations" / "registry.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    errors = validate(data)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print(f"PASS: {len(data['automations'])} automation contracts valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
