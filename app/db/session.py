# app/db/session.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql+psycopg2://todolist:todolist@localhost:5432/todolist_db")
engine = create_engine(DATABASE_URL, future=True, echo=False)

# Use scoped_session for simple CLI/short-lived usage; in web apps you would handle sessions differently.
SessionLocal = scoped_session(sessionmaker(bind=engine, autoflush=False, expire_on_commit=False, future=True))
