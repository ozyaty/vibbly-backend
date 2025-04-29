from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()  # ✅ This was missing

USERS_DB = {}

class UserCreate(BaseModel):
    username: str
    full_name: str
    avatar_url: str

@router.post("/users/register")
async def register_user(user: UserCreate):
    if user.username in USERS_DB:
        return {"success": False, "error": "Username already exists"}

    USERS_DB[user.username] = {
        "full_name": user.full_name,
        "avatar_url": user.avatar_url
    }
    return {"success": True, "user": USERS_DB[user.username]}

@router.get("/users/me/{username}")
async def get_user(username: str):
    user = USERS_DB.get(username)
    if not user:
        return {"success": False, "error": "User not found"}
    return {"success": True, "user": user}
