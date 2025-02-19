import pytest
from fastapi.testclient import TestClient
from ..app.main import read_root


@pytest.fixture(scope="module")
def client():
    with TestClient(read_root) as c:
        yield c
