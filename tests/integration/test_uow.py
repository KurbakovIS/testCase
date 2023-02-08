import pytest

from src.service_layer.unit_of_work.author_UoW import AuthorInitOfWork


async def insert_batch(session, message, employee_id, status):
    await session.execute(
        "INSERT INTO examples (message, employee_id, status)"
        " VALUES (:message, :employee_id, :status)",
        dict(message=message, employee_id=employee_id, status=status),
    )

# TODO добавить ассинхронность в создание сесии ( не создается корректно)
@pytest.mark.asyncio
async def test_uow_can_retrieve_a_batch_and_allocate_to_it(postgres_session_factory):
    session = postgres_session_factory()
    await insert_batch(session, "batch1", "HIPSTER-WORKBENCH", 100)
    session.commit()

    uow = AuthorInitOfWork(postgres_session_factory)
    async with uow:
        products = await uow.example_models.get_all()

    assert len(products) != 0
