def test_register_restituisce_utente(client):
    response = client.post(
        "/auth/register",
        json={"email": "nuovo@example.com", "password": "password-sicura-123"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "nuovo@example.com"
    assert "hashed_password" not in body
    assert "password" not in str(body)


def test_register_email_doppia(client):
    payload = {"email": "doppia@example.com", "password": "password-sicura-123"}
    assert client.post("/auth/register", json=payload).status_code == 201
    assert client.post("/auth/register", json=payload).status_code == 400


def test_register_password_corta(client):
    response = client.post(
        "/auth/register", json={"email": "corta@example.com", "password": "abc"}
    )
    assert response.status_code == 422


def test_login_e_me(client):
    email = "login@example.com"
    password = "password-sicura-123"
    client.post("/auth/register", json={"email": email, "password": password})

    response = client.post(
        "/auth/login", data={"username": email, "password": password}
    )
    assert response.status_code == 200
    tokens = response.json()
    assert tokens["token_type"] == "bearer"
    assert "access_token" in tokens and "refresh_token" in tokens

    me = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {tokens['access_token']}"},
    )
    assert me.status_code == 200
    assert me.json()["email"] == email


def test_login_password_sbagliata(client):
    email = "sbagliata@example.com"
    client.post("/auth/register", json={"email": email, "password": "password-sicura-123"})
    response = client.post(
        "/auth/login", data={"username": email, "password": "non-questa-123"}
    )
    assert response.status_code == 401


def test_me_senza_token(client):
    assert client.get("/auth/me").status_code == 401


def test_refresh_token(client):
    email = "refresh@example.com"
    password = "password-sicura-123"
    client.post("/auth/register", json={"email": email, "password": password})
    tokens = client.post(
        "/auth/login", data={"username": email, "password": password}
    ).json()

    refreshed = client.post(
        "/auth/refresh", json={"refresh_token": tokens["refresh_token"]}
    )
    assert refreshed.status_code == 200
    assert "access_token" in refreshed.json()

    # Un access token non e' un refresh token
    invalid = client.post(
        "/auth/refresh", json={"refresh_token": tokens["access_token"]}
    )
    assert invalid.status_code == 401
