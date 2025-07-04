from loguru import logger
import asyncio
from src.detector.infrastructure.openai.client import OpenAIClient
from src.rock.application.use_cases.fill_unfilled_data import FillUnfilledDataUseCase
from src.rock.infrastructure.elasticsearch.unit_of_work import ESRockUnitOfWork


async def _fill_rocks_data():
    openai_client = OpenAIClient()
    rock_uow = ESRockUnitOfWork()
    logger.info("Starting fill rocks data")
    await FillUnfilledDataUseCase(openai_client, rock_uow).execute()
    logger.info("Finished fill rocks data")


def fill_rocks_data():
    asyncio.run(_fill_rocks_data())
