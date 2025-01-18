import datetime
import json
from typing import Dict, List
from openai import OpenAI
import os
from datetime import datetime
from dotenv import load_dotenv
import uuid
from qdrant_client import QdrantClient, models

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


def lambda_handler(event, context):
    tickets_to_insert = []

    body = json.loads(event["body"])
    tickets = body["data"]
    if not tickets:
        return {
            "statusCode": 400,
            "body": json.dumps({"base": {"message": "ticket data is required"}}),
        }

    if isinstance(tickets, list):
        tickets_to_insert = tickets
    elif isinstance(tickets, dict):
        tickets_to_insert.append(tickets)
    else:
        return {
            "statusCode": 400,
            "body": json.dumps({"base": {"message": "invalid ticket payload"}}),
        }

    results = []
    for ticket in tickets_to_insert:
        ticket_str = stringify_ticket(ticket)
        ticket_embedding = text_to_embedding(ticket_str)
        inserted_ticket = insert_ticket(ticket, ticket_embedding)
        results.append(inserted_ticket)

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "base": {"code": 0, "message": "success"},
                "data": results[0] if len(results) == 0 else results,
            }
        ),
    }


def stringify_ticket(ticket: Dict):
    return f"ticket title: {ticket.get("title")}, ticket description: {ticket.get('description')}, ticket type: {ticket.get('type')}"


def text_to_embedding(text):
    embeddings = openai_client.embeddings.create(
        model="text-embedding-3-small", input=text, encoding_format="float"
    )
    return embeddings.data[0].embedding


def insert_ticket(ticket: Dict, embedding: List[float]):
    ticket_id = str(uuid.uuid4())
    ticket["id"] = ticket_id
    ticket["created_at"] = datetime.now().timestamp()
    ticket["updated_at"] = datetime.now().timestamp()

    qdrant_client.upsert(
        collection_name=QDRANT_COLLECTION_NAME,
        points=[
            models.PointStruct(
                id=ticket_id,
                payload=ticket,
                vector=embedding,
            )
        ],
    )

    return ticket
