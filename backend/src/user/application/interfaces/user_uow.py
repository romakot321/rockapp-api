import abc

from src.rock.application.interfaces.rock_repository import IRockRepository
from src.user.application.interfaces.user_repository import IUserRepository


class IUserUnitOfWork(abc.ABC):
    user: IUserRepository
    rock: IRockRepository

    async def commit(self):
        await self._commit()

    @abc.abstractmethod
    async def _rollback(self):
        pass

    @abc.abstractmethod
    async def _commit(self):
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, *excinfo):
        await self._rollback()
