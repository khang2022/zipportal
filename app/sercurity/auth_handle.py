import time
import jwt
from base.configs import settings
from typing import Dict
from base.log import logger

JWT_SECRET = settings.ACCESS_TOKEN_SECRET
JWT_ALGORITHM = settings.ALGORITHM


def token_response(token: str):
    return {"access_token": token}


def encodeJWT(user_email: str, role: str, id: int) -> Dict[str, str]:

    payload = {
        "expires": time.time() + 6000,
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)


def decodeJWT(token: str) -> dict:

    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        # return decoded_token if decoded_token["expires"] >= time.time() else None
        return decoded_token
    except Exception as e:
        return {}
