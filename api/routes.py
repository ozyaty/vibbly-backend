from fastapi import APIRouter
from pydantic import BaseModel

class TelegramAuth(BaseModel):
    query_id: str
    user: str  # stringified user object
    auth_date: str
    hash: str

@router.post("/auth")
async def authenticate_user(data: TelegramAuth):
    try:
        payload = data.dict()
        user_data = verify_telegram_auth(payload)
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

