import streamlit as st
from task_manager import TaskManager


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="TaskFlow | Task Management",
    page_icon="✓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* ---------- GLOBAL ---------- */

    .stApp {
        background: #f6f8fc;
    }

    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }


    /* ---------- SIDEBAR ---------- */

    section[data-testid="stSidebar"] {
        background: #0f2f52;
    }

    section[data-testid="stSidebar"] * {
        color: white;
    }


    /* ---------- HEADER ---------- */

    .brand-title {
        font-size: 38px;
        font-weight: 750;
        color: #123a63;
        margin-bottom: 0;
    }

    .brand-subtitle {
        color: #64748b;
        font-size: 16px;
        margin-top: 2px;
    }


    /* ---------- STAT CARDS ---------- */

    .stat-card {
        background: white;
        border: 1px solid #e5eaf1;
        border-radius: 14px;
        padding: 20px;
        min-height: 125px;
        box-shadow: 0 2px 8px rgba(15, 47, 82, 0.04);
    }

    .stat-label {
        color: #64748b;
        font-size: 14px;
        font-weight: 600;
    }

    .stat-value {
        color: #123a63;
        font-size: 32px;
        font-weight: 750;
        margin-top: 8px;
    }


    /* ---------- SECTION HEADINGS ---------- */

    .section-title {
        color: #123a63;
        font-size: 21px;
        font-weight: 700;
        margin-bottom: 12px;
    }


    /* ---------- TASK CARDS ---------- */

    .task-card {
        background: white;
        border: 1px solid #e5eaf1;
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 14px;
        box-shadow: 0 2px 8px rgba(15, 47, 82, 0.04);
    }

    .task-title {
        color: #172033;
        font-size: 18px;
        font-weight: 700;
    }

    .task-meta {
        color: #64748b;
        font-size: 14px;
        margin-top: 6px;
    }


    /* ---------- BADGES ---------- */

    .badge-high {
        background: #fee2e2;
        color: #b91c1c;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
    }

    .badge-medium {
        background: #fef3c7;
        color: #92400e;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
    }

    .badge-low {
        background: #dcfce7;
        color: #166534;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
    }


    /* ---------- PROGRESS CARD ---------- */

    .progress-card {
        background: white;
        border: 1px solid #e5eaf1;
        border-radius: 14px;
        padding: 22px;
        box-shadow: 0 2px 8px rgba(15, 47, 82, 0.04);
    }


    /* ---------- BUTTONS ---------- */

    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
    }


    /* ---------- FOOTER ---------- */

    .footer {
        text-align: center;
        color: #94a3b8;
        font-size: 13px;
        margin-top: 40px;
        padding-top: 20px;
        border-top: 1px solid #e5eaf1;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# TASK MANAGER
# =========================================================

if "manager" not in st.session_state:
    st.session_state.manager = TaskManager()

manager = st.session_state.manager


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def get_priority_badge(priority):
    """Return styled priority badge."""

    if priority == "High":
        return '<span class="badge-high">HIGH</span>'

    if priority == "Medium":
        return '<span class="badge-medium">MEDIUM</span>'

    return '<span class="badge-low">LOW</span>'


def display_task(task):
    """Display a single task card."""

    with st.container(border=True):

        col1, col2 = st.columns([5, 2])

        with col1:

            status = (
                "✓ Completed"
                if task.completed
                else "○ Pending"
            )

            st.markdown(
                f'<div class="task-title">'
                f'{task.title}</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div class="task-meta">'
                f'Status: {status}'
                f' &nbsp; • &nbsp; '
                f'Due: {task.due_date or "No deadline"}'
                f'</div>',
                unsafe_allow_html=True
            )

            if manager.is_overdue(task):

                st.warning(
                    "This task is overdue."
                )

        with col2:

            st.markdown(
                get_priority_badge(
                    task.priority
                ),
                unsafe_allow_html=True
            )

            st.write("")

            action1, action2 = st.columns(2)

            with action1:

                if not task.completed:

                    if st.button(
                        "Complete",
                        key=f"complete_{task.task_id}",
                        use_container_width=True
                    ):

                        manager.complete_task(
                            task.task_id
                        )

                        st.rerun()

            with action2:

                if st.button(
                    "Delete",
                    key=f"delete_{task.task_id}",
                    use_container_width=True
                ):

                    st.session_state[
                        f"confirm_delete_{task.task_id}"
                    ] = True

                    st.rerun()

            if st.session_state.get(
                f"confirm_delete_{task.task_id}",
                False
            ):

                st.warning(
                    "Are you sure you want to "
                    "delete this task?"
                )

                yes_col, no_col = st.columns(2)

                with yes_col:

                    if st.button(
                        "Yes, Delete",
                        key=f"yes_{task.task_id}",
                        use_container_width=True
                    ):

                        manager.remove_task(
                            task.task_id
                        )

                        st.session_state.pop(
                            f"confirm_delete_{task.task_id}",
                            None
                        )

                        st.rerun()

                with no_col:

                    if st.button(
                        "Cancel",
                        key=f"no_{task.task_id}",
                        use_container_width=True
                    ):

                        st.session_state.pop(
                            f"confirm_delete_{task.task_id}",
                            None
                        )

                        st.rerun()


def display_tasks(tasks):

    if not tasks:

        st.info(
            "No tasks found."
        )

        return

    for task in tasks:
        display_task(task)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            font-size:28px;
            font-weight:750;
            margin-bottom:4px;
        ">
            ✓ TaskFlow
        </div>
        """,
        unsafe_allow_html=True
    )

    st.caption("Smart Task Management")

    st.divider()

    st.markdown("### NAVIGATION")

    menu = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Add Task",
            "All Tasks",
            "Pending Tasks",
            "Completed Tasks",
            "Search Tasks",
            "Filter by Priority",
            "Statistics"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.caption("TaskFlow v1.0")
    st.caption("Python • Streamlit")


# =========================================================
# STATISTICS
# =========================================================

stats = manager.statistics()


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="brand-title">TaskFlow</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="brand-subtitle">'
    'Organize your work. Track your progress. Stay productive.'
    '</div>',
    unsafe_allow_html=True
)

st.write("")


# =========================================================
# STAT CARDS
# =========================================================

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-label">TOTAL TASKS</div>
            <div class="stat-value">{stats["total"]}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:

    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-label">COMPLETED</div>
            <div class="stat-value">{stats["completed"]}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:

    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-label">PENDING</div>
            <div class="stat-value">{stats["pending"]}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c4:

    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-label">OVERDUE</div>
            <div class="stat-value">{stats["overdue"]}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.write("")


# =========================================================
# PROGRESS
# =========================================================

st.markdown(
    '<div class="section-title">Overall Progress</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="progress-card">',
    unsafe_allow_html=True
)

st.progress(
    stats["progress"] / 100
)

st.write(
    f"**{stats['progress']:.1f}%** completed "
    f"• {stats['completed']} of "
    f"{stats['total']} tasks finished"
)

st.markdown(
    '</div>',
    unsafe_allow_html=True
)


st.write("")


# =========================================================
# DASHBOARD
# =========================================================

if menu == "Dashboard":

    st.markdown(
        '<div class="section-title">'
        'Your Workspace'
        '</div>',
        unsafe_allow_html=True
    )

    if stats["overdue"] > 0:

        st.warning(
            f"You have {stats['overdue']} "
            "overdue task(s) that need attention."
        )

    elif stats["pending"] > 0:

        st.info(
            f"You currently have {stats['pending']} "
            "pending task(s)."
        )

    else:

        st.success(
            "All tasks are completed. Great work!"
        )

    st.write("")

    left, right = st.columns(2)

    with left:

        st.markdown(
            '<div class="section-title">'
            'Pending Tasks'
            '</div>',
            unsafe_allow_html=True
        )

        pending = manager.get_pending_tasks()

        if pending:

            display_tasks(
                pending[:3]
            )

            if len(pending) > 3:

                st.caption(
                    f"+ {len(pending) - 3} more "
                    "pending task(s)"
                )

        else:

            st.success(
                "No pending tasks."
            )

    with right:

        st.markdown(
            '<div class="section-title">'
            'Priority Overview'
            '</div>',
            unsafe_allow_html=True
        )

        high = len(
            manager.filter_by_priority("High")
        )

        medium = len(
            manager.filter_by_priority("Medium")
        )

        low = len(
            manager.filter_by_priority("Low")
        )

        st.metric(
            "High Priority",
            high
        )

        st.metric(
            "Medium Priority",
            medium
        )

        st.metric(
            "Low Priority",
            low
        )


# =========================================================
# ADD TASK
# =========================================================

elif menu == "Add Task":

    st.header("Create New Task")

    st.caption(
        "Add a task with priority and deadline."
    )

    st.write("")

    with st.container(border=True):

        title = st.text_input(
            "Task Title",
            placeholder="e.g. Complete Python project"
        )

        priority = st.selectbox(
            "Priority",
            [
                "High",
                "Medium",
                "Low"
            ]
        )

        due_date = st.date_input(
            "Due Date"
        )

        st.write("")

        if st.button(
            "＋ Add Task",
            type="primary",
            use_container_width=True
        ):

            if not title.strip():

                st.error(
                    "Task title cannot be empty."
                )

            else:

                manager.add_task(
                    title.strip(),
                    priority,
                    str(due_date)
                )

                st.success(
                    "Task created successfully!"
                )

                st.rerun()


# =========================================================
# ALL TASKS
# =========================================================

elif menu == "All Tasks":

    st.header("All Tasks")

    st.caption(
        f"{stats['total']} task(s) in your workspace."
    )

    display_tasks(
        manager.get_sorted_tasks()
    )


# =========================================================
# PENDING TASKS
# =========================================================

elif menu == "Pending Tasks":

    st.header("Pending Tasks")

    pending = manager.get_pending_tasks()

    st.caption(
        f"{len(pending)} pending task(s)."
    )

    display_tasks(pending)


# =========================================================
# COMPLETED TASKS
# =========================================================

elif menu == "Completed Tasks":

    st.header("Completed Tasks")

    completed = manager.get_completed_tasks()

    st.caption(
        f"{len(completed)} completed task(s)."
    )

    display_tasks(completed)


# =========================================================
# SEARCH
# =========================================================

elif menu == "Search Tasks":

    st.header("Search Tasks")

    keyword = st.text_input(
        "Search by title",
        placeholder="Type a keyword..."
    )

    if keyword.strip():

        results = manager.search(
            keyword
        )

        st.caption(
            f"{len(results)} result(s) found."
        )

        display_tasks(results)

    else:

        st.info(
            "Enter a keyword to search your tasks."
        )


# =========================================================
# FILTER
# =========================================================

elif menu == "Filter by Priority":

    st.header("Filter Tasks")

    priority = st.selectbox(
        "Select Priority",
        [
            "High",
            "Medium",
            "Low"
        ]
    )

    results = manager.filter_by_priority(
        priority
    )

    st.caption(
        f"{len(results)} {priority.lower()} "
        "priority task(s)."
    )

    display_tasks(results)


# =========================================================
# STATISTICS
# =========================================================

elif menu == "Statistics":
    
    st.header("Task Analytics")

    st.caption(
        "Overview of your current task activity."
    )

    st.write("")

    a, b, c, d = st.columns(4)

    with a:
        st.metric(
            "Total",
            stats["total"]
        )

    with b:
        st.metric(
            "Completed",
            stats["completed"]
        )

    with c:
        st.metric(
            "Pending",
            stats["pending"]
        )

    with d:
        st.metric(
            "Overdue",
            stats["overdue"]
        )

    st.write("")

    st.subheader("Completion Rate")

    st.progress(
        stats["progress"] / 100
    )

    st.write(
        f"{stats['progress']:.1f}%"
    )

    st.subheader("Priority Distribution")

    high = len(
        manager.filter_by_priority("High")
    )

    medium = len(
        manager.filter_by_priority("Medium")
    )

    low = len(
        manager.filter_by_priority("Low")
    )

    chart_data = {
        "High": high,
        "Medium": medium,
        "Low": low
    }

    st.bar_chart(chart_data)


# =========================================================
# FOOTER
# =========================================================
 
st.markdown(
    """
    <div class="footer">
        TaskFlow • Professional Task Management System
        <br>
        Built with Python and Streamlit
    </div>
    """,
    unsafe_allow_html=True
)
