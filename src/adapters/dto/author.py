from datetime import date, datetime
from typing import List

from pydantic import validator

from src.adapters.dto.response import BaseSchema


class BookOut(BaseSchema):
    id: int
    name: str
    year: int

    class Config:
        orm_mode = True


class BookIn(BaseSchema):
    name: str
    year: int


class AuthorOut(BaseSchema):
    id: int
    name: str
    birthday: date
    books: List[BookOut]

    class Config:
        orm_mode = True


class AuthorIn(BaseSchema):
    name: str
    birthday: date
    books: List[BookIn]

    @validator("birthday", pre=True)
    def parse_birthdate(cls, value):
        return datetime.strptime(
            value,
            "%d.%m.%Y"
        ).date()

    class Config:
        schema_extra = {
            "example": {
                "name": "Василий",
                "birthday": "18.03.1888",
                "books": [
                    {
                        "name": "всячина",
                        "year": 1999
                    }
                ]
            }
        }
