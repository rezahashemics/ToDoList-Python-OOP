from src.db.session import SessionLocal
from typing import Generator
from sqlalchemy.orm import Session

def get_db() -> Generator[Session, None, None]:
    """
    Dependency function that yields a database session.
    It automatically closes the session after the request is processed.
    """
    db = SessionLocal()
    try:
        # Yield the session to the route handler
        yield db
    finally:
        # Ensure the session is closed, even if errors occur
        db.close()
