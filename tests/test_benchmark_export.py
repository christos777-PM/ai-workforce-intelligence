"""Tests for exporting pipeline predictions to the benchmark JSONL schema."""

import unittest

from aw_intelligence.analysis import analyze_roles
from aw_intelligence.benchmark import build_prediction_records


class TestBenchmarkExport(unittest.TestCase):
    def test_generates_stable_ids_and_unique_skill_labels(self):
        rows = [
            {"title": "AI Project Manager", "description": "Python and Python with cloud computing."},
            {"title": "Quantum Systems Lead", "role_id": "qc-lead", "description": "Systems engineering."},
        ]
        records = build_prediction_records(rows, analyze_roles(rows))

        self.assertEqual([record["role_id"] for record in records], ["ai-project-manager", "qc-lead"])
        self.assertEqual(records[0]["predicted_skills"], ["cloud computing", "python"])
        self.assertEqual(records[1]["predicted_skills"], ["systems engineering"])
        self.assertEqual(records[0]["title"], "AI Project Manager")

    def test_rejects_duplicate_generated_identifiers(self):
        rows = [
            {"title": "AI Project Manager", "description": "Python."},
            {"title": "AI Project Manager", "description": "SQL."},
        ]
        with self.assertRaisesRegex(ValueError, "Duplicate role_id"):
            build_prediction_records(rows, analyze_roles(rows))

    def test_rejects_mismatched_row_and_analysis_counts(self):
        rows = [{"title": "AI Project Manager", "description": "Python."}]
        with self.assertRaisesRegex(ValueError, "same length"):
            build_prediction_records(rows, [])

    def test_rejects_blank_titles_without_explicit_ids(self):
        rows = [{"title": "  ", "description": "Python."}]
        with self.assertRaisesRegex(ValueError, "non-empty role_id"):
            build_prediction_records(rows, analyze_roles(rows))


if __name__ == "__main__":
    unittest.main()
