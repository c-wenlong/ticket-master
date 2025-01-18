from entities import Ticket
from typing import Dict, Any
from datetime import datetime, timezone


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
