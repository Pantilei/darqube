from motor.motor_asyncio import AsyncIOMotorClient
from uuid import uuid4
from datetime import datetime
from typing import Union, List

from app.models.mongo_model import OID
from app.models.user import UserCreate, UserInDB, User, UserToDB, UserUpdate
from app.core.security import hash_password

_db_collection = "users"


async def get_many(db: AsyncIOMotorClient, limit: int = 100) -> List[User]:
    cr = db[_db_collection].find()
    users = await cr.to_list(length=limit)
    return [User.from_mongo(u) for u in users]


async def get_one(db: AsyncIOMotorClient, user_id: OID) -> Union[User, None]:
    user = await db[_db_collection].find_one({"_id": user_id})
    if user is None:
        return user
    return User.from_mongo(user)


async def create(db: AsyncIOMotorClient, user: UserCreate) -> User:
    db_obj = UserToDB(
        first_name=user.first_name,
        last_name=user.last_name,
        role=user.role,
        is_active=user.is_active,
        created_at=datetime.utcnow(),
        hashed_pass=hash_password(user.password),
    )

    result = await db[_db_collection].insert_one(db_obj.mongo())

    return User(**db_obj.dict(), id=result.inserted_id)


async def update(db: AsyncIOMotorClient, user: UserUpdate, user_id: OID) -> Union[User, None]:

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


async def delete(db: AsyncIOMotorClient, user_id: OID) -> bool:

    user = await db[_db_collection].find_one({"_id": user_id})
    print("\n\nUSER: ", user)
    if user is None:
        return user
    await db[_db_collection].delete_one({"_id": user_id})

    return User.from_mongo(user)
