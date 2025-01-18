from typing import List
from pydantic import BaseModel, RootModel, ValidationError
import requests

from frontend.src.entities.http import HttpResponse
from frontend.src.entities.ticket import Ticket

backend_base_url = "https://s618z67nt2.execute-api.ap-southeast-1.amazonaws.com"


class ListTicketData(RootModel[list[Ticket]]):
    pass


def get_tickets():
    list_endpoint = f"{backend_base_url}/ticket/list"
    response = requests.get(list_endpoint)
    res = response.json()

    try:
        res = HttpResponse[ListTicketData](**res)
    except ValidationError as e:
        print("Validate get ticket failed: ", e)
        return None

    if response.status_code != 200:
        print("Generate ticket failed: ", res)
        print(res.base.message)
        return None

    return res.data


class GenTicketData(BaseModel):
    master_ticket: Ticket
    sub_tickets: list[Ticket]


def generate_ticket(ticket_desc: str, reporter_id: str, assignee_id: str):
    create_endpoint = f"{backend_base_url}/ticket/gen"
    response = requests.post(
        create_endpoint,
        json={
            "data": {
                "ticket_description": ticket_desc,
                "reporter_id": reporter_id,
                "assignee_id": assignee_id,
            }
        },
    )
    res = response.json()

    try:
        res = HttpResponse[GenTicketData](**res)
    except ValidationError as e:
        print("Validate generate ticket failed: ", e)
        return None

    if response.status_code != 200:
        print("Generate ticket failed: ", res)
        print(res.base.message)
        return None

    return res.data


def create_ticket(ticket: Ticket):
    create_endpoint = f"{backend_base_url}/ticket/create"
    response = requests.post(create_endpoint, json={"data": ticket})
    res = response.json()

    try:
        res = HttpResponse[Ticket](**res)
    except ValidationError as e:
        print("Validate create ticket failed: ", e)
        return None

    if response.status_code != 200:
        print("Create ticket failed: ", res)
        print(res.base.message)
        return None

    return res.data


def create_tickets(tickets: List[Ticket]):
    create_endpoint = f"{backend_base_url}/ticket/create"
    response = requests.post(create_endpoint, json={"data": tickets})
    res = response.json()

    try:
        res = HttpResponse[ListTicketData](**res)
    except ValidationError as e:
        print("Validate create tickets failed: ", e)
        return None

    if response.status_code != 200:
        print("Create tickets failed: ", res)
        print(res.base.message)
        return None

    return res.data


def update_ticket(ticket: Ticket):
    update_endpoint = f"{backend_base_url}/ticket/update"
    response = requests.post(update_endpoint, json={"data": ticket})
    res = response.json()

    try:
        res = HttpResponse[Ticket](**res)
    except ValidationError as e:
        print("Validate update ticket failed: ", e)
        return None

    if response.status_code != 200:
        print("Update ticket failed: ", res)
        print(res.base.message)
        return None

    return res.data