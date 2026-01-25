# scripts/init_db.py

from db.db import engine, Base
import db.models

def main():
    Base.metadata.create_all(engine)
    print("Database created successfully")


if __name__ == "__main__":
    main()
