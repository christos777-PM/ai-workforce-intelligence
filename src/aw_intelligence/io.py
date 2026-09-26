"""CSV input/output helpers."""

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


def write_json(payload: object, path: str | Path) -> None:
    """Write structured analysis output as readable JSON."""
    Path(path).write_text(json.dumps(payload, indent=2), encoding="utf-8")
