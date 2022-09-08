from motor.motor_asyncio import AsyncIOMotorClient
import logging


from app.config.config import Configs


class MongoDB:

    def __init__(self):
        self._conn: AsyncIOMotorClient = None

    async def connect_to_db(self):
        logging.info("Connecting to DB!")
        self._conn = AsyncIOMotorClient(Configs.app_configs.get("db_url"))
        logging.info("Connected to DB!")

    async def close_connection_to_db(self):
        logging.info("Closing the connection to DB!")
        self._conn.close()
        logging.info("Connection to db closed!")

    async def get_db(self) -> AsyncIOMotorClient:
        return self._conn[Configs.app_configs.get("db_name")]


db = MongoDB()
