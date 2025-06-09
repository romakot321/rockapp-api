from fastapi import HTTPException
from loguru import logger
from src.rock.application.interfaces.image_storage import IImageStorage
from src.rock.domain.dtos import RockStoreDTO
from src.rock.application.interfaces.rock_uow import IRockUnitOfWork
from src.rock.domain.entities import Rock


class AddRockUseCase:
    ROCK_STORAGE_TOKEN = "iloverocks"

    def __init__(self, uow: IRockUnitOfWork, image_storage: IImageStorage, rock_storage_token: str) -> None:
        self._validate_rock_storage_token(rock_storage_token)
        self.uow = uow
        self.image_storage = image_storage

    @classmethod
    def _validate_rock_storage_token(cls, value: str):
        if value != cls.ROCK_STORAGE_TOKEN:
            raise HTTPException(401)

    async def execute(self, data: RockStoreDTO) -> None:
        rock = Rock(**data.model_dump(exclude_unset=True))
        async with self.uow:
            await self.uow.rocks.create(rock)
        if data.image_url:
            try:
                await self.image_storage.transfer_image(data.image_url, str(data.id))
            except Exception as e:
                logger.warning(f"Failed to load rock image for {rock.id}: {str(e)}")
