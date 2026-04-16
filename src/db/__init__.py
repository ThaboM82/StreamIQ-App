# src/db/__init__.py
# Makes db a package and exposes key imports

# src/db/init_db.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.db.connection import Base
from src.db import models

# Path to your SQLite database file
DATABASE_URL = "sqlite:///backend/streamiq.db"

# Create engine with SQLite
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # needed for SQLite in multithreaded apps
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """
    Initialize all database tables defined in models.py.
    This will create tables if they don't exist yet.
    """
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized: tables created if missing.")

if __name__ == "__main__":
    # Run directly to initialize DB
    init_db()
