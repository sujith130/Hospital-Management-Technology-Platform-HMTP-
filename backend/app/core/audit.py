from typing import Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.audit.models import AuditLog
from app.core.middleware import get_current_hospital_id

from fastapi.encoders import jsonable_encoder

async def log_audit_event(
    db: AsyncSession,
    user_id: str,
    action: str,
    resource_type: Optional[str] = None,
    resource_id: Optional[str] = None,
    details: Optional[Any] = None,
    ip_address: Optional[str] = None,
    hospital_id: Optional[str] = None
) -> None:
    """
    Utility function to log an audit event.
    If hospital_id is not provided, it attempts to fetch it from the request context.
    """
    if not hospital_id:
        hospital_id = get_current_hospital_id()
    
    # Ensure details are JSON serializable (handles dates, etc.)
    safe_details = jsonable_encoder(details) if details else None
    
    db_audit = AuditLog(
        user_id=user_id,
        hospital_id=hospital_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        details=safe_details,
        ip_address=ip_address
    )
    db.add(db_audit)
    # We don't commit here to allow it to be part of the caller's transaction
    # The caller is responsible for committing or we can commit separately if needed.
