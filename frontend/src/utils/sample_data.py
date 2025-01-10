from typing import List
from entities import Ticket, User

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

SAMPLE_USERS = [
    User(**user_data)
    for user_data in [
        {
            "id": "USER-KC",
            "name": "Kai Chen",
            "email": "kai@example.com",
            "username": "kai",
            "role": "developer",
        },
        {
            "id": "USER-AV",
            "name": "Avellin",
            "email": "avellin@example.com",
            "username": "avellin",
            "role": "developer",
        },
        {
            "id": "USER-XY",
            "name": "Xiaoyun",
            "email": "xiaoyun@example.com",
            "username": "xiaoyun",
            "role": "developer",
        },
        {
            "id": "USER-RY",
            "name": "Ryan",
            "email": "ryan@example.com",
            "username": "ryan",
            "role": "developer",
        },
    ]
]
