from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import logging


from app.config.config import settings
from app import crud
from app.models.user import UserCreate


class MongoDB:

    def __init__(self):
        self._conn: AsyncIOMotorClient = None

    async def connect_to_db(self):
        logging.info("Connecting to DB!")
        self._conn = AsyncIOMotorClient(settings.mongodb_url)
        logging.info("Connected to DB!")

    async def close_connection_to_db(self):
        logging.info("Closing the connection to DB!")
        self._conn.close()
        logging.info("Connection to db closed!")

    async def create_indexes(self):
        await self._conn[settings.db_name]["users"].create_index("first_name", unique=True)

    async def create_demo_data(self):
        admin_user = UserCreate(
            first_name=settings.admin_user_first_name,
            last_name=settings.admin_user_last_name,
            role="admin",
            is_active=True,
            password=settings.admin_user_last_password
        )
        user = await crud.user.get_by_first_name(self._conn[settings.db_name], "admin")
        if not user:
            await crud.user.create(self._conn[settings.db_name], admin_user)

    async def get_db(self) -> AsyncIOMotorDatabase:
        return self._conn[settings.db_name]


db = MongoDB()
