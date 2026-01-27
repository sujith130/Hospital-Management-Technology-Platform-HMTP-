from pydantic import BaseModel, ConfigDict
from datetime import datetime, date
from typing import Optional

class MedicineBase(BaseModel):
    name: str
    manufacturer: Optional[str] = None
    batch_number: Optional[str] = None
    expiry_date: date
    quantity: int = 0
    unit_price: float
    description: Optional[str] = None

class MedicineCreate(MedicineBase):
    pass

class MedicineUpdate(BaseModel):
    name: Optional[str] = None
    manufacturer: Optional[str] = None
    batch_number: Optional[str] = None
    expiry_date: Optional[date] = None
    quantity: Optional[int] = None
    unit_price: Optional[float] = None
    description: Optional[str] = None

class MedicineResponse(MedicineBase):
    id: int
    hospital_id: str
    model_config = ConfigDict(from_attributes=True)

class PrescriptionBase(BaseModel):
    patient_id: int
    doctor_id: int
    medicine_id: int
    dosage: str
    frequency: str
    duration: Optional[str] = None
    instructions: Optional[str] = None
    status: str = "active"

class PrescriptionCreate(PrescriptionBase):
    pass

class PrescriptionResponse(PrescriptionBase):
    id: int
    hospital_id: str
    prescribed_date: datetime
    model_config = ConfigDict(from_attributes=True)

class DispenseRequest(BaseModel):
    prescription_id: int
    quantity: int
