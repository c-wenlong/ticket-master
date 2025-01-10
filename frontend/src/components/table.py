import streamlit as st
import pandas as pd
from datetime import datetime, timezone
from typing import List, Dict, Optional
from entities import Status, Priority, Type


class TicketTableManager:
    def __init__(self, current_user_id: str, is_admin: bool = False):
        self.current_user_id = current_user_id
        self.is_admin = is_admin

        # Define field permissions
        self.read_only_fields = {
            "id",
            "reporter_id",
            "created_at",
            "updated_at",
            "embedding",
        }

        # Fields only editable by admins
        self.admin_only_fields = {"parent_ticket_id"}

        # Fields editable by ticket assignee
        self.assignee_fields = {"status", "description"}

        # Fields editable by anyone
        self.public_fields = {"labels"}

    def can_edit_field(
        self, field_name: str, ticket_assignee_id: Optional[str]
    ) -> bool:
        """Determine if current user can edit a specific field."""
        if field_name in self.read_only_fields:
            return False

        if field_name in self.admin_only_fields:
            return self.is_admin

        if field_name in self.assignee_fields:
            return self.is_admin or self.current_user_id == ticket_assignee_id

        return True

    def display_table(self, tickets: List[Dict]):
        """Display an editable table of tickets."""
        if not tickets:
            st.warning("No tickets found.")
            return

        # Initialize session state for edited values
        if "edited_values" not in st.session_state:
            st.session_state.edited_values = {}

        # Convert tickets to DataFrame for display
        df = pd.DataFrame(tickets)

        # Sort columns for consistent display
        columns = [
            "id",
            "title",
            "type",
            "status",
            "priority",
            "assignee_id",
            "reporter_id",
            "description",
            "labels",
            "created_at",
            "updated_at",
            "parent_ticket_id",
        ]
        df = df[columns]

        # Create expandable container for each ticket
        for idx, ticket in df.iterrows():
            with st.expander(
                f"🎫 {ticket['title']} ({ticket['id']}) - {ticket['type']}",
                expanded=False,
            ):
                self._display_ticket_fields(ticket, idx)

    def _display_ticket_fields(self, ticket: pd.Series, idx: int):
        """Display and handle editing for individual ticket fields."""
        # Create columns for better layout
        col1, col2 = st.columns([2, 1])

        with col1:
            # Title and Description
            if self.can_edit_field("title", ticket.get("assignee_id")):
                new_title = st.text_input(
                    "Title", ticket["title"], key=f"title_{idx}", max_chars=100
                )
                if new_title != ticket["title"]:
                    self._handle_field_update(ticket["id"], "title", new_title)

            st.write("Description:")
            if self.can_edit_field("description", ticket.get("assignee_id")):
                new_desc = st.text_area("", ticket["description"], key=f"desc_{idx}")
                if new_desc != ticket["description"]:
                    self._handle_field_update(ticket["id"], "description", new_desc)
            else:
                st.write(ticket["description"])

        with col2:
            # Type, Status and Priority
            if self.can_edit_field("type", ticket.get("assignee_id")):
                new_type = st.selectbox(
                    "Type",
                    options=[t.value for t in Type],
                    index=[t.value for t in Type].index(ticket["type"]),
                    key=f"type_{idx}",
                )
                if new_type != ticket["type"]:
                    self._handle_field_update(ticket["id"], "type", new_type)
            else:
                st.write(f"Type: {ticket['type']}")

            if self.can_edit_field("status", ticket.get("assignee_id")):
                new_status = st.selectbox(
                    "Status",
                    options=[s.value for s in Status],
                    index=[s.value for s in Status].index(ticket["status"]),
                    key=f"status_{idx}",
                )
                if new_status != ticket["status"]:
                    self._handle_field_update(ticket["id"], "status", new_status)
            else:
                st.write(f"Status: {ticket['status']}")

            if self.can_edit_field("priority", ticket.get("assignee_id")):
                new_priority = st.selectbox(
                    "Priority",
                    options=[p.value for p in Priority],
                    index=[p.value for p in Priority].index(ticket["priority"]),
                    key=f"priority_{idx}",
                )
                if new_priority != ticket["priority"]:
                    self._handle_field_update(ticket["id"], "priority", new_priority)
            else:
                st.write(f"Priority: {ticket['priority']}")

            # Assignment
            if self.can_edit_field("assignee_id", ticket.get("assignee_id")):
                new_assignee = st.text_input(
                    "Assignee",
                    value=ticket.get("assignee_id", ""),
                    key=f"assignee_{idx}",
                )
                if new_assignee != ticket.get("assignee_id"):
                    self._handle_field_update(ticket["id"], "assignee_id", new_assignee)
            else:
                st.write(f"Assignee: {ticket.get('assignee_id', 'Unassigned')}")

        # Labels (shown as tags)
        if self.can_edit_field("labels", ticket.get("assignee_id")):
            current_labels = (
                ", ".join(ticket["labels"])
                if isinstance(ticket["labels"], list)
                else ""
            )
            new_labels = st.text_input(
                "Labels (comma-separated)", value=current_labels, key=f"labels_{idx}"
            )
            new_labels_list = [
                label.strip() for label in new_labels.split(",") if label.strip()
            ]
            if new_labels_list != ticket["labels"]:
                self._handle_field_update(ticket["id"], "labels", new_labels_list)
        else:
            st.write(
                "Labels:",
                (
                    ", ".join(ticket["labels"])
                    if isinstance(ticket["labels"], list)
                    else ""
                ),
            )

        # Parent ticket (admin only)
        if self.is_admin:
            new_parent = st.text_input(
                "Parent Ticket ID",
                value=ticket.get("parent_ticket_id", ""),
                key=f"parent_{idx}",
            )
            if new_parent != ticket.get("parent_ticket_id"):
                self._handle_field_update(ticket["id"], "parent_ticket_id", new_parent)

        # Metadata row
        meta_col1, meta_col2, meta_col3 = st.columns(3)
        with meta_col1:
            created_at = ticket["created_at"]
            if isinstance(created_at, str):
                created_at = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
            st.write(f"Created: {created_at.strftime('%Y-%m-%d %H:%M')}")
        with meta_col2:
            updated_at = ticket["updated_at"]
            if isinstance(updated_at, str):
                updated_at = datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
            st.write(f"Updated: {updated_at.strftime('%Y-%m-%d %H:%M')}")
        with meta_col3:
            st.write(f"Reporter: {ticket['reporter_id']}")

    def _handle_field_update(self, ticket_id: str, field: str, new_value: any):
        """Handle updates to ticket fields."""
        if ticket_id not in st.session_state.edited_values:
            st.session_state.edited_values[ticket_id] = {}

        st.session_state.edited_values[ticket_id][field] = new_value
        st.session_state.edited_values[ticket_id]["updated_at"] = datetime.now(
            timezone.utc
        )

        # In a real application, you would update the database here
        st.write(f"Field '{field}' updated for ticket {ticket_id}")
