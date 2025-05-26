from fastapi import HTTPException
from backend.src.user.application.interfaces.user_uow import IUserUnitOfWork


class GetUserAvatarUseCase:
    def __init__(self, user_uow: IUserUnitOfWork) -> None:
        self.user_uow = user_uow

    async def execute(self, user_pk: str) -> bytes:
        async with self.user_uow:
            user = await self.user_uow.user.get_by_pk(user_pk)
        if user.avatar is None:
            raise HTTPException(400, detail="User hasn't avatar")
        return user.avatar
