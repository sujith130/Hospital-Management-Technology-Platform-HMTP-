import pytest
import asyncio
from typing import Generator, AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.base import Base
from app.core.config import settings

# Import all models to ensure they are registered for Base.metadata.create_all
from app.auth.models import User
from app.patients.models import Patient
from app.doctors.models import Doctor
from app.appointments.models import Appointment
from app.audit.models import AuditLog
from app.labs.models import LabTest
from app.procedures.models import Procedure
from app.pharmacy.models import Medicine, Prescription
from app.billing.models import Invoice, Payment

# Test database URL (local SQLite for tests)
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(TEST_DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

@pytest.fixture(scope="session")
def anyio_backend():
    return 'asyncio'

@pytest.fixture(scope="session", autouse=True)
async def setup_test_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncSessionLocal() as session:
        async def override_get_db():
            return session
        
        from app.core.database import get_db as core_get_db
        from app.auth.deps import get_db as auth_get_db
        
        app.dependency_overrides[core_get_db] = override_get_db
        app.dependency_overrides[auth_get_db] = override_get_db
        
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            yield ac
        
        app.dependency_overrides.clear()
