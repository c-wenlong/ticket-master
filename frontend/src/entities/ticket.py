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
        default_factory=lambda: f"TICKET-{uuid4().hex[:8].upper()}",
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
