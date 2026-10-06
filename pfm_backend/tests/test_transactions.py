def test_transazioni_crud(client, auth_headers, seed_categories):
    category_id = seed_categories["expense"]["id"]

    created = client.post(
        "/transactions",
        json={"amount": 42.50, "category_id": category_id, "description": "Spesa"},
        headers=auth_headers,
    )
    assert created.status_code == 201
    transaction_id = created.json()["id"]
    assert created.json()["amount"] == 42.5

    listed = client.get("/transactions", headers=auth_headers)
    assert listed.status_code == 200
    assert any(t["id"] == transaction_id for t in listed.json())

    updated = client.put(
        f"/transactions/{transaction_id}",
        json={"amount": 50.0, "category_id": category_id, "description": "Agg."},
        headers=auth_headers,
    )
    assert updated.status_code == 200
    assert updated.json()["amount"] == 50.0

    assert (
        client.delete(f"/transactions/{transaction_id}", headers=auth_headers).status_code
        == 204
    )


def test_transazione_importo_non_positivo(client, auth_headers, seed_categories):
    response = client.post(
        "/transactions",
        json={"amount": -5, "category_id": seed_categories["expense"]["id"]},
        headers=auth_headers,
    )
    assert response.status_code == 422


def test_transazione_categoria_altrui(client, auth_headers):
    # Categoria inesistente/non appartenente all'utente
    response = client.post(
        "/transactions",
        json={"amount": 10, "category_id": 999999},
        headers=auth_headers,
    )
    assert response.status_code == 400


def test_transazioni_richiedono_auth(client, seed_categories):
    response = client.post(
        "/transactions",
        json={"amount": 10, "category_id": seed_categories["expense"]["id"]},
    )
    assert response.status_code == 401
