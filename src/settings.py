import os
from enum import Enum, unique

from pydantic import BaseSettings, PositiveInt
from pydantic.types import NonNegativeInt


@unique
class Environment(str, Enum):
    local = "local"
    development = "development"
    production = "production"


class ServerSettings(BaseSettings):
    server_host: str = "127.0.0.1"
    server_port: PositiveInt = 8010
    debug: bool = 1


class ClientUrls(BaseSettings):
    websocket_service: str = "http://localhost:5000"


def get_api_url():
    host = os.environ.get("API_HOST", "localhost")
    port = 8010 if host == "localhost" else 80
    return f"http://{host}:{port}"


class DatabaseSettings(BaseSettings):
    dialect: str = "postgresql"

    db_user: str = "postgres"
    db_pass: str = "qwerty"
    db_host: str = "localhost"
    db_port: str = 5432
    db_name: str = "Author"

    db_pool_min_size: PositiveInt = 10
    db_pool_max_size: PositiveInt = 10
    statement_cache_size: NonNegativeInt = 0  # 0 to work with transaction_pooling

    @property
    def uri(self):
        db_name = self.db_name
        return f"{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{db_name}"

    @property
    def dsn_no_driver(self) -> str:
        """Возвращает dsn при отсутсвии драйвера бд.

        Returns:
            dsn_no_driver
        """
        return f"{self.dialect}://{self.uri}"

    @property
    def dsn(self) -> str:
        """Возвращает dsn.

        Returns:
            dsn
        """
        # https://docs.sqlalchemy.org/en/14/dialects/postgresql.html#dialect-postgresql-asyncpg
        return f"{self.dialect}+asyncpg://{self.uri}"


db_settings = DatabaseSettings(
    _env_file=".env",
    _env_file_encoding="utf-8",
)

server_settings = ServerSettings(
    _env_file=".env",
    _env_file_encoding="utf-8",
)

client_urls = ClientUrls(
    _env_file=".env",
    _env_file_encoding="utf-8",
)
