from sqlalchemy.orm import relationship

from src.adapters.db.orm.models import mapper_registry, book, author
from src.domain.author import Book, Author


def start_mappers():
    mapper_registry.map_imperatively(Book, book)
    mapper_registry.map_imperatively(Author, author,
                                     properties={
                                         'books': relationship(Book, backref="author", lazy='subquery'),
                                     }
                                     )
