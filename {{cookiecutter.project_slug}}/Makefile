# Variables de configuration
ENV_FILE=.env
REQUIREMENTS=requirements.txt
VENV=venv
PROJECT_NAME={{ cookiecutter.project_slug }}

.PHONY: help
help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  install         - Installe l'environnement et les dépendances."
	@echo "  start           - Initialise et lance les migrations."
	@echo "  check-all       - Exécute formatage, tests, linting et SonarQube."
	@echo "  tests           - Exécute les tests avec couverture."
	@echo "  run             - Démarre l'application FastAPI."
	@echo "  jupyterlab      - Lance JupyterLab."
	@echo "  sonar           - Analyse du code avec SonarQube."
	@echo "  format          - Formate le code avec Black."
	@echo "  lint            - Vérifie le code avec Flake8."
	@echo "  alembic-init    - Initialise Alembic."
	@echo "  alembic-migrate - Crée une migration."
	@echo "  alembic-upgrade - Applique les migrations."
	@echo "  alembic-downgrade - Annule la dernière migration."
	@echo "  alembic-reset   - Supprime et recrée la base de données."
	@echo "  docker-build    - Construit l'image Docker."
	@echo "  docker-run      - Lance le conteneur Docker."
	@echo "  clean           - Supprime les fichiers temporaires."


# ---------------------- INSTALLATION ----------------------

.PHONY: install
install: $(VENV)/bin/activate
$(VENV)/bin/activate: $(REQUIREMENTS)
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install --upgrade pip
	$(VENV)/bin/pip install -r $(REQUIREMENTS)
	@touch $(VENV)/bin/activate

# ---------------------- ALEMBIC COMMANDS ----------------------

.PHONY: alembic-init
alembic-init:
	$(VENV)/bin/alembic init migrations

.PHONY: alembic-migrate
alembic-migrate:
	@if [ -z "$(m)" ]; then \
		echo "⚠️  Erreur : Vous devez spécifier un message pour la migration (ex: make alembic-migrate m='ajout table user')"; \
		exit 1; \
	fi
	$(VENV)/bin/alembic revision --autogenerate -m "$(m)"

.PHONY: alembic-upgrade
alembic-upgrade:
	$(VENV)/bin/alembic upgrade head

.PHONY: alembic-downgrade
alembic-downgrade:
	$(VENV)/bin/alembic downgrade -1

.PHONY: alembic-history
alembic-history:
	$(VENV)/bin/alembic history

.PHONY: alembic-reset
alembic-reset:
	rm -f app/db.sqlite3
	$(VENV)/bin/alembic upgrade head
	@echo "✅ Base de données réinitialisée avec succès !"


# ---------------------- ENV.PY MANAGEMENT ----------------------

.PHONY: change-env
change-env: 
	@if [ -f "temp/env.py" ]; then \
		echo "🔄 Copie du fichier env.py personnalisé..."; \
		cp temp/env.py migrations/env.py; \
		rm -rf temp; \
		echo "✅ env.py mis à jour."; \
	else \
		echo "⚠️  Fichier temp/env.py introuvable !"; \
	fi

# ---------------------- START SETUP ----------------------

.PHONY: start
start: install alembic-init update-env alembic-migrate alembic-upgrade
	@echo "🚀 Projet prêt à l'emploi !"

# ---------------------- TESTS & VERIFICATIONS ----------------------

.PHONY: format
format: $(VENV)/bin/activate
	$(VENV)/bin/black app/

.PHONY: tests
tests: $(VENV)/bin/activate
	$(VENV)/bin/pytest --maxfail=1 --disable-warnings -q \
		--cov=app --cov-report=term-missing --cov-report=html \
		--cov-report=xml:results/coverage.xml tests/ \
		--junitxml=results/pytest-results.xml

.PHONY: lint
lint: $(VENV)/bin/activate
	$(VENV)/bin/flake8 app/ tests/ --format=json > results/flake8-report.json

.PHONY: sonar
sonar:
	docker run --rm --network=host \
	  -e SONAR_HOST_URL={{ cookiecutter.sonarqube_server_url }} \
	  -v "$(shell pwd)":/usr/src \
	  sonarsource/sonar-scanner-cli \
	  -Dsonar.projectKey={{ cookiecutter.sonarqube_project_key }} \
	  -Dsonar.token={{ cookiecutter.sonarqube_token }} \
	  -Dsonar.python.coverage.reportPaths=results/coverage.xml \
	  -Dsonar.python.xunit.reportPath=results/pytest-results.xml \
	  -Dsonar.python.flake8.reportPaths=results/flake8-report.json

.PHONY: check-all
check-all: format tests lint sonar
	@echo "✅ Tous les tests et vérifications sont passés avec succès !"


# ---------------------- APPLICATION COMMANDS ----------------------

.PHONY: run
run: $(VENV)/bin/activate
	$(VENV)/bin/uvicorn app.main:app --host 0.0.0.0 --port $(if $(PORT),$(PORT),8000) --reload

.PHONY: jupyterlab
jupyterlab: $(VENV)/bin/activate
	$(VENV)/bin/jupyter lab

.PHONY: stop-jupyterlab
stop-jupyterlab:
	@echo "Arrêt de JupyterLab..."
	@pkill -f "jupyter-lab"


# ---------------------- DOCKER COMMANDS ----------------------

.PHONY: docker-build
docker-build:
	docker build -t $(PROJECT_NAME) .

.PHONY: docker-run
docker-run:
	docker run -d --name $(PROJECT_NAME) -p 80:80 $(PROJECT_NAME)

# ---------------------- CLEANUP ----------------------

.PHONY: clean
clean:
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -exec rm -f {} +
	find . -type f -name "*.pyo" -exec rm -f {} +
	rm -rf results




.PHONY: update-env
update-env:
	@echo "🔄 Mise à jour de migrations/env.py..."
	@cat > migrations/env.py <<EOF
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
from app.db import models
import_submodules(models)

# Récupérer target_metadata automatiquement
from app.db.base import Base
target_metadata = Base.metadata

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

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
EOF
	@echo "✅ env.py mis à jour avec succès !"
