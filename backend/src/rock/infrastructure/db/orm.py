from uuid import UUID
from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db.base import Base, BaseMixin


class RockDetectionDB(BaseMixin, Base):
    __tablename__ = "rock_detections"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    app_bundle: Mapped[str]

    status: Mapped[str]
    detector_result: Mapped[str | None]
    rock_id: Mapped[UUID | None]
    details: Mapped[str | None]

    user: Mapped['UserDB'] = relationship(lazy="noload", back_populates="rock_detections")

