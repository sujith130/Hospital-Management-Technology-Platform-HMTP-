from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional, List
from datetime import time

class DoctorAvailabilityBase(BaseModel):
    day_of_week: int # 0-6
    start_time: time
    end_time: time
    is_available: bool = True

class DoctorAvailabilityCreate(DoctorAvailabilityBase):
    pass

class DoctorAvailabilityResponse(DoctorAvailabilityBase):
    id: int
    doctor_id: int
    hospital_id: str
    model_config = ConfigDict(from_attributes=True)

class DoctorBase(BaseModel):
    full_name: str
    specialization: Optional[str] = None
    qualification: Optional[str] = None
    license_number: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None

class DoctorCreate(DoctorBase):
    pass

class DoctorUpdate(DoctorBase):
    full_name: Optional[str] = None

class DoctorResponse(DoctorBase):
    id: int
    hospital_id: str
    availabilities: List[DoctorAvailabilityResponse] = []
    model_config = ConfigDict(from_attributes=True)
