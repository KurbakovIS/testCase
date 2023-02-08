from fastapi import APIRouter

from src.entrypoints.v1.endpoints import author

api_router = APIRouter()

api_router.include_router(author.router, prefix="/v1/authors", tags=["Author"])