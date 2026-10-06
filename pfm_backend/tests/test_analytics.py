def _registra_e_login(client, email):
    client.post("/auth/register", json={"email": email, "password": "password-sicura-123"})
    tokens = client.post(
        "/auth/login", data={"username": email, "password": "password-sicura-123"}
    ).json()
    return {"Authorization": f"Bearer {tokens['access_token']}"}


def test_riepilogo_mensile(client):
    headers = _registra_e_login(client, "analytics@example.com")

    income_cat = client.post(
        "/categories", json={"name": "Stipendio", "type": "income"}, headers=headers
    ).json()
    expense_cat = client.post(
        "/categories", json={"name": "Affitto", "type": "expense"}, headers=headers
    ).json()

    client.post(
        "/transactions",
        json={"amount": 3000, "category_id": income_cat["id"]},
        headers=headers,
    )
    client.post(
        "/transactions",
        json={"amount": 1000, "category_id": expense_cat["id"]},
        headers=headers,
    )

    summary = client.get("/analytics/monthly", headers=headers)
    assert summary.status_code == 200
    body = summary.json()
    assert body["total_income"] == 3000
    assert body["total_expenses"] == 1000
    assert body["net_balance"] == 2000
    assert body["savings_rate"] == 66.67

    by_category = client.get("/analytics/by-category", headers=headers)
    assert by_category.status_code == 200
    rows = {r["category_name"]: r["total"] for r in by_category.json()}
    assert rows == {"Affitto": 1000}


def test_raccomandazione_strategia(client):
    headers = _registra_e_login(client, "strategia@example.com")

    income_cat = client.post(
        "/categories", json={"name": "Entrate", "type": "income"}, headers=headers
    ).json()
    expense_cat = client.post(
        "/categories", json={"name": "Uscite", "type": "expense"}, headers=headers
    ).json()
    client.post(
        "/transactions",
        json={"amount": 2000, "category_id": income_cat["id"]},
        headers=headers,
    )
    client.post(
        "/transactions",
        json={"amount": 1800, "category_id": expense_cat["id"]},
        headers=headers,
    )

    response = client.get("/strategies/recommendation", headers=headers)
    assert response.status_code == 200
    body = response.json()
    assert body["net_balance"] == 200
    assert isinstance(body["status"], str) and body["status"]
    assert isinstance(body["recommendations"], list)


def test_analytics_richiedono_auth(client):
    assert client.get("/analytics/monthly").status_code == 401
    assert client.get("/strategies/recommendation").status_code == 401
