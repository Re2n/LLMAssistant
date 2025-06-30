from functools import lru_cache
import os
from pathlib import Path

from pydantic_settings import BaseSettings
from dotenv import load_dotenv


env_path = Path(__file__).absolute().parent.parent.parent / ".env"
load_dotenv(env_path)


class EnvironmentSettings(BaseSettings):
    BOT_TOKEN: str = os.getenv("BOT_TOKEN")
    OLLAMA_URL: str = os.getenv("OLLAMA_URL")
    MODEL_NAME: str = os.getenv("MODEL_NAME")
    ADMIN_USER: str = os.getenv("ADMIN_USER")
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD")


@lru_cache
def get_environment_variables():
    return EnvironmentSettings()