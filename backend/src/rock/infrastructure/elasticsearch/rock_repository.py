from uuid import UUID
from src.db.exceptions import ModelNotFoundException
from src.rock.application.interfaces.rock_repository import IRockRepository
from src.rock.domain.entities import Rock
from src.rock.infrastructure.elasticsearch.responses import (
    ElasticsearchResponse,
)
from elasticsearch import AsyncElasticsearch


class ESRockRepository(IRockRepository):
    INDEX_NAME = "rock"

    def __init__(self, session: AsyncElasticsearch) -> None:
        self.session = session

    async def get_by_id(self, id: UUID) -> Rock:
        response_raw = await self.session.search(index=self.INDEX_NAME, query={"match": {"id": id}})
        response = ElasticsearchResponse.model_validate(dict(response_raw))
        if response.hits.total.value == 0:
            raise ModelNotFoundException("elasticsearch.rock", name)
        return Rock.model_validate(response.hits.hits[0].source)

    async def search_by_name(self, name: str) -> Rock:
        response_raw = await self.session.search(
            index=self.INDEX_NAME, query={"match": {"name": name}}
        )
        response = ElasticsearchResponse.model_validate(dict(response_raw))
        if response.hits.total.value == 0:
            raise ModelNotFoundException("elasticsearch.rock", name)
        max_scored_hit = max(response.hits.hits, key=lambda i: i.score)
        return Rock.model_validate(max_scored_hit.source)

    async def create(self, rock_data: Rock) -> None:
        await self.session.index(
            index=self.INDEX_NAME, id=str(rock_data.id), document=rock_data.model_dump()
        )
