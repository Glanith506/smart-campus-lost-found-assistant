from __future__ import annotations

from datetime import datetime
from difflib import SequenceMatcher
from typing import Any


def similarity(left: str, right: str) -> float:
    left = (left or "").lower().strip()
    right = (right or "").lower().strip()

    if not left or not right:
        return 0.0

    if left == right:
        return 1.0

    return SequenceMatcher(None, left, right).ratio()


def date_similarity(left: str, right: str) -> float:
    if not left or not right:
        return 0.0

    try:
        first = datetime.strptime(left, "%Y-%m-%d")
        second = datetime.strptime(right, "%Y-%m-%d")
    except ValueError:
        return 0.0

    days = abs((first - second).days)

    if days == 0:
        return 1.0
    if days <= 2:
        return 0.8
    if days <= 7:
        return 0.5
    if days <= 14:
        return 0.2

    return 0.0


def description_similarity(left: str, right: str) -> float:
    left_words = set((left or "").lower().split())
    right_words = set((right or "").lower().split())

    if not left_words or not right_words:
        return 0.0

    return len(left_words & right_words) / len(left_words | right_words)


def match_score(query: dict[str, str], report: dict[str, Any]) -> float:
    score = (
        0.45 * similarity(query.get("item", ""), str(report.get("item", "")))
        + 0.15 * similarity(query.get("color", ""), str(report.get("color", "")))
        + 0.15 * similarity(query.get("location", ""), str(report.get("location", "")))
        + 0.10 * date_similarity(query.get("event_date", ""), str(report.get("event_date", "")))
        + 0.15 * description_similarity(
            query.get("description", ""),
            str(report.get("description", "")),
        )
    )

    return round(score, 3)


def find_matches(
    query: dict[str, str],
    reports: list[dict[str, Any]],
    expected_type: str | None = None,
    minimum_score: float = 0.42,
) -> list[dict[str, Any]]:
    matches: list[dict[str, Any]] = []

    for report in reports:
        if expected_type and report.get("report_type") != expected_type:
            continue

        score = match_score(query, report)

        if score >= minimum_score:
            result = dict(report)
            result["match_score"] = score
            matches.append(result)

    return sorted(matches, key=lambda item: item["match_score"], reverse=True)
