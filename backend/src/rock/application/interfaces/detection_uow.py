import abc

from src.rock.application.interfaces.detection_repository import IDetectionRepository


class IDetectionUnitOfWork(abc.ABC):
    detections: IDetectionRepository

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
