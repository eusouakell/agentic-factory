import json
import unittest
from pathlib import Path

from agents.validate_registry import validate_registry

ROOT = Path(__file__).resolve().parents[1]


class AgentRegistryTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / "agents" / "registry.json").read_text(encoding="utf-8"))

    def test_registry_is_valid(self):
        self.assertEqual(validate_registry(self.data, ROOT), [])

    def test_v2_shape(self):
        self.assertEqual(self.data["schema_version"], "2.0")
        self.assertEqual(len(self.data["agents"]), 21)
        self.assertEqual(sum(a["tier"] == "core" for a in self.data["agents"]), 7)
        self.assertEqual(sum(a["tier"] == "on_demand" for a in self.data["agents"]), 14)

    def test_agent_ids_are_unique(self):
        ids = [agent["id"] for agent in self.data["agents"]]
        self.assertEqual(len(ids), len(set(ids)))

    def test_pilot_agents_are_disabled_by_default(self):
        for agent in self.data["agents"]:
            if agent["status"] == "pilot":
                self.assertFalse(agent["enabled_by_default"])

    def test_no_agent_has_direct_main_or_publish_authority(self):
        forbidden = {"main", "publish", "production"}
        self.assertTrue(all(agent["write_authority"] not in forbidden for agent in self.data["agents"]))

    def test_every_agent_has_a_matching_contract(self):
        for agent in self.data["agents"]:
            expected = ROOT / "agents" / "contracts" / f"{agent['id']}.md"
            self.assertEqual(agent["contract"], str(expected.relative_to(ROOT)))
            self.assertTrue(expected.is_file())

    def test_inclusive_role_was_evolved_not_duplicated(self):
        ids = {agent["id"] for agent in self.data["agents"]}
        self.assertIn("inclusive-experience-reviewer", ids)
        self.assertNotIn("inclusive-visual-reviewer", ids)

    def test_core_review_chain_exists(self):
        ids = {agent["id"] for agent in self.data["agents"] if agent["tier"] == "core"}
        expected = {
            "research-synthesist",
            "frontend-engineer",
            "code-reviewer",
            "security-auditor",
            "accessibility-auditor",
            "readiness-evaluator",
            "flame-ui-composer",
        }
        self.assertEqual(ids, expected)


if __name__ == "__main__":
    unittest.main()
