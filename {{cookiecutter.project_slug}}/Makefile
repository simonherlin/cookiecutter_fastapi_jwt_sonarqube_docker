# Variables de configuration
ENV_FILE=.env
REQUIREMENTS=requirements.txt
VENV=venv
PROJECT_NAME={{ cookiecutter.project_name }}

.PHONY: help
help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  install         - Crée un environnement virtuel et installe les dépendances."
	@echo "  tests           - Exécute les tests avec génération de rapports de couverture."
	@echo "  run             - Lance l'application principale."
	@echo "  jupyterlab      - Lance JupyterLab."
	@echo "  stop-jupyterlab - Arrête JupyterLab."
	@echo "  sonar           - Exécute SonarQube pour analyser le code (si configuré)."
	@echo "  format          - Formate le code avec Black."
	@echo "  lint            - Vérifie le code avec Flake8."
	@echo "  build           - Construit le package (utilisez docker-build pour l'image Docker)."
	@echo "  docker-build    - Construit l'image Docker."
	@echo "  docker-run      - Lance l'image Docker."
	@echo "  clean           - Supprime l'environnement virtuel et les fichiers temporaires."

.PHONY: install
install: $(VENV)/bin/activate

$(VENV)/bin/activate: $(REQUIREMENTS)
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install --upgrade pip
	$(VENV)/bin/pip install -r $(REQUIREMENTS)
	@touch $(VENV)/bin/activate

.PHONY: tests
tests: $(VENV)/bin/activate
	$(VENV)/bin/pytest --maxfail=1 --disable-warnings -q \
		--cov={{ cookiecutter.project_slug }} --cov-report=term-missing --cov-report=html tests/ --junitxml=results/pytest-results.xml

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

{% if cookiecutter.use_sonarqube == "yes" %}
.PHONY: sonar
sonar:
	docker run --rm --network=host \
	  -e SONAR_HOST_URL={{ cookiecutter.sonarqube_server_url }} \
	  -v "$(shell pwd)":/usr/src \
	  sonarsource/sonar-scanner-cli \
	  -Dsonar.projectKey={{ cookiecutter.sonarqube_project_key }} \
	  -Dsonar.token={{ cookiecutter.sonarqube_token }}
{% else %}
.PHONY: sonar
sonar:
	@echo "SonarQube n'est pas configuré pour ce projet."
{% endif %}

.PHONY: format
format: $(VENV)/bin/activate
	$(VENV)/bin/black .

.PHONY: lint
lint: $(VENV)/bin/activate
	$(VENV)/bin/flake8 {{ cookiecutter.project_slug }} tests/ > results/flake8-report.txt

.PHONY: build
build: $(VENV)/bin/activate
	@echo "Construction du package non implémentée. Utilisez 'docker-build' pour construire l'image Docker."

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
