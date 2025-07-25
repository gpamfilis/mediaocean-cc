import logging
import os
import sys
from logging.config import fileConfig

from alembic import context
from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool

load_dotenv(override=True)

logger = logging.getLogger(__name__)

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
db_uri = os.environ.get("SQLALCHEMY_DATABASE_URI")
if not db_uri:
    raise Exception("SQLALCHEMY_DATABASE_URI not defined!")

logger.debug(f"SQLALCHEMY_DATABASE_URI: {db_uri}")
# Interpret the config file for Python logging.
# This line sets up loggers basically.

config.set_main_option("sqlalchemy.url", db_uri)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
try:
    from app.database.models import Base
except Exception:
    sys.path = ["", ".."] + sys.path[1:]
    from app.database.models import Base


target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
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

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
