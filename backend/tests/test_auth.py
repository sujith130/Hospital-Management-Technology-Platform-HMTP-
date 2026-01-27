import pytest
from httpx import AsyncClient
from app.core import config

@pytest.mark.anyio
async def test_register_user(client: AsyncClient):
    response = await client.post(
        f"{config.settings.API_V1_STR}/auth/register",
        json={
            "email": "test@hospital.com",
            "password": "password123",
            "full_name": "Test User",
            "role": "admin",
            "hospital_id": "HOSP1"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@hospital.com"
    assert data["hospital_id"] == "HOSP1"

@pytest.mark.anyio
async def test_login_user(client: AsyncClient):
    # First, register the user
    await client.post(
        f"{config.settings.API_V1_STR}/auth/register",
        json={
            "email": "login@hospital.com",
            "password": "password123",
            "full_name": "Login User",
            "role": "admin",
            "hospital_id": "HOSP1"
        }
    )
    
    # Then login
    response = await client.post(
        f"{config.settings.API_V1_STR}/auth/login",
        data={
            "username": "login@hospital.com",
            "password": "password123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
