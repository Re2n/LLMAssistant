from functools import lru_cache
import os
from pathlib import Path

from pydantic_settings import BaseSettings
from dotenv import load_dotenv


env_path = Path(__file__).absolute().parent.parent.parent / ".env"
load_dotenv(env_path)


class EnvironmentSettings(BaseSettings):
    BOT_TOKEN: str = os.getenv("BOT_TOKEN")

@lru_cache
def get_environment_variables():
    return EnvironmentSettings()
