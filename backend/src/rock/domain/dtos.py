from uuid import UUID
from fastapi import Form
from pydantic import BaseModel, Field

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


class RockStoreDTO(BaseModel):
    id: UUID
    image_url: str | None = None
    name: str
    price: int
    rarity: int = Field(gt=0, description="В усл. единицах")
    danger: str
    type: str
    locations: list[str]
    crystal_system: str = Field(description="физ. Кристаллическая система камня(строение атомов)")
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
    synonyms: list[str]
    parent: str | None = None

