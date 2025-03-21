from fastapi import APIRouter
from database import users_collection
from models import User
from utils import hash_password

router = APIRouter()

# criacao de user

@router.post("/")
async def create_user(user: User):
    hashed_password = hash_password(user.password)
    user_data = {"username": user.username, "hashed_password": hashed_password}
    result = await users_collection.insert_one(user_data)
    return {"id": str(result.inserted_id), "username": user.username}

# lista de users

@router.get("/list")
async def list_users(page: int = 1, page_size: int = 10):
    users = await users_collection.find().skip((page - 1) * page_size). limit(page_size). to_list(length=page_size)
    return users



