from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass


@dataclass(frozen=True)
class VisualEvidenceResult:
    passed: bool
    issues: tuple[str, ...]


def validate_visual_manifest(manifest: dict) -> VisualEvidenceResult:
    required_viewports = [int(v) for v in manifest.get("required_viewports", [])]
    required_sections = [str(s) for s in manifest.get("required_sections", [])]
    captures = list(manifest.get("captures", []))

    issues: list[str] = []
    if not required_viewports:
        issues.append("visual_manifest:no_required_viewports")
    if not required_sections:
        issues.append("visual_manifest:no_required_sections")

    indexed: dict[tuple[int, str], list[dict]] = defaultdict(list)
    hashes_by_viewport: dict[int, dict[str, str]] = defaultdict(dict)

    for capture in captures:
        try:
            viewport = int(capture["viewport_width"])
            section = str(capture["section_id"])
        except (KeyError, TypeError, ValueError):
            issues.append("visual_manifest:malformed_capture")
            continue

        indexed[(viewport, section)].append(capture)

        artifact_ref = str(capture.get("artifact_ref", "")).strip()
        content_hash = str(capture.get("content_sha256", "")).strip()
        heading = str(capture.get("observed_heading", "")).strip()
        dom_anchor = str(capture.get("dom_anchor", "")).strip()
        reviewer = str(capture.get("reviewer_id", "")).strip()
        review_run = str(capture.get("review_run_id", "")).strip()
        status = capture.get("status")

        prefix = f"visual_manifest:{viewport}:{section}"
        if not artifact_ref:
            issues.append(f"{prefix}:missing_artifact_ref")
        if len(content_hash) != 64:
            issues.append(f"{prefix}:missing_or_invalid_sha256")
        if not heading:
            issues.append(f"{prefix}:missing_observed_heading")
        if dom_anchor != section:
            issues.append(f"{prefix}:anchor_mismatch")
        if not reviewer or not review_run:
            issues.append(f"{prefix}:missing_independent_review")
        if status != "pass":
            issues.append(f"{prefix}:review_not_pass")

        if content_hash:
            prior_section = hashes_by_viewport[viewport].get(content_hash)
            if prior_section and prior_section != section:
                issues.append(
                    f"visual_manifest:{viewport}:duplicate_capture_hash:{prior_section}:{section}"
                )
            else:
                hashes_by_viewport[viewport][content_hash] = section

    for viewport in required_viewports:
        for section in required_sections:
            records = indexed.get((viewport, section), [])
            if not records:
                issues.append(f"visual_manifest:{viewport}:{section}:missing_capture")
            elif len(records) > 1:
                issues.append(f"visual_manifest:{viewport}:{section}:duplicate_capture")

    return VisualEvidenceResult(passed=not issues, issues=tuple(sorted(set(issues))))
