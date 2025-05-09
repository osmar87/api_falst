from fastapi.testclient import TestClient

from api_falst.app import app


def test_root_deve_retonar_ola_mundo():
    cliente = TestClient(app)

    response = cliente.get("/")

    assert response.json() == {"msg": "Ola Mundo!!!"}
