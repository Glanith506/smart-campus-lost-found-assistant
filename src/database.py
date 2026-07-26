from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB_PATH = PROJECT_ROOT / "data" / "lost_found.db"


def connect(db_path: Path = DEFAULT_DB_PATH) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    return connection


def init_db(db_path: Path = DEFAULT_DB_PATH) -> None:
    with connect(db_path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                report_type TEXT NOT NULL CHECK(report_type IN ('lost', 'found')),
                item TEXT NOT NULL,
                color TEXT,
                location TEXT,
                event_date TEXT,
                description TEXT,
                contact TEXT,
                image_path TEXT,
                status TEXT NOT NULL DEFAULT 'open',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        connection.commit()


def add_report(
    report_type: str,
    item: str,
    color: str = "",
    location: str = "",
    event_date: str = "",
    description: str = "",
    contact: str = "",
    image_path: str = "",
    db_path: Path = DEFAULT_DB_PATH,
) -> int:
    init_db(db_path)

    with connect(db_path) as connection:
        cursor = connection.execute(
            """
            INSERT INTO reports (
                report_type,
                item,
                color,
                location,
                event_date,
                description,
                contact,
                image_path
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                report_type.strip().lower(),
                item.strip().lower(),
                color.strip().lower(),
                location.strip().lower(),
                event_date.strip(),
                description.strip(),
                contact.strip(),
                image_path.strip(),
            ),
        )
        connection.commit()
        return int(cursor.lastrowid)


def get_reports(
    status: str | None = "open",
    report_type: str | None = None,
    db_path: Path = DEFAULT_DB_PATH,
) -> list[dict[str, Any]]:
    init_db(db_path)

    query = "SELECT * FROM reports WHERE 1 = 1"
    values: list[Any] = []

    if status:
        query += " AND status = ?"
        values.append(status)

    if report_type:
        query += " AND report_type = ?"
        values.append(report_type)

    query += " ORDER BY created_at DESC"

    with connect(db_path) as connection:
        rows = connection.execute(query, values).fetchall()

    return [dict(row) for row in rows]


def get_report(report_id: int, db_path: Path = DEFAULT_DB_PATH) -> dict[str, Any] | None:
    init_db(db_path)

    with connect(db_path) as connection:
        row = connection.execute(
            "SELECT * FROM reports WHERE id = ?",
            (report_id,),
        ).fetchone()

    return dict(row) if row else None


def update_status(
    report_id: int,
    new_status: str,
    db_path: Path = DEFAULT_DB_PATH,
) -> bool:
    if new_status not in {"open", "resolved"}:
        raise ValueError("Status must be 'open' or 'resolved'.")

    init_db(db_path)

    with connect(db_path) as connection:
        cursor = connection.execute(
            "UPDATE reports SET status = ? WHERE id = ?",
            (new_status, report_id),
        )
        connection.commit()

    return cursor.rowcount > 0


def delete_report(report_id: int, db_path: Path = DEFAULT_DB_PATH) -> bool:
    init_db(db_path)

    with connect(db_path) as connection:
        cursor = connection.execute(
            "DELETE FROM reports WHERE id = ?",
            (report_id,),
        )
        connection.commit()

    return cursor.rowcount > 0


def get_summary(db_path: Path = DEFAULT_DB_PATH) -> dict[str, int]:
    init_db(db_path)

    with connect(db_path) as connection:
        total = connection.execute("SELECT COUNT(*) FROM reports").fetchone()[0]
        open_count = connection.execute(
            "SELECT COUNT(*) FROM reports WHERE status = 'open'"
        ).fetchone()[0]
        lost_count = connection.execute(
            "SELECT COUNT(*) FROM reports WHERE report_type = 'lost'"
        ).fetchone()[0]
        found_count = connection.execute(
            "SELECT COUNT(*) FROM reports WHERE report_type = 'found'"
        ).fetchone()[0]
        resolved_count = connection.execute(
            "SELECT COUNT(*) FROM reports WHERE status = 'resolved'"
        ).fetchone()[0]

    return {
        "total": int(total),
        "open": int(open_count),
        "lost": int(lost_count),
        "found": int(found_count),
        "resolved": int(resolved_count),
    }
