"""Regression tests for target-role fit analysis."""

import unittest

from aw_intelligence.analysis import analyze_roles
from aw_intelligence.role_fit import rank_role_fit


class TestRoleFit(unittest.TestCase):
    def test_ranks_roles_by_target_coverage(self):
        analyses = analyze_roles(
            [
                {"title": "AI Project Manager", "description": "Python, machine learning, cloud computing, agile."},
                {"title": "Project Coordinator", "description": "Agile and stakeholder management."},
            ]
        )
        required = {"python", "machine learning", "cloud computing", "agile"}

        ranked = rank_role_fit(analyses, required)

        self.assertEqual(ranked[0].title, "AI Project Manager")
        self.assertEqual(ranked[0].coverage_percent, 100.0)
        self.assertEqual(ranked[1].coverage_percent, 25.0)
        self.assertEqual(ranked[1].missing_skills, ("cloud computing", "machine learning", "python"))

    def test_ties_are_deterministic(self):
        analyses = analyze_roles(
            [
                {"title": "Zeta Role", "description": "Python"},
                {"title": "Alpha Role", "description": "Python"},
            ]
        )

        ranked = rank_role_fit(analyses, {"python"})

        self.assertEqual([fit.title for fit in ranked], ["Alpha Role", "Zeta Role"])

    def test_empty_target_has_full_coverage(self):
        analyses = analyze_roles([{"title": "Any Role", "description": "Python"}])

        ranked = rank_role_fit(analyses, set())

        self.assertEqual(ranked[0].coverage_percent, 100.0)
        self.assertEqual(ranked[0].matched_skills, ())
        self.assertEqual(ranked[0].missing_skills, ())


if __name__ == "__main__":
    unittest.main()
