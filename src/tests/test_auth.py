from unittest.mock import Mock

import pytest
from fastapi.exceptions import HTTPException

from api import auth


def test_missing_bearer():
    oauth = auth.Oauth(audience="", issuer="", public_keys={})
    with pytest.raises(HTTPException) as e:
        oauth.verify("not.a.bearer")
    assert e.value.status_code == 403


def test_not_a_decodable_jwt():
    oauth = auth.Oauth(audience="", issuer="", public_keys={})
    with pytest.raises(HTTPException) as e:
        oauth.verify("bearer this.is.an.invalid.token")
    assert e.value.status_code == 403


def test_token_without_kid():
    token_without_kid = """eyJhbGciOiJIUzI1NiJ9\
    .e30.ZRrHA1JJJW8opsbCGfG_HACGpVUMN_a9IV7pAx_Zmeo"""
    oauth = auth.Oauth(audience="", issuer="", public_keys={})

    with pytest.raises(HTTPException) as e:
        oauth.verify(token_without_kid)
    assert e.value.status_code == 403


def test_public_keys_without_kid():
    token_without_kid = """eyJhbGciOiJIUzI1NiIsImtpZCI6ImlkIn0\
    .e30.rHWCMy2sWIp8pohPfD5Tx5QhjlJqPYlR6WAhVB8pmOI"""
    oauth = auth.Oauth(audience="", issuer="", public_keys={})

    with pytest.raises(HTTPException) as e:
        oauth.verify(f"bearer {token_without_kid}")

    assert e.value.status_code == 403


def test_ok():
    mock = Mock()
    kid = "id"
    key = "some_key"
    audience = "some_audience"
    issuer = "some_issuer"
    some_token = """eyJhbGciOiJIUzI1NiIsImtpZCI6ImlkIn0\
    .e30.rHWCMy2sWIp8pohPfD5Tx5QhjlJqPYlR6WAhVB8pmOI"""

    oauth = auth.Oauth(audience=audience, issuer=issuer, public_keys={kid: key})
    oauth.verify(some_token, decode=mock.method)

    mock.method.assert_called_with(
        jwt=some_token, key=key, issuer=issuer, audience=audience, algorithms=["RS256"]
    )
