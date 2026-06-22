from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "users-service"
    app_env: str = "local"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    postgres_db: str = "users_service"
    postgres_user: str = "users_service_user"
    postgres_password: str = "users_service_password"
    postgres_host: str = "db"
    postgres_port: int = 5432
    database_url: str = Field(
        default=(
            "postgresql+asyncpg://"
            "users_service_user:users_service_password@db:5432/users_service"
        )
    )
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
