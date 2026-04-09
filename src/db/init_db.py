# src/db/init_db.py
from .connection import Base, engine
from . import models   # ensures models are loaded

def init_db():
    """
    Initialize database schema.
    Creates all tables defined in models.py if they don't exist.
    """
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()


