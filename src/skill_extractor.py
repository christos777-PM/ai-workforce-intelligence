"""Basic skill extraction for AI Workforce Intelligence."""

from pathlib import Path
import csv
import re

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
    return {
        category: [skill for skill in skills if skill in normalized]
        for category, skills in SKILL_TAXONOMY.items()
        if any(skill in normalized for skill in skills)
    }

def load_roles(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))

def analyze_roles(path: Path) -> list[dict]:
    analyzed = []
    for role in load_roles(path):
        analyzed.append({
            "role": role["role"],
            "domain": role["domain"],
            "skills": extract_skills(role["job_description"]),
        })
    return analyzed

if __name__ == "__main__":
    project_root = Path(__file__).resolve().parents[1]
    dataset = project_root / "data" / "job_roles.csv"

    for result in analyze_roles(dataset):
        print(f"\n{result['role']} ({result['domain']})")
        for category, skills in result["skills"].items():
            print(f"  {category}: {', '.join(skills)}")
