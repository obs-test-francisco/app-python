import json

from .users import User


def serialize_users(users: list[User]) -> str:
    if users is not None:
        return json.dumps([user.__serialize__() for user in users])
    return json.dumps({})