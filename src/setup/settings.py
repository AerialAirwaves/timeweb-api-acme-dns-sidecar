from typing import List

from pydantic.networks import AnyHttpUrl
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    """
    Base configuration.
    """

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    DEBUG: bool = False
    LOGGING_LEVEL: str = "INFO"

    DOCS_ENABLED: bool = True

    DB_PATH: str = "/data/db.json"

    TIMEWEB_API_TOKEN: str
    MANAGED_DOMAIN: str

    UPDATE_USERNAME: str
    UPDATE_PASSWORD: str


def get_settings() -> AppSettings:
    return AppSettings(_env_file=".env", _env_file_encoding="utf-8")
