from src.user.application.interfaces.user_uow import IUserUnitOfWork
from src.user.domain.dtos import UserCreateDTO
from src.user.domain.entities import User, UserCreate


class CreateUserUseCase:
    def __init__(self, user_uow: IUserUnitOfWork) -> None:
        self.user_uow = user_uow

    async def execute(self, user_data: UserCreateDTO) -> User:
        command = UserCreate(**user_data.model_dump())
        async with self.user_uow:
            model = await self.user_uow.user.create(command)
            await self.user_uow.commit()
        return model
