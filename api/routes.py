from fastapi import APIRouter, Request
from pydantic import BaseModel
from api.auth import check_telegram_auth

router = APIRouter()

# Telegram authentication route
@router.get("/auth")
async def authenticate_user(request: Request):
    init_data = request.query_params.get("initData")
    if not init_data:
        return {"error": "Missing initData"}

    try:
        user_data = check_telegram_auth(init_data)
        return {"success": True, "user": user_data}
    except Exception as e:
        return {"success": False, "error": str(e)}

# Sample feed route
@router.get("/feed")
async def get_feed():
    return {"feed": []}

# User registration route
class User(BaseModel):
    username: str
    password: str

@router.post("/register")
def register(user: User):
    print(f"Received registration for: {user.username}")
    return {"message": f"User {user.username} registered successfully"}

