from abc import ABC, abstractmethod
from typing import Generic, Type, TypeVar

from src.adapters.dto.response import BaseSchema

IN_SCHEMA = TypeVar("IN_SCHEMA", bound=BaseSchema)
SCHEMA = TypeVar("SCHEMA", bound=BaseSchema)
TABLE = TypeVar("TABLE")


class AbstractRepository(Generic[IN_SCHEMA, SCHEMA, TABLE], ABC):
    @property
    @abstractmethod
    def _table(self) -> Type[TABLE]:
        pass

    @property
    @abstractmethod
    def _schema(self) -> Type[SCHEMA]:
        pass

    @abstractmethod
    def add(self, in_schema: IN_SCHEMA):
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, reference) -> TABLE:
        raise NotImplementedError
