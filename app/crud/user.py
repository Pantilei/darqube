from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import DuplicateKeyError
from fastapi import HTTPException, status
from datetime import datetime, timezone
from typing import Union, List

from app.models.mongo_model import OID
from app.models.user import UserCreate, User, UserToDB, UserUpdate
from app.core.security import hash_password, verify_password

_db_collection = "users"


async def get_many(db: AsyncIOMotorDatabase, limit: int = 100) -> List[User]:
    cr = db[_db_collection].find()
    users = await cr.to_list(length=limit)
    return [User.from_mongo(u) for u in users]


async def get_by_first_name(db: AsyncIOMotorDatabase, first_name: str) -> List[User]:
    user = await db[_db_collection].find_one({
        "first_name": first_name
    })
    if user is None:
        return user
    return User.from_mongo(user)


async def get_one(db: AsyncIOMotorDatabase, user_id: OID) -> Union[User, None]:
    user = await db[_db_collection].find_one({"_id": user_id})
    if user is None:
        return user
    return User.from_mongo(user)


async def create(db: AsyncIOMotorDatabase, user: UserCreate) -> User:
    db_obj = UserToDB(
        first_name=user.first_name,
        last_name=user.last_name,
        role=user.role,
        is_active=user.is_active,
        created_at=datetime.utcnow(),
        hashed_pass=hash_password(user.password),
    )
    try:
        result = await db[_db_collection].insert_one(db_obj.mongo())
    except DuplicateKeyError as de:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this first name already exists!"
        )

    return User(**db_obj.dict(), id=result.inserted_id)


async def update(db: AsyncIOMotorDatabase, user: UserUpdate, user_id: OID) -> Union[User, None]:

    res = await db[_db_collection].update_one(
        {"_id": user_id},
        {"$set": {**user.mongo()}}
    )
    if res is None:
        return res

    user_obj = await db[_db_collection].find_one(
        {"_id": user_id}
    )
    return User.from_mongo(user_obj)


async def delete(db: AsyncIOMotorDatabase, user_id: OID) -> bool:

    user = await db[_db_collection].find_one({"_id": user_id})
    if user is None:
        return user
    await db[_db_collection].delete_one({"_id": user_id})

    return User.from_mongo(user)


async def authenticate(db: AsyncIOMotorDatabase, first_name: str, password: str) -> Union[User, bool]:
    user = await db[_db_collection].find_one({"first_name": first_name})
    if not user:
        return False

    if not verify_password(password, user["hashed_pass"]):
        return False

    return User.from_mongo(user)


async def update_last_login(db: AsyncIOMotorDatabase, user_id: OID) -> bool:

    res = await db[_db_collection].update_one(
        {"_id": user_id},
        {"$set": {"last_login": datetime.now(timezone.utc)}}
    )
    return bool(res)
