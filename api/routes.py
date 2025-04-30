from fastapi import APIRouter
from pydantic import BaseModel
from .auth import verify_telegram_auth

router = APIRouter()

USERS = {}

class TelegramInit(BaseModel):
    query_id: str
    user: dict
    auth_date: str
    hash: str

@router.post("/auth")
async def authenticate_user(data: TelegramInit):
    try:
        user_data = verify_telegram_auth(data)
        telegram_id = user_data["id"]

        if telegram_id not in USERS:
            USERS[telegram_id] = {
                "id": telegram_id,
                "first_name": user_data.get("first_name", ""),
                "username": user_data.get("username", "")
            }

        return {"success": True, "user": USERS[telegram_id]}
    except Exception as e:
        return {"success": False, "error": f"Hash validation error: {str(e)}"}
