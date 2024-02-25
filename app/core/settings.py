from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIR.joinpath(".env"))

    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PREFIX: str

    @property
    def db_url(self) -> str:
        return f"mongodb://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?authSource=admin"  # noqa


settings = Settings()
