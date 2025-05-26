from enum import Enum
import string
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, Field


class DetectionStatus(str, Enum):
    queued = 'queued'
    finished = 'finished'
    started = 'started'
    failed = 'failed'


class Detection(BaseModel):
    id: UUID
    status: DetectionStatus
    details: str | None = None
    detector_result: str | None = None
    rock_id: UUID | None = None


class DetectionCreate(BaseModel):
    user_id: str
    app_bundle: str


class DetectionUpdate(BaseModel):
    status: DetectionStatus | None = None
    detector_result: str | None = None
    rock_id: UUID | None = None
    details: str | None = None


class Rock(BaseModel):
    id: UUID
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

