from motor.motor_asyncio import AsyncIOMotorClient
from uuid import uuid4
from datetime import datetime
from app.models.mongo_model import OID

from app.models.user import UserCreate, UserInDB, User, UserToDB, UserUpdate
from app.core.security import hash_password

_db_collection = "users"


async def get(db: AsyncIOMotorClient, user_id: OID) -> User:

    user = await db[_db_collection].find_one({"_in": user_id})

    return User(**user)


async def create(db: AsyncIOMotorClient, user: UserCreate) -> User:
    db_obj = UserToDB(
        first_name=user.first_name,
        last_name=user.last_name,
        role=user.role,
        is_active=user.is_active,
        created_at=datetime.utcnow(),
        hashed_pass=hash_password(),
    )
    result = await db[_db_collection].insert_one(db_obj.mongo())
    print("result: ", result)

    return User(**db_obj)


async def update(db: AsyncIOMotorClient, user: UserUpdate, user_id: OID) -> User:

    res = await db[_db_collection].update_one(
        {"_id": user_id},
        {"$set": {**user.mongo()}}
    )

    return User.from_mongo(res)


async def delete(db: AsyncIOMotorClient, user_id: OID) -> bool:

    user = await db[_db_collection].find_one({"_in": user_id})
    if user is None:
        return False
    await db[_db_collection].delete_one({"_id": user_id})

    return True
