from src.database import add_report, get_summary, init_db


def seed() -> None:
    init_db()

    if get_summary()["total"] > 0:
        print("Database already contains reports. No sample data was added.")
        return

    sample_reports = [
        {
            "report_type": "found",
            "item": "wallet",
            "color": "black",
            "location": "library",
            "event_date": "2026-07-20",
            "description": "Black leather wallet found near the second-floor computers.",
            "contact": "security@campus.edu",
        },
        {
            "report_type": "lost",
            "item": "bottle",
            "color": "blue",
            "location": "cafeteria",
            "event_date": "2026-07-21",
            "description": "Blue metal bottle with two travel stickers.",
            "contact": "student@example.com",
        },
        {
            "report_type": "found",
            "item": "keys",
            "color": "silver",
            "location": "parking",
            "event_date": "2026-07-22",
            "description": "Three silver keys with a red keychain.",
            "contact": "reception@campus.edu",
        },
    ]

    for report in sample_reports:
        add_report(**report)

    print("Sample reports added successfully.")


if __name__ == "__main__":
    seed()
