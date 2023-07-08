import httpx
import pytest
from tests.base import app, client


@pytest.mark.asyncio
async def test_successful_auth(client):
    body = {
        "username": "932.767.650-55",
        "password": "password123",
        'grant_type': 'password',
    }
    response = client.post("/token", data=body)
    access_token = response.json()['access_token']
    headers = {'authorization': f'Bearer {access_token}'}
    response = client.get("/me", headers=headers)
    assert response.status_code == 200
    assert "cpf" in response.json()
    assert "email" in response.json()
    assert "name" in response.json()
    assert "uuid" in response.json()
