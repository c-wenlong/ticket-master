import json
import os
from openai import OpenAI
from datetime import datetime
from typing import Dict
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import PointVectors, Record
from qdrant_client.http.models import PointStruct

load_dotenv()

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
QDRANT_URL = os.environ["QDRANT_URL"]
QDRANT_API_KEY = os.environ["QDRANT_API_KEY"]
QDRANT_COLLECTION_NAME = os.environ["QDRANT_COLLECTION_NAME"]

qdrant_client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
)
openai_client = OpenAI(api_key=OPENAI_API_KEY)


def lambda_handler(event, _context):
    query_params: Dict = json.loads(event["queryStringParameters"]) or {}
    ticket_id = query_params.get("id")
    if not ticket_id:
        return {
            "statusCode": 400,
            "body": json.dumps({"base": {"message": "ticket id is required"}}),
        }

    original_ticket = select_ticket(ticket_id)
    if not original_ticket:
        return {
            "statusCode": 404,
            "body": json.dumps({"base": {"message": "ticket not found"}}),
        }

    body: Dict = json.loads(event["body"])
    ticket_delta = body.get("data")

    if not ticket_delta or not isinstance(ticket_delta, dict) or len(ticket_delta) == 0:
        return {
            "statusCode": 400,
            "body": json.dumps({"base": {"message": "ticket data is required"}}),
        }

    update_ticket_payload(original_ticket, ticket_delta)
    original_ticket = select_ticket(ticket_id)
    assert original_ticket, "Unexpected state: ticket not found after update"

    return {
        "statusCode": 200,
        "body": json.dumps(
            {"base": {"code": 0, "message": "success"}, "data": original_ticket.payload}
        ),
    }


def select_ticket(ticket_id: int):
    ticket = qdrant_client.retrieve(
        collection_name=QDRANT_COLLECTION_NAME, ids=[ticket_id]
    )

    if not ticket:
        return None

    return ticket[0]


def text_to_embedding(text):
    embeddings = openai_client.embeddings.create(
        model="text-embedding-3-small", input=text, encoding_format="float"
    )
    return embeddings.data[0].embedding


def update_ticket_payload(original_ticket: Record, ticket_delta: Dict):
    qdrant_client.set_payload(
        collection_name=QDRANT_COLLECTION_NAME,
        points=[original_ticket.id],
        payload=ticket_delta,
    )

    ticket_title = ticket_delta.get("title") or (original_ticket.payload or {})["title"]
    ticket_desc = (
        ticket_delta.get("description")
        or (original_ticket.payload or {})["description"]
    )
    ticket_text = f"ticket title: {ticket_title}, ticket description: {ticket_desc}"

    qdrant_client.update_vectors(
        collection_name=QDRANT_COLLECTION_NAME,
        points=[
            PointVectors(id=original_ticket.id, vector=text_to_embedding(ticket_text)),
        ],
    )
