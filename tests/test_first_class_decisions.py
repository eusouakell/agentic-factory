import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class FirstClassDecisionTests(unittest.TestCase):
    def setUp(self):
        self.schema = json.loads(
            (ROOT / "control-plane" / "decision-record.schema.json").read_text(encoding="utf-8")
        )
        self.example = json.loads(
            (ROOT / "control-plane" / "decision-record.example.json").read_text(encoding="utf-8")
        )
        self.run_schema = json.loads(
            (ROOT / "control-plane" / "run-envelope.schema.json").read_text(encoding="utf-8")
        )

    def test_decision_schema_has_core_fields(self):
        required = set(self.schema["required"])
        expected = {
            "decision_id",
            "decision_type",
            "title",
            "outcome_ref",
            "decision_owner",
            "governance_profile",
            "inputs",
            "criteria",
            "authority_required",
            "oversight_mode",
            "state",
            "evidence",
            "expected_outcome",
        }
        self.assertTrue(expected.issubset(required))

    def test_example_matches_declared_enums_and_required_fields(self):
        for field in self.schema["required"]:
            self.assertIn(field, self.example)

        oversight_values = set(self.schema["properties"]["oversight_mode"]["enum"])
        state_values = set(self.schema["properties"]["state"]["enum"])
        reversibility_values = set(
            self.schema["properties"]["governance_profile"]["properties"]["reversibility"]["enum"]
        )

        self.assertIn(self.example["oversight_mode"], oversight_values)
        self.assertIn(self.example["state"], state_values)
        self.assertIn(
            self.example["governance_profile"]["reversibility"],
            reversibility_values,
        )

        for score in ("business_value", "risk", "frequency"):
            value = self.example["governance_profile"][score]
            self.assertGreaterEqual(value, 1)
            self.assertLessEqual(value, 5)

    def test_run_envelope_can_reference_decision(self):
        decision_ref = self.run_schema["properties"].get("decision_ref")
        self.assertIsNotNone(decision_ref)
        self.assertIn("string", decision_ref["type"])
        self.assertIn("null", decision_ref["type"])

    def test_exception_based_modes_have_documented_exception_conditions(self):
        text = (ROOT / "governance" / "first-class-decisions.md").read_text(encoding="utf-8")
        self.assertIn("exception condition", text.lower())
        self.assertIn("human_on_exception", text)
        self.assertIn("autonomous_bounded", text)


if __name__ == "__main__":
    unittest.main()
