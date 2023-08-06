"""Plugin configuration."""
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Plugin settings."""

    wordle_channels: list[str]


settings = Settings()
