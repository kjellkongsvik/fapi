import json
import logging
from functools import lru_cache

import jwt
import requests
from fastapi import HTTPException
from fastapi import Request
from fastapi import status
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from pydantic import parse_obj_as
from pydantic.error_wrappers import ValidationError

log = logging.getLogger(__name__)


@lru_cache
def get_oidc(authority: str) -> dict:
    url = f"{authority}/.well-known/openid-configuration"
    try:
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        raise RuntimeError(f"Could not connect to oidc server: {url=}")
    if not r:
        raise RuntimeError(
            f"Could not get config from oidc server: {url=} {r.status_code=}"
        )

    class Oid(BaseModel):
        jwks_uri: str
        issuer: str

    try:
        oidc = parse_obj_as(Oid, r.json())
        log.info(f"{oidc=}")
    except ValidationError as e:
        raise RuntimeError(str(e))

    jwks = requests.get(oidc.jwks_uri)
    if not jwks:
        raise RuntimeError("Could not get jwks")

    public_keys = {}
    keys = [key for key in jwks.json()["keys"] if key["kty"] == "RSA"]
    for jwk in keys:
        kid = jwk["kid"]
        public_keys[kid] = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))

    return {
        "public_keys": public_keys,
        "issuer": oidc.issuer,
    }


class Auth(HTTPBearer):
    def __init__(self, authority, audience):
        super().__init__()
        self.authority = authority
        self.audience = audience

    async def __call__(self, request: Request):
        ac = await super().__call__(request)
        token = ac.credentials
        self.verify(token, get_oidc(self.authority))
        return token

    def verify(self, token, oidc, decode=jwt.decode):
        try:
            jwt_header = jwt.get_unverified_header(token)
        except jwt.DecodeError as e:
            log.warning(f"could not get header: {e}")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        kid = jwt_header.get("kid")
        if kid is None:
            log.warning("jwt missing kid")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        key = oidc.get("public_keys").get(kid)
        if key is None:
            log.warning(f"oidc missing key for: {kid}")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        try:
            decode(
                jwt=token,
                key=key,
                issuer=oidc.get("issuer"),
                audience=self.audience,
                algorithms=["RS256"],
            )
        except jwt.PyJWTError as e:
            log.warning(f"invalid token: {e}")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
