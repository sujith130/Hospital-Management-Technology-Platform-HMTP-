from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class LabTestBase(BaseModel):
    patient_id: int
    doctor_id: int
    test_name: str
    category: Optional[str] = None
    result_summary: Optional[str] = None
    report_url: Optional[str] = None
    status: str = "completed"

class LabTestCreate(LabTestBase):
    pass

class LabTestUpdate(BaseModel):
    result_summary: Optional[str] = None
    report_url: Optional[str] = None
    status: Optional[str] = None

class LabTestResponse(LabTestBase):
    id: int
    hospital_id: str
    test_date: datetime
    model_config = ConfigDict(from_attributes=True)
