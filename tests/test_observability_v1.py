import json
import tempfile
import unittest
from pathlib import Path

from observability.dashboard import render_dashboard
from observability.metrics import summarize_portfolio, summarize_run
from orchestration.runtime import JsonlEventLog, WorkflowRuntime
from quality.gates import evaluate_gate


class FakeClock:
    def __init__(self):
        self.values = iter(
            [
                "2026-10-10T10:00:00+00:00",
                "2026-10-10T10:00:01+00:00",
                "2026-10-10T10:00:02+00:00",
                "2026-10-10T10:00:03+00:00",
                "2026-10-10T10:00:13+00:00",
                "2026-10-10T10:00:14+00:00",
                "2026-10-10T10:00:15+00:00",
                "2026-10-10T10:00:25+00:00",
                "2026-10-10T10:00:26+00:00",
                "2026-10-10T10:00:36+00:00",
                "2026-10-10T10:00:37+00:00",
                "2026-10-10T10:00:47+00:00",
                "2026-10-10T10:00:48+00:00",
                "2026-10-10T10:00:49+00:00",
                "2026-10-10T10:00:50+00:00",
            ]
        )

    def __call__(self):
        return next(self.values)


def read_events(path: Path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


class QualityGateTests(unittest.TestCase):
    def test_blocker_unknown_prevents_gate(self):
        items = [
            {"check_id": "a", "severity": "blocker"},
            {"check_id": "b", "severity": "advisory"},
        ]
        result = evaluate_gate("g1", items, {"b": {"status": "pass"}})
        self.assertFalse(result.passed)
        self.assertEqual(result.unknown_blockers, ("a",))

    def test_override_requires_reason(self):
        with self.assertRaises(ValueError):
            evaluate_gate(
                "g1",
                [{"check_id": "a", "severity": "blocker"}],
                {"a": {"status": "fail"}},
                override=True,
            )

        result = evaluate_gate(
            "g1",
            [{"check_id": "a", "severity": "blocker"}],
            {"a": {"status": "fail"}},
            override=True,
            override_reason="Human accepts residual risk",
        )
        self.assertTrue(result.passed)
        self.assertTrue(result.overridden)


class RuntimeAndMetricsTests(unittest.TestCase):
    def workflow(self, project="bussola-public-case", repo="eusouakell/bussola"):
        return {
            "workflow_id": f"{project}-v1",
            "project_id": project,
            "repository": repo,
            "workflow_type": "web_design",
            "target_period": "pilot-v1",
            "tasks": [
                {
                    "task_id": "direction",
                    "agent_id": "editorial-art-director",
                    "sizing_points": 3,
                    "planning_origin": "planned",
                    "retry_budget": 1,
                    "depends_on": [],
                }
            ],
        }

    def test_runtime_records_baseline_retry_wait_and_usage(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "events.jsonl"
            runtime = WorkflowRuntime(
                self.workflow(),
                JsonlEventLog(path),
                clock=FakeClock(),
            )
            runtime.create()
            runtime.start_task("direction")
            runtime.complete_task("direction", ["artifact://v1"])
            runtime.retry_task("direction", "Creative preflight requested revision")
            runtime.start_task("direction")
            runtime.complete_task("direction", ["artifact://v2"])
            runtime.open_human_gate("direction")
            runtime.resolve_human_gate("direction", "approve")
            runtime.record_usage(
                "direction",
                input_tokens=100,
                output_tokens=50,
                total_tokens=150,
                usage_quality="exact",
            )
            runtime.accept_artifact("direction", "artifact://v2")
            runtime.complete_workflow()

            events = read_events(path)
            summary = summarize_run(events)

            self.assertEqual(summary["committed_points"], 3)
            self.assertEqual(summary["accepted_planned_points"], 3)
            self.assertEqual(summary["remaining_planned_points"], 0)
            self.assertEqual(summary["spillover_points"], 0)
            self.assertEqual(summary["retries"], 1)
            self.assertGreater(summary["rework_seconds"], 0)
            self.assertGreater(summary["human_wait_seconds"], 0)
            self.assertEqual(summary["usage"]["total_tokens"], 150)
            self.assertEqual(summary["usage_quality"], "exact")

    def test_in_progress_work_is_remaining_not_spillover(self):
        events = [
            {
                "event_id": "1",
                "workflow_id": "w",
                "project_id": "p",
                "repository": "o/r",
                "workflow_type": "x",
                "run_id": "r",
                "task_id": None,
                "agent_id": None,
                "event_type": "workflow_created",
                "timestamp": "2026-10-10T10:00:00+00:00",
                "execution_surface": "codex",
                "artifact_refs": [],
                "metadata": {},
            },
            {
                "event_id": "2",
                "workflow_id": "w",
                "project_id": "p",
                "repository": "o/r",
                "workflow_type": "x",
                "run_id": "r",
                "task_id": "t",
                "agent_id": "a",
                "event_type": "task_planned",
                "timestamp": "2026-10-10T10:00:01+00:00",
                "execution_surface": "codex",
                "artifact_refs": [],
                "metadata": {"sizing_points": 5, "baseline_points": 5, "planning_origin": "planned"},
            },
        ]
        summary = summarize_run(events)
        self.assertEqual(summary["remaining_planned_points"], 5)
        self.assertEqual(summary["spillover_points"], 0)

    def test_point_sizing_is_not_converted_to_hours(self):
        events = [
            {
                "event_id": "1",
                "workflow_id": "w",
                "project_id": "p",
                "repository": "o/r",
                "workflow_type": "x",
                "run_id": "r",
                "task_id": None,
                "agent_id": None,
                "event_type": "workflow_created",
                "timestamp": "2026-10-10T10:00:00+00:00",
                "execution_surface": "codex",
                "artifact_refs": [],
                "metadata": {},
            },
            {
                "event_id": "2",
                "workflow_id": "w",
                "project_id": "p",
                "repository": "o/r",
                "workflow_type": "x",
                "run_id": "r",
                "task_id": "t",
                "agent_id": "a",
                "event_type": "task_planned",
                "timestamp": "2026-10-10T10:00:01+00:00",
                "execution_surface": "codex",
                "artifact_refs": [],
                "metadata": {"sizing_points": 5, "baseline_points": 5, "planning_origin": "planned"},
            },
        ]
        summary = summarize_run(events)
        self.assertEqual(summary["committed_points"], 5)
        self.assertNotIn("planned_hours", summary)
        self.assertNotIn("hours_per_point", summary)

    def test_portfolio_keeps_projects_as_filter_dimension(self):
        base = {
            "event_id": "1",
            "workflow_type": "editorial",
            "task_id": None,
            "agent_id": None,
            "event_type": "workflow_created",
            "timestamp": "2026-10-10T10:00:00+00:00",
            "execution_surface": "codex",
            "artifact_refs": [],
            "metadata": {},
        }
        events = [
            {**base, "workflow_id": "w1", "project_id": "bussola", "repository": "eusouakell/bussola", "run_id": "r1"},
            {**base, "event_id": "2", "workflow_id": "w2", "project_id": "cereja", "repository": "eusouakell/cereja-editorial-engine", "run_id": "r2"},
        ]
        portfolio = summarize_portfolio(events)
        self.assertEqual(portfolio["summary"]["workflow_count"], 2)
        self.assertEqual({run["project_id"] for run in portfolio["runs"]}, {"bussola", "cereja"})

        page = render_dashboard(portfolio)
        self.assertIn("Todos os projetos", page)
        self.assertIn("bussola", page)
        self.assertIn("cereja", page)


if __name__ == "__main__":
    unittest.main()
