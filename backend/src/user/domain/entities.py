from uuid import UUID
from pydantic import BaseModel


class UserRank(BaseModel):
    rank_1 = "Lord of Stones"
    rank_2 = "Neophyte"


class UserRockDetection(BaseModel):
    rock_id: UUID


class User(BaseModel):
    id: str
    avatar: bytes | None = None
    favorite_rock_id: UUID | None = None
    rock_detections: list[UserRockDetection]


class UserCreate(BaseModel):
    id: str
    app_bundle: str
    name: str


class UserUpdate(BaseModel):
    avatar: bytes | None = None
    favorite_rock_id: UUID | None = None

