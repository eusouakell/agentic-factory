import json
import tempfile
import unittest
from pathlib import Path

from automations.executor import BoundedExecutor, ExecutionRequest, PacketOnlyAdapter
from orchestration.deliberation import DeliberationRuntime
from orchestration.runtime import JsonlEventLog
from quality.reviews import evaluate_publish_readiness
from quality.visual_evidence import validate_visual_manifest


def load_rubric():
    return json.loads(
        Path("quality/rubrics/editorial-web-publish-ready-v1.json").read_text(encoding="utf-8")
    )


def workflow():
    return {
        "workflow_id": "bussola-v2-test",
        "project_id": "bussola-public-case",
        "repository": "eusouakell/bussola",
        "workflow_type": "web_design",
        "max_stage_rounds": 3,
        "max_same_blocker_attempts": 2,
    }


def complete_reviews(rubric):
    reviews = []
    seq = 0
    for dimension in rubric["dimensions"]:
        if dimension.get("applies_if"):
            continue
        for reviewer in [dimension["primary_reviewer"], dimension["secondary_reviewer"]]:
            seq += 1
            reviews.append(
                {
                    "dimension_id": dimension["id"],
                    "reviewer_id": reviewer,
                    "review_run_id": f"review-run-{seq}",
                    "score": 9.6,
                    "status": "pass",
                    "evidence_refs": [f"artifact://review/{seq}"],
                    "findings": [],
                }
            )
    return reviews


def visual_manifest():
    captures = []
    idx = 0
    for viewport in [1440, 390, 320]:
        for section in ["hero", "discovery", "evolution", "team"]:
            idx += 1
            captures.append(
                {
                    "viewport_width": viewport,
                    "section_id": section,
                    "dom_anchor": section,
                    "artifact_ref": f"artifact://capture/{viewport}/{section}",
                    "content_sha256": f"{idx:064x}",
                    "observed_heading": f"Heading {section}",
                    "reviewer_id": "visual-qa-reviewer",
                    "review_run_id": f"visual-review-{viewport}-{section}",
                    "status": "pass",
                }
            )
    return {
        "candidate_ref": "git://candidate",
        "required_viewports": [1440, 390, 320],
        "required_sections": ["hero", "discovery", "evolution", "team"],
        "captures": captures,
    }


