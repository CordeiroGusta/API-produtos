from fastapi.testclient import TestClient #bibioteca de testes automatizados para essa API
from app.main import app #Importando a instância do FastAPI

def teste_test(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == "Ola, mundo!"



