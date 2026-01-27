from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional

class PatientBase(BaseModel):
    first_name: str
    last_name: str
    gender: Optional[str] = None
    date_of_birth: Optional[date] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None

class PatientCreate(PatientBase):
    pass

class PatientUpdate(PatientBase):
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class PatientResponse(PatientBase):
    id: int
    hospital_id: str
    model_config = ConfigDict(from_attributes=True)
