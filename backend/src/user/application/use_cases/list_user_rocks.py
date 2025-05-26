from src.rock.domain.entities import Rock
from src.user.application.interfaces.user_uow import IUserUnitOfWork
from src.user.domain.dtos import UserRockDTO
from src.user.domain.entities import User
from src.core.config import settings


class ListUserRocksUseCase:
    def __init__(self, user_uow: IUserUnitOfWork):
        self.user_uow = user_uow

    async def execute(self, user_pk: str) -> list[UserRockDTO]:
        async with self.user_uow:
            user = await self.user_uow.user.get_by_pk(user_pk)
            rocks = await self._get_rocks_list(user)
        return rocks

    async def _get_rocks_list(self, user: User) -> list[UserRockDTO]:
        rocks = []
        for detection in user.rock_detections:
            rock = await self.user_uow.rock.get_by_id(detection.rock_id)
            rocks.append(self._rock_to_dto(rock))
        return rocks

    @staticmethod
    def _rock_to_dto(rock: Rock) -> UserRockDTO:
        return UserRockDTO(id=rock.id, name=rock.name, image_url=f"https://{settings.DOMAIN}/api/rock/{rock.id}/image")
