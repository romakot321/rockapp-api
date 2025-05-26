from pydantic import BaseModel
from uuid import UUID

from src.user.domain.entities import UserRank


class UserReadDTO(BaseModel):
    id: str
    rank: UserRank
    rocks_count: int
    rocks_total_cost: int
    favorite_rock_id: UUID | None = None


class UserReadShortDTO(BaseModel):
    id: str


class UserCreateDTO(BaseModel):
    id: str
    app_bundle: str
    name: str


class UserRockDTO(BaseModel):
    id: UUID
    name: str
    image_url: str | None = None


class UserUpdateDTO(BaseModel):
    name: str | None = None
    favorite_rock_id: UUID | None = None
