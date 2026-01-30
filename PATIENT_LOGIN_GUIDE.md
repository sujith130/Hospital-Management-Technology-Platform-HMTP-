# Patient Login Setup Guide

## Overview
This guide explains how to set up and use the patient login functionality for the HMTP platform.

## Sample Patient Credentials

The system includes pre-configured test accounts for easy testing:

### Patient Accounts
1. **Patient 1**
   - Email: `patient1@hospital.com`
   - Password: `password123`
   - Name: John Doe

2. **Patient 2**
   - Email: `patient2@hospital.com`
   - Password: `password123`
   - Name: Jane Smith

3. **Patient 3**
   - Email: `patient3@hospital.com`
   - Password: `password123`
   - Name: Robert Johnson

### Other Test Accounts
- **Doctor**: `doctor1@hospital.com` / `password123` (Dr. Sarah Williams)
- **Admin**: `admin@hospital.com` / `password123` (Admin User)

## Setting Up the Database

### Prerequisites
- Backend server must be running
- Database must be initialized

### Seeding the Database

1. Navigate to the backend directory:
   ```bash
   cd d:\Documents\projects\HT\backend
   ```

2. Run the seed script:
   ```bash
   python seed_patients.py
   ```

3. The script will:
   - Check if users already exist
   - Create new users if they don't exist
   - Display a summary of created accounts

### Expected Output
```
🌱 Starting database seeding...
============================================================
✓ Created user: patient1@hospital.com (patient)
✓ Created user: patient2@hospital.com (patient)
✓ Created user: patient3@hospital.com (patient)
✓ Created user: doctor1@hospital.com (doctor)
✓ Created user: admin@hospital.com (admin)

✅ Database seeding completed successfully!

📋 Sample Credentials:
============================================================
Email: patient1@hospital.com
Password: password123
Role: patient
Name: John Doe
------------------------------------------------------------
...
```

## Using the Login Page

### Accessing the Login Page

1. **From the Homepage**:
   - Click "Patient Login" button in the header
   - Or navigate directly to: `http://localhost:3000/login`

2. **Login Page Features**:
   - Medical-themed design (blue/teal color scheme)
   - Sample credentials displayed on desktop
   - One-click "Use" buttons to auto-fill credentials
   - Responsive design for mobile devices
   - Loading spinner during authentication
   - Error messages for failed login attempts

### Login Process

1. **Manual Login**:
   - Enter email address
   - Enter password
   - Click "Sign In"

2. **Quick Login (Desktop)**:
   - Click "Use" button next to any sample credential
   - Credentials will auto-fill
   - Click "Sign In"

3. **Quick Login (Mobile)**:
   - Tap on any credential card in the "Test Credentials" section
   - Credentials will auto-fill
   - Tap "Sign In"

### After Login

Once logged in successfully, users will be redirected to their role-specific dashboard:
- **Patients**: `/dashboard/patient`
- **Doctors**: `/dashboard/doctor`
- **Admins**: `/dashboard/admin`

## Troubleshooting

### "Login failed" Error
- **Cause**: User doesn't exist in database
- **Solution**: Run the seed script (`python seed_patients.py`)

### "Invalid credentials" Error
- **Cause**: Incorrect email or password
- **Solution**: Use the exact credentials listed above (case-sensitive)

### Backend Connection Error
- **Cause**: Backend server not running
- **Solution**: 
  ```bash
  cd d:\Documents\projects\HT\backend
  uvicorn app.main:app --reload
  ```

### Database Not Initialized
- **Cause**: Database tables don't exist
- **Solution**: Run database migrations first
  ```bash
  alembic upgrade head
  ```

## Security Notes

⚠️ **Important**: These are test credentials for development only!

- **DO NOT** use these credentials in production
- **DO NOT** commit real user passwords to version control
- **ALWAYS** use strong, unique passwords in production
- **ENABLE** proper password hashing (already implemented with bcrypt)
- **IMPLEMENT** password reset functionality for production

## Next Steps

After setting up patient login, you can:

1. **Test the Patient Dashboard**: Navigate to `/dashboard/patient` after login
2. **Book Appointments**: Use the appointment booking flow
3. **View Medical Records**: Access patient-specific data
4. **Manage Profile**: Update patient information

## Technical Details

### Authentication Flow
1. User submits email/password
2. Frontend sends credentials to `/api/v1/auth/login`
3. Backend validates credentials
4. Backend returns JWT access token
5. Frontend stores token and user info
6. Frontend redirects to role-specific dashboard

### JWT Token Structure
```json
{
  "sub": "patient1@hospital.com",
  "role": "patient",
  "hospital_id": 1,
  "exp": 1234567890
}
```

### Password Hashing
- Algorithm: bcrypt
- Rounds: 12 (default)
- Implemented in: `app/auth/security.py`

## Support

For issues or questions:
- Check the backend logs: `d:\Documents\projects\HT\backend\logs`
- Check the browser console for frontend errors
- Verify database connection settings in `.env`
