# Quick Start: Patient Login Testing

## ✅ Backend Server is Running!

Your backend server is now running at: **http://127.0.0.1:8000**

## 🔐 Option 1: Use Existing Accounts (If Available)

Try logging in with these credentials at http://localhost:3000/login:
- Email: `patient1@hospital.com`
- Password: `password123`

## 🔧 Option 2: Create Test Patients via API

If no accounts exist yet, you can create them using the registration endpoint:

### Using PowerShell:
```powershell
# Create Patient 1
$body = @{
    email = "patient1@hospital.com"
    password = "password123"
    full_name = "John Doe"
    role = "patient"
    hospital_id = 1
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/auth/register" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

### Using curl:
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "patient1@hospital.com",
    "password": "password123",
    "full_name": "John Doe",
    "role": "patient",
    "hospital_id": 1
  }'
```

### Using the Swagger UI (Easiest):
1. Open http://127.0.0.1:8000/docs in your browser
2. Find the `/api/v1/auth/register` endpoint
3. Click "Try it out"
4. Fill in the request body:
   ```json
   {
     "email": "patient1@hospital.com",
     "password": "password123",
     "full_name": "John Doe",
     "role": "patient",
     "hospital_id": 1
   }
   ```
5. Click "Execute"
6. Repeat for patient2, patient3, etc.

## 🚀 Test the Login

1. Go to: http://localhost:3000/login
2. Enter credentials:
   - Email: `patient1@hospital.com`
   - Password: `password123`
3. Click "Sign In"

## ✨ What's Working Now

- ✅ Frontend running on http://localhost:3000
- ✅ Backend running on http://127.0.0.1:8000
- ✅ Login page with medical theme
- ✅ Sample credentials displayed on login page
- ✅ API documentation at http://127.0.0.1:8000/docs

## 🐛 Troubleshooting

### Still getting "Failed to fetch"?
- Make sure both servers are running
- Frontend: http://localhost:3000
- Backend: http://127.0.0.1:8000

### Can't login?
- Create a user account first (see Option 2 above)
- Check the backend logs for errors
- Verify the email/password are correct

### Database errors?
- The database might need initialization
- Check if `alembic` migrations have been run
- Run: `alembic upgrade head` in the backend directory
