# scripts/init_db.py

from app.db.db import engine, Base
import app.db.schema

def main():
    Base.metadata.create_all(engine)
    print(f"Database created successfully: {engine.url}")


if __name__ == "__main__":
    main()
