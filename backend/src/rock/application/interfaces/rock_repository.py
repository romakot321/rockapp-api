import abc

from src.rock.domain.entities import Rock


class IRockRepository(abc.ABC):
    @abc.abstractmethod
    async def search_by_name(self, name: str) -> Rock: ...

    @abc.abstractmethod
    async def create(self, rock_data: Rock) -> None: ...
