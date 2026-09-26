"""Rule-based skill extraction with deterministic, auditable matching."""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass

from .taxonomy import SKILL_TAXONOMY


@dataclass(frozen=True)
class SkillMatch:
    skill: str
    category: str
    occurrences: int


def normalize_text(text: str) -> str:
    """Normalize text for case-insensitive matching."""
    text = text.lower().replace("&", " and ")
    return re.sub(r"\s+", " ", text).strip()


def _count_phrase(text: str, phrase: str) -> int:
    """Count whole-word/phrase occurrences without matching substrings."""
    pattern = r"(?<!\w)" + re.escape(phrase.lower()) + r"(?!\w)"
    return len(re.findall(pattern, text))


def extract_skills(text: str) -> list[SkillMatch]:
    """Extract taxonomy skills from a job description."""
    normalized = normalize_text(text)
    matches: list[SkillMatch] = []

    for category, skills in SKILL_TAXONOMY.items():
        for skill in skills:
            count = _count_phrase(normalized, skill)
            if count:
                matches.append(SkillMatch(skill, category, count))

    return sorted(matches, key=lambda item: (-item.occurrences, item.category, item.skill))


def category_counts(matches: list[SkillMatch]) -> Counter[str]:
    """Aggregate extracted skills by capability category."""
    return Counter(match.category for match in matches)


def skill_counts(matches: list[SkillMatch]) -> Counter[str]:
    """Aggregate extracted skills by individual skill."""
    return Counter({match.skill: match.occurrences for match in matches})
