from typing import Literal
from pydantic import BaseModel, Field, field_validator
from uuid import UUID, uuid4


{
  "formula": "Ni(C31H32N4)",
  "colour": "Pink-purple, dark greyish purple, pale purplish red, reddish brown",
  "lustre": "Adamantine, Sub-Metallic",
  "hardness": "2 - 3 on Mohs scale",
  "specific gravity": "1.33 - 1.48",
  "crystal system": "Triclinic",
  "name": "For American physicist Philip Hauge Abelson (27 April 1913, Tacoma, Washington, USA - 1 August 2004, Bethesda, Maryland, USA). He was co-discoverer of element 93 (neptunium), editor of the periodical Science (1962-1984), and director of the Carnegie Institution of Washington's Geophysical Laboratory (1953-1971).",
  "type locality": "\u24d8 WOSCO Well, Uintah County, Utah, USA",
  "transparency": "Translucent",
  "streak": "Pink",
  "cleavage": "Poor/IndistinctProbable on {111}.",
  "density": "1.33 - 1.48 g/cm3 (Measured) \u00a0\u00a0\u00a01.45 g/cm3 (Calculated)",
  "description": "Chemically a nickel porphyrine derivative, classified as deoxophylloerythroetioporphyrin. Unique combination of elements; the only organonickel mineral known. Formed at depth (Milton et al., 1978), likely from a chlorophyll (but likely not the chlorophyll-d) (Storm et al., 1984).\n\nAbelsonite is accompanied by its structural norisomer; the surrounding shale contains other Ni porphyrins, which represent a series of more extended homologues.\n\nStructure details (Storm et al., 1984): (1) methyl groups in the 2, 3, 7, 12, and 18 positions, (2) ethyl group in the 8 and 17 positions. According to Milton et al.(1978) the molecules in abelsonite are not planar. The substitution pattern in the mineral is genetically related to a typical chlorophyll. The potential precursor to abelsonite is 17-desethyl, 17-propionic acid.\n\nWorth of notice is an unnamed mineral coded as 'UM1984-14-CH:ClNOV', which is a natural vanadyl deoxophylloerythroetioporphyrin, the second known metalloporphyrin mineral, although not isostructural with abelsonite.",
  "locations": [
    "USA"
  ]
}



class Rock(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    price: str = ""
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
    parent: str | None = Field(validation_alias="synonym of", default=None)

    @field_validator("parent", mode="before")
    @classmethod
    def only_one_parent(cls, value: str | None, _info) -> str | None:
        if not value:
            return None
        return value.split(",")[0]
