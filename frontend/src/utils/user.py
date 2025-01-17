from entities import User
from typing import List


def get_user(users: List[User], username: str, email: str) -> User:
    for user in users:
        if user.name == username and user.email == email:
            return user
    return None
