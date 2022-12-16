from base.configs import settings
from passlib.context import CryptContext


JWT_SECRET = settings.ACCESS_TOKEN_SECRET


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password, salt=JWT_SECRET)
