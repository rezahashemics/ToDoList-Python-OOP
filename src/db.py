from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# 1. Load environment variables from .env file
load_dotenv()

# 2. Get credentials
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# 3. Construct the DATABASE_URL (Connection String)
if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
    raise ValueError("Database environment variables are not fully set in .env")

# Note: Using 'psycopg2' as the DBAPI for PostgreSQL
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 4. Create the SQLAlchemy Engine
# The 'pool_pre_ping' checks if the connection is still alive before using it
engine = create_engine(
    DATABASE_URL, pool_pre_ping=True
)

# 5. Configure SessionLocal for creating a new session
# autoflush=False means changes are not automatically written to DB after each operation
# autocommit=False is the default for transactional sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 6. Base class for our models (used by SQLAlchemy)
# Models will inherit from 'Base'
Base = declarative_base()

# 7. Dependency for getting a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
