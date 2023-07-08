import httpx
import pytest
from tests.base import app, client


@pytest.mark.asyncio
async def test_successful_sign_up(client):
    body = {
        "cpf": "932.767.650-55",
        "email": "test@example.com",
        "name": "John Doe",
        "password": "password123",
    }
    response =client.post("/sign-up", json=body)
    assert response.status_code == 201
    assert "cpf" in response.json()
    assert response.json()["cpf"] == "".join(filter(str.isdigit, body["cpf"]))
    assert response.json()["email"] == body["email"]
    assert response.json()["name"] == body["name"]


@pytest.mark.asyncio
async def test_sign_up_with_unavailable_cpf(client):
    body = {
        "cpf": "932.767.650-55",
        "email": "test@example.com",
        "name": "John Doe",
        "password": "password123",
    }
    with pytest.raises(ValueError) as exc_info:
       client.post("/sign-up", json=body)
    assert str(exc_info.value) == "CPF indisponível"


@pytest.mark.asyncio
async def test_sign_up_with_unavailable_email(client):
    body = {
        "cpf": "682.593.530-59",
        "email": "test@example.com",
        "name": "John Doe",
        "password": "password123",
    }
    with pytest.raises(ValueError) as exc_info:
       client.post("/sign-up", json=body)
    assert str(exc_info.value) == "Email indisponível"


@pytest.mark.asyncio
async def test_successful_sign_in(client):
    body = {
        "username": "932.767.650-55",
        "password": "password123",
        'grant_type': 'password',
    }
    response = client.post("/token", data=body)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "token_type" in response.json()


@pytest.mark.asyncio
async def test_unsuccessful_sign_in(client):
    body = {
        "username": "682.593.530-59",
        "password": "password123",
        'grant_type': 'password',
    }
    response = client.post("/token", data=body)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_unsuccessful_auth(client):
    invalid_access_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyODA1MTQ2MDAwNiIsImV4cCI6MTY4NzcyNzY2N30.0R52qXmleo-CgjB4jSYclnyiZoLPx1F-ohDl2H-unkY'
    headers = {'authorization': f'Bearer {invalid_access_token}'}
    response = client.get("/users/me", headers=headers)
    assert response.status_code == 404
