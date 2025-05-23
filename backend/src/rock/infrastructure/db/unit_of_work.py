from sqlalchemy.ext.asyncio import AsyncSession

from src.rock.application.interfaces.detection_uow import IDetectionUnitOfWork
from src.rock.infrastructure.db.detection_repository import PGDetectionRepository
from src.db.engine import async_session_maker


class PGDetectionUnitOfWork(IDetectionUnitOfWork):
    def __init__(self, session_factory=async_session_maker):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session: AsyncSession = self.session_factory()
        self.detections = PGDetectionRepository(self.session)
        return await super().__aenter__()

    async def __aexit__(self, *args):
        await super().__aexit__(*args)
        await self.session.close()

    async def _commit(self):
        await self.session.commit()

    async def _rollback(self):
        await self.session.rollback()
