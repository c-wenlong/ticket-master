import streamlit as st
from components import KanbanBoard
from utils import SAMPLE_TICKETS

st.set_page_config(
    page_title="Sprint Kanban Board", layout="wide", initial_sidebar_state="collapsed", page_icon="🎯"
)

if "show_form" not in st.session_state:
    st.session_state.show_form = False

# Initialize and render Kanban board
board = KanbanBoard(SAMPLE_TICKETS)
board.render()
# st.json(st.session_state.tickets)


def metrics():
    from entities import Status, Priority, Type
    import pandas as pd
    from datetime import datetime, timezone
    from collections import Counter

    # Add metrics and analytics at the bottom
    st.divider()

    # First row of metrics
    col1, col2, col3, col4 = st.columns(4)

    # Calculate metrics
    tickets = st.session_state.tickets.values()
    total_tickets = len(tickets)
    completed_tickets = sum(1 for t in tickets if t["status"] == Status.DONE.value)
    priority_counts = Counter(t["status"] for t in tickets)
    high_priority = sum(1 for t in tickets if t["priority"] == Priority.HIGH.value)

    with col1:
        st.metric(
            "Total Tickets", total_tickets, help="Total number of tickets in the sprint"
        )
    with col2:
        completion_rate = (
            (completed_tickets / total_tickets * 100) if total_tickets > 0 else 0
        )
        st.metric(
            "Sprint Progress",
            f"{completion_rate:.1f}%",
            help="Percentage of tickets completed",
        )
    with col3:
        st.metric(
            "High Priority Tickets",
            high_priority,
            help="Number of high priority tickets",
        )
    with col4:
        unassigned = sum(1 for t in tickets if not t["assignee_id"])
        st.metric(
            "Unassigned Tickets",
            unassigned,
            help="Number of tickets without an assignee",
        )

    # Second row of analytics
    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        # Tickets by type
        st.subheader("Tickets by Type")
        type_counts = Counter(t["type"] for t in tickets)
        type_df = pd.DataFrame(
            {"Type": list(type_counts.keys()), "Count": list(type_counts.values())}
        )
        st.bar_chart(type_df.set_index("Type"))

    with col2:
        # Tickets by priority
        st.subheader("Priority Distribution")
        priority_counts = Counter(t["priority"] for t in tickets)
        priority_df = pd.DataFrame(
            {
                "Priority": list(priority_counts.keys()),
                "Count": list(priority_counts.values()),
            }
        )
        st.bar_chart(priority_df.set_index("Priority"))

    # Third row - Additional insights
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Recent Updates")
        recent_tickets = sorted(tickets, key=lambda x: x["updated_at"], reverse=True)[
            :5
        ]

        for ticket in recent_tickets:
            st.markdown(
                f"""
                - **{ticket['id']}**: {ticket['title']}  
                  *Last updated: {ticket['updated_at'].strftime('%Y-%m-%d %H:%M')}*
                """
            )

    with col2:
        st.subheader("Label Distribution")
        all_labels = Counter(label for ticket in tickets for label in ticket["labels"])
        if all_labels:
            labels_df = pd.DataFrame(
                {"Label": list(all_labels.keys()), "Count": list(all_labels.values())}
            )
            st.bar_chart(labels_df.set_index("Label"))
        else:
            st.info("No labels have been added to tickets yet.")
