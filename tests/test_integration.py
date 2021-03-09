import os
from time import sleep
from urllib.parse import parse_qs
from urllib.parse import urlparse

import pytest
import requests

API_ADDR = os.getenv("API_ADDR", "http://localhost:5000")
AUTHORITY = os.getenv("AUTHORITY", "http://localhost:8089/common")
AUDIENCE = os.getenv("AUDIENCE")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

sleep(2)


@pytest.fixture(scope="session")
def oidc():
    r = requests.get(f"{AUTHORITY}/.well-known/openid-configuration")
    assert r
    return r.json()


def get_code(auth_endpoint):
    r = requests.get(
        f"{auth_endpoint}"
        f"?client_id={AUDIENCE}"
        "&response_type=code"
        "&redirect_uri=h"
        "&scope=openid"
        "&state=1234"
        "&nonce=5678"
        "&response_mode=fragment",
        allow_redirects=False,
    )
    return parse_qs(urlparse(r.headers["location"]).fragment)["code"][0]


@pytest.fixture(scope="session")
def access_token(oidc):
    code = get_code(oidc["authorization_endpoint"])
    data = (
        "grant_type=authorization_code"
        + f"&client_id={CLIENT_ID}"
        + f"&client_secret={CLIENT_SECRET}"
        + f"&code={code}"
        + "&redirect_uri=h"
    )
    headers = {"content-type": "application/x-www-form-urlencoded"}
    r = requests.post(
        oidc["token_endpoint"],
        str.encode(data),
        headers=headers,
    )
    assert r.status_code == 200
    d = r.json()
    return d["access_token"]


@pytest.fixture(scope="session")
def auth_header(access_token):
    return {"Authorization": f"Bearer {access_token}"}


def test_ok(auth_header):
    r = requests.get(f"{API_ADDR}", headers=auth_header)
    assert r
