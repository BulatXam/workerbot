""" Сборка переменных окружения из dotenv """

from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str
    DB_URL: str
    OWNER_IDS: List[int]

    class Config:
        case_sensitive = True
        env_file = "env.env"


settings = Settings()
