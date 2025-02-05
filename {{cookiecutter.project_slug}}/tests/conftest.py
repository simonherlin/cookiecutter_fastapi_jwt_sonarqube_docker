import pytest
from fastapi.testclient import TestClient
from {{ cookiecutter.project_slug }}.app.main import app

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c
