from uuid import UUID
from sqlalchemy import ForeignKey, LargeBinary, select
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.util import hybridproperty
from src.db.base import Base, BaseMixin


class UserRankDB(Base):
    __tablename__ = "user_ranks"

    rocks_cost: Mapped[int]
    title: Mapped[str] = mapped_column(primary_key=True)


class UserDB(BaseMixin, Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(primary_key=True)
    app_bundle: Mapped[str]
    name: Mapped[str]
    avatar: Mapped[bytes | None] = mapped_column(type_=LargeBinary, nullable=True)
    favorite_rock: Mapped[UUID | None] = mapped_column(ForeignKey("rocks.id", ondelete="SET NULL"))

    rock_detections: Mapped[list['RockDetectionDB']] = relationship(lazy="selectin", back_populates="user")

    @hybridproperty
    def successful_rock_detections(self):
        return [detection for detection in self.rock_detections if detection.status == "finished"]

    @successful_rock_detections.expression
    @classmethod
    def successful_rock_detections(cls):
        return select(cls.rock_detections).filter_by(status="finished")

