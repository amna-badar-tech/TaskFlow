
import streamlit as st
from datetime import date
from task_manager import TaskManager

st.set_page_config(
    page_title="TaskFlow | Task Management",
    page_icon="✓",
    layout="wide"
)

# ---------------- TASK MANAGER ----------------

if "manager" not in st.session_state:
    st.session_state.manager = TaskManager()

manager = st.session_state.manager


# ---------------- THEME SETTINGS ----------------

themes = {
    "Sea Green": {
        "bg": "#D5EAE3", "sidebar": "#B5D9CE",
        "card": "#EAF5F1", "primary": "#087568",
        "secondary": "#A3D2C4", "text": "#104C45",
        "muted": "#426F67", "border": "#9BC8BA",
    },
    "Navy Blue": {
        "bg": "#D0DDF0", "sidebar": "#AFC4E2",
        "card": "#E8EFF9", "primary": "#173F78",
        "secondary": "#9DB7DE", "text": "#142F55",
        "muted": "#48658B", "border": "#91ACD2",
    },
    "Dark Theme": {
        "bg": "#111722", "sidebar": "#1B2638",
        "card": "#253247", "primary": "#8DB5FF",
        "secondary": "#3A506F", "text": "#F0F4FC",
        "muted": "#B0BED3", "border": "#40516A",
    },
}


# ---------------- SIDEBAR ----------------

with st.sidebar:
    st.title("✓ TaskFlow")
    st.caption("Smart task management")
    st.divider()

    st.subheader("🎨 Choose Theme")
    theme = st.selectbox(
        "Dashboard appearance",
        ["Dark Theme", "Sea Green", "Navy Blue"],
        key="app_theme"
    )

    st.divider()
    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Add Task",
            "All Tasks",
            "Pending Tasks",
            "Completed Tasks",
            "Search Tasks",
            "Filter by Priority",
            "Statistics",
        ]
    )

    st.divider()
    st.caption("TaskFlow v1.2")
    st.caption("Built with Python and Streamlit")


# ---------------- APPLY THEME ----------------

colors = themes[theme]
button_text = "#FFFFFF" if theme != "Dark Theme" else "#111722"

