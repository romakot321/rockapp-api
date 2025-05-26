from typing import AsyncIterator
from src.rock.infrastructure.elasticsearch.rock_repository import ESRockRepository
from src.rock.application.interfaces.rock_repository import IRockRepository
from src.elasticsearch.engine import get_elasticsearch_session


async def get_elasticsearch_rock_repository() -> AsyncIterator[IRockRepository]:
    session = await get_elasticsearch_session()
    yield ESRockRepository(session)
    await session.close()

