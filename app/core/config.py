from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Application
    app_name: str = "Backlog Stats API"
    debug: bool = False

    # Database
    database_url: str = "sqlite:///./backlogstats.db"

    # IGDB API
    igdb_client_id: str = ""
    igdb_client_secret: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()
