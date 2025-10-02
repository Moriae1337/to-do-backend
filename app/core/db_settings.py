from pydantic import Field
from .base_config import BaseAppSettings


class DatabaseSettings(BaseAppSettings):
    user: str = Field("postgres", alias="POSTGRES_USER")
    password: str = Field("postgres", alias="POSTGRES_PASSWORD")
    db: str = Field("tododb", alias="POSTGRES_DB")
    host: str = Field("db", alias="POSTGRES_HOST")
    port: int = Field(5432, alias="POSTGRES_PORT")

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"
