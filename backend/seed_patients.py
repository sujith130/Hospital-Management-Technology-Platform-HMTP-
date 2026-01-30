"""
Database seeding script to create sample patient accounts for testing.

Usage:
    python seed_patients.py

This will create sample patient users in the database with the following credentials:
- patient1@hospital.com / password123
- patient2@hospital.com / password123
- patient3@hospital.com / password123
"""

import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.auth.models import User, UserRole
from app.auth.security import get_password_hash

# Sample patient data
SAMPLE_PATIENTS = [
    {
        "email": "patient1@hospital.com",
        "password": "password123",
        "full_name": "John Doe",
        "role": UserRole.PATIENT.value,
        "hospital_id": 1,
    },
    {
        "email": "patient2@hospital.com",
        "password": "password123",
        "full_name": "Jane Smith",
        "role": UserRole.PATIENT.value,
        "hospital_id": 1,
    },
    {
        "email": "patient3@hospital.com",
        "password": "password123",
        "full_name": "Robert Johnson",
        "role": UserRole.PATIENT.value,
        "hospital_id": 1,
    },
    {
        "email": "doctor1@hospital.com",
        "password": "password123",
        "full_name": "Dr. Sarah Williams",
        "role": UserRole.DOCTOR.value,
        "hospital_id": 1,
    },
    {
        "email": "admin@hospital.com",
        "password": "password123",
        "full_name": "Admin User",
        "role": UserRole.ADMIN.value,
        "hospital_id": 1,
    },
]


async def seed_users():
    """Seed the database with sample users."""
    # Create async engine
    engine = create_async_engine(settings.DATABASE_URL, echo=True)
    
    # Create async session
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        try:
            # Check if users already exist
            from sqlalchemy import select
            
            for patient_data in SAMPLE_PATIENTS:
                # Check if user exists
                result = await session.execute(
                    select(User).where(User.email == patient_data["email"])
                )
                existing_user = result.scalar_one_or_none()
                
                if existing_user:
                    print(f"✓ User {patient_data['email']} already exists, skipping...")
                    continue
                
                # Create new user
                user = User(
                    email=patient_data["email"],
                    hashed_password=get_password_hash(patient_data["password"]),
                    full_name=patient_data["full_name"],
                    role=patient_data["role"],
                    hospital_id=patient_data["hospital_id"],
                    is_active=True,
                )
                
                session.add(user)
                print(f"✓ Created user: {patient_data['email']} ({patient_data['role']})")
            
            # Commit all changes
            await session.commit()
            print("\n✅ Database seeding completed successfully!")
            print("\n📋 Sample Credentials:")
            print("=" * 60)
            for patient_data in SAMPLE_PATIENTS:
                print(f"Email: {patient_data['email']}")
                print(f"Password: {patient_data['password']}")
                print(f"Role: {patient_data['role']}")
                print(f"Name: {patient_data['full_name']}")
                print("-" * 60)
            
        except Exception as e:
            print(f"❌ Error seeding database: {e}")
            await session.rollback()
            raise
        finally:
            await engine.dispose()


if __name__ == "__main__":
    print("🌱 Starting database seeding...")
    print("=" * 60)
    asyncio.run(seed_users())
