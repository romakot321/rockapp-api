from src.user.application.interfaces.user_uow import IUserUnitOfWork
from src.user.domain.dtos import UserReadDTO
from src.user.domain.entities import User, UserRank


class GetUserUseCase:
    def __init__(self, user_uow: IUserUnitOfWork) -> None:
        self.user_uow = user_uow

    async def execute(self, pk: str) -> UserReadDTO:
        async with self.user_uow:
            user = await self.user_uow.user.get_by_pk(pk)
            rocks_total_cost = await self._calculate_rocks_cost(user)
            rank = await self._calculate_user_rank(user, rocks_total_cost)
        return UserReadDTO(
            id=user.id,
            rank=rank,
            rocks_count=len(user.rock_detections),
            rocks_total_cost=rocks_total_cost,
            favorite_rock_id=user.favorite_rock_id
        )

    async def _calculate_user_rank(self, user: User, rocks_total_cost: int) -> UserRank:
        return UserRank.rank_1

    async def _calculate_rocks_cost(self, user: User) -> int:
        total = 0
        for detection in user.rock_detections:
            rock = await self.user_uow.rock.get_by_id(detection.rock_id)
            total += rock.price
        return total
