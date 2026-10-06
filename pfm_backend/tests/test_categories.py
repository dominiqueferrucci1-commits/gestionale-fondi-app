def test_categorie_crud(client, auth_headers):
    # Create
    created = client.post(
        "/categories",
        json={"name": "Trasporti", "type": "expense"},
        headers=auth_headers,
    )
    assert created.status_code == 201
    category_id = created.json()["id"]

    # Read
    listed = client.get("/categories", headers=auth_headers)
    assert listed.status_code == 200
    names = [c["name"] for c in listed.json()]
    assert "Trasporti" in names

    single = client.get(f"/categories/{category_id}", headers=auth_headers)
    assert single.status_code == 200
    assert single.json()["type"] == "expense"

    # Update
    updated = client.put(
        f"/categories/{category_id}",
        json={"name": "Trasporti (agg.)", "type": "expense"},
        headers=auth_headers,
    )
    assert updated.status_code == 200
    assert updated.json()["name"] == "Trasporti (agg.)"

    # Delete
    deleted = client.delete(f"/categories/{category_id}", headers=auth_headers)
    assert deleted.status_code == 204
    assert (
        client.get(f"/categories/{category_id}", headers=auth_headers).status_code
        == 404
    )


def test_categorie_richiedono_auth(client):
    assert client.get("/categories").status_code == 401
    assert (
        client.post("/categories", json={"name": "x", "type": "expense"}).status_code
        == 401
    )


def test_categoria_tipo_non_valido(client, auth_headers):
    response = client.post(
        "/categories",
        json={"name": "Cattivo", "type": "invalido"},
        headers=auth_headers,
    )
    assert response.status_code == 422
