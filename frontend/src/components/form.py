import streamlit as st
from datetime import datetime, timezone
from typing import Optional
from enum import Enum
from entities import Ticket


class Type(str, Enum):
    BUG = "bug"
    FEATURE = "feature"
    TASK = "task"


class Status(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in-progress"
    DONE = "done"


class Priority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


def fetch_assignees():  #!TODO ONCE ENDPOINT IS DONE TO FETCH USER DATA
    return ["", "Avellin", "Kai", "Ryan", "Xiaoyun"]


def create_ticket_form(current_user_id: str) -> Optional[dict]:
    """
    Creates a Streamlit form for ticket creation that matches the Pydantic schema.
    Returns the ticket data if form is submitted, None otherwise.
    """
    with st.form("ticket_creation_form"):
        st.header("Create New Ticket")

        # Core Fields
        title = st.text_input(
            "Title",
            max_chars=100,  # Matching Pydantic schema constraint
            help="Short description of the ticket (1-100 characters)",
        )

        description = st.text_area(
            "Description",
            height=150,
            help="Detailed description of the issue or feature",
        )

        # Type, Status, and Priority in three columns
        col1, col2, col3 = st.columns(3)

        with col1:
            ticket_type = st.selectbox(
                "Type",
                options=[t.value for t in Type],
                index=list(Type).index(Type.TASK),
                help="Type of the ticket",
            )

        with col2:
            status = st.selectbox(
                "Status",
                options=[s.value for s in Status],
                index=list(Status).index(Status.OPEN),
                help="Current status of the ticket",
            )

        with col3:
            priority = st.selectbox(
                "Priority",
                options=[p.value for p in Priority],
                index=list(Priority).index(Priority.MEDIUM),
                help="Priority level of the ticket",
            )

        # Assignment fields in two columns
        col1, col2 = st.columns(2)

        with col1:
            assignee_id = st.selectbox(
                "Assignee (optional)",
                options=fetch_assignees(),  # Replace with actual user IDs
                format_func=lambda x: "Unassigned" if x == "" else x,
                help="Person assigned to this ticket",
            )

        with col2:
            parent_ticket_id = st.text_input(
                "Parent Ticket ID (optional)",
                help="If this ticket is split from a larger ticket",
            )

        # Labels
        labels = st.text_input(
            "Labels (comma-separated) (optional)",
            help="Add labels like 'backend,bug,feature'",
        )

        submitted = st.form_submit_button("Create Ticket")

        if submitted:
            if not title or not description:
                st.error("Title and description are required!")
                return None

            if not title.strip():
                st.error("Title cannot be empty!")
                return None

            if not description.strip():
                st.error("Description cannot be empty!")
                return None

            current_time = datetime.now(timezone.utc)

            # Create ticket data matching Pydantic schema
            ticket_data = {
                "title": title.strip(),
                "description": description.strip(),
                "type": ticket_type,
                "status": status,
                "priority": priority,
                "assignee_id": assignee_id if assignee_id else None,
                "reporter_id": current_user_id,
                "created_at": current_time,
                "updated_at": current_time,
                "parent_ticket_id": (
                    parent_ticket_id if parent_ticket_id.strip() else None
                ),
                "labels": [
                    label.strip() for label in labels.split(",") if label.strip()
                ],
                "embedding": None,  # AI processing field, initialized as None
            }

            try:
                validated_ticket = Ticket(**ticket_data)
            except:
                st.debug(f"Ticket validation failed with {ticket_data}")
                return None

            return validated_ticket

    return None
