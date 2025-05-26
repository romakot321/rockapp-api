from src.user.application.interfaces.user_uow import IUserUnitOfWork
from src.user.domain.entities import UserUpdate


class SetUserAvatarUseCase:
    def __init__(self, user_uow: IUserUnitOfWork) -> None:
        self.user_uow = user_uow

    async def execute(self, user_pk: str, file_body: bytes) -> None:
        async with self.user_uow:
            await self.user_uow.user.update_by_pk(user_pk, UserUpdate(avatar=file_body))
            await self.user_uow.commit()
