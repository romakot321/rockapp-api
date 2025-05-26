import abc

from src.user.domain.entities import UserCreate, UserUpdate
from src.user.domain.entities import User


class IUserRepository(abc.ABC):
    @abc.abstractmethod
    async def get_by_pk(self, pk: str) -> User: ...

    @abc.abstractmethod
    async def create(self, user_data: UserCreate) -> User: ...

    @abc.abstractmethod
    async def update_by_pk(self, pk: str, user_data: UserUpdate) -> User: ...
