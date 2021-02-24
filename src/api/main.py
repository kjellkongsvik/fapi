from typing import Optional

from fastapi import FastAPI
from fastapi import Security

from api.auth import Oauth

app = FastAPI()
oauth = Oauth("", "", {"id": ""})


@app.get("/")
def get(
    token: Optional[str] = Security(oauth),
):
    return {}
