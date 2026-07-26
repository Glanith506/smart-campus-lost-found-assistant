from pathlib import Path

from src.database import (
    add_report,
    delete_report,
    get_report,
    get_reports,
    get_summary,
    update_status,
)


def test_report_lifecycle(tmp_path: Path):
    db_path = tmp_path / "test.db"

    report_id = add_report(
        report_type="lost",
        item="wallet",
        color="black",
        location="library",
        event_date="2026-07-20",
        description="Test report",
        contact="test@example.com",
        db_path=db_path,
    )

    report = get_report(report_id, db_path=db_path)
    assert report is not None
    assert report["item"] == "wallet"

    summary = get_summary(db_path=db_path)
    assert summary["total"] == 1
    assert summary["open"] == 1

    assert update_status(report_id, "resolved", db_path=db_path)
    assert get_reports(status="open", db_path=db_path) == []

    assert delete_report(report_id, db_path=db_path)
    assert get_report(report_id, db_path=db_path) is None
