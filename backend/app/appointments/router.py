from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from typing import List
from datetime import timedelta
from app.core.database import get_db
from app.appointments import models, schemas
from app.auth.deps import get_current_user
from app.auth.models import User
from app.core.audit import log_audit_event
from app.patients.models import Patient
from app.doctors.models import Doctor, DoctorAvailability

router = APIRouter()

@router.post("/", response_model=schemas.AppointmentResponse)
async def create_appointment(
    appointment: schemas.AppointmentCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1. Validate Patient
    patient_result = await db.execute(
        select(Patient)
        .where(Patient.id == appointment.patient_id)
        .where(Patient.hospital_id == current_user.hospital_id)
    )
    if not patient_result.scalars().first():
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # 2. Validate Doctor
    doctor_result = await db.execute(
        select(Doctor)
        .where(Doctor.id == appointment.doctor_id)
        .where(Doctor.hospital_id == current_user.hospital_id)
    )
    if not doctor_result.scalars().first():
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    # 3. Check Doctor Availability
    day_of_week = appointment.appointment_datetime.weekday()
    appt_time = appointment.appointment_datetime.time()
    
    availability_result = await db.execute(
        select(DoctorAvailability)
        .where(DoctorAvailability.doctor_id == appointment.doctor_id)
        .where(DoctorAvailability.day_of_week == day_of_week)
        .where(DoctorAvailability.is_available == True)
        .where(DoctorAvailability.start_time <= appt_time)
        .where(DoctorAvailability.end_time > appt_time)
    )
    if not availability_result.scalars().first():
        raise HTTPException(
            status_code=400, 
            detail="Doctor is not available at the requested time"
        )
    
    # 4. Check for conflicts (30 minute window)
    window_start = appointment.appointment_datetime - timedelta(minutes=29)
    window_end = appointment.appointment_datetime + timedelta(minutes=29)
    
    conflict_result = await db.execute(
        select(models.Appointment)
        .where(models.Appointment.doctor_id == appointment.doctor_id)
        .where(models.Appointment.status == models.AppointmentStatus.SCHEDULED.value)
        .where(models.Appointment.appointment_datetime > window_start)
        .where(models.Appointment.appointment_datetime < window_end)
    )
    if conflict_result.scalars().first():
        raise HTTPException(status_code=400, detail="Doctor has a conflicting appointment")

    db_appointment = models.Appointment(
        **appointment.model_dump(),
        hospital_id=current_user.hospital_id
    )
    db.add(db_appointment)
    
    await log_audit_event(
        db=db,
        user_id=str(current_user.id),
        action="CREATE_APPOINTMENT",
        resource_type="Appointment",
        details=appointment.model_dump(),
        hospital_id=current_user.hospital_id
    )
    
    await db.commit()
    await db.refresh(db_appointment)
    return db_appointment

@router.get("/", response_model=List[schemas.AppointmentResponse])
async def list_appointments(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(models.Appointment).where(models.Appointment.hospital_id == current_user.hospital_id)
    )
    return result.scalars().all()

@router.get("/{appointment_id}", response_model=schemas.AppointmentResponse)
async def get_appointment(
    appointment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(models.Appointment)
        .where(models.Appointment.id == appointment_id)
        .where(models.Appointment.hospital_id == current_user.hospital_id)
    )
    db_appointment = result.scalars().first()
    if not db_appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return db_appointment

@router.put("/{appointment_id}", response_model=schemas.AppointmentResponse)
async def update_appointment(
    appointment_id: int,
    appointment_in: schemas.AppointmentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(models.Appointment)
        .where(models.Appointment.id == appointment_id)
        .where(models.Appointment.hospital_id == current_user.hospital_id)
    )
    db_appointment = result.scalars().first()
    if not db_appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    update_data = appointment_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_appointment, field, value)
    
    db.add(db_appointment)
    
    await log_audit_event(
        db=db,
        user_id=str(current_user.id),
        action="UPDATE_APPOINTMENT",
        resource_type="Appointment",
        resource_id=str(appointment_id),
        details=update_data,
        hospital_id=current_user.hospital_id
    )
    
    await db.commit()
    await db.refresh(db_appointment)
    return db_appointment

@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_appointment(
    appointment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(models.Appointment)
        .where(models.Appointment.id == appointment_id)
        .where(models.Appointment.hospital_id == current_user.hospital_id)
    )
    db_appointment = result.scalars().first()
    if not db_appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    await db.delete(db_appointment)
    
    await log_audit_event(
        db=db,
        user_id=str(current_user.id),
        action="DELETE_APPOINTMENT",
        resource_type="Appointment",
        resource_id=str(appointment_id),
        hospital_id=current_user.hospital_id
    )
    
    await db.commit()
    return None
