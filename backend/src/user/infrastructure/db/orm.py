from sqlalchemy.orm import Mapped, mapped_column


class UserRankDB():
    total_cost: Mapped[int]
    title: Mapped[str]
