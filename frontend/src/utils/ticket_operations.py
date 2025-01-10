from entities import Ticket
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
