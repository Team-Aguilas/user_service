from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorClient
from typing import Optional
from .config import settings
from common.models import UserInDB
from .security import decode_access_token
from . import user_service

mongo_client: Optional[AsyncIOMotorClient] = None
database_instance: Optional[AsyncIOMotorDatabase] = None

async def get_db() -> AsyncIOMotorDatabase:
    if database_instance is None: raise HTTPException(status_code=503, detail="La base de datos no está disponible.")
    return database_instance

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(db: AsyncIOMotorDatabase = Depends(get_db), token: str = Depends(oauth2_scheme)) -> UserInDB:
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No se pudieron validar las credenciales", headers={"WWW-Authenticate": "Bearer"})
    payload = decode_access_token(token)
    if payload is None or payload.get("sub") is None: raise credentials_exception
    user_id: str = payload.get("sub")
    user = await user_service.get_user_by_id(db, user_id=user_id)
    if user is None: raise credentials_exception
    return user

async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)) -> UserInDB:
    if not current_user.is_active: raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario inactivo")
    return current_user

async def get_current_active_superuser(current_user: UserInDB = Depends(get_current_active_user)) -> UserInDB:
    if not current_user.is_superuser: raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="El usuario no tiene suficientes privilegios")
    return current_user