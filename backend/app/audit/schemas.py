from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, Any

class AuditLogBase(BaseModel):
    user_id: str
    action: str
    resource_type: Optional[str] = None
    resource_id: Optional[str] = None
    details: Optional[Any] = None
    ip_address: Optional[str] = None

class AuditLogResponse(AuditLogBase):
    id: int
    hospital_id: str
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)
