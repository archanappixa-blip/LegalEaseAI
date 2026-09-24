from fastapi.testclient import (
    TestClient
)

from backend.main import app


client = TestClient(
    app
)


def test_root():

    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "running"


def test_health():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"


def test_invalid_generation_request():

    response = client.post(

        "/generate",

        json={

            "document_type": "",

            "parties": "",

            "terms": "",

            "effective_date": ""
        }
    )

    assert response.status_code == 422