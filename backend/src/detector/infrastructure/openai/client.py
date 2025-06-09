import json
from loguru import logger
from openai import AsyncOpenAI
from pydantic import ValidationError

from src.detector.domain.exceptions import DetectionError
from src.detector.infrastructure.openai.responses import OpenAIRockFillResponse


class OpenAIClient:
    def __init__(self) -> None:
        self.client = AsyncOpenAI()

    async def fill_rock_data(self, rock_data: dict) -> str:
        response = await self.client.chat.completions.create(
            model="gpt-4.1",
            messages=[self._make_fill_rock_system_message(), self._make_fill_rock_user_message(rock_data)],
            temperature=0.7,
            max_output_tokens=2048,
            top_p=1,
            store=True,
        )
        return self._validate_fill_rock_response(response)

    def _validate_fill_rock_response(self, response) -> str:
        if not response.output or not response.output[0].content:
            raise DetectionError("Fail to execute OpenAI detector: Empty response")
        try:
            result = OpenAIRockFillResponse.model_validate_json(
                response.output[0].content[0].text
            )
        except ValidationError as e:
            logger.exception(e)
            raise DetectionError("Fail to execute OpenAI detector: Unexpected response")
        return result.model_dump_json()

    @staticmethod
    def _make_fill_rock_system_message() -> dict:
        return {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": "Help user to fill missing data in rock data.\nData json schema: {id: UUID, image_url: str | None, name: str, price: int, rarity: int, danger: str, type: str, locations: list[str], crystal_system: str, hardness: str, fracture: str, streak: str, magnetism: str, colors: str, luster: str, transparency: str, chemical_formula: str, chemical_group: str, description: str, history: str, synonyms: list[str] parent: str}. Answer with provided data json schema.\nIf field is already filled, then do not modify it.\nIf price=0, then suggest price(in USD) of rock and replace in data.\nIf rarity=1, then suggest rarity(from 1 to 5) and replace in data.\nLocations is list of countries, where rock appears.\nDo not add nor synonyms or parent in data.\nParent is other name of rock.\nDescription is general description of rock in 2-3 sentences.\nHistory is history of rock in 5-6 sentences with fun-facts.",
                }
            ],
        }

    @staticmethod
    def _make_fill_rock_user_message(rock_data: dict) -> dict:
        return {
            "role": "user",
            "content": [{"type": "text", "text": json.dumps(rock_data)}],
        }
