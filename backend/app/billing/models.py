from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey, Text
from app.core.base import Base, HospitalIdMixin
from datetime import datetime, timezone
import enum

class InvoiceStatus(str, enum.Enum):
    UNPAID = "unpaid"
    PAID = "paid"
    PARTIAL = "partial"
    CANCELLED = "cancelled"

class Invoice(Base, HospitalIdMixin):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    appointment_id = Column(Integer, ForeignKey("appointments.id"), nullable=True)
    total_amount = Column(Float, default=0.0)
    tax_amount = Column(Float, default=0.0)
    discount_amount = Column(Float, default=0.0)
    final_amount = Column(Float, default=0.0)
    status = Column(String, default=InvoiceStatus.UNPAID.value)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    due_date = Column(DateTime)

class Payment(Base, HospitalIdMixin):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=False)
    amount = Column(Float, nullable=False)
    payment_method = Column(String) # Cash, Card, UPI, Insurance
    transaction_id = Column(String, unique=True, index=True)
    payment_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    notes = Column(Text)
class InsuranceClaim(Base, HospitalIdMixin):
    __tablename__ = "insurance_claims"

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=False)
    policy_number = Column(String, index=True, nullable=False)
    provider_name = Column(String, index=True, nullable=False)
    claimed_amount = Column(Float, nullable=False)
    status = Column(String, default="pending")
    claim_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    notes = Column(Text)
