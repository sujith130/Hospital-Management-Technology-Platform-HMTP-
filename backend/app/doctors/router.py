from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List
from app.core.database import get_db
from app.doctors import models, schemas
from app.auth.deps import get_current_user
from app.auth.models import User
from app.core.audit import log_audit_event

router = APIRouter()

@router.post("/", response_model=schemas.DoctorResponse)
async def create_doctor(
    doctor: schemas.DoctorCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_doctor = models.Doctor(
        **doctor.model_dump(),
        hospital_id=current_user.hospital_id
    )
    db.add(db_doctor)
    
    await log_audit_event(
        db=db,
        user_id=str(current_user.id),
        action="CREATE_DOCTOR",
        resource_type="Doctor",
        details=doctor.model_dump(),
        hospital_id=current_user.hospital_id
    )
    
    await db.commit()
    
    # Re-fetch with selectinload to avoid lazy-load error during serialization
    result = await db.execute(
        select(models.Doctor)
        .options(selectinload(models.Doctor.availabilities))
        .where(models.Doctor.id == db_doctor.id)
    )
    return result.scalars().first()

@router.get("/", response_model=List[schemas.DoctorResponse])
async def list_doctors(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(models.Doctor)
        .options(selectinload(models.Doctor.availabilities))
        .where(models.Doctor.hospital_id == current_user.hospital_id)
    )
    return result.scalars().all()

@router.get("/{doctor_id}", response_model=schemas.DoctorResponse)
async def get_doctor(
    doctor_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(models.Doctor)
        .options(selectinload(models.Doctor.availabilities))
        .where(models.Doctor.id == doctor_id)
        .where(models.Doctor.hospital_id == current_user.hospital_id)
    )
    db_doctor = result.scalars().first()
    if not db_doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return db_doctor

@router.put("/{doctor_id}", response_model=schemas.DoctorResponse)
async def update_doctor(
    doctor_id: int,
    doctor_in: schemas.DoctorUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(models.Doctor)
        .where(models.Doctor.id == doctor_id)
        .where(models.Doctor.hospital_id == current_user.hospital_id)
    )
    db_doctor = result.scalars().first()
    if not db_doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    update_data = doctor_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_doctor, field, value)
    
    db.add(db_doctor)
    
    await log_audit_event(
        db=db,
        user_id=str(current_user.id),
        action="UPDATE_DOCTOR",
        resource_type="Doctor",
        resource_id=str(doctor_id),
        details=update_data,
        hospital_id=current_user.hospital_id
    )
    
    await db.commit()
    
    # Re-fetch with selectinload
    result = await db.execute(
        select(models.Doctor)
        .options(selectinload(models.Doctor.availabilities))
        .where(models.Doctor.id == doctor_id)
    )
    return result.scalars().first()

# Availability Endpoints

@router.post("/{doctor_id}/availability", response_model=schemas.DoctorAvailabilityResponse)
async def create_doctor_availability(
    doctor_id: int,
    availability: schemas.DoctorAvailabilityCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Ensure doctor exists and belongs to the same hospital
    doctor_result = await db.execute(
        select(models.Doctor)
        .where(models.Doctor.id == doctor_id)
        .where(models.Doctor.hospital_id == current_user.hospital_id)
    )
    if not doctor_result.scalars().first():
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    db_availability = models.DoctorAvailability(
        **availability.model_dump(),
        doctor_id=doctor_id,
        hospital_id=current_user.hospital_id
    )
    db.add(db_availability)
    
    await log_audit_event(
        db=db,
        user_id=str(current_user.id),
        action="CREATE_DOCTOR_AVAILABILITY",
        resource_type="DoctorAvailability",
        resource_id=str(doctor_id),
        details=availability.model_dump(),
        hospital_id=current_user.hospital_id
    )
    
    await db.commit()
    await db.refresh(db_availability)
    return db_availability

@router.delete("/{doctor_id}/availability/{availability_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_doctor_availability(
    doctor_id: int,
    availability_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(models.DoctorAvailability)
        .where(models.DoctorAvailability.id == availability_id)
        .where(models.DoctorAvailability.doctor_id == doctor_id)
        .where(models.DoctorAvailability.hospital_id == current_user.hospital_id)
    )
    db_availability = result.scalars().first()
    if not db_availability:
        raise HTTPException(status_code=404, detail="Availability not found")
    
    await db.delete(db_availability)
    
    await log_audit_event(
        db=db,
        user_id=str(current_user.id),
        action="DELETE_DOCTOR_AVAILABILITY",
        resource_type="DoctorAvailability",
        resource_id=str(availability_id),
        hospital_id=current_user.hospital_id
    )
    
    await db.commit()
    return None

@router.delete("/{doctor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_doctor(
    doctor_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(models.Doctor)
        .where(models.Doctor.id == doctor_id)
        .where(models.Doctor.hospital_id == current_user.hospital_id)
    )
    db_doctor = result.scalars().first()
    if not db_doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    await db.delete(db_doctor)
    
    await log_audit_event(
        db=db,
        user_id=str(current_user.id),
        action="DELETE_DOCTOR",
        resource_type="Doctor",
        resource_id=str(doctor_id),
        hospital_id=current_user.hospital_id
    )
    
    await db.commit()
    return None
