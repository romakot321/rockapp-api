from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.user.application.interfaces.user_rank_repository import IUserRankRepository
from src.user.domain.entities import UserRank
from src.user.infrastructure.db.orm import UserRankDB


class PGUserRankRepository(IUserRankRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def calculate_rank(self, rocks_count: int) -> UserRank:
        query = select(UserRankDB).order_by(UserRankDB.rocks_count)
        ranks = list(await self.session.scalars(query))
        for i in range(1, len(ranks)):
            prev_rank, cur_rank = ranks[i - 1], ranks[i]
            if prev_rank.rocks_count <= rocks_count < cur_rank.rocks_count:
                return UserRank(title=prev_rank.title, next_rocks_count=cur_rank.rocks_count)
        return UserRank(title=ranks[-1].title, next_rocks_count=0)

