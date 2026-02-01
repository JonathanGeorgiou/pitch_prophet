from app.core.logging import setup_logging
from scripts.init_db import init_db


def main():
    init_db()
    setup_logging()

if __name__ == "__main__":
    main()

