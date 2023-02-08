from typing import List

from pydantic import parse_obj_as

from src.adapters.dto.author import AuthorOut, AuthorIn
from src.service_layer.unit_of_work.author_UoW import AuthorInitOfWork


class AuthorService:
    def __init__(self, uow):
        self.uow: AuthorInitOfWork = uow

    async def create_record(self, new_record: AuthorIn):
        """ Сохранение в базу автора со списком книг

        Args:
            new_record: инфо о новом авторе

        """
        new_author = new_record.dict()
        new_books = new_author.pop('books')

        async with self.uow:
            new_author_entity = await self.uow.author_repository.add(new_author)
            for book in new_books:
                book["author_id"] = new_author_entity.id
            await self.uow.author_repository.add_books_in_author(new_books)
            await self.uow.commit()

    async def get_all_authors(self) -> List[AuthorOut]:
        """Получение всех авторов со списком написанных книг

        Returns:
             найденный список авторов
        """
        async with self.uow:
            authors = await self.uow.author_repository.get_all()
            result = [r for r, in authors]

        return parse_obj_as(List[AuthorOut], result)

    async def get_author_by_id(self, author_id: int) -> AuthorOut:
        """Получение автора со списком книг по ID

        Args:
            author_id: Id автора

        Returns:
            найденный автор со списком написанных книг
        """
        async with self.uow:
            result = await self.uow.author_repository.get_by_id(author_id)

        return parse_obj_as(AuthorOut, result[0])
