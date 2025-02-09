# FastAPI Project with SonarQube, Pytest, Flake8, and Alembic

## Overview

This project is a FastAPI application with the following features:

- Database migrations with Alembic
- Unit tests with Pytest
- Code formatting with Black
- Linting with Flake8
- Static code analysis with SonarQube
- Task automation using Makefile
- Docker support for containerized deployment

## 📁 Project Structure

```bash
my_fastapi_project/
│── app/
│   ├── api/
│   │   ├── endpoints/
│   │   │   ├── auth.py
│   │   │   ├── user.py
│   │   ├── router.py
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   ├── db/
│   │   ├── base.py
│   │   ├── database.py
│   │   ├── session.py
│   │   ├── models/
│   │   │   ├── user.py
│   ├── schemas/
│   │   ├── user.py
│   ├── main.py
│── tests/
│   ├── test_main.py
│   ├── conftest.py
│── temp/
│── Makefile
│── alembic.ini
│── pytest.ini
│── requirements.txt
│── .flake8
│── sonar-project.properties
│── README.md

```

## 🔥 Quick Start

```bash
make start
```

## 🗄 Database Setup with Alembic

Initialize Alembic
```bash
make alembic-init
```

Generate a new migration
```bash
make alembic-revision m="Initial migration"
```

Apply migrations
```bash
make alembic-upgrade
```

## 🌍 Run the FastAPI Server
By default, the application runs on http://localhost:8000
```bash
make run
```

To run on a specific port, use:
```bash
make run PORT=8085
```

## ✅ Run Tests & Linting

Run unit tests with coverage
```bash
make tests
```

Run Flake8 for linting
```bash
make lint
```

Run code formatting with Black
```bash
make format
```

Run all checks (formatting, linting, tests, and SonarQube analysis)
```bash
make check-all
```

## 📊 SonarQube Integration

SonarQube is used for static code analysis.

Run SonarQube Analysis
```bash
make sonar
```

## 🐳 Docker Support

Build the Docker image
```bash
make docker-build
```

Run the Docker container
```bash
make docker-run
```

## 🔄 Switching from SQLite to PostgreSQL

Modify the database URL in app/db/database.py:
```python
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost:5432/mydatabase"
```

Modify alembic.ini:
```python
sqlalchemy.url = postgresql://user:password@localhost:5432/mydatabase
```

Apply the migrations to PostgreSQL:
```bash
make alembic-upgrade
```

## 🧹 Clean up the project

To remove all temporary files, virtual environments, and caches:

```bash
make clean
```