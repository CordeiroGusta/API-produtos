from fastapi.testclient import TestClient
from app.main import app

def teste_test(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == "Ola, mundo!"



