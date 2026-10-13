import json
import os
import subprocess
import sys
import unittest
from pathlib import Path


class OpenAIResponsesRunnerTests(unittest.TestCase):
    def test_runner_blocks_cleanly_without_api_key(self):
        packet = {
            "execution_id": "exec_test",
            "run_id": "run_test",
            "repository": "eusouakell/agentic-factory",
            "task_id": "review",
            "primary_agent": "code-reviewer",
            "agent_contract_ref": "agents/contracts/code-reviewer.md",
            "output_schema_ref": "quality/review-output.schema.json",
            "context_refs": ["README.md"],
            "tool_grants": ["repository:read"],
            "retry_budget": 0,
            "human_gate": "merge",
            "task_input": {"kind": "quality_review"},
        }
        env = os.environ.copy()
        env.pop("OPENAI_API_KEY", None)
        proc = subprocess.run(
            [sys.executable, "execution-surfaces/openai_responses_runner.py"],
            input=json.dumps(packet),
            text=True,
            capture_output=True,
            env=env,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        result = json.loads(proc.stdout)
        self.assertEqual(result["status"], "blocked")
        self.assertEqual(result["usage_quality"], "unavailable")
        self.assertTrue(any("OPENAI_API_KEY" in item for item in result["uncertainty"]))


if __name__ == "__main__":
    unittest.main()
