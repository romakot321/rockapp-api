from typing import Annotated

from fastapi import Depends
from src.user.application.interfaces.user_uow import IUserUnitOfWork
from src.user.infrastructure.user_uow import UserUnitOfWork


async def get_user_uow() -> IUserUnitOfWork:
    return UserUnitOfWork()


UserUoWDepend = Annotated[IUserUnitOfWork, Depends(get_user_uow)]
