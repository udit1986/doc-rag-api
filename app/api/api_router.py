from fastapi import APIRouter

from app.api import api_messages
from app.api.endpoints import documents

api_router = APIRouter()
api_router.include_router(users.router, prefix="/documents", tags=["documents"])