st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {colors["bg"]};
        color: {colors["text"]};
    }}
    [data-testid="stSidebar"] {{
        background-color: {colors["sidebar"]};
    }}
    [data-testid="stVerticalBlockBorderWrapper"] {{
        background-color: {colors["card"]};
        border: 1px solid {colors["border"]};
        border-radius: 12px;
    }}
    h1, h2, h3, h4, p, label,
    [data-testid="stMetricLabel"],
    [data-testid="stMetricValue"] {{
        color: {colors["text"]};
    }}
    [data-testid="stCaptionContainer"] {{
        color: {colors["muted"]};
    }}
    .stButton > button,
    .stFormSubmitButton > button {{
        background-color: {colors["primary"]};
        color: {button_text};
        border: 1px solid {colors["primary"]};
        border-radius: 9px;
        font-weight: 600;
    }}
    .stButton > button:hover,
    .stFormSubmitButton > button:hover {{
        background-color: {colors["secondary"]};
        color: {colors["text"]};
        border-color: {colors["primary"]};
    }}
    [data-testid="stProgressBar"] > div > div {{
        background-color: {colors["primary"]};
    }}
    [data-testid="stProgressBar"] > div {{
        background-color: {colors["secondary"]};
    }}
    [data-testid="stMetric"] {{
        background-color: {colors["card"]};
        padding: 12px;
        border-radius: 10px;
        border: 1px solid {colors["border"]};
    }}
    input, textarea {{
        border-color: {colors["border"]} !important;
    }}
    [data-baseweb="select"] > div {{
        border-color: {colors["border"]};
    }}
    </style>
    """,
    unsafe_allow_html=True
)


# ---------------- HELPER FUNCTIONS ----------------

def stats_now():
    return manager.statistics()


def priority_count(priority):
    return len(manager.filter_by_priority(priority))


def empty_state(title, message):
    with st.container(border=True):
        st.subheader(title)
        st.caption(message)


def display_task(task):
    with st.container(border=True):
        title_col, priority_col, status_col = st.columns(
            [4, 1.2, 1.5]
        )

        with title_col:
            st.markdown(f"**{task.title}**")
            st.caption(f"Due date: {task.due_date or 'No deadline'}")

        with priority_col:
            icon = {
                "High": "🔴",
                "Medium": "🟠",
                "Low": "🟢"
            }.get(task.priority, "⚪")
            st.write(f"{icon} **{task.priority}**")

        with status_col:
            if manager.is_overdue(task):
                st.warning("Overdue")
            elif task.completed:
                st.success("Completed")
            else:
                st.info("Pending")

        c1, c2, c3, _ = st.columns([1.2, 1, 1, 4])

        if not task.completed:
            with c1:
                if st.button(
                    "✓ Complete",
                    key=f"complete_{task.task_id}",
                    use_container_width=True
                ):
                    manager.complete_task(task.task_id)
                    st.rerun()

        with c2:
            if st.button(
                "✏️ Edit",
                key=f"edit_{task.task_id}",
                use_container_width=True
            ):
                st.session_state["editing_task_id"] = task.task_id
                st.rerun()

        with c3:
            if st.button(
                "Delete",
                key=f"delete_{task.task_id}",
                use_container_width=True
            ):
                st.session_state[f"confirm_delete_{task.task_id}"] = True
                st.rerun()

        # -------- EDIT TASK FORM --------

        if st.session_state.get("editing_task_id") == task.task_id:
            st.divider()
            st.subheader("✏️ Edit Task")

            with st.form(f"edit_form_{task.task_id}"):
                edited_title = st.text_input(
                    "Task title",
                    value=task.title
                )

                edited_priority = st.selectbox(
                    "Priority",
                    ["High", "Medium", "Low"],
                    index=["High", "Medium", "Low"].index(task.priority)
                )

                has_deadline = st.checkbox(
                    "Set a deadline",
                    value=bool(task.due_date)
                )

                try:
                    default_date = (
                        date.fromisoformat(task.due_date)
                        if task.due_date else date.today()
                    )
                except (ValueError, TypeError):
                    default_date = date.today()

                edited_date = st.date_input(
                    "Due date",
                    value=default_date
                )

                save_col, cancel_col = st.columns(2)

                with save_col:
                    save_clicked = st.form_submit_button(
                        "Save Changes",
                        use_container_width=True
                    )

                with cancel_col:
                    cancel_clicked = st.form_submit_button(
                        "Cancel",
                        use_container_width=True
                    )

            if save_clicked:
                if not edited_title.strip():
                    st.error("Task title cannot be empty.")
                else:
                    new_due_date = str(edited_date) if has_deadline else None

                    success = manager.update_task(
                        task.task_id,
                        edited_title.strip(),
                        edited_priority,
                        new_due_date
                    )

                    if success:
                        st.session_state.pop("editing_task_id", None)
                        st.success("Task updated successfully!")
                        st.rerun()
                    else:
                        st.error("Could not update the task.")

            if cancel_clicked:
                st.session_state.pop("editing_task_id", None)
                st.rerun()

        # -------- DELETE CONFIRMATION --------

        if st.session_state.get(
            f"confirm_delete_{task.task_id}", False
        ):
            st.warning("Are you sure you want to delete this task?")
            yes, no, _ = st.columns([1.2, 1.2, 4])

            with yes:
                if st.button(
                    "Yes, delete",
                    key=f"yes_{task.task_id}",
                    use_container_width=True
                ):
                    manager.remove_task(task.task_id)
                    st.session_state.pop(
                        f"confirm_delete_{task.task_id}", None
                    )
                    if st.session_state.get("editing_task_id") == task.task_id:
                        st.session_state.pop("editing_task_id", None)
                    st.rerun()

            with no:
                if st.button(
                    "Cancel",
                    key=f"no_{task.task_id}",
                    use_container_width=True
                ):
                    st.session_state.pop(
                        f"confirm_delete_{task.task_id}", None
                    )
                    st.rerun()


def display_tasks(tasks):
    if not tasks:
        empty_state(
            "No tasks found",
            "There are no tasks to display here yet."
        )
        return

    for task in tasks:
        display_task(task)


# ---------------- MAIN DASHBOARD ----------------

st.title("Welcome to TaskFlow 👋")
st.caption(
    "Your personal workspace to organize tasks, "
    "manage priorities, and track your progress."
)
st.caption(
    "Organize your work, track progress, "
    "and keep important tasks on schedule."
)

stats = stats_now()


# ---------------- DASHBOARD PAGE ----------------

if page == "Dashboard":
    st.subheader("Your Overview")
    cols = st.columns(4)

    labels = ["Total tasks", "Completed", "Pending", "Overdue"]
    values = [
        stats["total"], stats["completed"],
        stats["pending"], stats["overdue"]
    ]

    for col, label, value in zip(cols, labels, values):
        with col:
            st.metric(label, value)

    st.write("")
    progress_col, priority_col = st.columns([1.35, 1])

    with progress_col:
        with st.container(border=True):
            st.subheader("Overall Progress")
            progress = max(0.0, min(100.0, float(stats["progress"])))
            st.metric("Completion rate", f"{progress:.1f}%")
            st.progress(progress / 100)
            st.caption(
                f'{stats["completed"]} of {stats["total"]} tasks completed'
            )

    with priority_col:
        with st.container(border=True):
            st.subheader("Priority Overview")
            total = max(stats["total"], 1)

            for priority in ["High", "Medium", "Low"]:
                count = priority_count(priority)
                left, right = st.columns([3, 1])

                with left:
                    st.write(priority)
                with right:
                    st.write(f"**{count}**")

                st.progress(count / total)

    st.write("")
    recent_col, action_col = st.columns([3, 1])

    with recent_col:
        st.subheader("Recent Tasks")
        st.caption("A quick view of tasks that still need attention.")

    with action_col:
        if st.button("＋ Add Task", type="primary", use_container_width=True):
            st.session_state["show_add_message"] = True

    if st.session_state.get("show_add_message"):
        st.info("Choose **Add Task** from the sidebar to create a task.")

    pending = manager.get_pending_tasks()

    if pending:
        display_tasks(pending[:4])
        if len(pending) > 4:
            st.caption(
                "Showing 4 pending tasks. Open All Tasks to see everything."
            )
    elif stats["total"] == 0:
        empty_state(
            "No tasks yet",
            "Add your first task to start organizing your work."
        )
    else:
        empty_state(
            "All caught up",
            "You have no pending tasks right now. Great work!"
        )


# ---------------- ADD TASK PAGE ----------------

elif page == "Add Task":
    st.subheader("Create a New Task")
    st.caption("Give your task a clear title, priority, and deadline.")

    with st.container(border=True):
        with st.form("add_task_form", clear_on_submit=True):
            title = st.text_input(
                "Task title",
                placeholder="e.g. Complete Python assignment"
            )

            left, right = st.columns(2)

            with left:
                priority = st.selectbox("Priority", ["High", "Medium", "Low"])

            with right:
                add_deadline = st.checkbox("Set a deadline")
                due_date = st.date_input("Due date") if add_deadline else None

            submitted = st.form_submit_button(
                "＋ Add Task",
                type="primary",
                use_container_width=True
            )

    if submitted:
        if not title.strip():
            st.error("Task title cannot be empty.")
        else:
            manager.add_task(
                title.strip(),
                priority,
                str(due_date) if due_date else None
            )
            st.success("Task created successfully.")
            st.rerun()


# ---------------- ALL TASKS PAGE ----------------

elif page == "All Tasks":
    tasks = manager.get_sorted_tasks()
    st.subheader("All Tasks")
    st.caption(f"{len(tasks)} task(s) in your workspace.")
    display_tasks(tasks)


# ---------------- PENDING TASKS PAGE ----------------

elif page == "Pending Tasks":
    tasks = manager.get_pending_tasks()
    st.subheader("Pending Tasks")
    st.caption(f"{len(tasks)} task(s) waiting for completion.")
    display_tasks(tasks)


# ---------------- COMPLETED TASKS PAGE ----------------

elif page == "Completed Tasks":
    tasks = manager.get_completed_tasks()
    st.subheader("Completed Tasks")
    st.caption(f"{len(tasks)} task(s) successfully finished.")
    display_tasks(tasks)


# ---------------- SEARCH PAGE ----------------

elif page == "Search Tasks":
    st.subheader("Search Tasks")
    st.caption("Find a task by entering a word or phrase from its title.")

    keyword = st.text_input("Search by title", placeholder="Type a keyword...")

    if keyword.strip():
        results = manager.search(keyword.strip())
        st.caption(f"{len(results)} result(s) found.")
        display_tasks(results)
    else:
        empty_state(
            "Search your workspace",
            "Enter a keyword above to find matching tasks."
        )


# ---------------- FILTER PAGE ----------------

elif page == "Filter by Priority":
    st.subheader("Filter Tasks")
    st.caption("View tasks by their priority level.")

    priority = st.selectbox("Select priority", ["High", "Medium", "Low"])
    results = manager.filter_by_priority(priority)

    st.caption(f"{len(results)} {priority.lower()} priority task(s).")
    display_tasks(results)


# ---------------- STATISTICS PAGE ----------------

elif page == "Statistics":
    st.subheader("Task Analytics")
    st.caption("A concise overview of your current task activity.")

    cols = st.columns(4)
    labels = ["Total", "Completed", "Pending", "Overdue"]
    values = [
        stats["total"], stats["completed"],
        stats["pending"], stats["overdue"]
    ]

    for col, label, value in zip(cols, labels, values):
        with col:
            st.metric(label, value)

    st.write("")
    progress = max(0.0, min(100.0, float(stats["progress"])))

    with st.container(border=True):
        st.subheader("Completion Rate")
        st.metric("Tasks completed", f"{progress:.1f}%")
        st.progress(progress / 100)

    st.write("")
    st.subheader("Priority Distribution")
    st.bar_chart({
        "High": priority_count("High"),
        "Medium": priority_count("Medium"),
        "Low": priority_count("Low"),
    })


# ---------------- FOOTER ----------------

st.divider()
st.caption("TaskFlow · Python · Streamlit")
