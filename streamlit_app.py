import streamlit as st
import streamlit.components.v1 as components
from datetime import date
from task_manager import TaskManager


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="TaskFlow | Smart Task Management",
    page_icon="✓",
    layout="wide",
    initial_sidebar_state="expanded",
)

PRIORITIES = ["High", "Medium", "Low"]

PAGES = [
    "Dashboard",
    "Add Task",
    "All Tasks",
    "Pending Tasks",
    "Completed Tasks",
    "Search Tasks",
    "Filter by Priority",
    "Statistics",
]

THEMES = {
    "Sea Green": {
        "bg": "#F1F8F6",
        "sidebar": "#064E46",
        "card": "#FFFFFF",
        "metric": "#E4F3EF",
        "primary": "#078577",
        "hover": "#D0E9E0",
        "text": "#123D39",
        "muted": "#54756E",
        "border": "#C9E1DA",
        "side_text": "#FFFFFF",
        "button_text": "#FFFFFF",
    },
    "Navy Blue": {
        "bg": "#F1F5FB",
        "sidebar": "#102D50",
        "card": "#FFFFFF",
        "metric": "#E7EFFB",
        "primary": "#245FA8",
        "hover": "#D4E4F8",
        "text": "#142F50",
        "muted": "#526B8B",
        "border": "#CBD9ED",
        "side_text": "#FFFFFF",
        "button_text": "#FFFFFF",
    },
    "Dark Theme": {
        "bg": "#101722",
        "sidebar": "#080E18",
        "card": "#202D40",
        "metric": "#26364C",
        "primary": "#8DB5FF",
        "hover": "#3A506F",
        "text": "#F0F4FC",
        "muted": "#B0BED3",
        "border": "#40516A",
        "side_text": "#F0F4FC",
        "button_text": "#101722",
    },
}


# =====================================================
# SESSION STATE
# =====================================================

if "manager" not in st.session_state:
    st.session_state.manager = TaskManager()

if "navigation" not in st.session_state:
    st.session_state.navigation = "Dashboard"

if "app_theme" not in st.session_state:
    st.session_state.app_theme = "Sea Green"

manager = st.session_state.manager


