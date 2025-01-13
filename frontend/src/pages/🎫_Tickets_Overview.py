import streamlit as st
from utils import read_json
from components import ticket_table
from utils import SAMPLE_TICKETS


st.set_page_config(
    page_title="Tickets Overview",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="🎫",
)


def initialize_session_state():
    """Initialize session state variables"""
    if "current_user" not in st.session_state:
        st.session_state.current_user = "kai"  # Default user for demo
    if "is_admin" not in st.session_state:
        st.session_state.is_admin = True  # Default admin status for demo


def main():
    initialize_session_state()

    # Page Header
    st.title("🎫 All Tickets")

    # User context display
    with st.sidebar:
        st.header("User Context")
        # In a real app, these would come from authentication
        st.session_state.current_user = st.selectbox(
            "Current User", options=["kai", "ryan", "avellin"], index=0
        )
        st.session_state.is_admin = st.checkbox("Is Admin", value=True)

        st.divider()
        st.write("Current User:", st.session_state.current_user)
        st.write("Admin Status:", "✅" if st.session_state.is_admin else "❌")

    # Load sample data
    tickets = SAMPLE_TICKETS

    if not tickets:
        st.warning("No tickets found in sample data.")
        return

    # Display ticket statistics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Tickets", len(tickets))
    with col2:
        high_priority = sum(1 for t in tickets if t.priority == "high")
        st.metric("High Priority", high_priority)
    with col3:
        in_progress = sum(1 for t in tickets if t.status == "in-progress")
        st.metric("In Progress", in_progress)
    with col4:
        my_tickets = sum(
            1 for t in tickets if t.assignee_id == st.session_state.current_user
        )
        st.metric("My Tickets", my_tickets)

    # Add filters
    with st.expander("🔍 Filters", expanded=True):
        col1, col2, col3 = st.columns(3)

        with col1:
            filter_status = st.multiselect(
                "Status", options=list(set(t.status for t in tickets))
            )

        with col2:
            filter_priority = st.multiselect(
                "Priority", options=list(set(t.priority for t in tickets))
            )

        with col3:
            filter_assigned = st.multiselect(
                "Assignee", options=list(set(t.assignee_id for t in tickets))
            )

    # Apply filters
    filtered_tickets = tickets
    if filter_status:
        filtered_tickets = [t for t in filtered_tickets if t.status in filter_status]
    if filter_priority:
        filtered_tickets = [
            t for t in filtered_tickets if t.priority in filter_priority
        ]
    if filter_assigned:
        filtered_tickets = [
            t for t in filtered_tickets if t.assignee_id in filter_assigned
        ]

    # Display table
    ticket_table(filtered_tickets)

    # Handle pending changes
    if st.session_state.get("edited_values"):
        st.divider()
        col1, col2 = st.columns([3, 1])

        with col1:
            st.write("Pending Changes:")
            st.json(st.session_state.edited_values)

        with col2:
            st.write("")
            st.write("")
            if st.button("💾 Save Changes", type="primary"):
                # In a real application, you would save to database here
                st.success("Changes saved!")
                st.session_state.edited_values = {}
                st.rerun()


if __name__ == "__main__":
    main()
