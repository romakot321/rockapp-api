from uuid import UUID
from pydantic import BaseModel, Field


class OpenAIDetectionResponse(BaseModel):
    name: str
    price: int
    rarity: int = Field(gt=0, description="В усл. единицах")
    danger: str
    type: str
    locations: list[str]
    crystal_system: str = Field(
        description="физ. Кристаллическая система камня(строение атомов)"
    )
    hardness: str = Field(description="Твердость камня")
    fracture: str = Field(description="Вид разделения камня на 2 или более частей")
    streak: str = Field(description="Цвет в порошковом состоянии")
    magnetism: str = Field(description="Магнетические свойства камня")
    colors: str
    luster: str = Field(description="Блеск")
    transparency: str = Field(description="Прозрачность")
    chemical_formula: str
    chemical_group: str
    description: str
    history: str


class OpenAIRockFillResponse(BaseModel):
    id: UUID
    image_url: str | None = None
    name: str
    price: int
    rarity: int
    danger: str
    type: str
    locations: list[str]
    crystal_system: str
    hardness: str
    fracture: str
    streak: str
    magnetism: str
    colors: str
    luster: str
    transparency: str
    chemical_formula: str
    chemical_group: str
    description: str
    history: str
    synonyms: list[str]
    parent: str
