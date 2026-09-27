import unittest

from aw_intelligence.analysis import analyze_roles, coverage_score, skill_gap
from aw_intelligence.io import read_target_skills


class TestTargetRole(unittest.TestCase):
    def test_sample_profile_coverage(self):
        roles = [
            {"title": "AI PM", "description": "machine learning, Python, cloud computing, APIs, agile, Jira, stakeholder management and risk management."},
            {"title": "Cloud PM", "description": "project management, data analytics, APIs, SQL, architecture and stakeholder management."},
            {"title": "Systems PM", "description": "Python, APIs, requirements engineering, Agile and technical documentation."},
            {"title": "AI Product Manager", "description": "generative AI, LLMs, machine learning, data analytics, SQL, REST APIs, agile, Jira and technical documentation."},
        ]
        analyses = analyze_roles(roles)
        present = {match.skill for role in analyses for match in role.skills}
        required = read_target_skills("data/targets/ai_project_manager.json")
        self.assertEqual(coverage_score(required, present), 100.0)
        self.assertEqual(skill_gap(required, present), set())


if __name__ == "__main__":
    unittest.main()
