# scripts/init_db.py
import logging

from app.db.db import engine, Base
import app.db.schema

def init_db():
    Base.metadata.create_all(engine)
    logging.info(f"Database created successfully: {engine.url}")


if __name__ == "__main__":
    init_db()
