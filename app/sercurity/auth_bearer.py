from fastapi import Request, Header
from .auth_handle import decodeJWT
from base.log import logger
from typing import Union
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


class JWTBearer:
    def __init__(self):
        ...

    async def __call__(self, headers: Union[str, None] = Header(default=None)):
        if headers:
            payload = self.verify_jwt(headers)
            if not payload:
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token."
                )
            return headers
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid = False
        if decodeJWT(jwtoken):
            isTokenValid = True
        return isTokenValid
