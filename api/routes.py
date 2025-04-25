from fastapi import APIRouter, Request
from pydantic import BaseModel
from .auth import check_telegram_auth

router = APIRouter()

# In-memory users store (for now—replace with a real DB later)
USERS = {}

@router.get("/auth")
async def authenticate_user(request: Request):
    init_data = request.query_params.get("initData")
    if not init_data:
        return {"success": False, "error": "Missing initData"}
    try:
        # Verify Telegram signature and parse user data
        user_data = check_telegram_auth(init_data)
        telegram_id = user_data["id"]

        # Auto-register if new
        if telegram_id not in USERS:
            USERS[telegram_id] = {
                "id": telegram_id,
                "first_name": user_data.get("first_name", ""),
                "username": user_data.get("username", "")
            }

        # Return the stored user record
        return {"success": True, "user": USERS[telegram_id]}

    except Exception as e:
        return {"success": False, "error": str(e)}

@router.get("/feed")
async def get_feed():
    # Placeholder feed: replace with real posts later
    return {"feed": []}

# (Optional) Keep your manual register endpoint if you like:
class User(BaseModel):
    username: str
    password: str

@router.post("/register")
def register(user: User):
    print(f"Received registration for: {user.username}")
    return {"message": f"User {user.username} registered successfully"}
