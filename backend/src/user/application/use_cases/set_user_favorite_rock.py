from src.user.application.interfaces.user_uow import IUserUnitOfWork


class SetUserFavoriteRock:
    def __init__(self, user_uow: IUserUnitOfWork) -> None:
        self.user_uow = user_uow
