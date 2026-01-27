import asyncio
import pytest
from tests.conftest import client, db, setup_test_db
from tests.test_auth import test_register_user
import httpx

async def run_debug():
    try:
        # Manually trigger setup
        from tests.conftest import AsyncSessionLocal, engine
        from app.core.base import Base
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        async with AsyncSessionLocal() as session:
            # Manual client setup
            from app.main import app
            from app.core.database import get_db
            
            async def override_get_db():
                yield session
            
            app.dependency_overrides[get_db] = override_get_db
            
            from httpx import ASGITransport, AsyncClient
            transport = ASGITransport(app=app)
            async with AsyncClient(transport=transport, base_url="http://test") as ac:
                print("Running test...")
                await test_register_user(ac)
                print("Test passed!")
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    import os
    os.environ["PYTHONPATH"] = "."
    asyncio.run(run_debug())
