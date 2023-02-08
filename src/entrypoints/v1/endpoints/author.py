import logging
from typing import List

from sqlalchemy.exc import SQLAlchemyError
from starlette import status

from fastapi import APIRouter, HTTPException

from src.adapters.dto.author import AuthorOut, AuthorIn
from src.service_layer.author_service import AuthorService
from src.service_layer.unit_of_work.author_UoW import AuthorInitOfWork

router = APIRouter()


@router.get("/", response_model=List[AuthorOut])
async def get_all_authors():
    service = AuthorService(AuthorInitOfWork())
    return await service.get_all_authors()


@router.get("/{author_id}", response_model=AuthorOut)
async def get_all_authors(author_id: int):
    service = AuthorService(AuthorInitOfWork())
    return await service.get_author_by_id(author_id)


@router.post("", status_code=status.HTTP_200_OK)
async def get_all_authors(data: AuthorIn):
    try:
        service = AuthorService(AuthorInitOfWork())
        await service.create_record(data)
    except SQLAlchemyError as e:
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Error when saving an author"
        )
