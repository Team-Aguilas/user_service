# app/services/user_service.py
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from typing import List, Optional

from app.models import UserCreate, UserUpdate, UserInDB
from app.security import get_password_hash

USER_COLLECTION = "users"

async def get_user_by_email(db: AsyncIOMotorDatabase, email: str) -> Optional[UserInDB]:
    """Obtiene un usuario por su email."""
    user_doc = await db[USER_COLLECTION].find_one({"email": email})
    if user_doc:
        return UserInDB(**user_doc)
    return None

async def get_user_by_id(db: AsyncIOMotorDatabase, user_id: str) -> Optional[UserInDB]:
    """Obtiene un usuario por su ID."""
    if not ObjectId.is_valid(user_id):
        return None
    user_doc = await db[USER_COLLECTION].find_one({"_id": ObjectId(user_id)})
    if user_doc:
        return UserInDB(**user_doc)
    return None

async def create_user(db: AsyncIOMotorDatabase, user_in: UserCreate) -> UserInDB:
    """Crea un nuevo usuario."""
    hashed_password = get_password_hash(user_in.password)
    db_user = UserInDB(
        email=user_in.email,
        full_name=user_in.full_name,
        hashed_password=hashed_password
    )
    user_doc_to_insert = db_user.model_dump(by_alias=True, exclude_none=True)
    
    result = await db[USER_COLLECTION].insert_one(user_doc_to_insert)
    created_doc = await db[USER_COLLECTION].find_one({"_id": result.inserted_id})
    if not created_doc:
        raise Exception("No se pudo crear el usuario después de la inserción.")
    return UserInDB(**created_doc)

async def update_user(db: AsyncIOMotorDatabase, user_id: str, user_in: UserUpdate) -> Optional[UserInDB]:
    """Actualiza un usuario existente."""
    update_data = user_in.model_dump(exclude_unset=True)
    if "password" in update_data and update_data["password"]:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    
    if not update_data:
        return await get_user_by_id(db, user_id)

    updated_user_doc = await db[USER_COLLECTION].find_one_and_update(
        {"_id": ObjectId(user_id)},
        {"$set": update_data},
        return_document=True 
    )
    if updated_user_doc:
        return UserInDB(**updated_user_doc)
    return None

async def get_all_users(db: AsyncIOMotorDatabase, skip: int = 0, limit: int = 100) -> List[UserInDB]:
    """Obtiene una lista de todos los usuarios."""
    users_cursor = db[USER_COLLECTION].find().skip(skip).limit(limit)
    user_docs = await users_cursor.to_list(length=limit)
    return [UserInDB(**doc) for doc in user_docs]