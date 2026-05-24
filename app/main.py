from fastapi import FastAPI

from app.api import player
from app.core.config import config
from app.core.logging import setup_logging
from scripts.init_db import init_db

app = FastAPI(title=config.app_name)

app.include_router(player.router)

def main():
    # init_db()
    setup_logging()

if __name__ == "__main__":
    main()

