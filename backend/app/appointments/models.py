from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Enum as SQLAEnum, Text
from app.core.base import Base, HospitalIdMixin
import enum

class AppointmentStatus(str, enum.Enum):
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"

class Appointment(Base, HospitalIdMixin):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    appointment_datetime = Column(DateTime, nullable=False)
    reason = Column(String)
    status = Column(String, default=AppointmentStatus.SCHEDULED.value)
    notes = Column(Text)
