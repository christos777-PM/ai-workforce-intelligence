"""Command-line tests for workforce intelligence features."""

import contextlib
import io
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from aw_intelligence.cli import main


class TestCli(unittest.TestCase):
    def run_cli(self, *args):
        output = io.StringIO()
        with patch("sys.argv", ["workforce-intel", "data/sample_jobs.csv", *args]):
            with contextlib.redirect_stdout(output):
                main()
        return output.getvalue()

    def test_target_ranking_json_is_sorted_and_explained(self):
        output = self.run_cli(
            "--target",
            "data/targets/ai_project_manager.json",
            "--rank-target",
            "--json",
        )
        payload = json.loads(output)

        ranking = payload["role_fit_ranking"]
        self.assertGreater(len(ranking), 0)
        self.assertEqual([item["rank"] for item in ranking], list(range(1, len(ranking) + 1)))
        self.assertEqual(
            [item["coverage_percent"] for item in ranking],
            sorted([item["coverage_percent"] for item in ranking], reverse=True),
        )
        self.assertIn("matched_skills", ranking[0])
        self.assertIn("missing_skills", ranking[0])

    def test_ranking_requires_target(self):
        output = io.StringIO()
        with patch("sys.argv", ["workforce-intel", "data/sample_jobs.csv", "--rank-target"]):
            with contextlib.redirect_stderr(output), self.assertRaises(SystemExit) as raised:
                main()
        self.assertEqual(raised.exception.code, 2)
        self.assertIn("--rank-target requires --target", output.getvalue())

    def test_exports_predictions_as_jsonl_with_stable_role_ids(self):
        with TemporaryDirectory() as directory:
            output_path = Path(directory) / "predictions.jsonl"
            output = self.run_cli("--predictions-jsonl", str(output_path), "--json")
            payload = json.loads(output)
            records = [json.loads(line) for line in output_path.read_text(encoding="utf-8").splitlines()]

        self.assertEqual(payload["roles_analyzed"], 5)
        self.assertEqual(len(records), 5)
        self.assertEqual(records[0]["role_id"], "ai-project-manager")
        self.assertEqual(records[0]["title"], "AI Project Manager")
        self.assertIn("python", records[0]["predicted_skills"])
        self.assertTrue(all(record["role_id"] for record in records))


if __name__ == "__main__":
    unittest.main()
