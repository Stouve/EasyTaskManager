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
