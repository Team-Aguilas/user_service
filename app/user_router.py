from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from motor.motor_asyncio import AsyncIOMotorDatabase
from .dependencies import get_db, get_current_active_superuser, get_current_active_user
from common.models import UserCreate, UserRead, UserUpdate, UserInDB
from . import user_service

router = APIRouter()

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_new_user(user_in: UserCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    if await user_service.get_user_by_email(db, email=user_in.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ya existe un usuario con este email.")
    return await user_service.create_user(db, user_in=user_in)

@router.get("/", response_model=List[UserRead], dependencies=[Depends(get_current_active_superuser)])
async def read_all_users(skip: int = 0, limit: int = 100, db: AsyncIOMotorDatabase = Depends(get_db)):
    return await user_service.get_all_users(db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=UserRead)
async def read_user_by_id(user_id: str, db: AsyncIOMotorDatabase = Depends(get_db), current_user: UserInDB = Depends(get_current_active_user)):
    if str(current_user.id) != user_id and not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No autorizado para ver este usuario")
    user = await user_service.get_user_by_id(db, user_id=user_id)
    if not user: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return user

@router.put("/{user_id}", response_model=UserRead)
async def update_existing_user(user_id: str, user_in: UserUpdate, db: AsyncIOMotorDatabase = Depends(get_db), current_user: UserInDB = Depends(get_current_active_user)):
    if str(current_user.id) != user_id and not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No autorizado para actualizar este usuario")
    if not await user_service.get_user_by_id(db, user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado para actualizar")
    return await user_service.update_user(db, user_id=user_id, user_in=user_in)