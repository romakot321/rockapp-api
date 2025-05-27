from io import BytesIO
import base64

from loguru import logger
from pydantic import ValidationError
from backend.src.detector.domain.exceptions import DetectionError
from backend.src.detector.infrastructure.openai.responses import OpenAIDetectionResponse
from src.detector.application.interfaces.client import (
    IDetectorClient,
    TAdditional,
    TResult,
)
from openai import AsyncOpenAI


class OpenAIDetector[TResult: str, TAdditional: str | None](
    IDetectorClient
):
    def __init__(self) -> None:
        self.client = AsyncOpenAI()

    async def execute(
        self, image_content: bytes, additional_data: str | None
    ) -> str:
        image_buffer = BytesIO(image_content)
        image_buffer.name = "tmp.png"
        response = await self.client.responses.create(
            model="gpt-4o",
            input=[
                self._make_system_input(),
                self._make_user_input(image_content, additional_data),
            ],
            text=self._make_output_format(),
            temperature=0.7,
            max_output_tokens=2048,
            top_p=1,
            store=True,
        )
        if not response.choices:
            raise DetectionError("Fail to execute OpenAI detector: Empty response")
        try:
            result = OpenAIDetectionResponse.model_validate_json(
                response.choices[0].message.content
            )
        except ValidationError as e:
            logger.exception(e)
            raise DetectionError("Fail to execute OpenAI detector: Unexpected response")
        return result.model_dump_json()

    @staticmethod
    def _make_system_input() -> dict:
        return {
            "role": "system",
            "content": [
                {
                    "type": "input_text",
                    "text": "You are a geology expert. Describe the stone in the photograph using your internet knowledge. The identification should be as accurate as possible and adhere to the response schema.",
                }
            ],
        }

    @staticmethod
    def _make_user_input(image_content: bytes, additional_data: str | None) -> dict:
        user_input = {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "data:image/jpeg;base64,"
                        + base64.b64encode(image_content).decode()
                    },
                }
            ],
        }
        if additional_data is not None:
            user_input["content"].append({"type": "text", "text": additional_data})
        return user_input

    @staticmethod
    def _make_output_format() -> dict:
        return {
            "format": {
                "type": "json_schema",
                "name": "rock",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Name of the rock.",
                        },
                        "price": {
                            "type": "number",
                            "description": "Average price of the rock in USD for 1 kilogram.",
                        },
                        "rarity": {
                            "type": "number",
                            "description": "Rarity of the rock in arbitrary units, must be greater than 0.",
                        },
                        "danger": {
                            "type": "string",
                            "description": "Danger level associated with the rock.",
                        },
                        "type": {
                            "type": "string",
                            "description": "Type or classification of the rock.",
                        },
                        "locations": {
                            "type": "array",
                            "description": "List of locations where the rock can be found.",
                            "items": {"type": "string"},
                        },
                        "crystal_system": {
                            "type": "string",
                            "description": "Physical crystalline system of the rock, detailing atomic structure.",
                        },
                        "hardness": {
                            "type": "string",
                            "description": "Hardness of the rock.",
                        },
                        "fracture": {
                            "type": "string",
                            "description": "Type of fracture when the rock breaks into two or more pieces.",
                        },
                        "streak": {
                            "type": "string",
                            "description": "Color of the rock in powdered form.",
                        },
                        "magnetism": {
                            "type": "string",
                            "description": "Magnetic properties of the rock.",
                        },
                        "colors": {
                            "type": "string",
                            "description": "Colors of the rock.",
                        },
                        "luster": {
                            "type": "string",
                            "description": "Luster quality of the rock.",
                        },
                        "transparency": {
                            "type": "string",
                            "description": "Transparency level of the rock.",
                        },
                        "chemical_formula": {
                            "type": "string",
                            "description": "Chemical formula of the rock.",
                        },
                        "chemical_group": {
                            "type": "string",
                            "description": "Chemical group classification of the rock.",
                        },
                        "description": {
                            "type": "string",
                            "description": "Detailed description of the rock.",
                        },
                        "history": {
                            "type": "string",
                            "description": "History and significance of the rock.",
                        },
                    },
                    "required": [
                        "name",
                        "price",
                        "rarity",
                        "danger",
                        "type",
                        "locations",
                        "crystal_system",
                        "hardness",
                        "fracture",
                        "streak",
                        "magnetism",
                        "colors",
                        "luster",
                        "transparency",
                        "chemical_formula",
                        "chemical_group",
                        "description",
                        "history",
                    ],
                    "additionalProperties": False,
                },
            }
        }
