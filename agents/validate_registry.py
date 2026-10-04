from __future__ import annotations

import argparse
import json
from pathlib import Path

REQUIRED_FIELDS = {
    "id","name","domain","role_type","tier","status","enabled_by_default","purpose","trigger",
    "inputs","outputs","allowed_tools","write_authority","guides","guards","sensors",
    "checks","evals","human_gate","retry_policy","escalation","provenance","contract"
}
ROLE_TYPES = {"executor","auditor","evaluator","director","research_specialist"}
TIERS = {"core","on_demand"}
STATUSES = {"pilot","active","retired"}
FORBIDDEN_WRITE_AUTHORITIES = {"main","publish","production"}


def validate_registry(data: dict, repo_root: Path | None = None) -> list[str]:
    errors: list[str] = []
    repo_root = repo_root or Path(__file__).resolve().parents[1]

    if data.get("schema_version") != "2.0":
        errors.append("schema_version must be 2.0")

    control = data.get("control_plane", {})
    if control.get("orchestrator_is_agent") is not False:
        errors.append("control_plane.orchestrator_is_agent must be false")

    roster = data.get("roster", {})
    if not roster.get("core_definition") or not roster.get("on_demand_definition"):
        errors.append("roster must define core and on_demand semantics")

    agents = data.get("agents")
    if not isinstance(agents, list) or not agents:
        return errors + ["agents must be a non-empty list"]

    ids: set[str] = set()
    contracts: set[str] = set()

    for index, agent in enumerate(agents):
        prefix = f"agents[{index}]"
        missing = sorted(REQUIRED_FIELDS - set(agent))
        if missing:
            errors.append(f"{prefix}: missing fields: {', '.join(missing)}")
            continue

        agent_id = agent["id"]
        if agent_id in ids:
            errors.append(f"{prefix}: duplicate id {agent_id}")
        ids.add(agent_id)

        contract = agent["contract"]
        if contract in contracts:
            errors.append(f"{agent_id}: duplicate contract path {contract}")
        contracts.add(contract)

        expected_contract = f"agents/contracts/{agent_id}.md"
        if contract != expected_contract:
            errors.append(f"{agent_id}: contract must be {expected_contract}")
        if not (repo_root / contract).is_file():
            errors.append(f"{agent_id}: contract file not found: {contract}")

        if agent["role_type"] not in ROLE_TYPES:
            errors.append(f"{agent_id}: invalid role_type {agent['role_type']}")
        if agent["tier"] not in TIERS:
            errors.append(f"{agent_id}: invalid tier {agent['tier']}")
        if agent["status"] not in STATUSES:
            errors.append(f"{agent_id}: invalid status {agent['status']}")
        if agent["write_authority"] in FORBIDDEN_WRITE_AUTHORITIES:
            errors.append(f"{agent_id}: forbidden direct write authority {agent['write_authority']}")
        if agent["enabled_by_default"] is not False and agent["status"] == "pilot":
            errors.append(f"{agent_id}: pilot agents must not be enabled by default")

        for field in ("inputs","outputs","allowed_tools","guards","provenance"):
            if not isinstance(agent[field], list) or not agent[field]:
                errors.append(f"{agent_id}: {field} must be a non-empty list")

        if not str(agent["human_gate"]).strip():
            errors.append(f"{agent_id}: human_gate must be explicit")
        if not str(agent["escalation"]).strip():
            errors.append(f"{agent_id}: escalation must be explicit")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Agent Registry V2")
    parser.add_argument("registry", type=Path, nargs="?", default=Path("agents/registry.json"))
    args = parser.parse_args()

    data = json.loads(args.registry.read_text(encoding="utf-8"))
    errors = validate_registry(data, Path.cwd())
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    print(f"PASS: {len(data['agents'])} agents satisfy Registry V2 and contract checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
