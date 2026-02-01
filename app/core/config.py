import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pathlib import Path

load_dotenv()


class Config(BaseSettings):
    app_name: str = "pitch_prophet"
    db_name: str = os.getenv("DATABASE_NAME")

    @property
    def db_url(self):
        base_dir = Path(__file__).resolve().parents[2]
        db_path = base_dir / self.db_name
        return f"sqlite:///{db_path}"

config = Config()

