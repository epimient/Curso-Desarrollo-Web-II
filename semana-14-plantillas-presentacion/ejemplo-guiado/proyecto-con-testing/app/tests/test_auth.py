def test_register_success(client, test_user_data):
    response = client.post("/users/register", json=test_user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == test_user_data["username"]
    assert data["email"] == test_user_data["email"]
    assert data["role"] == "student"
    assert data["active"] is True
    assert "id" in data


def test_register_duplicate_username(client, test_user_data):
    client.post("/users/register", json=test_user_data)
    response = client.post("/users/register", json=test_user_data)
    assert response.status_code == 400
    assert response.json()["mensaje"] == "Username or email already exists"


def test_register_duplicate_email(client, test_user_data):
    client.post("/users/register", json=test_user_data)
    duplicate = {"username": "otro", "email": test_user_data["email"], "password": "123456"}
    response = client.post("/users/register", json=duplicate)
    assert response.status_code == 400


def test_login_success(client, test_user_data):
    client.post("/users/register", json=test_user_data)
    response = client.post("/token", data={
        "username": test_user_data["username"],
        "password": test_user_data["password"],
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, test_user_data):
    client.post("/users/register", json=test_user_data)
    response = client.post("/token", data={
        "username": test_user_data["username"],
        "password": "wrongpass",
    })
    assert response.status_code == 401
    assert response.json()["mensaje"] == "Incorrect username or password"


def test_users_me_without_token(client):
    response = client.get("/users/me")
    assert response.status_code == 401


def test_users_me_with_token(client, test_user_data, token):
    response = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == test_user_data["username"]
    assert data["email"] == test_user_data["email"]
