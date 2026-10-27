"""Skill taxonomy used by the workforce intelligence pipeline."""

from __future__ import annotations

SKILL_TAXONOMY: dict[str, tuple[str, ...]] = {
    "AI & ML": (
        "artificial intelligence", "machine learning", "deep learning",
        "llm", "large language model", "nlp", "generative ai",
    ),
    "Cloud": (
        "aws", "azure", "gcp", "google cloud", "cloud computing",
        "docker", "kubernetes",
    ),
    "Programming": (
        "python", "java", "javascript", "typescript", "c++", "sql",
    ),
    "Data & APIs": (
        "data analysis", "data analytics", "pandas", "api", "rest api",
        "json", "database", "snowflake",
    ),
    "Embedded": (
        "embedded systems", "microcontroller", "firmware", "iot",
        "internet of things",
    ),
    "VLSI": (
        "vlsi", "verilog", "systemverilog", "asic", "fpga",
        "semiconductor",
    ),
    "Project Management": (
        "project management", "program management", "agile", "scrum",
        "jira", "stakeholder management", "risk management",
    ),
    "Systems": (
        "systems engineering", "requirements engineering", "systems thinking",
        "architecture", "technical documentation",
    ),
}

# Common surface forms mapped to the taxonomy's canonical skill label.
# Keep this explicit and auditable rather than applying broad stemming.
SKILL_ALIASES: dict[str, tuple[str, ...]] = {
    "artificial intelligence": ("ai",),
    "llm": ("llms",),
    "large language model": ("large language models",),
    "api": ("apis",),
    "rest api": ("rest apis",),
    "microcontroller": ("microcontrollers",),
    "asic": ("asics",),
    "fpga": ("fpgas",),
    "semiconductor": ("semiconductors",),
}


def all_skills() -> tuple[str, ...]:
    """Return unique skills in deterministic order."""
    return tuple(dict.fromkeys(skill for skills in SKILL_TAXONOMY.values() for skill in skills))
