import os
import pathlib

# Ambiente di test: deve essere impostato PRIMA di importare l'applicazione,
# perche' app.database legge DATABASE_URL al momento dell'import.
TEST_DB = pathlib.Path(__file__).resolve().parent / "test_pfm.db"
if TEST_DB.exists():
    TEST_DB.unlink()
os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB.as_posix()}"
os.environ["SECRET_KEY"] = "test-secret-key-sicura"

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as test_client:
        yield test_client
    # Rilascia le connessioni del pool prima di eliminare il file DB (Windows).
    from app.database import engine

    engine.dispose()
    if TEST_DB.exists():
        TEST_DB.unlink()


@pytest.fixture()
def auth_headers(client):
    """Registra un utente di prova e restituisce gli header Authorization."""
    email = "tester@example.com"
    password = "password-sicura-123"
    client.post("/auth/register", json={"email": email, "password": password})
    response = client.post(
        "/auth/login", data={"username": email, "password": password}
    )
    assert response.status_code == 200, response.text
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def seed_categories(client, auth_headers):
    """Crea una categoria di spesa e una di entrate per l'utente di prova."""
    expense = client.post(
        "/categories",
        json={"name": "Alimentari", "type": "expense"},
        headers=auth_headers,
    )
    income = client.post(
        "/categories",
        json={"name": "Stipendio", "type": "income"},
        headers=auth_headers,
    )
    assert expense.status_code == 201
    assert income.status_code == 201
    return {"expense": expense.json(), "income": income.json()}
