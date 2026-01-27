from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text
from app.core.base import Base, HospitalIdMixin
from datetime import datetime, timezone

class LabTest(Base, HospitalIdMixin):
    __tablename__ = "lab_tests"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    test_name = Column(String, index=True, nullable=False) # e.g., "Complete Blood Count", "MRI Brain"
    category = Column(String, index=True) # e.g., "Blood Test", "Scan", "X-Ray"
    test_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    result_summary = Column(Text)
    report_url = Column(String) # Link to digital report/image
    status = Column(String, default="completed") # pending, completed, reviewed
