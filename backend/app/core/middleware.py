import contextvars
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from jose import jwt, JWTError
from app.core.config import settings

# Context variable to store hospital_id for the current request
hospital_context: contextvars.ContextVar[str] = contextvars.ContextVar("hospital_id", default="")

class MultiTenantMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Exclude public paths from tenancy enforcement
        public_paths = [
            "/",
            "/health",
            f"{settings.API_V1_STR}/auth/login",
            f"{settings.API_V1_STR}/auth/register",
            f"{settings.API_V1_STR}/docs",
            f"{settings.API_V1_STR}/redoc",
            f"{settings.API_V1_STR}/openapi.json",
        ]
        
        if request.url.path in public_paths or request.method == "OPTIONS":
            return await call_next(request)

        # Extract token from Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            # We don't raise 401 here to let FastAPI dependency injection handle it if needed
            # but we also don't set the context
            return await call_next(request)

        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            hospital_id = payload.get("hospital_id")
            if hospital_id:
                token = hospital_context.set(str(hospital_id))
                try:
                    response = await call_next(request)
                finally:
                    hospital_context.reset(token)
                return response
        except (JWTError, Exception):
            # If token is invalid, let the auth dependency handle the error
            pass

        return await call_next(request)

def get_current_hospital_id() -> str:
    """Helper to get the hospital_id from context."""
    return hospital_context.get()
