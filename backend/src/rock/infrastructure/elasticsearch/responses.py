from typing import Any
from pydantic import BaseModel, ConfigDict, Field


{'took': 8, 'timed_out': False, 'hits': {'total': {'value': 1, 'relation': 'eq'}, 'max_score': 3.0839214, 'hits': [{'_index': 'rocks', '_id': '3a4f8429-3516-442b-ac05-dbfda57a20c9', '_score': 3.0839214, '_source': {'id': '3a4f8429-3516-442b-ac05-dbfda57a20c9', 'name': 'Amethyst', 'price': '214-1229 USD/kg', 'rarity': 1, 'danger': 'Generally safe, handle with care', 'type': 'Oxide', 'locations': ['Australia'], 'crystal_system': 'hexagonal', 'hardness': 4.87, 'fracture': 'Uneven', 'streak': 'White', 'magnetism': 'Magnetic', 'colors': 'Various', 'luster': 'Resinous', 'transparency': 'Transparent', 'chemical_formula': 'Varies', 'chemical_group': 'Halides', 'description': 'Amethyst is a well-known mineral valued for its beauty and industrial applications.', 'history': 'Amethyst has been known since ancient times and used in various cultures.'}}]}}



class ElasticsearchResponse(BaseModel):
    class Hits(BaseModel):
        class Total(BaseModel):
            value: int
            relation: str

        class Hit(BaseModel):
            index: str = Field(validation_alias="_index")
            id: str = Field(validation_alias="_id")
            score: float = Field(validation_alias="_score")
            source: object = Field(validation_alias="_source")

        total: Total
        hits: list[Hit]
        max_score: float

    hits: Hits
    took: int
    timed_out: bool

    model_config = ConfigDict(from_attributes=True)
