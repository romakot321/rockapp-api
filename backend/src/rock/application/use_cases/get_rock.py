from uuid import UUID
from src.rock.application.interfaces.rock_uow import IRockUnitOfWork
from src.rock.domain.entities import Rock


class GetRockUseCase:
    def __init__(self, uow: IRockUnitOfWork) -> None:
        self.uow = uow

    async def execute_with_name(self, rock_name: str) -> Rock:
        async with self.uow:
            rock = await self.uow.rocks.search_by_name(rock_name.lower())
        return rock

    async def execute_with_pk(self, rock_pk: UUID) -> Rock:
        async with self.uow:
            rock = await self.uow.rocks.get_by_id(rock_pk)
        return rock
