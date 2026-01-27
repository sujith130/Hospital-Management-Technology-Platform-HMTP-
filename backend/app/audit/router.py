from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.core.database import get_db
from app.audit import models, schemas

router = APIRouter()

@router.get("/", response_model=List[schemas.AuditLogResponse])
async def list_audit_logs(hospital_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.AuditLog).where(models.AuditLog.hospital_id == hospital_id))
    return result.scalars().all()
