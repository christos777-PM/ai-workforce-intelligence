import unittest

from aw_intelligence.extractor import extract_skills, normalize_text
from aw_intelligence.analysis import coverage_score, skill_gap


class TestExtractor(unittest.TestCase):
    def test_normalize_text(self):
        self.assertEqual(normalize_text("Python   AND  AWS"), "python and aws")

    def test_extracts_categories_and_counts(self):
        matches = extract_skills("Python and Python are used with AWS and project management.")
        result = {(m.skill, m.category, m.occurrences) for m in matches}
        self.assertIn(("python", "Programming", 2), result)
        self.assertIn(("aws", "Cloud", 1), result)
        self.assertIn(("project management", "Project Management", 1), result)

    def test_does_not_match_substrings(self):
        matches = extract_skills("A pythonic workflow uses javascript.")
        self.assertEqual([m.skill for m in matches], ["javascript"])

    def test_plural_aliases_map_to_canonical_labels(self):
        matches = extract_skills(
            "APIs, LLMs, microcontrollers, FPGAs, ASICs, and semiconductors."
        )
        result = {match.skill for match in matches}
        self.assertEqual(
            result,
            {"api", "llm", "microcontroller", "fpga", "asic", "semiconductor"},
        )

    def test_specific_rest_api_match_suppresses_overlapping_generic_api(self):
        matches = extract_skills("The service exposes REST APIs and APIs.")
        counts = {match.skill: match.occurrences for match in matches}
        self.assertEqual(counts["rest api"], 1)
        self.assertEqual(counts["api"], 1)

    def test_singular_and_plural_forms_share_one_count(self):
        matches = extract_skills("An API and several APIs are documented.")
        counts = {match.skill: match.occurrences for match in matches}
        self.assertEqual(counts["api"], 2)

    def test_gap_and_coverage(self):
        required = {"python", "sql", "aws"}
        present = {"python", "aws"}
        self.assertEqual(skill_gap(required, present), {"sql"})
        self.assertEqual(coverage_score(required, present), 66.7)


if __name__ == "__main__":
    unittest.main()
