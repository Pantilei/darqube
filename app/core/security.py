
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from typing import Union

from app.config.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def create_token(data: dict, expire_delta: Union[datetime, None] = None):
    to_encode = data.copy()
    if expire_delta:
        exp = datetime.now(timezone.utc) + expire_delta
    else:
        exp = datetime.now(timezone.utc) + timedelta(minutes=settings.api_v1)
