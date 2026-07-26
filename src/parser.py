from __future__ import annotations

import re

ITEMS = {
    "wallet", "phone", "mobile", "laptop", "bag", "backpack", "bottle",
    "umbrella", "watch", "keys", "key", "card", "id", "passport",
    "charger", "headphones", "earbuds", "book", "notebook", "jacket",
    "coat", "glasses", "ring", "bracelet", "purse", "tablet", "camera",
    "calculator", "pen", "folder",
}

COLORS = {
    "black", "white", "blue", "red", "green", "yellow", "brown", "grey",
    "gray", "pink", "purple", "orange", "silver", "gold", "beige",
}

LOCATIONS = {
    "library", "cafeteria", "canteen", "classroom", "lab", "laboratory",
    "reception", "parking", "bus stop", "hall", "auditorium", "gym",
    "hostel", "dorm", "office", "campus", "washroom", "toilet",
    "seminar room", "computer room", "sports ground", "main gate",
}

ALIASES = {
    "mobile": "phone",
    "key": "keys",
    "gray": "grey",
    "canteen": "cafeteria",
    "laboratory": "lab",
    "dorm": "hostel",
}


def detect_intent(message: str) -> str:
    text = message.lower()

    if any(phrase in text for phrase in ["show reports", "list reports", "all reports"]):
        return "list"

    if any(phrase in text for phrase in ["found", "picked up", "discovered"]):
        return "report_found"

    if any(phrase in text for phrase in ["lost", "missing", "cannot find", "can't find"]):
        return "report_lost"

    if any(phrase in text for phrase in ["search", "match", "check", "look for"]):
        return "search"

    if any(phrase in text for phrase in ["help", "commands", "what can you do"]):
        return "help"

    return "unknown"


def _first_match(words: set[str], text: str) -> str:
    for word in sorted(words, key=len, reverse=True):
        if re.search(rf"\b{re.escape(word)}\b", text):
            return word
    return ""


def extract_details(message: str) -> dict[str, str]:
    text = message.lower()

    item = _first_match(ITEMS, text)
    color = _first_match(COLORS, text)
    location = _first_match(LOCATIONS, text)

    return {
        "item": ALIASES.get(item, item),
        "color": ALIASES.get(color, color),
        "location": ALIASES.get(location, location),
        "description": message.strip(),
    }
