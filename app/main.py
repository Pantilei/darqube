import uvicorn
from fastapi import FastAPI

from app.db.db import db
from app.api.v1.api import api_router

app = FastAPI()

app.add_event_handler("startup", db.connect_to_db)
app.add_event_handler("startup", db.create_indexes)
app.add_event_handler("startup", db.create_demo_data)
app.add_event_handler("shutdown", db.close_connection_to_db)


app.include_router(api_router)
