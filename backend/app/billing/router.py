from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.core.database import get_db
from app.billing import models, schemas
from app.auth.deps import get_current_user
from app.auth.models import User
from app.core.audit import log_audit_event

router = APIRouter()

# Invoice Endpoints
@router.post("/invoices/", response_model=schemas.InvoiceResponse)
async def create_invoice(
    invoice: schemas.InvoiceCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_invoice = models.Invoice(
        **invoice.model_dump(),
        hospital_id=current_user.hospital_id
    )
    db.add(db_invoice)
    
    await log_audit_event(
        db=db,
        user_id=str(current_user.id),
        action="CREATE_INVOICE",
        resource_type="Invoice",
        details=invoice.model_dump(),
        hospital_id=current_user.hospital_id
    )
    
    await db.commit()
    await db.refresh(db_invoice)
    return db_invoice

@router.get("/invoices/patient/{patient_id}", response_model=List[schemas.InvoiceResponse])
async def get_patient_invoices(
    patient_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(models.Invoice)
        .where(models.Invoice.patient_id == patient_id)
        .where(models.Invoice.hospital_id == current_user.hospital_id)
    )
    return result.scalars().all()

# Payment Endpoints
@router.post("/payments/", response_model=schemas.PaymentResponse)
async def create_payment(
    payment: schemas.PaymentCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verify invoice exists and belongs to the same hospital
    invoice_result = await db.execute(
        select(models.Invoice)
        .where(models.Invoice.id == payment.invoice_id)
        .where(models.Invoice.hospital_id == current_user.hospital_id)
    )
    invoice = invoice_result.scalars().first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    db_payment = models.Payment(
        **payment.model_dump(),
        hospital_id=current_user.hospital_id
    )
    db.add(db_payment)
    
    # Simple logic: Update invoice status if fully paid
    # In a real system, we'd check total payments vs final_amount
    invoice.status = models.InvoiceStatus.PAID.value
    db.add(invoice)
    
    await log_audit_event(
        db=db,
        user_id=str(current_user.id),
        action="CREATE_PAYMENT",
        resource_type="Payment",
        details=payment.model_dump(),
        hospital_id=current_user.hospital_id
    )
    
    await db.commit()
    await db.refresh(db_payment)
    return db_payment

# Insurance Endpoints
@router.post("/insurance-claims/", response_model=schemas.InsuranceClaimResponse)
async def create_insurance_claim(
    claim: schemas.InsuranceClaimCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verify invoice exists and belongs to the same hospital
    invoice_result = await db.execute(
        select(models.Invoice)
        .where(models.Invoice.id == claim.invoice_id)
        .where(models.Invoice.hospital_id == current_user.hospital_id)
    )
    if not invoice_result.scalars().first():
        raise HTTPException(status_code=404, detail="Invoice not found")

    db_claim = models.InsuranceClaim(
        **claim.model_dump(),
        hospital_id=current_user.hospital_id
    )
    db.add(db_claim)
    
    await log_audit_event(
        db=db,
        user_id=str(current_user.id),
        action="SUBMIT_INSURANCE_CLAIM",
        resource_type="InsuranceClaim",
        details=claim.model_dump(),
        hospital_id=current_user.hospital_id
    )
    
    await db.commit()
    await db.refresh(db_claim)
    return db_claim
