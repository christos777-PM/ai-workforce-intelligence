"""Export deterministic extractor predictions for benchmark evaluation."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .analysis import RoleAnalysis


def build_prediction_records(
    rows: list[dict[str, str]],
    analyses: list[RoleAnalysis],
) -> list[dict[str, Any]]:
    """Build evaluator-compatible JSONL records with stable role identifiers.

    A supplied non-empty role_id column takes precedence. Otherwise the
    identifier is a slug of the role title. Duplicate identifiers are rejected
    rather than silently assigning order-dependent IDs.
    """
    if len(rows) != len(analyses):
        raise ValueError("Input rows and role analyses must have the same length.")

    records: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for row, analysis in zip(rows, analyses):
        title = row.get("title", "").strip()
        supplied_id = row.get("role_id", "").strip()
        identifier_source = supplied_id or title.casefold()
        role_id = re.sub(r"[^a-z0-9]+", "-", identifier_source.casefold()).strip("-")
        if not role_id:
            raise ValueError("Each role needs a non-empty role_id or a title that can form one.")
        if role_id in seen_ids:
            raise ValueError(
                f"Duplicate role_id {role_id!r}; provide unique values in the CSV role_id column."
            )
        seen_ids.add(role_id)

        records.append(
            {
                "role_id": role_id,
                "title": title,
                "predicted_skills": sorted({match.skill for match in analysis.skills}),
            }
        )
    return records


def write_predictions_jsonl(
    rows: list[dict[str, str]],
    analyses: list[RoleAnalysis],
    path: str | Path,
) -> None:
    """Write one evaluator-compatible prediction object per line."""
    records = build_prediction_records(rows, analyses)
    rendered = "".join(
        json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n"
        for record in records
    )
    Path(path).write_text(rendered, encoding="utf-8")
