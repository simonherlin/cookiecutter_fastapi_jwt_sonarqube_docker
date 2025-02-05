# Utilise une image Python minimaliste
FROM python:{{ cookiecutter.python_version }}-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier de dépendances et l'installer
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copier l'ensemble du projet dans le conteneur
COPY . .

# Exposer le port utilisé par l'application
EXPOSE 80

# Lancer l'application avec Uvicorn
CMD ["uvicorn", "{{ cookiecutter.project_slug }}.app.main:app", "--host", "0.0.0.0", "--port", "80"]
