from uuid import UUID
from fastapi import Form
from pydantic import BaseModel

from src.rock.domain.entities import DetectionStatus


class RockDetectionReadDTO(BaseModel):
    id: UUID
    status: DetectionStatus
    rock_id: UUID | None = None


class RockDetectionCreateDTO(BaseModel):
    user_id: str
    app_bundle: str

    @classmethod
    def as_form(cls, user_id: str = Form(), app_bundle: str = Form()):
        return cls(
            user_id=user_id,
            app_bundle=app_bundle
        )
