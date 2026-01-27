from sqlalchemy import Column, String, Integer, DateTime, JSON, Text
from app.core.base import Base, HospitalIdMixin
from datetime import datetime, timezone

class AuditLog(Base, HospitalIdMixin):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False)
    action = Column(String, index=True, nullable=False) # e.g., "LOGIN", "VIEW_PATIENT", "UPDATE_BILLING"
    resource_type = Column(String, index=True) # e.g., "Patient", "Appointment"
    resource_id = Column(String, index=True)
    details = Column(JSON) # Detailed context about the action
    ip_address = Column(String)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
