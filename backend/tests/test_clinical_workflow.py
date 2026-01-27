import pytest
from httpx import AsyncClient
from app.core import config
from datetime import datetime, timedelta

@pytest.mark.anyio
async def test_end_to_end_clinical_workflow(client: AsyncClient):
    # 1. Setup Tenant A
    hospital_a = "HOSP_A"
    user_a_email = "admin@hosp-a.com"
    reg_a = await client.post(
        f"{config.settings.API_V1_STR}/auth/register",
        json={"email": user_a_email, "password": "password", "full_name": "Admin A", "role": "admin", "hospital_id": hospital_a}
    )
    assert reg_a.status_code == 200, f"Registration A failed: {reg_a.text}"
    
    login_a = await client.post(
        f"{config.settings.API_V1_STR}/auth/login",
        data={"username": user_a_email, "password": "password"}
    )
    assert login_a.status_code == 200, f"Login A failed: {login_a.text}"
    token_a = login_a.json()["access_token"]
    headers_a = {"Authorization": f"Bearer {token_a}"}

    # 2. Setup Tenant B (for isolation check)
    hospital_b = "HOSP_B"
    user_b_email = "admin@hosp-b.com"
    await client.post(
        f"{config.settings.API_V1_STR}/auth/register",
        json={"email": user_b_email, "password": "password", "full_name": "Admin B", "role": "admin", "hospital_id": hospital_b}
    )
    login_b = await client.post(
        f"{config.settings.API_V1_STR}/auth/login",
        data={"username": user_b_email, "password": "password"}
    )
    token_b = login_b.json()["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}

    # 3. Create Patient in Tenant A
    patient_res = await client.post(
        f"{config.settings.API_V1_STR}/patients/",
        json={"first_name": "John", "last_name": "Doe", "gender": "Male", "date_of_birth": "1990-01-01"},
        headers=headers_a
    )
    assert patient_res.status_code == 200
    patient_id = patient_res.json()["id"]

    # 4. Verify isolation: Tenant B cannot see Patient A
    list_patients_b = await client.get(f"{config.settings.API_V1_STR}/patients/", headers=headers_b)
    assert len(list_patients_b.json()) == 0

    # 5. Create Doctor and Availability in Tenant A
    doctor_res = await client.post(
        f"{config.settings.API_V1_STR}/doctors/",
        json={"full_name": "Dr. Smith", "specialization": "Cardiology"},
        headers=headers_a
    )
    assert doctor_res.status_code == 200
    doctor_id = doctor_res.json()["id"]

    # Set availability: Monday (0), 09:00 - 17:00
    avail_res = await client.post(
        f"{config.settings.API_V1_STR}/doctors/{doctor_id}/availability",
        json={"day_of_week": 0, "start_time": "09:00:00", "end_time": "17:00:00"},
        headers=headers_a
    )
    assert avail_res.status_code == 200

    # 6. Book Appointment (valid time)
    # Next Monday
    today = datetime.now()
    next_monday = today + timedelta(days=(7 - today.weekday()) % 7)
    appt_time = next_monday.replace(hour=10, minute=0, second=0, microsecond=0)
    
    appt_res = await client.post(
        f"{config.settings.API_V1_STR}/appointments/",
        json={
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_datetime": appt_time.isoformat(),
            "reason": "Checkup"
        },
        headers=headers_a
    )
    assert appt_res.status_code == 200
    appt_id = appt_res.json()["id"]

    # 7. Verify conflict: Double booking
    conflict_res = await client.post(
        f"{config.settings.API_V1_STR}/appointments/",
        json={
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_datetime": appt_time.isoformat(),
            "reason": "Duplicate"
        },
        headers=headers_a
    )
    assert conflict_res.status_code == 400
    assert "conflicting appointment" in conflict_res.json()["detail"]

    # 8. Pharmacy Flow
    # Create Medicine
    med_res = await client.post(
        f"{config.settings.API_V1_STR}/pharmacy/medicines/",
        json={"name": "Paracetamol", "quantity": 100, "unit_price": 5.0, "expiry_date": "2026-12-31"},
        headers=headers_a
    )
    assert med_res.status_code == 200
    medicine_id = med_res.json()["id"]

    # Create Prescription
    presc_res = await client.post(
        f"{config.settings.API_V1_STR}/pharmacy/prescriptions/",
        json={
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "medicine_id": medicine_id,
            "dosage": "500mg",
            "frequency": "Twice daily",
            "duration": "5 days"
        },
        headers=headers_a
    )
    assert presc_res.status_code == 200
    prescription_id = presc_res.json()["id"]

    # Dispense Medicine
    disp_res = await client.post(
        f"{config.settings.API_V1_STR}/pharmacy/dispense/",
        json={"prescription_id": prescription_id, "quantity": 10},
        headers=headers_a
    )
    assert disp_res.status_code == 200
    assert disp_res.json()["remaining_stock"] == 90

    # 9. Billing Flow
    invoice_res = await client.post(
        f"{config.settings.API_V1_STR}/billing/invoices/",
        json={"patient_id": patient_id, "appointment_id": appt_id, "total_amount": 100.0, "final_amount": 110.0, "tax_amount": 10.0},
        headers=headers_a
    )
    assert invoice_res.status_code == 200
    invoice_id = invoice_res.json()["id"]

    # Create Payment
    pay_res = await client.post(
        f"{config.settings.API_V1_STR}/billing/payments/",
        json={"invoice_id": invoice_id, "amount": 110.0, "payment_method": "Cash"},
        headers=headers_a
    )
    assert pay_res.status_code == 200

    # Verify Invoice status updated
    invoice_after_pay = await client.get(f"{config.settings.API_V1_STR}/billing/invoices/patient/{patient_id}", headers=headers_a)
    assert invoice_after_pay.json()[0]["status"] == "paid"

    # 10. Verify Audit logs
    audit_res = await client.get(f"{config.settings.API_V1_STR}/audit/", headers=headers_a)
    # The audit list might be long, check if something exists
    assert len(audit_res.json()) > 0
