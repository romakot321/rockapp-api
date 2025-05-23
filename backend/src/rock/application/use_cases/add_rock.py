from fastapi import HTTPException
from src.rock.application.interfaces.rock_uow import IRockUnitOfWork
from src.rock.domain.entities import Rock


class AddRockUseCase:
    ROCK_STORAGE_TOKEN = "iloverocks"

    def __init__(self, uow: IRockUnitOfWork, rock_storage_token: str) -> None:
        self._validate_rock_storage_token(rock_storage_token)
        self.uow = uow

    @classmethod
    def _validate_rock_storage_token(cls, value: str):
        if value != cls.ROCK_STORAGE_TOKEN:
            raise HTTPException(401)

    async def execute(self, data: Rock) -> None:
        async with self.uow:
            await self.uow.rocks.create(data)
