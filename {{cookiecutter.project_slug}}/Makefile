ENV_FILE=.env
REQUIREMENTS=requirements.txt
VENV=venv
PROJECT_NAME={{ cookiecutter.project_slug }}

# ---------------------- COMMANDES D'AIDE ----------------------

.PHONY: help
help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "📌 Commandes disponibles :"
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
	@echo "📦 Installation de l'environnement virtuel et des dépendances..."
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install --upgrade pip
	$(VENV)/bin/pip install -r $(REQUIREMENTS)
	@touch $(VENV)/bin/activate
	@echo "✅ Installation terminée !"

# ---------------------- ALEMBIC COMMANDS ----------------------

.PHONY: alembic-init
alembic-init:
	@echo "🔧 Initialisation d'Alembic..."
	$(VENV)/bin/alembic init migrations
	@echo "✅ Alembic initialisé avec succès."

.PHONY: alembic-migrate
alembic-migrate:
	@if [ -z "$(m)" ]; then \
		echo "⚠️  Erreur : Vous devez spécifier un message pour la migration (ex: make alembic-migrate m='ajout table user')"; \
		exit 1; \
	fi
	@echo "📌 Création d'une migration avec le message : $(m)"
	$(VENV)/bin/alembic revision --autogenerate -m "$(m)"
	@echo "✅ Migration créée avec succès."

.PHONY: alembic-upgrade
alembic-upgrade:
	@echo "🚀 Application des migrations..."
	$(VENV)/bin/alembic upgrade head
	@echo "✅ Migrations appliquées avec succès."

.PHONY: alembic-downgrade
alembic-downgrade:
	@echo "🔄 Annulation de la dernière migration..."
	$(VENV)/bin/alembic downgrade -1
	@echo "✅ Migration annulée avec succès."

.PHONY: alembic-reset
alembic-reset:
	@echo "⚠️  Réinitialisation complète de la base de données..."
	rm -f app/db.sqlite3
	$(VENV)/bin/alembic upgrade head
	@echo "✅ Base de données réinitialisée avec succès !"

# ---------------------- GESTION DU FICHIER ENV.PY ----------------------

.PHONY: change-env
change-env: 
	@echo "🔄 Remplacement du fichier env.py personnalisé..."
	@if [ -f "temp/env.py" ]; then \
		cp temp/env.py migrations/env.py; \
		rm -rf temp; \
		echo "✅ env.py mis à jour."; \
	else \
		echo "⚠️  Fichier temp/env.py introuvable !"; \
	fi

# ---------------------- INITIALISATION COMPLÈTE ----------------------

.PHONY: start
start: install alembic-init change-env
	@echo "🚀 Initialisation de la base de données..."
	@make alembic-migrate m="Initial migration"
	@make alembic-upgrade
	@echo "✅ Projet prêt à l'emploi !"

# ---------------------- TESTS & ANALYSE DU CODE ----------------------

.PHONY: format
format: $(VENV)/bin/activate
	@echo "🎨 Formatage du code avec Black..."
	$(VENV)/bin/black app/
	@echo "✅ Formatage terminé."

.PHONY: tests
tests: $(VENV)/bin/activate
	@echo "🧪 Exécution des tests avec Pytest..."
	$(VENV)/bin/pytest --maxfail=1 --disable-warnings -q \
		--cov=app --cov-report=term-missing --cov-report=html \
		--cov-report=xml:results/coverage.xml tests/ \
		--junitxml=results/pytest-results.xml
	@echo "✅ Tests terminés."

.PHONY: lint
lint: $(VENV)/bin/activate
	@echo "🔍 Vérification du code avec Flake8..."
	$(VENV)/bin/flake8 app/ tests/ --format=json > results/flake8-report.json
	@echo "✅ Vérification terminée."

.PHONY: sonar
sonar:
	@echo "📡 Analyse du code avec SonarQube..."
	docker run --rm --network=host \
	  -e SONAR_HOST_URL={{ cookiecutter.sonarqube_server_url }} \
	  -v "$(shell pwd)":/usr/src \
	  sonarsource/sonar-scanner-cli \
	  -Dsonar.projectKey={{ cookiecutter.sonarqube_project_key }} \
	  -Dsonar.token={{ cookiecutter.sonarqube_token }} \
	  -Dsonar.python.coverage.reportPaths=results/coverage.xml \
	  -Dsonar.python.xunit.reportPath=results/pytest-results.xml \
	  -Dsonar.python.flake8.reportPaths=results/flake8-report.json
	@echo "✅ Analyse SonarQube terminée."

.PHONY: check-all
check-all: format tests lint sonar
	@echo "✅ Tous les tests et vérifications sont passés avec succès !"

# ---------------------- CELERY COMMANDS ----------------------

.PHONY: celery-worker
celery-worker:
	@echo "🚀 Lancement du worker Celery..."
	$(VENV)/bin/celery -A app.celery_worker.celery_app worker --loglevel=info

.PHONY: celery-flower
celery-flower:
	@echo "📊 Lancement de Flower pour le monitoring des tâches..."
	$(VENV)/bin/celery -A app.celery_worker.celery_app flower

.PHONY: redis-start
redis-start:
	@echo "🚀 Démarrage de Redis..."
	docker start redis || docker run -d --name redis -p 6379:6379 redis

.PHONY: redis-stop
redis-stop:
	@echo "🛑 Arrêt de Redis..."
	docker stop redis

# ---------------------- APPLICATION COMMANDS ----------------------

.PHONY: run
run:
	@echo "🚀 Vérification et démarrage des services nécessaires..."
	@make redis-start
	@echo "🚀 Lancement du worker Celery..."
	@tmux new-session -d -s celery_worker '$(VENV)/bin/celery -A app.celery_worker.celery_app worker --loglevel=info'
	@echo "🚀 Lancement de FastAPI..."
	@$(VENV)/bin/uvicorn app.main:app --host 0.0.0.0 --port $(if $(PORT),$(PORT),8000) --reload


.PHONY: jupyterlab
jupyterlab: $(VENV)/bin/activate
	@echo "📖 Démarrage de JupyterLab..."
	$(VENV)/bin/jupyter lab
	@echo "✅ JupyterLab lancé."

# ---------------------- GESTION DE DOCKER ----------------------

.PHONY: docker-build
docker-build:
	@echo "🐳 Construction de l'image Docker..."
	docker build -t $(PROJECT_NAME) .
	@echo "✅ Image Docker construite."

.PHONY: docker-run
docker-run:
	@echo "🚀 Lancement du conteneur Docker..."
	docker run -d --name $(PROJECT_NAME) -p 80:80 $(PROJECT_NAME)
	@echo "✅ Conteneur lancé."

# ---------------------- GESTION DE FLOWER ----------------------

.PHONY: celery-flower
celery-flower:
	@echo "📊 Lancement de Flower pour le monitoring des tâches..."
	docker run -d --name flower -p 5555:5555 --network="host" mher/flower --broker=redis://localhost:6379/0

.PHONY: celery-flower-stop
celery-flower-stop:
	@echo "🛑 Arrêt de Flower..."
	docker stop flower && docker rm flower


# ---------------------- NETTOYAGE ----------------------

.PHONY: clean
clean:
	@echo "🧹 Nettoyage des fichiers temporaires..."
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -exec rm -f {} +
	find . -type f -name "*.pyo" -exec rm -f {} +
	rm -rf results
	@echo "✅ Nettoyage terminé."
