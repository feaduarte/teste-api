from fastapi import APIRouter
from database import users_collection
from models import User
from utils import hash_password

router = APIRouter()

@router.post("/")
async def create_user(user: User):
    hashed_password = hash_password(user.password)
    user_data = {"username": user.username, "hashed_password": hashed_password}
    result = await users_collection.insert_one(user_data)
    return {"id": str(result.inserted_id), "username": user.username}
