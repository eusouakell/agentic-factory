from __future__ import annotations

from dataclasses import dataclass
from statistics import mean

from quality.visual_evidence import validate_visual_manifest


@dataclass(frozen=True)
class RubricEvaluation:
    passed: bool
    weighted_score: float
    dimension_scores: dict[str, float]
    reviewer_spread: dict[str, float]
    blockers: tuple[str, ...]
    missing_reviews: tuple[str, ...]


def evaluate_publish_readiness(
    rubric: dict,
    reviews: list[dict],
    *,
    visual_manifest: dict,
    readiness_status: str,
    open_material_questions: int = 0,
    unresolved_dissent: int = 0,
    applicability: dict[str, bool] | None = None,
    execution_run_ids: set[str] | None = None,
) -> RubricEvaluation:
    thresholds = rubric.get("thresholds", {})
    weighted_min = float(thresholds.get("weighted_minimum", 0))
    dimension_min = float(thresholds.get("dimension_minimum", 0))
    max_spread = float(thresholds.get("max_independent_reviewer_spread", 999))
    applicability = applicability or {}

    by_key: dict[tuple[str, str], dict] = {}
    blockers: list[str] = []
    missing: list[str] = []
    dimension_scores: dict[str, float] = {}
    spreads: dict[str, float] = {}
    weighted_parts: list[tuple[float, float]] = []

    for review in reviews:
        dimension_id = str(review.get("dimension_id", ""))
        reviewer_id = str(review.get("reviewer_id", ""))
        key = (dimension_id, reviewer_id)
        if not dimension_id or not reviewer_id:
            blockers.append("rubric:malformed_review")
            continue
        if key in by_key:
            blockers.append(f"rubric:duplicate_review:{dimension_id}:{reviewer_id}")
        by_key[key] = review

    for dimension in rubric.get("dimensions", []):
        dimension_id = dimension["id"]
        applies_if = dimension.get("applies_if")
        if applies_if and not applicability.get(applies_if, False):
            continue

        primary = dimension["primary_reviewer"]
        secondary = dimension["secondary_reviewer"]
        primary_record = by_key.get((dimension_id, primary))
        secondary_record = by_key.get((dimension_id, secondary))

        if not primary_record:
            missing.append(f"{dimension_id}:{primary}")
        if not secondary_record:
            missing.append(f"{dimension_id}:{secondary}")
        if not primary_record or not secondary_record:
            continue

        if primary == secondary:
            blockers.append(f"rubric:reviewers_not_independent:{dimension_id}")

        primary_run = str(primary_record.get("review_run_id", "")).strip()
        secondary_run = str(secondary_record.get("review_run_id", "")).strip()
        if not primary_run or not secondary_run:
            blockers.append(f"rubric:missing_review_run_id:{dimension_id}")
        elif primary_run == secondary_run:
            blockers.append(f"rubric:same_execution_for_both_reviews:{dimension_id}")

        if execution_run_ids is not None:
            if primary_run and primary_run not in execution_run_ids:
                blockers.append(
                    f"rubric:unverified_review_run:{dimension_id}:{primary}"
                )
            if secondary_run and secondary_run not in execution_run_ids:
                blockers.append(
                    f"rubric:unverified_review_run:{dimension_id}:{secondary}"
                )

        records = [primary_record, secondary_record]
        scores: list[float] = []
        for record in records:
            evidence = record.get("evidence_refs") or []
            if not evidence:
                blockers.append(
                    f"rubric:missing_evidence:{dimension_id}:{record.get('reviewer_id')}"
                )
            status = record.get("status")
            if status != "pass":
                blockers.append(
                    f"rubric:review_not_pass:{dimension_id}:{record.get('reviewer_id')}:{status}"
                )
            score = record.get("score")
            if not isinstance(score, (int, float)) or not 0 <= float(score) <= 10:
                blockers.append(
                    f"rubric:invalid_score:{dimension_id}:{record.get('reviewer_id')}"
                )
            else:
                scores.append(float(score))

            for finding in record.get("findings", []):
                if finding.get("severity") == "blocker" and finding.get("status") != "resolved":
                    blockers.append(
                        f"rubric:open_blocker:{dimension_id}:{finding.get('finding_id', 'unknown')}"
                    )

        if len(scores) != 2:
            continue

        dimension_score = round(mean(scores), 3)
        spread = round(abs(scores[0] - scores[1]), 3)
        dimension_scores[dimension_id] = dimension_score
        spreads[dimension_id] = spread
        weighted_parts.append((dimension_score, float(dimension.get("weight", 1))))

        if dimension_score < dimension_min:
            blockers.append(f"rubric:dimension_below_threshold:{dimension_id}")
        if spread > max_spread:
            blockers.append(f"rubric:reviewer_spread_exceeded:{dimension_id}")

    visual = validate_visual_manifest(visual_manifest)
    blockers.extend(visual.issues)

    if readiness_status != "READY":
        blockers.append("rubric:readiness_not_ready")
    if open_material_questions:
        blockers.append("rubric:open_material_questions")
    if unresolved_dissent:
        blockers.append("rubric:unresolved_dissent")
    if missing:
        blockers.extend(f"rubric:missing_review:{item}" for item in missing)

    weight_sum = sum(weight for _, weight in weighted_parts)
    weighted_score = (
        round(sum(score * weight for score, weight in weighted_parts) / weight_sum, 3)
        if weight_sum
        else 0.0
    )
    if weighted_score < weighted_min:
        blockers.append("rubric:weighted_score_below_threshold")

    unique_blockers = tuple(sorted(set(blockers)))
    return RubricEvaluation(
        passed=not unique_blockers,
        weighted_score=weighted_score,
        dimension_scores=dimension_scores,
        reviewer_spread=spreads,
        blockers=unique_blockers,
        missing_reviews=tuple(sorted(set(missing))),
    )
