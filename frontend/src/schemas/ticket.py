from datetime import datetime
from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field, field_validator
from uuid import uuid4


class TicketType(str, Enum):
    BUG = "BUG"
    FEATURE = "FEATURE"
    TASK = "TASK"


class TicketPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class TicketStatus(str, Enum):
    NEW = "NEW"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"


class Ticket(BaseModel):
    # Required fields
    id: str = Field(
        default_factory=lambda: f"TICKET-{uuid4().hex[:8].upper()}",
        description="Unique identifier for the ticket",
    )

    title: str = Field(
        ...,  # ... means required
        min_length=1,
        max_length=100,
        description="Short description of the ticket",
    )

    description: str = Field(
        ..., min_length=1, description="Detailed description of the issue or feature"
    )

    # Fields with defaults
    type: TicketType = Field(default=TicketType.TASK, description="Type of the ticket")

    priority: TicketPriority = Field(
        default=TicketPriority.MEDIUM, description="Priority level of the ticket"
    )

    status: TicketStatus = Field(
        default=TicketStatus.NEW, description="Current status of the ticket"
    )

    created: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when the ticket was created",
    )

    # Optional fields
    components: Optional[List[str]] = Field(
        default_factory=list, description="System components affected by this ticket"
    )

    labels: Optional[List[str]] = Field(
        default_factory=list, description="Labels for categorizing the ticket"
    )

    # Custom validators
    @field_validator("title")
    def title_must_be_meaningful(cls, v):
        if len(v.split()) < 2:
            raise ValueError("Title must contain at least two words")
        return v.strip()

    @field_validator("components", "labels")
    def deduplicate_lists(cls, v):
        if v is not None:
            return list(dict.fromkeys(v))  # Remove duplicates while preserving order
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Login page throws 500 error with special characters",
                "description": "Users experience 500 error when logging in with special characters",
                "type": "BUG",
                "priority": "HIGH",
                "components": ["Authentication"],
                "labels": ["security", "production"],
            }
        }


# Example usage:
if __name__ == "__main__":
    # Create a ticket with minimal required fields
    minimal_ticket = Ticket(
        title="Fix login page error",
        description="Login page crashes with special characters",
    )
    print("\nMinimal ticket:", minimal_ticket.model_dump_json(indent=2))

    # Create a ticket with all fields
    full_ticket = Ticket(
        title="Implement OAuth2 Authentication",
        description="Add OAuth2 authentication support with Google provider",
        type=TicketType.FEATURE,
        priority=TicketPriority.HIGH,
        components=["Authentication", "Frontend"],
        labels=["security", "user-experience"],
    )
    print("\nFull ticket:", full_ticket.model_dump_json(indent=2))

    # Validate a ticket from JSON
    ticket_json = {
        "title": "DB Connection Timeout",
        "description": "Database connections timing out under heavy load",
        "type": "BUG",
        "priority": "HIGH",
        "components": ["Database", "Database"],  # Duplicate will be removed
        "labels": ["performance"],
    }

    parsed_ticket = Ticket.model_validate(ticket_json)
    print("\nParsed ticket:", parsed_ticket.model_dump_json(indent=2))
