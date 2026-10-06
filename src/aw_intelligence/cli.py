"""Command-line interface for workforce intelligence."""

from __future__ import annotations

import argparse
import json

from .analysis import analyze_roles, coverage_score, frequency_by_category, skill_gap, top_skills
from .io import read_jobs, read_target_skills
from .role_fit import rank_role_fit


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Analyze skills in technology job descriptions.")
    parser.add_argument("csv", help="CSV with title,description columns")
    parser.add_argument("--top", type=int, default=10, help="Number of top skills to show")
    parser.add_argument("--target", help="JSON file defining skills for a target role")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    analyses = analyze_roles(read_jobs(args.csv))
    observed_skills = {match.skill for role in analyses for match in role.skills}
    payload = {
        "roles_analyzed": len(analyses),
        "category_frequency": dict(frequency_by_category(analyses)),
        "top_skills": top_skills(analyses, args.top),
        "roles": [
            {
                "title": role.title,
                "skills": [
                    {"skill": match.skill, "category": match.category, "occurrences": match.occurrences}
                    for match in role.skills
                ],
            }
            for role in analyses
        ],
    }

    if args.target:
        required = read_target_skills(args.target)
        payload["target_role"] = {
            "required_skills": sorted(required),
            "coverage_percent": coverage_score(required, observed_skills),
            "skills_gap": sorted(skill_gap(required, observed_skills)),
        }

    if args.json:
        print(json.dumps(payload, indent=2))
        return

    print(f"Roles analyzed: {payload['roles_analyzed']}")
    print("\nCategory frequency:")
    for category, count in sorted(payload["category_frequency"].items(), key=lambda item: (-item[1], item[0])):
        print(f"  {category}: {count}")
    print("\nTop skills:")
    for skill, count in payload["top_skills"]:
        print(f"  {skill}: {count}")

    if "target_role" in payload:
        target = payload["target_role"]
        print(f"\nTarget-role coverage: {target['coverage_percent']}%")
        print("Skills gap:")
        for skill in target["skills_gap"]:
            print(f"  - {skill}")


if __name__ == "__main__":
    main()
