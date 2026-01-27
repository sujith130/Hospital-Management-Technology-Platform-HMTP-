from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text
from app.core.base import Base, HospitalIdMixin
from datetime import datetime, timezone

class Procedure(Base, HospitalIdMixin):
    __tablename__ = "procedures"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    procedure_name = Column(String, index=True, nullable=False) # e.g., "Appendectomy"
    procedure_date = Column(DateTime, nullable=False)
    description = Column(Text)
    outcome = Column(Text)
    notes = Column(Text)
