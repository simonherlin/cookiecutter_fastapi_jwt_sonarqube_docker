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
	@echo "  tests           - Exécute les tests avec couverture."
	@echo "  run             - Démarre l'application FastAPI."
	@echo "  jupyterlab      - Lance JupyterLab."
	@echo "  stop-jupyterlab - Arrête JupyterLab."
	@echo "  sonar           - Analyse du code avec SonarQube."
	@echo "  format          - Formate le code avec Black."
	@echo "  lint            - Vérifie le code avec Flake8."
	@echo "  alembic-init    - Initialise Alembic."
	@echo "  alembic-migrate - Crée une migration (ex: make alembic-migrate m='Message')."
	@echo "  alembic-upgrade - Applique les migrations."
	@echo "  alembic-downgrade - Annule la dernière migration."
	@echo "  alembic-history - Affiche l'historique des migrations."
	@echo "  alembic-reset   - Supprime et recrée toute la base de données."
	@echo "  docker-build    - Construit l'image Docker."
	@echo "  docker-run      - Lance le conteneur Docker."
	@echo "  clean           - Supprime les fichiers temporaires."

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

# ---------------------- APPLICATION COMMANDS ----------------------

.PHONY: tests
tests: $(VENV)/bin/activate
	$(VENV)/bin/pytest --maxfail=1 --disable-warnings -q \
		--cov=app --cov-report=term-missing --cov-report=html \
		--cov-report=xml:results/coverage.xml tests/ \
		--junitxml=results/pytest-results.xml


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

.PHONY: format
format: $(VENV)/bin/activate
	$(VENV)/bin/black app/

.PHONY: lint
lint: $(VENV)/bin/activate
	$(VENV)/bin/flake8 app/ tests/ --format=json > results/flake8-report.json

# ---------------------- DOCKER COMMANDS ----------------------

.PHONY: docker-build
docker-build:
	docker build -t $(PROJECT_NAME) .

.PHONY: docker-run
docker-run:
	docker run -d --name $(PROJECT_NAME) -p 80:80 $(PROJECT_NAME)

.PHONY: clean
clean:
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -exec rm -f {} +
	find . -type f -name "*.pyo" -exec rm -f {} +
	rm -rf results
