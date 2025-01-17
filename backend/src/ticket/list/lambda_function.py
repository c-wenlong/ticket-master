import json
import os
from datetime import datetime
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


def lambda_handler(_event, _context):
    tickets = list_tickets()
    return {
        "statusCode": 200,
        "body": json.dumps(
            {"base": {"code": 0, "message": "success"}, "data": tickets}
        ),
    }


def list_tickets():
    tickets = []

    offset = 0
    while True:
        scroll_result = qdrant_client.scroll(
            collection_name=QDRANT_COLLECTION_NAME,
            limit=100,
            offset=offset,
            with_payload=True,
        )

        points = scroll_result[0]
        tickets.extend(points)

        offset = scroll_result[1]
        if offset == None:
            break

    return [ticket.payload for ticket in tickets]
