import unittest

from aw_intelligence.analysis import analyze_roles, frequency_by_category, top_skills


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


if __name__ == "__main__":
    unittest.main()
