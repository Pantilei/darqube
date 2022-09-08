from os import stat
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from motor.motor_asyncio import AsyncIOMotorClient
from jose import jwt, JWTError
from bson import ObjectId

from app.db.db import db
from app.config.config import settings
from app import crud
from app.models.user import User
from app.models.mongo_model import OID

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.api_v1}/access-token"
)


async def get_current_user(
    db: AsyncIOMotorClient = Depends(db.get_db), token: str = Depends(oauth2_scheme)
):
    excep = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Couldn't validate the credentials!"
    )
    try:
        payload = jwt.decode(
            token,
            settings.jwt_token_secret,
            algorithms=[settings.jwt_token_algo]
        )
        user_id = payload.get("sub")
    except JWTError as e:
        raise excep from e
    user = await crud.user.get_one(db, ObjectId(user_id))
    if not user:
        raise excep
    return user


async def get_current_admin_user(user: User = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not enough privileges"
        )
    return user
