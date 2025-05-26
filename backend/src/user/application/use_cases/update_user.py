from src.user.application.interfaces.user_uow import IUserUnitOfWork
from src.user.domain.dtos import UserReadShortDTO, UserUpdateDTO
from src.user.domain.entities import User, UserUpdate


class UpdateUserUseCase:
    def __init__(self, user_uow: IUserUnitOfWork) -> None:
        self.user_uow = user_uow

    async def execute(self, pk:str, user_data: UserUpdateDTO) -> UserReadShortDTO:
        command = UserUpdate(**user_data.model_dump(exclude_unset=True))
        async with self.user_uow:
            user = await self.user_uow.user.update_by_pk(pk, command)
            await self.user_uow.commit()
        return self._to_dto(user)

    @staticmethod
    def _to_dto(model: User) -> UserReadShortDTO:
        return UserReadShortDTO(id=model.id)
