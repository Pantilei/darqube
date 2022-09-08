from fastapi import APIRouter, Response, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List, Union

from app.db.db import db
from app.models.mongo_model import OID
from app.models.user import User, UserCreate, UserUpdate
from app import crud
from app.errors import UnprocessableError


router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.get("/", response_model=List[User])
async def get_users(limit: int = 100, db: AsyncIOMotorClient = Depends(db.get_db)):
    users = await crud.user.get_many(db, limit=limit)
    return users


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: OID, db: AsyncIOMotorClient = Depends(db.get_db)):
    user = await crud.user.get_one(db, user_id)
    if user is None:
        return Response(status_code=204)

    return user


@router.post("/", response_model=User)
async def create_user(user: UserCreate, db: AsyncIOMotorClient = Depends(db.get_db)):
    user = await crud.user.create(db, user)
    return user


@router.put("/{user_id}", response_model=User)
async def update_user(user_id: OID, user: UserUpdate, db: AsyncIOMotorClient = Depends(db.get_db)):
    user = await crud.user.update(db, user, user_id)
    if user is None:
        raise HTTPException(["User with provided id doesn't exist!"])
    return user


@router.delete("/{user_id}")
async def delete_user(user_id: OID, db: AsyncIOMotorClient = Depends(db.get_db)):
    user = await crud.user.delete(db, user_id)
    if user is None:
        raise UnprocessableError(["User with provided id doesn't exist!"])
    return Response(status_code=204)
