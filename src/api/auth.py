import jwt
from fastapi import HTTPException
from fastapi import Request
from fastapi import status
from fastapi.security import HTTPBearer


class Oauth(HTTPBearer):
    def __init__(self, issuer, audience, public_keys):
        super().__init__()
        self.issuer = issuer
        self.audience = audience
        self.public_keys = public_keys

    async def __call__(self, request: Request):
        ac = await super().__call__(request)
        token = ac.credentials
        self.verify(token)
        return token

    def verify(self, token, decode=jwt.decode):
        try:
            jwt_header = jwt.get_unverified_header(token)
        except jwt.DecodeError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        kid = jwt_header.get("kid")
        if kid is None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        key = self.public_keys.get(kid)
        if key is None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        try:
            decode(
                jwt=token,
                key=key,
                issuer=self.issuer,
                audience=self.audience,
                algorithms=["RS256"],
            )
        except jwt.PyJWTError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
