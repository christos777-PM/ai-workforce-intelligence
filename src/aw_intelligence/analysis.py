"""Workforce analysis utilities."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from .extractor import SkillMatch, extract_skills


@dataclass(frozen=True)
class RoleAnalysis:
    title: str
    skills: tuple[SkillMatch, ...]


@dataclass(frozen=True)
class RoleFit:
    """Coverage of a single observed role against a target skill set."""

    title: str
    coverage_percent: float
    matched_skills: tuple[str, ...]
    missing_skills: tuple[str, ...]


def analyze_roles(rows: list[dict[str, str]]) -> list[RoleAnalysis]:
    """Extract skills from rows containing title and description fields."""
    return [
        RoleAnalysis(
            title=row.get("title", "").strip(),
            skills=tuple(extract_skills(row.get("description", ""))),
        )
        for row in rows
    ]


def frequency_by_category(analyses: list[RoleAnalysis]) -> Counter[str]:
    """Count roles requiring each capability category."""
    counts: Counter[str] = Counter()
    for role in analyses:
        counts.update({category: 1 for category in {m.category for m in role.skills}})
    return counts


def top_skills(analyses: list[RoleAnalysis], limit: int = 10) -> list[tuple[str, int]]:
    """Return the most frequently observed skills across roles."""
    counts: Counter[str] = Counter()
    for role in analyses:
        counts.update({m.skill: 1 for m in role.skills})
    return counts.most_common(limit)


def coverage_score(required: set[str], present: set[str]) -> float:
    """Return percentage coverage of a required skill set."""
    if not required:
        return 100.0
    return round(100 * len(required & present) / len(required), 1)


def skill_gap(required: set[str], present: set[str]) -> set[str]:
    """Return required skills absent from the observed capability set."""
    return required - present


def role_fit(analyses: list[RoleAnalysis], required: set[str]) -> list[RoleFit]:
    """Rank observed roles by coverage of a target capability profile."""
    fits = []
    for role in analyses:
        present = {match.skill for match in role.skills}
        matched = tuple(sorted(required & present))
        missing = tuple(sorted(required - present))
        fits.append(
            RoleFit(
                title=role.title,
                coverage_percent=coverage_score(required, present),
                matched_skills=matched,
                missing_skills=missing,
            )
        )
    return sorted(fits, key=lambda fit: (-fit.coverage_percent, fit.title.lower()))
