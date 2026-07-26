from pathlib import Path

import pandas as pd
import streamlit as st

from src.database import (
    delete_report,
    get_reports,
    get_summary,
    update_status,
)

st.set_page_config(
    page_title="Lost-and-Found Admin",
    page_icon="🛠️",
    layout="wide",
)

st.title("Admin Dashboard")
st.caption("Review, resolve, reopen, or delete lost-and-found reports.")

summary = get_summary()
columns = st.columns(5)
columns[0].metric("Total", summary["total"])
columns[1].metric("Open", summary["open"])
columns[2].metric("Lost", summary["lost"])
columns[3].metric("Found", summary["found"])
columns[4].metric("Resolved", summary["resolved"])

status_filter = st.selectbox("Status", ["all", "open", "resolved"])
type_filter = st.selectbox("Report type", ["all", "lost", "found"])

reports = get_reports(
    status=None if status_filter == "all" else status_filter,
    report_type=None if type_filter == "all" else type_filter,
)

if reports:
    table = pd.DataFrame(reports)
    visible_columns = [
        "id",
        "report_type",
        "item",
        "color",
        "location",
        "event_date",
        "contact",
        "status",
        "created_at",
    ]
    st.dataframe(
        table[[column for column in visible_columns if column in table.columns]],
        use_container_width=True,
        hide_index=True,
    )
else:
    st.info("No reports match the selected filters.")

st.divider()
st.subheader("Manage a report")

report_id = st.number_input("Report ID", min_value=1, step=1)
action = st.selectbox("Action", ["Mark resolved", "Reopen", "Delete"])

if st.button("Apply action"):
    if action == "Mark resolved":
        changed = update_status(int(report_id), "resolved")
    elif action == "Reopen":
        changed = update_status(int(report_id), "open")
    else:
        changed = delete_report(int(report_id))

    if changed:
        st.success("Report updated successfully.")
        st.rerun()
    else:
        st.error("Report ID was not found.")

st.divider()
st.subheader("Report images")

for report in reports:
    image_path = report.get("image_path")
    if image_path and Path(image_path).exists():
        with st.container(border=True):
            st.markdown(
                f"**Report #{report['id']} — "
                f"{report['report_type'].title()} {report['item'].title()}**"
            )
            st.image(image_path, width=250)
