from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from typing import List, Optional
from common.models import UserCreate, UserUpdate, UserInDB
from .security import get_password_hash

USER_COLLECTION = "users"

async def get_user_by_email(db: AsyncIOMotorDatabase, email: str) -> Optional[UserInDB]:
    user_doc = await db[USER_COLLECTION].find_one({"email": email})
    return UserInDB(**user_doc) if user_doc else None

async def get_user_by_id(db: AsyncIOMotorDatabase, user_id: str) -> Optional[UserInDB]:
    if not ObjectId.is_valid(user_id): return None
    user_doc = await db[USER_COLLECTION].find_one({"_id": ObjectId(user_id)})
    return UserInDB(**user_doc) if user_doc else None

async def create_user(db: AsyncIOMotorDatabase, user_in: UserCreate) -> UserInDB:
    hashed_password = get_password_hash(user_in.password)
    db_user = UserInDB(email=user_in.email, full_name=user_in.full_name, hashed_password=hashed_password)
    user_doc = db_user.model_dump(by_alias=True)
    result = await db[USER_COLLECTION].insert_one(user_doc)
    created_doc = await db[USER_COLLECTION].find_one({"_id": result.inserted_id})
    return UserInDB(**created_doc)

async def update_user(db: AsyncIOMotorDatabase, user_id: str, user_in: UserUpdate) -> Optional[UserInDB]:
    update_data = user_in.model_dump(exclude_unset=True)
    if "password" in update_data and update_data["password"]:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    if not update_data: return await get_user_by_id(db, user_id)
    doc = await db[USER_COLLECTION].find_one_and_update({"_id": ObjectId(user_id)}, {"$set": update_data}, return_document=True)
    return UserInDB(**doc) if doc else None

async def get_all_users(db: AsyncIOMotorDatabase, skip: int = 0, limit: int = 100) -> List[UserInDB]:
    docs = await db[USER_COLLECTION].find().skip(skip).limit(limit).to_list(length=limit)
    return [UserInDB(**doc) for doc in docs]