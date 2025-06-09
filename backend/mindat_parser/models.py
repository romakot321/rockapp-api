from typing import Literal
from pydantic import BaseModel, Field, field_validator
from uuid import UUID, uuid4


class Rock(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    image_url: str | None = None
    name: str
    price: int = 0
    rarity: int = Field(gt=0, description="В усл. единицах", default=1)
    danger: str = ""
    type: str = ""
    locations: list[str] = []
    crystal_system: str = Field(description="физ. Кристаллическая система камня(строение атомов)", validation_alias="crystal system", default="")
    hardness: str = ""
    fracture: str = ""
    streak: str = ""
    magnetism: str = ""
    colors: str = Field(validation_alias="colour", default="")
    luster: str = Field(description="Блеск", validation_alias="lustre", default="")
    transparency: str = ""
    chemical_formula: str = Field(validation_alias="formula", default="")
    chemical_group: str = ""
    description: str = ""
    history: str = ""
    synonyms: list[str] = []
    parent: str | None = Field(default=None)

    @field_validator("parent", mode="before")
    @classmethod
    def only_one_parent(cls, value: str | None, _info) -> str | None:
        if not value:
            return None
        return value.split(",")[0]
