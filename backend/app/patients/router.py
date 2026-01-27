from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.core.database import get_db
from app.patients import models, schemas
from app.auth.deps import get_current_user
from app.auth.models import User
from app.core.audit import log_audit_event

router = APIRouter()

@router.post("/", response_model=schemas.PatientResponse)
async def create_patient(
    patient: schemas.PatientCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_patient = models.Patient(
        **patient.model_dump(),
        hospital_id=current_user.hospital_id
    )
    db.add(db_patient)
    
    await log_audit_event(
        db=db,
        user_id=str(current_user.id),
        action="CREATE_PATIENT",
        resource_type="Patient",
        details=patient.model_dump(),
        hospital_id=current_user.hospital_id
    )
    
    await db.commit()
    await db.refresh(db_patient)
    return db_patient

@router.get("/", response_model=List[schemas.PatientResponse])
async def list_patients(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(models.Patient).where(models.Patient.hospital_id == current_user.hospital_id)
    )
    return result.scalars().all()

@router.get("/{patient_id}", response_model=schemas.PatientResponse)
async def get_patient(
    patient_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(models.Patient)
        .where(models.Patient.id == patient_id)
        .where(models.Patient.hospital_id == current_user.hospital_id)
    )
    db_patient = result.scalars().first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return db_patient

@router.put("/{patient_id}", response_model=schemas.PatientResponse)
async def update_patient(
    patient_id: int,
    patient_in: schemas.PatientUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(models.Patient)
        .where(models.Patient.id == patient_id)
        .where(models.Patient.hospital_id == current_user.hospital_id)
    )
    db_patient = result.scalars().first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    update_data = patient_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_patient, field, value)
    
    db.add(db_patient)
    
    await log_audit_event(
        db=db,
        user_id=str(current_user.id),
        action="UPDATE_PATIENT",
        resource_type="Patient",
        resource_id=str(patient_id),
        details=update_data,
        hospital_id=current_user.hospital_id
    )
    
    await db.commit()
    await db.refresh(db_patient)
    return db_patient

@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_patient(
    patient_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(models.Patient)
        .where(models.Patient.id == patient_id)
        .where(models.Patient.hospital_id == current_user.hospital_id)
    )
    db_patient = result.scalars().first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    await db.delete(db_patient)
    
    await log_audit_event(
        db=db,
        user_id=str(current_user.id),
        action="DELETE_PATIENT",
        resource_type="Patient",
        resource_id=str(patient_id),
        hospital_id=current_user.hospital_id
    )
    
    await db.commit()
    return None
