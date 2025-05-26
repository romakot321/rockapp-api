from src.rock.infrastructure.elasticsearch.rock_repository import ESRockRepository
from src.elasticsearch.engine import get_elasticsearch_session
from src.rock.application.interfaces.rock_uow import IRockUnitOfWork
from elasticsearch import AsyncElasticsearch


class ESRockUnitOfWork(IRockUnitOfWork):
    def __init__(self, session_factory=get_elasticsearch_session) -> None:
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session: AsyncElasticsearch = await self.session_factory()
        self.rocks = ESRockRepository(self.session)
        return await super().__aenter__()

    async def __aexit__(self, *args):
        await super().__aexit__(*args)
        await self.session.close()
