import streamlit as st
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Callable
from enum import Enum
from entities import Priority


@dataclass
class CardStyle:
    """Defines the styling for a Kanban card"""

    colors = {
        Priority.HIGH.value: "#ff6b6b",  # Red for high priority
        Priority.MEDIUM.value: "#ffd93d",  # Yellow for medium priority
        Priority.LOW.value: "#6bff6b",  # Green for low priority
    }
    padding = "10px"
    border_radius = "5px"
    margin = "5px 0"
    opacity = "0.9"
    min_height = "120px"


class KanbanCard:
    def __init__(
        self,
        ticket_id: str,
        title: str,
        description: str,
        ticket_type: str,
        priority: str,
        status: str,
        assignee_id: Optional[str],
        reporter_id: str,
        labels: List[str],
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        parent_ticket_id: Optional[str] = None,
        embedding: Optional[List[float]] = None,
    ):
        self.id = ticket_id
        self.title = title
        self.description = description
        self.type = ticket_type
        self.priority = priority
        self.status = status
        self.assignee_id = assignee_id
        self.reporter_id = reporter_id
        self.labels = labels
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
        self.parent_ticket_id = parent_ticket_id
        self.embedding = embedding
        self.style = CardStyle()

    @classmethod
    def from_dict(cls, data: dict) -> "KanbanCard":
        """Create a KanbanCard instance from a dictionary"""
        return cls(
            ticket_id=data["id"],
            title=data["title"],
            description=data["description"],
            ticket_type=data["type"],
            priority=data["priority"],
            status=data["status"],
            assignee_id=data["assignee_id"],
            reporter_id=data["reporter_id"],
            labels=data["labels"],
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            parent_ticket_id=data.get("parent_ticket_id"),
            embedding=data.get("embedding"),
        )

    def to_dict(self) -> dict:
        """Convert the card to a dictionary"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "type": self.type,
            "priority": self.priority,
            "status": self.status,
            "assignee_id": self.assignee_id,
            "reporter_id": self.reporter_id,
            "labels": self.labels,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "parent_ticket_id": self.parent_ticket_id,
            "embedding": self.embedding,
        }

    def _format_labels(self) -> str:
        """Format labels for display"""
        return " ".join([f"#{label}" for label in self.labels])

    def _get_assignee_display(self) -> str:
        """Get display text for assignee"""
        return self.assignee_id if self.assignee_id else "Not Assigned"

    def _generate_card_html(self) -> str:
        """Generate the HTML for the card content"""
        return f"""
        <div style="
            background-color: {self.style.colors[self.priority]};
            padding: {self.style.padding};
            border-radius: {self.style.border_radius};
            margin: {self.style.margin};
            opacity: {self.style.opacity};
            min-height: {self.style.min_height};
        ">
            <div style="color: black;">
                <strong>{self.id}</strong>: {self.title}
                <br>
                📝 {self.type} | 👤 {self.reporter_id}  ➜  👤 {self._get_assignee_display()}
                <br>
                <small>{self._format_labels()}</small>
            </div>
        </div>
        """

    def render(
        self,
        current_column: str,
        available_columns: List[str],
        on_move: Callable[[str, str], None],
    ) -> None:
        """
        Render the card in the Streamlit UI

        Args:
            current_column: Current status/column of the card
            available_columns: List of all available columns
            on_move: Callback function for moving the card
        """
        card = st.container()

        with card:
            # Split into card content and buttons
            card_col, buttons_col = st.columns([4, 1])

            with card_col:
                st.markdown(self._generate_card_html(), unsafe_allow_html=True)

            with buttons_col:
                # Add spacing for vertical alignment
                st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)

                current_col_idx = available_columns.index(current_column)

                # Left arrow button
                if current_col_idx > 0:
                    if st.button("←", key=f"left_{self.id}"):
                        on_move(self.id, available_columns[current_col_idx - 1])

                # Right arrow button
                if current_col_idx < len(available_columns) - 1:
                    if st.button("→", key=f"right_{self.id}"):
                        on_move(self.id, available_columns[current_col_idx + 1])


# Example usage:
if __name__ == "__main__":
    # Sample data
    card_data = {
        "id": "TICKET-123",
        "title": "Implement login feature",
        "description": "Add user authentication",
        "type": "feature",
        "priority": "high",
        "status": "in-progress",
        "assignee_id": "john",
        "reporter_id": "alice",
        "labels": ["frontend", "auth"],
        "embedding": [0.1, 0.2, 0.3],
    }

    # Create card instance
    card = KanbanCard.from_dict(card_data)

    # Define columns
    columns = ["open", "in-progress", "done"]

    # Mock move callback
    def on_move(ticket_id: str, new_status: str):
        print(f"Moving ticket {ticket_id} to {new_status}")

    # Render card (in a Streamlit app)
    card.render(
        current_column="in-progress", available_columns=columns, on_move=on_move
    )
