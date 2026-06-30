from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "order-service"
    app_env: str = "local"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    database_url: str = Field(
        default="postgresql+asyncpg://postgres:postgres@postgres:5432/orders_db"
    )
    billing_service_url: str = "http://billing-service:8000"
    kafka_bootstrap_servers: str = "kafka:9092"
    order_payment_result_topic: str = "order.payment.result"
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
