"""Target-role fit analysis."""

from __future__ import annotations

from dataclasses import dataclass

from .analysis import RoleAnalysis, coverage_score


@dataclass(frozen=True)
class RoleFit:
    """Coverage of one observed role against a target capability profile."""

    title: str
    coverage_percent: float
    matched_skills: tuple[str, ...]
    missing_skills: tuple[str, ...]


def rank_role_fit(
    analyses: list[RoleAnalysis], required: set[str]
) -> list[RoleFit]:
    """Rank observed roles by coverage of a target capability profile."""
    fits: list[RoleFit] = []

    for role in analyses:
        present = {match.skill for match in role.skills}
        fits.append(
            RoleFit(
                title=role.title,
                coverage_percent=coverage_score(required, present),
                matched_skills=tuple(sorted(required & present)),
                missing_skills=tuple(sorted(required - present)),
            )
        )

    return sorted(fits, key=lambda fit: (-fit.coverage_percent, fit.title.lower()))