class DeliberationRuntimeTests(unittest.TestCase):
    def test_owner_challenger_resolution_emits_internal_resolution(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "events.jsonl"
            runtime = DeliberationRuntime(
                workflow(),
                JsonlEventLog(path),
                run_id="run-test",
            )
            issue = runtime.create_issue(
                issue_id="visual-1",
                stage_id="art-direction",
                question="Are the image proportions coherent?",
                issue_class="visual",
                raised_by="creative-director",
                owner="editorial-art-director",
                severity="blocker",
                root_cause="image-proportion",
                round_number=1,
                evidence_refs=["artifact://desktop"],
                proposed_resolution="Rebalance person/product scale.",
                arbiter="creative-director",
            )
            self.assertEqual(issue.status, "open")
            runtime.owner_respond(
                "visual-1",
                decision="accept",
                rationale="The evidence shows the human figure dominates the product surface.",
                artifact_refs=["artifact://revision"],
            )
            runtime.challenger_rereview(
                "visual-1",
                resolved=True,
                rationale="Revised composition resolves the proportion issue.",
            )
            self.assertEqual(runtime.open_material_issues(), [])
            self.assertEqual(runtime.internal_resolution_rate(), 1.0)
            event_types = [
                json.loads(line)["event_type"]
                for line in path.read_text(encoding="utf-8").splitlines()
            ]
            self.assertIn("convergence_issue_created", event_types)
            self.assertIn("convergence_issue_resolved", event_types)
            self.assertNotIn("human_escalation_opened", event_types)

    def test_same_root_cause_budget_exhaustion_escalates(self):
        with tempfile.TemporaryDirectory() as tmp:
            runtime = DeliberationRuntime(
                workflow(),
                JsonlEventLog(Path(tmp) / "events.jsonl"),
                run_id="run-test",
            )
            for idx in [1, 2]:
                issue = runtime.create_issue(
                    issue_id=f"visual-{idx}",
                    stage_id="art-direction",
                    question="Still distorted?",
                    issue_class="visual",
                    raised_by="creative-director",
                    owner="editorial-art-director",
                    severity="blocker",
                    root_cause="image-proportion",
                    round_number=idx,
                    arbiter="creative-director",
                )
                self.assertEqual(issue.status, "open")
            third = runtime.create_issue(
                issue_id="visual-3",
                stage_id="art-direction",
                question="Still distorted after two revisions?",
                issue_class="visual",
                raised_by="creative-director",
                owner="editorial-art-director",
                severity="blocker",
                root_cause="image-proportion",
                round_number=3,
                arbiter="creative-director",
            )
            self.assertEqual(third.status, "human_escalation")


class PublishReadinessTests(unittest.TestCase):
    def test_complete_independent_reviews_and_visual_evidence_pass(self):
        rubric = load_rubric()
        result = evaluate_publish_readiness(
            rubric,
            complete_reviews(rubric),
            visual_manifest=visual_manifest(),
            readiness_status="READY",
        )
        self.assertTrue(result.passed)
        self.assertGreaterEqual(result.weighted_score, 9.2)

    def test_same_execution_cannot_self_certify_both_reviewer_roles(self):
        rubric = load_rubric()
        reviews = complete_reviews(rubric)
        narrative = [r for r in reviews if r["dimension_id"] == "narrative"]
        narrative[1]["review_run_id"] = narrative[0]["review_run_id"]
        result = evaluate_publish_readiness(
            rubric,
            reviews,
            visual_manifest=visual_manifest(),
            readiness_status="READY",
        )
        self.assertFalse(result.passed)
        self.assertIn("rubric:same_execution_for_both_reviews:narrative", result.blockers)

    def test_review_run_must_match_executed_specialist_when_provenance_is_supplied(self):
        rubric = load_rubric()
        reviews = complete_reviews(rubric)
        allowed = {review["review_run_id"] for review in reviews}
        missing_id = reviews[0]["review_run_id"]
        allowed.remove(missing_id)
        result = evaluate_publish_readiness(
            rubric,
            reviews,
            visual_manifest=visual_manifest(),
            readiness_status="READY",
            execution_run_ids=allowed,
        )
        self.assertFalse(result.passed)
        self.assertTrue(
            any(
                blocker.startswith("rubric:unverified_review_run:")
                for blocker in result.blockers
            )
        )

    def test_duplicate_visual_content_under_different_section_labels_fails(self):
        manifest = visual_manifest()
        captures = [
            c for c in manifest["captures"] if c["viewport_width"] == 1440
        ]
        captures[1]["content_sha256"] = captures[0]["content_sha256"]
        result = validate_visual_manifest(manifest)
        self.assertFalse(result.passed)
        self.assertTrue(
            any("duplicate_capture_hash" in issue for issue in result.issues)
        )

    def test_missing_viewport_capture_blocks_publish_ready(self):
        rubric = load_rubric()
        manifest = visual_manifest()
        manifest["captures"] = [
            capture
            for capture in manifest["captures"]
            if not (
                capture["viewport_width"] == 320
                and capture["section_id"] == "team"
            )
        ]
        result = evaluate_publish_readiness(
            rubric,
            complete_reviews(rubric),
            visual_manifest=manifest,
            readiness_status="READY",
        )
        self.assertFalse(result.passed)
        self.assertIn("visual_manifest:320:team:missing_capture", result.blockers)


class BoundedExecutorTests(unittest.TestCase):
    def test_packet_adapter_does_not_claim_a2_completion(self):
        with tempfile.TemporaryDirectory() as tmp:
            executor = BoundedExecutor(
                repository_allowlist={"eusouakell/bussola"},
                agent_allowlist={"creative-director"},
                max_retry_budget=2,
            )
            request = ExecutionRequest(
                run_id="run-1",
                repository="eusouakell/bussola",
                task_id="review",
                primary_agent="creative-director",
                context_refs=("git://prd",),
                tool_grants=("repository:read",),
                retry_budget=1,
                human_gate="publish",
            )
            result = executor.execute(request, PacketOnlyAdapter(Path(tmp)))
            self.assertEqual(result.status, "waiting_external_executor")
            self.assertEqual(result.execution_surface, "packet-only")

    def test_executor_rejects_non_allowlisted_repository(self):
        with tempfile.TemporaryDirectory() as tmp:
            executor = BoundedExecutor(
                repository_allowlist={"eusouakell/bussola"},
                agent_allowlist={"creative-director"},
            )
            request = ExecutionRequest(
                run_id="run-1",
                repository="evil/other",
                task_id="review",
                primary_agent="creative-director",
                context_refs=("git://prd",),
                tool_grants=("repository:read",),
                retry_budget=0,
                human_gate=None,
            )
            with self.assertRaises(PermissionError):
                executor.execute(request, PacketOnlyAdapter(Path(tmp)))


if __name__ == "__main__":
    unittest.main()
