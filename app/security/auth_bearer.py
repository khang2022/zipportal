from fastapi import Depends, HTTPException
from .auth_handle import decodeJWT
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials



bearer_scheme = HTTPBearer()

async def get_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    # if decodeJWT(credentials.credentials):
    #     return credentials
    # else:
    #     raise HTTPException(status_code=403, detail="Invalid token or expired token")
    return credentials
