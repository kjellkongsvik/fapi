from fastapi.testclient import TestClient

from api.main import app
from api.main import oauth

client = TestClient(app)


def mock_oauth():
    return ""


app.dependency_overrides[oauth] = mock_oauth


def test_ok():
    r = client.get("/")
    assert r
