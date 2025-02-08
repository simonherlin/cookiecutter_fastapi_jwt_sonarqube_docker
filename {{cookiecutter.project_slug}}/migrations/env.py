from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import importlib
import pkgutil

# Charger la configuration depuis alembic.ini
config = context.config
sqlalchemy_url = config.get_main_option("sqlalchemy.url")

# Configuration du logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Détection automatique des modèles SQLAlchemy
def import_submodules(package):
    """Importe automatiquement tous les sous-modules d'un package donné."""
    package_name = package.__name__
    return {
        name: importlib.import_module(package_name + "." + name)
        for _, name, _ in pkgutil.iter_modules(package.__path__)
    }

# Charger automatiquement tous les modèles de app.db.models
from app.db import models  # Assurez-vous que tous les modèles sont dans ce package
import_submodules(models)

# Récupérer target_metadata automatiquement
from app.db.base import Base
target_metadata = Base.metadata

# Fonction pour exécuter les migrations en mode offline
def run_migrations_offline():
    """Exécuter les migrations en mode offline."""
    context.configure(
        url=sqlalchemy_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

# Fonction pour exécuter les migrations en mode online
def run_migrations_online():
    """Exécuter les migrations en mode online."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

# Déterminer si on exécute en mode offline ou online
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
