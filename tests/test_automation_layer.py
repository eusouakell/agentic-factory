import json
import unittest
from pathlib import Path

from automations.route import route_event
from automations.validate_registry import validate

ROOT = Path(__file__).resolve().parents[1]


class AutomationLayerTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(
            (ROOT / "automations" / "registry.json").read_text(encoding="utf-8")
        )

    def test_registry_valid(self):
        self.assertEqual(validate(self.data), [])

    def test_factory_governance_pr_routes_core_reviewers(self):
        plans = route_event(
            self.data,
            repository="eusouakell/agentic-factory",
            event="pull_request",
            paths=["governance/change-control.md"],
        )
        self.assertEqual(len(plans), 1)
        self.assertIn("code-reviewer", plans[0]["required_agents"])
        self.assertIn("readiness-evaluator", plans[0]["required_agents"])

    def test_unrelated_repo_does_not_match(self):
        plans = route_event(
            self.data,
            repository="eusouakell/eusouakell",
            event="pull_request",
            paths=["README.md"],
        )
        self.assertEqual(plans, [])

    def test_editorial_label_required(self):
        without_label = route_event(
            self.data,
            repository="eusouakell/cereja-editorial-engine",
            event="draft_ready",
            paths=["drafts/031.md"],
            labels=[],
        )
        self.assertEqual(without_label, [])

        with_label = route_event(
            self.data,
            repository="eusouakell/cereja-editorial-engine",
            event="draft_ready",
            paths=["drafts/031.md"],
            labels=["editorial-draft"],
        )
        self.assertEqual(len(with_label), 1)
        self.assertIn("distinctiveness_authorship", with_label[0]["semantic_evals"])


if __name__ == "__main__":
    unittest.main()
