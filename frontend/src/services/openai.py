from openai import OpenAI
import streamlit as st
from uuid import uuid4


SYSTEM = ""

OPENAI_API_KEY = st.secrets["OPENAI"]["OPENAI_API_KEY"]
openai_client = OpenAI(api_key=OPENAI_API_KEY)


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


def text_to_ticket(text):
    # return sample ticket
    return """{
        "title": "SAMPLE AI TICKET",
        "description": "THE TICKET ID SHOULD BE RANDOMISED USING THE TICKET ENTITY, ALL DATES AND REPORT_ID sARE AUTOMATED BY ENTITY.",
        "status": "open",
        "type": "task",
        "priority": "medium",
        "labels": ["feature"]
    }"""
