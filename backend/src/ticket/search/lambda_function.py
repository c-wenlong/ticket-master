import json
from openai import OpenAI
import os
from datetime import datetime
from dotenv import load_dotenv
from qdrant_client import QdrantClient, models
load_dotenv()
SYSTEM = ""
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

QDRANT_URL = os.environ['QDRANT_URL']
QDRANT_API_KEY = os.environ['QDRANT_API_KEY']
QDRANT_COLLECTION_NAME = os.environ['QDRANT_COLLECTION_NAME']

openai_client = OpenAI(api_key=OPENAI_API_KEY)
qdrant_client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
)


def lambda_handler(event, context):
    body = json.loads(event['body'])
    response = user_to_vectordb_prompt(body['user_ticket_text'])

    results = fetch_similar_tickets(response, QDRANT_COLLECTION_NAME, qdrant_client, 5)
    print(results)
    return {
        'statusCode': 200,
        'body': json.dumps(results)
    }

def user_to_vectordb_prompt(user_prompt) -> str:
    completion = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": user_prompt},
        ],
    )
    return completion.choices[0].message.content


def text_to_embedding(text):
    embeddings = openai_client.embeddings.create(
        model="text-embedding-3-small", input=text, encoding_format="float"
    )
    return embeddings.data[0].embedding

def fetch_similar_tickets(
    text, collection_name, qdrant_client, limit=5
):
    text_embedding = text_to_embedding(text)
    similar_tickets = qdrant_client.search(
        collection_name=collection_name, query_vector=text_embedding, limit=limit
    )
    results = []
    for ticket in similar_tickets:
        results.append({"payload": ticket.payload, "score": ticket.score})
    return results

