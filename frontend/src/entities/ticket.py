from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4
import streamlit as st


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


class Ticket(BaseModel):
    id: str = Field(
        description="Unique identifier for the ticket",
    )
    title: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Short description of the ticket",
    )
    description: str = Field(
        ..., min_length=1, description="Detailed description of the issue or feature"
    )

    # Core Fields
    type: Type = Field(default=Type.TASK, description="Type of the ticket")
    status: Status = Field(
        default=Status.OPEN, description="Current status of the ticket"
    )
    priority: Priority = Field(
        default=Priority.MEDIUM, description="Priority level of the ticket"
    )

    # Assignment
    assignee_id: Optional[str] = Field(default=None)
    reporter_id: str = Field(
        default_factory=lambda: st.session_state.curr_user.id,
        description="User ID of the person who created the ticket",
    )

    # Timestamps
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp when the ticket was created",
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp when the ticket was created",
    )

    # AI Processing Fields
    embedding: Optional[List[float]] = Field(
        default=None, description="Vector for semantic search"
    )
    parent_ticket_id: Optional[str] = Field(
        default=None, description="If split from larger ticket"
    )

    # Basic Metadata
    labels: List[str] = Field(default_factory=list)

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "TICK-123",
                "title": "Implement user authentication",
                "description": "Add JWT-based authentication system",
                "status": "open",
                "priority": "high",
                "reporter_id": "USER-1",
                "labels": ["backend", "security"],
            }
        }


SAMPLE_TICKETS: List[Ticket] = [
    Ticket(**ticket_data)
    for ticket_data in [
        {
            "id": "TICKET-A95216E6",
            "title": "Implement Login",
            "description": "Add login functionality to the app",
            "type": "feature",
            "status": "open",
            "priority": "high",
            "assignee_id": "kai",
            "reporter_id": "ryan",
            "created_at": "2024-01-08T09:00:00Z",
            "updated_at": "2024-01-08T09:00:00Z",
            "embedding": None,
            "parent_ticket_id": None,
            "labels": ["auth", "frontend"],
        },
        {
            "id": "TICKET-46BD8794",
            "title": "Database Setup",
            "description": "Set up database for the project",
            "type": "task",
            "status": "in-progress",
            "priority": "medium",
            "assignee_id": "kai",
            "reporter_id": "avellin",
            "created_at": "2024-01-08T10:30:00Z",
            "updated_at": "2024-01-08T14:15:00Z",
            "embedding": None,
            "parent_ticket_id": None,
            "labels": ["database", "backend"],
        },
        {
            "id": "TICKET-C8D92E4F",
            "title": "Implement User Analytics Dashboard",
            "description": "Create a dashboard showing user engagement metrics and usage patterns",
            "type": "feature",
            "status": "in-progress",
            "priority": "high",
            "assignee_id": "avellin",
            "reporter_id": "kai",
            "created_at": "2024-01-08T11:00:00Z",
            "updated_at": "2024-01-08T15:20:00Z",
            "embedding": None,
            "parent_ticket_id": None,
            "labels": ["analytics", "frontend", "dashboard"],
        },
        {
            "id": "TICKET-F7B31A2E",
            "title": "Fix Password Reset Email",
            "description": "Debug and fix issue with password reset emails not being delivered",
            "type": "bug",
            "status": "open",
            "priority": "high",
            "assignee_id": "ryan",
            "reporter_id": "kai",
            "created_at": "2024-01-08T13:45:00Z",
            "updated_at": "2024-01-08T13:45:00Z",
            "embedding": None,
            "parent_ticket_id": None,
            "labels": ["auth", "email", "bug-fix"],
        },
        {
            "id": "TICKET-92AE5D1B",
            "title": "Update Documentation",
            "description": "Update API documentation with new endpoints and examples",
            "type": "task",
            "status": "done",
            "priority": "low",
            "assignee_id": "kai",
            "reporter_id": "avellin",
            "created_at": "2024-01-07T09:00:00Z",
            "updated_at": "2024-01-08T16:30:00Z",
            "embedding": None,
            "parent_ticket_id": None,
            "labels": ["documentation", "maintenance"],
        },
        {
            "id": "TICKET-E4D87C3A",
            "title": "Implement Dark Mode",
            "description": "Add dark mode theme support across all pages",
            "type": "feature",
            "status": "open",
            "priority": "medium",
            "assignee_id": "avellin",
            "reporter_id": "ryan",
            "created_at": "2024-01-08T14:00:00Z",
            "updated_at": "2024-01-08T14:00:00Z",
            "embedding": None,
            "parent_ticket_id": None,
            "labels": ["ui", "frontend", "theme"],
        },
        {
            "id": "TICKET-B5F19D8C",
            "title": "Optimize Database Queries",
            "description": "Improve performance of slow database queries in the user profile section",
            "type": "task",
            "status": "in-progress",
            "priority": "medium",
            "assignee_id": "ryan",
            "reporter_id": "avellin",
            "created_at": "2024-01-08T15:20:00Z",
            "updated_at": "2024-01-08T16:45:00Z",
            "embedding": None,
            "parent_ticket_id": None,
            "labels": ["performance", "backend", "database"],
        },
        {
            "id": "TICKET-D2C41E9B",
            "title": "Add Export to CSV Feature",
            "description": "Implement functionality to export analytics data to CSV format",
            "type": "feature",
            "status": "done",
            "priority": "medium",
            "assignee_id": "kai",
            "reporter_id": "kai",
            "created_at": "2024-01-07T13:00:00Z",
            "updated_at": "2024-01-08T11:30:00Z",
            "embedding": None,
            "parent_ticket_id": "TICKET-C8D92E4F",
            "labels": ["analytics", "export", "feature"],
        },
    ]
]

if __name__ == "__main__":
    for ticket in SAMPLE_TICKETS:
        print(f"id is {ticket.id}")
        print(f"reporter_id is {ticket.reporter_id}")
