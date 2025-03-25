from fastapi.testclient import TestClient
from fapi import app
from fapi.hello import Hello


client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    _ = Hello(**response.json())  # pyright: ignore [reportAny]
