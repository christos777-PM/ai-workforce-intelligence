"""Rule-based skill extraction with deterministic, auditable matching."""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass

from .taxonomy import SKILL_ALIASES, SKILL_TAXONOMY


@dataclass(frozen=True)
class SkillMatch:
    skill: str
    category: str
    occurrences: int


def normalize_text(text: str) -> str:
    """Normalize text for case-insensitive matching."""
    text = text.lower().replace("&", " and ")
    return re.sub(r"\s+", " ", text).strip()


def _phrase_spans(text: str, phrase: str) -> list[tuple[int, int]]:
    """Return whole-word/phrase spans, avoiding substring matches."""
    pattern = r"(?<!\w)" + re.escape(phrase.lower()) + r"(?!\w)"
    return [(match.start(), match.end()) for match in re.finditer(pattern, text)]


def extract_skills(text: str) -> list[SkillMatch]:
    """Extract canonical taxonomy skills, including explicitly listed aliases.

    When a specific phrase contains a shorter skill phrase (for example,
    "REST APIs" contains "APIs"), retain the longer match to avoid counting
    the same text span as both a specific and a generic skill.
    """
    normalized = normalize_text(text)
    candidates: list[tuple[int, int, str, str]] = []

    for category, skills in SKILL_TAXONOMY.items():
        for skill in skills:
            phrases = (skill, *SKILL_ALIASES.get(skill, ()))
            for phrase in phrases:
                candidates.extend(
                    (start, end, skill, category)
                    for start, end in _phrase_spans(normalized, phrase)
                )

    selected: list[tuple[int, int, str, str]] = []
    for candidate in candidates:
        start, end, _, _ = candidate
        overlaps_a_longer_phrase = any(
            other_end - other_start > end - start
            and other_start < end
            and start < other_end
            for other_start, other_end, _, _ in candidates
        )
        if not overlaps_a_longer_phrase:
            selected.append(candidate)

    counts = Counter((skill, category) for _, _, skill, category in selected)
    matches = [
        SkillMatch(skill=skill, category=category, occurrences=count)
        for (skill, category), count in counts.items()
    ]
    return sorted(matches, key=lambda item: (-item.occurrences, item.category, item.skill))


def category_counts(matches: list[SkillMatch]) -> Counter[str]:
    """Aggregate extracted skills by capability category."""
    return Counter(match.category for match in matches)


def skill_counts(matches: list[SkillMatch]) -> Counter[str]:
    """Aggregate extracted skills by individual skill."""
    return Counter({match.skill: match.occurrences for match in matches})
