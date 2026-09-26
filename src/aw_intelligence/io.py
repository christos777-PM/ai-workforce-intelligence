"""CSV and JSON input/output helpers."""

from __future__ import annotations

import csv
import json
from pathlib import Path


def read_jobs(path: str | Path) -> list[dict[str, str]]:
    """Read job records from a CSV file."""
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    required = {"title", "description"}
    if not rows or not required.issubset(rows[0].keys()):
        raise ValueError("CSV must contain 'title' and 'description' columns.")
    return rows


def read_target_skills(path: str | Path) -> set[str]:
    """Read a target role definition containing a JSON skills list."""
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    skills = payload.get("skills")
    if not isinstance(skills, list) or not all(isinstance(skill, str) for skill in skills):
        raise ValueError("Target JSON must contain a 'skills' list of strings.")
    return {skill.strip().lower() for skill in skills if skill.strip()}


def write_json(payload: object, path: str | Path) -> None:
    """Write structured analysis output as readable JSON."""
    Path(path).write_text(json.dumps(payload, indent=2), encoding="utf-8")
