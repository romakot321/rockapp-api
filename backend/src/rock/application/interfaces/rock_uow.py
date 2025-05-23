import abc

from src.rock.application.interfaces.rock_repository import IRockRepository


class IRockUnitOfWork(abc.ABC):
    rocks: IRockRepository

    async def __aenter__(self):
        return self

    async def __aexit__(self, *excinfo):
        pass
