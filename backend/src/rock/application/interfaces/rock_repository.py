import abc
from typing import AsyncGenerator
from uuid import UUID

from src.rock.domain.entities import Rock


class IRockRepository(abc.ABC):
    @abc.abstractmethod
    async def get_by_id(self, id: UUID) -> Rock: ...

    @abc.abstractmethod
    async def search_by_name(self, name: str) -> Rock: ...

    @abc.abstractmethod
    async def create(self, rock_data: Rock) -> None: ...

    @abc.abstractmethod
    async def iter_ids(self) -> AsyncGenerator[str]: ...
