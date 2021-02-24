import os

from fastapi import APIRouter
from fastapi import Security

from api.auth import Auth

router = APIRouter()

AUTHORITY = os.environ.get("AUTHORITY", "http::/localhost:8089/default")
AUDIENCE = os.environ.get("AUDIENCE", "default")

sec = Auth(AUTHORITY, AUDIENCE)


@router.get("/")
def get(token: str = Security(sec)):
    return token
