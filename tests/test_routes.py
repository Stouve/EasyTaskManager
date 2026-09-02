import pytest


async def test_register_via_api_creates_user(client):

    # Arrange : Data we send via POST body request through dict, httpx auto convert into JSON

    payload = {
        "email": "api-test@example.com",
        "password": "strongpassword123",
    }

    # Act : real request HTTP POST to /auth/register.
    # "client" is async fixture which call FastAPI app in memory via ASGITransport
    response = await client.post("/auth/register", json=payload)

    # Assert : Check complete HTTP answer
    assert response.status_code == 201  # status code defined in auth_router.py(HTTP_201_CREATED)

    data = response.json() # parse body anwser JSON into dict

    assert data["email"] == payload["email"]
    assert data["role"] == "user"
    assert data["is_active"] is True
    assert "id" in data

    #Never check that pwd or hashed pwd is on response, UserOut schema doesn't have pwd field to avoid sensitive data leak

async def test_login_returns_access_token(client):

    # Arrange : We need existing user from DB to login so we create it via true HTTP request no via authservice

    register_payload = {
        "email": "login-test@example.com",
        "password": "strongpassword123",
    }

    # Act : login with same ids
    await client.post("/auth/register", json=register_payload)

    login_payload = {
        "email": "login-test@example.com",
        "password": "strongpassword123",
    }

    response = await client.post("/auth/login", json=login_payload)

    #No explicit status_code, so we check 200 by default for a POST request
    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"
    #Check header.payload.signature : 3 separate parts separated by dots
    assert data["access_token"].count(".") == 2

async def test_create_task_with_valid_token(client,auth_headers):

    #Arrange
    task_payload = {
        "title":"test",
        "description":"test",
    }

    response=await client.post("/tasks/", json=task_payload, headers=auth_headers)

    assert response.status_code == 200

    data = response.json()
    assert data["title"] == task_payload["title"]
    assert data["description"] == task_payload["description"]
    assert data["status"] == "pending"
    assert "id" in data
    assert "created_at" in data