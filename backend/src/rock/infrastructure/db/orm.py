from uuid import UUID
from sqlalchemy.orm import Mapped
from src.db.base import Base, BaseMixin


class RockDetectionDB(BaseMixin, Base):
    __tablename__ = "rock_detections"

    user_id: Mapped[str]
    app_bundle: Mapped[str]

    status: Mapped[str]
    detector_result: Mapped[str | None]
    rock_id: Mapped[UUID | None]
    details: Mapped[str | None]
