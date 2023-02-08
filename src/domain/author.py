from datetime import datetime
from typing import List


class Book:
    id: int
    name: str
    year: int


class Author:
    id: int
    name: str
    birthday: datetime
    books: List[Book]
