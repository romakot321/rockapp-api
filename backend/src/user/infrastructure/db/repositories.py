from typing import Any
from uuid import UUID

from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.db.exceptions import ModelNotFoundException
from src.db.exceptions import ModelConflictException
from src.user.infrastructure.db.orm import UserDB
from src.user.application.interfaces.user_repository import IUserRepository
from src.user.domain.entities import User, UserCreate, UserUpdate


class PGUserRepository(IUserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def _flush(self, exc_args: Any):
        try:
            await self.session.flush()
        except IntegrityError:
            raise ModelConflictException(UserDB.__tablename__, exc_args)

    async def get_by_pk(self, pk: str) -> User:
        model = await self.session.get(UserDB, pk, options=[selectinload(UserDB.rock_detections)])
        if model is None:
            raise ModelNotFoundException(UserDB.__tablename__, pk)
        return self._to_domain(model)

    async def create(self, user_data: UserCreate) -> User:
        model = UserDB(**user_data.model_dump(exclude_unset=True))

        self.session.add(model)
        await self._flush(user_data)

        return User(
            id=model.id,
            avatar=model.avatar,
            rock_detections=[]
        )

    async def update_by_pk(self, pk: str, user_data: UserUpdate) -> User:
        query = update(UserDB).filter_by(id=pk).values(**user_data.model_dump(exclude_unset=True))
        await self.session.execute(query)
        await self._flush((pk, user_data))
        return await self.get_by_pk(pk)

    @staticmethod
    def _to_domain(model: UserDB) -> User:
        return User(
            id=model.id,
            avatar=model.avatar,
            rock_detections=model.successful_rock_detections
        )
