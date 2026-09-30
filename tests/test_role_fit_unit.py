import unittest

from aw_intelligence.analysis import analyze_roles
from aw_intelligence.role_fit import rank_role_fit


class RoleFitTests(unittest.TestCase):
    def test_best_role_has_full_coverage(self):
        rows = [{"title": "AI PM", "description": "Python, machine learning, project management."}]
        fits = rank_role_fit(analyze_roles(rows), {"python", "machine learning", "project management"})
        self.assertEqual(fits[0].coverage_percent, 100.0)

    def test_missing_skill_is_reported(self):
        rows = [{"title": "Cloud PM", "description": "Python, SQL, project management."}]
        fits = rank_role_fit(analyze_roles(rows), {"python", "machine learning", "project management"})
        self.assertEqual(fits[0].missing_skills, ("machine learning",))


if __name__ == "__main__":
    unittest.main()
