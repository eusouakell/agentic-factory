from __future__ import annotations

import json
import sys


packet = json.load(sys.stdin)
task_input = packet.get("task_input") or {}
kind = task_input.get("kind")

if kind == "quality_review":
    output = {
        "dimension_id": task_input["dimension_id"],
        "reviewer_id": task_input["reviewer_id"],
        "score": 9.4,
        "status": "pass",
        "evidence_refs": task_input.get("evidence_refs") or ["artifact://candidate"],
        "findings": [],
    }
elif kind == "deliberation_position":
    role = task_input.get("role")
    output = {
        "decision": "revise" if role == "challenger" else "keep",
        "evidence": task_input.get("evidence_refs") or [],
        "criterion": task_input.get("criterion", "quality"),
        "risk": "The composition may misallocate visual emphasis.",
        "recommended_action": "Rebalance image and type scale." if role == "challenger" else "Keep the current route.",
        "confidence": 0.9 if role == "challenger" else 0.8,
    }
elif kind == "deliberation_arbitration":
    if task_input.get("owner_execution_id") == task_input.get("challenger_execution_id"):
        print(json.dumps({"status": "failed", "output": {}, "uncertainty": ["non-independent inputs"]}))
        raise SystemExit(0)
    output = {
        "decision": "REVISE_OWNER",
        "rationale": "The challenger identifies a concrete criterion failure with lower downstream risk.",
        "evidence_refs": task_input.get("evidence_refs") or [],
    }
else:
    output = {"ok": True}

print(
    json.dumps(
        {
            "status": "completed",
            "output": output,
            "artifact_refs": [],
            "usage": {
                "input_tokens": 100,
                "output_tokens": 40,
                "cached_tokens": 0,
                "total_tokens": 140,
            },
            "usage_quality": "exact",
            "uncertainty": [],
        }
    )
)
