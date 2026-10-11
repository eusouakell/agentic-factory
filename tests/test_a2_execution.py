import json
import sys
import tempfile
import unittest
from pathlib import Path

from automations.executor import (
    BoundedExecutor,
    ExecutionRequest,
    JsonSubprocessAdapter,
    PacketOnlyAdapter,
)
from orchestration.a2 import A2DeliberationEngine, A2Orchestrator
from orchestration.runtime import JsonlEventLog


def workflow():
    return {
        "workflow_id": "a2-test",
        "project_id": "bussola-public-case",
        "repository": "eusouakell/bussola",
        "workflow_type": "web_design",
    }


class JsonSubprocessAdapterTests(unittest.TestCase):
    def adapter(self, tmp):
        return JsonSubprocessAdapter(
            [sys.executable, "tests/fixtures/fake_agent_runner.py"],
            Path(tmp) / "artifacts",
            timeout_seconds=10,
        )

    def executor(self):
        return BoundedExecutor(
            repository_allowlist={"eusouakell/bussola"},
            agent_allowlist={
                "editorial-storyteller",
                "experience-designer",
                "creative-director",
            },
            max_retry_budget=2,
        )

    def test_autonomous_run_is_separate_process_and_persists_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            request = ExecutionRequest(
                run_id="run-a2",
                repository="eusouakell/bussola",
                task_id="review:narrative",
                primary_agent="editorial-storyteller",
                context_refs=("git://candidate",),
                tool_grants=("repository:read",),
                retry_budget=0,
                human_gate="publish",
                agent_contract_ref="agents/contracts/editorial-storyteller.md",
                output_schema_ref="quality/review-output.schema.json",
                task_input={
                    "kind": "quality_review",
                    "dimension_id": "narrative",
                    "reviewer_id": "editorial-storyteller",
                    "evidence_refs": ["artifact://candidate"],
                },
            )
            result = self.executor().execute(request, self.adapter(tmp))
            self.assertEqual(result.status, "completed")
            self.assertTrue(result.execution_id)
            self.assertEqual(result.usage_quality, "exact")
            self.assertEqual(result.usage["total_tokens"], 140)
            local_refs = [Path(ref) for ref in result.artifact_refs if not ref.startswith("artifact://")]
            self.assertTrue(all(path.exists() for path in local_refs))

    def test_agent_cannot_receive_merge_or_publish_authority(self):
        with tempfile.TemporaryDirectory() as tmp:
            request = ExecutionRequest(
                run_id="run-a2",
                repository="eusouakell/bussola",
                task_id="bad",
                primary_agent="editorial-storyteller",
                context_refs=("git://candidate",),
                tool_grants=("repository:merge",),
                retry_budget=0,
                human_gate="publish",
                agent_contract_ref="agents/contracts/editorial-storyteller.md",
                output_schema_ref="quality/review-output.schema.json",
            )
            with self.assertRaises(PermissionError):
                self.executor().execute(request, self.adapter(tmp))

    def test_autonomous_execution_requires_contract_and_output_schema(self):
        with tempfile.TemporaryDirectory() as tmp:
            request = ExecutionRequest(
                run_id="run-a2",
                repository="eusouakell/bussola",
                task_id="review",
                primary_agent="editorial-storyteller",
                context_refs=("git://candidate",),
                tool_grants=("repository:read",),
                retry_budget=0,
                human_gate="publish",
            )
            with self.assertRaises(ValueError):
                self.executor().execute(request, self.adapter(tmp))


class A2OrchestrationTests(unittest.TestCase):
    def make_orchestrator(self, tmp):
        return A2Orchestrator(
            workflow(),
            JsonlEventLog(Path(tmp) / "events.jsonl"),
            BoundedExecutor(
                repository_allowlist={"eusouakell/bussola"},
                agent_allowlist={
                    "editorial-storyteller",
                    "experience-designer",
                    "creative-director",
                },
                max_retry_budget=2,
            ),
            JsonSubprocessAdapter(
                [sys.executable, "tests/fixtures/fake_agent_runner.py"],
                Path(tmp) / "artifacts",
                timeout_seconds=10,
            ),
        )

    def test_independent_reviews_receive_distinct_execution_ids(self):
        with tempfile.TemporaryDirectory() as tmp:
            orchestrator = self.make_orchestrator(tmp)
            first = orchestrator.run_review(
                run_id="run-a2",
                dimension_id="narrative",
                reviewer_id="editorial-storyteller",
                candidate_ref="git://candidate",
                evidence_refs=("artifact://render",),
                context_refs=("git://prd",),
            )
            second = orchestrator.run_review(
                run_id="run-a2",
                dimension_id="narrative",
                reviewer_id="experience-designer",
                candidate_ref="git://candidate",
                evidence_refs=("artifact://render",),
                context_refs=("git://prd",),
            )
            self.assertNotEqual(first["review_run_id"], second["review_run_id"])
            self.assertEqual(first["reviewer_id"], "editorial-storyteller")
            self.assertEqual(second["reviewer_id"], "experience-designer")

            events = [
                json.loads(line)
                for line in (Path(tmp) / "events.jsonl").read_text(encoding="utf-8").splitlines()
            ]
            completed = [e for e in events if e["event_type"] == "agent_execution_completed"]
            self.assertEqual(len(completed), 2)
            self.assertEqual(len({e["metadata"]["execution_id"] for e in completed}), 2)

    def test_deliberation_runs_owner_challenger_and_arbiter_independently(self):
        with tempfile.TemporaryDirectory() as tmp:
            engine = A2DeliberationEngine(self.make_orchestrator(tmp))
            outcome = engine.deliberate(
                run_id="run-a2",
                question_id="visual-proportion",
                question="Are the image proportions coherent with the hierarchy?",
                owner_agent="experience-designer",
                challenger_agent="editorial-storyteller",
                arbiter_agent="creative-director",
                candidate_ref="git://candidate",
                criterion="visual hierarchy",
                evidence_refs=("artifact://desktop",),
                context_refs=("git://prd",),
            )
            ids = {
                outcome.owner_run.execution_id,
                outcome.challenger_run.execution_id,
                outcome.arbiter_run.execution_id,
            }
            self.assertEqual(len(ids), 3)
            self.assertEqual(outcome.decision, "REVISE_OWNER")

    def test_deliberation_rejects_role_collapse(self):
        with tempfile.TemporaryDirectory() as tmp:
            engine = A2DeliberationEngine(self.make_orchestrator(tmp))
            with self.assertRaises(ValueError):
                engine.deliberate(
                    run_id="run-a2",
                    question_id="q",
                    question="Question",
                    owner_agent="experience-designer",
                    challenger_agent="experience-designer",
                    arbiter_agent="creative-director",
                    candidate_ref="git://candidate",
                    criterion="quality",
                    evidence_refs=("artifact://desktop",),
                    context_refs=("git://prd",),
                )


class BackwardsCompatibilityTests(unittest.TestCase):
    def test_packet_only_adapter_remains_non_autonomous(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = BoundedExecutor(
                repository_allowlist={"eusouakell/bussola"},
                agent_allowlist={"creative-director"},
            ).execute(
                ExecutionRequest(
                    run_id="r",
                    repository="eusouakell/bussola",
                    task_id="t",
                    primary_agent="creative-director",
                    context_refs=("git://x",),
                    tool_grants=("repository:read",),
                    retry_budget=0,
                    human_gate=None,
                ),
                PacketOnlyAdapter(Path(tmp)),
            )
            self.assertEqual(result.status, "waiting_external_executor")


if __name__ == "__main__":
    unittest.main()
