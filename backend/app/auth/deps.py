from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from app.core import database, config
from app.auth import models, schemas, security

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{config.settings.API_V1_STR}/auth/login")

from app.core.database import get_db

async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config.settings.SECRET_KEY, algorithms=[config.settings.ALGORITHM])
        email: str = payload.get("sub")
        hospital_id: str = payload.get("hospital_id")
        if email is None or hospital_id is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    from sqlalchemy import select
    result = await db.execute(
        select(models.User)
        .filter(models.User.email == token_data.email)
        .filter(models.User.hospital_id == hospital_id)
    )
    user = result.scalars().first()
    
    if user is None:
        raise credentials_exception
    return user

async def get_hospital_id(current_user: models.User = Depends(get_current_user)) -> str:
    return current_user.hospital_id
