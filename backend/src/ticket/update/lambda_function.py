import json
import os
from datetime import datetime
from typing import Dict
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct

load_dotenv()

QDRANT_URL = os.environ["QDRANT_URL"]
QDRANT_API_KEY = os.environ["QDRANT_API_KEY"]
QDRANT_COLLECTION_NAME = os.environ["QDRANT_COLLECTION_NAME"]

qdrant_client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
)

def lambda_handler(event, _context):
    query_params: Dict = json.loads(event["queryStringParameters"]) or {}
    ticket_id = query_params.get("id")
    if not ticket_id:
        return {"statusCode": 400, "body": json.dumps({"base": {"message": "ticket id is required"}})}

    original_ticket = select_ticket(ticket_id)
    if not original_ticket:
        return {"statusCode": 404, "body": json.dumps({"base": {"message": "ticket not found"}})}
    
    body: Dict = json.loads(event["body"])
    ticket_delta = body.get("data")
    
    if not ticket_delta or not isinstance(ticket_delta, dict) or len(ticket_delta) == 0:
        return {"statusCode": 400, "body": json.dumps({"base": {"message": "ticket data is required"}})}
      
    update_ticket_payload(ticket_id, ticket_delta)
    original_ticket = select_ticket(ticket_id)
    assert original_ticket, "Unexpected state: ticket not found after update"
    
    return json.dumps({"base": {"code": 0, "message": "success"}, "data": original_ticket.payload})

def select_ticket(ticket_id: int):
    ticket = qdrant_client.retrieve(
      collection_name=QDRANT_COLLECTION_NAME,
      ids=[ticket_id]
    )
    
    if not ticket:
        return None
    
    return ticket[0]

def update_ticket_payload(ticket_id: int, ticket_delta: Dict):
    res = qdrant_client.set_payload(
        collection_name=QDRANT_COLLECTION_NAME,
        points=[ticket_id],
        payload=ticket_delta
    )
    
    return res