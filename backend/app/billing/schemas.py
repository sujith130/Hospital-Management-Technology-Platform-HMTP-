from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List

class InvoiceBase(BaseModel):
    patient_id: int
    appointment_id: Optional[int] = None
    total_amount: float = 0.0
    tax_amount: float = 0.0
    discount_amount: float = 0.0
    final_amount: float = 0.0
    status: str = "unpaid"
    due_date: Optional[datetime] = None

class InvoiceCreate(InvoiceBase):
    pass

class InvoiceUpdate(BaseModel):
    status: Optional[str] = None
    total_amount: Optional[float] = None
    final_amount: Optional[float] = None

class InvoiceResponse(InvoiceBase):
    id: int
    hospital_id: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class PaymentBase(BaseModel):
    invoice_id: int
    amount: float
    payment_method: Optional[str] = None
    transaction_id: Optional[str] = None
    notes: Optional[str] = None

class PaymentCreate(PaymentBase):
    pass

class InsuranceClaimBase(BaseModel):
    invoice_id: int
    policy_number: str
    provider_name: str
    claimed_amount: float
    status: str = "pending" # pending, approved, rejected

class InsuranceClaimCreate(InsuranceClaimBase):
    pass

class InsuranceClaimResponse(InsuranceClaimBase):
    id: int
    hospital_id: str
    claim_date: datetime
    model_config = ConfigDict(from_attributes=True)

class PaymentResponse(PaymentBase):
    id: int
    hospital_id: str
    payment_date: datetime
    model_config = ConfigDict(from_attributes=True)
