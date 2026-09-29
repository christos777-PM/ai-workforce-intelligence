import unittest

from aw_intelligence.analysis import (
    analyze_roles,
    coverage_score,
    frequency_by_category,
    role_fit,
    skill_gap,
    top_skills,
)
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

    def test_role_fit_ranks_and_explains_gap(self):
        rows = [
            {
                "title": "AI Project Manager",
                "description": "Python, machine learning, agile, Jira and project management.",
            },
            {
                "title": "Cloud Analyst",
                "description": "Python, SQL and AWS.",
            },
        ]
        required = {"python", "project management", "agile", "sql"}
        fits = role_fit(analyze_roles(rows), required)

        self.assertEqual([fit.title for fit in fits], ["AI Project Manager", "Cloud Analyst"])
        self.assertEqual(fits[0].coverage_percent, 75.0)
        self.assertEqual(fits[0].missing_skills, ("sql",))
        self.assertEqual(fits[1].coverage_percent, 50.0)
        self.assertEqual(fits[1].missing_skills, ("agile", "project management"))

    def test_role_fit_is_deterministic_on_ties(self):
        rows = [
            {"title": "Zulu Role", "description": "Python"},
            {"title": "Alpha Role", "description": "Python"},
        ]
        fits = role_fit(analyze_roles(rows), {"python", "sql"})
        self.assertEqual([fit.title for fit in fits], ["Alpha Role", "Zulu Role"])


if __name__ == "__main__":
    unittest.main()
