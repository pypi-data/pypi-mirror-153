"""Configuration settings."""
from pathlib import Path

import platformdirs
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Top level settings."""

    meatball_database: Path = platformdirs.user_data_path("casper7") / "meatball.db"


settings = Settings()
