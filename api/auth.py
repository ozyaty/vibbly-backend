import os
import hmac
import hashlib
from fastapi import HTTPException

# ✅ Load your Bot API token securely from an environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable is not set!")

# ✅ Derive the secret key by taking SHA256 of the Bot token
SECRET_KEY = hashlib.sha256(BOT_TOKEN.encode()).digest()

def check_telegram_auth(init_data: str) -> dict:
    """
    Verify the initData string from Telegram and return user info dict.
    Raises HTTPException(400) if verification fails.
    """
    params = dict(item.split("=", 1) for item in init_data.split("&"))
    received_hash = params.pop("hash", None)
    if not received_hash:
        raise HTTPException(status_code=400, detail="Missing hash")

    data_check_arr = [f"{k}={v}" for k, v in sorted(params.items())]
    data_check_string = "\n".join(data_check_arr)

    computed_hash = hmac.new(SECRET_KEY, data_check_string.encode(), hashlib.sha256).hexdigest()

    if computed_hash != received_hash:
        raise HTTPException(status_code=400, detail="Invalid hash")

    return params
