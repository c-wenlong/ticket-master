import json
from typing import Dict, List
from openai import OpenAI
import os
from pydantic import BaseModel
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


class TicketGenResponse(BaseModel):
    master_ticket: Ticket
    sub_tickets: list[Ticket]


def lambda_handler(event, _context):
    body = json.loads(event["body"])
    ticket_description = body["data"]
    generated = generate_tickets(ticket_description)

    if not generated:
        return {
            "statusCode": 400,
            "body": json.dumps({"base": {"message": "ticket generation failed"}}),
        }

    response = {
        "master_ticket": None,
        "sub_tickets": [],
    }

    master_ticket = generated.master_ticket
    similar_master_tickets = find_similar_tickets(master_ticket)
    response["master_ticket"] = {
        "ticket": master_ticket.model_dump(),
        "similar_tickets": similar_master_tickets,
    }

    sub_tickets = generated.sub_tickets
    for sub_ticket in sub_tickets:
        similar_sub_tickets = find_similar_tickets(sub_ticket)
        response["sub_tickets"].append(
            {"ticket": sub_ticket.model_dump(), "similar_tickets": similar_sub_tickets}
        )

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "base": {"code": 0, "message": "success"},
                "data": response,
            }
        ),
    }


def generate_tickets(ticket_desc: str):
    generate_ticket_prompt = """
    You will be given a Software Engineering related ticket description.
    Please generate a master ticket based on the description.
    If the ticket is too complex, you may create sub-tickets as well if needed.
    Do not generate sub-tickets unnecessarily. Each ticket should minimumly take 1 man-day to complete.
    i.e. tickets that can be completed in less than a day should not be split.
    
    The ticket should have a title, description, type, priority and status.
    The ticket title should be descriptive and be in title case.
    The ticket description should be detailed and provide context.
    The ticket type should be one of the following: "bug", "feature", "task".
    The ticket priority should be one of the following: "low", "medium", "high".
    The ticket status should default to "open".
    
    Each ticket should be structured as follows:
    {
      "title": <str>,
      "description": <str>,
      "type": <str>,
      "priority": <str>,
      "status": "open"
    }
    
    Your response should be structured as follows:
    {
      "master_ticket": <Ticket>,
      "sub_tickets": [<Ticket>, <Ticket>, ...]
    }
    """

    user_prompt = f"The following is the ticket description: {ticket_desc}. Please generate the specified tickets based on the description."

    completion = openai_client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": generate_ticket_prompt},
            {"role": "user", "content": user_prompt},
        ],
        response_format=TicketGenResponse,
    )

    return completion.choices[0].message.parsed


def stringify_ticket(ticket: Ticket):
    return f"ticket title: {ticket.title}, ticket description: {ticket.description}, ticket type: {ticket.type}"


def text_to_embedding(ticket: Ticket):
    ticket_string = stringify_ticket(ticket)
    embeddings: CreateEmbeddingResponse = openai_client.embeddings.create(
        model="text-embedding-3-small", input=ticket_string, encoding_format="float"
    )
    return embeddings.data[0].embedding


#! Arbitrary score_threshold used
def find_similar_tickets(ticket: Ticket, score_threshold=0.5) -> List[Dict]:
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
