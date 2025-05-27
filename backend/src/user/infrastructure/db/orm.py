from uuid import UUID
from sqlalchemy import ForeignKey, LargeBinary, select
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from src.db.base import Base, BaseMixin


class UserRankDB(Base):
    __tablename__ = "user_ranks"

    id: Mapped[int] = mapped_column(primary_key=True)
    rocks_count: Mapped[int]
    title: Mapped[str]


class UserDB(BaseMixin, Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(primary_key=True)
    app_bundle: Mapped[str]
    name: Mapped[str]
    avatar: Mapped[bytes | None] = mapped_column(type_=LargeBinary, nullable=True)
    favorite_rock: Mapped[UUID | None]

    rock_detections: Mapped[list['RockDetectionDB']] = relationship(lazy="selectin", back_populates="user")

    @hybrid_property
    def successful_rock_detections(self):
        return [detection for detection in self.rock_detections if detection.status == "finished"]

    @successful_rock_detections.expression
    @classmethod
    def successful_rock_detections(cls):
        return select(cls.rock_detections).filter_by(status="finished")

