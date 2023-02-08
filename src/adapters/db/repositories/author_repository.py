import logging
from typing import Type

from sqlalchemy import insert, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import contains_eager, lazyload, joinedload

from src.adapters.db.repositories.base import AbstractRepository
from src.adapters.dto.author import AuthorOut, AuthorIn
from src.domain.author import Author, Book


class AuthorRepository(AbstractRepository):
    def __init__(self, session):
        self.db: AsyncSession = session

    @property
    def _in_schema(self) -> Type[AuthorIn]:
        return AuthorIn

    @property
    def _schema(self) -> Type[AuthorOut]:
        return AuthorOut

    @property
    def _table(self) -> Type[Author]:
        return Author

    async def add(self, in_schema: AuthorIn) -> Author:
        query = insert(Author).values(in_schema).returning(Author)
        res = await self.db.execute(query)
        return res.first()

    async def add_books_in_author(self, in_schema):
        query = insert(Book).values(in_schema)
        await self.db.execute(query)

    async def get_all(self):
        entry = await self.db.execute(select(Author)
                                      .order_by(Author.id))
        return entry.fetchall()

    async def get_by_id(self, entry_id: id):
        qur = select(self._table).where(Author.id == entry_id)
        entry = await self.db.execute(qur)
        return entry.fetchone()
