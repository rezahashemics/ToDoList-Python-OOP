from logging.config import fileConfig
import sys
import os

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# --- بخش وارد کردن ماژول‌های پروژه ---

# Add project root to path to import our modules
# This is necessary so Alembic can find src.db and src.core.models
sys.path.insert(0, os.path.realpath('.'))

# Import the Base and engine from your db setup
from src.db import engine, Base
# Import your models file to ensure Base knows about them (all models inherit from Base)
from src.core import models 

# --- تنظیمات Alembic ---

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# target_metadata is where Base.metadata is set.
# We set it to the Base.metadata imported from src.db
target_metadata = Base.metadata


# --- تعریف توابع Migrations ---

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine.
    """
    # Note: For offline mode to work, sqlalchemy.url must be set in alembic.ini,
    # or you must manually provide the full URL here (e.g., from .env file)
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    We use the pre-configured 'engine' from src.db which handles 
    reading the credentials from the .env file.
    """
    # We use the 'engine' imported from src.db
    connectable = engine 

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


# --- اجرای Migrations ---

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
