import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.adapters.db.orm.orm import start_mappers
from src.entrypoints.v1.api import api_router
from src.logging.costum_logging import CustomizeLogger

tags_metadata = [
    {"name": "event", "description": "Управление событиями"},
]
logger = logging.getLogger(__name__)
config_path = Path(__file__).with_name("logging_config.json")


def create_app() -> FastAPI:
    new_app = FastAPI(
        title="author API",
        version="0.0.1",
        description="REST API and backend services",
        openapi_tags=tags_metadata,
        docs_url="/api/author/docs",
        redoc_url="/api/author/redoc",
        openapi_url="/api/author/openapi.json",
        on_startup=[start_mappers],
    )
    new_app.include_router(api_router)
    new_app.logger = CustomizeLogger.make_logger(config_path)

    return new_app


app = create_app()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
