from typing import List
import streamlit as st
from datetime import datetime, timezone
import time

from entities import Ticket, Status, Priority, Type
from .card import KanbanCard


class KanbanBoard:
    def __init__(self, tickets: List[Ticket]):
        # Initialize columns using Status enum
        self.columns = [
            status.value for status in Status
        ]  # ['Open', 'In Progress', 'Done']

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

    def create_ticket_card(self, ticket: Ticket, column):
        """Create a visual card for a ticket."""
        card = st.container()

        with card:
            # Convert ticket data to KanbanCard instance
            card = KanbanCard(
                ticket_id=ticket.id,
                title=ticket.title,
                description=ticket.description,
                ticket_type=ticket.type,
                priority=ticket.priority,
                status=ticket.status,
                assignee_id=ticket.assignee_id,
                reporter_id=ticket.reporter_id,
                created_at=ticket.created_at,
                updated_at=ticket.updated_at,
                embedding=ticket.embedding,
                parent_ticket_id=ticket.parent_ticket_id,
                labels=ticket.labels,
            )

            # Render the card with proper column information
            card.render(
                current_column=column,
                available_columns=self.columns,
                on_move=self.move_ticket,
                on_delete=self.delete_ticket,
            )

    def move_ticket(self, ticket_id: str, new_status: str):
        """Move a ticket to a new status column."""
        # Find the ticket by ID in the list
        for i, ticket in enumerate(st.session_state.tickets):
            if ticket.id == ticket_id:
                # Create a new Ticket object with updated status
                updated_ticket = Ticket(
                    **{
                        **ticket.model_dump(),  # Convert existing ticket to dict and unpack
                        "status": Status(new_status),  # Update status using Status enum
                        "updated_at": datetime.now(timezone.utc),  # Update timestamp
                    }
                )
                # Replace the old ticket with updated one
                st.session_state.tickets[i] = updated_ticket
                st.rerun()

    def delete_ticket(self, ticket_id: str):
        """Delete a ticket from the board."""
        # Find the ticket in the list
        for i, ticket in enumerate(st.session_state.tickets):
            if ticket.id == ticket_id:
                # Create a temp container for the toast
                toast_container = st.empty()

                # Remove the ticket
                st.session_state.tickets.pop(i)

                # Show success toast
                with toast_container:
                    st.toast(f"Ticket {ticket_id} deleted successfully", icon="🗑️")

                # Rerun to update the UI
                time.sleep(0.5)  # Small delay to show the toast
                st.rerun()
                break

    def render(self):
        """Render the Kanban board."""
        st.title("📋 Sprint Kanban Board")

        # Add filters in the sidebar
        with st.sidebar:
            st.header("Filters")
            selected_assignee = st.multiselect(
                "Assignee",
                options=list(set(t.assignee_id for t in st.session_state.tickets)),
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
                    set(label for t in st.session_state.tickets for label in t.labels)
                ),
                default=[],
            )

        # Create columns for each status
        cols = st.columns(len(self.columns), gap="small")

        # Display column headers with ticket counts
        for col, status in zip(cols, self.columns):
            tickets_in_column = [
                t for t in st.session_state.tickets if t.status == status
            ]
            col.markdown(f"### {status} ({len(tickets_in_column)})")

        # Filter tickets based on sidebar selections
        filtered_tickets: List[Ticket] = st.session_state.tickets
        if selected_assignee:
            filtered_tickets = [
                t for t in filtered_tickets if t.assignee_id in selected_assignee
            ]
        if selected_type:
            filtered_tickets = [t for t in filtered_tickets if t.type in selected_type]
        if selected_priority:
            filtered_tickets = [
                t for t in filtered_tickets if t.priority in selected_priority
            ]
        if selected_labels:
            filtered_tickets = [
                t
                for t in filtered_tickets
                if any(label in t.labels for label in selected_labels)
            ]

        # Display tickets in their respective columns
        for col, status in zip(cols, self.columns):
            with col:
                status_tickets = [t for t in filtered_tickets if t.status == status]
                for ticket in status_tickets:
                    self.create_ticket_card(
                        ticket, status
                    )  # Pass both ticket and current status
