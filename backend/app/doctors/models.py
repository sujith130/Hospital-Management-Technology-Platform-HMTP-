from sqlalchemy import Column, String, Integer, Time, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.core.base import Base, HospitalIdMixin

class Doctor(Base, HospitalIdMixin):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True, nullable=False)
    specialization = Column(String, index=True)
    qualification = Column(String)
    license_number = Column(String, unique=True, index=True)
    phone_number = Column(String)
    email = Column(String, unique=True, index=True)

    availabilities = relationship("DoctorAvailability", back_populates="doctor", cascade="all, delete-orphan")

class DoctorAvailability(Base, HospitalIdMixin):
    __tablename__ = "doctor_availabilities"

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    day_of_week = Column(Integer, nullable=False) # 0-6 (Monday-Sunday)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    is_available = Column(Boolean, default=True)

    doctor = relationship("Doctor", back_populates="availabilities")
