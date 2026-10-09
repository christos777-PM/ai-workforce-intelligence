"""Target-role fit analysis for observed workforce roles."""

from __future__ import annotations

from dataclasses import dataclass

from .analysis import RoleAnalysis, coverage_score


@dataclass(frozen=True)
class RoleFit:
    """Transparent fit summary for one observed role."""

    title: str
    coverage_percent: float
    matched_skills: tuple[str, ...]
    missing_skills: tuple[str, ...]


def rank_role_fit(
    roles: list[RoleAnalysis],
    required_skills: set[str],
) -> list[RoleFit]:
    """Rank observed roles against a target capability profile.

    Coverage is the percentage of required target skills detected in each
    role description. It is a descriptive workforce-planning signal, not a
    measure of individual competence or suitability for employment.
    """
    results: list[RoleFit] = []

    for role in roles:
        observed_skills = {match.skill for match in role.skills}
        matched = tuple(sorted(required_skills & observed_skills))
        missing = tuple(sorted(required_skills - observed_skills))
        results.append(
            RoleFit(
                title=role.title,
                coverage_percent=coverage_score(required_skills, observed_skills),
                matched_skills=matched,
                missing_skills=missing,
            )
        )

    return sorted(results, key=lambda item: (-item.coverage_percent, item.title.casefold()))
