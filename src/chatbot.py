from __future__ import annotations

from .database import add_report, get_reports
from .matcher import find_matches
from .notifications import send_match_email
from .parser import detect_intent, extract_details


HELP_MESSAGE = """
Try messages like:

- `I lost a black wallet in the library`
- `I found a blue bottle in the cafeteria`
- `Search for my silver keys`
- `Show all reports`

For image upload and date selection, use the report form below the chat.
""".strip()


def format_match(report: dict) -> str:
    percentage = int(report["match_score"] * 100)
    color = report.get("color") or "unknown colour"
    location = report.get("location") or "unknown location"
    event_date = report.get("event_date") or "unknown date"
    contact = report.get("contact") or "not provided"

    return (
        f"**{percentage}% match** — {color.title()} "
        f"{report['item'].title()} at {location.title()} on {event_date}. "
        f"Report ID: #{report['id']}. Contact: {contact}"
    )


def process_message(message: str, contact: str = "") -> str:
    intent = detect_intent(message)
    details = extract_details(message)

    if intent == "help":
        return HELP_MESSAGE

    if intent == "list":
        reports = get_reports(status="open")
        if not reports:
            return "There are no open reports."

        lines = [
            f"#{report['id']} — {report['report_type'].title()}: "
            f"{(report['color'] or 'unknown colour').title()} "
            f"{report['item'].title()} at "
            f"{(report['location'] or 'unknown location').title()}"
            for report in reports[:10]
        ]
        return "Open reports:\n\n" + "\n".join(lines)

    if intent in {"report_lost", "report_found"}:
        if not details["item"]:
            return (
                "I understood the report, but I could not identify the item. "
                "Please mention an item such as wallet, phone, bag, keys, or bottle."
            )

        report_type = "lost" if intent == "report_lost" else "found"
        report_id = add_report(
            report_type=report_type,
            item=details["item"],
            color=details["color"],
            location=details["location"],
            description=details["description"],
            contact=contact,
        )

        opposite_type = "found" if report_type == "lost" else "lost"
        matches = find_matches(
            details,
            get_reports(status="open"),
            expected_type=opposite_type,
        )

        reply = (
            f"Your **{report_type}** report was saved with ID **#{report_id}**.\n\n"
            f"- Item: {(details['color'] or 'unspecified colour').title()} "
            f"{details['item'].title()}\n"
            f"- Location: {(details['location'] or 'not specified').title()}"
        )

        if matches:
            reply += "\n\n### Possible match\n" + format_match(matches[0])

            sent, message_text = send_match_email(
                recipient=contact,
                item_name=details["item"],
                match_details=format_match(matches[0]).replace("**", ""),
            )
            reply += f"\n\n{message_text}"
        else:
            reply += "\n\nNo strong match was found yet."

        return reply

    if intent == "search":
        if not details["item"]:
            return "Please mention the item you want to search for."

        matches = find_matches(details, get_reports(status="open"))

        if not matches:
            return "I could not find a close match."

        return "### Best matches\n" + "\n\n".join(
            format_match(report) for report in matches[:5]
        )

    return (
        "I did not understand that message. "
        "Type `help` to see example commands."
    )
