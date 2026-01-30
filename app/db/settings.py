# DB Settings

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]  # .../football_predictor
DB_PATH = BASE_DIR / ".nostradamus.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"