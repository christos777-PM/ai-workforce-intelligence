import unittest

from aw_intelligence.analysis import analyze_roles, coverage_score, frequency_by_category, skill_gap, top_skills
from aw_intelligence.io import read_target_skills


class TestPipeline(unittest.TestCase):
    def test_role_pipeline(self):
        rows = [
            {"title": "AI PM", "description": "Python, machine learning, agile and Jira."},
            {"title": "Cloud PM", "description": "AWS, Python, project management and SQL."},
        ]
        analyses = analyze_roles(rows)
        self.assertEqual(len(analyses), 2)
        self.assertEqual(frequency_by_category(analyses)["Programming"], 2)
        self.assertEqual(top_skills(analyses, 2)[0], ("python", 2))

    def test_target_role_gap(self):
        required = {"python", "sql", "aws"}
        present = {"python", "aws"}
        self.assertEqual(coverage_score(required, present), 66.7)
        self.assertEqual(skill_gap(required, present), {"sql"})

    def test_target_file_loader(self):
        target = read_target_skills("data/targets/ai_project_manager.json")
        self.assertIn("python", target)
        self.assertIn("project management", target)


if __name__ == "__main__":
    unittest.main()
