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
        async for rock_id in (await self.rock_uow.rocks.iter_ids()):
            try:
                rock_data = await self.rock_uow.rocks.get_by_id(UUID(rock_id))
                result = await self.openai_client.fill_rock_data(rock_data.model_dump())
                rock = Rock.model_validate_json(result)
                await self.rock_uow.rocks.create(rock)
            except Exception as e:
                logger.debug(f"Failed fill {rock_id=}: {e}")
            else:
                logger.debug(f"Filled {rock_id=}. From {rock_data} TO {result}")
