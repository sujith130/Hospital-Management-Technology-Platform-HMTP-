from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.core.database import get_db
from app.pharmacy import models, schemas
from app.auth.deps import get_current_user
from app.auth.models import User
from app.core.audit import log_audit_event

router = APIRouter()

# Medicine Endpoints
@router.post("/medicines/", response_model=schemas.MedicineResponse)
async def create_medicine(
    medicine: schemas.MedicineCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_medicine = models.Medicine(
        **medicine.model_dump(),
        hospital_id=current_user.hospital_id
    )
    db.add(db_medicine)
    
    await log_audit_event(
        db=db,
        user_id=str(current_user.id),
        action="CREATE_MEDICINE",
        resource_type="Medicine",
        details=medicine.model_dump(),
        hospital_id=current_user.hospital_id
    )
    
    await db.commit()
    await db.refresh(db_medicine)
    return db_medicine

@router.get("/medicines/", response_model=List[schemas.MedicineResponse])
async def list_medicines(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(models.Medicine).where(models.Medicine.hospital_id == current_user.hospital_id)
    )
    return result.scalars().all()

@router.put("/medicines/{medicine_id}", response_model=schemas.MedicineResponse)
async def update_medicine(
    medicine_id: int,
    medicine_in: schemas.MedicineUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(models.Medicine)
        .where(models.Medicine.id == medicine_id)
        .where(models.Medicine.hospital_id == current_user.hospital_id)
    )
    db_medicine = result.scalars().first()
    if not db_medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    
    update_data = medicine_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_medicine, field, value)
    
    db.add(db_medicine)
    await db.commit()
    await db.refresh(db_medicine)
    return db_medicine

# Prescription Endpoints
@router.post("/prescriptions/", response_model=schemas.PrescriptionResponse)
async def create_prescription(
    prescription: schemas.PrescriptionCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verify medicine exists and belongs to the same hospital
    med_result = await db.execute(
        select(models.Medicine)
        .where(models.Medicine.id == prescription.medicine_id)
        .where(models.Medicine.hospital_id == current_user.hospital_id)
    )
    if not med_result.scalars().first():
        raise HTTPException(status_code=404, detail="Medicine not found")

    db_prescription = models.Prescription(
        **prescription.model_dump(),
        hospital_id=current_user.hospital_id
    )
    db.add(db_prescription)
    
    await log_audit_event(
        db=db,
        user_id=str(current_user.id),
        action="CREATE_PRESCRIPTION",
        resource_type="Prescription",
        details=prescription.model_dump(),
        hospital_id=current_user.hospital_id
    )
    
    await db.commit()
    await db.refresh(db_prescription)
    return db_prescription

@router.get("/prescriptions/patient/{patient_id}", response_model=List[schemas.PrescriptionResponse])
async def get_patient_prescriptions(
    patient_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(models.Prescription)
        .where(models.Prescription.patient_id == patient_id)
        .where(models.Prescription.hospital_id == current_user.hospital_id)
    )
    return result.scalars().all()

# Dispensing logic
@router.post("/dispense/", status_code=status.HTTP_200_OK)
async def dispense_medicine(
    request: schemas.DispenseRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1. Fetch prescription
    prescription_result = await db.execute(
        select(models.Prescription)
        .where(models.Prescription.id == request.prescription_id)
        .where(models.Prescription.hospital_id == current_user.hospital_id)
    )
    db_prescription = prescription_result.scalars().first()
    if not db_prescription:
        raise HTTPException(status_code=404, detail="Prescription not found")
    
    if db_prescription.status != "active":
        raise HTTPException(status_code=400, detail="Prescription is not active")

    # 2. Fetch medicine
    medicine_result = await db.execute(
        select(models.Medicine)
        .where(models.Medicine.id == db_prescription.medicine_id)
        .where(models.Medicine.hospital_id == current_user.hospital_id)
    )
    db_medicine = medicine_result.scalars().first()
    if not db_medicine:
        # Should not happen if data integrity is maintained
        raise HTTPException(status_code=404, detail="Medicine not found")

    # 3. Check inventory
    if db_medicine.quantity < request.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    # 4. Update inventory
    db_medicine.quantity -= request.quantity
    db.add(db_medicine)

    # 5. Log audit
    await log_audit_event(
        db=db,
        user_id=str(current_user.id),
        action="DISPENSE_MEDICINE",
        resource_type="Prescription",
        resource_id=str(request.prescription_id),
        details={"quantity": request.quantity, "medicine_id": db_medicine.id},
        hospital_id=current_user.hospital_id
    )

    # Note: In a real system, we might mark prescription as partially or fully dispensed
    
    await db.commit()
    return {"message": "Medicine dispensed successfully", "remaining_stock": db_medicine.quantity}
