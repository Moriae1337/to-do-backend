from pydantic import Field
from .base_config import BaseAppSettings
from .db_settings import DatabaseSettings


class Settings(BaseAppSettings):
    # CORS
    allowed_origins: list[str] = Field(
        default=["http://localhost:5173"],
        description="List of allowed origins for CORS",
    )
    # App config
    debug: bool = Field(default=True, description="Enable debug mode")
    app_version: str = Field(default="1.0.0", description="Application version")

    # Compose databases
    db: DatabaseSettings = Field(default_factory=DatabaseSettings)


settings = Settings()
