from __future__ import annotations

import os
import smtplib
from email.message import EmailMessage


def email_is_configured() -> bool:
    required = [
        "SMTP_HOST",
        "SMTP_PORT",
        "SMTP_USERNAME",
        "SMTP_PASSWORD",
        "SMTP_FROM_EMAIL",
    ]
    return all(os.getenv(name) for name in required)


def send_match_email(
    recipient: str,
    item_name: str,
    match_details: str,
) -> tuple[bool, str]:
    if not recipient or "@" not in recipient:
        return False, "No valid email address was provided."

    if not email_is_configured():
        return False, "Email is not configured. The match is still shown on screen."

    message = EmailMessage()
    message["Subject"] = f"Possible match found for your {item_name}"
    message["From"] = os.environ["SMTP_FROM_EMAIL"]
    message["To"] = recipient
    message.set_content(
        "A possible match has been found in the Smart Campus Lost-and-Found "
        f"Assistant.\n\n{match_details}\n\nPlease contact campus reception "
        "before collecting any item."
    )

    try:
        with smtplib.SMTP(
            os.environ["SMTP_HOST"],
            int(os.environ["SMTP_PORT"]),
            timeout=15,
        ) as server:
            server.starttls()
            server.login(
                os.environ["SMTP_USERNAME"],
                os.environ["SMTP_PASSWORD"],
            )
            server.send_message(message)
    except Exception as exc:
        return False, f"Email could not be sent: {exc}"

    return True, "Email notification sent."
