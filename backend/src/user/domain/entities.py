from pydantic import BaseModel


class UserRank(BaseModel):
    rank_1 = "Lord of Stones"
    rank_2 = "Neophyte"


class User(BaseModel):
    external_id: str

