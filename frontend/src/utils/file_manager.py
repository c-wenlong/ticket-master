import json
from pathlib import Path
from entities import Type, Status, Priority
from datetime import datetime, timezone


def read_json(file_path=Path("src/assets/datasets/session_metadata.json")):
    with open(file_path, "r") as file:
        sessions = json.load(file)
    return sessions


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
