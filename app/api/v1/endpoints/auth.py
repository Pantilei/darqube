from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime, timezone

from app.db.db import db
from app import crud
from app.core.security import create_token
from app.models.token import Token
from app.models.user import UserUpdate

router = APIRouter()


@router.post("/access-token", response_model=Token)
async def login(db: AsyncIOMotorDatabase = Depends(db.get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = await crud.user.authenticate(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username or password is incorrect!",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_token({
        "sub": str(user.id),
        "first_name": user.first_name,
        "last_name": user.last_name,
        "role": user.role
    })

    print("\n\nuser.id", user.id)
    res = await crud.user.update_last_login(db, user.id)
    print("res", res)
    return Token(**{
        "access_token": token,
        "token_type": "bearer"
    })
