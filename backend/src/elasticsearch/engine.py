from elasticsearch import AsyncElasticsearch

from src.core.config import settings


async def get_elasticsearch_session() -> AsyncElasticsearch:
    return AsyncElasticsearch(
        hosts=[f'http://{settings.ELASTICSEARCH_USER}:{settings.ELASTICSEARCH_PASSWORD}@{settings.ELASTICSEARCH_HOST}:9200'],
        max_retries=10,
        retry_on_timeout=True,
    )

