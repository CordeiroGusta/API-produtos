import pytest
from fastapi.testclient import TestClient
from app.repositories_local import items_repositories
from app.main import app

@pytest.fixture
def client():
    items_repositories._items.clear()
    items_repositories._next_id = 1

    with TestClient(app) as test_client:
        yield test_client

    items_repositories._items.clear()
    items_repositories._next_id = 1