from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.routers import root

app = FastAPI()
app.include_router(root.router)

client = TestClient(app)


def override_auth():
    return ""


app.dependency_overrides[root.sec] = override_auth


def test_root():
    r = client.get("/")
    assert r
