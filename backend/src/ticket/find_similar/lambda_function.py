import json
from typing import Dict, List
from openai import OpenAI
import os
from pydantic import BaseModel, ValidationError
from enum import StrEnum
from dotenv import load_dotenv
from openai.types.create_embedding_response import CreateEmbeddingResponse
from qdrant_client import QdrantClient

load_dotenv()

SYSTEM = ""
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

QDRANT_URL = os.environ["QDRANT_URL"]
QDRANT_API_KEY = os.environ["QDRANT_API_KEY"]
QDRANT_COLLECTION_NAME = os.environ["QDRANT_COLLECTION_NAME"]

openai_client = OpenAI(api_key=OPENAI_API_KEY)
qdrant_client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
)


class TicketStatus(StrEnum):
    open = "open"
    in_progress = "in_progress"
    closed = "closed"


class TicketPriority(StrEnum):
    low = "low"
    medium = "medium"
    high = "high"


class TicketType(StrEnum):
    bug = "bug"
    feature = "feature"
    task = "task"


class Ticket(BaseModel):
    title: str
    description: str
    status: TicketStatus
    priority: TicketPriority
    type: TicketType
    labels: list[str]


class TicketGenResponse(BaseModel):
    master_ticket: Ticket
    sub_tickets: list[Ticket]


def lambda_handler(event, _context):
    body = json.loads(event["body"])
    data = body.get("data") or {}
    
    try:
      ticket = Ticket(**data)
    except ValidationError as e:
      return {
        "statusCode": 400,
        "body": json.dumps(
            {
                "base": {"message": "Invalid ticket data"},
            }
        ),
    }
      
    similar_tickets = find_similar_tickets(ticket)
    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "base": {"code": 0, "message": "success"},
                "data": similar_tickets,
            }
        ),
    }



def stringify_ticket(ticket: Ticket):
    return f"ticket title: {ticket.title}, ticket description: {ticket.description}, ticket type: {ticket.type}"


def text_to_embedding(ticket: Ticket):
    ticket_string = stringify_ticket(ticket)
    embeddings: CreateEmbeddingResponse = openai_client.embeddings.create(
        model="text-embedding-3-small", input=ticket_string, encoding_format="float"
    )
    return embeddings.data[0].embedding


#! Arbitrary score_threshold used
def find_similar_tickets(ticket: Ticket, score_threshold=0.75) -> List[Dict]:
    text_embedding = text_to_embedding(ticket)
    similar_tickets = qdrant_client.search(
        collection_name=QDRANT_COLLECTION_NAME,
        query_vector=text_embedding,
        limit=5,
        score_threshold=score_threshold,
    )

    return [
        {"ticket": ticket.payload, "score": ticket.score} for ticket in similar_tickets
    ]
