from logging import getLogger

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from src import settings
from src.settings import db_settings

log = getLogger()


engine = create_async_engine(
    db_settings.dsn,
    pool_pre_ping=True,
    pool_use_lifo=True,
    pool_size=20,
    echo=True,
    echo_pool="debug",
    max_overflow=5,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    class_=AsyncSession,
    bind=engine,
    expire_on_commit=False,
)

get_db_session = SessionLocal
