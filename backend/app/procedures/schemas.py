from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class ProcedureBase(BaseModel):
    patient_id: int
    doctor_id: int
    procedure_name: str
    procedure_date: datetime
    description: Optional[str] = None
    outcome: Optional[str] = None
    notes: Optional[str] = None

class ProcedureCreate(ProcedureBase):
    hospital_id: str

class ProcedureUpdate(BaseModel):
    procedure_name: Optional[str] = None
    procedure_date: Optional[datetime] = None
    outcome: Optional[str] = None

class ProcedureResponse(ProcedureBase):
    id: int
    hospital_id: str
    model_config = ConfigDict(from_attributes=True)
