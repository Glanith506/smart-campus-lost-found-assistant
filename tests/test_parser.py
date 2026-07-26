from src.parser import detect_intent, extract_details


def test_detect_lost_intent():
    assert detect_intent("I lost my wallet") == "report_lost"


def test_detect_found_intent():
    assert detect_intent("I found a blue bottle") == "report_found"


def test_extract_details():
    result = extract_details("I found a black wallet in the library")
    assert result["item"] == "wallet"
    assert result["color"] == "black"
    assert result["location"] == "library"
