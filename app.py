from datetime import date
from pathlib import Path

import streamlit as st

from src.chatbot import HELP_MESSAGE, format_match, process_message
from src.database import add_report, get_reports, get_summary
from src.matcher import find_matches
from src.notifications import send_match_email
from src.storage import save_uploaded_image

st.set_page_config(
    page_title="Smart Campus Lost-and-Found Assistant",
    page_icon="🔎",
    layout="wide",
)

st.title("Smart Campus Lost-and-Found Assistant")
st.caption(
    "Report lost and found items, upload images, and discover possible matches."
)

summary = get_summary()
metric_columns = st.columns(4)
metric_columns[0].metric("Open reports", summary["open"])
metric_columns[1].metric("Lost reports", summary["lost"])
metric_columns[2].metric("Found reports", summary["found"])
metric_columns[3].metric("Resolved", summary["resolved"])

with st.sidebar:
    st.header("User details")
    contact = st.text_input(
        "Email or phone",
        placeholder="student@example.com",
        help="Email alerts work only when SMTP settings are configured.",
    )

    st.info("Example: I lost a black wallet in the library")

chat_tab, report_tab, search_tab = st.tabs(
    ["Chat Assistant", "Detailed Report", "Search Reports"]
)

with chat_tab:
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "Hello! I can save lost and found reports and search for matches.\n\n"
                    + HELP_MESSAGE
                ),
            }
        ]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_message = st.chat_input("Describe a lost or found item")

    if user_message:
        st.session_state.messages.append(
            {"role": "user", "content": user_message}
        )

        reply = process_message(user_message, contact=contact)

        st.session_state.messages.append(
            {"role": "assistant", "content": reply}
        )
        st.rerun()

with report_tab:
    st.subheader("Create a detailed report")

    with st.form("report_form", clear_on_submit=True):
        left, right = st.columns(2)

        with left:
            report_type = st.selectbox("Report type", ["lost", "found"])
            item = st.text_input("Item name", placeholder="wallet")
            color = st.text_input("Colour", placeholder="black")
            location = st.text_input("Location", placeholder="library")

        with right:
            event_date = st.date_input("Date lost or found", value=date.today())
            report_contact = st.text_input(
                "Contact email or phone",
                value=contact,
            )
            image = st.file_uploader(
                "Upload item image",
                type=["png", "jpg", "jpeg", "webp"],
            )

        description = st.text_area(
            "Description",
            placeholder="Black leather wallet with a student card inside.",
        )

        submitted = st.form_submit_button("Save report")

    if submitted:
        if not item.strip():
            st.error("Please enter an item name.")
        else:
            try:
                image_path = save_uploaded_image(image)
                report_id = add_report(
                    report_type=report_type,
                    item=item,
                    color=color,
                    location=location,
                    event_date=event_date.isoformat(),
                    description=description,
                    contact=report_contact,
                    image_path=image_path,
                )

                query = {
                    "item": item,
                    "color": color,
                    "location": location,
                    "event_date": event_date.isoformat(),
                    "description": description,
                }

                expected_type = "found" if report_type == "lost" else "lost"
                matches = find_matches(
                    query,
                    get_reports(status="open"),
                    expected_type=expected_type,
                )

                st.success(f"Report #{report_id} was saved.")

                if matches:
                    st.subheader("Possible match")
                    st.markdown(format_match(matches[0]))

                    match_image = matches[0].get("image_path")
                    if match_image and Path(match_image).exists():
                        st.image(match_image, width=300)

                    sent, notification_message = send_match_email(
                        report_contact,
                        item,
                        format_match(matches[0]).replace("**", ""),
                    )

                    if sent:
                        st.success(notification_message)
                    else:
                        st.info(notification_message)
                else:
                    st.info("No strong match was found yet.")

            except ValueError as exc:
                st.error(str(exc))

with search_tab:
    st.subheader("Search open reports")

    search_item = st.text_input("Item", key="search_item")
    search_color = st.text_input("Colour", key="search_color")
    search_location = st.text_input("Location", key="search_location")
    search_description = st.text_area("Description", key="search_description")

    if st.button("Search for matches"):
        if not search_item.strip():
            st.warning("Please enter an item name.")
        else:
            query = {
                "item": search_item,
                "color": search_color,
                "location": search_location,
                "event_date": "",
                "description": search_description,
            }

            matches = find_matches(
                query,
                get_reports(status="open"),
                minimum_score=0.35,
            )

            if not matches:
                st.info("No close matches were found.")
            else:
                for match in matches[:10]:
                    with st.container(border=True):
                        st.markdown(format_match(match))
                        st.write(match.get("description") or "No description")

                        image_path = match.get("image_path")
                        if image_path and Path(image_path).exists():
                            st.image(image_path, width=250)
