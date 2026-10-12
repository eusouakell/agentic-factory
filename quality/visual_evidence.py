from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass


@dataclass(frozen=True)
class VisualEvidenceResult:
    passed: bool
    issues: tuple[str, ...]


def _number(value):
    return float(value) if isinstance(value, (int, float)) else None


def validate_visual_manifest(manifest: dict) -> VisualEvidenceResult:
    required_viewports = [int(v) for v in manifest.get("required_viewports", [])]
    required_sections = [str(s) for s in manifest.get("required_sections", [])]
    captures = list(manifest.get("captures", []))
    constraints = dict(manifest.get("constraints") or {})
    section_constraints = dict(manifest.get("section_constraints") or {})
    section_anchors = dict(manifest.get("section_anchors") or {})
    require_geometry = bool(manifest.get("require_geometry", False))

    overflow_tolerance = float(constraints.get("horizontal_overflow_tolerance_px", 2))
    aspect_delta_limit = float(constraints.get("max_image_aspect_ratio_delta", 0.04))
    default_min_heading_ratio = float(constraints.get("min_heading_body_ratio", 1.4))
    default_max_heading_ratio = float(constraints.get("max_heading_body_ratio", 7.5))

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
        expected_anchor = str(section_anchors.get(section, section))
        if dom_anchor != expected_anchor:
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

        document_metrics = capture.get("document_metrics")
        section_box = capture.get("section_box")
        images = capture.get("images")
        typography = capture.get("typography")

        if require_geometry and not isinstance(document_metrics, dict):
            issues.append(f"{prefix}:missing_document_metrics")
        if require_geometry and not isinstance(section_box, dict):
            issues.append(f"{prefix}:missing_section_box")
        if require_geometry and not isinstance(images, list):
            issues.append(f"{prefix}:missing_image_metrics")
        if require_geometry and not isinstance(typography, dict):
            issues.append(f"{prefix}:missing_typography_metrics")

        if isinstance(document_metrics, dict):
            scroll_width = _number(document_metrics.get("scroll_width"))
            client_width = _number(document_metrics.get("client_width"))
            if scroll_width is not None and client_width is not None:
                if scroll_width - client_width > overflow_tolerance:
                    issues.append(f"{prefix}:horizontal_overflow")

        if isinstance(section_box, dict):
            left = _number(section_box.get("left"))
            right = _number(section_box.get("right"))
            width = _number(section_box.get("width"))
            if left is not None and left < -overflow_tolerance:
                issues.append(f"{prefix}:section_overflows_left")
            if right is not None and right > viewport + overflow_tolerance:
                issues.append(f"{prefix}:section_overflows_right")
            if width is not None and width > viewport + overflow_tolerance:
                issues.append(f"{prefix}:section_wider_than_viewport")

        local_constraints = dict(section_constraints.get(section) or {})
        max_image_width_ratio = _number(local_constraints.get("max_image_width_ratio"))
        max_image_area_ratio = _number(local_constraints.get("max_image_viewport_area_ratio"))
        viewport_height = _number(capture.get("viewport_height"))

        if isinstance(images, list):
            for index, image in enumerate(images):
                if not isinstance(image, dict):
                    issues.append(f"{prefix}:image_{index}:malformed")
                    continue
                natural_width = _number(image.get("natural_width"))
                natural_height = _number(image.get("natural_height"))
                rendered_width = _number(image.get("rendered_width"))
                rendered_height = _number(image.get("rendered_height"))
                if (
                    natural_width
                    and natural_height
                    and rendered_width
                    and rendered_height
                    and natural_width > 0
                    and natural_height > 0
                    and rendered_width > 0
                    and rendered_height > 0
                ):
                    natural_ratio = natural_width / natural_height
                    rendered_ratio = rendered_width / rendered_height
                    delta = abs(rendered_ratio / natural_ratio - 1.0)
                    if delta > aspect_delta_limit:
                        issues.append(f"{prefix}:image_{index}:aspect_ratio_distorted")
                    if max_image_width_ratio is not None:
                        width_ratio = rendered_width / viewport
                        if width_ratio > max_image_width_ratio:
                            issues.append(f"{prefix}:image_{index}:width_dominance_exceeded")
                    if max_image_area_ratio is not None and viewport_height:
                        area_ratio = (rendered_width * rendered_height) / (
                            viewport * viewport_height
                        )
                        if area_ratio > max_image_area_ratio:
                            issues.append(f"{prefix}:image_{index}:area_dominance_exceeded")

        if isinstance(typography, dict):
            heading_px = _number(typography.get("heading_font_px"))
            body_px = _number(typography.get("body_font_px"))
            if heading_px is not None and body_px is not None and body_px > 0:
                ratio = heading_px / body_px
                min_ratio = float(
                    local_constraints.get("min_heading_body_ratio", default_min_heading_ratio)
                )
                max_ratio = float(
                    local_constraints.get("max_heading_body_ratio", default_max_heading_ratio)
                )
                if ratio < min_ratio:
                    issues.append(f"{prefix}:heading_hierarchy_too_weak")
                if ratio > max_ratio:
                    issues.append(f"{prefix}:heading_hierarchy_too_extreme")

    for viewport in required_viewports:
        for section in required_sections:
            records = indexed.get((viewport, section), [])
            if not records:
                issues.append(f"visual_manifest:{viewport}:{section}:missing_capture")
            elif len(records) > 1:
                issues.append(f"visual_manifest:{viewport}:{section}:duplicate_capture")

    return VisualEvidenceResult(passed=not issues, issues=tuple(sorted(set(issues))))
