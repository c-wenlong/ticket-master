import streamlit as st
import pandas as pd
from datetime import datetime
from typing import List, Dict, Optional


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
            "semantic_hash",
            "embedding",
            "is_processed",
        }

        # Fields only editable by admins
        self.admin_only_fields = {"duplicate_ticket_ids", "parent_ticket_id"}

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
            "status",
            "priority",
            "assignee_id",
            "description",
            "labels",
            "created_at",
            "updated_at",
        ]
        df = df[columns]

        # Create expandable container for each ticket
        for idx, ticket in df.iterrows():
            with st.expander(f"🎫 {ticket['title']} ({ticket['id']})"):
                self._display_ticket_fields(ticket, idx)

    def _display_ticket_fields(self, ticket: pd.Series, idx: int):
        """Display and handle editing for individual ticket fields."""

        # Create columns for better layout
        col1, col2 = st.columns([2, 1])

        with col1:
            # Title and Description
            if self.can_edit_field("title", ticket.get("assignee_id")):
                new_title = st.text_input("Title", ticket["title"], key=f"title_{idx}")
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
            # Status and Priority
            if self.can_edit_field("status", ticket.get("assignee_id")):
                new_status = st.selectbox(
                    "Status",
                    options=["open", "in-progress", "done"],
                    index=["open", "in-progress", "done"].index(ticket["status"]),
                    key=f"status_{idx}",
                )
                if new_status != ticket["status"]:
                    self._handle_field_update(ticket["id"], "status", new_status)
            else:
                st.write(f"Status: {ticket['status']}")

            if self.can_edit_field("priority", ticket.get("assignee_id")):
                new_priority = st.selectbox(
                    "Priority",
                    options=["high", "medium", "low"],
                    index=["high", "medium", "low"].index(ticket["priority"]),
                    key=f"priority_{idx}",
                )
                if new_priority != ticket["priority"]:
                    self._handle_field_update(ticket["id"], "priority", new_priority)
            else:
                st.write(f"Priority: {ticket['priority']}")

        # Labels (shown as tags)
        if isinstance(ticket["labels"], list):
            st.write("Labels:", ", ".join(ticket["labels"]))

        # Metadata row
        meta_col1, meta_col2, meta_col3 = st.columns(3)
        with meta_col1:
            st.write(f"Created: {ticket['created_at'].strftime('%Y-%m-%d %H:%M')}")
        with meta_col2:
            st.write(f"Updated: {ticket['updated_at'].strftime('%Y-%m-%d %H:%M')}")
        with meta_col3:
            st.write(f"Assignee: {ticket.get('assignee_id', 'Unassigned')}")

    def _handle_field_update(self, ticket_id: str, field: str, new_value: any):
        """Handle updates to ticket fields."""
        if ticket_id not in st.session_state.edited_values:
            st.session_state.edited_values[ticket_id] = {}

        st.session_state.edited_values[ticket_id][field] = new_value

        # In a real application, you would update the database here
        st.write(f"Field '{field}' updated for ticket {ticket_id}")


def main():
    st.set_page_config(page_title="Ticket Table", page_icon="🎫", layout="wide")

    # Sample data
    sample_tickets = [
        {
            "id": "TICK-001",
            "title": "Implement Login",
            "description": "Create login page with OAuth",
            "status": "open",
            "priority": "high",
            "assignee_id": "USER-1",
            "reporter_id": "USER-2",
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "labels": ["frontend", "auth"],
            "is_processed": True,
        },
        {
            "id": "TICK-002",
            "title": "Database Backup",
            "description": "Setup automated backups",
            "status": "in-progress",
            "priority": "medium",
            "assignee_id": "USER-2",
            "reporter_id": "USER-1",
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "labels": ["backend", "ops"],
            "is_processed": True,
        },
    ]

    # Initialize table manager
    current_user_id = "USER-1"  # In real app, get from authentication
    is_admin = True  # In real app, get from user roles
    table_manager = TicketTableManager(current_user_id, is_admin)

    # Display table
    st.title("Ticket Management")
    table_manager.display_table(sample_tickets)

    # Show pending changes
    if st.session_state.get("edited_values"):
        st.write("Pending Changes:")
        st.json(st.session_state.edited_values)

        if st.button("Save Changes"):
            # In a real application, you would save to database here
            st.success("Changes saved!")
            st.session_state.edited_values = {}


if __name__ == "__main__":
    main()
