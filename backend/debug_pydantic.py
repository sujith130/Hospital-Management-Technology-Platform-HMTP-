from app.auth import schemas

data = {
    "email": "admin@hosp-a.com",
    "password": "password",
    "full_name": "Admin A",
    "role": "admin",
    "hospital_id": "HOSP_A"
}

try:
    user_in = schemas.UserCreate(**data)
    print("Validation successful")
    print(user_in.model_dump())
except Exception as e:
    print(f"Validation failed: {e}")
