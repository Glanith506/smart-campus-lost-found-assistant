from datetime import date
from pathlib import Path
import html

import streamlit as st

from src.chatbot import HELP_MESSAGE, format_match, process_message
from src.database import add_report, get_reports, get_summary
from src.matcher import find_matches
from src.notifications import send_match_email
from src.storage import save_uploaded_image


# --------------------------------------------------
# PAGE SETTINGS
# --------------------------------------------------
st.set_page_config(
    page_title="CampusFind | Lost & Found",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------
# CUSTOM DESIGN
# --------------------------------------------------
st.markdown(
    """
    <style>
    @import url(
        'https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap'
    );

    :root {
        --navy: #142b3b;
        --mint: #b8f3d1;
        --text: #193344;
        --muted: #6b7f8c;
        --border: #e2eae8;
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .stApp {
        background: #f4f7f6;
        color: var(--text);
    }

    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    h1, h2, h3 {
        font-family: 'Manrope', sans-serif !important;
        color: var(--navy);
        letter-spacing: -0.6px;
    }

    [data-testid="stHeader"] {
        background: #f4f7f6;
    }

    #MainMenu, footer {
        visibility: hidden;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #142b3b;
        border-right: none;
    }

    [data-testid="stSidebar"] .block-container {
        padding-top: 2rem;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label {
        color: #eef6f3 !important;
    }

    [data-testid="stSidebar"] input {
        color: #193344 !important;
        -webkit-text-fill-color: #193344 !important;
        background: #ffffff !important;
    }

    .sidebar-brand {
        font-family: 'Manrope', sans-serif;
        font-size: 29px;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -1px;
    }

    .sidebar-brand span {
        color: #b8f3d1;
    }

    .sidebar-tagline {
        color: #a6bbc4;
        font-size: 13px;
        margin-top: 6px;
        margin-bottom: 32px;
    }

    .sidebar-label {
        color: #9bb5bf;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 2px;
        margin-bottom: 14px;
    }

    .sidebar-note {
        background: #203c4b;
        border: 1px solid #355360;
        padding: 18px;
        border-radius: 16px;
        margin-top: 25px;
        color: #dbe9e6;
        font-size: 13px;
        line-height: 1.8;
    }

    .sidebar-note strong {
        color: #b8f3d1;
    }

    .sidebar-bottom {
        color: #9bb5bf;
        font-size: 12px;
        line-height: 1.8;
        margin-top: 35px;
    }

    /* Top navigation */
    .topbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 15px;
        margin-bottom: 27px;
    }

    .breadcrumb {
        color: #7b8b94;
        font-size: 13px;
    }

    .breadcrumb strong {
        color: #193344;
        font-weight: 600;
    }

    .date-pill {
        background: #ffffff;
        border: 1px solid #e2eae8;
        color: #536c78;
        border-radius: 50px;
        padding: 9px 16px;
        font-size: 12px;
        white-space: nowrap;
    }

    /* Hero */
    .hero {
        background: #142b3b;
        border-radius: 26px;
        padding: 38px 42px;
        color: #ffffff;
        position: relative;
        overflow: hidden;
        margin-bottom: 27px;
    }

    .hero::after {
        content: "";
        position: absolute;
        width: 310px;
        height: 310px;
        border: 45px solid rgba(184, 243, 209, 0.08);
        border-radius: 50%;
        right: -70px;
        top: -100px;
        pointer-events: none;
    }

    .hero-content {
        position: relative;
        z-index: 1;
        max-width: 740px;
    }

    .hero-eyebrow {
        display: inline-block;
        color: #b8f3d1;
        background: rgba(184, 243, 209, 0.09);
        border: 1px solid rgba(184, 243, 209, 0.22);
        border-radius: 30px;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 2px;
        padding: 7px 13px;
        margin-bottom: 17px;
    }

    .hero h1 {
        color: #ffffff !important;
        font-size: clamp(30px, 4vw, 47px);
        font-weight: 800;
        line-height: 1.18;
        margin: 0 0 14px;
        padding: 0;
        letter-spacing: -1.8px;
    }

    .hero h1 span {
        color: #b8f3d1;
    }

    .hero p {
        color: #b7c9d1;
        font-size: 14px;
        line-height: 1.8;
        margin: 0;
        max-width: 570px;
    }

    .hero-tags {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 25px;
    }

    .hero-tag {
        border: 1px solid #3b535f;
        border-radius: 8px;
        color: #deebe6;
        padding: 7px 11px;
        font-size: 11px;
    }

    /* Statistics */
    .stat-card {
        background: #ffffff;
        border: 1px solid #e2eae8;
        border-radius: 18px;
        padding: 21px 23px;
        min-height: 150px;
        box-sizing: border-box;
    }

    .stat-top {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 10px;
    }

    .stat-label {
        color: #6b7f8c;
        font-size: 12px;
        font-weight: 600;
    }

    .stat-icon {
        height: 33px;
        width: 33px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
    }

    .icon-blue { background: #e9f0fe; }
    .icon-orange { background: #fff0e5; }
    .icon-purple { background: #f1eafe; }
    .icon-green { background: #e3f6eb; }

    .stat-value {
        font-family: 'Manrope', sans-serif;
        color: #142b3b;
        font-size: 33px;
        line-height: 1.2;
        font-weight: 800;
        letter-spacing: -1px;
    }

    .stat-foot {
        color: #8a9aa2;
        font-size: 11px;
        margin-top: 8px;
    }

    .section-heading {
        margin: 30px 0 5px;
        font-family: 'Manrope', sans-serif;
        font-size: 21px;
        font-weight: 800;
        color: #142b3b;
    }

    .section-description {
        font-size: 13px;
        color: #7b8b94;
        margin-bottom: 20px;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: #e9efec;
        border-radius: 13px;
        padding: 6px;
        gap: 6px;
        margin-bottom: 22px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 9px;
        padding: 11px 22px;
        height: auto;
        color: #687e89;
        font-weight: 600;
        background: transparent;
    }

    .stTabs [aria-selected="true"] {
        color: #142b3b !important;
        background: #ffffff !important;
        box-shadow: 0 2px 7px rgba(20, 43, 59, 0.06);
    }

    .stTabs [data-baseweb="tab-highlight"],
    .stTabs [data-baseweb="tab-border"] {
        display: none;
    }

    /* Forms and inputs */
    [data-testid="stForm"] {
        background: #ffffff;
        border: 1px solid #e2eae8;
        border-radius: 19px;
        padding: 25px;
    }

    [data-testid="stWidgetLabel"] p {
        color: #39515f;
        font-size: 13px;
        font-weight: 600;
    }

    [data-baseweb="input"],
    [data-baseweb="select"] > div,
    [data-baseweb="textarea"] {
        border-radius: 10px !important;
        border-color: #dce6e2 !important;
        background: #ffffff !important;
    }

    [data-baseweb="input"] input,
    [data-baseweb="textarea"] textarea {
        color: #193344 !important;
        -webkit-text-fill-color: #193344 !important;
    }

    [data-testid="stFileUploader"] {
        background: #f7faf8;
        border-radius: 12px;
    }

    .stButton > button,
    .stFormSubmitButton > button {
        background: #142b3b;
        color: #ffffff;
        border: 1px solid #142b3b;
        border-radius: 10px;
        padding: 11px 23px;
        font-weight: 600;
        transition: background 0.2s, border-color 0.2s;
    }

    .stButton > button:hover,
    .stFormSubmitButton > button:hover {
        color: #142b3b;
        background: #b8f3d1;
        border-color: #b8f3d1;
    }

    .stButton > button:focus,
    .stFormSubmitButton > button:focus {
        color: #142b3b !important;
        background: #b8f3d1 !important;
        border-color: #b8f3d1 !important;
        box-shadow: none !important;
    }

    /* Chat */
    [data-testid="stChatMessage"] {
        background: #ffffff;
        border: 1px solid #e2eae8;
        border-radius: 15px;
        margin-bottom: 12px;
        padding: 18px;
    }

    [data-testid="stChatMessage"] p {
        color: #314e5c;
        line-height: 1.75;
    }

    [data-testid="stChatInput"] {
        border-radius: 14px;
        border: 1px solid #cfdfd7;
        background: #ffffff;
    }

    .assistant-intro {
        display: flex;
        align-items: center;
        gap: 13px;
        margin-bottom: 20px;
    }

    .assistant-symbol {
        background: #dff5e8;
        width: 47px;
        height: 47px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 14px;
        font-size: 22px;
    }

    .assistant-name {
        font-family: 'Manrope', sans-serif;
        font-size: 17px;
        font-weight: 800;
        color: #142b3b;
    }

    .assistant-subtitle {
        color: #7a8d96;
        font-size: 12px;
        margin-top: 3px;
    }

    /* Guidance cards */
    .tip-card {
        background: #ffffff;
        border: 1px solid #e2eae8;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 14px;
    }

    .tip-number {
        display: inline-block;
        background: #e7f5ed;
        color: #337657;
        padding: 5px 9px;
        font-size: 11px;
        border-radius: 7px;
        font-weight: 700;
        margin-bottom: 10px;
    }

    .tip-title {
        color: #193344;
        font-size: 14px;
        font-weight: 700;
        margin-bottom: 6px;
    }

    .tip-text {
        color: #7a8d96;
        font-size: 12px;
        line-height: 1.8;
    }

    .privacy-note {
        background: #e8f2ec;
        color: #537363;
        padding: 15px 17px;
        border-radius: 12px;
        font-size: 12px;
        line-height: 1.8;
        margin-top: 15px;
    }

    .result-label {
        color: #71858f;
        font-size: 11px;
        letter-spacing: 1.5px;
        font-weight: 700;
        margin-bottom: 12px;
    }

    .app-footer {
        border-top: 1px solid #dfe8e3;
        margin-top: 42px;
        padding-top: 21px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 15px;
        color: #83958d;
        font-size: 12px;
    }

    .app-footer strong {
        color: #284b3a;
        font-weight: 700;
    }

    @media (max-width: 768px) {
        .block-container {
            padding-top: 1rem;
        }

        .hero {
            padding: 28px 23px;
        }

        .topbar,
        .app-footer {
            flex-direction: column;
            align-items: flex-start;
        }

        .stTabs [data-baseweb="tab"] {
            padding: 10px 12px;
        }

        .stat-card {
            min-height: 135px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# HELPERS
# --------------------------------------------------
def statistic_card(label, value, icon, icon_class, footnote):
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-top">
                <div class="stat-label">{html.escape(label)}</div>
                <div class="stat-icon {icon_class}">{icon}</div>
            </div>
            <div class="stat-value">{html.escape(str(value))}</div>
            <div class="stat-foot">{html.escape(footnote)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def display_match_image(match, width=280):
    image_path = match.get("image_path")

    if image_path and Path(image_path).is_file():
        st.image(str(image_path), width=width)


def refresh_statistics():
    st.session_state["refresh_dashboard"] = True


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-brand">Campus<span>Find.</span></div>
        <div class="sidebar-tagline">A little help. A happy reunion.</div>

        <div class="sidebar-label">YOUR CAMPUS COMPANION</div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Stay connected")

    contact = st.text_input(
        "Email or phone",
        placeholder="student@example.com",
        help=(
            "Used as the contact for your reports. "
            "Email notifications require configured SMTP settings "
            "and a valid email address."
        ),
        key="user_contact",
    )

    st.markdown(
        """
        <div class="sidebar-note">
            <strong>💡 Start with a simple message</strong><br>
            “I lost a black wallet in the library.”
            <br><br>
            Include the item, colour, and location
            to help find a closer match.
        </div>

        <div class="sidebar-bottom">
            REPORT IT. FIND IT. RECONNECT.<br>
            Bringing belongings back to their people.
        </div>
        """,
        unsafe_allow_html=True,
    )


# --------------------------------------------------
# TOP BAR
# --------------------------------------------------
today_label = date.today().strftime("%d %B %Y")

st.markdown(
    f"""
    <div class="topbar">
        <div class="breadcrumb">
            CampusFind &nbsp; / &nbsp; <strong>Dashboard</strong>
        </div>
        <div class="date-pill">📅 &nbsp; {today_label}</div>
    </div>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# WELCOME BANNER
# --------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <div class="hero-content">
            <div class="hero-eyebrow">SMART CAMPUS · LOST & FOUND</div>
            <h1>Lost something?<br><span>Let’s bring it home.</span></h1>
            <p>
                A missing notebook. A forgotten wallet. A pair of keys.
                Connect the dots with your campus community and find
                what matters.
            </p>
            <div class="hero-tags">
                <div class="hero-tag">💬 Chat to report</div>
                <div class="hero-tag">📸 Add item photos</div>
                <div class="hero-tag">🔎 Discover matches</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# LIVE STATISTICS
# --------------------------------------------------
summary = get_summary()

# This placeholder lets us update counts after saving a report.
statistics = st.empty()


def render_statistics():
    with statistics.container():
        columns = st.columns(4)

        with columns[0]:
            statistic_card(
                "Open reports",
                summary["open"],
                "📋",
                "icon-blue",
                "Currently awaiting resolution",
            )

        with columns[1]:
            statistic_card(
                "Lost reports",
                summary["lost"],
                "🔍",
                "icon-orange",
                "Items reported as lost",
            )

        with columns[2]:
            statistic_card(
                "Found reports",
                summary["found"],
                "📦",
                "icon-purple",
                "Items reported as found",
            )

        with columns[3]:
            statistic_card(
                "Resolved",
                summary["resolved"],
                "✓",
                "icon-green",
                "Reports marked as resolved",
            )


render_statistics()


# --------------------------------------------------
# WORKSPACE
# --------------------------------------------------
st.markdown(
    """
    <div class="section-heading">Your lost & found workspace</div>
    <div class="section-description">
        Report an item, talk to the assistant, or explore possible matches.
    </div>
    """,
    unsafe_allow_html=True,
)

chat_tab, report_tab, search_tab = st.tabs(
    [
        "💬  Chat Assistant",
        "📝  Report an Item",
        "🔎  Find Matches",
    ]
)


# --------------------------------------------------
# CHAT ASSISTANT
# --------------------------------------------------
with chat_tab:
    chat_column, help_column = st.columns([2.2, 1], gap="large")

    with chat_column:
        st.markdown(
            """
            <div class="assistant-intro">
                <div class="assistant-symbol">✦</div>
                <div>
                    <div class="assistant-name">Meet your campus assistant</div>
                    <div class="assistant-subtitle">
                        Describe your item. We’ll help with the next step.
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if "messages" not in st.session_state:
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": (
                        "Hello! 👋 Welcome to CampusFind.\n\n"
                        "I can help you report a lost item, register "
                        "something you found, and search for possible matches.\n\n"
                        + HELP_MESSAGE
                    ),
                }
            ]

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        user_message = st.chat_input(
            "For example: I lost a black wallet in the library",
            key="campus_chat",
        )

        if user_message:
            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": user_message,
                }
            )

            with st.spinner("Looking into that for you..."):
                reply = process_message(user_message, contact=contact)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": reply,
                }
            )

            st.rerun()

    with help_column:
        st.markdown(
            """
            <div class="tip-card">
                <div class="tip-number">01 · DESCRIBE</div>
                <div class="tip-title">The details make a difference</div>
                <div class="tip-text">
                    Mention the item name, colour, and where you last
                    saw it. Add distinctive features when possible.
                </div>
            </div>

            <div class="tip-card">
                <div class="tip-number">02 · CONNECT</div>
                <div class="tip-title">Leave a way to reach you</div>
                <div class="tip-text">
                    Add your email or phone in the sidebar before
                    submitting a report.
                </div>
            </div>

            <div class="tip-card">
                <div class="tip-number">03 · REUNITE</div>
                <div class="tip-title">Check a possible match</div>
                <div class="tip-text">
                    Compare the details carefully and confirm ownership
                    before handing over an item.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# --------------------------------------------------
# DETAILED REPORT
# --------------------------------------------------
with report_tab:
    st.markdown("### Every reunion starts with a report")
    st.caption(
        "Share a few details so we can compare your item with existing reports."
    )

    with st.form("report_form", clear_on_submit=True):
        left, right = st.columns(2, gap="large")

        with left:
            st.markdown("#### 📋 Item details")

            report_type = st.selectbox(
                "What would you like to report?",
                ["lost", "found"],
                format_func=lambda value: (
                    "🔍 I lost an item"
                    if value == "lost"
                    else "📦 I found an item"
                ),
            )

            item = st.text_input(
                "Item name *",
                placeholder="e.g. Wallet, headphones, student ID",
            )

            color = st.text_input(
                "Colour",
                placeholder="e.g. Black, navy blue, silver",
            )

            location = st.text_input(
                "Location",
                placeholder="e.g. Central library, second floor",
            )

        with right:
            st.markdown("#### 📍 When & how to reach you")

            event_date = st.date_input(
                "Date lost or found",
                value=date.today(),
                max_value=date.today(),
            )

            report_contact = st.text_input(
                "Contact email or phone",
                value=contact,
                placeholder="How can someone reach you?",
            )

            image = st.file_uploader(
                "Add a photo of the item",
                type=["png", "jpg", "jpeg", "webp"],
                help="Optional. Add a clear photo if you have one.",
            )

        description = st.text_area(
            "What makes this item recognisable?",
            placeholder=(
                "e.g. A black leather wallet with a small zip pocket "
                "and a university student card inside."
            ),
            height=115,
        )

        st.caption("* Item name is required.")

        submitted = st.form_submit_button(
            "Save report & check matches →",
            use_container_width=True,
        )

    if submitted:
        if not item.strip():
            st.error("Please enter an item name before saving.")
        else:
            # Saving and notification are separate so an email problem
            # does not make a successfully saved report look unsuccessful.
            try:
                image_path = save_uploaded_image(image)

                report_id = add_report(
                    report_type=report_type,
                    item=item.strip(),
                    color=color.strip(),
                    location=location.strip(),
                    event_date=event_date.isoformat(),
                    description=description.strip(),
                    contact=report_contact.strip(),
                    image_path=image_path,
                )

            except ValueError as exc:
                st.error(str(exc))

            else:
                st.success(
                    f"Report #{report_id} saved. "
                    "Thank you for helping your campus community!"
                )

                summary = get_summary()
                render_statistics()

                query = {
                    "item": item.strip(),
                    "color": color.strip(),
                    "location": location.strip(),
                    "event_date": event_date.isoformat(),
                    "description": description.strip(),
                }

                expected_type = (
                    "found" if report_type == "lost" else "lost"
                )

                with st.spinner("Checking existing reports..."):
                    matches = find_matches(
                        query,
                        get_reports(status="open"),
                        expected_type=expected_type,
                    )

                if matches:
                    st.markdown("### ✨ A possible connection")

                    with st.container(border=True):
                        st.markdown(format_match(matches[0]))
                        display_match_image(matches[0])

                    if report_contact.strip():
                        try:
                            sent, notification_message = send_match_email(
                                report_contact.strip(),
                                item.strip(),
                                format_match(matches[0]).replace("**", ""),
                            )
                        except Exception:
                            st.info(
                                "Your report is saved, but the email alert "
                                "could not be sent. You can review the "
                                "possible match above."
                            )
                        else:
                            if sent:
                                st.success(notification_message)
                            else:
                                st.info(notification_message)
                else:
                    st.info(
                        "No strong match yet. Your report is saved, "
                        "and you can search again when more items are reported."
                    )

    st.markdown(
        """
        <div class="privacy-note">
            🛡️ Keep sensitive details private. Avoid uploading identity
            document numbers, passwords, or bank information. Leave
            some identifying details for ownership verification.
        </div>
        """,
        unsafe_allow_html=True,
    )


# --------------------------------------------------
# SEARCH REPORTS
# --------------------------------------------------
with search_tab:
    st.markdown("### Your next match could be here")
    st.caption(
        "Search open reports using the details you remember."
    )

    with st.form("search_form"):
        search_left, search_right = st.columns(2, gap="large")

        with search_left:
            search_item = st.text_input(
                "What item are you looking for? *",
                placeholder="e.g. Wallet",
                key="search_item",
            )

            search_color = st.text_input(
                "Colour",
                placeholder="e.g. Black",
                key="search_color",
            )

        with search_right:
            search_location = st.text_input(
                "Location",
                placeholder="e.g. Library",
                key="search_location",
            )

            search_type = st.selectbox(
                "Which reports would you like to search?",
                ["All open reports", "Found items", "Lost items"],
                key="search_type",
            )

        search_description = st.text_area(
            "Any other clues?",
            placeholder="Brand, material, markings, or other details...",
            key="search_description",
            height=100,
        )

        search_submitted = st.form_submit_button(
            "Find possible matches →",
            use_container_width=True,
        )

    if search_submitted:
        if not search_item.strip():
            st.warning("Enter an item name to start your search.")
        else:
            query = {
                "item": search_item.strip(),
                "color": search_color.strip(),
                "location": search_location.strip(),
                "event_date": "",
                "description": search_description.strip(),
            }

            expected_type = {
                "All open reports": None,
                "Found items": "found",
                "Lost items": "lost",
            }[search_type]

            # Filter reports here to preserve compatibility with
            # your existing matcher implementation.
            reports = get_reports(status="open")

            if expected_type is not None:
                # Using the matcher's existing expected_type parameter
                # avoids relying on database field names.
                with st.spinner("Searching campus reports..."):
                    matches = find_matches(
                        query,
                        reports,
                        expected_type=expected_type,
                        minimum_score=0.35,
                    )
            else:
                with st.spinner("Searching campus reports..."):
                    matches = find_matches(
                        query,
                        reports,
                        minimum_score=0.35,
                    )

            # Store results so they remain visible during other interactions.
            st.session_state["campus_search_results"] = matches

    if "campus_search_results" in st.session_state:
        matches = st.session_state["campus_search_results"]

        if not matches:
            st.info(
                "No close matches found. Try a broader location "
                "or fewer descriptive details."
            )
        else:
            st.markdown(
                f"### 🔎 {len(matches)} possible "
                f"{'match' if len(matches) == 1 else 'matches'}"
            )
            st.caption(
                "Compare each report carefully. A suggested match "
                "does not confirm ownership."
            )

            for index, match in enumerate(matches[:10], start=1):
                with st.container(border=True):
                    st.markdown(
                        f'<div class="result-label">POSSIBLE MATCH '
                        f'{index:02d}</div>',
                        unsafe_allow_html=True,
                    )

                    st.markdown(format_match(match))

                    # Display user-provided descriptions as plain text.
                    st.text(
                        match.get("description") or "No description provided."
                    )

                    display_match_image(match, width=250)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown(
    """
    <div class="app-footer">
        <div>CampusFind. &nbsp; Made for your campus community.</div>
        <div>Designed & developed by <strong>Glanith Dcunha</strong></div>
    </div>
    """,
    unsafe_allow_html=True,
)