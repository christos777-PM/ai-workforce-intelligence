import unittest

from aw_intelligence.role_fit import rank_role_fit


class TestRoleFit(unittest.TestCase):
    def test_ranks_roles_by_target_coverage(self):
        target = {"python", "sql", "project management"}
        roles = [
            ("Cloud PM", {"python", "sql"}),
            ("AI PM", {"python", "sql", "project management"}),
            ("Analyst", {"python"}),
        ]

        ranked = rank_role_fit(roles, target)

        self.assertEqual(ranked[0].title, "AI PM")
        self.assertEqual(ranked[0].coverage_percent, 100.0)
        self.assertEqual(ranked[1].coverage_percent, 66.7)
        self.assertEqual(ranked[2].coverage_percent, 33.3)

    def test_reports_matched_and_missing_skills(self):
        result = rank_role_fit(
            [("Cloud PM", {"python", "aws"})],
            {"python", "aws", "sql"},
        )[0]

        self.assertEqual(result.matched_skills, ("aws", "python"))
        self.assertEqual(result.missing_skills, ("sql",))

    def test_ties_are_deterministic(self):
        roles = [("Zeta", {"python"}), ("Alpha", {"python"})]
        ranked = rank_role_fit(roles, {"python", "sql"})

        self.assertEqual([role.title for role in ranked], ["Alpha", "Zeta"])


if __name__ == "__main__":
    unittest.main()
