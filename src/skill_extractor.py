"""Skill extraction and role analysis for AI Workforce Intelligence."""
from pathlib import Path
import csv
import re
from collections import Counter

SKILL_TAXONOMY = {
    "Programming": ["python", "c", "c++", "sql"],
    "AI & ML": ["artificial intelligence", "machine learning", "llm"],
    "Cloud": ["aws", "azure", "cloud"],
    "Data & APIs": ["api", "apis", "database", "databases"],
    "Embedded": ["microcontroller", "microcontrollers", "sensors", "embedded systems"],
    "VLSI": ["vlsi", "semiconductor", "verification"],
    "Project Management": ["agile", "project", "roadmap", "stakeholders", "risks"],
    "Systems": ["networking", "hardware-software integration", "debugging", "testing"],
}

def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()

def extract_skills(text: str) -> dict[str, list[str]]:
    normalized = normalize(text)
    results = {}
    for category, skills in SKILL_TAXONOMY.items():
        matches = [skill for skill in skills if skill in normalized]
        if matches:
            results[category] = matches
    return results

def load_roles(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))

def analyze_roles(path: Path) -> list[dict]:
    return [{"role": r["role"], "domain": r["domain"], "skills": extract_skills(r["job_description"])}
            for r in load_roles(path)]

def skill_frequency(results: list[dict]) -> Counter:
    frequency = Counter()
    for result in results:
        for skills in result["skills"].values():
            frequency.update(skills)
    return frequency

def category_frequency(results: list[dict]) -> Counter:
    frequency = Counter()
    for result in results:
        frequency.update(result["skills"].keys())
    return frequency

def print_report(results: list[dict]) -> None:
    for result in results:
        print(f"\n{result['role']} ({result['domain']})")
        for category, skills in result["skills"].items():
            print(f"  {category}: {', '.join(skills)}")
    print("\n=== Skill Frequency ===")
    for skill, count in skill_frequency(results).most_common():
        print(f"{skill}: {count}")
    print("\n=== Capability Coverage ===")
    for category, count in category_frequency(results).most_common():
        print(f"{category}: {count}/{len(results)} roles")

if __name__ == "__main__":
    project_root = Path(__file__).resolve().parents[1]
    results = analyze_roles(project_root / "data" / "job_roles.csv")
    print_report(results)
