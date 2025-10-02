import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from app.core.config import settings
from sqlalchemy.ext.asyncio import create_async_engine
from app.db.base import Base
from app.models.task import Task
from alembic import context

config = context.config
fileConfig(config.config_file_name)


target_metadata = Base.metadata


def run_migrations_offline():
    context.configure(
        url=settings.db.url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    connectable = create_async_engine(
        settings.db.url,
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:

        def do_run_migrations(sync_conn):
            context.configure(
                connection=sync_conn,
                target_metadata=target_metadata,
                compare_type=True,
            )
            with context.begin_transaction():
                context.run_migrations()

        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
