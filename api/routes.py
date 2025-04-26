from fastapi import APIRouter
from pydantic import BaseModel
from .auth import verify_telegram_auth

router = APIRouter()

USERS = {}

class InitData(BaseModel):
    initData: str

@router.post("/auth")
async def authenticate_user(data: InitData):
    try:
        user_data = verify_telegram_auth(data.initData)
        telegram_id = user_data["id"]

        if telegram_id not in USERS:
            USERS[telegram_id] = {
                "id": telegram_id,
                "first_name": user_data.get("first_name", ""),
                "username": user_data.get("username", "")
            }

        return {"success": True, "user": USERS[telegram_id]}
    except Exception as e:
        return {"success": False, "error": f"400: Hash validation error: {str(e)}"}

@router.get("/feed")
async def get_feed():
    return {"feed": []}

class User(BaseModel):
    username: str
    password: str

@router.post("/register")
def register(user: User):
    print(f"Received registration for: {user.username}")
    return {"message": f"User {user.username} registered successfully"}
