import json
from openai import OpenAI
import os
from datetime import datetime
from dotenv import load_dotenv
import uuid
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

    tickets = {
        body['user_ticket_text']:response
        }


    results = add_to_vectordb(tickets, QDRANT_COLLECTION_NAME, qdrant_client)
    print(results)
    return {
        'statusCode': 200,
        'body': json.dumps(tickets)
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

def add_to_vectordb(tickets, collection_name, qdrant_client):

    # Convert the ticket inputs into embeddings

    ticket_embeddings = {}

    # Iterate through each ticket
    for ticket_user_input, ticket_text in tickets.items():
        print(ticket_user_input)

        # Get embedding
        embedding = text_to_embedding(ticket_text)

        # Store result
        ticket_embeddings[ticket_user_input] = {
            "ticket_text": ticket_text,
            "ticket_user_input": ticket_user_input,
            "embedding": embedding,
        }

    # Result to be returned
    results = {}

    # Upload vector embeddings into QDRANT DB

    for idx, (ticket_user_input, ticket_data) in enumerate(ticket_embeddings.items()):
        response = qdrant_client.upsert(
            collection_name=collection_name,
            points=[
                models.PointStruct(
                    id =  str(generate_guid(ticket_data['ticket_text'])),
                    payload = {
                        "ticket_user_input": ticket_data['ticket_user_input'],
                        "ticket_text": ticket_data['ticket_text'],
                        "created_at": datetime.now().isoformat(),
                    },
                    vector = ticket_data["embedding"],
                )
            ],
        )

        results[ticket_user_input] = response

    return results

def generate_guid(text):
    class NULL_NAMESPACE:
        bytes = b''

    guid = uuid.uuid3(NULL_NAMESPACE, text.encode('utf-8'))
    return guid