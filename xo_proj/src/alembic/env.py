from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# Импортируем настройки и Base
from datasource.sql.config import settings
from datasource.sql.model import Base  # таким образом импортируем всю нашу модель, т.к. она наследуется от Base

config = context.config

# Берём URL из Settings — теперь всё читается из .env
config.set_main_option('sqlalchemy.url', settings.DATABASE_URL_psycopg)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, compare_type=True
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
