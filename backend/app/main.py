from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core import config
from app.auth import router as auth_router
from app.patients import router as patient_router
from app.doctors import router as doctor_router
from app.appointments import router as appointment_router
from app.audit import router as audit_router
from app.labs import router as lab_router
from app.procedures import router as procedure_router
from app.pharmacy import router as pharmacy_router
from app.billing import router as billing_router
from app.core.middleware import MultiTenantMiddleware

app = FastAPI(
    title=config.settings.PROJECT_NAME,
    description="Enterprise Multi-Tenant Hospital Management System",
    version="1.0.0",
    openapi_url=f"{config.settings.API_V1_STR}/openapi.json",
    docs_url=f"{config.settings.API_V1_STR}/docs",
    redoc_url=f"{config.settings.API_V1_STR}/redoc",
)

# CORS Middleware
app.add_middleware(MultiTenantMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router, prefix=f"{config.settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(patient_router.router, prefix=f"{config.settings.API_V1_STR}/patients", tags=["patients"])
app.include_router(doctor_router.router, prefix=f"{config.settings.API_V1_STR}/doctors", tags=["doctors"])
app.include_router(appointment_router.router, prefix=f"{config.settings.API_V1_STR}/appointments", tags=["appointments"])
app.include_router(audit_router.router, prefix=f"{config.settings.API_V1_STR}/audit", tags=["audit"])
app.include_router(lab_router.router, prefix=f"{config.settings.API_V1_STR}/labs", tags=["labs"])
app.include_router(procedure_router.router, prefix=f"{config.settings.API_V1_STR}/procedures", tags=["procedures"])
app.include_router(pharmacy_router.router, prefix=f"{config.settings.API_V1_STR}/pharmacy", tags=["pharmacy"])
app.include_router(billing_router.router, prefix=f"{config.settings.API_V1_STR}/billing", tags=["billing"])

@app.get("/")
def read_root():
    return {
        "message": "Welcome to HMTP API",
        "status": "active",
        "documentation": f"{config.settings.API_V1_STR}/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
