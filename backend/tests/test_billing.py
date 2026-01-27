import pytest
from httpx import AsyncClient
from app.core import config

@pytest.fixture
async def auth_headers(client: AsyncClient):
    # Register and login a user to get headers
    await client.post(
        f"{config.settings.API_V1_STR}/auth/register",
        json={
            "email": "doctor@hospital.com",
            "password": "password123",
            "full_name": "Dr. Test",
            "role": "doctor",
            "hospital_id": "HOSP1"
        }
    )
    response = await client.post(
        f"{config.settings.API_V1_STR}/auth/login",
        data={
            "username": "doctor@hospital.com",
            "password": "password123"
        }
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.mark.anyio
async def test_create_medicine_and_billing(client: AsyncClient, auth_headers: dict):
    # Create a medicine
    medicine_resp = await client.post(
        f"{config.settings.API_V1_STR}/pharmacy/medicines/",
        json={
            "name": "Paracetamol",
            "manufacturer": "HealthCorp",
            "batch_number": "B123",
            "expiry_date": "2026-12-31",
            "quantity": 100,
            "unit_price": 5.0,
            "hospital_id": "HOSP1"
        },
        headers=auth_headers
    )
    assert medicine_resp.status_code == 200
    
    # Create an invoice (simulation)
    invoice_resp = await client.post(
        f"{config.settings.API_V1_STR}/billing/invoices/",
        json={
            "patient_id": 1,
            "total_amount": 50.0,
            "final_amount": 50.0,
            "hospital_id": "HOSP1"
        },
        headers=auth_headers
    )
    assert invoice_resp.status_code == 200
    invoice_id = invoice_resp.json()["id"]
    
    # Record a payment
    payment_resp = await client.post(
        f"{config.settings.API_V1_STR}/billing/payments/",
        json={
            "invoice_id": invoice_id,
            "amount": 50.0,
            "payment_method": "Cash",
            "hospital_id": "HOSP1"
        },
        headers=auth_headers
    )
    assert payment_resp.status_code == 200
    
    # Verify invoice is paid
    get_invoice_resp = await client.get(
        f"{config.settings.API_V1_STR}/billing/invoices/patient/1",
        headers=auth_headers
    )
    assert get_invoice_resp.status_code == 200
    assert get_invoice_resp.json()[0]["status"] == "paid"
