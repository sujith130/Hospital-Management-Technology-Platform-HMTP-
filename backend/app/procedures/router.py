from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.core.database import get_db
from app.procedures import models, schemas

router = APIRouter()

@router.post("/", response_model=schemas.ProcedureResponse)
async def create_procedure(procedure: schemas.ProcedureCreate, db: AsyncSession = Depends(get_db)):
    db_procedure = models.Procedure(**procedure.model_dump())
    db.add(db_procedure)
    await db.commit()
    await db.refresh(db_procedure)
    return db_procedure

@router.get("/", response_model=List[schemas.ProcedureResponse])
async def list_procedures(hospital_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Procedure).where(models.Procedure.hospital_id == hospital_id))
    return result.scalars().all()

@router.get("/patient/{patient_id}", response_model=List[schemas.ProcedureResponse])
async def get_patient_procedure_history(patient_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Procedure).where(models.Procedure.patient_id == patient_id))
    return result.scalars().all()
