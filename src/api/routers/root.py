import os

from fastapi import APIRouter
from fastapi import Security

from api.auth import Auth

router = APIRouter()

AUTHORITY = os.environ.get("AUTHORITY")
AUDIENCE = os.environ.get("AUDIENCE")

sec = Auth(AUTHORITY, AUDIENCE)


@router.get("/")
def get(token: str = Security(sec)):
    return token
