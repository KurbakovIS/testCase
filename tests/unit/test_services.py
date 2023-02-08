from abc import ABC
from typing import Type

import pytest

from src.db.orm.models import Example
from src.db.repositories.base import AbstractRepository, TABLE, SCHEMA
from src.dto.example import ExampleIn, ExampleOut
from src.domain.model import ExampleProduct
from src.service_layer.author_service import AuthorService
from src.service_layer.unit_of_work.base import AbstractUnitOfWork


class FakeExampleRepository(AbstractRepository):

    @property
    def _in_schema(self) -> Type[ExampleIn]:
        return ExampleIn

    @property
    def _schema(self) -> Type[ExampleOut]:
        return ExampleOut

    @property
    def _table(self) -> Type[Example]:
        return Example

    def __init__(self, batches):
        self._batches = list(batches)

    def get_by_id(self, reference) -> TABLE:
        pass

    def add(self, batch: ExampleIn):
        self._batches.append(batch)

    def get(self, message) -> list[TABLE]:
        print(self._batches)
        return next((p for p in self._batches if p.message == message), None)

    def list(self) -> list[TABLE]:
        return list(self._batches)


class FakeUnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        self.example_models = FakeExampleRepository([])
        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        pass


@pytest.mark.asyncio
async def test_add_batch_for_new_product():
    uow = FakeUnitOfWork()
    service = AuthorService(uow)
    new_example = ExampleProduct(message="CRUNCHY-ARMCHAIR", employee_id=100, status=True)
    await service.create_record(new_example)
    assert uow.example_models.get("CRUNCHY-ARMCHAIR") is not None
    assert uow.committed


