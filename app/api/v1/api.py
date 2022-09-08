from fastapi import APIRouter

from app.api.v1.endpoints import auth, user
from app.config.config import settings

api_router = APIRouter(
    prefix=settings.api_v1
)

api_router.include_router(user.router)
api_router.include_router(auth.router)