def go_to_add_task():
    st.session_state.navigation = "Add Task"


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:
    st.markdown(
        """
        <div class="brand">
            <div class="brand-title">✓ TaskFlow</div>
            <div class="brand-subtitle">SMART TASK MANAGEMENT</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 🎨 Appearance")

    theme = st.selectbox(
        "Choose theme",
        list(THEMES.keys()),
        key="app_theme",
    )

    st.divider()

    page = st.radio(
        "NAVIGATION",
        PAGES,
        key="navigation",
    )

    st.divider()

    st.caption("✓ TaskFlow v2.0")
    st.caption("Plan smarter. Achieve more.")


c = THEMES[theme]


# =====================================================
# GLOBAL CSS AND ANIMATIONS
# =====================================================

st.markdown(
    f"""
    <style>
    :root {{
        --app-bg: {c["bg"]};
        --sidebar-bg: {c["sidebar"]};
        --card-bg: {c["card"]};
        --metric-bg: {c["metric"]};
        --primary: {c["primary"]};
        --hover: {c["hover"]};
        --text: {c["text"]};
        --muted: {c["muted"]};
        --border: {c["border"]};
        --side-text: {c["side_text"]};
        --button-text: {c["button_text"]};
    }}

    .stApp {{
        background: var(--app-bg);
        color: var(--text);
        font-family: "Segoe UI", Arial, sans-serif;
    }}

    [data-testid="stHeader"] {{
        background: var(--app-bg);
    }}

    [data-testid="stSidebar"] {{
        background: var(--sidebar-bg);
        border-right: 1px solid var(--border);
    }}

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {{
        color: var(--side-text) !important;
    }}

    [data-testid="stSidebar"] [data-baseweb="select"] > div {{
        background: #FFFFFF !important;
        border-radius: 9px !important;
    }}

    [data-testid="stSidebar"] [data-baseweb="select"] * {{
        color: #18334D !important;
        -webkit-text-fill-color: #18334D !important;
    }}

    .brand {{
        padding: 8px 0 22px;
        border-bottom: 1px solid rgba(255,255,255,.24);
        margin-bottom: 22px;
    }}

    .brand-title {{
        font-size: 29px;
        font-weight: 800;
        letter-spacing: -.8px;
    }}

    .brand-subtitle {{
        margin-top: 7px;
        font-size: 10px;
        letter-spacing: 1.5px;
        opacity: .85;
    }}

    h1, h2, h3, h4 {{
        color: var(--text) !important;
        font-family: "Segoe UI", Arial, sans-serif !important;
        font-weight: 750 !important;
        letter-spacing: -.35px;
    }}

    h1 {{
        font-size: clamp(30px, 3vw, 44px) !important;
    }}

    h2 {{
        font-size: 26px !important;
    }}

    h3 {{
        font-size: 20px !important;
    }}

    p, label {{
        color: var(--text);
    }}

    [data-testid="stCaptionContainer"] {{
        color: var(--muted) !important;
        font-size: 13px !important;
    }}

    [data-testid="stMetric"] {{
        background: var(--metric-bg);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 17px;
        min-height: 108px;
    }}

    [data-testid="stMetricLabel"],
    [data-testid="stMetricLabel"] p {{
        color: var(--muted) !important;
        font-weight: 600 !important;
    }}

    [data-testid="stMetricValue"],
    [data-testid="stMetricValue"] div {{
        color: var(--text) !important;
        font-size: 30px !important;
        font-weight: 800 !important;
    }}

    [data-testid="stVerticalBlockBorderWrapper"] {{
        background: var(--card-bg);
        border: 1px solid var(--border);
        border-radius: 14px;
    }}

    .stButton > button,
    .stFormSubmitButton > button {{
        background: var(--primary) !important;
        color: var(--button-text) !important;
        border: 1px solid var(--primary) !important;
        border-radius: 9px !important;
        min-height: 41px;
        font-weight: 650 !important;
        transition: transform .2s ease, opacity .2s ease;
    }}

    .stButton > button *,
    .stFormSubmitButton > button * {{
        color: var(--button-text) !important;
        -webkit-text-fill-color: var(--button-text) !important;
    }}

    .stButton > button:hover,
    .stFormSubmitButton > button:hover {{
        opacity: .88;
        transform: translateY(-2px);
    }}

    [data-testid="stTextInput"] input,
    [data-testid="stDateInput"] input,
    [data-testid="stNumberInput"] input {{
        background: var(--card-bg) !important;
        color: var(--text) !important;
        border-color: var(--border) !important;
        border-radius: 9px !important;
        min-height: 41px;
    }}

    [data-testid="stCheckbox"] label p {{
        color: var(--text) !important;
    }}

    [data-testid="stProgressBar"] > div {{
        background: var(--hover);
        border-radius: 12px;
    }}

    [data-testid="stProgressBar"] > div > div {{
        background: var(--primary);
        border-radius: 12px;
    }}

    hr {{
        border-color: var(--border);
    }}

    /* ================= HERO SECTION ================= */

    .hero {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 25px;
        min-height: 245px;
        padding: 10px 12px;
        margin-bottom: 12px;
        overflow: hidden;
    }}

    .hero-copy {{
        flex: 1;
        min-width: 220px;
        animation: fadeSlideIn .8s ease both;
    }}

    .hero-copy h1 {{
        margin: 0 0 13px;
        font-size: clamp(31px, 3vw, 44px) !important;
        line-height: 1.18;
        color: var(--text) !important;
    }}

    .hero-copy p {{
        max-width: 470px;
        color: var(--muted);
        font-size: 16px;
        line-height: 1.8;
        margin: 0;
    }}

    .hero-label {{
        display: inline-block;
        margin-bottom: 15px;
        padding: 7px 12px;
        background: var(--hover);
        color: var(--text);
        border-radius: 20px;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1px;
    }}

    .hero-art {{
        position: relative;
        flex: 0 1 390px;
        width: 390px;
        max-width: 45%;
        min-width: 260px;
        height: 225px;
        display: flex;
        justify-content: center;
        align-items: center;
        isolation: isolate;
    }}

    .hero-glow {{
        position: absolute;
        width: 190px;
        height: 160px;
        background: var(--hover);
        border-radius: 50%;
        filter: blur(22px);
        opacity: .9;
        z-index: -1;
        animation: glowPulse 4s ease-in-out infinite;
    }}

    .task-board {{
        position: relative;
        z-index: 2;
        width: 225px;
        padding: 19px;
        background: var(--card-bg);
        border: 1px solid var(--border);
        border-radius: 17px;
        box-shadow: 0 15px 35px rgba(20,60,70,.13);
        transform: rotate(-4deg);
        animation: boardFloat 5s ease-in-out infinite;
    }}

    .board-heading {{
        font-size: 15px;
        font-weight: 800;
        color: var(--text);
        margin-bottom: 17px;
    }}

    .board-row {{
        display: flex;
        align-items: center;
        gap: 10px;
        margin: 13px 0;
    }}

    .board-check {{
        width: 23px;
        height: 23px;
        flex-shrink: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        background: var(--primary);
        color: var(--button-text);
        font-size: 13px;
        font-weight: 900;
        animation: checkPulse 2.5s ease-in-out infinite;
    }}

    .board-line {{
        height: 8px;
        width: 135px;
        background: var(--hover);
        border-radius: 20px;
        overflow: hidden;
    }}

    .board-line::after {{
        content: "";
        display: block;
        height: 100%;
        width: 60%;
        background: var(--primary);
        border-radius: inherit;
        animation: progressMove 3.5s ease-in-out infinite;
    }}

    .board-line.short {{
        width: 95px;
    }}

    .orbit {{
        position: absolute;
        width: 195px;
        height: 195px;
        top: 50%;
        left: 50%;
        margin-left: -97px;
        margin-top: -97px;
        border: 1px dashed var(--primary);
        border-radius: 50%;
        opacity: .5;
        animation: orbitSpin 12s linear infinite;
        z-index: 1;
    }}

    .orbit-check {{
        position: absolute;
        top: 13px;
        right: 36px;
        z-index: 3;
        width: 42px;
        height: 42px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        background: var(--primary);
        color: var(--button-text);
        font-size: 22px;
        font-weight: 900;
        box-shadow: 0 8px 20px rgba(0,0,0,.12);
        animation: checkPulse 2s ease-in-out infinite;
    }}

    .plane {{
        position: absolute;
        left: 18px;
        top: 20px;
        z-index: 3;
        font-size: 31px;
        color: var(--primary);
        animation: planeFloat 4s ease-in-out infinite;
    }}

    .hero-tag {{
        position: absolute;
        right: 0;
        bottom: 0;
        z-index: 4;
        padding: 7px 10px;
        border-radius: 8px;
        background: var(--card-bg);
        color: var(--muted);
        border: 1px solid var(--border);
        font-size: 10px;
        font-weight: 800;
        letter-spacing: .7px;
        white-space: nowrap;
    }}

    @keyframes boardFloat {{
        0%, 100% {{ transform: translateY(0) rotate(-4deg); }}
        50% {{ transform: translateY(-9px) rotate(1deg); }}
    }}

    @keyframes orbitSpin {{
        from {{ transform: rotate(0deg); }}
        to {{ transform: rotate(360deg); }}
    }}

    @keyframes planeFloat {{
        0%, 100% {{ transform: translate(0,0) rotate(-8deg); }}
        50% {{ transform: translate(12px,-9px) rotate(5deg); }}
    }}

    @keyframes checkPulse {{
        0%, 100% {{ scale: 1; }}
        50% {{ scale: 1.1; }}
    }}

    @keyframes progressMove {{
        0%, 100% {{ width: 35%; }}
        50% {{ width: 90%; }}
    }}

    @keyframes glowPulse {{
        0%, 100% {{ transform: scale(.9); opacity: .55; }}
        50% {{ transform: scale(1.12); opacity: 1; }}
    }}

    @keyframes fadeSlideIn {{
        from {{ opacity: 0; transform: translateY(15px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    @media (max-width: 760px) {{
        .hero {{
            flex-direction: column;
            align-items: flex-start;
            gap: 5px;
            padding: 10px 0;
        }}

        .hero-art {{
            width: 100%;
            max-width: 100%;
            min-width: 0;
            height: 215px;
            align-self: center;
        }}

        .hero-tag {{
            right: 0;
            bottom: 0;
        }}
    }}

    @media (prefers-reduced-motion: reduce) {{
        .hero-art *,
        .hero-copy {{
            animation: none !important;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


# =====================================================
# HELPER FUNCTIONS
# =====================================================

def get_stats():
    return manager.statistics()


def count_priority(priority):
    return len(manager.filter_by_priority(priority))


def empty_state(title, message):
    with st.container(border=True):
        st.subheader(title)
        st.caption(message)


def show_hero():
    """Render a lightweight animated hero illustration."""
    components.html(
        f"""
        <html>
        <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            :root {{
                --primary: {c["primary"]};
                --hover: {c["hover"]};
                --text: {c["text"]};
                --muted: {c["muted"]};
                --card: {c["card"]};
                --border: {c["border"]};
            }}
            * {{ box-sizing: border-box; }}
            body {{
                margin: 0;
                padding: 8px 4px;
                background: transparent;
                font-family: "Segoe UI", Arial, sans-serif;
                color: var(--text);
            }}
            .hero {{
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 20px;
                min-height: 250px;
                width: 100%;
                overflow: hidden;
            }}
            .hero-copy {{
                flex: 1 1 50%;
                min-width: 0;
                animation: fade-in .7s ease both;
            }}
            .label {{
                display: inline-block;
                padding: 7px 11px;
                margin-bottom: 12px;
                border-radius: 20px;
                background: var(--hover);
                color: var(--text);
                font-size: 10px;
                font-weight: 800;
                letter-spacing: 1px;
            }}
            h1 {{
                margin: 0 0 12px;
                font-size: clamp(27px, 3.3vw, 42px);
                line-height: 1.15;
                color: var(--text);
            }}
            p {{
                margin: 0;
                max-width: 420px;
                color: var(--muted);
                font-size: 15px;
                line-height: 1.7;
            }}
            .art {{
                position: relative;
                flex: 0 1 340px;
                min-width: 220px;
                height: 235px;
                display: flex;
                align-items: center;
                justify-content: center;
            }}
            .glow {{
                position: absolute;
                width: 165px;
                height: 150px;
                border-radius: 50%;
                background: var(--hover);
                filter: blur(18px);
                animation: pulse 4s ease-in-out infinite;
            }}
            .orbit {{
                position: absolute;
                width: 190px;
                height: 190px;
                border: 1px dashed var(--primary);
                border-radius: 50%;
                opacity: .5;
                animation: spin 18s linear infinite;
            }}
            .board {{
                position: relative;
                z-index: 2;
                width: 215px;
                padding: 18px;
                border: 1px solid var(--border);
                border-radius: 16px;
                background: var(--card);
                box-shadow: 0 12px 28px rgba(20, 50, 60, .12);
                animation: float 4.5s ease-in-out infinite;
            }}
            .board-title {{
                margin-bottom: 14px;
                font-size: 14px;
                font-weight: 800;
            }}
            .row {{
                display: flex;
                align-items: center;
                gap: 9px;
                margin: 12px 0;
            }}
            .check {{
                display: grid;
                place-items: center;
                width: 22px;
                height: 22px;
                flex: 0 0 22px;
                border-radius: 50%;
                background: var(--primary);
                color: white;
                font-size: 12px;
                font-weight: 800;
                animation: check 2.5s ease-in-out infinite;
            }}
            .line {{
                height: 7px;
                width: 125px;
                border-radius: 20px;
                background: var(--hover);
                overflow: hidden;
            }}
            .line::after {{
                content: "";
                display: block;
                width: 55%;
                height: 100%;
                border-radius: inherit;
                background: var(--primary);
                animation: progress 3.5s ease-in-out infinite;
            }}
            .line.short {{ width: 88px; }}
            .float-tag {{
                position: absolute;
                right: 0;
                bottom: 2px;
                z-index: 3;
                padding: 7px 9px;
                border: 1px solid var(--border);
                border-radius: 8px;
                background: var(--card);
                color: var(--muted);
                font-size: 9px;
                font-weight: 800;
                letter-spacing: .5px;
            }}
            .spark {{
                position: absolute;
                top: 15px;
                right: 22px;
                z-index: 3;
                font-size: 27px;
                color: var(--primary);
                animation: bob 3s ease-in-out infinite;
            }}
            @keyframes float {{
                0%, 100% {{ transform: translateY(0) rotate(-3deg); }}
                50% {{ transform: translateY(-9px) rotate(1deg); }}
            }}
            @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
            @keyframes pulse {{
                0%, 100% {{ opacity: .5; transform: scale(.92); }}
                50% {{ opacity: .9; transform: scale(1.08); }}
            }}
            @keyframes check {{
                0%, 100% {{ transform: scale(1); }}
                50% {{ transform: scale(1.08); }}
            }}
            @keyframes progress {{
                0%, 100% {{ width: 35%; }}
                50% {{ width: 90%; }}
            }}
            @keyframes bob {{
                0%, 100% {{ transform: translateY(0); }}
                50% {{ transform: translateY(-8px); }}
            }}
            @keyframes fade-in {{
                from {{ opacity: 0; transform: translateY(8px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
            @media (max-width: 600px) {{
                .hero {{ flex-direction: column; align-items: flex-start; gap: 0; }}
                .art {{ width: 100%; flex-basis: auto; min-width: 0; height: 220px; }}
                h1 {{ font-size: 30px; }}
            }}
            @media (prefers-reduced-motion: reduce) {{
                *, *::before, *::after {{ animation: none !important; }}
            }}
        </style>
        </head>
        <body>
            <section class="hero">
                <div class="hero-copy">
                    <div class="label">YOUR PERSONAL WORKSPACE</div>
                    <h1>Welcome to TaskFlow</h1>
                    <p>Organize your tasks, manage your priorities, and turn everyday plans into meaningful progress.</p>
                </div>
                <div class="art" aria-label="Animated task checklist">
                    <div class="glow"></div>
                    <div class="orbit"></div>
                    <div class="spark">✦</div>
                    <div class="board">
                        <div class="board-title">✓ Your task plan</div>
                        <div class="row"><div class="check">✓</div><div class="line"></div></div>
                        <div class="row"><div class="check">✓</div><div class="line short"></div></div>
                        <div class="row"><div class="check">✓</div><div class="line"></div></div>
                    </div>
                    <div class="float-tag">ORGANIZE · PLAN · ACHIEVE</div>
                </div>
            </section>
        </body>
        </html>
        """,
        height=275,
        scrolling=False,
    )


def display_task(task):
    with st.container(border=True):
        title_col, priority_col, status_col = st.columns(
            [4, 1.4, 1.5]
        )

        with title_col:
            st.markdown(f"### {task.title}")
            st.caption(f"Due date: {task.due_date or 'No deadline'}")

        with priority_col:
            priority_icon = {
                "High": "🔴",
                "Medium": "🟠",
                "Low": "🟢",
            }.get(task.priority, "⚪")

            st.markdown(f"**{priority_icon} {task.priority}**")

        with status_col:
            if task.completed:
                status = "✅ Completed"
            elif manager.is_overdue(task):
                status = "🔴 Overdue"
            else:
                status = "⏳ Pending"

            st.markdown(f"**{status}**")

        edit_col, complete_col, delete_col = st.columns(
            [1, 1.3, 1]
        )

        with edit_col:
            if st.button(
                "✏️ Edit",
                key=f"edit_{task.task_id}",
                use_container_width=True,
            ):
                st.session_state["editing_task_id"] = task.task_id
                st.rerun()

        with complete_col:
            if not task.completed:
                if st.button(
                    "✓ Complete",
                    key=f"complete_{task.task_id}",
                    use_container_width=True,
                ):
                    manager.complete_task(task.task_id)
                    st.rerun()

        with delete_col:
            if st.button(
                "🗑 Delete",
                key=f"delete_{task.task_id}",
                use_container_width=True,
            ):
                st.session_state[
                    f"confirm_delete_{task.task_id}"
                ] = True
                st.rerun()

        # EDIT TASK

        if st.session_state.get("editing_task_id") == task.task_id:
            st.divider()
            st.subheader("Edit Task")

            try:
                default_date = (
                    date.fromisoformat(str(task.due_date))
                    if task.due_date
                    else date.today()
                )
            except (ValueError, TypeError):
                default_date = date.today()

            with st.form(f"edit_form_{task.task_id}"):
                edited_title = st.text_input(
                    "Task title",
                    value=task.title,
                    key=f"edit_title_{task.task_id}",
                )

                edited_priority = st.selectbox(
                    "Priority",
                    PRIORITIES,
                    index=(
                        PRIORITIES.index(task.priority)
                        if task.priority in PRIORITIES
                        else 1
                    ),
                    key=f"edit_priority_{task.task_id}",
                )

                has_deadline = st.checkbox(
                    "Set a deadline",
                    value=bool(task.due_date),
                    key=f"edit_deadline_{task.task_id}",
                )

                edited_date = st.date_input(
                    "Due date",
                    value=default_date,
                    key=f"edit_date_{task.task_id}",
                )

                save_col, cancel_col = st.columns(2)

                with save_col:
                    save = st.form_submit_button(
                        "Save changes",
                        use_container_width=True,
                    )

                with cancel_col:
                    cancel = st.form_submit_button(
                        "Cancel",
                        use_container_width=True,
                    )

            if save:
                if not edited_title.strip():
                    st.error("Task title cannot be empty.")
                else:
                    new_due_date = (
                        str(edited_date) if has_deadline else None
                    )

                    updated = manager.update_task(
                        task.task_id,
                        edited_title.strip(),
                        edited_priority,
                        new_due_date,
                    )

                    if updated:
                        st.session_state.pop(
                            "editing_task_id", None
                        )
                        st.rerun()
                    else:
                        st.error("Could not update the task.")

            if cancel:
                st.session_state.pop("editing_task_id", None)
                st.rerun()

        # DELETE CONFIRMATION

        confirm_key = f"confirm_delete_{task.task_id}"

        if st.session_state.get(confirm_key):
            st.warning("Are you sure you want to delete this task?")

            yes_col, no_col = st.columns(2)

            with yes_col:
                if st.button(
                    "Yes, delete",
                    key=f"yes_{task.task_id}",
                    use_container_width=True,
                ):
                    manager.remove_task(task.task_id)
                    st.session_state.pop(confirm_key, None)

                    if (
                        st.session_state.get("editing_task_id")
                        == task.task_id
                    ):
                        st.session_state.pop(
                            "editing_task_id", None
                        )

                    st.rerun()

            with no_col:
                if st.button(
                    "Keep task",
                    key=f"no_{task.task_id}",
                    use_container_width=True,
                ):
                    st.session_state.pop(confirm_key, None)
                    st.rerun()


def display_tasks(tasks):
    if not tasks:
        empty_state(
            "No Tasks Found",
            "There are no tasks to display here yet.",
        )
        return

    for task in tasks:
        display_task(task)


# =====================================================
# PAGE HEADER
# =====================================================

if page == "Dashboard":
    show_hero()
else:
    st.title(page)
    st.caption(
        "Your personal workspace to organize and manage tasks."
    )


stats = get_stats()


# =====================================================
# DASHBOARD
# =====================================================

if page == "Dashboard":

    st.subheader("📊 Your Overview")

    metrics = [
        ("Total Tasks", stats["total"]),
        ("✓ Completed", stats["completed"]),
        ("◷ Pending", stats["pending"]),
        ("! Overdue", stats["overdue"]),
    ]

    columns = st.columns(4)

    for col, (label, value) in zip(columns, metrics):
        with col:
            st.metric(label, value)

    progress_col, priority_col = st.columns([1.15, 1])

    with progress_col:
        with st.container(border=True):
            st.subheader("🎯 Overall Progress")

            progress = max(
                0.0,
                min(100.0, float(stats["progress"])),
            )

            st.metric("Completion Rate", f"{progress:.1f}%")
            st.progress(progress / 100)

            st.caption(
                f'{stats["completed"]} of {stats["total"]} '
                "tasks completed"
            )

    with priority_col:
        with st.container(border=True):
            st.subheader("📊 Priority Overview")

            total = max(stats["total"], 1)
            priority_counts = {
                priority: count_priority(priority)
                for priority in PRIORITIES
            }

            for priority in PRIORITIES:
                left, right = st.columns([4, 1])

                with left:
                    st.write(priority)

                with right:
                    st.write(f"**{priority_counts[priority]}**")

                st.progress(priority_counts[priority] / total)

    st.write("")

    recent_col, add_col = st.columns([4, 1])

    with recent_col:
        st.subheader("◷ Recent Tasks")

    with add_col:
        st.button(
            "+ Add Task",
            type="primary",
            use_container_width=True,
            on_click=go_to_add_task,
        )

    display_tasks(manager.get_sorted_tasks()[:4])


# =====================================================
# ADD TASK
# =====================================================

elif page == "Add Task":

    st.subheader("Create a New Task")
    st.caption(
        "Add a clear title, priority, and optional deadline."
    )

    with st.container(border=True):
        with st.form("add_task_form", clear_on_submit=True):

            title = st.text_input(
                "Task title",
                placeholder="e.g. Complete Python assignment",
            )

            col1, col2 = st.columns(2)

            with col1:
                priority = st.selectbox(
                    "Priority",
                    PRIORITIES,
                )

            with col2:
                has_deadline = st.checkbox("Set a deadline")

                due_date = st.date_input(
                    "Due date",
                    value=date.today(),
                    min_value=date.today(),
                )

            submitted = st.form_submit_button(
                "+ Create Task",
                type="primary",
                use_container_width=True,
            )

    if submitted:
        if not title.strip():
            st.error("Task title cannot be empty.")
        else:
            manager.add_task(
                title.strip(),
                priority,
                str(due_date) if has_deadline else None,
            )

            st.success("Task created successfully!")
            st.rerun()


# =====================================================
# ALL TASKS
# =====================================================

elif page == "All Tasks":

    tasks = manager.get_sorted_tasks()

    st.caption(f"{len(tasks)} task(s) in your workspace.")

    display_tasks(tasks)


# =====================================================
# PENDING TASKS
# =====================================================

elif page == "Pending Tasks":

    tasks = manager.get_pending_tasks()

    st.caption(
        f"{len(tasks)} task(s) waiting for completion."
    )

    display_tasks(tasks)


# =====================================================
# COMPLETED TASKS
# =====================================================

elif page == "Completed Tasks":

    tasks = manager.get_completed_tasks()

    st.caption(f"{len(tasks)} task(s) completed.")

    display_tasks(tasks)


# =====================================================
# SEARCH TASKS
# =====================================================

elif page == "Search Tasks":

    keyword = st.text_input(
        "Search by title",
        placeholder="Enter a keyword...",
    )

    if keyword.strip():
        results = manager.search(keyword.strip())

        st.caption(f"{len(results)} result(s) found.")

        display_tasks(results)
    else:
        empty_state(
            "Search Your Workspace",
            "Enter a keyword to find tasks.",
        )


# =====================================================
# FILTER BY PRIORITY
# =====================================================

elif page == "Filter by Priority":

    priority = st.selectbox(
        "Select priority",
        PRIORITIES,
    )

    results = manager.filter_by_priority(priority)

    st.caption(
        f"{len(results)} {priority.lower()} priority task(s)."
    )

    display_tasks(results)


# =====================================================
# STATISTICS
# =====================================================

elif page == "Statistics":

    st.subheader("📈 Task Analytics")

    metrics = [
        ("Total Tasks", stats["total"]),
        ("Completed", stats["completed"]),
        ("Pending", stats["pending"]),
        ("Overdue", stats["overdue"]),
    ]

    columns = st.columns(4)

    for col, (label, value) in zip(columns, metrics):
        with col:
            st.metric(label, value)

    progress = max(
        0.0,
        min(100.0, float(stats["progress"])),
    )

    with st.container(border=True):
        st.subheader("Completion Rate")

        st.metric(
            "Tasks Completed",
            f"{progress:.1f}%",
        )

        st.progress(progress / 100)

    st.subheader("Priority Distribution")

    st.bar_chart(
        {
            "High": [count_priority("High")],
            "Medium": [count_priority("Medium")],
            "Low": [count_priority("Low")],
        }
    )
