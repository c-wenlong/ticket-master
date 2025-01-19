from typing import List
from entities import Ticket, User
from services.ticket import list_tickets

# TODO: Replace this with some sort of state management
SAMPLE_TICKETS: List[Ticket] = list_tickets()

SAMPLE_USERS = [
    User(**user_data)
    for user_data in [
        {
            "id": "USER-1",
            "name": "Kai Chen",
            "email": "chenwenlongofficial@gmail.com",
            "username": "kai",
            "role": "developer",
        },
        {
            "id": "USER-2",
            "name": "Avellin",
            "email": "avellin@gmail.com",
            "username": "avellin",
            "role": "developer",
        },
        {
            "id": "USER-3",
            "name": "Xiaoyun",
            "email": "xiaoyun@gmail.com",
            "username": "xiaoyun",
            "role": "developer",
        },
        {
            "id": "USER-4",
            "name": "Ryan",
            "email": "ryan@gmail.com",
            "username": "ryan",
            "role": "developer",
        },
    ]
]
