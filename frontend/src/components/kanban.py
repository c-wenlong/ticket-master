from typing import Any, Dict
import streamlit as st
from datetime import datetime, timezone
from uuid import uuid4
from entities import Ticket, Status, Priority, Type
from .card import KanbanCard


class KanbanBoard:
    def __init__(self, tickets):
        # Initialize columns using Status enum
        self.columns = [status.value for status in Status]

        # Initialize session state for tickets if not exists
        if "tickets" not in st.session_state:
            st.session_state.tickets = tickets

        if "dragging" not in st.session_state:
            st.session_state.dragging = None

        self.ticket_colors = {
            Priority.HIGH.value: "#ff6b6b",  # Red for high priority
            Priority.MEDIUM.value: "#ffd93d",  # Yellow for medium priority
            Priority.LOW.value: "#6bff6b",  # Green for low priority
        }

    def unpack_ticket(ticket: Ticket) -> Dict[str, Any]:
        """
        Converts a Ticket model into a dictionary format suitable for the Kanban board.
        """
        return {
            "id": ticket.id,
            "title": ticket.title,
            "description": ticket.description,
            "type": ticket.type.value,
            "status": ticket.status.value,
            "priority": ticket.priority.value,
            "assignee_id": ticket.assignee_id,
            "reporter_id": ticket.reporter_id,
            "created_at": ticket.created_at,
            "updated_at": ticket.updated_at,
            "embedding": ticket.embedding,
            "parent_ticket_id": ticket.parent_ticket_id,
            "labels": ticket.labels,
        }

    def create_ticket_card(self, ticket_data, column):
        """Create a visual card for a ticket."""
        card = st.container()

        with card:
            # Convert ticket data to KanbanCard instance
            card = KanbanCard(
                ticket_id=ticket_data["id"],
                title=ticket_data["title"],
                description=ticket_data["description"],
                ticket_type=ticket_data["type"],
                priority=ticket_data["priority"],
                status=ticket_data["status"],
                assignee_id=ticket_data["assignee_id"],
                reporter_id=ticket_data["reporter_id"],
                labels=ticket_data["labels"],
                created_at=ticket_data.get("created_at"),
                updated_at=ticket_data.get("updated_at"),
                parent_ticket_id=ticket_data.get("parent_ticket_id"),
                embedding=ticket_data.get("embedding"),
            )

            # Render the card with proper column information
            card.render(
                current_column=column,
                available_columns=self.columns,
                on_move=self.move_ticket,
            )

    def move_ticket(self, ticket_id: str, new_status: str):
        """Move a ticket to a new status column."""
        if ticket_id in st.session_state.tickets:
            ticket = st.session_state.tickets[ticket_id]
            ticket["status"] = new_status
            ticket["updated_at"] = datetime.now(timezone.utc)
            st.rerun()

    def render(self):
        """Render the Kanban board."""
        st.title("📋 Sprint Kanban Board")

        # Add filters in the sidebar
        with st.sidebar:
            st.header("Filters")
            selected_assignee = st.multiselect(
                "Assignee",
                options=list(
                    set(t["assignee_id"] for t in st.session_state.tickets.values())
                ),
                default=[],
            )

            selected_type = st.multiselect(
                "Type",
                options=[t.value for t in Type],
                default=[],
            )

            selected_priority = st.multiselect(
                "Priority",
                options=[p.value for p in Priority],
                default=[],
            )

            selected_labels = st.multiselect(
                "Labels",
                options=list(
                    set(
                        label
                        for t in st.session_state.tickets.values()
                        for label in t["labels"]
                    )
                ),
                default=[],
            )

        # Create columns for each status
        cols = st.columns(len(self.columns), gap="small")

        # Display column headers with ticket counts
        for col, status in zip(cols, self.columns):
            tickets_in_column = [
                t for t in st.session_state.tickets.values() if t["status"] == status
            ]
            col.markdown(f"### {status} ({len(tickets_in_column)})")

        # Filter tickets based on sidebar selections
        filtered_tickets = st.session_state.tickets.values()
        if selected_assignee:
            filtered_tickets = [
                t for t in filtered_tickets if t["assignee_id"] in selected_assignee
            ]
        if selected_type:
            filtered_tickets = [
                t for t in filtered_tickets if t["type"] in selected_type
            ]
        if selected_priority:
            filtered_tickets = [
                t for t in filtered_tickets if t["priority"] in selected_priority
            ]
        if selected_labels:
            filtered_tickets = [
                t
                for t in filtered_tickets
                if any(label in t["labels"] for label in selected_labels)
            ]

        # Display tickets in their respective columns
        for col, status in zip(cols, self.columns):
            with col:
                status_tickets = [t for t in filtered_tickets if t["status"] == status]
                for ticket in status_tickets:
                    self.create_ticket_card(
                        ticket, status
                    )  # Pass both ticket and current status

                # Add "Add Ticket" button at bottom of Open column
                if status == Status.OPEN.value:
                    if st.button("+ Add Ticket", key=f"add_{status}"):
                        self.show_add_ticket_form()

    def show_add_ticket_form(self):
        """Show form to add a new ticket."""
        with st.form("add_ticket_form"):
            st.subheader("Add New Ticket")

            title = st.text_input("Title", max_chars=100)
            description = st.text_area("Description")
            ticket_type = st.selectbox("Type", [t.value for t in Type])
            priority = st.selectbox("Priority", [p.value for p in Priority])
            assignee_id = st.text_input("Assignee ID")
            reporter_id = st.text_input("Reporter ID")
            parent_ticket_id = st.text_input("Parent Ticket ID (optional)")
            labels = st.text_input("Labels (comma-separated)")

            if st.form_submit_button("Create Ticket"):
                if not title or not description or not reporter_id:
                    st.error("Title, description and reporter ID are required!")
                    return

                new_id = f"TICKET-{uuid4().hex[:8].upper()}"
                current_time = datetime.now(timezone.utc)

                st.session_state.tickets[new_id] = {
                    "id": new_id,
                    "title": title,
                    "description": description,
                    "type": ticket_type,
                    "status": Status.OPEN.value,
                    "priority": priority,
                    "assignee_id": assignee_id if assignee_id else None,
                    "reporter_id": reporter_id,
                    "created_at": current_time,
                    "updated_at": current_time,
                    "embedding": None,
                    "parent_ticket_id": parent_ticket_id if parent_ticket_id else None,
                    "labels": [
                        label.strip() for label in labels.split(",") if label.strip()
                    ],
                }
                st.success("Ticket created!")
                st.rerun()
