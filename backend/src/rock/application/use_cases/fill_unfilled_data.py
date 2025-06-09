from uuid import UUID

from loguru import logger
from src.detector.infrastructure.openai.client import OpenAIClient
from src.rock.application.interfaces.rock_repository import IRockRepository
from src.rock.application.interfaces.rock_uow import IRockUnitOfWork
from src.rock.domain.entities import Rock


class FillUnfilledDataUseCase:
    def __init__(self, openai_client: OpenAIClient, rock_uow: IRockUnitOfWork) -> None:
        self.openai_client = openai_client
        self.rock_uow = rock_uow

    async def execute(self) -> None:
        async with self.rock_uow:
            async for rock_id in await self.rock_uow.rocks.iter_ids():
                try:
                    await self._fill(rock_id)
                except Exception as e:
                    logger.debug(f"Failed fill {rock_id=}: {e}")

    async def _fill(self, rock_id: str):
        rock_data = (await self.rock_uow.rocks.get_by_id(UUID(rock_id))).model_dump()
        if not self._is_rock_need_filling(rock_data):
            logger.debug(f"Skipped {rock_id=} {rock_data}")
            return

        result = await self.openai_client.fill_rock_data(rock_data)
        rock = Rock.model_validate_json(result)
        await self.rock_uow.rocks.create(rock)
        logger.debug(f"Filled {rock_id=}. From {rock_data} TO {result}")

    def _is_rock_need_filling(self, rock_data: dict) -> bool:
        empty_fields_count = len([i for i in rock_data.values() if not i])
        fields_count = len(rock_data)
        return empty_fields_count / fields_count >= 0.5
