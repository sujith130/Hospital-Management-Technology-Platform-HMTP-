from sqlalchemy import Column, String, Integer, Boolean, Enum as SQLAEnum
from app.core.base import Base, HospitalIdMixin
import enum

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    DOCTOR = "doctor"
    PATIENT = "patient"
    NURSE = "nurse"
    LAB_TECHNICIAN = "lab_technician"
    PHARMACIST = "pharmacist"

class User(Base, HospitalIdMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, index=True)
    is_active = Column(Boolean, default=True)
    role = Column(String, default=UserRole.PATIENT.value) # Storing as string for simplicity with Enum
