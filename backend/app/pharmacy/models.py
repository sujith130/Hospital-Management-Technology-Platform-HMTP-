from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey, Text, Date
from app.core.base import Base, HospitalIdMixin
from datetime import datetime, timezone

class Medicine(Base, HospitalIdMixin):
    __tablename__ = "medicines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    manufacturer = Column(String)
    batch_number = Column(String, index=True)
    expiry_date = Column(Date, nullable=False)
    quantity = Column(Integer, default=0)
    unit_price = Column(Float, nullable=False)
    description = Column(Text)

class Prescription(Base, HospitalIdMixin):
    __tablename__ = "prescriptions"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    medicine_id = Column(Integer, ForeignKey("medicines.id"), nullable=False)
    dosage = Column(String, nullable=False) # e.g., "500mg"
    frequency = Column(String, nullable=False) # e.g., "Twice a day"
    duration = Column(String) # e.g., "5 days"
    instructions = Column(Text)
    prescribed_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    status = Column(String, default="active") # active, completed, cancelled
