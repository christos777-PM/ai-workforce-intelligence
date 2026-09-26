"""Command-line interface for workforce intelligence."""

from __future__ import annotations

import argparse
import json

from .analysis import analyze_roles, frequency_by_category, top_skills
from .io import read_jobs


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Analyze skills in technology job descriptions.")
    parser.add_argument("csv", help="CSV with title,description columns")
    parser.add_argument("--top", type=int, default=10, help="Number of top skills to show")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    analyses = analyze_roles(read_jobs(args.csv))
    payload = {
        "roles_analyzed": len(analyses),
        "category_frequency": dict(frequency_by_category(analyses)),
        "top_skills": top_skills(analyses, args.top),
        "roles": [
            {"title": r.title, "skills": [
                {"skill": m.skill, "category": m.category, "occurrences": m.occurrences}
                for m in r.skills
            ]}
            for r in analyses
        ],
    }
    if args.json:
        print(json.dumps(payload, indent=2))
        return

    print(f"Roles analyzed: {payload['roles_analyzed']}")
    print("\nCategory frequency:")
    for category, count in sorted(payload["category_frequency"].items(), key=lambda x: (-x[1], x[0])):
        print(f"  {category}: {count}")
    print("\nTop skills:")
    for skill, count in payload["top_skills"]:
        print(f"  {skill}: {count}")


if __name__ == "__main__":
    main()
