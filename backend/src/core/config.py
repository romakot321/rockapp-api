from pydantic import AnyUrl, PostgresDsn, ValidationInfo, field_validator
from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    REDIS_HOST: str = "redis"

    ELASTICSEARCH_HOST: str = "elasticsearch"
    ELASTICSEARCH_USER: str = "elastic"
    ELASTICSEARCH_PASSWORD: str = "password"

    DB_NAME: str
    DB_USER: str | None
    DB_PASSWORD: str | None
    DB_HOST: str | None
    DB_PORT: str | None
    DATABASE_URI: str | None = None
    ALEMBIC_DATABASE_URI: str | None = None

    @staticmethod
    def _build_dsn(scheme: str, values: dict) -> str:
        return str(
            PostgresDsn.build(
                scheme=scheme,
                username=values.get("DB_USER"),
                password=values.get("DB_PASSWORD"),
                host=values.get("DB_HOST"),
                port=int(values["DB_PORT"]) if values.get("DB_PORT") else None,
                path=values.get("DB_NAME"),
            )
        )

    @field_validator("DATABASE_URI")
    def assemble_db_connection(cls, v: str | None, info: ValidationInfo) -> str:
        if isinstance(v, str):
            return v
        elif isinstance(v, AnyUrl):
            return str(v)
        return cls._build_dsn("postgresql+asyncpg", info.data)

    @field_validator("ALEMBIC_DATABASE_URI", mode="before")
    def assemble_alembic_connection(cls, v: str | None, info: ValidationInfo) -> str:
        if isinstance(v, str):
            return v
        elif isinstance(v, AnyUrl):
            return str(v)
        elif info.data.get("DATABASE_URI"):
            return info.data.get("DATABASE_URI")
        raise ValueError("Invalid alembic database uri")


settings = Settings()
