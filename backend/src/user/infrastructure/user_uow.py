from sqlalchemy.ext.asyncio import AsyncSession
from src.db.dependencies import get_async_session
from src.rock.infrastructure.elasticsearch.dependencies import get_elasticsearch_rock_repository
from src.user.infrastructure.db.repositories import PGUserRepository
from src.user.application.interfaces.user_uow import IUserUnitOfWork


class UserUnitOfWork(IUserUnitOfWork):
    def __init__(self, session_factory=get_async_session, rock_repository_factory=get_elasticsearch_rock_repository) -> None:
        self.session_factory = session_factory
        self.rock_repository_factory = rock_repository_factory()

    async def _commit(self):
        await self.session.commit()

    async def _rollback(self):
        await self.session.rollback()

    async def __aenter__(self):
        self.session: AsyncSession = await self.session_factory()
        self.rock = await anext(self.rock_repository_factory)
        self.user = PGUserRepository(self.session)
        return await super().__aenter__()

    async def __aexit__(self, *args):
        await super().__aexit__(*args)
        await self.session.close()
        try:
            await anext(self.rock_repository_factory)
        except StopAsyncIteration:
            pass
