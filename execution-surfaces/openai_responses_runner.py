#!/usr/bin/env python3
"""Provider-backed A2 runner for the OpenAI Responses API.

Reads one ExecutionRequest packet from stdin and emits one ExecutionResult-like
JSON object to stdout. The runner is deliberately read-only: it receives no
repository credentials and has no write/merge/publish tools.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


API_URL = os.environ.get("OPENAI_RESPONSES_URL", "https://api.openai.com/v1/responses")
MODEL = os.environ.get("A2_OPENAI_MODEL", "gpt-5.3-codex")
TIMEOUT = int(os.environ.get("A2_OPENAI_HTTP_TIMEOUT", "120"))


def _read_local(ref: str, root: Path) -> str | None:
    ref = ref.removeprefix("file://")
    if "://" in ref:
        return None
    path = (root / ref).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError:
        return None
    if not path.is_file() or path.stat().st_size > 300_000:
        return None
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return None


def _context(packet: dict[str, Any], root: Path) -> dict[str, Any]:
    materialized: dict[str, Any] = {}
    refs = list(packet.get("context_refs") or [])
    task_input = packet.get("task_input") or {}
    for key in ("candidate_ref",):
        value = task_input.get(key)
        if isinstance(value, str):
            refs.append(value)
    refs.extend(x for x in (task_input.get("evidence_refs") or []) if isinstance(x, str))

    for ref in refs:
        if not isinstance(ref, str) or ref in materialized:
            continue
        text = _read_local(ref, root)
        materialized[ref] = text if text is not None else {"unresolved_ref": ref}

    bundle = task_input.get("context_bundle")
    if isinstance(bundle, (dict, list, str)):
        materialized["inline_context_bundle"] = bundle
    return materialized


def _extract_output_text(response: dict[str, Any]) -> str:
    chunks: list[str] = []
    for item in response.get("output") or []:
        if not isinstance(item, dict):
            continue
        for part in item.get("content") or []:
            if isinstance(part, dict) and part.get("type") == "output_text":
                text = part.get("text")
                if isinstance(text, str):
                    chunks.append(text)
    return "\n".join(chunks).strip()


def main() -> int:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print(json.dumps({
            "status": "blocked",
            "output": {},
            "usage_quality": "unavailable",
            "uncertainty": ["OPENAI_API_KEY is not configured for the provider runner."],
        }))
        return 0

    packet = json.loads(sys.stdin.read())
    root = Path(os.environ.get("A2_REPOSITORY_ROOT", ".")).resolve()

    contract = None
    contract_ref = packet.get("agent_contract_ref")
    if isinstance(contract_ref, str):
        contract = _read_local(contract_ref, root)

    schema_text = None
    schema_ref = packet.get("output_schema_ref")
    if isinstance(schema_ref, str):
        schema_text = _read_local(schema_ref, root)

    prompt = {
        "role": packet.get("primary_agent"),
        "task": packet.get("task_input") or {},
        "authority": {
            "tool_grants": packet.get("tool_grants") or [],
            "human_gate": packet.get("human_gate"),
            "forbidden": ["merge", "publish", "modify authority", "invent evidence"],
        },
        "contract": contract or {"unresolved_ref": contract_ref},
        "output_schema": schema_text or {"unresolved_ref": schema_ref},
        "context": _context(packet, root),
    }

    instructions = (
        "You are one isolated specialist execution in an agentic review system. "
        "Use only the supplied packet and materialized context. Do not claim to have "
        "opened unresolved references. Respect the declared human gate and authority. "
        "Return ONLY one JSON object with keys: status, output, uncertainty. "
        "status must be completed, failed, or blocked. output must be a JSON object "
        "that follows the supplied output schema when available. uncertainty must be "
        "an array of concise strings."
    )

    body = json.dumps({
        "model": MODEL,
        "instructions": instructions,
        "input": json.dumps(prompt, ensure_ascii=False),
        "store": False,
    }).encode("utf-8")
    request = urllib.request.Request(
        API_URL,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[-2000:]
        print(json.dumps({
            "status": "failed",
            "output": {},
            "usage_quality": "unavailable",
            "uncertainty": [f"OpenAI Responses API HTTP {exc.code}: {detail}"],
        }))
        return 0
    except Exception as exc:
        print(json.dumps({
            "status": "failed",
            "output": {},
            "usage_quality": "unavailable",
            "uncertainty": [f"OpenAI provider runner error: {type(exc).__name__}: {exc}"],
        }))
        return 0

    raw_text = _extract_output_text(payload)
    try:
        specialist = json.loads(raw_text)
    except json.JSONDecodeError:
        specialist = {
            "status": "failed",
            "output": {},
            "uncertainty": ["Provider returned non-JSON specialist output."],
        }

    usage_raw = payload.get("usage") or {}
    usage = {
        key: value
        for key, value in {
            "input_tokens": usage_raw.get("input_tokens"),
            "output_tokens": usage_raw.get("output_tokens"),
            "total_tokens": usage_raw.get("total_tokens"),
            "cached_tokens": (usage_raw.get("input_tokens_details") or {}).get("cached_tokens"),
        }.items()
        if isinstance(value, int) and value >= 0
    }

    result = {
        "status": specialist.get("status", "failed"),
        "output": specialist.get("output") if isinstance(specialist.get("output"), dict) else {},
        "uncertainty": specialist.get("uncertainty") if isinstance(specialist.get("uncertainty"), list) else [],
        "usage": usage,
        "usage_quality": "exact" if usage else "unavailable",
        "artifact_refs": [],
        "provider": {
            "name": "openai-responses",
            "model": payload.get("model", MODEL),
            "response_id": payload.get("id"),
        },
    }
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
