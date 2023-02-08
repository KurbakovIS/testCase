from sqlalchemy import Column, String, Integer, Boolean, MetaData, Date, ForeignKey
from sqlalchemy.testing.schema import Table
from sqlalchemy.orm import registry

metadata = MetaData()
mapper_registry = registry(metadata=metadata)

author = Table(
    'authors',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(30)),
    Column('birthday', Date),
)

book = Table(
    'books',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(30)),
    Column('year', Integer),
    Column('author_id', Integer, ForeignKey("authors.id")),
)
