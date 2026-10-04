from __future__ import annotations

import argparse
import fnmatch
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_registry(path: Path | None = None) -> dict:
    path = path or ROOT / "automations" / "registry.json"
    return json.loads(path.read_text(encoding="utf-8"))


def any_path_matches(paths: list[str], patterns: list[str]) -> bool:
    if not patterns:
        return True
    return any(fnmatch.fnmatch(path, pattern) for path in paths for pattern in patterns)


def route_event(
    registry: dict,
    repository: str,
    event: str,
    paths: list[str] | None = None,
    labels: list[str] | None = None,
) -> list[dict]:
    paths = paths or []
    labels = labels or []
    matches: list[dict] = []

    for automation in registry.get("automations", []):
        if automation.get("repository") != repository:
            continue
        if automation.get("event") != event:
            continue

        triggers = automation.get("triggers", {})
        path_patterns = triggers.get("paths", [])
        trigger_labels = triggers.get("labels", [])

        path_match = any_path_matches(paths, path_patterns)
        label_match = not trigger_labels or any(label in labels for label in trigger_labels)

        if not path_match or not label_match:
            continue

        required_agents = []
        conditional_agents = []
        for route in automation.get("route", []):
            if route.get("required"):
                required_agents.append(route["agent_id"])
                continue

            path_conditions = route.get("required_if_paths", [])
            if path_conditions and any_path_matches(paths, path_conditions):
                required_agents.append(route["agent_id"])
                continue

            conditional_agents.append(
                {
                    "agent_id": route["agent_id"],
                    "conditions": {
                        key: value
                        for key, value in route.items()
                        if key != "agent_id"
                    },
                }
            )

        matches.append(
            {
                "automation_id": automation["id"],
                "repository": repository,
                "event": event,
                "matched_paths": paths,
                "required_agents": required_agents,
                "conditional_agents": conditional_agents,
                "semantic_evals": automation.get("semantic_evals", []),
                "execution_surface": automation["execution_surface"],
                "human_gate": automation["human_gate"],
                "max_retries": automation["max_retries"],
                "adapter_status": automation.get("adapter_status", "spec_only"),
            }
        )

    return matches


def render_markdown(plans: list[dict]) -> str:
    if not plans:
        return "## Agentic Factory automation route\n\nNo automation matched this event.\n"

    lines = ["## Agentic Factory automation route", ""]
    for plan in plans:
        lines.extend(
            [
                f"### {plan['automation_id']}",
                f"- Execution surface: `{plan['execution_surface']}`",
                f"- Human gate: **{plan['human_gate']}**",
                f"- Adapter: `{plan['adapter_status']}`",
                f"- Retry budget: {plan['max_retries']}",
                "- Required agents: "
                + (
                    ", ".join(f"`{x}`" for x in plan["required_agents"])
                    if plan["required_agents"]
                    else "none"
                ),
            ]
        )
        if plan["conditional_agents"]:
            lines.append("- Conditional agents:")
            for item in plan["conditional_agents"]:
                cond = ", ".join(
                    f"{k}={v}" for k, v in item["conditions"].items()
                )
                lines.append(f"  - `{item['agent_id']}` — {cond}")
        if plan["semantic_evals"]:
            lines.append(
                "- Semantic evals: "
                + ", ".join(f"`{x}`" for x in plan["semantic_evals"])
            )
        lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Route an event through Automation Layer V1.")
    parser.add_argument("--repository", required=True)
    parser.add_argument("--event", required=True)
    parser.add_argument("--path", action="append", default=[])
    parser.add_argument("--label", action="append", default=[])
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    plans = route_event(
        load_registry(),
        repository=args.repository,
        event=args.event,
        paths=args.path,
        labels=args.label,
    )

    if args.as_json:
        print(json.dumps({"plans": plans}, indent=2))
    else:
        print(render_markdown(plans))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
