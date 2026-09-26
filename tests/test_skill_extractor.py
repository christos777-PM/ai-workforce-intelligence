"""Tests for the baseline workforce intelligence pipeline."""
import unittest
from src.skill_extractor import category_frequency, extract_skills, skill_frequency

class TestSkillExtractor(unittest.TestCase):
    def test_extracts_programming_and_cloud(self):
        skills = extract_skills("Build Python services using SQL and AWS.")
        self.assertIn("python", skills["Programming"])
        self.assertIn("sql", skills["Programming"])
        self.assertIn("aws", skills["Cloud"])

    def test_case_insensitive(self):
        skills = extract_skills("PYTHON, AWS and AGILE")
        self.assertIn("python", skills["Programming"])
        self.assertIn("aws", skills["Cloud"])
        self.assertIn("agile", skills["Project Management"])

    def test_skill_frequency(self):
        results = [{"skills":{"Cloud":["aws"],"Programming":["python"]}},
                   {"skills":{"Cloud":["aws"],"Programming":["sql"]}}]
        frequency = skill_frequency(results)
        self.assertEqual(frequency["aws"], 2)

    def test_category_coverage(self):
        results = [{"skills":{"Cloud":["aws"],"AI & ML":["llm"]}},
                   {"skills":{"Cloud":["azure"]}}]
        coverage = category_frequency(results)
        self.assertEqual(coverage["Cloud"], 2)
        self.assertEqual(coverage["AI & ML"], 1)

if __name__ == "__main__":
    unittest.main()
