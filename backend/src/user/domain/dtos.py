from pydantic import BaseModel
from uuid import UUID

from src.user.domain.entities import UserRank


class UserReadDTO(BaseModel):
    id: UUID
    rank: UserRank
    rocks_count: int
    rocks_total_cost: int
    favorite_rock_id: UUID | None = None
