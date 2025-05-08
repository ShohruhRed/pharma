# alembic/env.py

import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# --- подключаем корень проекта, чтобы импорты из app.db.database работали ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# читаем конфиг alembic.ini
config = context.config

# настраиваем логирование
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# импортируем ваши модели
from app.db.database import Base  # содержит metadata для всех моделей
from app.db.database import engine as app_engine  # SQLAlchemy Engine из вашего приложения

# указываем Alembic, откуда брать метаданные
target_metadata = Base.metadata

# Если в alembic.ini не прописан url, то подставляем ваш из приложения:
if not config.get_main_option("sqlalchemy.url"):
    config.set_main_option("sqlalchemy.url", str(app_engine.url))


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,  # чтобы замечать изменения типа колонок
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
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


# запускаем нужный режим
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
