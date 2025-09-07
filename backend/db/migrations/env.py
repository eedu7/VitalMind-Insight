import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine

from core.config import settings
from db.models import Base

# Alembic Config object
config = context.config

# Load logging config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Database Url
DATABASE_URL = settings.DATABASE_URL

# Metadata for autogenerate
target_metadata = Base.metadata


def run_migration_offline() -> None:
    """Run migrations in 'offline' mode (no DB Connection)."""
    url = DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Helper for running migrations with a connection"""
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode (with DB connection)."""
    connectable = create_async_engine(DATABASE_URL, poolclass=pool.NullPool, future=True)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migration_offline()
else:
    asyncio.run(run_migrations_online())
