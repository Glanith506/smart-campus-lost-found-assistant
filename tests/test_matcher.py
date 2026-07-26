from src.matcher import date_similarity, find_matches, match_score


def test_exact_match_scores_high():
    query = {
        "item": "wallet",
        "color": "black",
        "location": "library",
        "event_date": "2026-07-20",
        "description": "black leather wallet",
    }

    report = {
        "id": 1,
        "report_type": "found",
        "item": "wallet",
        "color": "black",
        "location": "library",
        "event_date": "2026-07-20",
        "description": "black leather wallet",
    }

    assert match_score(query, report) == 1.0


def test_find_matches_filters_opposite_type():
    query = {
        "item": "wallet",
        "color": "black",
        "location": "library",
        "event_date": "",
        "description": "",
    }

    reports = [
        {
            "id": 1,
            "report_type": "found",
            "item": "wallet",
            "color": "black",
            "location": "library",
            "event_date": "",
            "description": "",
        },
        {
            "id": 2,
            "report_type": "lost",
            "item": "wallet",
            "color": "black",
            "location": "library",
            "event_date": "",
            "description": "",
        },
    ]

    matches = find_matches(query, reports, expected_type="found")
    assert len(matches) == 1
    assert matches[0]["id"] == 1


def test_nearby_dates_receive_partial_score():
    assert date_similarity("2026-07-20", "2026-07-22") == 0.8
