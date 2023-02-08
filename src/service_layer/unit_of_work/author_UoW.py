from src.adapters.db.repositories.author_repository import AuthorRepository
from src.service_layer.unit_of_work.base import AbstractUnitOfWork, DEFAULT_SESSION_FACTORY


class AuthorInitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()
        self.author_repository = AuthorRepository(self.session)
        return await super().__aenter__()

    async def __aexit__(self, *args):
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def close(self):
        await self.session.close()

    async def rollback(self):
        await self.session.rollback()
