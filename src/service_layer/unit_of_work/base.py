from abc import ABC, abstractmethod

from accessify import protected

from src.adapters.db.database import get_db_session


class AbstractUnitOfWork(ABC):

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.rollback()

    def __await__(self):
        return self.__aenter__().__await__()

    @protected
    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @protected
    @abstractmethod
    def rollback(self):
        raise NotImplementedError


DEFAULT_SESSION_FACTORY = get_db_session
