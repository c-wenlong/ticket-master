import streamlit as st
from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4
from entities import Status, Priority, Type


class KanbanBoard:
    def __init__(self):
        # Initialize columns using Status enum
        self.columns = [status.value for status in Status]

        # Initialize session state for tickets if not exists
        if "tickets" not in st.session_state:
            st.session_state.tickets = self.get_sample_tickets()

        if "dragging" not in st.session_state:
            st.session_state.dragging = None

        self.ticket_colors = {
            Priority.HIGH.value: "#ff6b6b",  # Red for high priority
            Priority.MEDIUM.value: "#ffd93d",  # Yellow for medium priority
            Priority.LOW.value: "#6bff6b",  # Green for low priority
        }

    def get_sample_tickets(self):
        """Generate sample ticket data matching the Pydantic schema."""
        return {
            "TICKET-A95216E6": {
                "id": "TICKET-A95216E6",
                "title": "Implement Login",
                "description": "Add login functionality to the app",
                "type": Type.FEATURE.value,
                "status": Status.OPEN.value,
                "priority": Priority.HIGH.value,
                "assignee_id": "kai",
                "reporter_id": "ryan",
                "embedding": None,
                "parent_ticket_id": None,
                "labels": ["auth", "frontend"],
            },
            "TICKET-46BD8794": {
                "id": "TICKET-46BD8794",
                "title": "Database Setup",
                "description": "Set up database for the project",
                "type": Type.TASK.value,
                "status": Status.IN_PROGRESS.value,
                "priority": Priority.MEDIUM.value,
                "assignee_id": "kai",
                "reporter_id": "avellin",
                "created_at": datetime.now(timezone.utc),
                "updated_at": datetime.now(timezone.utc),
                "embedding": None,
                "parent_ticket_id": None,
                "labels": ["database", "backend"],
            },
        }

    def create_ticket_card(self, ticket, column):
        """Create a visual card for a ticket."""
        card = st.container()

        with card:
            # Card header with background color based on priority
            labels_str = " ".join([f"#{label}" for label in ticket["labels"]])
            assignee_display = (
                ticket["assignee_id"] if ticket["assignee_id"] else "Not Assigned"
            )

            st.markdown(
                f"""
                <div style="
                    background-color: {self.ticket_colors[ticket['priority']]};
                    padding: 10px;
                    border-radius: 5px;
                    margin: 5px 0;
                    opacity: 0.9;
                ">
                    <div style="color: black;">
                        <strong>{ticket['id']}</strong>: {ticket['title']}
                        <br>
                        📝 {ticket['type']} | 👤 {ticket['reporter_id']}  ➜  👤 {assignee_display}
                        <br>
                        <small>{labels_str}</small>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Add move buttons
            cols = st.columns(len(self.columns))
            current_col_idx = self.columns.index(column)

            # Show move left button if not first column
            if current_col_idx > 0:
                if cols[0].button("←", key=f'left_{ticket["id"]}'):
                    self.move_ticket(ticket["id"], self.columns[current_col_idx - 1])

            # Show move right button if not last column
            if current_col_idx < len(self.columns) - 1:
                if cols[-1].button("→", key=f'right_{ticket["id"]}'):
                    self.move_ticket(ticket["id"], self.columns[current_col_idx + 1])

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
                    self.create_ticket_card(ticket, status)

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
