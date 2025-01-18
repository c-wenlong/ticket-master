from entities import Ticket, Type, Status, Priority
from datetime import datetime, timezone
from typing import Dict, Any


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


def get_sample_tickets():
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
            "reporter_id": "xiaoyun",
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
            "embedding": None,
            "parent_ticket_id": None,
            "labels": ["database", "backend"],
        },
        "TICKET-C8D92E4F": {
            "id": "TICKET-C8D92E4F",
            "title": "Implement User Analytics Dashboard",
            "description": "Create a dashboard showing user engagement metrics and usage patterns",
            "type": Type.FEATURE.value,
            "status": Status.IN_PROGRESS.value,
            "priority": Priority.HIGH.value,
            "assignee_id": "avellin",
            "reporter_id": "xiaoyun",
            "embedding": None,
            "parent_ticket_id": None,
            "labels": ["analytics", "frontend", "dashboard"],
        },
        "TICKET-F7B31A2E": {
            "id": "TICKET-F7B31A2E",
            "title": "Fix Password Reset Email",
            "description": "Debug and fix issue with password reset emails not being delivered",
            "type": Type.BUG.value,
            "status": Status.OPEN.value,
            "priority": Priority.HIGH.value,
            "assignee_id": "ryan",
            "reporter_id": "kai",
            "embedding": None,
            "parent_ticket_id": None,
            "labels": ["auth", "email", "bug-fix"],
        },
        "TICKET-92AE5D1B": {
            "id": "TICKET-92AE5D1B",
            "title": "Update Documentation",
            "description": "Update API documentation with new endpoints and examples",
            "type": Type.TASK.value,
            "status": Status.DONE.value,
            "priority": Priority.LOW.value,
            "assignee_id": "ryan",
            "reporter_id": "avellin",
            "embedding": None,
            "parent_ticket_id": None,
            "labels": ["documentation", "maintenance"],
        },
        "TICKET-E4D87C3A": {
            "id": "TICKET-E4D87C3A",
            "title": "Implement Dark Mode",
            "description": "Add dark mode theme support across all pages",
            "type": Type.FEATURE.value,
            "status": Status.OPEN.value,
            "priority": Priority.MEDIUM.value,
            "assignee_id": "xiaoyun",
            "reporter_id": "ryan",
            "embedding": None,
            "parent_ticket_id": None,
            "labels": ["ui", "frontend", "theme"],
        },
        "TICKET-B5F19D8C": {
            "id": "TICKET-B5F19D8C",
            "title": "Optimize Database Queries",
            "description": "Improve performance of slow database queries in the user profile section",
            "type": Type.TASK.value,
            "status": Status.IN_PROGRESS.value,
            "priority": Priority.MEDIUM.value,
            "assignee_id": "ryan",
            "reporter_id": "avellin",
            "embedding": None,
            "parent_ticket_id": None,
            "labels": ["performance", "backend", "database"],
        },
    }

def get_sample_analytics(): 
    return [
        {
            "id": "sprint_1",
            "start_time": int(datetime(2025, 1, 11, 0, 0, 0, tzinfo=timezone.utc).timestamp() * 1000), # 1735948800000
            "end_time": int(datetime(2025, 1, 25, 0, 0, 0, tzinfo=timezone.utc).timestamp() * 1000), #1737158400000,
            "events": [
                { "ticket_id": "1", "timestamp": int(datetime(2025, 1, 11, 0, 0, 0, tzinfo=timezone.utc).timestamp() * 1000), "description": "create ticket", "status": "open", "priority": "medium" },
                { "ticket_id": "1", "timestamp": int(datetime(2025, 1, 11, 15, 0, 0, tzinfo=timezone.utc).timestamp() * 1000), "description": "update status - in_progress", "status": "in_progress", "priority": "medium" },
                { "ticket_id": "1", "timestamp": int(datetime(2025, 1, 12, 14, 0, 0, tzinfo=timezone.utc).timestamp() * 1000), "description": "complete ticket", "status": "done", "priority": "medium" },
                { "ticket_id": "2", "timestamp": int(datetime(2025, 1, 15, 0, 0, 0, tzinfo=timezone.utc).timestamp() * 1000), "description": "create ticket", "status": "open", "priority": "high" },
                { "ticket_id": "2", "timestamp": int(datetime(2025, 1, 17, 0, 0, 0, tzinfo=timezone.utc).timestamp() * 1000), "description": "update status - in_progress", "status": "in_progress", "priority": "high" },
                { "ticket_id": "3", "timestamp": int(datetime(2025, 1, 12, 22, 0, 0, tzinfo=timezone.utc).timestamp() * 1000), "description": "create ticket", "status": "open", "priority": "low" },
                { "ticket_id": "3", "timestamp": int(datetime(2025, 1, 15, 9, 30, 0, tzinfo=timezone.utc).timestamp() * 1000), "description": "complete ticket", "status": "done", "priority": "low" },
                { "ticket_id": "4", "timestamp": int(datetime(2025, 1, 18, 0, 0, 0, tzinfo=timezone.utc).timestamp() * 1000), "description": "create ticket", "status": "open", "priority": "medium" },
                { "ticket_id": "4", "timestamp": int(datetime(2025, 1, 18, 16, 0, 0, tzinfo=timezone.utc).timestamp() * 1000), "description": "update priority - high", "status": "open", "priority": "high" },
            ],
        }
    ]
