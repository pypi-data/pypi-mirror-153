"""Configuration settings."""
from pathlib import Path

import platformdirs
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Top level settings."""

    meatball_database: Path = (
        Path(platformdirs.user_data_dir(__package__)) / "meatball.db"
    )


settings = Settings()
