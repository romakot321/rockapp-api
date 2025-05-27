import abc

from src.user.domain.entities import UserRank


class IUserRankRepository(abc.ABC):
    @abc.abstractmethod
    async def calculate_rank(self, rocks_count: int) -> UserRank: ...
