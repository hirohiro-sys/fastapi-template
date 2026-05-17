from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "fastapi-guide-tutorial"
    app_env: str = "development"
    app_debug: bool = True

    database_url: str = "sqlite:///./app.db"

    api_v1_prefix: str = "/api/v1"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    # lru_cache でプロセス内シングルトン化し、.env の再読込コストを避ける
    return Settings()


settings = get_settings()
