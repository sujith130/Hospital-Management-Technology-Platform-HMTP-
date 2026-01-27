from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.core.database import get_db
from app.labs import models, schemas
from app.auth.deps import get_current_user
from app.auth.models import User
from app.core.audit import log_audit_event

router = APIRouter()

@router.post("/", response_model=schemas.LabTestResponse)
async def create_lab_test(
    test: schemas.LabTestCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_test = models.LabTest(
        **test.model_dump(),
        hospital_id=current_user.hospital_id
    )
    db.add(db_test)
    
    await log_audit_event(
        db=db,
        user_id=str(current_user.id),
        action="CREATE_LAB_TEST",
        resource_type="LabTest",
        details=test.model_dump(),
        hospital_id=current_user.hospital_id
    )
    
    await db.commit()
    await db.refresh(db_test)
    return db_test

@router.get("/", response_model=List[schemas.LabTestResponse])
async def list_lab_tests(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(models.LabTest).where(models.LabTest.hospital_id == current_user.hospital_id)
    )
    return result.scalars().all()

@router.get("/{test_id}", response_model=schemas.LabTestResponse)
async def get_lab_test(
    test_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(models.LabTest)
        .where(models.LabTest.id == test_id)
        .where(models.LabTest.hospital_id == current_user.hospital_id)
    )
    db_test = result.scalars().first()
    if not db_test:
        raise HTTPException(status_code=404, detail="Lab test not found")
    return db_test

@router.put("/{test_id}", response_model=schemas.LabTestResponse)
async def update_lab_test(
    test_id: int,
    test_in: schemas.LabTestUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(models.LabTest)
        .where(models.LabTest.id == test_id)
        .where(models.LabTest.hospital_id == current_user.hospital_id)
    )
    db_test = result.scalars().first()
    if not db_test:
        raise HTTPException(status_code=404, detail="Lab test not found")
    
    update_data = test_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_test, field, value)
    
    db.add(db_test)
    
    await log_audit_event(
        db=db,
        user_id=str(current_user.id),
        action="UPDATE_LAB_TEST",
        resource_type="LabTest",
        resource_id=str(test_id),
        details=update_data,
        hospital_id=current_user.hospital_id
    )
    
    await db.commit()
    await db.refresh(db_test)
    return db_test

@router.get("/patient/{patient_id}", response_model=List[schemas.LabTestResponse])
async def get_patient_lab_history(
    patient_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(models.LabTest)
        .where(models.LabTest.patient_id == patient_id)
        .where(models.LabTest.hospital_id == current_user.hospital_id)
    )
    return result.scalars().all()
