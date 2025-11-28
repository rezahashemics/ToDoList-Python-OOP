import sys
from pathlib import Path
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# Make sure project root is on PYTHONPATH
sys.path.append(str(Path(__file__).resolve().parents[1]))

# Alembic Config object
config = context.config

# Logging
fileConfig(config.config_file_name)

# Import Base metadata
from app.db.base import Base
from app.models import project, task  # Ensure models are imported

target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
